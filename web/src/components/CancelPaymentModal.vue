<template>
  <div class="btn btn-secondary btn-sm" onclick="cancel_payment.showModal()">
    Cancel
  </div>
  <dialog id="cancel_payment" class="modal">
    <div class="modal-box">
      <form method="dialog" v-on:submit.prevent="closeModal">
        <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">
          ✕
        </button>
      </form>
      <p class="pt-4" v-if="payment.type === 'Fine'">
        Cancel payment of {{ payment.type }} {{ payment.weight }}g
        {{ payment.quality }}% to {{ payment.retailer.id }}:{{
          payment.retailer.name
        }}?
      </p>
      <p class="pt-4" v-else>
        Cancel payment of {{ payment.type }} {{ payment.amount }}₹ to
        {{ payment.retailer.id }}:{{ payment.retailer.name }}?
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
          v-on:click="cancelPayment"
        >
          Yes
        </button>
      </div>
    </div>
  </dialog>
</template>

<script setup>
import { ref } from "vue";
import { httpClient } from "@/services/http.js";

const props = defineProps({
  payment: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(["done"]);

const loading = ref(false);

const closeModal = () => {
  cancel_payment.close();
};

const cancelPayment = async () => {
  loading.value = true;
  try {
    await httpClient.post(`/api/payments/${props.payment.id}/cancel`);
    cancel_payment.close();
    emit("done");
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
};
</script>
