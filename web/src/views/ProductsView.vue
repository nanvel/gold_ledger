<template>
  <Navbar>
    <div class="py-4">
      <ProductsList
        :supplier-id="supplierId"
        :retailer-id="retailerId"
        v-if="supplierId || retailerId"
        :key="refreshKey"
      />
    </div>
  </Navbar>
</template>

<script setup>
import Navbar from "@/components/Navbar.vue";
import ProductsList from "@/components/ProductsList.vue";
import { useMeStore } from "@/stores/index.js";
import { storeToRefs } from "pinia";

const meStore = useMeStore();

const { supplierId, retailerId, refreshKey } = storeToRefs(meStore);
</script>
