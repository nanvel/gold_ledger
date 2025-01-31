<template>
  <div class="btn btn-neutral btn-sm" onclick="select_retailer.showModal()">
    <span v-if="retailer">
      Retailer {{ retailer.id }} : {{ retailer.name }}</span
    >
    <span v-else>Select retailer</span>
  </div>
  <dialog id="select_retailer" class="modal">
    <div class="modal-box">
      <form method="dialog" v-on:submit.prevent="closeModal">
        <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">
          ✕
        </button>
      </form>
      <retailer-picker v-on:selected="setRetailer" allow-none />
    </div>
  </dialog>
</template>

<script setup>
import { ref } from "vue";
import RetailerPicker from "@/components/RetailerPicker.vue";

const retailer = ref(null);

const emit = defineEmits(["selected"]);

const closeModal = () => {
  select_retailer.close();
};

const setRetailer = async (r) => {
  select_retailer.close();
  retailer.value = r;
  emit("selected", r);
};
</script>
