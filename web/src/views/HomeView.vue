<template>
  <Navbar>
    <placeholder text="Loading ..." loading />
    <activities-table />
  </Navbar>
</template>

<script setup>
import Navbar from "@/components/Navbar.vue";
import ActivitiesTable from "@/components/ActivitiesTable.vue";
import Placeholder from "@/components/Placeholder.vue";
</script>
