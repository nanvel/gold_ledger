<template>
  <div class="btn btn-primary btn-sm" onclick="confirm_payment.showModal()">
    Confirm
  </div>
  <dialog id="confirm_payment" class="modal">
    <div class="modal-box">
      <form method="dialog" v-on:submit.prevent="closeModal">
        <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">
          ✕
        </button>
      </form>
      <p class="pt-4" v-if="payment.type === 'Fine'">
        Confirm payment of {{ payment.type }} {{ payment.weight }}g
        {{ payment.quality }}% was received from {{ payment.retailer.id }}:{{
          payment.retailer.name
        }}.
      </p>
      <p class="pt-4" v-else>
        Confirm payment of {{ payment.type }} {{ payment.amount }}₹ was received
        from {{ payment.retailer.id }}:{{ payment.retailer.name }}.
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
          v-on:click="confirmPayment"
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
  confirm_payment.close();
};

const confirmPayment = async () => {
  loading.value = true;
  try {
    await httpClient.post(`/api/payments/${props.payment.id}/confirm`);
    confirm_payment.close();
    emit("done");
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
};
</script>
