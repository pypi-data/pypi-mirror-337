# generate-code
一个简单的 Java 代码生成器

## 必备安装:

brew install python # 安装Python (Python 3.x.x)

git clone https://github.com/luojizhen99/generate-code.git # 拉取项目

cd java-code-generator # 进入项目

python3 -m venv venv  # 创建虚拟环境

source venv/bin/activate  # macOS执行开启虚拟环境

source venv/Scripts/activate # windows执行开启虚拟环境

pip install -e .  # 以开发模式安装

## 生成代码:
generate-code --db "root:password@localhost:3306/database_name"

必填
--db: 指定需要连接的数据库

选填
--table "table_name"": 可以指定需要成代码的表,也可以是多个用逗号隔开; 如: sys_user,sys_dept (默认扫描全部的表)

选填
--project-path /User/luojizhen/IdeaProjects/test: 可以指定存放代码的目录路径 (默认存放在根目录的generate-code下)
 