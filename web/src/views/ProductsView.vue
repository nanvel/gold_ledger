<template>
  <Navbar>
    <div class="py-4">
      <add-product-modal
        v-on:product-added="productsListVersion += 1"
        v-if="supplierId"
      />

      <ProductsList
        :supplier-id="supplierId"
        :retailer-id="retailerId"
        v-if="supplierId || retailerId"
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

const { supplierId, retailerId } = storeToRefs(meStore);

const productsListVersion = ref(0);
</script>
