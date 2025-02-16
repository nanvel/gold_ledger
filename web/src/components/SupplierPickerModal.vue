<template>
  <div class="btn btn-neutral btn-sm" v-on:click.prevent="showModal">
    <span v-if="supplier">
      Supplier {{ supplier.id }} : {{ supplier.name }}</span
    >
    <span v-else>Select supplier</span>
  </div>
  <dialog id="select_supplier" class="modal">
    <div class="modal-box">
      <form method="dialog" v-on:submit.prevent="closeModal">
        <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">
          ✕
        </button>
      </form>
      <supplier-picker
        v-on:selected="setSupplier"
        allow-none
        :visible="isVisible"
      />
    </div>
  </dialog>
</template>

<script setup>
import { ref } from "vue";
import SupplierPicker from "@/components/SupplierPicker.vue";

const supplier = ref(null);
const isVisible = ref(false);

const emit = defineEmits(["selected"]);

const closeModal = () => {
  select_supplier.close();
};

const showModal = () => {
  select_supplier.showModal();
  isVisible.value = true;
};

const setSupplier = async (s) => {
  supplier.value = s;
  select_supplier.close();
  emit("selected", s);
};
</script>
