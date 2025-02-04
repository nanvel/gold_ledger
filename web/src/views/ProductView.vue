<template>
  <Navbar>
    <div class="flex flex-col space-y-4 pt-4" v-if="details">
      <div class="text-lg">
        Product: {{ details.name }}
        <StatusBadge :status="details.status" />
      </div>
      <div>
        <div class="badge badge-neutral">
          {{ details.supplier.id }} : {{ details.supplier.name }}
        </div>
        delivered to
        <div class="badge badge-neutral">
          {{ details.retailer.id }} : {{ details.retailer.name }}
        </div>
        on
        {{ details.date }}
      </div>
      <div class="flex flex-row items-center space-x-4">
        <div
          v-if="
            details &&
            !(
              details.confirmed_by ||
              details.rejected_by ||
              details.cancelled_by
            )
          "
          class="flex flex-row space-x-2"
        >
          <confirm-product-modal
            :product="details"
            v-if="isRetailer"
            v-on:done="onAction"
          />
          <reject-product-modal
            :product="details"
            v-if="isRetailer"
            v-on:done="onAction"
          />
          <cancel-product-modal
            :product="details"
            v-if="!isRetailer"
            v-on:done="onAction"
          />
        </div>
      </div>

      <div v-if="details.images?.length">
        <img
          :alt="details.name"
          :src="details.images[0].thumb_url"
          class="rounded-md"
        />
        <a :href="details.images[0].url" target="_blank" class="text-sm link"
          >Original image</a
        >
      </div>

      <descriptive-table :rows="tableRows" />

      <activities-table :product-id="details.id" :key="activitiesKey" />
    </div>
  </Navbar>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { httpClient } from "@/services/http.js";
import router from "@/router/index.js";
import Navbar from "@/components/Navbar.vue";
import { useMeStore } from "@/stores/index.js";
import { storeToRefs } from "pinia";
import { timestampToString } from "@/services/time.js";
import ActivitiesTable from "@/components/ActivitiesTable.vue";
import ConfirmProductModal from "@/components/ConfirmProductModal.vue";
import RejectProductModal from "@/components/RejectProductModal.vue";
import CancelProductModal from "@/components/CancelProductModal.vue";
import StatusBadge from "@/components/StatusBadge.vue";
import DescriptiveTable from "@/components/DescriptiveTable.vue";

const meStore = useMeStore();

const { isRetailer } = storeToRefs(meStore);

const productId = ref(parseInt(router.currentRoute.value.params.id));
const details = ref(null);
const loading = ref(true);
const activitiesKey = ref(0);

const tableRows = computed(() => {
  if (!details.value) {
    return [];
  }
  const res = [
    ["Weight", `${details.value.weight}g`],
    ["Quality", `${details.value.quality}%`],
    ["Rate", `${details.value.rate}₹/g`],
    [
      "Payment",
      details.value.payment_type === "fine"
        ? `${details.value.payment_type} ${details.value.payment_weight}g @ ${details.value.payment_quality}% by ${details.value.payment_due_date}`
        : `${details.value.payment_type} ${details.value.payment_amount}₹ by ${details.value.payment_due_date}`,
    ],
    ["Created by", details.value.creator.name || details.value.creator.email],
    ["Created at", timestampToString(details.value.created_at)],
  ];
  if (details.value.confirmed_by) {
    res.push([
      "Confirmed by",
      details.value.confirmed_by.name || details.value.confirmed_by.email,
    ]);
  }
  if (details.value.rejected_by) {
    res.push([
      "Rejected by",
      details.value.rejected_by.name || details.value.rejected_by.email,
    ]);
  }
  if (details.value.canceled_by) {
    res.push([
      "Canceled by",
      details.value.canceled_by.name || details.value.canceled_by.email,
    ]);
  }

  return res;
});

const onAction = async () => {
  await loadProduct();
  activitiesKey.value += 1;
};

const loadProduct = async () => {
  loading.value = true;
  try {
    details.value = await httpClient.get(`/api/products/${productId.value}`);
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  await loadProduct();
});
</script>
