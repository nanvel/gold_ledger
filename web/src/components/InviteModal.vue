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
      <div class="mt-8">Show this QR code to the retailer</div>
      <div
        class="border rounded-md border-base-300 p-2 flex flex-col items-center mt-2"
      >
        <qrcode-vue :value="inviteUrl" :size="200" v-if="code" />
        <div class="mt-2 break-words max-w-full">
          {{ inviteUrl }}
        </div>
      </div>
      <div class="modal-action justify-between">
        <button
          class="btn btn-secondary"
          :disabled="loading"
          v-on:click="closeModal"
        >
          Close
        </button>
        <div class="btn btn-primary" v-on:click.prevent="copyCode">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            height="1em"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 0 1-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 0 1 1.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 0 0-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 0 1-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 0 0-3.375-3.375h-1.5a1.125 1.125 0 0 1-1.125-1.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H9.75"
            />
          </svg>
          Copy to clipboard
        </div>
      </div>
    </div>
  </dialog>
</template>

<script setup>
import { ref, computed } from "vue";
import { httpClient } from "@/services/http.js";
import QrcodeVue from "qrcode.vue";
import { useToast } from "vue-toastification";

const code = ref(null);

const emit = defineEmits(["done"]);

const loading = ref(false);

const closeModal = () => {
  invite_modal.close();
  code.value = null;
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

const copyCode = () => {
  const toast = useToast();
  navigator.clipboard.writeText(inviteUrl.value);
  closeModal();
  toast.success("Copied to clipboard!");
};

const inviteUrl = computed(
  () => `${window.location.origin}/invite/${code.value}`,
);
</script>
