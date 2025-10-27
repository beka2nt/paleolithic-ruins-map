#!/bin/sh

# 如果任何命令失败，立即退出
set -e

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Starting Gunicorn server..."
# 使用 Gunicorn 启动应用
# 将 RuinsProject.wsgi 替换为您的项目名称.wsgi
exec gunicorn main_project.wsgi:application --bind 0.0.0.0:8000 --workers 3