<template>
  <button
    class="btn btn-sm btn-primary text-sm"
    onclick="change_store_name.showModal()"
  >
    Change store name
  </button>
  <dialog id="change_store_name" class="modal">
    <div class="modal-box">
      <form v-on:submit.prevent="addStaff" class="space-y-2">
        <label class="form-control w-full">
          <div class="label">
            <span class="label-text">Name:</span>
            <span class="label-text text-error" v-if="nameError">{{
              nameError
            }}</span>
          </div>
          <input
            type="text"
            required
            class="input input-bordered w-full input-md"
            v-model="name"
            autofocus
          />
        </label>
      </form>
      <div v-if="error" class="mt-4 whitespace-pre-line text-error">
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
import { onMounted, ref, watch } from "vue";
import { httpClient } from "@/services/http.js";
import { useToast } from "vue-toastification";

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
      "/api/me/store-name",
      {
        name: name.value,
      },
      null,
      { showToast: false },
    );
    change_store_name.close();
    emit("nameChanged", name.value);
    clearFields();
    toast.success("Store name changed successfully");
  } catch (e) {
    if (e.detail?.length) {
      if (e.detail[0]["loc"][1] === "name") {
        nameError.value = e.detail[0]["msg"];
      }
    } else {
      error.value = e.detail || "An error occurred";
    }

    console.log(e);
  } finally {
    loading.value = false;
  }
};
</script>
