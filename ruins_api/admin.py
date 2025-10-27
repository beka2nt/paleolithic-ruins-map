from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import ArchaeologicalSite
from .forms import ArchaeologicalSiteAdminForm

class ArchaeologicalSiteAdmin(LeafletGeoAdmin):
    form = ArchaeologicalSiteAdminForm

    list_display = ('name', 'period', 'protection_level', 'protection_batch', 'province', 'city', 'updated_at')
    search_fields = ('name', 'location_description', 'period', 'protection_batch', 'province', 'city', 'county_district', 'description')
    list_filter = ('protection_level', 'protection_batch', 'province', 'period', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('name', 'period', 'protection_level', 'protection_batch')
        }),
        ('地理坐标输入', {
            'fields': ('longitude', 'latitude', 'geom')
        }),
        ('地理位置描述', {
            'fields': ('location_description', 'province', 'city', 'county_district')
        }),
        ('详细描述与发现', {
            'fields': ('description', 'gallery_urls', 'discovered_by', 'discovery_date', 'excavation_info'),
            'classes': ('collapse',)
        }),
    )

    # 新增 Media 类来加载自定义 JavaScript
    class Media:
        js = (
            'ruins_api/js/admin_map_enhancer.js', # 相对于 STATIC_URL 的路径
        )

admin.site.register(ArchaeologicalSite, ArchaeologicalSiteAdmin)