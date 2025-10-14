# 中国旧石器时代遗址可视化平台 - 本地部署与开发指南

## 1. 项目概述

本项目是一个基于 Django 和 GeoDjango 构建的交互式 Web 应用，旨在通过地理信息系统（GIS）技术，可视化地展示、查询和管理中国旧石器时代的考古遗址数据。项目后端提供 REST API 接口，前端通过 Leaflet.js 渲染地理数据。

## 2. 核心技术栈

* **后端**: Python (3.11+), Django (4.2+), GeoDjango, Django REST Framework
* **数据库**: PostgreSQL (14+) with PostGIS (3+)
* **前端**: HTML, CSS, JavaScript, Leaflet.js, Bootstrap 5
* **地理空间库 (C/C++ Libs)**: GDAL, PROJ, GEOS

---

## 3. 本地环境搭建 (Windows)

在开始项目设置之前，必须在本地计算机上安装并配置好以下软件。**这是项目成功运行的关键，请严格按照步骤操作。**

### 3.1. 安装 Python

* **推荐版本**: Python 3.11.x
* **下载地址**: [https://www.python.org/downloads/](https://www.python.org/downloads/)
* **安装注意**: 在安装过程中，务必勾选 **"Add Python to PATH"** 选项。

### 3.2. 安装 PostgreSQL 与 PostGIS

* **推荐版本**: PostgreSQL 14 或 15
* **安装指南**:
    1.  从 [PostgreSQL 官网](https://www.postgresql.org/download/) 下载并安装。
    2.  安装过程中，请设置并**记录**超级用户（默认为 `postgres`）的密码。
    3.  安装完成后，启动 **Stack Builder** 工具。
    4.  在 Stack Builder 中，选择 `Spatial Extensions` -> `PostGIS`，安装与 PostgreSQL 版本兼容的最新版 PostGIS 扩展。

### 3.3. 安装 GDAL/PROJ/GEOS (核心 C/C++ 库)

GeoDjango 依赖这些底层的地理空间处理库。在 Windows 上，推荐使用 **OSGeo4W** 进行安装。

* **安装工具**: [OSGeo4W 网络安装程序](https://trac.osgeo.org/osgeo4w/)
* **安装步骤**:
    1.  运行安装程序，选择 **"Advanced Install"** (高级安装)。
    2.  在包选择（Select Packages）阶段，定位到 `Commandline_Utilities` 分类。
    3.  找到 `gdal` 包，点击 "New" 列，选择一个较新的稳定版本（例如 `3.6.x` 或更高）。选择 GDAL 会自动关联并选择兼容的 PROJ 和 GEOS 库。
    4.  完成安装。

### 3.4. 配置环境变量

为保证 GDAL 能被项目正确找到，需要配置系统环境变量。

1.  打开 Windows 的“编辑系统环境变量”。
2.  在“高级”选项卡下，点击“环境变量”。
3.  在“系统变量”中，检查并确保以下变量存在且路径正确（路径以您的 OSGeo4W 安装目录为准）：
    * `GDAL_DATA`: `C:\OSGeo4W\share\gdal`
    * `PROJ_LIB`: `C:\OSGeo4W\share\proj`
        * **【警告】**：请务必检查此路径值前后**不能有任何空格**，否则会导致 `OGR Failure` 错误。
    * `Path`: 确保 `C:\OSGeo4W\bin` 已被包含在 `Path` 变量中。
4.  配置完成后，建议**重启计算机**以使所有环境变量完全生效。

---

## 4. 项目部署步骤

### 4.1. 获取项目代码

通过 `git clone` 或直接复制，将项目文件夹 (`RuinsProject`) 放置到本地工作目录。

### 4.2. 创建并激活 Python 虚拟环境

1.  打开命令行工具（推荐 PowerShell）。
2.  导航至项目根目录 (例如 `D:\project\RuinsProject`)。
3.  创建虚拟环境：
    ```bash
    python -m venv venv
    ```
4.  激活虚拟环境：
    ```powershell
    .\venv\Scripts\Activate.ps1
    # 如果提示脚本执行策略问题，请先运行: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    ```
    激活成功后，命令行提示符前应有 `(venv)` 标识。

### 4.3. 安装 Python 依赖

1.  在激活的虚拟环境中，首先升级 pip：
    ```bash
    python -m pip install --upgrade pip
    ```
2.  安装所有项目依赖：
    ```bash
    pip install -r requirements.txt
    ```
    **注意**: 如果 `requirements.txt` 中的 `GDAL` Python 绑定版本与第 3.3 步中安装的 GDAL C 库版本不兼容，可能会导致错误。请确保两边版本大致匹配。

### 4.4. 数据库设置与数据恢复

1.  打开 `psql` 或 pgAdmin，以 `postgres` 用户身份登录。
2.  创建数据库：
    ```sql
    CREATE DATABASE ruins_db ENCODING 'UTF8';
    ```
3.  连接到新创建的数据库：
    ```sql
    \c ruins_db
    ```
4.  启用 PostGIS 扩展：
    ```sql
    CREATE EXTENSION postgis;
    ```
5.  恢复数据备份：
    * 打开一个新的命令行窗口（**不要**在 `psql` 内部）。
    * 导航到项目根目录。
    * 运行 `psql` 命令导入 `ruins_db_fresh_backup.sql` 文件：
        ```bash
        psql -U postgres -d ruins_db -f ruins_db_fresh_backup.sql
        ```
    * 按提示输入 `postgres` 用户的密码。

### 4.5. Django 项目配置

1.  在项目根目录创建 `.env` 文件。复制以下内容并根据您的本地环境修改密码。
    ```env
    # .env 文件
    DJANGO_SECRET_KEY=a-new-secret-key-should-be-generated-here
    DJANGO_DEBUG=1
    DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1
    
    # -- 本地数据库配置 --
    DATABASE_URL=postgis://postgres:your_password@localhost:5432/ruins_db
    ```
    **请将 `your_password` 替换为您在 3.2 步中为 `postgres` 用户设置的密码。**

2.  运行数据库迁移以同步 Django 状态：
    ```bash
    python manage.py migrate
    ```

3.  创建本地管理员账户：
    ```bash
    python manage.py createsuperuser
    ```

---

## 5. 运行项目

1.  启动 Django 开发服务器：
    ```bash
    python manage.py runserver
    ```
2.  访问应用：
    * **地图主页**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
    * **后台管理**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 6. 项目结构简介

* `main_project/`: Django 项目核心配置目录 (`settings.py`, `urls.py`)。
* `ruins_api/`: 项目核心应用目录，包含了模型、视图、API等。
* `templates/`: 全局 HTML 模板目录。
* `static/`: 全局静态文件目录 (CSS, JS, Images)。
* `mediafiles/`: 用户上传的媒体文件存储目录。
* `manage.py`: Django 项目管理命令行工具。
* `ruins_db_fresh_backup.sql`: 项目的核心数据库备份文件。

## 7. 故障排查

* **`GDALException: OGR failure.`**:
    * 检查 `GDAL_DATA` 和 `PROJ_LIB` 环境变量是否正确设置且无多余空格。
    * 确认安装的 GDAL C 库与 `requirements.txt` 中的 Python GDAL 绑定版本兼容。
* **数据库连接错误 (`psycopg2.OperationalError`)**:
    * 确认 PostgreSQL 服务正在运行。
    * 检查 `.env` 文件中的 `DATABASE_URL` 是否正确，特别是密码、主机(`localhost`)和端口(`5432`)。
