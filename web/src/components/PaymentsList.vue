<template>
  <div class="flex flex-col space-y-1 py-2">
    <div>Products received: {{ totalProducts }}</div>
    <div>Payments confirmed: {{ totalPayments }}</div>
    <div>Pending payments: {{ totalPending }} ({{ totalOverdue }} overdue)</div>
  </div>
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
const totalProducts = ref(0);
const totalPayments = ref(0);
const totalPending = ref(0);
const totalOverdue = ref(0);

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

const loadSummary = async () => {
  loading.value = true;
  try {
    let q = "";
    if (props.retailerId && props.supplierId) {
      q = `?retailer_id=${props.retailerId}&supplier_id=${props.supplierId}`;
    } else if (props.retailerId) {
      q = `?retailer_id=${props.retailerId}`;
    } else if (props.supplierId) {
      q = `?supplier_id=${props.supplierId}`;
    }
    const resp = await httpClient.get(`/api/payments-summary${q}`, null, null);
    totalProducts.value = resp["total_products"];
    totalPayments.value = resp["total_payments"];
    totalPending.value = resp["total_pending"];
    totalOverdue.value = resp["total_overdue"];
  } finally {
    loading.value = false;
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
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  await loadPage(1);
  await loadSummary();
});
</script>
