<script>
  import * as Turf from "@turf/turf";
  import { Deck } from "@deck.gl/core";
  import { ArcLayer } from "@deck.gl/layers";
  import { MapboxOverlay } from "@deck.gl/mapbox";
    import Search from "./Search.svelte";

  export let title;
  export let date;
  export let link;
  export let excerpt;
  export let map;
  export let point;
  export let coordinates;
  let searchTerm

  async function highlightNetwork() {
    let width = 200;
    let height = 200;
    let toBehighlighted = [];
    let features;
    let parentBbox = [
      [point.x - width / 2, point.y - height / 2],
      [point.x + width / 2, point.y + height / 2],
    ];

    // query the layer for the existence of a keyword in teh title
    // get random points from nearby
    let getNearbyFeatures = map.queryRenderedFeatures(parentBbox, {
      layers: ["point"],
    });

    // loop through the properties
    // if the property exists, add it to the highlight layer
    getNearbyFeatures.forEach((element) => {
      if (element.properties.excerpt.toLowerCase().includes(searchTerm.toLowerCase())) {
        toBehighlighted.push(element);
      }
    });


    // create a duplicate source for the highlight
    if (map.getSource("hwdb-highlight")) {
      features = map
        .getSource("hwdb-highlight")
        .setData({ type: "FeatureCollection", features: toBehighlighted })[
        "_data"
      ]["features"];
    } else {
      map.addSource("hwdb-highlight", {
        type: "geojson",
        data: {
          type: "FeatureCollection",
          features: "",
        },
      });
      features = map
        .getSource("hwdb-highlight")
        .setData({ type: "FeatureCollection", features: toBehighlighted })[
        "_data"
      ]["features"];
    }

    // Extract coordinates for arcs
    let arcs = features.map((highlightedPoint) => ({
      sourcePosition: coordinates,
      targetPosition: highlightedPoint._geometry.coordinates,
      sourceColor: [0, 255, 0], // RGB color for the source point
      targetColor: [255, 0, 0], // RGB color for the target point
    }));

    // convert to line features in geojson
    let arcgeojson = Turf.featureCollection(
      arcs.map((arc) =>
        Turf.lineString([arc.sourcePosition, arc.targetPosition]),
      ),
    );

    // Draw lines
    if (map.getSource("arcs")) {
      map.getSource("arcs").setData(arcgeojson);
    } else {
      map.addSource("arcs", {
        type: "geojson",
        data: arcgeojson,
      });
      map.addLayer({
        id: "arcs",
        type: "line",
        source: "arcs",
        paint: {
          "line-color": "brown",
          "line-width": 4,
          "line-opacity": 0.8,
        },
      });
    }

    // console.log(arcs);

    // // Use deck.gl to render arcs
    // const deckgl = new MapboxOverlay({
    //   layers: [
    //     new ArcLayer({
    //       id: "arc-layer",
    //       data: arcs,
    //       pickable: true,
    // getWidth: 12,
    //       opacity: 0.5,
    //     }),
    //   ],
    // });
    // map.addControl(deckgl);
    // console.log(deckgl);

    // // Handle map movement to update deck.gl layer
    // map.on('move', () => {
    //   const { lng, lat } = map.getCenter();
    //   deckgl.setProps({
    //     viewState: { longitude: lng, latitude: lat, zoom: map.getZoom() },
    //   });
    // });
  }
</script>

<div class="popup">
  <h3>{@html title}</h3>
  <p>{date}</p>
  <a href={link}>Link to article</a>
  <p>{@html excerpt}</p>
  <br />
  <input type="text" bind:value={searchTerm} placeholder="Search for related organisational involvement nearby" class="text-white p-2 rounded-lg"/>
  <button class="bg-slate-700" id="addToList" disabled={searchTerm === ""} on:click={highlightNetwork}>
    Visualise connections
  </button>
</div>

<style lang="postcss">
  .popup {
    @apply text-black text-left bg-slate-100 p-3 rounded-md w-80;
  }
  :global(.maplibre-gl-popup-close-button) {
    @apply text-black bg-slate-700;
  }
  :global(.maplibre-gl-popup-content) {
    @apply bg-transparent;
  }
</style>
