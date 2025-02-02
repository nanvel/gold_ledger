<template>
  <div :class="['badge', `badge-${props.size}`, 'capitalize', badge, 'ml-2']">
    {{ props.status }}
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  status: String,
  size: {
    type: String,
    default: "lg",
  },
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
