<template>
  <div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
      <img
        class="mx-auto h-10 w-auto"
        src="https://tailwindui.com/plus/img/logos/mark.svg?color=indigo&shade=600"
        alt="Your Company"
      />
      <h2 class="mt-10 text-center text-2xl/9 font-bold tracking-tight">
        Register a store
      </h2>
    </div>

    <div
      role="tablist"
      class="tabs tabs-boxed mt-10 sm:mx-auto sm:w-full sm:max-w-sm"
    >
      <a
        role="tab"
        :class="{ tab: true, 'tab-active': storeType === 'retailer' }"
        v-on:click="storeType = 'retailer'"
        >Retailer</a
      >
      <a
        role="tab"
        :class="{ tab: true, 'tab-active': storeType === 'supplier' }"
        v-on:click="storeType = 'supplier'"
        >Supplier</a
      >
    </div>

    <div class="mt-2 sm:mx-auto sm:w-full sm:max-w-sm">
      <form
        class="space-y-4"
        action="#"
        method="POST"
        v-on:submit.prevent="onRegister"
      >
        <div class="form-control w-full">
          <div class="label"><span class="label-text">Store name</span></div>
          <input
            type="text"
            name="name"
            id="name"
            required
            class="input input-bordered w-full max-w-sm input-sm"
            v-model="name"
          />
        </div>

        <div class="form-control w-full">
          <div class="label"><span class="label-text">Email address</span></div>
          <input
            type="email"
            name="email"
            id="email"
            autocomplete="email"
            required
            class="input input-bordered w-full max-w-sm input-sm"
            v-model="email"
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
            required
            class="input input-bordered w-full max-w-sm input-sm"
            v-model="password"
          />
        </div>

        <div class="form-control w-full">
          <div class="label">
            <span class="label-text">Repeat password</span>
          </div>
          <input
            type="password"
            name="passwordRepeat"
            id="password-repeat"
            required
            class="input input-bordered w-full max-w-sm input-sm"
            v-model="passwordRepeat"
          />
        </div>

        <div>
          <button
            type="submit"
            class="btn btn-primary btn-sm sm:mx-auto sm:w-full sm:max-w-sm mt-4"
            :disabled="loading"
          >
            Register
          </button>
        </div>
      </form>

      <p class="mt-10 text-center text-sm/6">
        Have a account?
        <RouterLink to="/login" class="font-semibold">Sign in</RouterLink>
      </p>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref } from "vue";
import { httpClient } from "@/services/http.js";
import { useAuthStore } from "@/stores/index.js";
import { RouterLink, useRouter } from "vue-router";
import { useToast } from "vue-toastification";

const storeType = ref("retailer");
const email = ref("");
const password = ref("");
const passwordRepeat = ref("");
const name = ref("");
const loading = ref(false);

const { login } = useAuthStore();
const toast = useToast();

const onRegister = async () => {
  if (loading.value) {
    return;
  }

  if (password.value !== passwordRepeat.value) {
    toast.error("Passwords do not match.");

    return;
  }

  loading.value = true;
  try {
    const res = await httpClient.post("/api/register", {
      type: storeType.value,
      name: name.value,
      email: email.value,
      password: password.value,
    });

    if (res.success) {
      toast.success("The store was created.");
      await login(email.value, password.value);
    } else {
      toast.error("An error occurred.");
    }
  } finally {
    loading.value = false;
  }
};
</script>
