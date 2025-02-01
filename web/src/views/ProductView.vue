<template>
  <Navbar>
    <div class="flex flex-col space-y-4 pt-4" v-if="details">
      <div class="text-lg">
        Product: {{ details.name }}
        <StatusBadge :status="details.status" />
      </div>
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

      <div>
        <table class="w-auto text-lg">
          <tr>
            <td class="pr-2 text-sm">Weight</td>
            <td>
              <div class="badge badge-lg">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                  stroke="currentColor"
                  height="1em"
                  class="mr-1 inline"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M12 3v17.25m0 0c-1.472 0-2.882.265-4.185.75M12 20.25c1.472 0 2.882.265 4.185.75M18.75 4.97A48.416 48.416 0 0 0 12 4.5c-2.291 0-4.545.16-6.75.47m13.5 0c1.01.143 2.01.317 3 .52m-3-.52 2.62 10.726c.122.499-.106 1.028-.589 1.202a5.988 5.988 0 0 1-2.031.352 5.988 5.988 0 0 1-2.031-.352c-.483-.174-.711-.703-.59-1.202L18.75 4.971Zm-16.5.52c.99-.203 1.99-.377 3-.52m0 0 2.62 10.726c.122.499-.106 1.028-.589 1.202a5.989 5.989 0 0 1-2.031.352 5.989 5.989 0 0 1-2.031-.352c-.483-.174-.711-.703-.59-1.202L5.25 4.971Z"
                  />
                </svg>
                {{ details.weight }}g
              </div>
            </td>
          </tr>
          <tr>
            <td class="pr-2 text-sm">Quality</td>
            <td>
              <div class="badge badge-lg">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                  stroke="currentColor"
                  height="1em"
                  class="mr-1 inline"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M11.48 3.499a.562.562 0 0 1 1.04 0l2.125 5.111a.563.563 0 0 0 .475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 0 0-.182.557l1.285 5.385a.562.562 0 0 1-.84.61l-4.725-2.885a.562.562 0 0 0-.586 0L6.982 20.54a.562.562 0 0 1-.84-.61l1.285-5.386a.562.562 0 0 0-.182-.557l-4.204-3.602a.562.562 0 0 1 .321-.988l5.518-.442a.563.563 0 0 0 .475-.345L11.48 3.5Z"
                  />
                </svg>
                {{ details.quality }}%
              </div>
            </td>
          </tr>
          <tr>
            <td class="pr-2 text-sm">Rate</td>
            <td>
              <div class="badge badge-lg">{{ details.rate }}₹/g</div>
            </td>
          </tr>
          <tr>
            <td class="pr-2 text-sm">Payment</td>
            <td>
              <div class="badge badge-lg">
                <template v-if="details.payment_type === 'FINE'">
                  {{ details.payment_type }} {{ details.payment_weight }}g @
                  {{ details.payment_quality }}%
                </template>
                <template v-else>
                  {{ details.payment_type }} {{ details.payment_amount }}₹
                </template>
                by {{ details.payment_due_date }}
              </div>
            </td>
          </tr>
          <tr>
            <td class="pr-2 text-sm">Created by</td>
            <td>
              <div class="badge badge-lg">
                {{ details.creator.email }} ({{ details.creator.name }})
              </div>
            </td>
          </tr>
          <tr>
            <td class="pr-2 text-sm">Created at</td>
            <td>
              <div class="badge badge-lg">
                <timestamp :value="details.created_at" show-duration />
              </div>
            </td>
          </tr>
          <tr v-if="details.confirmed_by">
            <td class="pr-2 text-sm">Confirmed by</td>
            <td>
              <div class="badge badge-lg">
                {{ details.confirmed_by.email }} ({{
                  details.confirmed_by.name
                }})
              </div>
            </td>
          </tr>
          <tr v-if="details.rejected_by">
            <td class="pr-2 text-sm">Rejected by</td>
            <td>
              <div class="badge badge-lg">
                {{ details.rejected_by.email }} ({{ details.rejected_by.name }})
              </div>
            </td>
          </tr>
          <tr v-if="details.canceled_by">
            <td class="pr-2 text-sm">Canceled by</td>
            <td>
              <div class="badge badge-lg">
                {{ details.canceled_by.email }} ({{ details.canceled_by.name }})
              </div>
            </td>
          </tr>
        </table>
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
import StatusBadge from "@/components/StatusBadge.vue";

const meStore = useMeStore();

const { isRetailer } = storeToRefs(meStore);

const productId = ref(parseInt(router.currentRoute.value.params.id));
const details = ref(null);
const loading = ref(true);
const activitiesKey = ref(0);

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
