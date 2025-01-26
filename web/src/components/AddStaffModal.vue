<template>
  <button
    class="btn btn-sm btn-primary text-sm"
    onclick="add_staff.showModal()"
  >
    Add a staff member
  </button>
  <dialog id="add_staff" class="modal">
    <div class="modal-box">
      <form v-on:submit.prevent="addStaff" class="space-y-2">
        <label class="form-control w-full">
          <div class="label">
            <span class="label-text">Email</span>
            <span class="label-text text-error" v-if="emailError">{{
              emailError
            }}</span>
          </div>
          <input
            type="email"
            required
            class="input input-bordered w-full input-md"
            v-model="email"
            autofocus
          />
        </label>
        <label class="form-control w-full">
          <div class="label">
            <span class="label-text">Password</span>
            <span class="label-text text-error" v-if="passwordError">{{
              passwordError
            }}</span>
          </div>
          <input
            type="password"
            required
            class="input input-bordered w-full input-md text-lg"
            v-model="password"
            autofocus
          />
        </label>
        <label class="form-control w-full">
          <div class="label">
            <span class="label-text">Repeat password</span>
            <span class="label-text text-error" v-if="passwordRepeatError">{{
              passwordRepeatError
            }}</span>
          </div>
          <input
            type="password"
            required
            class="input input-bordered w-full input-md text-lg"
            v-model="passwordRepeat"
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
          Add
        </button>
      </div>
    </div>
  </dialog>
</template>

<script setup>
import { ref, watch } from "vue";
import { httpClient } from "@/services/http.js";
import { useToast } from "vue-toastification";

const email = ref("");
const emailError = ref(null);
const password = ref("");
const passwordError = ref(null);
const passwordRepeat = ref("");
const passwordRepeatError = ref(null);
const loading = ref(false);
const error = ref("");

const emit = defineEmits(["staffAdded"]);

const toast = useToast();

const clearFields = () => {
  email.value = "";
  emailError.value = null;
  password.value = "";
  passwordError.value = null;
  passwordRepeat.value = "";
  passwordRepeatError.value = null;
  loading.value = false;
  error.value = "";
};

watch([email, password, passwordRepeat], () => {
  emailError.value = null;
  passwordError.value = null;
  passwordRepeatError.value = null;
});

const addStaff = async () => {
  if (password.value !== passwordRepeat.value) {
    passwordRepeatError.value = "Passwords do not match";
    return;
  }

  if (password.value.length < 8) {
    passwordError.value = "Password must be at least 8 characters long";
    return;
  }

  loading.value = true;
  try {
    await httpClient.post(
      "/api/staff",
      {
        email: email.value,
        password: password.value,
      },
      null,
      { showToast: false },
    );
    add_staff.close();
    clearFields();
    toast.success("Staff member added successfully");
    emit("staffAdded");
  } catch (e) {
    if (e.detail?.length) {
      if (e.detail[0]["loc"][1] === "email") {
        emailError.value = e.detail[0]["msg"];
      } else if (e.detail[0]["loc"][1] === "password") {
        passwordError.value = e.detail[0]["msg"];
      }
    }

    console.log(e);
  } finally {
    loading.value = false;
  }
};
</script>
