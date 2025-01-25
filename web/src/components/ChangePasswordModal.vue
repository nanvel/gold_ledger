<template>
  <button
    class="btn btn-sm btn-primary text-sm"
    onclick="change_password.showModal()"
  >
    Change password
  </button>
  <dialog id="change_password" class="modal">
    <div class="modal-box">
      <form v-on:submit.prevent="changePassword" class="space-y-2">
        <label class="form-control w-full">
          <div class="label">
            <span class="label-text">Old password:</span>
            <span class="label-text text-error" v-if="oldPasswordError">{{
              oldPasswordError
            }}</span>
          </div>
          <input
            type="password"
            required
            class="input input-bordered w-full input-md text-lg"
            v-model="oldPassword"
            autofocus
          />
        </label>
        <label class="form-control w-full">
          <div class="label">
            <span class="label-text">New password:</span>
            <span class="label-text text-error" v-if="newPasswordError">{{
              newPasswordError
            }}</span>
          </div>
          <input
            type="password"
            required
            class="input input-bordered w-full input-md text-lg"
            v-model="newPassword"
            autofocus
          />
        </label>
        <label class="form-control w-full">
          <div class="label">
            <span class="label-text">Repeat the new password:</span>
            <span class="label-text text-error" v-if="newPasswordRepeatError">{{
              newPasswordRepeatError
            }}</span>
          </div>
          <input
            type="password"
            required
            class="input input-bordered w-full input-md text-lg"
            v-model="newPasswordRepeat"
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
          v-on:click="changePassword"
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

const oldPassword = ref("");
const oldPasswordError = ref(null);
const newPassword = ref("");
const newPasswordError = ref(null);
const newPasswordRepeat = ref("");
const loading = ref(false);
const error = ref("");
const newPasswordRepeatError = ref(null);

const toast = useToast();

const clearFields = () => {
  oldPassword.value = "";
  newPassword.value = "";
  newPasswordRepeat.value = "";
  newPasswordRepeatError.value = null;
  error.value = "";
};

watch([oldPassword, newPassword, newPasswordRepeat], () => {
  oldPasswordError.value = null;
  newPasswordError.value = null;
  newPasswordRepeatError.value = null;
});

const changePassword = async () => {
  if (newPassword.value !== newPasswordRepeat.value) {
    newPasswordRepeatError.value = "Passwords do not match";
    return;
  }

  if (newPassword.value.length < 8) {
    newPasswordError.value = "Password must be at least 8 characters long";
    return;
  }

  loading.value = true;
  try {
    await httpClient.post(
      "/api/change-password",
      {
        old_password: oldPassword.value,
        new_password: newPassword.value,
      },
      null,
      { showToast: false },
    );
    change_password.close();
    clearFields();
    toast.success("Password changed successfully");
  } catch (e) {
    if (e.detail?.length) {
      if (e.detail[0]["loc"][1] === "new_password") {
        newPasswordError.value = e.detail[0]["msg"];
      } else if (e.detail[0]["loc"][1] === "old_password") {
        oldPasswordError.value = e.detail[0]["msg"];
      }
    }

    console.log(e);
  } finally {
    loading.value = false;
  }
};
</script>
