<template>
  <div class="flex flex-col space-y-4 py-4 flex-wrap">
    <div
      class="flex flex-col space-y-2 md:flex-row md:space-x-2 md:space-y-0"
      v-if="summary"
    >
      <div v-for="pt in paymentTypes" :key="pt">
        <balance-sheet-row :row="summary" :payment-type="pt" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { httpClient } from "@/services/http.js";
import { useMeStore } from "@/stores/index.js";
import BalanceSheetRow from "@/components/BalanceSheetRow.vue";

const data = ref(null);

const meStore = useMeStore();

const paymentTypes = ["cash", "rtgs", "fine"];

const summary = computed(() => {
  if (!data.value) {
    return null;
  }

  let res = { ...data.value[0] };

  for (let i = 1; i < data.value.length; i++) {
    const item = data.value[i];
    for (const pt of paymentTypes) {
      res[`${pt}_products`] += item[`${pt}_products`];
      res[`${pt}_payments`] += item[`${pt}_payments`];
      if (!res[`${pt}_due_date`]) {
        res[`${pt}_due_date`] = item[`${pt}_due_date`];
        res[`${pt}_to_pay`] += item[`${pt}_to_pay`];
      } else if (item[`${pt}_due_date`] === res[`${pt}_due_date`]) {
        res[`${pt}_to_pay`] += item[`${pt}_to_pay`];
      } else if (item[`${pt}_due_date`] < res[`${pt}_due_date`]) {
        res[`${pt}_due_date`] = item[`${pt}_due_date`];
        res[`${pt}_to_pay`] = item[`${pt}_to_pay`];
      }
    }
  }

  return res;
});

onMounted(async () => {
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
    console.log(data.value);
  } catch (error) {
    console.error(error);
  }
});
</script>
