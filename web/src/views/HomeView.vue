<template>
  <Navbar>
    <div class="flex flex-col space-y-8 pb-4">
      <div class="divider mb-0">
        <RouterLink to="/balance-sheet" class="link"
          >Balance sheet (view details)</RouterLink
        >
      </div>
      <balance-sheet-summary />
      <div class="divider" v-if="isSupplier">
        Payments to confirm
        <template v-if="totalToConfirm">({{ totalToConfirm }})</template>
      </div>
      <payments-pending-approval
        v-if="isSupplier"
        v-on:setTotal="onTotalToConfirm"
      />
      <div class="divider" v-if="!isSupplier">
        Products to confirm
        <template v-if="totalToConfirm">({{ totalToConfirm }})</template>
      </div>
      <products-pending-approval
        v-if="!isSupplier"
        v-on:setTotal="onTotalToConfirm"
      />
      <div class="divider">Activities</div>
      <activities-table />
    </div>
  </Navbar>
</template>

<script setup>
import { ref } from "vue";
import Navbar from "@/components/Navbar.vue";
import ActivitiesTable from "@/components/ActivitiesTable.vue";
import BalanceSheetSummary from "@/components/BalanceSheetSummary.vue";
import { RouterLink } from "vue-router";
import { useMeStore } from "@/stores/index.js";
import { storeToRefs } from "pinia";
import ProductsPendingApproval from "@/components/ProductsPendingApproval.vue";
import PaymentsPendingApproval from "@/components/PaymentsPendingApproval.vue";

const meStore = useMeStore();

const totalToConfirm = ref(0);

const onTotalToConfirm = (total) => {
  totalToConfirm.value = total;
};

const { isSupplier } = storeToRefs(meStore);
</script>
