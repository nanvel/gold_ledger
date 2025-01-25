<template>
  <div>
    <div class="join">
      <button
        class="btn join-item"
        :disabled="productsView === 'table'"
        v-on:click="setProductsView('table')"
      >
        Table
      </button>
      <button
        class="btn join-item"
        :disabled="productsView === 'cards'"
        v-on:click="setProductsView('cards')"
      >
        Cards
      </button>
    </div>

    <ProductTable
      :products="products"
      v-if="products?.length && !loading && productsView === 'table'"
    />
    <ProductCards
      :products="products"
      v-if="products?.length && !loading && productsView === 'cards'"
    />
  </div>
</template>

<script setup>
import { onMounted, ref, defineProps } from "vue";
import { httpClient } from "@/services/http.js";
import ProductTable from "@/components/ProductTable.vue";
import ProductCards from "@/components/ProductCards.vue";

const props = defineProps({
  retailerId: Number,
  supplierId: Number,
});

const products = ref([]);
const total = ref(0);
const loading = ref(false);
const productsView = ref(localStorage.getItem("productsView") || "table");

const setProductsView = (view) => {
  productsView.value = view;
  localStorage.setItem("productsView", view);
};

onMounted(async () => {
  let q = "?limit=20";
  if (props.retailerId) {
    q += `&retailer_id=${props.retailerId}`;
  }
  if (props.supplierId) {
    q += `&supplier_id=${props.supplierId}`;
  }
  loading.value = true;
  try {
    const resp = await httpClient.get(`/api/products?${q}`, null, null);
    products.value = resp["items"];
    total.value = resp["total"];
  } finally {
    loading.value = false;
  }
});
</script>
