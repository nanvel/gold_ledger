<template>
  <Navbar>
    <div class="flex flex-col space-y-8 pb-8">
      <div class="divider">Account</div>
      <template v-if="myName?.length">{{ myName }} |</template> {{ myEmail }}
      <div
        class="flex flex-col space-y-4 sm:flex-row sm:space-y-0 sm:space-x-2"
        v-if="myEmail"
      >
        <div>
          <button class="btn btn-sm btn-primary" v-on:click="logout">
            Log out
          </button>
        </div>
        <div><change-password-modal /></div>
        <div>
          <ChangeNameModal :name="myName" v-on:name-changed="onNameChanged" />
        </div>
      </div>

      <div class="divider">Theme</div>
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

      <div class="divider" v-if="isOwner">Store</div>
      <div class="flex flex-row space-x-4" v-if="isOwner">
        <ChangeStoreNameModal
          :name="storeName"
          v-on:name-changed="meStore.setStoreName"
        />
      </div>

      <div class="divider" v-if="isOwner">Staff</div>
      <div v-if="isOwner">
        <add-staff-modal v-on:staff-added="staffListVersion += 1" />
        <staff-list :key="staffListVersion" />
      </div>
    </div>
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
import ChangeNameModal from "@/components/ChangeNameModal.vue";
import ChangeStoreNameModal from "@/components/ChangeStoreNameModal.vue";

const meStore = useMeStore();
const { selectedTheme, myEmail, myName, isOwner, storeName } =
  storeToRefs(meStore);
const staffListVersion = ref(0);

const themes = [
  ["light", "Light"],
  ["dark", "Dark"],
  ["cupcake", "Cupcake"],
];

const setTheme = (theme) => {
  meStore.setTheme(theme);
};

const onNameChanged = (name) => {
  meStore.setName(name);
  staffListVersion.value += 1;
};

const logout = async () => {
  const authStore = useAuthStore();

  await authStore.logout();
  meStore.reset();
};
</script>
