import { defineStore } from "pinia";

import { ref } from "vue";
import { httpClient } from "@/services/http.js";

export const useMeStore = defineStore("me", () => {
  const selectedTheme = ref(
    localStorage.getItem("theme") || document.body.getAttribute("data-theme"),
  );
  const myEmail = ref(null);
  const storeName = ref("No Store Selected");
  const storeId = ref(null);
  const storeType = ref(null);

  const setTheme = (theme) => {
    localStorage.setItem("theme", theme);
    document.body.setAttribute("data-theme", theme);
    selectedTheme.value = theme;
  };

  const load = async () => {
    if (myEmail.value) {
      return;
    }

    document.body.setAttribute("data-theme", selectedTheme.value);

    const resp = await httpClient.get("/api/me", null, null);

    myEmail.value = resp.email;
    storeName.value = resp.store_name;
    storeId.value = resp.store_id;
    storeType.value = resp.store_type;
  };

  return {
    selectedTheme,
    myEmail,
    storeType,
    storeId,
    storeName,
    load,
    setTheme,
  };
});
