<template>
  <Navbar>
    <article class="prose lg:prose-xl py-4 px-2">
      <h2>{{ retailerName }}</h2>
    </article>
  </Navbar>
</template>

<script setup>
import Navbar from "@/components/Navbar.vue";
import { onMounted, ref } from "vue";
import { httpClient } from "@/services/http.js";
import router from "@/router";

const retailerName = ref(false);

onMounted(async () => {
  const resp = await httpClient.get(
    `/api/retailers/${router.currentRoute.value.params.id}`,
    null,
    null,
  );

  retailerName.value = resp["name"];
});
</script>
