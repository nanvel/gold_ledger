import { defineStore } from "pinia";

import { ref, computed } from "vue";
import router from "@/router";
import { httpClient } from "@/services/http.js";

const baseUrl = `/api/auth`;

export const useAuthStore = defineStore("auth", () => {
  const authToken = ref(localStorage.getItem("auth_token"));
  const returnUrl = ref(null);

  const loggedIn = computed(() => !!authToken.value);

  const setReturnUrl = (url) => {
    returnUrl.value = url;
  };

  const login = async (username, password) => {
    const body = new URLSearchParams();
    body.append("username", username);
    body.append("password", password);
    const resp = await httpClient.post(
      `${baseUrl}/token`,
      null,
      body,
      "application/x-www-form-urlencoded",
    );

    authToken.value = resp.access_token;

    // store user details and jwt in local storage to keep user logged in between page refreshes
    localStorage.setItem("auth_token", resp.access_token);

    // redirect to previous url or default to home page
    await router.push(returnUrl.value || "/");
  };

  const logout = async () => {
    authToken.value = null;
    localStorage.removeItem("auth_token");
    await router.push("/login");
  };

  return {
    authToken,
    returnUrl,
    loggedIn,
    setReturnUrl,
    login,
    logout,
  };
});
