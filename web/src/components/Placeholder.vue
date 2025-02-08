<template>
  <div
    :class="{
      rounded: true,
      'text-center': true,
      flex: true,
      'flex-col': true,
      'justify-center': true,
      'py-4': true,
      border: true,
      'border-base-300': true,
      skeleton: props.loading,
    }"
  >
    <div class="flex-row space-x-4">
      <span v-if="props.text" class="text-sm text-base-content">{{
        props.text
      }}</span>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  text: {
    type: String,
    default: null,
  },
  loading: {
    type: Boolean,
    default: false,
  },
});
</script>
