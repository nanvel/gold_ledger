<template>
  <button class="btn btn-primary" onclick="add_product.showModal()">
    <svg
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-6"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M12 4.5v15m7.5-7.5h-15"
      />
    </svg>
    Product
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
              <span class="label-text">Rate</span>
              <span class="label-text">₹/g</span>
            </div>
            <input
              type="number"
              class="input input-bordered w-full input-md text-lg"
              v-model="rate"
              min="0"
              step="0.1"
            />
            <div class="label" v-if="rateError">
              <span class="label-text-alt text-error">{{ rateError }}</span>
            </div>
          </div>
          <div class="form-control w-full pb-4">
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
          <div class="p-4 rounded-md bg-base-300">
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
            <div class="form-control w-full" v-if="paymentType !== 3">
              <div class="label">
                <span class="label-text">Amount</span>
                <span class="label-text">₹</span>
              </div>
              <input
                type="number"
                class="input input-bordered w-full input-md text-lg"
                v-model="paymentAmount"
                min="0"
                step="0.1"
              />
              <div class="label" v-if="paymentAmountError">
                <span class="label-text-alt text-error">{{
                  paymentAmountError
                }}</span>
              </div>
            </div>
            <div class="form-control w-full" v-if="paymentType === 3">
              <div class="label">
                <span class="label-text">Weight</span>
                <span class="label-text">g</span>
              </div>
              <input
                type="number"
                class="input input-bordered w-full input-md text-lg"
                v-model="paymentWeight"
                min="0"
                step="0.1"
              />
              <div class="label" v-if="paymentWeightError">
                <span class="label-text-alt text-error">{{
                  paymentWeightError
                }}</span>
              </div>
            </div>
            <div class="form-control w-full" v-if="paymentType === 3">
              <div class="label">
                <span class="label-text">Quality</span>
                <span class="label-text">%</span>
              </div>
              <input
                type="number"
                class="input input-bordered w-full input-md text-lg"
                v-model="paymentQuality"
                min="0"
                max="100"
                step="0.1"
              />
              <div class="label" v-if="paymentQualityError">
                <span class="label-text-alt text-error">{{
                  paymentQualityError
                }}</span>
              </div>
            </div>
            <div class="form-control w-full">
              <div class="label">
                <span class="label-text">Due date</span>
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
const rate = ref(0);
const rateError = ref(null);
const paymentType = ref(1);
const paymentTypeError = ref(null);
const paymentAmount = ref(0);
const paymentAmountError = ref(null);
const paymentWeight = ref(0);
const paymentWeightError = ref(null);
const paymentQuality = ref(0);
const paymentQualityError = ref(null);
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
  rate.value = 0;
  paymentAmount.value = 0;
  paymentWeight.value = 0;
  paymentQuality.value = 0;
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
    rate,
    paymentAmount,
    paymentQuality,
    paymentWeight,
    paymentType,
    paymentDueDate,
  ],
  () => {
    nameError.value = null;
    dateError.value = null;
    weightError.value = null;
    qualityError.value = null;
    rateError.value = null;
    paymentAmountError.value = null;
    paymentWeightError.value = null;
    paymentQualityError.value = null;
    paymentDueDateError.value = null;
    paymentTypeError.value = null;
  },
);

const addProduct = async () => {
  loading.value = true;
  const data = {
    name: name.value,
    date: dateToStr(date.value),
    weight: weight.value,
    quality: quality.value,
    rate: rate.value,
    payment_type: paymentType.value,
    payment_due_date: dateToStr(paymentDueDate.value),
    retailer_id: retailer.value.id,
    image_id: imageId.value,
  };
  if (paymentType.value === 3) {
    data["payment_weight"] = paymentWeight.value;
    data["payment_quality"] = paymentQuality.value;
  } else {
    data["payment_amount"] = paymentAmount.value;
  }
  try {
    await httpClient.post(`/api/products`, data, null, { showToast: false });
    add_product.close();
    clearFields();
    emit("productAdded");
  } catch (e) {
    error.value = parseError(e);
    nameError.value = parseError(e, "name");
    dateError.value = parseError(e, "date");
    weightError.value = parseError(e, "weight");
    qualityError.value = parseError(e, "quality");
    rateError.value = parseError(e, "rate");
    paymentTypeError.value = parseError(e, "payment_type");
    paymentAmountError.value = parseError(e, "payment_amount");
    paymentQualityError.value = parseError(e, "payment_quality");
    paymentWeightError.value = parseError(e, "payment_weight");
    paymentDueDateError.value = parseError(e, "payment_due_date");
    imageIdError.value = parseError(e, "image_id");
  } finally {
    loading.value = false;
  }
};
</script>
