from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from .models import ArchaeologicalSite

class ArchaeologicalSiteListSerializer(GeoFeatureModelSerializer):
    popup_content = serializers.SerializerMethodField()
    protection_level_display = serializers.CharField(source='get_protection_level_display', read_only=True)

    class Meta:
        model = ArchaeologicalSite
        geo_field = "geom"
        fields = ('id', 'name', 'period', 'protection_level_display', 'protection_batch', 'popup_content')

    def get_popup_content(self, obj):
        # 使用 Bootstrap 按钮样式，并调用一个 JavaScript 函数 showSiteDetails，传递遗址的 ID
        return (
            f"<strong>{obj.name}</strong><br>"
            f"年代: {obj.period or '未知'}<br>"
            f"级别: {obj.get_protection_level_display() or '未知'}<br>"
            f"批次: {obj.protection_batch or '无'}<br>"
            f"<button class='btn btn-info btn-sm mt-1 w-100' onclick='showSiteDetails({obj.id})'>更多信息</button>" # 修改了按钮样式和添加了 w-100
        )

class ArchaeologicalSiteDetailSerializer(serializers.ModelSerializer):
    protection_level_display = serializers.CharField(source='get_protection_level_display', read_only=True)

    class Meta:
        model = ArchaeologicalSite
        fields = (
            'id', 'name', 'location_description', 'period',
            'protection_level', 'protection_level_display', 'protection_batch',
            'province', 'city', 'county_district',
            'description',
            'gallery_urls',
            'discovered_by',
            'discovery_date',
            'excavation_info',
            'geom',
            'created_at', 'updated_at'
        )