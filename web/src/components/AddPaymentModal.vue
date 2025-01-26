<template>
  <button class="btn btn-sm btn-primary" onclick="add_payment.showModal()">
    Add a payment
  </button>
  <dialog id="add_payment" class="modal">
    <div class="modal-box">
      <form method="dialog" v-on:submit.prevent="closeModal">
        <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">
          ✕
        </button>
      </form>
      <template v-if="!supplier">
        <supplier-picker v-on:selected="setSupplier" />
      </template>
      <template v-if="supplier">
        <div class="text-md">
          Supplier
          <a
            class="underline text-primary cursor-pointer"
            v-on:click="supplier = null"
            >{{ supplier.id }} : {{ supplier.name }}</a
          >
        </div>
        <form v-on:submit.prevent="addPayment" class="space-y-2 mt-4">
          <div
            role="tablist"
            class="tabs tabs-boxed mt-10 sm:mx-auto sm:w-full sm:max-w-sm"
          >
            <a
              role="tab"
              :class="{ tab: true, 'tab-active': type === 1 }"
              v-on:click="type = 1"
              >Cash</a
            >
            <a
              role="tab"
              :class="{ tab: true, 'tab-active': type === 2 }"
              v-on:click="type = 2"
              >Bank transfer</a
            >
            <a
              role="tab"
              :class="{ tab: true, 'tab-active': type === 3 }"
              v-on:click="type = 3"
              >Goods</a
            >
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
              autofocus
            />
          </div>
          <div class="form-control w-full" v-if="type === 3">
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
          <div class="form-control w-full" v-if="type === 3">
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
          <div class="form-control w-full" v-if="type === 3">
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
            v-on:click="addPayment"
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
import SupplierPicker from "@/components/SupplierPicker.vue";

const supplier = ref(null);
const type = ref(1);
const typeError = ref(null);
const date = ref(new Date());
const dateError = ref(null);
const weight = ref(null);
const weightError = ref(null);
const quality = ref(null);
const qualityError = ref(null);
const ratePerGram = ref(null);
const ratePerGramError = ref(null);
const totalAmount = ref(0);
const totalAmountError = ref(null);
const loading = ref(false);
const error = ref(null);

const emit = defineEmits(["paymentAdded"]);

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
  supplier.value = null;
  type.value = 1;
  date.value = new Date();
  weight.value = null;
  quality.value = null;
  ratePerGram.value = null;
  totalAmount.value = 0;
  error.value = null;
  typeError.value = null;
  dateError.value = null;
  weightError.value = null;
  qualityError.value = null;
  ratePerGramError.value = null;
  totalAmountError.value = null;
};

const setSupplier = (r) => {
  supplier.value = r;
};

const closeModal = () => {
  add_payment.close();
};

watch([type, date, weight, quality, ratePerGram, totalAmount], () => {
  typeError.value = null;
  dateError.value = null;
  weightError.value = null;
  qualityError.value = null;
  ratePerGramError.value = null;
  totalAmountError.value = null;
});

const addPayment = async () => {
  const data = {
    type: type.value,
    date: dateToStr(date.value),
    total_amount: totalAmount.value,
    supplier_id: supplier.value.id,
  };
  if (type.value === 3) {
    data["weight"] = weight.value;
    data["quality"] = quality.value;
    data["rate_per_gram"] = ratePerGram.value;
  }

  loading.value = true;
  try {
    await httpClient.post(`/api/payments`, data, null, { showToast: false });
    add_payment.close();
    clearFields();
    emit("paymentAdded");
  } catch (e) {
    error.value = parseError(e);
    typeError.value = parseError(e, "type");
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
