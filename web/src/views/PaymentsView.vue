<template>
  <navbar>
    <payments-list
      :supplier-id="supplierId"
      :retailer-id="retailerId"
      :key="paymentsListVersion"
    />
  </navbar>
</template>

<script setup>
import Navbar from "@/components/Navbar.vue";
import { useMeStore } from "@/stores/index.js";
import { storeToRefs } from "pinia";
import PaymentsList from "@/components/PaymentsList.vue";
import { ref } from "vue";

const paymentsListVersion = ref(0);

const meStore = useMeStore();

const { retailerId, supplierId } = storeToRefs(meStore);
</script>
