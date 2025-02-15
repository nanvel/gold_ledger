<template>
  <div class="btn btn-secondary btn-sm" v-on:click.prevent="showModal">
    Add a Retailer
  </div>
  <dialog id="invite_modal" class="modal">
    <div class="modal-box">
      <form method="dialog" v-on:submit.prevent="closeModal">
        <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">
          ✕
        </button>
      </form>
      <div>Show this QR code to the retailer</div>
      <qrcode-vue :value="inviteUrl" :size="200" v-if="code" class="mt-2" />
      <div class="mt-2 break-words">{{ inviteUrl }}</div>
      <div class="modal-action justify-between">
        <button
          class="btn btn-secondary"
          :disabled="loading"
          v-on:click="closeModal"
        >
          Close
        </button>
      </div>
    </div>
  </dialog>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { httpClient } from "@/services/http.js";
import QrcodeVue from "qrcode.vue";

const code = ref(null);

const emit = defineEmits(["done"]);

const loading = ref(false);

const closeModal = () => {
  invite_modal.close();
};

const showModal = async () => {
  invite_modal.showModal();

  loading.value = true;
  try {
    const resp = await httpClient.get("/api/connect");
    code.value = resp.code;
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
};

const inviteUrl = computed(
  () => `${window.location.origin}/invite/${code.value}`,
);
</script>
