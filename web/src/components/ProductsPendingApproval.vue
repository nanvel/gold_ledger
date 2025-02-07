<template>
  <div class="flex flex-col space-y-4">
    <Placeholder
      v-if="!products?.length && !loading"
      text="No products to confirm"
    />
    <Placeholder v-if="loading" loading text="Loading" />
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import { httpClient } from "@/services/http.js";
import Placeholder from "@/components/Placeholder.vue";

const products = ref([]);
const total = ref(0);
const loading = ref(false);

onMounted(async () => {
  let q = `?limit=10`;
  loading.value = true;
  try {
    const resp = await httpClient.get(`/api/products${q}`, null, null);
    products.value = resp["items"];
    total.value = resp["total"];
  } finally {
    loading.value = false;
  }
});
</script>
