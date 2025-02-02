<template>
  <button
    class="btn btn-sm btn-primary text-sm"
    onclick="change_name.showModal()"
  >
    Change name
  </button>
  <dialog id="change_name" class="modal">
    <div class="modal-box">
      <form v-on:submit.prevent="addStaff" class="space-y-2">
        <div class="form-control w-full">
          <div class="label">
            <span class="label-text">Name</span>
          </div>
          <input
            type="text"
            required
            class="input input-bordered w-full input-md"
            v-model="name"
            autofocus
          />
          <div class="label" v-if="nameError">
            <span class="label-text-alt text-error">{{ nameError }}</span>
          </div>
        </div>
      </form>
      <div v-if="error" class="mt-4 whitespace-pre-line text-error text-sm">
        {{ error }}
      </div>
      <div class="modal-action justify-between">
        <form method="dialog" v-on:submit="clearFields">
          <button class="btn btn-secondary" :disabled="loading">Cancel</button>
        </form>
        <button
          class="btn btn-primary"
          :disabled="loading"
          v-on:click="addStaff"
        >
          Change
        </button>
      </div>
    </div>
  </dialog>
</template>

<script setup>
import { ref, watch } from "vue";
import { httpClient } from "@/services/http.js";
import { useToast } from "vue-toastification";
import { parseError } from "@/services/http.js";

const props = defineProps({
  name: String,
});

const name = ref(props.name || "");
const nameError = ref(null);
const loading = ref(false);
const error = ref("");

const emit = defineEmits(["nameChanged"]);

const toast = useToast();

const clearFields = () => {
  nameError.value = null;
  loading.value = false;
  error.value = "";
};

watch([name], () => {
  nameError.value = null;
});

const addStaff = async () => {
  loading.value = true;
  try {
    await httpClient.put(
      "/api/me/name",
      {
        name: name.value,
      },
      null,
      { showToast: false },
    );
    change_name.close();
    emit("nameChanged", name.value);
    clearFields();
    toast.success("Name changed successfully");
  } catch (e) {
    error.value = parseError(e);
    nameError.value = parseError(e, "name");
  } finally {
    loading.value = false;
  }
};
</script>
