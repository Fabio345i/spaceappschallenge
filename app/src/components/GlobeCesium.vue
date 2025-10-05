<script setup>
import { onMounted, ref, watch } from 'vue'
import {
  Viewer,
  UrlTemplateImageryProvider,
  EllipsoidTerrainProvider,
  GeoJsonDataSource,
  Color,
  Cartesian3,
  HeadingPitchRange,
  ScreenSpaceEventType,
  ScreenSpaceEventHandler
} from 'cesium'
import 'cesium/Build/Cesium/Widgets/widgets.css'
import Popup from './Popup.vue'

const props = defineProps({
  target: {
    type: Object,
    default: null
  },
  resetTrigger: {
    type: Number,
    default: 0
  },
  isLoading: {
    type: Boolean,
    default: false
  }
})

const cesiumContainer = ref(null)
const globeWrapper = ref(null)
let viewer = null
let cityDataSource = null
let markerEntity = null
const showPopup = ref(false)
const popupTitle = ref('')
const climatData = ref(null)
const recommandation = ref('')
const popupPosition = ref({ top: '50%', left: '50%' })

// Dimensions approximatives du popup (ajuste selon ton popup réel)
const POPUP_WIDTH = 350
const POPUP_HEIGHT = 450
const PADDING = 10

async function fetchOsmBoundary(osmId) {
  try {
    const url = `https://osm-boundaries.com/Download/Submit?db=osm&osm_ids=${osmId}&format=geojson&simplify=0`
    const res = await fetch(url)
    if (!res.ok) throw new Error('OSM Boundaries error')
    return await res.json()
  } catch (e) {
    console.warn('Failed to load OSM boundaries', e)
    return null
  }
}

function resetCameraView() {
  if (viewer) {
    viewer.camera.flyTo({
      destination: Cartesian3.fromDegrees(-95, 50, 9000000),
      duration: 1.5
    })
  }
}

onMounted(() => {
  viewer = new Viewer(cesiumContainer.value, {
    baseLayerPicker: false,
    geocoder: false,
    timeline: false,
    animation: false,
    terrainProvider: new EllipsoidTerrainProvider()
  })

  viewer.imageryLayers.removeAll()
  viewer.imageryLayers.addImageryProvider(
    new UrlTemplateImageryProvider({
      url: 'https://cartodb-basemaps-a.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png',
      credit: '© OpenStreetMap contributors © CARTO'
    })
  )

  viewer.camera.flyTo({
    destination: Cartesian3.fromDegrees(-95, 50, 9000000)
  })

  const handler = new ScreenSpaceEventHandler(viewer.scene.canvas)
handler.setInputAction((movement) => {
  const wrapper = globeWrapper.value
  if (!wrapper) return

  const wrapperRect = wrapper.getBoundingClientRect()

  const header  = document.querySelector('header')
  const sidenav = document.querySelector('.sidenav') || document.querySelector('aside')
  const headerBottom = header ? header.getBoundingClientRect().bottom : 0
  const sideRight    = sidenav ? sidenav.getBoundingClientRect().right : 0

  // Position du clic dans le viewport
  const clickViewportX = movement.position.x
  const clickViewportY = movement.position.y

  // Conversion : viewport -> coordonnées locales du wrapper
  let popupX = clickViewportX - wrapperRect.left - (POPUP_WIDTH / 2)
  let popupY = clickViewportY - wrapperRect.top - POPUP_HEIGHT - 20

  const minX = sideRight - wrapperRect.left + PADDING
  const minY = headerBottom - wrapperRect.top + PADDING
  const maxX = wrapperRect.width  - POPUP_WIDTH  - PADDING
  const maxY = wrapperRect.height - POPUP_HEIGHT - PADDING

  // Si "au-dessus" sort en haut => on met en dessous
  if (popupY < minY) popupY = clickViewportY - wrapperRect.top + 20

  // Clamp final
  popupX = Math.min(Math.max(popupX, minX), maxX)
  popupY = Math.min(Math.max(popupY, minY), maxY)

  popupPosition.value = {
    top:  `${popupY}px`,
    left: `${popupX}px`
  }

  popupTitle.value = "Nom de la montagne"
  climatData.value = { /* ... */ }
  showPopup.value = true
}, ScreenSpaceEventType.LEFT_CLICK)

})

watch(
  () => props.resetTrigger,
  () => {
    resetCameraView()
  }
)

watch(
  () => props.target,
  async (val) => {
    if (props.isLoading || !val || !viewer) return
    
    if (cityDataSource) {
      viewer.dataSources.remove(cityDataSource, true)
      cityDataSource = null
    }
    if (markerEntity) {
      viewer.entities.remove(markerEntity)
      markerEntity = null
    }

    let geojsonToLoad = null

    if (val.geojson) {
      geojsonToLoad = val.geojson
    } else if (val.osm_id) {
      geojsonToLoad = await fetchOsmBoundary(val.osm_id)
    }

    if (geojsonToLoad) {
      if (geojsonToLoad.type === 'Polygon' || geojsonToLoad.type === 'MultiPolygon') {
        geojsonToLoad = {
          type: 'Feature',
          properties: {},
          geometry: geojsonToLoad
        }
      }

      cityDataSource = await GeoJsonDataSource.load(geojsonToLoad, {
        stroke: Color.fromCssColorString('#6b7280'),
        fill: Color.fromCssColorString('#6b7280').withAlpha(0.2),
        strokeWidth: 2
      })
      viewer.dataSources.add(cityDataSource)

      const entities = cityDataSource.entities.values
      if (entities.length > 0) {
        viewer.flyTo(entities, {
          duration: 1.5,
          offset: new HeadingPitchRange(0, -0.5, 0)
        })
      }
    }

    if (val.lat && val.lon) {
      markerEntity = viewer.entities.add({
        position: Cartesian3.fromDegrees(val.lon, val.lat),
        billboard: {
          image: 'https://cdn-icons-png.flaticon.com/512/684/684908.png',
          scale: 0.08,
          verticalOrigin: 1
        }
      })

      if (!geojsonToLoad) {
        viewer.camera.flyTo({
          destination: Cartesian3.fromDegrees(val.lon, val.lat, 30000),
          duration: 1.5
        })
      }
    }
  },
  { deep: true }
)

watch(
  () => props.isLoading,
  (newIsLoading, oldIsLoading) => {
    if (oldIsLoading && !newIsLoading && props.target && viewer) {
      animateToTarget(props.target)
    }
  }
)

async function animateToTarget(val) {
  if (!val || !viewer) return
  
  if (cityDataSource) {
    viewer.dataSources.remove(cityDataSource, true)
    cityDataSource = null
  }
  if (markerEntity) {
    viewer.entities.remove(markerEntity)
    markerEntity = null
  }

  let geojsonToLoad = null

  if (val.geojson) {
    geojsonToLoad = val.geojson
  } else if (val.osm_id) {
    geojsonToLoad = await fetchOsmBoundary(val.osm_id)
  }

  if (geojsonToLoad) {
    if (geojsonToLoad.type === 'Polygon' || geojsonToLoad.type === 'MultiPolygon') {
      geojsonToLoad = {
        type: 'Feature',
        properties: {},
        geometry: geojsonToLoad
      }
    }

    cityDataSource = await GeoJsonDataSource.load(geojsonToLoad, {
      stroke: Color.fromCssColorString('#6b7280'),
      fill: Color.fromCssColorString('#6b7280').withAlpha(0.2),
      strokeWidth: 2
    })
    viewer.dataSources.add(cityDataSource)

    const entities = cityDataSource.entities.values
    if (entities.length > 0) {
      viewer.flyTo(entities, {
        duration: 1.5,
        offset: new HeadingPitchRange(0, -0.5, 0)
      })
    }
  }

  if (val.lat && val.lon) {
    markerEntity = viewer.entities.add({
      position: Cartesian3.fromDegrees(val.lon, val.lat),
      billboard: {
        image: 'https://cdn-icons-png.flaticon.com/512/684/684908.png',
        scale: 0.08,
        verticalOrigin: 1
      }
    })

    if (!geojsonToLoad) {
      viewer.camera.flyTo({
        destination: Cartesian3.fromDegrees(val.lon, val.lat, 30000),
        duration: 1.5
      })
    }
  }
}

</script>

<template>
  <div ref="globeWrapper" class="globe-wrapper">
    <div ref="cesiumContainer" class="globe"></div>
    
    <div v-if="showPopup" class="popup-container" :style="popupPosition">
      <Popup
        :visible="showPopup"
        :title="popupTitle"
        :climatData="climatData"
        @close="showPopup = false"
      />
    </div>
  </div>
</template>

<style scoped>
.globe-wrapper {
  position: relative;




  overflow: hidden;
  z-index: 1;
  flex-shrink: 0;
}

.popup-container {
  position: absolute;
  z-index: 100;
  pointer-events: auto;
}
</style>
