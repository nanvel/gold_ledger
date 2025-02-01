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
          Retailer {{ retailer.id }} : {{ retailer.name }}
        </div>
        <form v-on:submit.prevent="addProduct" class="space-y-2 mt-4">
          <div class="form-control w-full">
            <div class="label">
              <span class="label-text">Name</span>
            </div>
            <input
              type="text"
              class="input input-bordered w-full input-md text-lg"
              v-model="name"
              autofocus
            />
            <div class="label" v-if="nameError">
              <span class="label-text-alt text-error">{{ nameError }}</span>
            </div>
          </div>
          <div class="form-control w-full">
            <div class="label">
              <span class="label-text">Date</span>
            </div>
            <input
              type="date"
              class="input input-bordered w-full input-md text-lg"
              :value="dateToStr(date)"
              @input="date = $event.target.valueAsDate"
            />
            <div class="label" v-if="dateError">
              <span class="label-text-alt text-error">{{ dateError }}</span>
            </div>
          </div>
          <div class="form-control w-full">
            <div class="label">
              <span class="label-text">Weight</span>
              <span class="label-text">g</span>
            </div>
            <input
              type="number"
              class="input input-bordered w-full input-md text-lg"
              v-model="weight"
              min="0"
              step="0.1"
            />
            <div class="label" v-if="weightError">
              <span class="label-text-alt text-error">{{ weightError }}</span>
            </div>
          </div>
          <div class="form-control w-full">
            <div class="label">
              <span class="label-text">Quality</span>
              <span class="label-text">%</span>
            </div>
            <input
              type="number"
              class="input input-bordered w-full input-md text-lg"
              v-model="quality"
              min="0"
              max="100"
              step="0.1"
            />
            <div class="label" v-if="qualityError">
              <span class="label-text-alt text-error">{{ qualityError }}</span>
            </div>
          </div>
          <div class="form-control w-full">
            <div class="label">
              <span class="label-text">Rate per gram</span>
              <span class="label-text">₹</span>
            </div>
            <input
              type="number"
              class="input input-bordered w-full input-md text-lg"
              v-model="ratePerGram"
              min="0"
              step="0.1"
            />
            <div class="label" v-if="ratePerGramError">
              <span class="label-text-alt text-error">{{
                ratePerGramError
              }}</span>
            </div>
          </div>
          <div class="form-control w-full">
            <div class="label">
              <span class="label-text">Payment type</span>
            </div>
            <div role="tablist" class="tabs tabs-boxed border-neutral border">
              <a
                role="tab"
                :class="{ tab: true, 'tab-active': paymentType === 1 }"
                v-on:click="paymentType = 1"
                >Cash</a
              >
              <a
                role="tab"
                :class="{ tab: true, 'tab-active': paymentType === 2 }"
                v-on:click="paymentType = 2"
                >RTGS</a
              >
              <a
                role="tab"
                :class="{ tab: true, 'tab-active': paymentType === 3 }"
                v-on:click="paymentType = 3"
                >Fine</a
              >
            </div>
            <div class="label" v-if="paymentTypeError">
              <span class="label-text-alt text-error">{{
                paymentTypeError
              }}</span>
            </div>
          </div>
          <div class="form-control w-full">
            <div class="label">
              <span class="label-text">Total amount</span>
              <span class="label-text">₹</span>
            </div>
            <input
              type="number"
              class="input input-bordered w-full input-md text-lg"
              v-model="totalAmount"
              min="0"
              step="0.1"
            />
            <div class="label" v-if="totalAmountError">
              <span class="label-text-alt text-error">{{
                totalAmountError
              }}</span>
            </div>
          </div>
          <div class="form-control w-full">
            <div class="label">
              <span class="label-text">Payment due date</span>
            </div>
            <input
              type="date"
              class="input input-bordered w-full input-md text-lg"
              :value="dateToStr(paymentDueDate)"
              @input="paymentDueDate = $event.target.valueAsDate"
            />
            <div class="label" v-if="paymentDueDateError">
              <span class="label-text-alt text-error">{{
                paymentDueDateError
              }}</span>
            </div>
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
            />
            <div v-if="imageThumb && !imageLoading">
              <img
                v-if="imageThumb"
                :src="imageThumb"
                alt="Product image"
                class="mt-2 rounded-lg max-h-60"
              />
            </div>
            <div v-if="imageLoading">Uploading ...</div>
            <div class="label" v-if="imageIdError && !imageLoading">
              <span class="label-text-alt text-error">{{ imageIdError }}</span>
            </div>
          </div>
        </form>
        <div v-if="error" class="mt-4 whitespace-pre-line text-error text-sm">
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
const paymentType = ref(1);
const paymentTypeError = ref(null);
const paymentDueDate = ref(new Date());
const paymentDueDateError = ref(null);
const loading = ref(false);
const imageId = ref(null);
const imageIdError = ref(null);
const imageThumb = ref(null);
const imageLoading = ref(false);
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
  paymentType.value = 1;
  paymentDueDate.value = new Date();
  imageId.value = null;
  imageThumb.value = null;
  imageLoading.value = false;
  error.value = null;
};

const onFileChanged = async (event) => {
  imageLoading.value = true;
  try {
    const body = new FormData();
    body.append("file", event.target.files[0]);
    const result = await httpClient.post(`/api/images/upload`, null, body);
    imageId.value = result["id"];
    imageThumb.value = result["thumb_url"];
  } finally {
    imageLoading.value = false;
  }
};

const setRetailer = (r) => {
  retailer.value = r;
};

const closeModal = () => {
  add_product.close();
};

watch(
  [
    name,
    date,
    weight,
    quality,
    ratePerGram,
    totalAmount,
    paymentType,
    paymentDueDate,
  ],
  () => {
    nameError.value = null;
    dateError.value = null;
    weightError.value = null;
    qualityError.value = null;
    ratePerGramError.value = null;
    totalAmountError.value = null;
    paymentDueDateError.value = null;
    paymentTypeError.value = null;
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
        payment_type: paymentType.value,
        payment_due_date: dateToStr(paymentDueDate.value),
        retailer_id: retailer.value.id,
        image_id: imageId.value,
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
    paymentTypeError.value = parseError(e, "payment_type");
    paymentDueDateError.value = parseError(e, "payment_due_date");
    imageIdError.value = parseError(e, "image_id");
  } finally {
    loading.value = false;
  }
};
</script>
