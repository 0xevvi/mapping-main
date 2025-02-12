<script>
  /**
   * Initialize the map and handle resource fetching and display based on spatialEnabled and resource properties.
   * @param {Object} resource - The resource object containing details like id, filterExpression, center, zoom, pitch, bearing.
   * @param {Blob} resourceBlob - The blob containing the resource data.
   * @param {boolean} spatialEnabled - Flag indicating if spatial is enabled.
   */

  // @ts-ignore
  import maplibre from "maplibre-gl";
  import "maplibre-gl/dist/maplibre-gl.css";
  import { onMount } from "svelte";
  import MarkerPopup from "./MarkerPopup.svelte";

  let publicMaptilerKey = "XtQybTQjRpKFSRHVSG0G";

  export let map;

  let filterExpression, appearanceExpression, mapContainer, resourceJSON;
  filterExpression;

  async function getResource() {
    return await fetch("/HWdb_geocoded.geojson").then(async (response) => {
      return response.json();
    });
  }

  const addLayer = async () => {
    const resourceBlob = await getResource();

    // Add source and layer to the map
    map.addSource("hwdb", {
      type: "geojson",
      data: resourceBlob,
    });

    map.addLayer({
      id: "point",
      type: "circle",
      source: "hwdb",
      paint: {
        "circle-radius": 10,
        "circle-color": "orange",
        "circle-opacity": 0.5,
      },
    });

    map.on("click", "point", (e) => {
      let properties = e.features[0].properties;
      const coordinates = e.features[0].geometry.coordinates.slice();
      // const description = properties.title + "<br><br>" + properties.excerpt +
      // "<button class='bg-slate-700' on:click={detectHighlight()}>Highlight</button>";

      // Ensure that if the map is zoomed out such that multiple
      // copies of the feature are visible, the popup appears
      // over the copy being pointed to.
      while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
        coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
      }
      let popup = new maplibre.Popup()
        .setLngLat(coordinates)
        .setHTML("")
        .addTo(map);
      let child = popup.getElement();

      let p = new MarkerPopup({
        target: child.children[1],
        anchor: null,
        props: {
          title: properties.title,
          excerpt: properties.excerpt,
          date: properties.date,
          link: properties.links,
          map: map,
          coordinates: coordinates,
          point: e.point,
        },
      });
    });

    // Change the cursor to a pointer when the mouse is over the places layer.
    map.on("mouseenter", "point", () => {
      map.getCanvas().style.cursor = "pointer";
    });

    // Change it back to a pointer when it leaves.
    map.on("mouseleave", "point", () => {
      map.getCanvas().style.cursor = "";
    });
  };

  /**
   * Event handler for map initialization and resource loading.
   */
  onMount(async () => {
    // Map initialization
    map = new maplibre.Map({
      container: mapContainer,
      style: `https://api.maptiler.com/maps/5b0fdf12-ac62-4bd8-975b-50ac01e3abbd/style.json?key=${publicMaptilerKey}`,
      center: [77.695313, 23.160563],
      pitch: 32,
      bearing: 20,
      zoom: 3,
      maxZoom: 14,
      minZoom: 3,
      transformRequest: (url) => {
        // cache header
        return {
          url: url,
          cache: "force-cache",
        };
      },
    });

    map.on("load", function () {
      addLayer();
    });
  });
</script>

<!-- Map and sidebar section -->
<section id="map" class=" h-full w-full">
  <div bind:this={mapContainer} class="h-full w-full" />
</section>

<!-- Styling -->
<style global lang="postcss">
</style>
