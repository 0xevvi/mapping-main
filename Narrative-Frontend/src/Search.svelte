<script>
  import maplibre from "maplibre-gl";
  import "maplibre-gl/dist/maplibre-gl.css";

  let searchQuery;

  export let map;

  export function searchLayer() {
    let toBehighlighted = [],
      features;
    // query the layer for the existence of a keyword in teh title
    // get random points from nearby
    let getNearbyFeatures = map.queryRenderedFeatures({
      layers: ["point"],
    });

    // loop through the properties
    // if the property exists, add it to the highlight layer
    getNearbyFeatures.forEach((element) => {
      if (
        element.properties.excerpt
          .toLowerCase()
          .includes(searchQuery.toLowerCase())
      ) {
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
      map.addLayer({
        id: "hwdb-highlight",
        type: "circle",
        source: "hwdb-highlight",
        paint: {
          "circle-radius": 10,
          "circle-color": "red",
          "circle-opacity": 0.5,
        },
      });
      features = map
        .getSource("hwdb-highlight")
        .setData({ type: "FeatureCollection", features: toBehighlighted })[
        "_data"
      ]["features"];
    }
  }
</script>

<div class="w-full">
  <input
    type="text"
    id="search-input"
    bind:value={searchQuery}
    class="rounded-md text-white p-1 bg-slate-700"
    placeholder="Search for an event"
  />
  <button
    on:click={() => searchLayer()}
    class="rounded-md p-1 mt-2 bg-slate-700"
    id="search-button">Search</button
  >
</div>
