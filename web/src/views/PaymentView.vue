<template>
  <Navbar>
    <div class="flex flex-col space-y-4 pt-4" v-if="details">
      <div class="text-lg">
        Payment: {{ details.type }}
        <StatusBadge :status="details.status" />
      </div>
      <div>
        <div class="badge badge-neutral">
          {{ details.retailer.id }} : {{ details.retailer.name }}
        </div>
        paid to
        <div class="badge badge-neutral">
          {{ details.supplier.id }} : {{ details.supplier.name }}
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
          <confirm-payment-modal
            :payment="details"
            v-if="isSupplier"
            v-on:done="onAction"
          />
          <reject-payment-modal
            :payment="details"
            v-if="isSupplier"
            v-on:done="onAction"
          />
          <cancel-payment-modal
            :payment="details"
            v-if="!isSupplier"
            v-on:done="onAction"
          />
        </div>
      </div>

      <descriptive-table :rows="tableRows" />

      <activities-table :payment-id="details.id" :key="activitiesKey" />
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
import ActivitiesTable from "@/components/ActivitiesTable.vue";
import StatusBadge from "@/components/StatusBadge.vue";
import DescriptiveTable from "@/components/DescriptiveTable.vue";
import ConfirmPaymentModal from "@/components/ConfirmPaymentModal.vue";
import RejectPaymentModal from "@/components/RejectPaymentModal.vue";
import CancelPaymentModal from "@/components/CancelPaymentModal.vue";
import { timestampToString } from "@/services/time.js";

const meStore = useMeStore();

const { isSupplier } = storeToRefs(meStore);

const paymentId = ref(parseInt(router.currentRoute.value.params.id));
const details = ref(null);
const loading = ref(true);
const activitiesKey = ref(0);

const tableRows = computed(() => {
  if (!details.value) {
    return [];
  }
  const res = [["Type", `${details.value.type}`]];

  if (details.value.type === "Fine") {
    res.push(["Weight", `${details.weight}g`]);
    res.push(["Quality", `${details.quality}%`]);
  } else {
    res.push(["Amount", `${details.value.amount}₹`]);
  }

  res.push([
    "Created by",
    details.value.creator.name || details.value.creator.email,
  ]);
  res.push(["Created at", timestampToString(details.value.created_at)]);

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

const loadPayment = async () => {
  loading.value = true;
  try {
    details.value = await httpClient.get(`/api/payments/${paymentId.value}`);
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
};

const onAction = async () => {
  await loadPayment();
  activitiesKey.value += 1;
};

onMounted(async () => {
  await loadPayment();
});
</script>
