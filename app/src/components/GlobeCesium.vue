<script setup>
import { onMounted, ref } from 'vue'
import {
  Viewer,
  UrlTemplateImageryProvider,
  EllipsoidTerrainProvider,
  Cartesian3,
  Cartographic,
  Math as CesiumMath,
  ScreenSpaceEventType
} from 'cesium'
import 'cesium/Build/Cesium/Widgets/widgets.css'

const cesiumContainer = ref(null)

onMounted(() => {
  const viewer = new Viewer(cesiumContainer.value, {
    baseLayerPicker: false,
    geocoder: false,
    timeline: false,
    animation: false,
    terrainProvider: new EllipsoidTerrainProvider()
  })

  viewer.imageryLayers.removeAll()
  viewer.imageryLayers.addImageryProvider(
    new UrlTemplateImageryProvider({
      url: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
      credit: '© OpenStreetMap contributors'
    })
  )

  viewer.camera.flyTo({
    destination: Cartesian3.fromDegrees(-71.2082, 46.8139, 3000000.0)
  })

  viewer.screenSpaceEventHandler.setInputAction(click => {
    const cartesian = viewer.camera.pickEllipsoid(click.position)
    if (cartesian) {
      const cartographic = Cartographic.fromCartesian(cartesian)
      const lat = CesiumMath.toDegrees(cartographic.latitude)
      const lon = CesiumMath.toDegrees(cartographic.longitude)
      console.log(`Lat: ${lat}, Lon: ${lon}`)
    }
  }, ScreenSpaceEventType.LEFT_CLICK)
})
</script>

<template>
  <div ref="cesiumContainer" class="globe"></div>
</template>

<style scoped>
.globe {
  width: 125vh;
  height: 100vh; 
}
</style>
