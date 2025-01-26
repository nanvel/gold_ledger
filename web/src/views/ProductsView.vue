<template>
  <Navbar>
    <div class="py-4">
      <add-product-modal />

      <ProductsList :supplier-id="supplierId" v-if="supplierId" />
    </div>
  </Navbar>
</template>

<script setup>
import Navbar from "@/components/Navbar.vue";
import ProductsList from "@/components/ProductsList.vue";
import { useMeStore } from "@/stores/index.js";
import { storeToRefs } from "pinia";
import AddProductModal from "@/components/AddProductModal.vue";

const meStore = useMeStore();

const { supplierId } = storeToRefs(meStore);
</script>
