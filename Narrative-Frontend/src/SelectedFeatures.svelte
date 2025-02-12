<script>
  import "leaflet";
  import { map } from "./Map.svelte";

  import {
    Node,
    Svelvet,
    Minimap,
    Controls,
    Resizer,
    Anchor,
    Background,
  } from "svelvet";

  import { selectedFeatures } from "./stores.js";
  import { onMount } from "svelte";

  let highlightLayer = new L.FeatureGroup();

  let edges = [];

  let width;
  export let height;
  let nodes = [];
  let lastValue;

  let categories = [
    { text: "Category 1", value: "1" },
    { text: "Category 2", value: "2" },
    { text: "Category 3", value: "3" },
  ];
  // read from subscribed store
  // if reloading, load all from store
  // else load from local storage

  onMount(() => {
    for (let i = 0; i < $selectedFeatures.length; i++) {
      let feature = $selectedFeatures[i];
      nodes.push({
        label: feature.title,
        width: 220,
        height: 100,
        notes: "",
        feature: feature,
      });
    }
    nodes = nodes;
  });

  $: if ($selectedFeatures.length > 0) {
    lastValue = $selectedFeatures[$selectedFeatures.length - 1];

    nodes.push({
      label: lastValue.title,
      width: 220,
      height: 200,
      notes: "",
      feature: lastValue.feature,
    });

    nodes = nodes;
  }

  function zoomToFeature(e) {
    let feature = e.feature;
    highlightLayer.clearLayers();
    console.log("Zooming to feature");

    // Add a circle marker to highlight the feature
    highlightLayer.addLayer(
      new L.CircleMarker(feature.geometry.coordinates.reverse(), {
        radius: 30,
        color: "#ff7800",
        weight: 5,
        opacity: 0.65,
      })
    );

    map.flyTo(feature.geometry.coordinates, 4);
    highlightLayer.addTo(map);
  }
  function highlightAllFeatures(feature) {
    highlightLayer.clearLayers();
    console.log("Zooming to feature");

    $selectedFeatures.forEach((feature) => {
      highlightLayer.addLayer(
        new L.CircleMarker(feature.feature.geometry.coordinates.reverse(), {
          radius: 30,
          color: "#ff7800",
          weight: 5,
          opacity: 0.9,
        })
      );
    });

    // map.flyTo(feature.geometry.coordinates, 8);
    highlightLayer.addTo(map);
  }
</script>

<div id="events-in-focus">
  <Svelvet {height} editable={true}>
    <Background bgColor="#faebd7" slot="background" />
    {#each nodes as node}
      <Node {...node} on:nodeClicked={zoomToFeature}>
        <div class="node">
          <section class="container mx-3 my-3">
            <h2>{node.label}</h2>
            <input
              class="text-white my-1"
              value={node.notes}
              placeholder="Enter notes"
            />

            <select
              class="text-white my-1"
              value={node.category}
              placeholder="Select a category"
            >
              {#each categories as category}
                <option value={category}>
                  {category.text}
                </option>
              {/each}
            </select>

            <input
              class="text-white my-1"
              value={node.notes}
              placeholder="Charts to display"
            />

            <input
              class="text-white my-1"
              value={node.notes}
              placeholder="Geospatial morphing/effects"
            />
            <Resizer width height rotation />
          </section>

          <Anchor direction="west" dynamic />
          <Anchor direction="west" dynamic />
        </div>
      </Node>
    {/each}
  </Svelvet>

  {#if nodes.length < 1}
    <p>No events selected. Please open an event and click, "Add to list"</p>
  {:else}
    <button
      on:click={() => highlightAllFeatures(selectedFeatures)}
      class="bg-slate-700"
    >
      Highlight all events
    </button>

    <button
      on:click={() => {
        selectedFeatures.set([]);
        highlightLayer.clearLayers();
        nodes = [];
      }}
      class="bg-slate-700"
    >
      Clear all events
    </button>
  {/if}
</div>

<style>
  button {
    margin-top: 0.2em;
    size: 1em;
    padding: 0.2em 0.5em;
  }

  #background-wrapper {
    background-color: #faebd7;
  }

  .node {
    width: 100%;
    height: 100%;
    background-color: #faebd7;
    border-radius: 8px;
    border: 2px solid black;
  }
  .selected {
    border: 2px solid white;
  }
  ul {
    list-style-type: none;
    padding: 1em;
  }
</style>
