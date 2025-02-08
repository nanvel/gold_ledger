<template>
  <div class="flex flex-col space-y-4">
    <Placeholder v-if="!payments?.length && !loading" text="-" />
    <Placeholder v-if="loading" loading text="Loading" />
    <div class="overflow-x-auto" v-if="payments?.length && !loading">
      <table class="table table-zebra">
        <thead>
          <tr>
            <th>Payment</th>
            <th>Supplier</th>
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
              {{ `${payment.supplier.id} : ${payment.supplier.name}` }}
            </td>
            <td>
              {{ payment.date }}
            </td>
            <td><status-badge :status="payment.status" size="sm" /></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, defineEmits } from "vue";
import { httpClient } from "@/services/http.js";
import Placeholder from "@/components/Placeholder.vue";
import { RouterLink } from "vue-router";
import StatusBadge from "@/components/StatusBadge.vue";

const emit = defineEmits(["setTotal"]);

const payments = ref([]);
const total = ref(0);
const loading = ref(false);

const paymentStr = (payment) => {
  if (payment.type === "fine") {
    return `${payment.type} ${payment.weight}g @ ${payment.quality}%`;
  } else {
    return `${payment.type} ${payment.amount}₹`;
  }
};

onMounted(async () => {
  let q = `?limit=10&status=1&reverse=false`;
  loading.value = true;
  try {
    const resp = await httpClient.get(`/api/payments${q}`, null, null);
    payments.value = resp["items"];
    total.value = resp["total"];
    emit("setTotal", total.value);
  } finally {
    loading.value = false;
  }
});
</script>
