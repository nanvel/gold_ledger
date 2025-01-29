<template>
  <div class="mt-4">Total: {{ amountSum }}</div>
  <div class="flex flex-col space-y-2">
    <div class="join mt-8">
      <button
        class="btn btn-sm join-item"
        :disabled="productsView === 'table'"
        v-on:click="setProductsView('table')"
      >
        Table
      </button>
      <button
        class="btn btn-sm join-item"
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
  <div class="join mt-8" v-if="!loading && total > 0">
    <button
      class="join-item btn"
      v-if="page > 1"
      v-on:click="loadPage(page - 1)"
    >
      «
    </button>
    <button class="join-item btn">
      Page {{ page }} / {{ pages }} <small>Total: {{ total }}</small>
    </button>
    <button
      class="join-item btn"
      v-if="page < pages"
      v-on:click="loadPage(page + 1)"
    >
      »
    </button>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import { httpClient } from "@/services/http.js";
import ProductTable from "@/components/ProductTable.vue";
import ProductCards from "@/components/ProductCards.vue";

const props = defineProps({
  retailerId: Number,
  supplierId: Number,
});

const products = ref([]);
const total = ref(0);
const page = ref(1);
const limit = ref(20);
const amountSum = ref(null);
const loading = ref(false);
const productsView = ref(localStorage.getItem("products_view") || "table");

const pages = computed(() => Math.ceil(total.value / limit.value));

const setProductsView = (view) => {
  productsView.value = view;
  localStorage.setItem("products_view", view);
};

const loadPage = async (p) => {
  page.value = p;
  let q = `?offset=${(page.value - 1) * limit.value}&limit=${limit.value}`;
  if (props.retailerId) {
    q += `&retailer_id=${props.retailerId}`;
  }
  if (props.supplierId) {
    q += `&supplier_id=${props.supplierId}`;
  }
  loading.value = true;
  try {
    const resp = await httpClient.get(`/api/products${q}`, null, null);
    products.value = resp["items"];
    total.value = resp["total"];
    amountSum.value = resp["amount_sum"];
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  await loadPage(1);
});
</script>
