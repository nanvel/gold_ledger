<template>
  <div :class="['badge', 'capitalize', badge, 'ml-2']">
    {{ props.status }}
  </div>
</template>

<script setup>
import { defineProps, computed } from "vue";

const props = defineProps({
  status: String,
});

const colorMap = {
  pending: "warning",
  confirmed: "success",
  rejected: "error",
  canceled: "info",
};

const badge = computed(() => {
  return "badge-" + (colorMap[props.status] || "neutral");
});
</script>
