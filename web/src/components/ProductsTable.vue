<template>
  <div class="overflow-x-auto">
    <table class="table table-zebra" v-if="products.length && !loading">
      <thead>
        <tr>
          <th>Name</th>
          <th>Date</th>
          <th>Total</th>
          <th>Created</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in products" :key="product.id">
          <td>
            {{ product.name }}
          </td>
          <td>
            <timestamp :value="product.date" />
          </td>
          <td>
            {{ product.total_amount }}
          </td>
          <td>
            <timestamp :value="product.created_at" :show-duration="true" />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { onMounted, ref, defineProps } from "vue";
import { httpClient } from "@/services/http.js";
import Timestamp from "@/components/Timestamp.vue";

const props = defineProps({
  retailerId: Number,
  supplierId: Number,
});

const products = ref([]);
const total = ref(0);
const loading = ref(false);

onMounted(async () => {
  let q = "?limit=20";
  if (props.retailerId) {
    q += `&retailer_id=${props.retailerId}`;
  }
  if (props.supplierId) {
    q += `&supplier_id=${props.supplierId}`;
  }
  loading.value = true;
  try {
    const resp = await httpClient.get(`/api/products?${q}`, null, null);
    products.value = resp["items"];
    total.value = resp["total"];
  } finally {
    loading.value = false;
  }
});
</script>
