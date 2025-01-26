<template>
  <Navbar>
    <div class="py-4">
      <add-product-modal v-on:product-added="productsListVersion += 1" />

      <ProductsList
        :supplier-id="supplierId"
        v-if="supplierId"
        :key="productsListVersion"
      />
    </div>
  </Navbar>
</template>

<script setup>
import { ref } from "vue";
import Navbar from "@/components/Navbar.vue";
import ProductsList from "@/components/ProductsList.vue";
import { useMeStore } from "@/stores/index.js";
import { storeToRefs } from "pinia";
import AddProductModal from "@/components/AddProductModal.vue";

const meStore = useMeStore();

const { supplierId } = storeToRefs(meStore);

const productsListVersion = ref(0);
</script>
