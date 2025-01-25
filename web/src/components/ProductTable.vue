<template>
  <div class="overflow-x-auto">
    <table class="table table-zebra">
      <thead>
        <tr>
          <th>Name</th>
          <th>Date</th>
          <th>Total</th>
          <th>Created</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in props.products" :key="product.id">
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
import { defineProps } from "vue";
import Timestamp from "@/components/Timestamp.vue";

const props = defineProps({
  products: Array,
});
</script>
