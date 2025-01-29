<template>
  <div class="mt-4">Total: {{ amountSum }}</div>
  <div class="flex flex-col space-y-2">
    <div class="overflow-x-auto">
      <table class="table table-zebra">
        <thead>
          <tr>
            <th>Type</th>
            <th>Date</th>
            <th>Total</th>
            <th>Created</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="payment in payments" :key="payment.id">
            <td>
              {{ payment.type }}
            </td>
            <td>
              {{ payment.date }}
            </td>
            <td>
              {{ payment.total_amount }}
            </td>
            <td>
              <timestamp :value="payment.created_at" :show-duration="true" />
            </td>
            <td>{{ parseStatus(payment) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="join mt-8" v-if="!loading && total > 0">
    <button
      class="join-item btn"
      v-if="page > 1"
      v-on:click="loadPage(page - 1)"
    >
      «
    </button>
    <button class="join-item btn">
      Page {{ page }} / {{ pages }} <small>Total: {{ total }}</small>
    </button>
    <button
      class="join-item btn"
      v-if="page < pages"
      v-on:click="loadPage(page + 1)"
    >
      »
    </button>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import { httpClient } from "@/services/http.js";
import Timestamp from "@/components/Timestamp.vue";

const props = defineProps({
  retailerId: Number,
  supplierId: Number,
});

const payments = ref([]);
const total = ref(0);
const page = ref(1);
const limit = ref(20);
const loading = ref(false);
const amountSum = ref(null);

const pages = computed(() => Math.ceil(total.value / limit.value));

const parseStatus = (payment) => {
  if (payment.rejected_by) {
    return "Rejected";
  } else if (payment.confirmed_by) {
    return "Confirmed";
  } else {
    return "Pending";
  }
};

const loadPage = async (p) => {
  page.value = p;
  let q = `?offset=${(page.value - 1) * limit.value}&limit=${limit.value}`;
  if (props.retailerId) {
    q += `&retailer_id=${props.retailerId}`;
  }
  if (props.supplierId) {
    q += `&supplier_id=${props.supplierId}`;
  }
  loading.value = true;
  try {
    const resp = await httpClient.get(`/api/payments${q}`, null, null);
    payments.value = resp["items"];
    total.value = resp["total"];
    amountSum.value = resp["amount_sum"];
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  await loadPage(1);
});
</script>
