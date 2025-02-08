<template>
  <div class="flex flex-col space-y-4">
    <Placeholder v-if="!products?.length && !loading" text="-" />
    <Placeholder v-if="loading" loading />
    <div class="overflow-x-auto" v-if="products?.length">
      <table class="table table-zebra">
        <thead>
          <tr>
            <th>Name</th>
            <th>Supplier</th>
            <th>Created</th>
            <th>Payment</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in products" :key="product.id">
            <td>
              <RouterLink :to="`/products/${product.id}`" class="link">{{
                product.name
              }}</RouterLink>
            </td>
            <td>
              {{ `${product.supplier.id} : ${product.supplier.name}` }}
            </td>
            <td>
              {{ timestampToString(product.created_at) }}
            </td>
            <td>
              {{ computePayment(product) }}
            </td>
            <td><status-badge :status="product.status" size="md" /></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { httpClient } from "@/services/http.js";
import Placeholder from "@/components/Placeholder.vue";
import { RouterLink } from "vue-router";
import StatusBadge from "@/components/StatusBadge.vue";
import { timestampToString } from "@/services/time.js";

const products = ref([]);
const total = ref(0);
const loading = ref(false);

const emit = defineEmits(["setTotal"]);

const computePayment = (product) => {
  if (product.payment_type === "fine") {
    return `${product.payment_type} ${product.payment_weight}g @ ${product.payment_quality}% by ${product.payment_due_date}`;
  } else {
    return `${product.payment_type} ${product.payment_amount}₹ by ${product.payment_due_date}`;
  }
};

onMounted(async () => {
  let q = `?limit=10&status=1&reverse=false`;
  loading.value = true;
  try {
    const resp = await httpClient.get(`/api/products${q}`, null, null);
    products.value = resp["items"];
    total.value = resp["total"];
    emit("setTotal", total.value);
  } finally {
    loading.value = false;
  }
});
</script>
