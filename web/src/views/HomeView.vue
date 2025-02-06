<template>
  <Navbar>
    <div class="divider">
      <RouterLink to="/balance-sheet" class="link"
        >Balance sheet (view all)</RouterLink
      >
    </div>
    <balance-sheet-summary />
    <div class="divider">Activities</div>
    <activities-table />
  </Navbar>
</template>

<script setup>
import Navbar from "@/components/Navbar.vue";
import ActivitiesTable from "@/components/ActivitiesTable.vue";
import BalanceSheetSummary from "@/components/BalanceSheetSummary.vue";
import { RouterLink } from "vue-router";
</script>
