<template>
  <Navbar>
    <article class="prose lg:prose-xl py-4 px-2">
      <h2>Settings</h2>
      <h3 class="text-2xl font-semibold">Session</h3>
      <div class="py-2">
        <template v-if="myName?.length">{{ myName }} |</template> {{ myEmail }}
      </div>

      <div class="flex flex-row space-x-4">
        <button class="btn btn-sm btn-primary" v-on:click="logout">
          Log out
        </button>
        <change-password-modal />
        <change-name-modal :name="myName" v-on:name-changed="meStore.setName" />
      </div>

      <h3 class="text-2xl font-semibold">Theme</h3>
      <div class="join join-horizontal mt-2">
        <input
          type="radio"
          name="theme-buttons"
          class="btn btn-sm theme-controller join-item"
          :aria-label="theme[1]"
          :value="theme[0]"
          :key="theme[0]"
          v-for="theme in themes"
          :disabled="theme[0] === selectedTheme"
          v-on:click.prevent="setTheme(theme[0])"
        />
      </div>

      <h3 class="text-2xl font-semibold" v-if="isOwner">Staff</h3>
      <add-staff-modal
        v-if="isOwner"
        v-on:staff-added="staffListVersion += 1"
      />
      <staff-list v-if="isOwner" :key="staffListVersion" />
    </article>
  </Navbar>
</template>

<script setup>
import { ref } from "vue";
import Navbar from "@/components/Navbar.vue";
import { useAuthStore, useMeStore } from "@/stores/index.js";
import { storeToRefs } from "pinia";
import changePasswordModal from "@/components/ChangePasswordModal.vue";
import StaffList from "@/components/StaffList.vue";
import AddStaffModal from "@/components/AddStaffModal.vue";
import changeNameModal from "@/components/ChangeNameModal.vue";

const meStore = useMeStore();
const { selectedTheme, myEmail, myName, isOwner } = storeToRefs(meStore);
const staffListVersion = ref(0);

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
