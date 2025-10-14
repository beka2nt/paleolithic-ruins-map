# 中国旧石器时代遗址分布图项目部署指南

本文档指导你如何在新的计算机上设置和运行“中国旧石器时代遗址分布图”项目。
本项目使用 Django 框架，并依赖 PostgreSQL、PostGIS 和 GDAL 等地理空间处理相关的库。

## 一、 系统和软件

### 1. 操作系统
* 本项目理论上可以在 Windows,  Linux 系统上运行。

### 2. Python
* **Python 版本**: 3.11.3 
    * 请从 [Python 官网](https://www.python.org/downloads/) 下载并安装。
    * 安装时，请确保勾选 "Add Python to PATH" (将 Python 添加到系统环境变量) 选项。

### 3. PostgreSQL 数据库
* **PostgreSQL 版本**: 推荐 12.x 或更高版本。
    * 请从 [PostgreSQL 官网](https://www.postgresql.org/download/) 下载并安装适合你操作系统的版本。
    * 安装过程中，你会设置一个超级用户（通常是 `postgres`）的密码，请务必记住此密码。

### 4. PostGIS 扩展
* PostGIS 是 PostgreSQL 的地理空间数据处理扩展。
    * **Windows**: 通常在安装 PostgreSQL 后，可以通过其附带的 **Stack Builder** (应用程序栈构建器) 工具来搜索并安装 PostGIS。请选择与你 PostgreSQL 版本兼容的 PostGIS 版本。

### 5. GDAL (Geospatial Data Abstraction Library)
* GDAL 是 Django 的 GeoDjango 模块处理地理空间数据所必需的底层库。
    * **Windows**: 使用 **OSGeo4W 安装程序** ([OSGeo4W 官网](https://trac.osgeo.org/osgeo4w/))。
        1.  下载并运行 OSGeo4W 安装程序。
        2.  选择 "Advanced Install" (高级安装)。
        3.  在包选择阶段，确保选中与 Python 版本和架构（通常是64位）兼容的 `gdal` 包 (例如 `gdal-python` 或核心 `gdal` 组件)。本项目开发时使用的是 GDAL 3.1.0 对应的 DLL (`gdal310.dll`)。
        4.  安装完成后，需要配置环境变量：
            * 将 OSGeo4W 的 `bin` 目录 (例如 `C:\OSGeo4W\bin`) 添加到系统 `PATH`。
            * 设置 `GDAL_DATA` 环境变量，指向 OSGeo4W 安装目录下的 `share\gdal` 文件夹 (例如 `C:\OSGeo4W\share\gdal`)。
            * 设置 `PROJ_LIB` 环境变量，指向 OSGeo4W 安装目录下的 `share\proj` 文件夹 (例如 `C:\OSGeo4W\share\proj`)。
            * (或者，也可以像项目 `settings.py` 中那样，通过代码指定 GDAL 相关的 DLL 路径，但这要求路径固定。)

## 二、 项目代码和依赖安装

1.  **获取项目代码**：
    * 将整个项目文件夹 (`RuinsProject`) 复制到新计算机的目标位置。

2.  **创建并激活 Python 虚拟环境**：
    * 打开命令行工具（Windows上是 CMD 或 PowerShell，Linux/macOS上是终端）。
    
    * 导航到复制的项目根目录 (`RuinsProject`)。
    
    * 创建虚拟环境 (推荐命名为 `venv`):
        ```bash
        python -m venv venv
        ```
        
    * 激活虚拟环境：
        * Windows CMD: `venv\Scripts\activate`
        * Windows PowerShell: `venv\Scripts\Activate.ps1`
            * (如果 PowerShell 提示禁止运行脚本，请先在该 PowerShell 窗口中运行：`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`，然后按 `Y` 确认，再重新运行激活命令。)
        
    * 激活成功后，命令行提示符前应出现 `(venv)` 字样。
    
3.  **安装 Python 依赖包**：
    * 确保 `requirements.txt` 文件位于项目根目录下。
    * 在已激活的虚拟环境中，运行：
        ```bash
        pip install -r requirements.txt
        ```
        这将安装 Django、Django REST framework、psycopg2-binary、djangorestframework-gis 等所有必要的 Python 包。
        * **注意**：`djangorestframework-gis` 的安装有时比较棘手。如果遇到 `ModuleNotFoundError` (例如关于 `filters` 或 `serializers`，因为本项目使用的备选 `views.py` 依赖它们)，请确保此包至少部分核心文件已正确安装。

## 三、 数据库配置与数据恢复

1.  **在 PostgreSQL 中创建数据库和用户**：
    * 打开 `psql` (PostgreSQL 的命令行工具) 或使用 pgAdmin 等图形化工具。
    * 以 PostgreSQL 超级用户（例如 `postgres`）身份登录。
    * 创建项目所需的数据库（例如 `ruins_db`）：
        ```sql
        CREATE DATABASE ruins_db ENCODING 'UTF8'; 
        ```
    * (可选，但推荐) 创建一个专用的数据库用户并授予权限：
        ```sql
        CREATE USER <你的数据库用户名> WITH PASSWORD '<你的密码>';
        GRANT ALL PRIVILEGES ON DATABASE ruins_db TO <你的数据库用户名>;
        ALTER DATABASE ruins_db OWNER TO <你的数据库用户名>; 
        ```
        如果你选择使用默认的 `postgres` 用户，可以跳过此步骤中创建新用户的部分，但在 `settings.py` 中需要使用 `postgres` 及其密码。本项目开发时数据库用户是 `postgres`，密码是 `123456`。

2.  **为数据库启用 PostGIS 扩展**：
    * 连接到你刚创建的 `ruins_db` 数据库：
        ```sql
        \c ruins_db 
        ```
    * 执行以下命令启用 PostGIS：
        ```sql
        CREATE EXTENSION postgis;
        ```
    * 如果提示已存在，则无需重复操作。

3.  **恢复数据库备份**：
    * 本项目文件夹内已有一个 `ruins_db_backup.tar` 备份文件。将此文件复制到新计算机上一个方便访问的位置。
    * 打开命令行工具，使用 `pg_restore` 命令来恢复数据。请根据你 PostgreSQL 的用户和数据库名进行调整：
        ```bash
        pg_restore -U postgres -d ruins_db -W ruins_db_backup.tar
        ```
        * `-U postgres`: 指定 PostgreSQL 用户为 `postgres`。
        * `-d ruins_db`: 指定要恢复到的数据库名称。
        * `-W`: 会提示你输入 `postgres` 用户的密码。
        * `ruins_db_backup.tar`: 指向备份文件路径。
    * 输入密码后，数据将被导入。

## 四、 配置 Django 项目

1.  **修改 `settings.py` 文件**：
    * 打开项目中的 `main_project/settings.py` 文件。
    * **`DATABASES` 设置**：
        * 确保 `ENGINE` 是 `django.contrib.gis.db.backends.postgis`。
        * 根据你在新电脑上 PostgreSQL 的实际配置，修改（或确保环境变量能正确提供）`NAME`, `USER`, `PASSWORD`, `HOST`, `PORT` 的值。
            * `HOST`: 如果 PostgreSQL 和 Django 在同一台机器，通常是 `'localhost'`。
            * `PORT`: 原生 PostgreSQL 默认是 `'5432'`。
            * `NAME`, `USER`, `PASSWORD`: 必须与你在第 三.1 步中创建或使用的数据库、用户及密码一致。
    * **`SECRET_KEY`**: 确保存在一个有效的密钥。
    * **`DEBUG`**: 建议在非开发调试时设为 `False`。
    * **`ALLOWED_HOSTS`**: 如果 `DEBUG = False`，则必须将新电脑的 IP 地址或你计划用来访问应用的主机名添加到此列表中。例如：`ALLOWED_HOSTS = ['192.168.1.100', 'localhost', '127.0.0.1']`。
    * **GDAL/GEOS 路径** (如果环境变量未全局设置或 GeoDjango 找不到)：
        `settings.py` 中 `if os.name == 'nt':` 的部分是针对 Windows 的。如果你在新电脑是其他操作系统，且 GDAL 未能被自动找到，你可能需要参照该逻辑，为新系统添加类似的路径指定（或确保环境变量已正确配置，这是更推荐的做法）。

2.  **运行 Django 数据库迁移**：
    * 即使你恢复了数据库备份，也建议运行一次 `migrate` 命令。这能确保 Django 的迁移状态表与数据库结构一致，并应用任何可能在备份之后但在代码中存在的新迁移（尽管对于完整备份恢复，通常不会有新的结构迁移）。
    * 在激活的虚拟环境中，项目根目录下运行：
        ```bash
        python manage.py migrate
        ```

3.  **创建超级用户（如果需要）**：
    * 如果数据库恢复没有包含你想用的管理员账户，或者你想为新环境创建一个，请运行：
        ```bash
        python manage.py createsuperuser
        ```
    * 按照提示设置用户名、邮箱（可选）和密码。

## 五、 运行项目

1.  **启动 Django 开发服务器**：
    在激活的虚拟环境中，项目根目录下运行：
    ```bash
    python manage.py runserver
    ```
    
2.  **访问应用**：
    * **前端地图页面**：在浏览器中打开 `http://localhost:8000/` (或 `http://<新电脑的IP地址>:8000/`)。
    * **Admin 后台**：访问 `http://localhost:8000/admin/` (或 `http://<新电脑的IP地址>:8000/admin/`)。

