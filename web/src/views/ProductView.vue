<template>
  <Navbar>
    <article class="prose lg:prose-xl py-4 px-2" v-if="details">
      <h2>{{ details.name }}</h2>
      <div v-if="details.images?.length">
        <img
          :alt="details.name"
          :src="details.images[0].thumb_url"
          class="rounded-md"
        />
        <a :href="details.images[0].url" target="_blank" class="text-sm"
          >Original image</a
        >
      </div>

      <div class="overflow-x-auto">
        <table class="table table-zebra table-sm">
          <thead>
            <tr>
              <th>Name</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Date</td>
              <td>{{ details.date }}</td>
            </tr>
            <tr>
              <td>Weight</td>
              <td>{{ details.weight }} g</td>
            </tr>
            <tr>
              <td>Quality</td>
              <td>{{ details.quality }} %</td>
            </tr>
            <tr>
              <td>Rate</td>
              <td>{{ details.rate }} ₹/g</td>
            </tr>
            <tr>
              <td>Amount</td>
              <td>{{ details.amount }} ₹</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div
        v-if="
          details &&
          !(details.confirmed_by || details.rejected_by || details.cancelled_by)
        "
        class="flex flex-row space-x-2"
      >
        <button
          class="btn btn-primary"
          v-on:click="confirmProduct"
          v-if="isRetailer"
        >
          Confirm
        </button>
        <button
          class="btn btn-secondary"
          v-on:click="rejectProduct"
          v-if="isRetailer"
        >
          Reject
        </button>
        <button
          class="btn btn-secondary"
          v-on:click="cancelProduct"
          v-if="!isRetailer"
        >
          Cancel
        </button>
      </div>
    </article>
  </Navbar>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { httpClient } from "@/services/http.js";
import router from "@/router/index.js";
import Navbar from "@/components/Navbar.vue";
import { useMeStore } from "@/stores/index.js";
import { storeToRefs } from "pinia";

const meStore = useMeStore();

const { isRetailer } = storeToRefs(meStore);

const productId = ref(parseInt(router.currentRoute.value.params.id));
const details = ref(null);
const loading = ref(true);

const confirmProduct = async () => {
  try {
    await httpClient.post(`/api/products/${productId.value}/confirm`);
    await loadProduct();
  } catch (error) {
    console.error(error);
  }
};

const rejectProduct = async () => {
  try {
    await httpClient.post(`/api/products/${productId.value}/reject`);
    await loadProduct();
  } catch (error) {
    console.error(error);
  }
};

const cancelProduct = async () => {
  try {
    await httpClient.post(`/api/products/${productId.value}/cancel`);
    await loadProduct();
  } catch (error) {
    console.error(error);
  }
};

const loadProduct = async () => {
  loading.value = true;
  try {
    details.value = await httpClient.get(`/api/products/${productId.value}`);
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  await loadProduct();
});
</script>
