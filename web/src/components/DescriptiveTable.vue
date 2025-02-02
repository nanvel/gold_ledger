<template>
  <div class="overflow-x-auto">
    <table class="table table-md table-zebra w-auto">
      <tbody>
        <tr v-for="row in props.rows" :key="row[0]">
          <td>{{ row[0] }}</td>
          <td>{{ row[1] }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
const props = defineProps({
  rows: Array,
});
</script>
