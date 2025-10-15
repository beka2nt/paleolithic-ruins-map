* * # 中国旧石器时代遗址可视化平台 - 本地部署与开发指南
    
      ## 1. 项目概述
    
      本项目是一个基于 Django 和 GeoDjango 构建的交互式 Web 应用，旨在通过地理信息系统（GIS）技术，可视化地展示、查询和管理中国旧石器时代的考古遗址数据。项目后端提供 REST API 接口，前端通过 Leaflet.js 渲染地理数据。
    
      ## 2. 核心技术栈
    
      * **后端**: Python (3.11+), Django (4.2+), GeoDjango, Django REST Framework
      * **数据库**: PostgreSQL (14+) with PostGIS (3+)
      * **前端**: HTML, CSS, JavaScript, Leaflet.js, Bootstrap 5
      * **地理空间库**: GDAL, PROJ, GEOS (由 Anaconda/Conda 管理)
    
      ---
    
      ## 3. 环境搭建指南 (Windows)
    
      部署本项目的核心是正确配置 Python 和地理空间依赖。**推荐使用 Anaconda 进行环境管理**，它可以极大地简化 GDAL 等复杂库的安装。
    
      ### 3.1. 安装必备软件
    
      1.  **Anaconda Navigator**:
          * **定位**: Python 环境与包的核心管理器。
          * **下载地址**: [Anaconda Distribution](https://www.anaconda.com/download)
          * 请下载并安装适用于 Windows 的最新版本。
    
      2.  **PostgreSQL 与 PostGIS**:
          * **推荐版本**: PostgreSQL 14 或 15
          * **安装指南**:
              1.  从 [PostgreSQL 官网](https://www.postgresql.org/download/) 下载并安装。
              2.  安装过程中，请设置并**记录**超级用户（默认为 `postgres`）的密码。
              3.  安装完成后，启动 **Stack Builder** 工具。
              4.  在 Stack Builder 中，选择 `Spatial Extensions` -> `PostGIS`，安装与 PostgreSQL 版本兼容的最新版 PostGIS 扩展。
    
      ### 3.2. 创建并配置 Conda 环境
    
      1.  **创建 Conda 环境**:
          * 从 Windows 开始菜单打开 **Anaconda Prompt**。
          * 运行以下命令，创建一个名为 `ruinsenv` 的新环境。此命令将**同时安装 Python 和所有必需的地理空间库 (GDAL, PROJ, GEOS)**：
              ```bash
              conda create --name ruinsenv python=3.11 gdal -c conda-forge
              ```
          * 在提示 `Proceed ([y]/n)?` 时，输入 `y` 并按回车。
          * **优势**: 此步骤完成后，所有复杂的 C/C++ 库依赖和环境变量均由 Conda 自动管理，无需手动配置 `GDAL_DATA` 或 `PROJ_LIB`。
    
      2.  **激活 Conda 环境**:
          * 在 Anaconda Prompt 中，运行：
              ```bash
              conda activate ruinsenv
              ```
          * 激活成功后，命令行提示符前应有 `(ruinsenv)` 标识。后续所有操作都应在此环境中进行。
    
      ---
    
      ## 4. 项目部署步骤
    
      ### 4.1. 获取项目代码
    
      通过 `git clone <仓库地址>` 或直接复制，将项目文件夹 (`RuinsProject`) 放置到本地工作目录 (例如 `D:\project\`)。
    
      ### 4.2. 安装 Python 依赖
    
      1.  打开 Anaconda Prompt 并激活 `ruinsenv` 环境。
      2.  导航至项目根目录：
          ```bash
          cd D:\project\RuinsProject
          ```
      3.  使用 `pip` 安装 `requirements.txt` 文件中列出的其余 Python 包：
          ```bash
          pip install -r requirements.txt
          ```
          **注意**: 请确保 `requirements.txt` 文件中**不包含** `GDAL` 相关的行，因为该库已由 Conda 负责管理。
    
      ### 4.3. 数据库设置与数据恢复
    
      1.  打开 `psql` 或 pgAdmin，以 `postgres` 用户身份登录。
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
      5.  恢复数据备份：
          * 打开一个新的命令行窗口（**不要**在 `psql` 内部）。
          * 导航到项目根目录。
          * 运行 `psql` 命令导入 `ruins_db_fresh_backup.sql` 文件：
              ```bash
              psql -U postgres -d ruins_db -f ruins_db_fresh_backup.sql
              ```
          * 按提示输入 `postgres` 用户的密码。
    
      ### 4.4. Django 项目配置
    
      1.  在项目根目录创建 `.env` 文件，用于存放本地配置。复制以下内容并根据实际情况修改：
          ```env
          # .env 文件
          DJANGO_SECRET_KEY=a-new-secret-key-should-be-generated-here
          DJANGO_DEBUG=1
          DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1
          
          # -- 本地数据库配置 --
          DATABASE_URL=postgis://postgres:your_password@localhost:5432/ruins_db
          ```
          **请将 `your_password` 替换为您为 `postgres` 用户设置的密码。**
    
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
    
      1.  确保 `ruinsenv` Conda 环境已激活。
      2.  在项目根目录下，启动 Django 开发服务器：
          ```bash
          python manage.py runserver
          ```
      3.  访问应用：
          * **地图主页**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
          * **后台管理**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
    
      ## 6. 故障排查
    
      * **`ModuleNotFoundError`**:
          * 确认 `ruinsenv` Conda 环境是否已激活。
          * 确认是否已在激活的环境中成功运行 `pip install -r requirements.txt`。
      * **数据库连接错误 (`psycopg2.OperationalError`)**:
          * 确认本地 PostgreSQL 服务正在运行。
          * 检查 `.env` 文件中的 `DATABASE_URL` 是否正确，特别是**密码**、主机 (`localhost`) 和端口 (`5432`)。
      * **GDAL 相关错误**:
          * 此类错误通常与环境配置有关。请确保您严格按照第 3.2 步使用 Conda 创建了环境，并且所有命令都在激活的 `ruinsenv` 环境中执行。
