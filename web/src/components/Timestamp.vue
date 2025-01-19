<template>
  {{ timeString }}{{ endTimeString }}
  <span v-if="timeString.length">({{ durationString }})</span
  ><span v-else>{{ durationString }}</span>
</template>

<script setup>
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

const date = new Date(props.value * 1000);

const toString = (d) => {
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, "0"); // Months are zero-based
  const dd = String(d.getDate()).padStart(2, "0");
  const HH = String(d.getHours()).padStart(2, "0");
  const MM = String(d.getMinutes()).padStart(2, "0");

  return `${yyyy}-${mm}-${dd} ${HH}:${MM}`;
};

const timeString = toString(date);
const endTimeString =
  props.showEndTime && props.endValue
    ? " - " + toString(new Date(props.endValue * 1000))
    : "";

let durationString = "";
if (props.showDuration) {
  const endDate = props.endValue ? new Date(props.endValue * 1000) : new Date();

  const diffMs = endDate - date;
  const diffMins = Math.floor(diffMs / 1000 / 60);
  let diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);
  diffHours -= diffDays * 24;
  const remainingMins = diffMins % 60;

  if (diffDays > 0) {
    durationString += diffDays + "d ";
  }
  if (diffHours > 0) {
    durationString += diffHours + "h ";
  }
  if (remainingMins > 0 && diffDays === 0) {
    durationString += remainingMins + "m ";
  }

  durationString = durationString.trim();

  if (!durationString.length) {
    durationString = Math.floor(diffMs / 1000) + "s";
  }
}
</script>
