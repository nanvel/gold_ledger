<template>
  <Navbar>
    <div v-for="row in data" :key="row.id" v-if="data" class="flex flex-col">
      <div class="mt-2" v-if="isSupplier">
        {{ row.retailer.id }} : {{ row.retailer.name }}
      </div>
      <div class="mt-2" v-else>
        {{ row.supplier.id }} : {{ row.supplier.name }}
      </div>
      <table class="table table-sm table-zebra max-w-xl">
        <thead>
          <tr>
            <th></th>
            <th v-for="pt in paymentTypes" :key="pt" class="capitalize">
              {{ pt }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Products</td>
            <td v-for="pt in paymentTypes" :key="pt">
              {{ row[`${pt}_products`] }}
            </td>
          </tr>
          <tr>
            <td>Payment</td>
            <td v-for="pt in paymentTypes" :key="pt">
              {{ row[`${pt}_payments`] }}
            </td>
          </tr>
          <tr>
            <td>Pending</td>
            <td v-for="pt in paymentTypes" :key="pt">
              {{
                parseFloat(row[`${pt}_products`]) -
                parseFloat(row[`${pt}_payments`])
              }}
            </td>
          </tr>
          <tr>
            <td>Next payment</td>
            <td v-for="pt in paymentTypes" :key="pt">
              {{ row[`${pt}_due_date`] }} {{ row[`${pt}_to_pay`] }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </Navbar>
</template>

<script setup>
import Navbar from "@/components/Navbar.vue";
import { ref, onMounted } from "vue";
import { httpClient } from "@/services/http.js";
import { useMeStore } from "@/stores/index.js";
import { storeToRefs } from "pinia";

const data = ref(null);

const meStore = useMeStore();

const { isSupplier } = storeToRefs(meStore);

const paymentTypes = ["cash", "rtgs", "fine"];

onMounted(async () => {
  try {
    const response = await httpClient.get("/api/accounting");
    data.value = response.items;
  } catch (error) {
    console.error(error);
  }
});
</script>
