<template>
  <div class="btn btn-secondary btn-sm" onclick="cancel_product.showModal()">
    Cancel
  </div>
  <dialog id="cancel_product" class="modal">
    <div class="modal-box">
      <form method="dialog" v-on:submit.prevent="closeModal">
        <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">
          ✕
        </button>
      </form>
      <p class="pt-4">
        Cancel product "{{ product.name }}" for {{ product.retailer.id }}:{{
          product.retailer.name
        }}?
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
          v-on:click="cancelProduct"
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
  cancel_product.close();
};

const cancelProduct = async () => {
  loading.value = true;
  try {
    await httpClient.post(`/api/products/${props.product.id}/cancel`);
    cancel_product.close();
    emit("done");
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
};
</script>
