<template>
  <div class="btn btn-secondary btn-sm" onclick="reject_product.showModal()">
    Reject
  </div>
  <dialog id="reject_product" class="modal">
    <div class="modal-box">
      <form method="dialog" v-on:submit.prevent="closeModal">
        <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">
          ✕
        </button>
      </form>
      <p class="pt-4">
        Reject "{{ product.name }}" from {{ product.supplier.id }}:{{
          product.supplier.name
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
          v-on:click="rejectProduct"
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
  reject_product.close();
};

const rejectProduct = async () => {
  loading.value = true;
  try {
    await httpClient.post(`/api/products/${props.product.id}/reject`);
    reject_product.close();
    emit("done");
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
};
</script>
