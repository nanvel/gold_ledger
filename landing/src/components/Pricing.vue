<script setup>
import { ref } from "vue";

let period = ref("monthly");
</script>

<template>
  <section class="py-8 lg:py-20" id="pricing">
    <div class="container">
      <div class="text-center">
        <h2 class="text-4xl font-semibold">Pricing Plans</h2>
        <p class="mt-2 text-lg">
          Explore flexible pricing that scales with your needs. No hidden fees,
          just transparent options for your success.
        </p>
      </div>
      <div class="mt-6 flex justify-center">
        <div class="tabs-boxed tabs">
          <button
            class="tab lg:px-10"
            :class="{ 'tab-active': period === 'monthly' }"
            @click="() => (period = 'monthly')"
          >
            Monthly
          </button>
          <button
            class="tab indicator lg:px-10"
            :class="{ 'tab-active': period === 'yearly' }"
            @click="() => (period = 'yearly')"
          >
            Yearly
            <span class="badge indicator-item badge-neutral">-25%</span>
          </button>
        </div>
      </div>
      <div class="mt-8 grid gap-8 lg:grid-cols-3">
        <div class="card border border-base-content/10 p-3 shadow-sm">
          <div class="card bg-base-200 p-6 text-base-content">
            <h3 class="text-xl font-semibold">Retailer</h3>
            <p class="mt-2 flex items-baseline">
              <span class="text-5xl font-bold tracking-tight">$0</span>
              <span class="ml-1 text-xl font-semibold">/month</span>
            </p>
            <p class="mt-4">Free for retailers.</p>
          </div>
          <div class="p-6">
            <ul
              class="list-inside list-disc space-y-3 text-base-content"
              role="list"
            >
              <li>
                <span class="ms-3">All available features</span>
              </li>
              <li>
                <span class="ms-3">Unlimited suppliers</span>
              </li>
              <li>
                <span class="ms-3">Support</span>
              </li>
            </ul>
          </div>
          <button class="btn btn-outline btn-primary btn-block mt-auto">
            Start for Free
          </button>
        </div>
        <div
          class="card border border-base-content/10 bg-base-100 p-3 shadow-sm"
        >
          <div class="card bg-base-200 p-6 text-base-content">
            <div class="flex justify-between">
              <h3 class="text-xl font-semibold text-primary">Supplier</h3>
              <!--              <div class="badge badge-outline text-sm font-medium">-->
              <!--                Best Offer-->
              <!--              </div>-->
            </div>

            <p class="mt-4 flex items-baseline">
              <span class="text-5xl font-bold tracking-tight text-primary"
                >₹{{ period == "monthly" ? 2000 : 1500 }}</span
              >
              <span class="ml-1 text-xl font-semibold">/month</span>
            </p>
            <p class="mt-6">Pay after 2 months free trial.</p>
          </div>
          <div class="p-6">
            <ul
              class="list-inside list-disc space-y-3 text-base-content"
              role="list"
            >
              <li>
                <span class="ms-3">All available features</span>
              </li>
              <li>
                <span class="ms-3">Unlimited retailers</span>
              </li>
              <li>
                <span class="ms-3">Support</span>
              </li>
            </ul>
          </div>
          <button class="btn btn-primary btn-block mt-auto">Upgrade</button>
        </div>
      </div>
    </div>
  </section>
</template>
