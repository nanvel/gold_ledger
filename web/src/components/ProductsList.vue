<template>
  <div class="flex flex-col space-y-4">
    <div class="flex flex-row space-x-2 justify-between">
      <div
        class="flex flex-col space-y-2 sm:flex-row sm:space-x-2 sm:space-y-0"
      >
        <retailer-picker-modal v-if="isSupplier" v-on:selected="setRetailer" />
        <supplier-picker-modal v-else v-on:selected="setSupplier" />

        <select
          class="select select-bordered select-sm w-full max-w-xs"
          v-model="status"
        >
          <option selected :value="0">Status - all</option>
          <option :value="1">Status - pending</option>
          <option :value="2">Status - confirmed</option>
          <option :value="3">Status - rejected</option>
          <option :value="4">Status - canceled</option>
        </select>
      </div>
      <div
        class="flex flex-col space-y-2 sm:flex-row sm:space-x-2 sm:space-y-0"
      >
        <div class="btn btn-neutral btn-sm" v-on:click.prevent="downloadCsv">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            height="1em"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3"
            />
          </svg>
          CSV
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
    <div class="join" v-if="!loading && total > 0">
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
  </div>
</template>

<script setup>
import { onMounted, ref, computed, watch } from "vue";
import { httpClient, downloadFile } from "@/services/http.js";
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
const status = ref(0);

const isSupplier = computed(() => props.supplierId);

const pages = computed(() => Math.ceil(total.value / limit.value));

const setProductsView = (view) => {
  productsView.value = view;
  localStorage.setItem("products_view", view);
};

const downloadCsv = async () => {
  const q = [];
  if (retailerId.value) {
    q.push(`retailer_id=${retailerId.value}`);
  }
  if (supplierId.value) {
    q.push(`&supplier_id=${supplierId.value}`);
  }
  if (status.value) {
    q.push(`&status=${status.value}`);
  }
  await downloadFile(`/api/products-csv${q.length ? "?" + q.join("&") : ""}`);
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
  if (status.value) {
    q += `&status=${status.value}`;
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

watch([status], () => {
  loadPage(1);
});

onMounted(async () => {
  await loadPage(1);
});
</script>
