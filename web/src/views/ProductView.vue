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
              <td>{{ details.weight }}</td>
            </tr>
            <tr>
              <td>Quality</td>
              <td>{{ details.quality }}</td>
            </tr>
            <tr>
              <td>Rate per gram</td>
              <td>{{ details.rate_per_gram }}</td>
            </tr>
            <tr>
              <td>Total amount</td>
              <td>{{ details.total_amount }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </article>
  </Navbar>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { httpClient } from "@/services/http.js";
import router from "@/router/index.js";
import Navbar from "@/components/Navbar.vue";

const productId = ref(parseInt(router.currentRoute.value.params.id));
const details = ref(null);
const loading = ref(true);

onMounted(async () => {
  loading.value = true;
  try {
    const res = await httpClient.get(`/api/products/${productId.value}`);
    details.value = res;
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
});
</script>
