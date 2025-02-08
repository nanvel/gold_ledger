<template>
  <div class="flex flex-col space-y-4">
    <div class="flex flex-row space-x-2 justify-between">
      <div>
        <retailer-picker-modal v-if="isSupplier" v-on:selected="setRetailer" />
        <supplier-picker-modal v-else v-on:selected="setSupplier" />
      </div>
      <div class="join">
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
    </div>

    <Placeholder v-if="!products?.length && !loading" text="-" />
    <Placeholder v-if="loading" loading />

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
import SupplierPickerModal from "@/components/SupplierPickerModal.vue";
import RetailerPickerModal from "@/components/RetailerPickerModal.vue";
import Placeholder from "@/components/Placeholder.vue";

const props = defineProps({
  retailerId: Number,
  supplierId: Number,
});

const products = ref([]);
const total = ref(0);
const page = ref(1);
const limit = ref(20);
const loading = ref(false);
const retailerId = ref(props.retailerId);
const supplierId = ref(props.supplierId);
const productsView = ref(localStorage.getItem("products_view") || "table");

const isSupplier = computed(() => props.supplierId);

const pages = computed(() => Math.ceil(total.value / limit.value));

const setProductsView = (view) => {
  productsView.value = view;
  localStorage.setItem("products_view", view);
};

const loadPage = async (p) => {
  page.value = p;
  let q = `?offset=${(page.value - 1) * limit.value}&limit=${limit.value}`;
  if (retailerId.value) {
    q += `&retailer_id=${retailerId.value}`;
  }
  if (supplierId.value) {
    q += `&supplier_id=${supplierId.value}`;
  }
  loading.value = true;
  try {
    const resp = await httpClient.get(`/api/products${q}`, null, null);
    products.value = resp["items"];
    total.value = resp["total"];
  } finally {
    loading.value = false;
  }
};

const setRetailer = (retailer) => {
  retailerId.value = retailer?.id;
  loadPage(1);
};

const setSupplier = (supplier) => {
  supplierId.value = supplier?.id;
  loadPage(1);
};

onMounted(async () => {
  await loadPage(1);
});
</script>
