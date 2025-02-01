<template>
  <Navbar>
    <article class="prose lg:prose-xl py-4 px-2" v-if="details">
      <h2>{{ details.name }}</h2>

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
              <td>Type</td>
              <td>{{ details.type }}</td>
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
              <td>Amount</td>
              <td>{{ details.amount }}</td>
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
          v-on:click="confirmPayment"
          v-if="isSupplier"
        >
          Confirm
        </button>
        <button
          class="btn btn-secondary"
          v-on:click="rejectPayment"
          v-if="isSupplier"
        >
          Reject
        </button>
        <button
          class="btn btn-secondary"
          v-on:click="cancelPayment"
          v-if="!isSupplier"
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

const { isSupplier } = storeToRefs(meStore);

const paymentId = ref(parseInt(router.currentRoute.value.params.id));
const details = ref(null);
const loading = ref(true);

const confirmPayment = async () => {
  try {
    await httpClient.post(`/api/payments/${paymentId.value}/confirm`);
    await loadPayment();
  } catch (error) {
    console.error(error);
  }
};

const rejectPayment = async () => {
  try {
    await httpClient.post(`/api/payments/${paymentId.value}/reject`);
    await loadPayment();
  } catch (error) {
    console.error(error);
  }
};

const cancelPayment = async () => {
  try {
    await httpClient.post(`/api/payments/${paymentId.value}/cancel`);
    await loadPayment();
  } catch (error) {
    console.error(error);
  }
};

const loadPayment = async () => {
  loading.value = true;
  try {
    details.value = await httpClient.get(`/api/payments/${paymentId.value}`);
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  await loadPayment();
});
</script>
