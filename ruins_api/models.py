from django.contrib.gis.db import models

class ArchaeologicalSite(models.Model):
    name = models.CharField(max_length=255, verbose_name="遗址名称")
    location_description = models.TextField(blank=True, null=True, verbose_name="地理位置描述")
    period = models.CharField(max_length=100, blank=True, null=True, verbose_name="年代")

    geom = models.PointField(srid=4326, verbose_name="地理坐标")

    PROTECTION_LEVEL_CHOICES = [
        ('national_1', '国家级-一级'),
        ('national_2', '国家级-二级'),
        ('national_3', '国家级-三级'),
        ('national', '国家级'),
        ('provincial', '省级'),
        ('municipal', '市级'),
        ('county', '县级'),
        ('other', '其他'),
        ('unknown', '未定级'),
    ]
    protection_level = models.CharField(
        max_length=20,
        choices=PROTECTION_LEVEL_CHOICES,
        default='unknown',
        verbose_name="文物保护级别"
    )

    # 新增：文保批次字段
    protection_batch = models.CharField(
        max_length=100,
        blank=True,         # 允许为空白 (对于 admin 和表单验证)
        null=True,          # 允许数据库中为 NULL (如果字段是可选的)
        verbose_name="文保批次"
    )

    province = models.CharField(max_length=50, blank=True, null=True, verbose_name="所在省份")
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name="所在城市")
    county_district = models.CharField(max_length=50, blank=True, null=True, verbose_name="所在区县")

    description = models.TextField(blank=True, null=True, verbose_name="遗址简介")
    gallery_urls = models.TextField(blank=True, null=True, verbose_name="图片画廊URL列表 (每行一个URL)")

    discovered_by = models.CharField(max_length=100, blank=True, null=True, verbose_name="发现者/单位")
    discovery_date = models.DateField(blank=True, null=True, verbose_name="发现年代/日期")
    excavation_info = models.TextField(blank=True, null=True, verbose_name="发掘信息")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "考古遗址"
        verbose_name_plural = "考古遗址"
        ordering = ['name']