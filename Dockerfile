# 使用与您项目兼容的 Python 版本
FROM python:3.11-slim-bullseye

# 设置环境变量，避免 Python 产生 .pyc 文件和缓冲输出
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 设置工作目录
WORKDIR /app

# 关键：安装系统依赖，特别是 GDAL/GEOS/PROJ 的 C 库
# build-essential 用于编译某些 Python 包，python3-gdal 保证了 C 库和 Python 绑定的兼容性
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gdal-bin \
    libgdal-dev \
    python3-gdal \
    && rm -rf /var/lib/apt/lists/*

# 复制 requirements.txt 并安装 Python 依赖
# GDAL Python 绑定已由 python3-gdal 安装，requirements.txt 中应移除 GDAL
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制整个项目代码到工作目录
COPY . .

# 复制并设置入口点脚本的执行权限
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 暴露 Gunicorn 运行的端口
EXPOSE 8000

# 设置容器启动时执行的入口点脚本
ENTRYPOINT ["/entrypoint.sh"]