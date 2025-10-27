# 中国旧石器时代遗址可视化平台 - 本地部署与开发指南

## 1. 项目概述

本项目是一个基于 Django 和 GeoDjango 构建的交互式 Web 应用，旨在通过地理信息系统（GIS）技术，可视化地展示、查询和管理中国旧石器时代的考古遗址数据。项目后端提供 REST API 接口，前端通过 Leaflet.js 渲染地理数据。

## 2. 核心技术栈

为确保环境一致性，请严格遵守以下推荐的版本：

* **Python 环境**: **Anaconda** (Miniconda 亦可)
* **Python 版本**: **3.11.x**
* **核心框架**: **Django 4.2.x**
* **数据库**: **PostgreSQL 15.x** (或 14、16)
* **数据库插件**: **PostGIS 3.x** (必须与 PostgreSQL 版本兼容)
* **地理空间库**: **GDAL**, **PROJ**, **GEOS** (由 Anaconda/Conda 统一管理)
* **API 框架**: Django REST Framework
* **前端**: Leaflet.js, Bootstrap 5

---

## 3. 本地环境搭建与部署 (Windows)

请严格按照以下顺序执行。

### 3.1. 安装必备软件

在开始之前，请在本地计算机上安装以下两个核心软件：

1.  **Anaconda Navigator**:
    * **定位**: Python 环境与包的核心管理器。
    * **下载地址**: [Anaconda Distribution](https://www.anaconda.com/download)
    * 请下载并安装适用于 Windows 的最新版本。

2.  **PostgreSQL 与 PostGIS**:
    * **推荐版本**: PostgreSQL 15.x
    * **安装指南**:
        1.  从 [PostgreSQL 官网](https://www.postgresql.org/download/) 下载并安装。
        2.  安装过程中，请设置并**记录**超级用户（默认为 `postgres`）的密码。
        3.  安装完成后，启动 **Stack Builder** 工具。
        4.  在 Stack Builder 中，选择 `Spatial Extensions` -> `PostGIS`。
        5.  **【关键】** 确保选择与您 PostgreSQL 版本（如 15）完全匹配的 PostGIS 包进行安装。
        6.  安装完成后，请检查并确保 PostgreSQL 服务正在运行（详见 7.2 节）。

### 3.2. 获取项目代码

* 打开命令行工具（例如 Anaconda Prompt）。
* `cd` 到您希望存放项目的目录（例如 `D:\project`）。
* 运行 `git clone` 命令下载项目：
    ```bash
    git clone [https://github.com/beka2nt/paleolithic-ruins-map.git](https://github.com/beka2nt/paleolithic-ruins-map.git)
    ```
* **进入项目目录**：
    ```bash
    cd paleolithic-ruins-map
    ```
* **（重要）** 接下来的所有命令都**必须**在此项目根目录下执行。

### 3.3. 创建并激活 Conda 环境

1.  **创建 Conda 环境**:
    * 在项目根目录下，运行以下命令。此命令将创建一个名为 `ruinsenv` 的新环境，并**自动安装 Python 和所有必需的地理空间库 (GDAL)**：
        ```bash
        conda create --name ruinsenv python=3.11 gdal -c conda-forge
        ```
    * 在提示 `Proceed ([y]/n)?` 时，输入 `y` 并按回车。
    * **优势**: 此步骤完成后，所有复杂的 C/C++ 库依赖均由 Conda 自动管理，**无需再单独安装 OSGeo4W 或手动配置系统环境变量**。

2.  **激活 Conda 环境**:
    ```bash
    conda activate ruinsenv
    ```
    * 激活成功后，命令行提示符前应有 `(ruinsenv)` 标识。

### 3.4. 安装 Python 依赖

* 在已激活的 `(ruinsenv)` 环境中，运行 `pip` 来安装 `requirements.txt` 文件中列出的其余 Python 包：
    ```bash
    pip install -r requirements.txt
    ```
    **注意**: `requirements.txt` 中不应包含 `GDAL`，因为它已由 Conda 负责管理。

### 3.5. 数据库设置与数据恢复

1.  打开 `psql` (PostgreSQL 命令行工具) 或 pgAdmin，以 `postgres` 用户身份登录。
2.  创建数据库：
    ```sql
    CREATE DATABASE ruins_db ENCODING 'UTF8';
    ```
3.  连接到新创建的数据库：
    ```sql
    \c ruins_db
    ```
4.  为数据库启用 PostGIS 扩展：
    ```sql
    CREATE EXTENSION postgis;
    ```
    * (如果此步失败，请检查 3.1 节的 PostGIS 是否已正确安装且版本匹配)
5.  恢复数据备份：
    * 打开**另一个新的**命令行窗口（**不要**在 `psql` 内部）。
    * 导航到项目根目录。
    * 运行 `psql` 命令导入 `ruins_db_fresh_backup.sql` 文件：
        ```bash
        psql -U postgres -d ruins_db -f ruins_db_fresh_backup.sql
        ```
    * 按提示输入 `postgres` 用户的密码。

### 3.6. Django 项目配置 (重要)

本项目**已配置**为自动检测并使用 Conda 环境中的 GDAL 库。您**唯一**需要修改的就是数据库密码。

1.  打开 `main_project/settings.py` 文件。
2.  找到 `DATABASES` 配置部分。
3.  将 `PASSWORD` 的值修改为您在 3.1 步中为 `postgres` 用户设置的密码。
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'ruins_db',
            'USER': 'postgres',
            'PASSWORD': 'your_local_password', # <-- 将这里替换为你电脑上的 postgres 密码
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```
    **注意**: `settings.py` 中其他关于 GDAL 的路径配置是为 Conda 环境特意编写的，请**不要删除**它们。

### 3.7. 运行数据库迁移

在激活的 `(ruinsenv)` Anaconda Prompt 中，运行 `migrate` 以同步数据库状态：
```bash
python manage.py migrate
```
* 您应该会看到 "No migrations to apply."，这表示恢复的数据已包含所有表格，是正常现象。

### 3.8. 创建本地管理员账户

```bash
python manage.py createsuperuser
```
* 按照提示设置用户名和密码，用于登录后台。

---

## 4. 运行项目

1.  确保 `ruinsenv` Conda 环境已激活。
2.  确保本地 PostgreSQL 服务正在运行（详见 7.2 节）。
3.  在项目根目录下，启动 Django 开发服务器：
    ```bash
    python manage.py runserver
    ```
4.  访问应用：
    * **地图主页**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
    * **后台管理**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## 5. 技术栈学习指南 

为顺利理解并扩展本项目，建议按以下路径学习相关技术：

#### **第一层：基础与核心**

1.  **Anaconda/Conda**: 学习如何创建 (`create`)、激活 (`activate`) 环境，以及如何安装包 (`install`)。这是管理项目依赖的基础。
2.  **Python 编程**: 掌握基础语法、面向对象编程（类）和模块。
3.  **Django 框架**:
    * **学习重点**: MVT 架构（模型、视图、模板），URL 路由，Django ORM（`models.py` 如何定义数据库），以及 Django Admin 的使用。
4.  **前端基础 (HTML, CSS, JavaScript)**:
    * **学习重点**: 掌握 JavaScript 的 DOM 操作、事件处理和异步编程 (`fetch` API)，这是与后端 API 交互的核心。

#### **第二层：项目特色与进阶**

1.  **Django REST Framework (DRF)**:
    * **定位**: 用于构建项目的 API 接口 (`ruins_api/serializers.py` 和 `ruins_api/views.py` 中的 `ViewSet`)。
    * **学习重点**: 序列化器 (Serializers)，视图集 (ViewSets)。

2.  **Leaflet.js**:
    * **定位**: 前端地理信息可视化库 (`templates/ruins_map.html` 中的 `<script>` 标签内)。
    * **学习重点**: `Map`, `TileLayer`, `Marker`, `Popup` 等核心概念，以及如何加载和渲染 GeoJSON 数据。

3.  **数据库与地理空间 **:
    * **PostgreSQL**: 了解它是一个强大的关系型数据库。
    * **PostGIS**: 理解它作为 PostgreSQL 空间数据库扩展的角色，特别是 `PointField` 等地理数据类型。
    * **GeoDjango**: 学习 Django 如何通过 ORM 进行空间查询，并理解 GDAL/PROJ/GEOS 作为其底层依赖的重要性（Conda 已为我们解决了这个问题）。

## 6. 故障排查

* **`ModuleNotFoundError: No module named 'django'`**:
    * **原因**: 忘记了激活 Conda 环境。
    * **解决**: 关闭终端，重新打开 Anaconda Prompt，运行 `conda activate ruinsenv`，然后再执行命令。
* **`psql : 无法将“psql”项识别为...`**:
    * **原因**: PostgreSQL 的 `bin` 目录没有被添加到 Windows 的 `PATH` 环境变量中。
    * **解决**: （可选）将 `C:\Program Files\PostgreSQL\15\bin` 添加到系统 `Path` 环境变量中。或**使用 `pgAdmin` 的图形界面**来执行 3.5 节中的数据库创建和恢复操作。
* **访问 `http://localhost:8000/` 页面空白或数据加载不出来**:
    * **原因 (99% 的可能性)**: 重启了电脑，但 PostgreSQL 数据库服务没有自动启动。
    * **解决**:
        1.  按 `Win + R` 键，输入 `services.msc` 并回车。
        2.  在列表中找到 `postgresql-x64-15`（或类似）的服务。
        3.  右键点击，选择 **"Start" (启动)**。
        4.  (推荐) 再次右键点击 -> "属性" -> "启动类型" -> 改为 **"Automatic" (自动)**，以便将来自动启动。
