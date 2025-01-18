<template>
  <div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
      <img
        class="mx-auto h-10 w-auto"
        src="https://tailwindui.com/plus/img/logos/mark.svg?color=indigo&shade=600"
        alt="Your Company"
      />
      <h2 class="mt-10 text-center text-2xl/9 font-bold tracking-tight">
        Sign in to your account
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
          <div class="label"><span class="label-text">Email address</span></div>
          <input
            type="email"
            name="email"
            id="email"
            autocomplete="email"
            required
            class="input input-bordered w-full max-w-sm input-sm"
            v-model="username"
          />
        </div>

        <div class="form-control w-full">
          <div class="label">
            <span class="label-text">Password</span>
          </div>
          <input
            type="password"
            name="password"
            id="password"
            autocomplete="current-password"
            required
            class="input input-bordered w-full max-w-sm input-sm"
            v-model="password"
          />
        </div>

        <div>
          <button
            type="submit"
            class="btn btn-primary btn-sm sm:mx-auto sm:w-full sm:max-w-sm mt-4"
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
import { ref } from "vue";
import { useAuthStore } from "@/stores/index.js";
import { RouterLink } from "vue-router";

const loading = ref(false);
const username = ref("");
const password = ref("");
const { login } = useAuthStore();

const onLogin = async () => {
  if (loading.value) {
    return;
  }
  loading.value = true;
  try {
    await login(username.value, password.value);
  } finally {
    loading.value = false;
  }
};
</script>
