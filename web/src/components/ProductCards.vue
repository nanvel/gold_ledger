<template>
  <div class="flex flex-row flex-wrap justify-start">
    <div
      class="card bg-base-100 border-neutral border-2 w-96 mx-2 my-2"
      v-for="product in props.products"
      :key="product.id"
    >
      <div class="card-body">
        <h2 class="card-title">{{ product.name }}</h2>
        <p>
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
                  <td>Total amount</td>
                  <td>{{ product.total_amount }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from "vue";
import Timestamp from "@/components/Timestamp.vue";

const props = defineProps({
  products: Array,
});
</script>
