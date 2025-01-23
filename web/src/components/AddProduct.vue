<template>
  <button
    class="btn btn-wide btn-primary text-md"
    onclick="add_product.showModal()"
  >
    Add a product sold
  </button>
  <dialog id="add_product" class="modal">
    <div class="modal-box">
      <form method="dialog">
        <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">
          ✕
        </button>
      </form>
      <form v-on:submit.prevent="addProduct" class="space-y-2">
        <label class="form-control w-full">
          <div class="label">
            <span class="label-text">Name:</span>
          </div>
          <input
            type="text"
            class="input input-bordered w-full input-md text-lg"
            v-model="name"
          />
        </label>
        <label class="form-control w-full">
          <div class="label">
            <span class="label-text">Date:</span>
          </div>
          <input
            type="date"
            class="input input-bordered w-full input-md text-lg"
            v-model.lazy="date"
          />
        </label>
        <label class="form-control w-full">
          <div class="label">
            <span class="label-text">Weight:</span>
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
            <span class="label-text">Quality:</span>
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
            <span class="label-text">Rate per gram:</span>
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
            <span class="label-text">Total amount:</span>
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
            <span class="label-text">Image:</span>
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
      <div class="modal-action justify-between">
        <form
          method="dialog"
          class="flex flex-row gap-4 justify-between"
          v-on:submit.prevent="addProduct"
        >
          <button class="btn btn-secondary" :disabled="loading">Cancel</button>
        </form>
        <button class="btn btn-primary" :disabled="loading">Save</button>
      </div>
    </div>
  </dialog>
</template>

<script setup>
import { ref } from "vue";
import { httpClient } from "@/services/http.js";
import { useToast } from "vue-toastification";

const props = defineProps({
  retailer_id: Number,
});

const name = ref("");
const date = ref(new Date());
const weight = ref(0);
const quality = ref(0);
const ratePerGram = ref(0);
const totalAmount = ref(0);
const loading = ref(false);
const formImageId = ref(null);
const formImageThumb = ref(null);
const formImageLoading = ref(false);

const toast = useToast();

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

const addProduct = async () => {
  loading.value = true;
  try {
    await httpClient.post(
      `/api/products`,
      {
        name: name.value,
        date: date.value,
        weight: weight.value,
        quality: quality.value,
        rate_per_gram: ratePerGram.value,
        total_amount: totalAmount.value,
        retailer_id: props.retailer_id,
        image_id: formImageId.value,
      },
      null,
    );
    toast.success("Product added successfully.");
    add_product.showModal();
  } catch (error) {
    console.log(error);
    toast.error("Failed to add product.");
  } finally {
    loading.value = false;
  }
};
</script>
