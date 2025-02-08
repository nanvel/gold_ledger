<template>
  <div v-if="row.shouldShow" class="border border-base-300 rounded-md">
    <div
      class="bg-base-300 py-1 px-2 rounded-md rounded-b-none justify-between flex flex-row"
    >
      <span class="capitalize">{{ paymentType }}</span>
      <div>
        {{ row.pending }}{{ unit }} <span class="text-sm">pending</span>
      </div>
    </div>
    <div class="m-1">
      {{ row.products }}{{ unit }} <span class="text-sm">products</span> -
      {{ row.payments }}{{ unit }}
      <span class="text-sm">payments</span>
    </div>
    <div
      v-for="payment in duePayments"
      :class="['m-1', 'border-t', 'border-base-300', dueColor(payment.date)]"
    >
      {{ payment.amount }}{{ unit }} by {{ payment.date }}
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  row: Object,
  paymentType: String,
});

const unit = computed(() => {
  return props.paymentType === "fine" ? "g" : "₹";
});

const duePayments = computed(() => {
  if (!props.row?.due_payments) return [];
  return [
    ...props.row.due_payments.filter(
      (payment) => payment.type === props.paymentType,
    ),
  ];
});

const dueColor = (d) => {
  const today = new Date();
  const due = new Date(d);
  const diff = due - today;
  const daysRemain = Math.ceil(diff / (1000 * 60 * 60 * 24));

  if (daysRemain < 0) return "text-error";
  if (daysRemain < 3) return "text-warning";
  return "text-secondary";
};

const row = computed(() => {
  const products = props.row[`${props.paymentType}_products`];
  const payments = props.row[`${props.paymentType}_payments`];
  return {
    products: products,
    payments: payments,
    pending: products - payments,
    shouldShow: products || payments,
  };
});
</script>
