<template>
  <div class="btn btn-secondary btn-sm" onclick="reject_payment.showModal()">
    Reject
  </div>
  <dialog id="reject_payment" class="modal">
    <div class="modal-box">
      <form method="dialog" v-on:submit.prevent="closeModal">
        <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">
          ✕
        </button>
      </form>
      <p class="pt-4" v-if="payment.type === 'Fine'">
        Reject payment of {{ payment.type }} {{ payment.weight }}g
        {{ payment.quality }}% from {{ payment.retailer.id }}:{{
          payment.retailer.name
        }}?
      </p>
      <p class="pt-4" v-else>
        Reject payment of {{ payment.type }} {{ payment.amount }}₹ from from
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
          v-on:click="rejectPayment"
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
  reject_payment.close();
};

const rejectPayment = async () => {
  loading.value = true;
  try {
    await httpClient.post(`/api/payments/${props.payment.id}/reject`);
    reject_payment.close();
    emit("done");
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
};
</script>
