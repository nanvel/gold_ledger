<template>
  <Navbar>
    <div v-for="row in data" :key="row.id" v-if="data" class="flex flex-col">
      <div class="mt-2">{{ row.id }} : {{ row.name }}</div>
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
              {{ row[pt]?.products || "0" }}
            </td>
          </tr>
          <tr>
            <td>Confirmed</td>
            <td v-for="pt in paymentTypes" :key="pt">
              {{ row[pt]?.confirmed || "0" }}
            </td>
          </tr>
          <tr>
            <td>Pending</td>
            <td v-for="pt in paymentTypes" :key="pt">
              {{ row[pt]?.pending || "0" }}
            </td>
          </tr>
          <tr>
            <td>Sum</td>
            <td v-for="pt in paymentTypes" :key="pt">
              {{ row[pt]?.sum || "0" }}
            </td>
          </tr>
          <tr>
            <td>Overdue</td>
            <td v-for="pt in paymentTypes" :key="pt">
              {{ row[pt]?.overdue || "0" }}
            </td>
          </tr>
          <tr>
            <td>Due today</td>
            <td v-for="pt in paymentTypes" :key="pt">
              {{ row[pt]?.due_today || "0" }}
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

const data = ref(null);

const paymentTypes = ["cash", "rtgs", "fine"];

onMounted(async () => {
  try {
    const response = await httpClient.get("/api/accounting");
    data.value = response;
  } catch (error) {
    console.error(error);
  }
});
</script>
