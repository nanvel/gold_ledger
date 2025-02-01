<template>
  <div class="flex flex-col space-y-4">
    <div class="flex flex-col space-y-1 py-2">
      <div>Products received: {{ totalProducts }}</div>
      <div>Payments confirmed: {{ totalPayments }}</div>
      <div>
        Pending payments: {{ totalPending }} ({{ totalOverdue }} overdue)
      </div>
    </div>
    <div class="flex flex-row space-x-2 mt-4 justify-between">
      <div>
        <retailer-picker-modal v-if="isSupplier" v-on:selected="setRetailer" />
        <supplier-picker-modal v-else v-on:selected="setSupplier" />
      </div>
    </div>
    <placeholder
      v-if="!payments?.length && !loading"
      text="No payments found"
    />
    <placeholder v-if="loading" loading text="Loading" />
    <div class="overflow-x-auto" v-if="payments?.length && !loading">
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
              {{ payment.amount }}
            </td>
            <td>
              <timestamp :value="payment.created_at" :show-duration="true" />
            </td>
            <td>{{ parseStatus(payment) }}</td>
          </tr>
        </tbody>
      </table>
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
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import { httpClient } from "@/services/http.js";
import Timestamp from "@/components/Timestamp.vue";
import RetailerPickerModal from "@/components/RetailerPickerModal.vue";
import SupplierPickerModal from "@/components/SupplierPickerModal.vue";
import Placeholder from "@/components/Placeholder.vue";

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
const supplierId = ref(props.supplierId);
const retailerId = ref(props.retailerId);

const isSupplier = computed(() => props.supplierId);

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
    if (retailerId.value && supplierId.value) {
      q = `?retailer_id=${retailerId.value}&supplier_id=${supplierId.value}`;
    } else if (retailerId.value) {
      q = `?retailer_id=${retailerId.value}`;
    } else if (supplierId.value) {
      q = `?supplier_id=${supplierId.value}`;
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
  if (retailerId.value) {
    q += `&retailer_id=${retailerId.value}`;
  }
  if (supplierId.value) {
    q += `&supplier_id=${supplierId.value}`;
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

const setSupplier = (supplier) => {
  supplierId.value = supplier?.id;
  loadPage(1);
  loadSummary();
};

const setRetailer = (retailer) => {
  retailerId.value = retailer?.id;
  loadPage(1);
  loadSummary();
};

onMounted(async () => {
  await loadPage(1);
  await loadSummary();
});
</script>
