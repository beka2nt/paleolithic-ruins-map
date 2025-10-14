
window.addEventListener('load', function() {
    // 获取经纬度输入框和 geom 字段的 textarea
    // Django 表单字段的 ID 通常是 'id_' + 字段名
    const lonInput = document.getElementById('id_longitude');
    const latInput = document.getElementById('id_latitude');
    const geomTextarea = document.getElementById('id_geom'); // 这是 django-leaflet 用来存储 WKT 数据的 textarea

    // 确保所有关键元素都存在
    if (!lonInput || !latInput || !geomTextarea) {
        console.warn('Admin Map Enhancer: 经纬度或geom输入字段未找到。脚本可能无法正常工作。');
        return;
    }

    // 函数：根据经纬度输入更新地图和 geom textarea
    function updateMapAndGeomFromInputs() {
        const lon = parseFloat(lonInput.value);
        const lat = parseFloat(latInput.value);

        // 简单验证
        if (!isNaN(lon) && !isNaN(lat) && lon >= -180 && lon <= 180 && lat >= -90 && lat <= 90) {
            // 获取 django-leaflet 的地图实例和标记实例
            // mapWidget 是 django-leaflet 在 window 对象上创建的全局对象
            // mapWidget.maps['id_FIELDNAME'] 存储了特定字段的地图相关信息
            if (window.mapWidget && window.mapWidget.maps && window.mapWidget.maps['id_geom']) {
                const mapCtrl = window.mapWidget.maps['id_geom']; // 地图控制器对象
                const mapInstance = mapCtrl.map;     // Leaflet 地图实例
                let markerInstance = mapCtrl.marker; // Leaflet 标记实例

                const newLatLng = L.latLng(lat, lon);

                if (markerInstance) {
                    markerInstance.setLatLng(newLatLng); // 更新现有标记的位置
                } else {
                    markerInstance = L.marker(newLatLng).addTo(mapInstance);
                    mapCtrl.marker = markerInstance; // 将新标记存回控制器
                }

                const currentZoom = mapInstance.getZoom();
                mapInstance.setView(newLatLng, currentZoom < 5 ? 12 : currentZoom);


                const wktValue = `SRID=4326;POINT(${lon} ${lat})`;
                geomTextarea.value = wktValue;


                const event = new Event('change', { bubbles: true });
                geomTextarea.dispatchEvent(event);


            } else {
                console.warn('Admin Map Enhancer: 未找到 "id_geom" 的 Leaflet 地图实例。');
            }
        }
    }

    // 函数：根据 geom textarea 的值更新经纬度输入框
    function updateInputsFromGeomTextarea() {
        const wktValue = geomTextarea.value;
        // 解析 WKT: SRID=4326;POINT(lon lat)
        const match = wktValue.match(/POINT\(\s*([+-]?\d+(?:\.\d+)?)\s+([+-]?\d+(?:\.\d+)?)\s*\)/);

        if (match && match[1] && match[2]) {
            const lonFromGeom = parseFloat(match[1]);
            const latFromGeom = parseFloat(match[2]);

            // 只有当值不同或输入框未聚焦时才更新，避免覆盖用户正在输入的内容
            if (document.activeElement !== lonInput && parseFloat(lonInput.value) !== lonFromGeom) {
                lonInput.value = lonFromGeom.toFixed(6); // 保留6位小数
            }
            if (document.activeElement !== latInput && parseFloat(latInput.value) !== latFromGeom) {
                latInput.value = latFromGeom.toFixed(6);
            }
        } else if (wktValue === "" || wktValue.toUpperCase().includes("EMPTY")) {
            // 如果 geom 被清空 (例如地图上的标记被移除)
            if (document.activeElement !== lonInput) lonInput.value = "";
            if (document.activeElement !== latInput) latInput.value = "";
        }
    }

    // 为经纬度输入框添加事件监听器 (input 事件会在每次内容改变时触发)
    lonInput.addEventListener('input', updateMapAndGeomFromInputs);
    latInput.addEventListener('input', updateMapAndGeomFromInputs);

    // 监听 geom textarea 的变化 (例如地图点击导致的变化)
    const observer = new MutationObserver(function(mutationsList) {
        for(let mutation of mutationsList) {
            // 监视 value 属性的变化或者 textarea 内容的直接变化
            if (mutation.type === 'attributes' && mutation.attributeName === 'value' || mutation.type === 'childList') {
                updateInputsFromGeomTextarea();
                return;
            }
        }
    });

    // 配置观察选项:
    const config = { attributes: true, childList: true, subtree: true, characterData: true };
    // 开始观察目标节点以应对配置 Mutations:
    observer.observe(geomTextarea, config);

    // 初始加载时也调用一次，以同步地图点击可能已填充的 geomTextarea
    if (geomTextarea.value) {
        updateInputsFromGeomTextarea();
    }
});