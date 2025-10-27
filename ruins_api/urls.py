from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArchaeologicalSiteViewSet

# 创建一个路由器并注册我们的 ViewSet
router = DefaultRouter()
# 'sites' 是 URL 前缀, ArchaeologicalSiteViewSet 是处理请求的视图集, 'archaeologicalsite' 是 basename (用于生成 URL 名称)
router.register(r'sites', ArchaeologicalSiteViewSet, basename='archaeologicalsite')

# API URL 由路由器自动生成
urlpatterns = [
    path('', include(router.urls)),
]