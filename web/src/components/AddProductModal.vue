<template>
  <button class="btn btn-sm btn-primary" onclick="add_product.showModal()">
    Add a product sold
  </button>
  <dialog id="add_product" class="modal">
    <div class="modal-box">
      <form method="dialog" v-on:submit.prevent="closeModal">
        <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">
          ✕
        </button>
      </form>
      <template v-if="!retailer">
        <retailer-picker v-on:selected="setRetailer" />
      </template>
      <template v-if="retailer">
        <div class="text-md">
          Retailer
          <a
            class="underline text-primary cursor-pointer"
            v-on:click="retailer = null"
            >{{ retailer.id }} : {{ retailer.name }}</a
          >
        </div>
        <form v-on:submit.prevent="addProduct" class="space-y-2 mt-4">
          <label class="form-control w-full">
            <div class="label">
              <span class="label-text">Name</span>
            </div>
            <input
              type="text"
              class="input input-bordered w-full input-md text-lg"
              v-model="name"
              autofocus
            />
          </label>
          <label class="form-control w-full">
            <div class="label">
              <span class="label-text">Date</span>
            </div>
            <input
              type="date"
              class="input input-bordered w-full input-md text-lg"
              :value="dateToStr(date)"
              @input="date = $event.target.valueAsDate"
            />
          </label>
          <label class="form-control w-full">
            <div class="label">
              <span class="label-text">Weight</span>
            </div>
            <input
              type="number"
              class="input input-bordered w-full input-md text-lg"
              v-model="weight"
              min="0"
              step="0.1"
            />
          </label>
          <label class="form-control w-full">
            <div class="label">
              <span class="label-text">Quality</span>
            </div>
            <input
              type="number"
              class="input input-bordered w-full input-md text-lg"
              v-model="quality"
              min="0"
              step="0.1"
            />
          </label>
          <label class="form-control w-full">
            <div class="label">
              <span class="label-text">Rate per gram</span>
            </div>
            <input
              type="number"
              class="input input-bordered w-full input-md text-lg"
              v-model="ratePerGram"
              min="0"
              step="0.1"
            />
          </label>
          <label class="form-control w-full">
            <div class="label">
              <span class="label-text">Total amount</span>
            </div>
            <input
              type="number"
              class="input input-bordered w-full input-md text-lg"
              v-model="totalAmount"
              min="0"
              step="0.1"
            />
          </label>
          <label class="form-control w-full">
            <div class="label">
              <span class="label-text">Payment due date</span>
            </div>
            <input
              type="date"
              class="input input-bordered w-full input-md text-lg"
              :value="dateToStr(paymentDueDate)"
              @input="paymentDueDate = $event.target.valueAsDate"
            />
          </label>
          <label class="form-control w-full">
            <div class="label">
              <span class="label-text">Image</span>
            </div>
            <input
              type="file"
              @change="onFileChanged($event)"
              accept="image/*"
              class="file-input file-input-bordered file-input-md w-full text-lg"
              capture
            />
            <div v-if="formImageThumb && !formImageLoading">
              <img
                v-if="formImageThumb"
                :src="formImageThumb"
                alt="Product image"
                class="mt-2 rounded-lg max-h-60"
              />
            </div>
            <div v-if="formImageLoading">Uploading ...</div>
          </label>
        </form>
        <div v-if="error" class="mt-4 whitespace-pre-line text-error">
          {{ error }}
        </div>
        <div class="modal-action justify-between">
          <button
            class="btn btn-secondary"
            :disabled="loading"
            v-on:click="closeModal"
          >
            Cancel
          </button>
          <button
            class="btn btn-primary"
            :disabled="loading"
            v-on:click="addProduct"
          >
            Save
          </button>
        </div>
      </template>
    </div>
  </dialog>
</template>

<script setup>
import { ref } from "vue";
import { httpClient } from "@/services/http.js";
import RetailerPicker from "@/components/RetailerPicker.vue";

const retailer = ref(null);
const name = ref("");
const date = ref(new Date());
const weight = ref(0);
const quality = ref(0);
const ratePerGram = ref(0);
const totalAmount = ref(0);
const paymentDueDate = ref(new Date());
const loading = ref(false);
const formImageId = ref(null);
const formImageThumb = ref(null);
const formImageLoading = ref(false);
const error = ref("");

const emit = defineEmits(["productAdded"]);

const dateToStr = (d) => {
  // alternative implementations in https://stackoverflow.com/q/23593052/1850609
  return (
    d &&
    new Date(d.getTime() - d.getTimezoneOffset() * 60 * 1000)
      .toISOString()
      .split("T")[0]
  );
};

const clearFields = () => {
  retailer.value = null;
  name.value = "";
  date.value = new Date();
  weight.value = 0;
  quality.value = 0;
  ratePerGram.value = 0;
  totalAmount.value = 0;
  paymentDueDate.value = new Date();
  formImageId.value = null;
  formImageThumb.value = null;
  formImageLoading.value = false;
  error.value = "";
};

const parseError = (r) => {
  if (r.detail) {
    return r.detail.map((d) => `${d.loc.slice(-1)}: ${d.msg}.`).join("\n");
  } else if (r.message) {
    return r.message;
  } else {
    return "Internal server error.";
  }
};

const onFileChanged = async (event) => {
  formImageLoading.value = true;
  try {
    const body = new FormData();
    body.append("file", event.target.files[0]);
    const result = await httpClient.post(`/api/images/upload`, null, body);
    formImageId.value = result["id"];
    formImageThumb.value = result["thumb_url"];
  } finally {
    formImageLoading.value = false;
  }
};

const setRetailer = (r) => {
  retailer.value = r;
};

const closeModal = () => {
  add_product.close();
};

const addProduct = async () => {
  loading.value = true;
  try {
    const resp = await httpClient.post(
      `/api/products`,
      {
        name: name.value,
        date: dateToStr(date.value),
        weight: weight.value,
        quality: quality.value,
        rate_per_gram: ratePerGram.value,
        total_amount: totalAmount.value,
        payment_due_date: dateToStr(paymentDueDate.value),
        retailer_id: retailer.value.id,
        image_id: formImageId.value,
      },
      null,
      { showToast: false },
    );
    add_product.close();
    clearFields();
    emit("productAdded");
  } catch (e) {
    error.value = parseError(e);
    console.log(e);
  } finally {
    loading.value = false;
  }
};
</script>
