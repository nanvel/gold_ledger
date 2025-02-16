<template>
  <navbar
    ><div class="flex flex-col space-y-4">
      <div><invite-modal target="retailer" /></div>
      <retailers-list /></div
  ></navbar>
</template>

<script setup>
import Navbar from "@/components/Navbar.vue";
import InviteModal from "@/components/InviteModal.vue";
import RetailersList from "@/components/RetailersList.vue";
</script>
