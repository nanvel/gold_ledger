<template>
  <div class="flex flex-col space-y-4">
    <placeholder
      v-if="!activities?.length && !loading"
      text="There were no activities recorded"
    />
    <placeholder v-if="loading" loading text="Loading" />
    <div class="overflow-x-auto" v-if="activities?.length && !loading">
      <table class="table table-zebra">
        <thead>
          <tr>
            <th>Time</th>
            <th>Activity</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="activity in activities" :key="activity.id">
            <td>
              <timestamp :value="activity.created_at" :show-duration="true" />
            </td>
            <td>
              <RouterLink
                :to="
                  activity.product_id
                    ? `/products/${activity.product_id}`
                    : `/payments/${activity.payment_id}`
                "
                ><svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                  stroke="currentColor"
                  height="1em"
                  class="pr-1 inline"
                  v-if="activity.product_id"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M9.568 3H5.25A2.25 2.25 0 0 0 3 5.25v4.318c0 .597.237 1.17.659 1.591l9.581 9.581c.699.699 1.78.872 2.607.33a18.095 18.095 0 0 0 5.223-5.223c.542-.827.369-1.908-.33-2.607L11.16 3.66A2.25 2.25 0 0 0 9.568 3Z"
                  />
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M6 6h.008v.008H6V6Z"
                  />
                </svg>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                  stroke="currentColor"
                  class="pr-1 inline"
                  height="1em"
                  v-if="activity.payment_id"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M2.25 18.75a60.07 60.07 0 0 1 15.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 0 1 3 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 0 0-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 0 1-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 0 0 3 15h-.75M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm3 0h.008v.008H18V10.5Zm-12 0h.008v.008H6V10.5Z"
                  /></svg
                >{{ activity.message }}</RouterLink
              >
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="join mt-8" v-if="!loading && total > 0">
    <button
      class="join-item btn"
      v-if="page > 1"
      v-on:click="loadPage(page - 1)"
    >
      «
    </button>
    <button class="join-item btn">
      Page {{ page }} / {{ pages }} <small>Total: {{ total }}</small>
    </button>
    <button
      class="join-item btn"
      v-if="page < pages"
      v-on:click="loadPage(page + 1)"
    >
      »
    </button>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import { httpClient } from "@/services/http.js";
import Timestamp from "@/components/Timestamp.vue";
import { useMeStore } from "@/stores/index.js";
import { storeToRefs } from "pinia";
import { RouterLink } from "vue-router";
import Placeholder from "@/components/Placeholder.vue";

const props = defineProps({
  retailerId: {
    type: Number,
    required: false,
  },
  supplierId: {
    type: Number,
    required: false,
  },
  productId: {
    type: Number,
    required: false,
  },
  paymentId: {
    type: Number,
    required: false,
  },
});

const meStore = useMeStore();
const { isSupplier, isRetailer } = storeToRefs(meStore);

const activities = ref([]);
const total = ref(0);
const page = ref(1);
const limit = ref(20);
const loading = ref(false);

const pages = computed(() => Math.ceil(total.value / limit.value));

const loadPage = async (p) => {
  page.value = p;
  let q = `?offset=${(page.value - 1) * limit.value}&limit=${limit.value}`;
  if (props.retailerId) {
    q += `&retailer_id=${props.retailerId}`;
  }
  if (props.supplierId) {
    q += `&supplier_id=${props.supplierId}`;
  }
  if (props.productId) {
    q += `&product_id=${props.productId}`;
  }
  if (props.paymentId) {
    q += `&payment_id=${props.paymentId}`;
  }
  loading.value = true;
  try {
    const resp = await httpClient.get(`/api/activities${q}`, null, null);
    activities.value = resp["items"];
    total.value = resp["total"];
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  await loadPage(1);
});
</script>
