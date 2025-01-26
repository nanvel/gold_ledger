<template>
  <div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
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
          <div class="label">
            <span class="label-text">Store name</span
            ><span class="label-text text-error" v-if="nameError">{{
              nameError
            }}</span>
          </div>
          <input
            type="text"
            name="name"
            id="name"
            required
            autofocus
            class="input input-bordered w-full max-w-sm input-md text-lg"
            v-model="name"
          />
        </div>

        <div class="form-control w-full">
          <div class="label">
            <span class="label-text">Email address</span
            ><span class="label-text text-error" v-if="emailError">{{
              emailError
            }}</span>
          </div>
          <input
            type="email"
            name="email"
            id="email"
            autocomplete="email"
            required
            class="input input-bordered w-full max-w-sm input-md-text-lg"
            v-model="email"
          />
        </div>

        <password-input
          v-model="password"
          label="Password"
          :error="passwordError"
        />
        <password-input v-model="passwordRepeat" label="Repeat password" />

        <div v-if="error" class="mt-4 whitespace-pre-line text-error">
          {{ error }}
        </div>

        <div>
          <button
            type="submit"
            class="btn btn-primary btn-md sm:mx-auto sm:w-full sm:max-w-sm mt-4"
            :disabled="loading"
          >
            Register
          </button>
        </div>
      </form>

      <p class="mt-10 text-center text-sm/6">
        Have an account?
        <RouterLink to="/login" class="font-semibold">Sign in</RouterLink>
      </p>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, watch } from "vue";
import { httpClient, parseError } from "@/services/http.js";
import { useAuthStore } from "@/stores/index.js";
import { RouterLink } from "vue-router";
import { useToast } from "vue-toastification";
import PasswordInput from "@/components/inputs/PasswordInput.vue";

const storeType = ref("retailer");
const email = ref("");
const emailError = ref(null);
const password = ref("");
const passwordError = ref(null);
const passwordRepeat = ref("");
const name = ref("");
const nameError = ref(null);
const loading = ref(false);
const error = ref(null);

const toast = useToast();

watch([email, password, passwordRepeat, name], () => {
  emailError.value = null;
  passwordError.value = null;
  nameError.value = null;
});

const onRegister = async () => {
  if (loading.value) {
    return;
  }

  if (password.value !== passwordRepeat.value) {
    passwordError.value = "Passwords do not match";
    return;
  }

  loading.value = true;
  try {
    const res = await httpClient.post(
      "/api/register",
      {
        type: storeType.value,
        name: name.value,
        email: email.value,
        password: password.value,
      },
      null,
      { showToast: false },
    );

    toast.success("The store was created");

    const { login } = useAuthStore();
    await login(email.value, password.value);
  } catch (e) {
    error.value = parseError(e);
    nameError.value = parseError(e, "name");
    emailError.value = parseError(e, "email");
    passwordError.value = parseError(e, "password");
  } finally {
    loading.value = false;
  }
};
</script>
