<template>
  <div class="form-control w-full">
    <div class="label">
      <span class="label-text">{{ props.label }}</span>
      <span class="label-text text-error" v-if="error">{{ error }}</span>
    </div>
    <input
      type="password"
      required
      class="input input-bordered w-full input-md text-lg"
      :autofocus="props.autofocus"
      :autocomplete="props.autocomplete"
      :value="modelValue"
      @input="emit('update:modelValue', $event.target.value)"
    />
  </div>
</template>

<script setup>
const props = defineProps({
  label: String,
  error: {
    type: [String, null],
    required: false,
  },
  autofocus: {
    type: Boolean,
    default: false,
  },
  autocomplete: {
    type: String,
    default: "off",
  },
  modelValue: String,
});

const emit = defineEmits(["update:modelValue"]);
</script>
