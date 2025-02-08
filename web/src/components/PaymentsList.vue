<template>
  <div class="flex flex-col space-y-4">
    <div class="flex flex-row space-x-2 mt-4 justify-between">
      <div>
        <retailer-picker-modal v-if="isSupplier" v-on:selected="setRetailer" />
        <supplier-picker-modal v-else v-on:selected="setSupplier" />
      </div>
    </div>
    <placeholder v-if="!payments?.length && !loading" text="-" />
    <placeholder v-if="loading" loading />
    <div class="overflow-x-auto" v-if="payments?.length && !loading">
      <table class="table table-zebra">
        <thead>
          <tr>
            <th>Payment</th>
            <th>{{ isSupplier ? "Retailer" : "Supplier" }}</th>
            <th>Date</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="payment in payments" :key="payment.id">
            <td>
              <RouterLink :to="`/payments/${payment.id}`" class="link">{{
                paymentStr(payment)
              }}</RouterLink>
            </td>
            <td>
              {{
                isSupplier
                  ? `${payment.retailer.id} : ${payment.retailer.name}`
                  : `${payment.supplier.id} : ${payment.supplier.name}`
              }}
            </td>
            <td>
              {{ payment.date }}
            </td>
            <td><status-badge :status="payment.status" size="sm" /></td>
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
import StatusBadge from "@/components/StatusBadge.vue";
import { useMeStore } from "@/stores/index.js";
import { storeToRefs } from "pinia";
import { RouterLink } from "vue-router";

const props = defineProps({
  retailerId: Number,
  supplierId: Number,
});

const meStore = useMeStore();
const { isSupplier } = storeToRefs(meStore);

const payments = ref([]);
const total = ref(0);
const page = ref(1);
const limit = ref(20);
const loading = ref(false);
const supplierId = ref(props.supplierId);
const retailerId = ref(props.retailerId);

const pages = computed(() => Math.ceil(total.value / limit.value));

const paymentStr = (payment) => {
  if (payment.type === "fine") {
    return `${payment.type} ${payment.weight}g @ ${payment.quality}%`;
  } else {
    return `${payment.type} ${payment.amount}₹`;
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
};

const setRetailer = (retailer) => {
  retailerId.value = retailer?.id;
  loadPage(1);
};

onMounted(async () => {
  await loadPage(1);
});
</script>
