<template>
  <div class="drawer lg:drawer-open">
    <input id="my-drawer-2" type="checkbox" class="drawer-toggle" />
    <div class="drawer-content flex flex-col items-center justify-center">
      <!-- Page content here -->
      <label for="my-drawer-2" class="btn btn-primary drawer-button lg:hidden">
        Open drawer
      </label>
    </div>
    <div class="drawer-side">
      <label
        for="my-drawer-2"
        aria-label="close sidebar"
        class="drawer-overlay"
      ></label>
      <ul class="menu bg-base-200 text-base-content min-h-full w-80 p-4">
        <li><a>Retailers</a></li>
        <li><a>Products</a></li>
        <li><LogOutButton /></li>
        <li>
          <DarkModeToggle />
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import DarkModeToggle from "@/components/DarkModeToggle.vue";
import LogOutButton from "@/components/LogOutButton.vue";
import { onMounted } from "vue";
import { httpClient } from "@/services/http.js";

onMounted(async () => {
  const resp = await httpClient.get("/api/me");
  console.log(resp.data);
});
</script>
