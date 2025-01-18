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

    <div
      role="tablist"
      class="tabs tabs-boxed mt-10 sm:mx-auto sm:w-full sm:max-w-sm"
    >
      <a role="tab" class="tab tab-active">Retailer</a>
      <a role="tab" class="tab">Supplier</a>
    </div>

    <div class="mt-2 sm:mx-auto sm:w-full sm:max-w-sm">
      <form class="space-y-4" action="#" method="POST">
        <div class="form-control w-full">
          <div class="label"><span class="label-text">Email address</span></div>
          <input
            type="email"
            name="email"
            id="email"
            autocomplete="email"
            required
            class="input input-bordered w-full max-w-sm input-sm"
          />
        </div>

        <div class="form-control w-full">
          <div class="label">
            <span class="label-text">Password</span
            ><span class="label-text-alt">Forgot password?</span>
          </div>
          <input
            type="password"
            name="password"
            id="password"
            autocomplete="current-password"
            required
            class="input input-bordered w-full max-w-sm input-sm"
          />
        </div>

        <div>
          <button
            type="submit"
            class="btn btn-primary btn-sm sm:mx-auto sm:w-full sm:max-w-sm mt-4"
          >
            Sign in
          </button>
        </div>
      </form>

      <p class="mt-10 text-center text-sm/6">
        Have a account?
        <RouterLink to="/login" v-on:click="onMenuClick" class="font-semibold"
          >Sign in</RouterLink
        >
      </p>
    </div>
  </div>
</template>
<script setup lang="ts">
import { RouterLink } from "vue-router";
</script>
