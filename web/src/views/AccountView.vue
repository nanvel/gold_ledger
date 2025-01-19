<template>
  <Navbar>
    <article class="prose lg:prose-xl py-4 px-2">
      <h2>Account</h2>
      <h3 class="text-2xl font-semibold">Session</h3>
      <div class="p-2">
        {{ myEmail }}
      </div>

      <button class="btn" v-on:click="logout">Log out</button>

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
    </article>
  </Navbar>
</template>

<script setup>
import Navbar from "@/components/Navbar.vue";
import { useAuthStore, useMeStore } from "@/stores/index.js";
import { storeToRefs } from "pinia";

const authStore = useAuthStore();

const meStore = useMeStore();
const { selectedTheme, myEmail } = storeToRefs(meStore);

const themes = [
  ["light", "Light"],
  ["dark", "Dark"],
  ["cupcake", "Cupcake"],
];

const setTheme = (theme) => {
  meStore.setTheme(theme);
};

const logout = async () => {
  await authStore.logout();
};
</script>
