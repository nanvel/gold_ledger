<template>
  <div>
    <label class="form-control w-full max-w-2xl">
      <label class="input input-bordered flex items-center gap-2">
        <input
          type="text"
          class="grow"
          placeholder="Search"
          v-model="searchQuery"
        />
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
      </label>
      <div class="label">
        <span class="label-text-alt" v-if="!loading">Found: {{ total }}</span>
        <span class="label-text-alt" v-else>Loading...</span>
      </div>
    </label>
    <div class="overflow-x-auto">
      <table class="table table-zebra" v-if="retailers.length && !loading">
        <thead>
          <tr>
            <th>Name</th>
            <th>Created</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="retailer in retailers" :key="retailer.id">
            <td>
              <RouterLink :to="`/retailers/${retailer.id}`">{{
                retailer.name
              }}</RouterLink>
            </td>
            <td>
              <timestamp :value="retailer.created_at" :show-duration="true" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from "vue";
import Timestamp from "@/components/Timestamp.vue";
import { httpClient } from "@/services/http.js";

const loading = ref(false);
const retailers = ref([]);
const total = ref(0);

let searchTimer = null;
let searchQuery = ref("");

const loadRetailers = async () => {
  loading.value = true;
  try {
    let q = "limit=20";
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
  searchTimer = setTimeout(async () => {
    await loadRetailers();
  }, 800);
});

onMounted(async () => {
  await loadRetailers();
});
</script>
