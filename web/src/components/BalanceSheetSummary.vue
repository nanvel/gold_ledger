<template>
  <div
    class="flex flex-col space-y-2 md:flex-row md:space-x-2 md:space-y-0"
    v-if="summary && !loading"
  >
    <balance-sheet-row
      :row="summary"
      :payment-type="pt"
      v-for="pt in paymentTypes"
      :key="pt"
    />
  </div>
  <placeholder v-if="loading" loading />
  <placeholder v-else-if="!summary && !loading" text="-" />
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { httpClient } from "@/services/http.js";
import BalanceSheetRow from "@/components/BalanceSheetRow.vue";
import Placeholder from "@/components/Placeholder.vue";

const data = ref(null);
const loading = ref(false);

const paymentTypes = ["cash", "rtgs", "fine"];

const summary = computed(() => {
  if (!data.value) {
    return null;
  }

  const res = {
    cash_products: 0,
    cash_payments: 0,
    rtgs_products: 0,
    rtgs_payments: 0,
    fine_products: 0,
    fine_payments: 0,
    due_payments: [],
  };

  data.value.forEach((item) => {
    for (const pt of paymentTypes) {
      res[`${pt}_products`] += item[`${pt}_products`];
      res[`${pt}_payments`] += item[`${pt}_payments`];
    }
    item.due_payments.forEach((payment) => {
      res.due_payments.push({ ...payment });
    });
  });

  // find sum of amounts for each type and date
  const sum = {
    cash: {},
    rtgs: {},
    fine: {},
  };
  res.due_payments.forEach((payment) => {
    if (!sum[payment.type][payment.date]) {
      sum[payment.type][payment.date] = 0;
    }
    sum[payment.type][payment.date] += payment.amount;
  });
  // back to array
  res.due_payments = Object.keys(sum)
    .map((type) => {
      return Object.keys(sum[type]).map((date) => {
        return {
          type,
          date,
          amount: sum[type][date],
        };
      });
    })
    .flat();

  return res;
});

onMounted(async () => {
  loading.value = true;
  try {
    const response = await httpClient.get("/api/balance-sheet");
    data.value = response.items.map((item) => {
      return {
        ...item,
        cash_products: parseFloat(item.cash_products),
        cash_payments: parseFloat(item.cash_payments),
        cash_to_pay: parseFloat(item.cash_to_pay),
        rtgs_products: parseFloat(item.rtgs_products),
        rtgs_payments: parseFloat(item.rtgs_payments),
        rtgs_to_pay: parseFloat(item.rtgs_to_pay),
        fine_products: parseFloat(item.fine_products),
        fine_payments: parseFloat(item.fine_payments),
        fine_to_pay: parseFloat(item.fine_to_pay),
      };
    });
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
});
</script>
