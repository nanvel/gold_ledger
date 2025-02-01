<template>
  <Navbar>
    <div class="flex flex-col space-y-4 pt-4" v-if="details">
      <div class="text-lg">Product: {{ details.name }}</div>
      <div>
        <div class="badge badge-neutral">
          {{ details.supplier.id }} : {{ details.supplier.name }}
        </div>
        delivered to
        <div class="badge badge-neutral">
          {{ details.retailer.id }} : {{ details.retailer.name }}
        </div>
        on
        {{ details.date }}
      </div>
      <div class="flex flex-row items-center space-x-4">
        <div>
          Status:
          <div class="badge badge-warning" v-if="status === 'Pending'">
            {{ status }}
          </div>
          <div class="badge badge-neutral" v-if="status === 'Cancelled'">
            {{ status }}
          </div>
          <div class="badge badge-error" v-if="status === 'Rejected'">
            {{ status }}
          </div>
          <div class="badge badge-success" v-if="status === 'Confirmed'">
            {{ status }}
          </div>
        </div>
        <div
          v-if="
            details &&
            !(
              details.confirmed_by ||
              details.rejected_by ||
              details.cancelled_by
            )
          "
          class="flex flex-row space-x-2"
        >
          <confirm-product-modal
            :product="details"
            v-if="isRetailer"
            v-on:done="onAction"
          />
          <reject-product-modal
            :product="details"
            v-if="isRetailer"
            v-on:done="onAction"
          />
          <cancel-product-modal
            :product="details"
            v-if="!isRetailer"
            v-on:done="onAction"
          />
        </div>
      </div>

      <div v-if="details.images?.length">
        <img
          :alt="details.name"
          :src="details.images[0].thumb_url"
          class="rounded-md"
        />
        <a :href="details.images[0].url" target="_blank" class="text-sm link"
          >Original image</a
        >
      </div>

      <div class="flex flex-col space-y-2">
        <div class="text-md font-bold">Details</div>
        <div>
          Weight
          <div class="badge">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              height="1em"
              class="mr-1"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M12 3v17.25m0 0c-1.472 0-2.882.265-4.185.75M12 20.25c1.472 0 2.882.265 4.185.75M18.75 4.97A48.416 48.416 0 0 0 12 4.5c-2.291 0-4.545.16-6.75.47m13.5 0c1.01.143 2.01.317 3 .52m-3-.52 2.62 10.726c.122.499-.106 1.028-.589 1.202a5.988 5.988 0 0 1-2.031.352 5.988 5.988 0 0 1-2.031-.352c-.483-.174-.711-.703-.59-1.202L18.75 4.971Zm-16.5.52c.99-.203 1.99-.377 3-.52m0 0 2.62 10.726c.122.499-.106 1.028-.589 1.202a5.989 5.989 0 0 1-2.031.352 5.989 5.989 0 0 1-2.031-.352c-.483-.174-.711-.703-.59-1.202L5.25 4.971Z"
              />
            </svg>
            {{ details.weight }}g
          </div>
        </div>
        <div>
          Quality
          <div class="badge">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              height="1em"
              class="mr-1"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M11.48 3.499a.562.562 0 0 1 1.04 0l2.125 5.111a.563.563 0 0 0 .475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 0 0-.182.557l1.285 5.385a.562.562 0 0 1-.84.61l-4.725-2.885a.562.562 0 0 0-.586 0L6.982 20.54a.562.562 0 0 1-.84-.61l1.285-5.386a.562.562 0 0 0-.182-.557l-4.204-3.602a.562.562 0 0 1 .321-.988l5.518-.442a.563.563 0 0 0 .475-.345L11.48 3.5Z"
              />
            </svg>
            {{ details.quality }}%
          </div>
        </div>
        <div>
          Rate
          <div class="badge">{{ details.rate }}₹/g</div>
        </div>

        <div>
          Created by
          <div class="badge" v-if="details.creator.name?.length">
            {{ details.creator.email }} ({{ details.creator.name }})
          </div>
          <div class="badge" v-else>{{ details.creator.email }}</div>
        </div>

        <div>
          Created at <timestamp :value="details.created_at" show-duration />
        </div>

        <div v-if="details.confirmed_by">
          Confirmed by
          <div class="badge" v-if="details.confirmed_by.name?.length">
            {{ details.confirmed_by.email }} ({{ details.confirmed_by.name }})
          </div>
          <div class="badge" v-else>{{ details.confirmed_by.email }}</div>
        </div>

        <div v-if="details.rejected_by">
          Rejected by
          <div class="badge" v-if="details.rejected_by.name?.length">
            {{ details.rejected_by.email }} ({{ details.rejected_by.name }})
          </div>
          <div class="badge" v-else>{{ details.rejected_by.email }}</div>
        </div>

        <div v-if="details.cancelled_by">
          Cancelled by
          <div class="badge" v-if="details.cancelled_by.name?.length">
            {{ details.cancelled_by.email }} ({{ details.cancelled_by.name }})
          </div>
          <div class="badge" v-else>{{ details.cancelled_by.email }}</div>
        </div>

        <div>
          Payment
          <div class="badge" v-if="details.payment_type === 'FINE'">
            {{ details.payment_type }} {{ details.payment_weight }}g @
            {{ details.payment_quality }}%
          </div>
          <div class="badge" v-else>
            {{ details.payment_type }} {{ details.payment_amount }}₹
          </div>
          by {{ details.payment_due_date }}
        </div>
      </div>

      <activities-table :product-id="details.id" :key="activitiesKey" />
    </div>
  </Navbar>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { httpClient } from "@/services/http.js";
import router from "@/router/index.js";
import Navbar from "@/components/Navbar.vue";
import { useMeStore } from "@/stores/index.js";
import { storeToRefs } from "pinia";
import Timestamp from "@/components/Timestamp.vue";
import ActivitiesTable from "@/components/ActivitiesTable.vue";
import ConfirmProductModal from "@/components/ConfirmProductModal.vue";
import RejectProductModal from "@/components/RejectProductModal.vue";
import CancelProductModal from "@/components/CancelProductModal.vue";

const meStore = useMeStore();

const { isRetailer } = storeToRefs(meStore);

const productId = ref(parseInt(router.currentRoute.value.params.id));
const details = ref(null);
const loading = ref(true);
const activitiesKey = ref(0);

const status = computed(() => {
  if (details.value.confirmed_by) {
    return "Confirmed";
  }
  if (details.value.rejected_by) {
    return "Rejected";
  }
  if (details.value.cancelled_by) {
    return "Cancelled";
  }
  return "Pending";
});

const onAction = async () => {
  await loadProduct();
  activitiesKey.value += 1;
};

const loadProduct = async () => {
  loading.value = true;
  try {
    details.value = await httpClient.get(`/api/products/${productId.value}`);
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  await loadProduct();
});
</script>
