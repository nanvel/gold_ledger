<template>
  <navbar>
    <div class="py-4">
      <payments-list
        :supplier-id="supplierId"
        :retailer-id="retailerId"
        :key="refreshKey"
      />
    </div>
  </navbar>
</template>

<script setup>
import Navbar from "@/components/Navbar.vue";
import { useMeStore } from "@/stores/index.js";
import { storeToRefs } from "pinia";
import PaymentsList from "@/components/PaymentsList.vue";

const meStore = useMeStore();

const { retailerId, supplierId, refreshKey } = storeToRefs(meStore);
</script>
