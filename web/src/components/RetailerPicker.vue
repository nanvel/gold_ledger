<template>
  <div>
    <div class="form-control w-full max-w-2xl">
      <div class="label">
        <span class="label-text">Search retailers by name or id</span>
      </div>
      <div class="input input-bordered flex items-center gap-2">
        <input type="text" class="grow" v-model="searchQuery" />
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 16 16"
          fill="currentColor"
          class="h-4 w-4 opacity-70"
        >
          <path
            fill-rule="evenodd"
            d="M9.965 11.026a5 5 0 1 1 1.06-1.06l2.755 2.754a.75.75 0 1 1-1.06 1.06l-2.755-2.754ZM10.5 7a3.5 3.5 0 1 1-7 0 3.5 3.5 0 0 1 7 0Z"
            clip-rule="evenodd"
          />
        </svg>
      </div>
      <div class="label">
        <span class="label-text-alt" v-if="!loading">Found: {{ total }}</span>
        <span class="label-text-alt" v-else>Loading...</span>
      </div>
    </div>
    <div
      class="overflow-x-auto flex flex-col space-y-2 max-w-2xl"
      v-if="retailers.length"
    >
      <div
        v-for="retailer in retailers"
        :key="retailers.id"
        class="bg-base-200 p-4 rounded-lg cursor-pointer"
        v-on:click="selectRetailer(retailer)"
      >
        {{ retailer.id }} : {{ retailer.name }}
      </div>
    </div>
    <div
      v-if="!searchQuery.length && recent.length"
      class="flex flex-row space-x-2 mt-2"
    >
      <span
        v-for="r in recent.slice().reverse()"
        :key="r.id"
        v-on:click="selectRetailer(r)"
        class="rounded-md bg-base-200 px-2 cursor-pointer"
        >{{ r.id }} : {{ r.name }}</span
      >
      <span
        class="rounded-md px-2 cursor-pointer bg-base-200"
        v-if="props.allowNone"
        v-on:click="selectRetailer(null)"
        >None</span
      >
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from "vue";
import { httpClient } from "@/services/http.js";

const loading = ref(false);
const retailers = ref([]);
const total = ref(0);
const recent = ref([]);

let searchTimer = null;
let searchQuery = ref("");

const props = defineProps({
  allowNone: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["selected"]);

const loadRetailers = async () => {
  loading.value = true;
  try {
    let q = "limit=10";
    if (searchQuery.value.length) {
      q += `&q=${searchQuery.value}`;
    }
    const response = await httpClient.get(`/api/retailers?${q}`, null, null);
    retailers.value = response["items"];
    total.value = response["total"];
  } finally {
    loading.value = false;
  }
};

watch(searchQuery, async (query) => {
  if (searchTimer) {
    clearTimeout(searchTimer);
    searchTimer = null;
  }
  if (!query?.length) {
    retailers.value = [];
    total.value = 0;
    return;
  }
  searchTimer = setTimeout(async () => {
    await loadRetailers();
  }, 800);
});

const addRecent = (retailer) => {
  if (!retailer) {
    return;
  }
  const r = [...recent.value.filter((r) => r.id !== retailer.id)];
  r.push(retailer);
  recent.value = r.slice(-4);
  localStorage.setItem("recent_retailers", JSON.stringify(recent.value));
};

const selectRetailer = (retailer) => {
  searchQuery.value = "";
  retailers.value = [];
  total.value = 0;
  addRecent(retailer);
  emit("selected", retailer);
};

const loadRecent = () => {
  const recentSaved = localStorage.getItem("recent_retailers");
  try {
    if (recentSaved) {
      recent.value = JSON.parse(recentSaved);
    }
  } catch (e) {
    console.log(e);
  }
};

onMounted(async () => {
  loadRecent();
});
</script>
