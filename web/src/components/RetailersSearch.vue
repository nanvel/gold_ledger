<template>
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
</template>

<script setup>
import { onMounted, ref } from "vue";
import Timestamp from "@/components/Timestamp.vue";
import { httpClient } from "@/services/http.js";

const loading = ref(false);
const retailers = ref([]);
const total = ref(0);

onMounted(async () => {
  loading.value = true;
  try {
    const response = await httpClient.get("/api/retailers", null, null);
    retailers.value = response["items"];
    total.value = response["total"];
  } finally {
    loading.value = false;
  }
});
</script>
