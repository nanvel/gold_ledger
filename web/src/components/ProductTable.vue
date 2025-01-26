<template>
  <div class="overflow-x-auto">
    <table class="table table-zebra">
      <thead>
        <tr>
          <th>Name</th>
          <th>Date</th>
          <th>Total</th>
          <th>Created</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in props.products" :key="product.id">
          <td>
            <RouterLink :to="`/products/${product.id}`">{{
              product.name
            }}</RouterLink>
          </td>
          <td>
            {{ product.date }}
          </td>
          <td>
            {{ product.total_amount }}
          </td>
          <td>
            <timestamp :value="product.created_at" :show-duration="true" />
          </td>
          <td>{{ parseStatus(product) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";

const props = defineProps({
  products: Array,
});

const parseStatus = (product) => {
  if (product.rejected_by) {
    return "Rejected";
  } else if (product.confirmed_by) {
    return "Confirmed";
  } else {
    return "Pending";
  }
};
</script>
