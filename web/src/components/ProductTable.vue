<template>
  <div class="overflow-x-auto">
    <table class="table table-zebra">
      <thead>
        <tr>
          <th>Name</th>
          <th>{{ isSupplier ? "Retailer" : "Supplier" }}</th>
          <th>Date</th>
          <th>Payment</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in props.products" :key="product.id">
          <td>
            <RouterLink :to="`/products/${product.id}`" class="link">{{
              product.name
            }}</RouterLink>
          </td>
          <td>
            {{
              isSupplier
                ? `${product.retailer.id} : ${product.retailer.name}`
                : `${product.supplier.id} : ${product.supplier.name}`
            }}
          </td>
          <td>
            {{ product.date }}
          </td>
          <td>
            {{ computePayment(product) }}
          </td>
          <td><status-badge :status="product.status" size="md" /></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";
import StatusBadge from "@/components/StatusBadge.vue";
import { useMeStore } from "@/stores/index.js";
import { storeToRefs } from "pinia";

const props = defineProps({
  products: Array,
});

const meStore = useMeStore();
const { isSupplier } = storeToRefs(meStore);

const computePayment = (product) => {
  if (product.payment_type === "fine") {
    return `${product.payment_type} ${product.payment_weight}g @ ${product.payment_quality}% by ${product.payment_due_date}`;
  } else {
    return `${product.payment_type} ${product.payment_amount}₹ by ${product.payment_due_date}`;
  }
};
</script>
