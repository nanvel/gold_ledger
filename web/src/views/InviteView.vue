<template>
  <navbar>
    <div class="flex flex-col space-y-4 items-center">
      <placeholder v-if="loading" loading />
      <div v-if="error" class="text-error">{{ error }}</div>
      <div v-if="success" class="text-success">Connected successfully!</div>
    </div>
  </navbar>
</template>

<script setup>
import { ref, onMounted } from "vue";
import router from "@/router/index.js";
import { httpClient, parseError } from "@/services/http.js";
import Navbar from "@/components/Navbar.vue";
import Placeholder from "@/components/Placeholder.vue";
import { useMeStore } from "@/stores/index.js";
import { storeToRefs } from "pinia";

const inviteCode = ref(router.currentRoute.value.params.code);
const error = ref(null);
const loading = ref(false);
const success = ref(null);

const meStore = useMeStore();

const { isSupplier } = storeToRefs(meStore);

onMounted(async () => {
  loading.value = true;
  try {
    const response = await httpClient.post(
      "/api/connect",
      {
        code: inviteCode.value,
      },
      null,
      { showToast: false },
    );
    success.value = response.success;
    if (isSupplier) {
      await router.push("/retailers");
    } else {
      await router.push("/suppliers");
    }
  } catch (e) {
    error.value = parseError(e, "code") || parseError(e);
  } finally {
    loading.value = false;
  }
});
</script>
