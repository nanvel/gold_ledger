<template>
  <Navbar>
    <div class="flex flex-col space-y-4 py-4 flex-wrap">
      <div
        class="flex flex-col space-y-2 md:flex-row md:space-x-2 md:space-y-0"
        v-if="summary"
      >
        <div v-for="pt in paymentTypes" :key="pt">
          <balance-sheet-row :row="summary" :payment-type="pt" />
        </div>
      </div>

      <div class="divider"></div>

      <div class="form-control w-full max-w-sm">
        <div class="label">
          <span class="label-text">{{
            `Filter by ${isSupplier ? "retailer" : "supplier"}`
          }}</span>
        </div>
        <div class="input input-bordered flex items-center gap-2">
          <input type="text" class="grow" v-model="searchQuery" />
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 16 16"
            fill="currentColor"
            class="h-4 w-4 opacity-70"
          >
            <path
              fill-rule="evenodd"
              d="M9.965 11.026a5 5 0 1 1 1.06-1.06l2.755 2.754a.75.75 0 1 1-1.06 1.06l-2.755-2.754ZM10.5 7a3.5 3.5 0 1 1-7 0 3.5 3.5 0 0 1 7 0Z"
              clip-rule="evenodd"
            />
          </svg>
        </div>
      </div>

      <div v-for="row in items" :key="row.id" class="flex flex-col space-y-2">
        <div class="mt-2" v-if="isSupplier">
          {{ row.retailer.id }} : {{ row.retailer.name }}
        </div>
        <div class="mt-2" v-else>
          {{ row.supplier.id }} : {{ row.supplier.name }}
        </div>
        <div
          class="flex flex-col space-y-2 md:flex-row md:space-x-2 md:space-y-0"
        >
          <balance-sheet-row
            :row="row"
            :payment-type="pt"
            v-for="pt in paymentTypes"
            :key="pt"
          />
        </div>
      </div>
    </div>
  </Navbar>
</template>

<script setup>
import Navbar from "@/components/Navbar.vue";
import { ref, onMounted, computed } from "vue";
import { httpClient } from "@/services/http.js";
import { useMeStore } from "@/stores/index.js";
import { storeToRefs } from "pinia";
import BalanceSheetRow from "@/components/BalanceSheetRow.vue";

const data = ref(null);
const searchQuery = ref("");

const meStore = useMeStore();

const { isSupplier } = storeToRefs(meStore);

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

const items = computed(() => {
  if (!data.value) {
    return [];
  }

  const searchId = /^\d+$/.test(searchQuery.value)
    ? parseInt(searchQuery.value)
    : null;

  return data.value.filter((item) => {
    if (!searchQuery.value) {
      return true;
    }

    if (isSupplier) {
      if (searchId) {
        return item.retailer.id === parseInt(searchQuery.value);
      } else {
        return item.retailer.name
          .toLowerCase()
          .includes(searchQuery.value.toLowerCase());
      }
    } else {
      if (searchId) {
        return item.supplier.id === parseInt(searchQuery.value);
      } else {
        return item.supplier.name
          .toLowerCase()
          .includes(searchQuery.value.toLowerCase());
      }
    }
  });
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
