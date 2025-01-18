<template>
  <button class="btn" v-on:click.prevent="logOut">Log Out</button>
</template>

<script setup>
import { useAuthStore } from "@/stores/auth";

const { logout } = useAuthStore();

const logOut = async () => {
  await logout();
};
</script>
