from django.contrib import admin
from django.urls import path, include
from ruins_api.views import map_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('ruins_api.urls')),
    path('', map_view, name='home_map_view'),
    # 其他 URL 模式...
]