<template>
  <div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
      <h2 class="mt-10 text-center text-2xl/9 font-bold tracking-tight">
        Sign in
      </h2>
    </div>

    <div class="mt-2 sm:mx-auto sm:w-full sm:max-w-sm">
      <form
        class="space-y-4"
        action="#"
        method="POST"
        v-on:submit.prevent="onLogin"
      >
        <div class="form-control w-full">
          <div class="label">
            <span class="label-text">Email address</span>
            <span class="label-text text-error" v-if="usernameError">{{
              usernameError
            }}</span>
          </div>
          <input
            type="email"
            name="email"
            id="email"
            autocomplete="email"
            required
            class="input input-bordered w-full max-w-sm input-md text-lg"
            v-model="username"
            autofocus
          />
        </div>

        <password-input
          label="Password"
          v-model="password"
          autocomplete="current-password"
          :error="passwordError"
        />

        <div v-if="error" class="mt-4 whitespace-pre-line text-error">
          {{ error }}
        </div>

        <div>
          <button
            type="submit"
            class="btn btn-primary btn-md sm:mx-auto sm:w-full sm:max-w-sm mt-4"
            :disabled="loading"
          >
            Sign in
          </button>
        </div>
      </form>

      <p class="mt-10 text-center text-sm/6">
        Not a member?
        <RouterLink to="/register" class="font-semibold"
          >Register a store</RouterLink
        >
      </p>
    </div>
  </div>
</template>
<script setup>
import { ref, watch } from "vue";
import { useAuthStore } from "@/stores/index.js";
import { RouterLink } from "vue-router";
import PasswordInput from "@/components/inputs/PasswordInput.vue";
import { parseError } from "@/services/http.js";

const loading = ref(false);
const username = ref("");
const usernameError = ref(null);
const password = ref("");
const passwordError = ref(null);
const error = ref(null);
const { login } = useAuthStore();

watch([username, password], () => {
  usernameError.value = null;
  passwordError.value = null;
});

const onLogin = async () => {
  if (loading.value) {
    return;
  }
  loading.value = true;
  try {
    await login(username.value, password.value);
  } catch (e) {
    error.value = parseError(e);
    usernameError.value = parseError(e, "username");
    passwordError.value = parseError(e, "password");
  } finally {
    loading.value = false;
  }
};
</script>
