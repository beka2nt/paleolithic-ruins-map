from django import forms
from django.contrib.gis.geos import Point
from django.contrib.gis.forms import PointField
from .models import ArchaeologicalSite


class ArchaeologicalSiteAdminForm(forms.ModelForm):
    longitude = forms.FloatField(required=False, label="经度 (Longitude)")
    latitude = forms.FloatField(required=False, label="纬度 (Latitude)")

    # 将 geom 字段的 required 设置为 False，让我们的 clean 方法来做最终的必需性校验
    geom = PointField(srid=4326, label="地理坐标 (地图/输入)", required=False)

    class Meta:
        model = ArchaeologicalSite
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.geom:
            self.fields['longitude'].initial = self.instance.geom.x
            self.fields['latitude'].initial = self.instance.geom.y

        desired_order_prefix = [
            'name', 'period', 'protection_level', 'protection_batch',
            'longitude', 'latitude', 'geom'
        ]
        all_current_fields = list(self.fields.keys())
        ordered_prefix_fields = [f for f in desired_order_prefix if f in self.fields]
        other_fields = [f for f in all_current_fields if f not in ordered_prefix_fields]
        final_ordered_keys = ordered_prefix_fields + other_fields
        self.fields = {key: self.fields[key] for key in final_ordered_keys}

    def clean(self):
        cleaned_data = super().clean()
        longitude = cleaned_data.get('longitude')
        latitude = cleaned_data.get('latitude')

        # 从 PointField 的 widget 清理得到的值 (可能来自地图点击，或JS对id_geom的填充)
        # 由于 geom 字段现在是 required=False，如果 id_geom 为空，geom_from_widget 可能为 None
        geom_from_widget = cleaned_data.get('geom')

        final_point_object = None  # 用于存储最终确定的 Point 对象

        # 优先处理用户输入的经纬度
        if longitude is not None and latitude is not None:  # 注意：0.0 也是有效的输入
            # 验证经纬度范围
            valid_lon = -180 <= longitude <= 180
            valid_lat = -90 <= latitude <= 90

            if not valid_lon:
                self.add_error('longitude', '经度必须在 -180 到 180 之间。')
            if not valid_lat:
                self.add_error('latitude', '纬度必须在 -90 到 90 之间。')

            # 只有当经纬度都有效时，才创建 Point 对象
            if valid_lon and valid_lat:
                try:
                    final_point_object = Point(longitude, latitude, srid=4326)
                except ValueError:  # Point 构造失败 (理论上FloatField已保证是数字)
                    self.add_error(None, "根据输入的经纬度创建地理坐标点失败。")

        # 如果通过经纬度成功创建了 Point，则用它
        if final_point_object:
            cleaned_data['geom'] = final_point_object
            # 如果之前 geom 字段因为某种原因有错误 (例如，用户先点地图得到无效点，后输经纬度)
            # 并且我们现在通过经纬度得到了有效点，可以考虑清除 geom 上的旧错误
            if 'geom' in self._errors and self.errors.get('geom'):
                del self._errors['geom']  # 清除 geom 字段的特定错误
        elif geom_from_widget:
            # 如果没有通过经纬度输入得到 Point，但地图小部件提供了有效的 Point
            # (例如用户点击了地图，JS 未能完全填充经纬度框，但 id_geom 有效)
            final_point_object = geom_from_widget  # cleaned_data['geom'] 应该已经是这个值了
            cleaned_data['geom'] = final_point_object  # 再次确保

        # 最后检查：我们是否得到了一个有效的 Point 对象？
        # 模型的 geom 字段是必需的 (除非模型中定义了 null=True, blank=True)
        # 我们在这里强制要求表单必须提供一个有效的 geom
        if not final_point_object:
            # 只有当没有其他关于经纬度的具体错误时，才添加这个通用的 geom 错误
            # 以免错误信息过多且重复
            if not (self.errors.get('longitude') or self.errors.get('latitude')):
                self.add_error('geom', "地理坐标是必填项。请在地图上选择一个点，或输入有效的经纬度。")

        return cleaned_data