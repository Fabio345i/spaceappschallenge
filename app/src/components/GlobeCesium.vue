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

const props = defineProps({
  target: {
    type: Object,
    default: null
  }
})

const cesiumContainer = ref(null)
let viewer = null
let cityDataSource = null
let markerEntity = null
const showPopup = ref(false);
const popupTitle = ref('');
const climatData = ref(null);


async function fetchOsmBoundary(osmId) {
  try {
    const url = `https://osm-boundaries.com/Download/Submit?db=osm&osm_ids=${osmId}&format=geojson&simplify=0`
    const res = await fetch(url)
    if (!res.ok) throw new Error('OSM Boundaries error')
    return await res.json()
  } catch (e) {
    console.warn('Impossible de charger les limites OSM Boundaries', e)
    return null
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
  handler.setInputAction((mouvement) => {
    // Attribuer les données
      popupTitle.value = "Nom de la montagne";
      
      climatData.value = {
        altitude_base: 265,
        altitude_sommet: 875,
        temperature_base: 15,
        humiditer_base: 65,
        vent_base: 12,
        precipitation_base: 0,
        temperature_sommet: 8,
        vent_sommet: 8,
        precipitation_sommet: 2,
      }

      showPopup.value = true
    }, ScreenSpaceEventType.LEFT_CLICK);
})

watch(
  () => props.target,
  async (val) => {
    if (!val || !viewer) return

    if (cityDataSource) {
      console.log(cityDataSource);
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
    }
    else if (val.osm_id) {
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
  <InfoPopup
    :visible="showPopup"
    :title="popupTitle"
    :climatData="climatData"
    @close="showPopup = false"
  />

  <div class="globe-wrapper">
    <div ref="cesiumContainer" class="globe"></div>
  </div>
</template>



<style scoped>

.globe {
  width: 100%;
  height: 100%;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #374151;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}
</style>




