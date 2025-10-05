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
  }
})

const cesiumContainer = ref(null)
let viewer = null
let cityDataSource = null
let markerEntity = null
const showPopup = ref(false);
const popupTitle = ref('');
const climatData = ref(null);
const recommandation = ref('')


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
  },
  { deep: true }
)
</script>

<template>
  <div class="w-full h-full bg-gray-900 border border-gray-800 rounded-md overflow-hidden">
    <div ref="cesiumContainer" class="w-full h-full"></div>
  </div>
</template>
