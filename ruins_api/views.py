from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet # 使用标准的 ReadOnlyModelViewSet
from rest_framework_gis.filters import InBBoxFilter   # 导入 InBBoxFilter
# from rest_framework_gis.pagination import GeoJsonPagination # 如果需要分页

from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import ArchaeologicalSite
# 确保 serializers.py 中的 ArchaeologicalSiteListSerializer 继承自 GeoFeatureModelSerializer
from .serializers import ArchaeologicalSiteListSerializer, ArchaeologicalSiteDetailSerializer

class ArchaeologicalSiteViewSet(ReadOnlyModelViewSet):
    """
    考古遗址 API 端点 (备选方案)。
    - 列表视图 (`/api/sites/`) 返回 GeoJSON FeatureCollection。
    - 详情视图 (`/api/sites/{id}/`) 返回单个遗址的详细 JSON 数据。
    - 只读行为。
    - 手动添加 Bbox 过滤。
    """
    queryset = ArchaeologicalSite.objects.all().order_by('name')

    http_method_names = ['get', 'head', 'options'] # 保持只读

    def get_serializer_class(self):
        if self.action == 'list':
            return ArchaeologicalSiteListSerializer
        return ArchaeologicalSiteDetailSerializer

    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter, InBBoxFilter)

    bbox_filter_field = 'geom'
    bbox_filter_include_overlapping = True # 根据需要设置

    filterset_fields = {
        'protection_level': ['exact', 'in'],
        'province': ['exact', 'in'],
        'period': ['exact', 'icontains'],
        'protection_batch': ['exact', 'icontains'],
    }

    search_fields = [
        'name', 'location_description', 'period', 'protection_batch',
        'province', 'city', 'county_district', 'description'
    ]

    ordering_fields = ['name', 'period', 'protection_level', 'protection_batch', 'province', 'updated_at']
    ordering = ['name']


# 确保 map_view 函数仍然存在
def map_view(request):
    protection_levels = ArchaeologicalSite.PROTECTION_LEVEL_CHOICES
    provinces = ArchaeologicalSite.objects.values_list('province', flat=True).distinct().order_by('province')
    provinces = [p for p in provinces if p]

    context = {
        'protection_levels': protection_levels,
        'provinces': provinces,
    }
    return render(request, 'ruins_map.html', context)