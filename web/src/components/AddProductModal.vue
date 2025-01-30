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
        <div class="btn btn-neutral" v-on:click="retailer = null">
          Retailer
          <a class="underline text-primary cursor-pointer"
            >{{ retailer.id }} : {{ retailer.name }}</a
          >
        </div>
        <form v-on:submit.prevent="addProduct" class="space-y-2 mt-4">
          <div class="form-control w-full">
            <div class="label">
              <span class="label-text">Name</span>
              <span class="label-text text-error" v-if="nameError">{{
                nameError
              }}</span>
            </div>
            <input
              type="text"
              class="input input-bordered w-full input-md text-lg"
              v-model="name"
              autofocus
            />
          </div>
          <div class="form-control w-full">
            <div class="label">
              <span class="label-text">Date</span>
              <span class="label-text text-error" v-if="dateError">{{
                dateError
              }}</span>
            </div>
            <input
              type="date"
              class="input input-bordered w-full input-md text-lg"
              :value="dateToStr(date)"
              @input="date = $event.target.valueAsDate"
            />
          </div>
          <div class="form-control w-full">
            <div class="label">
              <span class="label-text">Weight</span>
              <span class="label-text text-error" v-if="weightError">{{
                weightError
              }}</span>
            </div>
            <input
              type="number"
              class="input input-bordered w-full input-md text-lg"
              v-model="weight"
              min="0"
              step="0.1"
            />
          </div>
          <div class="form-control w-full">
            <div class="label">
              <span class="label-text">Quality</span>
              <span class="label-text text-error" v-if="qualityError">{{
                qualityError
              }}</span>
            </div>
            <input
              type="number"
              class="input input-bordered w-full input-md text-lg"
              v-model="quality"
              min="0"
              step="0.1"
            />
          </div>
          <div class="form-control w-full">
            <div class="label">
              <span class="label-text">Rate per gram</span>
              <span class="label-text text-error" v-if="ratePerGramError">{{
                ratePerGramError
              }}</span>
            </div>
            <input
              type="number"
              class="input input-bordered w-full input-md text-lg"
              v-model="ratePerGram"
              min="0"
              step="0.1"
            />
          </div>
          <div class="form-control w-full">
            <div class="label">
              <span class="label-text">Total amount</span>
              <span class="label-text text-error" v-if="totalAmountError">{{
                totalAmountError
              }}</span>
            </div>
            <input
              type="number"
              class="input input-bordered w-full input-md text-lg"
              v-model="totalAmount"
              min="0"
              step="0.1"
            />
          </div>
          <div class="form-control w-full">
            <div class="label">
              <span class="label-text">Payment due date</span>
              <span class="label-text text-error" v-if="paymentDueDateError">{{
                paymentDueDateError
              }}</span>
            </div>
            <input
              type="date"
              class="input input-bordered w-full input-md text-lg"
              :value="dateToStr(paymentDueDate)"
              @input="paymentDueDate = $event.target.valueAsDate"
            />
          </div>
          <div class="form-control w-full">
            <div class="label">
              <span class="label-text">Image</span>
            </div>
            <input
              type="file"
              @change="onFileChanged($event)"
              accept="image/*"
              class="file-input file-input-bordered file-input-md w-full text-lg"
              capture="environment"
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
          </div>
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
import { ref, watch } from "vue";
import { httpClient, parseError } from "@/services/http.js";
import RetailerPicker from "@/components/RetailerPicker.vue";

const retailer = ref(null);
const name = ref("");
const nameError = ref(null);
const date = ref(new Date());
const dateError = ref(null);
const weight = ref(0);
const weightError = ref(null);
const quality = ref(0);
const qualityError = ref(null);
const ratePerGram = ref(0);
const ratePerGramError = ref(null);
const totalAmount = ref(0);
const totalAmountError = ref(null);
const paymentDueDate = ref(new Date());
const paymentDueDateError = ref(null);
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
  error.value = null;
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

watch(
  [name, date, weight, quality, ratePerGram, totalAmount, paymentDueDate],
  () => {
    nameError.value = null;
    dateError.value = null;
    weightError.value = null;
    qualityError.value = null;
    ratePerGramError.value = null;
    totalAmountError.value = null;
    paymentDueDateError.value = null;
  },
);

const addProduct = async () => {
  loading.value = true;
  try {
    await httpClient.post(
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
    nameError.value = parseError(e, "name");
    dateError.value = parseError(e, "date");
    weightError.value = parseError(e, "weight");
    qualityError.value = parseError(e, "quality");
    ratePerGramError.value = parseError(e, "rate_per_gram");
    totalAmountError.value = parseError(e, "total_amount");
  } finally {
    loading.value = false;
  }
};
</script>
