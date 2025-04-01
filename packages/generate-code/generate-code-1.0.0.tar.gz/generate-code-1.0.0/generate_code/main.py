import argparse
from jinja2 import Environment, FileSystemLoader
from sqlalchemy import create_engine, MetaData
import os
from datetime import datetime
import shutil
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
import sys

def main():

    # 解析命令行参数
    parser = argparse.ArgumentParser(description="Java 代码生成器")
    parser.add_argument("--db", type=str, required=True, help="数据库连接字符串，例如：mysql+pymysql://root:password@localhost:3306/test_db")
    parser.add_argument("--table", type=str, help="指定要生成的表名，多个表用逗号分隔（默认全部表）", default="all")
    parser.add_argument("--project-path", type=str, help="指定 IDEA 项目路径（代码将直接生成到 src/main/java）")
    try:
        args = parser.parse_args()
    except SystemExit:
        # 捕获 SystemExit 异常，输出自定义错误信息
        print("❌ 错误: --db 参数是必填项！")
        print("使用示例: generate-code --db root:password@localhost:3306/test_db")
        sys.exit(1)  # 确保程序退出

    # 如果参数解析成功，可以继续执行后续逻辑
    print(f"数据库连接: {args.db}")

    # 连接数据库
    try:
        engine = create_engine("mysql+pymysql://" + args.db)
        metadata = MetaData()
        metadata.reflect(bind=engine)
        if not metadata.tables:
            print("❌ 未找到表！请确认数据库是否存在且包含表。")
            exit(1)
    except OperationalError as e:
        print(f"❌ 数据库连接失败或数据库不存在!")
        exit(1)

    # 获取当前脚本所在目录的上一级目录（项目根目录）
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 指定模板路径
    TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

    # 配置 Jinja2
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

    # 代码输出目录
    if args.project_path is None:
        base_output_dir = os.path.abspath("../../generated")  # 默认使用当前目录
    else:
        base_output_dir = os.path.join(args.project_path, "src/main/java/com/softding/tms")

    # 确保目录存在
    os.makedirs(base_output_dir, exist_ok=True)

    # 数据库类型转换（MySQL -> Java）
    type_mapping = {
        "VARCHAR": "String",
        "TEXT": "String",
        "INT": "Integer",
        "BIGINT": "Long",
        "DECIMAL": "BigDecimal",
        "DATETIME": "LocalDateTime",
        "TINYINT": "Boolean"  # 布尔类型转换
    }


    # 获取注解的函数
    def get_annotation_for_field(field_name):
        if field_name.lower() == "user_id":
            return "@TableId(type = IdType.ASSIGN_ID)"
        elif field_name.lower() == "deleted":
            return "@TableLogic"
        elif field_name.lower() == "created_by_id":
            return "@CreatedById"
        elif field_name.lower() == "created_by":
            return "@CreatedBy"
        elif field_name.lower() == "created_time":
            return "@CreatedDate"
        elif field_name.lower() == "updated_by_id":
            return "@LastModifiedById"
        elif field_name.lower() == "updated_by":
            return "@LastModifiedBy"
        elif field_name.lower() == "updated_time":
            return "@LastModifiedDate"
        else:
            return ""  # 对于没有特殊注解的字段，返回空字符串


    # 转换字段为驼峰格式
    def to_camel_case(name):
        parts = name.split("_")
        return parts[0].lower() + ''.join([part.capitalize() for part in parts[1:]])


    # 获取表描述
    def get_table_comment(table_name):
        query = text(f"SELECT TABLE_COMMENT FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'")
        with engine.connect() as connection:
            result = connection.execute(query).fetchone()
        return result[0] if result and result[0] else table_name  # 如果没有描述，则返回表名

    # 新增方法：将 sys_user 转换为 sys-user
    def to_dash_case(name):
        return name.replace("_", "-")

    # 将 sys_user 转换为 sysUser
    def to_lower_camel_case(name):
        parts = name.split("_")
        return parts[0].lower() + ''.join([part.capitalize() for part in parts[1:]])

    # 生成 Entity, DTO, VO 和 Controller, Service 代码的函数
    def generate_code(table_name, columns, primary_key_column):
        global max_length
        class_name = "".join([word.capitalize() for word in table_name.split("_")])

        fields = []
        for col in columns:
            # 强制将 "deleted" 字段转换为 Boolean 类型
            if col.name.lower() == "deleted":
                field_type = "Boolean"
            else:
                field_type = type_mapping.get(str(col.type).upper(), "String")

                # 获取字段长度（仅针对 String 类型）
                max_length = getattr(col.type, "length", None) if field_type == "String" else None
            field = {
                "name": to_camel_case(col.name),  # 转换为驼峰格式
                "type": field_type,
                "description": col.comment if col.comment else "无描述",  # 获取字段描述，若无则填“无描述”
                "is_primary": col.name == primary_key_column,  # 判断是否是主键
                "annotation": get_annotation_for_field(col.name),  # 获取字段注解
                "is_long": field_type == "Long",  # 判断是否是 Long 类型
                "max_length": max_length  # 记录字段的最大长度（如果有的话）
            }
            fields.append(field)

        table_name_dash = to_dash_case(table_name)  # 转换 sys_user -> sys-user
        table_description = get_table_comment(table_name)  # 获取表描述
        table_name_camel = to_lower_camel_case(table_name)  # 转换 sys_user -> sysUser

        # 渲染 Entity 模板
        entity_template = env.get_template("entity_template.jinja2")
        entity_code = entity_template.render(
            class_name=class_name,
            table_name=table_name,
            author="骆吉振",  # 可以动态传入
            date=datetime.now().strftime("%Y/%m/%d"),  # 当前日期
            fields=fields  # 渲染字段信息
        )

        # 渲染 DTO 模板
        dto_template = env.get_template("dto_template.jinja2")
        dto_code = dto_template.render(
            class_name=class_name,
            author="骆吉振",  # 可以动态传入
            date=datetime.now().strftime("%Y/%m/%d"),  # 当前日期
            fields=fields  # DTO 使用相同的字段
        )

        # 渲染 VO 模板
        vo_template = env.get_template("vo_template.jinja2")
        vo_code = vo_template.render(
            class_name=class_name,
            author="骆吉振",  # 可以动态传入
            date=datetime.now().strftime("%Y/%m/%d"),  # 当前日期
            fields=fields  # VO 使用相同的字段
        )

        # 渲染 Controller 模板
        controller_template = env.get_template("controller_template.jinja2")
        controller_code = controller_template.render(
            class_name=class_name,
            table_name=table_description,  # 使用表描述代替表名
            urlName= table_name_dash, # 传递 sys-user 形式的表名
            table_name_camel=table_name_camel, # 传递 sysUser 形式的表名
            author="骆吉振",  # 可以动态传入
            date=datetime.now().strftime("%Y/%m/%d")  # 当前日期
        )

        # 渲染 Service 模板
        service_template = env.get_template("service_template.jinja2")
        service_code = service_template.render(
            class_name=class_name,
            table_name=table_description,  # 使用表描述代替表名
            urlName= table_name_dash, # 传递 sys-user 形式的表名
            table_name_camel=table_name_camel, # 传递 sysUser 形式的表名
            author="骆吉振",  # 可以动态传入
            date=datetime.now().strftime("%Y/%m/%d")  # 当前日期
        )

        # 渲染 Mapper 模板
        mapper_template = env.get_template("mapper_template.jinja2")
        mapper_code = mapper_template.render(
            class_name=class_name,
            table_name=table_description,  # 使用表描述代替表名
            urlName=table_name_dash,  # 传递 sys-user 形式的表名
            table_name_camel=table_name_camel,  # 传递 sysUser 形式的表名
            author="骆吉振",  # 可以动态传入
            date=datetime.now().strftime("%Y/%m/%d")  # 当前日期
        )

        # 确保文件夹存在
        os.makedirs("generated/domain/entity", exist_ok=True)
        os.makedirs("generated/domain/dto", exist_ok=True)
        os.makedirs("generated/domain/vo", exist_ok=True)
        os.makedirs("generated/controller", exist_ok=True)
        os.makedirs("generated/service", exist_ok=True)
        os.makedirs("generated/mapper", exist_ok=True)

        # 写入 Entity 类 Java 文件，文件名是表名的驼峰格式
        with open(f"generated/domain/entity/{class_name}.java", "w") as f:
            f.write(entity_code)

        # 写入 DTO 类 Java 文件，文件名是表名的驼峰格式
        with open(f"generated/domain/dto/{class_name}DTO.java", "w") as f:
            f.write(dto_code)

        # 写入 VO 类 Java 文件，文件名是表名的驼峰格式
        with open(f"generated/domain/vo/{class_name}VO.java", "w") as f:
            f.write(vo_code)

        # 写入 Controller 类 Java 文件，文件名是表名的驼峰格式
        with open(f"generated/controller/{class_name}Controller.java", "w") as f:
            f.write(controller_code)

        # 写入 Service 类 Java 文件，文件名是表名的驼峰格式
        with open(f"generated/service/{class_name}Service.java", "w") as f:
            f.write(service_code)

        # 写入 Mapper 类 Java 文件
        with open(f"generated/mapper/{class_name}Mapper.java", "w") as f:
            f.write(mapper_code)

    # 遍历表，生成代码
    if args.table.lower() == "all":
        for table_name, table in metadata.tables.items():
            generate_code(table_name, table.columns, table.primary_key.columns.keys())
    else:
        table_names = args.table.split(",")  # 支持多个表名
        for table_name in table_names:
            table_name = table_name.strip()
            if table_name in metadata.tables:
                table = metadata.tables[table_name]
                generate_code(table_name, table.columns, table.primary_key.columns.keys())
            else:
                print(f"⚠️  表 {table_name} 不存在！")

    print("✅ Java 代码生成完毕！")

    # 目标目录映射
    target_dirs = {
        "domain/entity": "domain/entity/",
        "domain/dto": "domain/dto/",
        "domain/vo": "domain/vo/",
        "controller": "controller/",
        "service": "service/",
        "mapper": "mapper/"
    }

    # 遍历生成的 Java 代码并复制到 IDEA 项目
    for folder, target in target_dirs.items():
        src_path = f"generated/{folder}/"
        dest_path = os.path.join(base_output_dir, target)

        if os.path.exists(src_path):
            os.makedirs(dest_path, exist_ok=True)
            for file in os.listdir(src_path):
                if file.endswith(".java"):
                    # 只把 Controller 和 Service 文件放入正确的文件夹
                    if "Controller" in file and folder != "controller":
                        continue
                    elif "Service" in file and folder != "service":
                        continue
                    if os.path.abspath(src_path) == os.path.abspath(dest_path):
                        continue
                    shutil.copy(os.path.join(src_path, file), dest_path)

    print(f"🚀 Java 代码已存放到   {base_output_dir} 目录下 赶快去看看吧！✈️")
if __name__ == "__main__":
    main()