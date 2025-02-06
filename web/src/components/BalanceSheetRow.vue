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
    <div v-if="row.dueDate" class="m-1 border-t text-secondary border-base-300">
      Pay {{ row.toPay }}{{ unit }} by {{ row.dueDate
      }}<span v-if="row.dueToday" class="text-warning pl-2">due today</span
      ><span v-if="row.overdue" class="text-error pl-2">overdue!</span>
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

const row = computed(() => {
  const products = props.row[`${props.paymentType}_products`];
  const payments = props.row[`${props.paymentType}_payments`];
  const d = new Date();
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, "0");
  const dd = String(d.getDate()).padStart(2, "0");
  const today = `${yyyy}-${mm}-${dd}`;
  const dueDate = props.row[`${props.paymentType}_due_date`];
  return {
    products: products,
    payments: payments,
    pending: products - payments,
    dueDate: dueDate,
    toPay: props.row[`${props.paymentType}_to_pay`],
    shouldShow: products + payments > 0,
    dueToday: dueDate ? dueDate === today : null,
    overdue: dueDate ? dueDate < today : null,
  };
});
</script>
