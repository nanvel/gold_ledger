<template>
  <div class="flex flex-col space-y-4">
    <placeholder v-if="!retailers?.length && !loading" text="-" />
    <placeholder v-if="loading" loading />
    <div class="overflow-x-auto" v-if="retailers?.length && !loading">
      <table class="table table-zebra">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Added</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="retailer in retailers" :key="retailer.id">
            <td>
              {{ retailer.id }}
            </td>
            <td>
              {{ retailer.name }}
            </td>
            <td>
              <timestamp :value="retailer.added_at" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="join" v-if="!loading && total > 0">
      <button
        class="join-item btn"
        v-if="page > 1"
        v-on:click="loadPage(page - 1)"
      >
        «
      </button>
      <button class="join-item btn">
        Page {{ page }} / {{ pages }} <small>Total: {{ total }}</small>
      </button>
      <button
        class="join-item btn"
        v-if="page < pages"
        v-on:click="loadPage(page + 1)"
      >
        »
      </button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import { httpClient } from "@/services/http.js";
import Placeholder from "@/components/Placeholder.vue";
import Timestamp from "@/components/Timestamp.vue";

const retailers = ref([]);
const total = ref(0);
const page = ref(1);
const limit = ref(20);
const loading = ref(false);

const pages = computed(() => Math.ceil(total.value / limit.value));

const loadPage = async (p) => {
  page.value = p;
  let q = `?offset=${(page.value - 1) * limit.value}&limit=${limit.value}`;
  loading.value = true;
  try {
    const resp = await httpClient.get(`/api/retailers${q}`, null, null);
    retailers.value = resp["items"];
    total.value = resp["total"];
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  await loadPage(1);
});
</script>
