<template>
  <Navbar>
    <retailer-picker />

    <ProductsList :supplier-id="supplierId" v-if="supplierId" />
  </Navbar>
</template>

<script setup>
import Navbar from "@/components/Navbar.vue";
import ProductsList from "@/components/ProductsList.vue";
import { useMeStore } from "@/stores/index.js";
import { storeToRefs } from "pinia";
import RetailerPicker from "@/components/RetailerPicker.vue";

const meStore = useMeStore();

const { supplierId } = storeToRefs(meStore);
</script>
