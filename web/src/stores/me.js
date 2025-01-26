import { defineStore } from "pinia";

import { computed, ref } from "vue";
import { httpClient } from "@/services/http.js";

export const useMeStore = defineStore("me", () => {
  const selectedTheme = ref(
    localStorage.getItem("theme") || document.body.getAttribute("data-theme"),
  );
  const myId = ref(null);
  const myEmail = ref(null);
  const myName = ref(null);
  const storeName = ref(null);
  const storeOwnerId = ref(null);
  const supplierId = ref(null);
  const retailerId = ref(null);

  const isSupplier = computed(() => supplierId.value !== null);
  const isRetailer = computed(() => retailerId.value !== null);
  const isOwner = computed(() => storeOwnerId.value === myId.value);

  const setTheme = (theme) => {
    localStorage.setItem("theme", theme);
    document.body.setAttribute("data-theme", theme);
    selectedTheme.value = theme;
  };

  const setName = (name) => {
    myName.value = name;
  };

  const setStoreName = (name) => {
    storeName.value = name;
  };

  const load = async () => {
    if (myEmail.value) {
      return;
    }

    document.body.setAttribute("data-theme", selectedTheme.value);

    const resp = await httpClient.get("/api/me", null, null);

    myId.value = resp.id;
    myEmail.value = resp.email;
    myName.value = resp.name;
    storeName.value = resp.store_name;
    storeOwnerId.value = resp.store_owner_id;
    supplierId.value = resp.supplier_id;
    retailerId.value = resp.retailer_id;
  };

  return {
    selectedTheme,
    myEmail,
    myName,
    storeName,
    isSupplier,
    isRetailer,
    isOwner,
    supplierId,
    retailerId,
    load,
    setTheme,
    setName,
    setStoreName,
  };
});
