<template>
  <div class="drawer box-border">
    <input id="nav-drawer" type="checkbox" class="drawer-toggle" />
    <div class="drawer-content flex flex-col">
      <!-- Navbar -->
      <div class="navbar bg-base-300 w-full shadow-md fixed z-10">
        <div class="flex-none lg:hidden">
          <label
            for="nav-drawer"
            aria-label="open sidebar"
            class="btn btn-square btn-ghost"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              class="inline-block h-6 w-6 stroke-current"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
              ></path>
            </svg>
          </label>
        </div>
        <div class="mx-2 flex-1 px-2">
          <RouterLink to="/"
            >{{ supplierId || retailerId }} : {{ storeName }}</RouterLink
          >
        </div>
        <div class="hidden flex-none lg:block">
          <ul class="menu menu-horizontal">
            <!-- Navbar menu content here -->
            <li><RouterLink to="/products">Products</RouterLink></li>
            <li><RouterLink to="/payments">Payments</RouterLink></li>
            <li><RouterLink to="/settings">Settings</RouterLink></li>
          </ul>
        </div>
        <add-product-modal
          v-if="isSupplier"
          v-on:product-added="store.incrementVersion"
        />
        <add-payment-modal v-else v-on:payment-added="store.incrementVersion" />
      </div>
      <div class="p-2 relative mt-20">
        <slot></slot>
      </div>
    </div>
    <div class="drawer-side">
      <label
        for="nav-drawer"
        aria-label="close sidebar"
        class="drawer-overlay"
      ></label>
      <ul class="menu bg-base-200 min-h-full w-80 p-4 pt-20">
        <!-- Sidebar content here -->
        <li><RouterLink to="/products">Products</RouterLink></li>
        <li><RouterLink to="/payments">Payments</RouterLink></li>
        <li><RouterLink to="/settings">Settings</RouterLink></li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { useMeStore } from "@/stores/index.js";
import { onMounted } from "vue";
import { storeToRefs } from "pinia";
import { RouterLink } from "vue-router";
import AddPaymentModal from "@/components/AddPaymentModal.vue";
import AddProductModal from "@/components/AddProductModal.vue";

const store = useMeStore();
const { storeName, supplierId, retailerId, isSupplier } = storeToRefs(store);

onMounted(async () => {
  await store.load();
});
</script>
