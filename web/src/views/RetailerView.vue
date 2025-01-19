<template>
  <Navbar>
    <article class="prose lg:prose-xl py-4 px-2">
      <h2>{{ retailerName }}</h2>
    </article>

    <AddProduct :retailer_id="retailerId" />
  </Navbar>
</template>

<script setup>
import Navbar from "@/components/Navbar.vue";
import { onMounted, ref } from "vue";
import { httpClient } from "@/services/http.js";
import router from "@/router";
import AddProduct from "@/components/AddProduct.vue";

const retailerName = ref(false);
const retailerId = ref(parseInt(router.currentRoute.value.params.id));

onMounted(async () => {
  const resp = await httpClient.get(
    `/api/retailers/${retailerId.value}`,
    null,
    null,
  );

  retailerName.value = resp["name"];
});
</script>
