<template>
  {{ timeString }}{{ endTimeString }}
  <template v-if="showDuration">
    <span v-if="timeString.length">({{ durationString }})</span
    ><span v-else>{{ durationString }}</span>
  </template>
</template>

<script setup>
import { timestampToString, timestampToDuration } from "@/services/time.js";

const props = defineProps({
  value: {
    type: Number,
    required: true,
  },
  endValue: {
    type: Number,
    required: false,
  },
  showTime: {
    type: Boolean,
    required: false,
    default: true,
  },
  showEndTime: {
    type: Boolean,
    required: false,
    default: false,
  },
  showDuration: {
    type: Boolean,
    required: false,
    default: false,
  },
});

const timeString = timestampToString(props.value);
const endTimeString =
  props.showEndTime && props.endValue
    ? " - " + timestampToString(props.endValue)
    : "";

let durationString = timestampToDuration(props.value, props.endValue);
</script>
