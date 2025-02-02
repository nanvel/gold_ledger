<template>
  <div class="overflow-x-auto">
    <placeholder v-if="loading" loading />
    <table class="table table-sm table-zebra" v-if="staff.length && !loading">
      <thead>
        <tr>
          <th>Email</th>
          <th>Name</th>
          <th>Created</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="s in staff" :key="s.id">
          <td>
            {{ s.email }}
          </td>
          <td>
            {{ s.name }}
          </td>
          <td>
            <timestamp :value="s.created_at" />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import Timestamp from "@/components/Timestamp.vue";
import { httpClient } from "@/services/http.js";
import Placeholder from "@/components/Placeholder.vue";

const loading = ref(false);
const staff = ref([]);
const total = ref(0);

const loadStaff = async () => {
  loading.value = true;
  try {
    const response = await httpClient.get("/api/staff", null, null);
    staff.value = response["items"];
    total.value = response["total"];
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  await loadStaff();
});
</script>
