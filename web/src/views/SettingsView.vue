<template>
  <Navbar>
    <article class="prose lg:prose-xl py-4 px-2">
      <h2>Settings</h2>
      <h3 class="text-2xl font-semibold">Session</h3>
      <div class="py-2">
        {{ myEmail }}
      </div>

      <div class="flex flex-row space-x-4">
        <button class="btn btn-sm btn-primary" v-on:click="logout">
          Log out
        </button>
        <change-password-modal />
      </div>

      <h3 class="text-2xl font-semibold">Theme</h3>
      <div class="join join-horizontal mt-2">
        <input
          type="radio"
          name="theme-buttons"
          class="btn theme-controller join-item"
          :aria-label="theme[1]"
          :value="theme[0]"
          :key="theme[0]"
          v-for="theme in themes"
          :disabled="theme[0] === selectedTheme"
          v-on:click.prevent="setTheme(theme[0])"
        />
      </div>

      <h3 class="text-2xl font-semibold" v-if="isOwner">Staff</h3>
    </article>
  </Navbar>
</template>

<script setup>
import Navbar from "@/components/Navbar.vue";
import { useAuthStore, useMeStore } from "@/stores/index.js";
import { storeToRefs } from "pinia";
import changePasswordModal from "@/components/ChangePasswordModal.vue";

const meStore = useMeStore();
const { selectedTheme, myEmail, isOwner } = storeToRefs(meStore);

const themes = [
  ["light", "Light"],
  ["dark", "Dark"],
  ["cupcake", "Cupcake"],
];

const setTheme = (theme) => {
  meStore.setTheme(theme);
};

const logout = async () => {
  const authStore = useAuthStore();

  await authStore.logout();
};
</script>
