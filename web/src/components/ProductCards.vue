<template>
  <div class="flex flex-row flex-wrap justify-start">
    <div
      class="card bg-base-100 border-base-300 border-2 w-96 mx-2 my-2"
      v-for="product in props.products"
      :key="product.id"
    >
      <div class="card-body" style="padding: 1rem">
        <h2 class="card-title">
          <RouterLink :to="`/products/${product.id}`">{{
            product.name
          }}</RouterLink>
          <status-badge :status="product.status" size="md" />
        </h2>
        <div>
          <img
            v-if="product.images?.length"
            :src="product.images[0].thumb_url"
            :alt="product.name"
          />
          <descriptive-table
            :rows="tableRows(product)"
            size="sm"
            class="mt-2"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";
import DescriptiveTable from "@/components/DescriptiveTable.vue";
import StatusBadge from "@/components/StatusBadge.vue";
import { timestampToString } from "@/services/time.js";
import { useMeStore } from "@/stores/index.js";
import { storeToRefs } from "pinia";

const props = defineProps({
  products: Array,
});

const meStore = useMeStore();
const { isSupplier } = storeToRefs(meStore);

const tableRows = (product) => {
  const res = [
    ["Date", product.date],
    ["Weight", `${product.weight}g`],
    ["Quality", `${product.quality}%`],
    ["Rate", `${product.quality}₹/g`],
  ];
  if (isSupplier) {
    res.push(["Retailer", `${product.retailer.id} : ${product.retailer.name}`]);
  } else {
    res.push(["Supplier", `${product.supplier.id} : ${product.supplier.name}`]);
  }
  if (product.payment_type === "fine") {
    res.push([
      "Payment",
      `${product.payment_type} ${product.payment_weight}g @ ${product.payment_quality}% by ${product.payment_due_date}`,
    ]);
  } else {
    res.push([
      "Payment",
      `${product.payment_type} ${product.payment_amount}₹ by ${product.payment_due_date}`,
    ]);
  }

  res.push(["Created", timestampToString(product.created_at)]);
  return res;
};
</script>
