<template>
  <navbar
    ><div class="flex flex-col space-y-4">
      <div><invite-modal target="supplier" /></div>
      <suppliers-list /></div
  ></navbar>
</template>

<script setup>
import Navbar from "@/components/Navbar.vue";
import InviteModal from "@/components/InviteModal.vue";
import SuppliersList from "@/components/SuppliersList.vue";
</script>
