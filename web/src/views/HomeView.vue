<template>
  <Navbar>
    <div class="flex flex-col space-y-4">
      <div class="divider">
        <RouterLink to="/balance-sheet" class="link"
          >Balance sheet (view details)</RouterLink
        >
      </div>
      <balance-sheet-summary />
      <div class="divider">Activities</div>
      <activities-table />
    </div>
  </Navbar>
</template>

<script setup>
import Navbar from "@/components/Navbar.vue";
import ActivitiesTable from "@/components/ActivitiesTable.vue";
import BalanceSheetSummary from "@/components/BalanceSheetSummary.vue";
import { RouterLink } from "vue-router";
</script>
