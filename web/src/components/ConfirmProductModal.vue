<template>
  <div class="btn btn-primary btn-sm" onclick="confirm_product.showModal()">
    Confirm
  </div>
  <dialog id="confirm_product" class="modal">
    <div class="modal-box">
      <form method="dialog" v-on:submit.prevent="closeModal">
        <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">
          ✕
        </button>
      </form>
      <p class="pt-4">
        Confirm that product "{{ product.name }}" was received from
        {{ product.supplier.id }}:{{ product.supplier.name }}.
      </p>
      <div class="modal-action justify-between">
        <button
          class="btn btn-secondary"
          :disabled="loading"
          v-on:click="closeModal"
        >
          No
        </button>
        <button
          class="btn btn-primary"
          :disabled="loading"
          v-on:click="confirmProduct"
        >
          Yes
        </button>
      </div>
    </div>
  </dialog>
</template>

<script setup>
import { defineProps, ref } from "vue";
import { httpClient } from "@/services/http.js";

const props = defineProps({
  product: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(["done"]);

const loading = ref(false);

const closeModal = () => {
  confirm_product.close();
};

const confirmProduct = async () => {
  loading.value = true;
  try {
    await httpClient.post(`/api/products/${props.product.id}/confirm`);
    confirm_product.close();
    emit("done");
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
};
</script>
