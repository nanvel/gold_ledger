<template>
  <div class="flex flex-row flex-wrap justify-start">
    <div
      class="card bg-base-100 border-neutral border-2 w-96 mx-2 my-2"
      v-for="product in props.products"
      :key="product.id"
    >
      <div class="card-body">
        <h2 class="card-title">
          <RouterLink :to="`/products/${product.id}`">{{
            product.name
          }}</RouterLink>
        </h2>
        <div>
          <img
            v-if="product.images?.length"
            :src="product.images[0].thumb_url"
            :alt="product.name"
          />
          <div class="overflow-x-auto">
            <table class="table table-zebra">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Value</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Date</td>
                  <td>{{ product.date }}</td>
                </tr>
                <tr>
                  <td>Weight</td>
                  <td>{{ product.weight }}</td>
                </tr>
                <tr>
                  <td>Quality</td>
                  <td>{{ product.quality }}</td>
                </tr>
                <tr>
                  <td>Rate per gram</td>
                  <td>{{ product.rate_per_gram }}</td>
                </tr>
                <tr>
                  <td>Amount</td>
                  <td>{{ product.amount }}</td>
                </tr>
                <tr>
                  <td>Status</td>
                  <td>{{ parseStatus(product) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
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
