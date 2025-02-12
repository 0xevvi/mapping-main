<script>
  window.global ||= window;
  import Map from "./Map.svelte";
  // import SelectedFeatures from "./SelectedFeatures.svelte";
  import Search from "./Search.svelte";
  import { CollapsibleCard } from "svelte-collapsible/dist/index.mjs";

  let innerWidth;
  let innerHeight;

  let height;

  let map;

  $: height = innerHeight / 1.4;
</script>

<svelte:window bind:innerWidth bind:innerHeight />

<main class="h-screen w-screen">
  <Map bind:map />
  <div id="left-bar">
    <div id="meta-info" class="p-4 bg-orange-100 rounded-xl">
      <h1 class="font-bold font-700 text-3xl">
        Explorer for Ethno-Political activity globally on Tamils
      </h1>
      <h3>
        <br />
        This is a prototype to explore linked stories of Tamil activity
        <br /> <br /> Search for events or click on an
        event and do a proximity search.
      </h3>
    </div>

    <div id="search" class="mt-3 p-2 w-full bg-orange-100 rounded-xl">
      <Search bind:map />
    </div>
  </div>
  <!-- <div id="right-bar" class="p-4">
  <CollapsibleCard>
      <h2 class="font-semibold text-xl " slot="header">Events in focus &#8964;</h2>
      <div slot='body'>
        <SelectedFeatures 
          height={height}/>
      </div>

  </CollapsibleCard>
</div> -->
</main>

<style>
  #left-bar {
    position: absolute;
    top: 3%;
    left: 3%;
    width: 50%;
  }

  #right-bar {
    position: absolute;
    top: 5%;
    right: 5%;
    width: 90%;
    max-width: 40% !important;
  }
  #left-bar,
  #right-bar {
    z-index: 2000;
    text-align: left;
    color: black;
    border-radius: 10px;

    max-width: 20%;
  }

  #meta-info {
  }
</style>
