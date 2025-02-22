<script setup>
import supplierRegisterImage from "@/assets/screens/supplier_register.png";
import supplierInviteImage from "@/assets/screens/supplier_invite.png";
import supplierProduct1Image from "@/assets/screens/supplier_product_1.png";
import supplierProduct2Image from "@/assets/screens/supplier_product_2.png";
import retailerDashboardImage from "@/assets/screens/retailer_dashboard.png";
import retailerConfirmImage from "@/assets/screens/retailer_confirm.png";
import retailerDashboard1Image from "@/assets/screens/retailer_dashboard_1.png";
import retailerPayment1Image from "@/assets/screens/retailer_payment_1.png";
import supplierDashboardImage from "@/assets/screens/supplier_dashboard.png";
import supplierConfirmPaymentImage from "@/assets/screens/supplier_confirm_payment.png";
import balanceSheetImage from "@/assets/screens/balance_sheet.png";
import lightThemeImage from "@/assets/screens/light_theme.png";
import darkThemeImage from "@/assets/screens/dark_theme.png";
import productsListImage from "@/assets/screens/products_list.png";
import paymentsListImage from "@/assets/screens/payments_list.png";
</script>

<template>
  <section class="relative py-8 lg:py-20" id="features">
    <div class="absolute start-[10%] z-0">
      <div
        class="pointer-events-none aspect-square w-60 rounded-full bg-gradient-to-r from-primary/10 via-violet-500/10 to-purple-500/10 blur-3xl [transform:translate3d(0,0,0)] lg:w-[600px]"
      ></div>
    </div>

    <div class="container">
      <div class="flex flex-col items-center">
        <h2 class="inline text-4xl font-semibold">Features</h2>

        <p class="mt-4 text-lg sm:text-center">
          Simplify you business operation with our powerful SaaS product.
        </p>
      </div>

      <div
        class="relative z-[2] mt-8 grid gap-8 lg:mt-20 lg:grid-cols-2 lg:gap-12"
      >
        <div
          class="overflow-hidden rounded-lg bg-base-200 shadow-md transition-all hover:shadow-xl flex flex-row space-x-2"
        >
          <img
            alt="saas img"
            class="overflow-hidden rounded-ss-lg"
            :src="supplierRegisterImage"
          />
          <img
            alt="saas img"
            class="overflow-hidden rounded-ss-lg"
            :src="supplierInviteImage"
          />
        </div>

        <div class="lg:mt-8">
          <div class="badge badge-primary">Sign Up</div>
          <h3 class="mt-2 text-3xl font-semibold">
            Sign Up and onboard retailers
          </h3>
          <p class="mt-2 text-base font-medium">
            Elevate control with our dynamic SaaS dashboard—real-time insights,
            intuitive navigation, seamless customization.
          </p>

          <ul class="mt-4 list-inside list-disc text-base">
            <li>Real-Time Data Insights</li>
            <li>Customizable Widgets</li>
            <li>Intuitive User Interface</li>
            <li>Performance Metrics at a Glance</li>
          </ul>
        </div>
      </div>

      <div class="mt-8 grid gap-8 lg:mt-20 lg:grid-cols-2 lg:gap-12">
        <div>
          <div class="badge badge-primary">Products</div>
          <h3 class="mt-2 text-3xl font-semibold">
            Adding products and acceptance
          </h3>
          <p class="mt-2 text-base">
            Our SaaS platform offers seamless management, allowing you to
            effortlessly oversee users, projects, and resources in one
            centralized hub. Gain real-time insights, streamline workflows, and
            optimize resource allocation for unparalleled efficiency.
          </p>

          <ul class="mt-4 list-inside list-disc text-base">
            <li>User-Friendly Tools</li>
            <li>Resource Management</li>
            <li>Task Assignment</li>
            <li>Robust Control</li>
          </ul>
        </div>

        <div class="order-first lg:order-last">
          <div
            class="overflow-hidden rounded-lg bg-base-200 shadow-md transition-all hover:shadow-xl flex flex-row space-x-2"
          >
            <img
              alt="saas img"
              class="overflow-hidden rounded-ss-lg"
              :src="supplierProduct1Image"
            />
            <img
              alt="saas img"
              class="overflow-hidden rounded-ss-lg"
              :src="supplierProduct2Image"
            />
          </div>
        </div>
      </div>

      <div class="mt-8 grid gap-8 lg:mt-20 lg:grid-cols-2 lg:gap-12">
        <div
          class="overflow-hidden rounded-lg bg-base-200 shadow-md transition-all hover:shadow-xl flex flex-row space-x-2"
        >
          <img
            alt="saas img"
            class="overflow-hidden rounded-ss-lg"
            :src="retailerDashboardImage"
          />
          <img
            alt="saas img"
            class="overflow-hidden rounded-ss-lg"
            :src="retailerConfirmImage"
          />
        </div>

        <div class="lg:mt-8">
          <div class="badge badge-primary">Products</div>
          <h3 class="mt-2 text-3xl font-semibold">Product acceptance</h3>
          <p class="mt-2 text-base">
            Connect key tools seamlessly with our SaaS platform, streamlining
            your processes and boosting productivity. Experience a cohesive
            digital ecosystem that empowers your business for innovation and
            growth.
          </p>

          <ul class="mt-4 list-inside list-disc text-base">
            <li>Real-time chat with Slack</li>
            <li>Engage your customer with Email</li>
            <li>Getting order from Amazon</li>
            <li>Using Ai from OpenAI</li>
          </ul>
        </div>
      </div>

      <div class="mt-8 grid gap-8 lg:mt-20 lg:grid-cols-2 lg:gap-12">
        <div>
          <div class="badge badge-primary">Payments</div>
          <h3 class="mt-2 text-3xl font-semibold">Adding a payment</h3>
          <p class="mt-2 text-base">
            Our SaaS platform offers seamless management, allowing you to
            effortlessly oversee users, projects, and resources in one
            centralized hub. Gain real-time insights, streamline workflows, and
            optimize resource allocation for unparalleled efficiency.
          </p>

          <ul class="mt-4 list-inside list-disc text-base">
            <li>User-Friendly Tools</li>
            <li>Resource Management</li>
            <li>Task Assignment</li>
            <li>Robust Control</li>
          </ul>
        </div>

        <div class="order-first lg:order-last">
          <div
            class="overflow-hidden rounded-lg bg-base-200 shadow-md transition-all hover:shadow-xl flex flex-row space-x-2"
          >
            <img
              alt="saas img"
              class="overflow-hidden rounded-ss-lg"
              :src="retailerDashboard1Image"
            />
            <img
              alt="saas img"
              class="overflow-hidden rounded-ss-lg"
              :src="retailerPayment1Image"
            />
          </div>
        </div>
      </div>

      <div class="mt-8 grid gap-8 lg:mt-20 lg:grid-cols-2 lg:gap-12">
        <div
          class="overflow-hidden rounded-lg bg-base-200 shadow-md transition-all hover:shadow-xl flex flex-row space-x-2"
        >
          <img
            alt="saas img"
            class="overflow-hidden rounded-ss-lg"
            :src="supplierDashboardImage"
          />
          <img
            alt="saas img"
            class="overflow-hidden rounded-ss-lg"
            :src="supplierConfirmPaymentImage"
          />
        </div>

        <div class="lg:mt-8">
          <div class="badge badge-primary">Payments</div>
          <h3 class="mt-2 text-3xl font-semibold">Payment acceptance</h3>
          <p class="mt-2 text-base">
            Connect key tools seamlessly with our SaaS platform, streamlining
            your processes and boosting productivity. Experience a cohesive
            digital ecosystem that empowers your business for innovation and
            growth.
          </p>

          <ul class="mt-4 list-inside list-disc text-base">
            <li>Real-time chat with Slack</li>
            <li>Engage your customer with Email</li>
            <li>Getting order from Amazon</li>
            <li>Using Ai from OpenAI</li>
          </ul>
        </div>
      </div>

      <div class="mt-8 grid gap-8 lg:mt-20 lg:grid-cols-2 lg:gap-12">
        <div>
          <div class="badge badge-primary">Accounting</div>
          <h3 class="mt-2 text-3xl font-semibold">Balance sheet</h3>
          <p class="mt-2 text-base">
            Our SaaS platform offers seamless management, allowing you to
            effortlessly oversee users, projects, and resources in one
            centralized hub. Gain real-time insights, streamline workflows, and
            optimize resource allocation for unparalleled efficiency.
          </p>

          <ul class="mt-4 list-inside list-disc text-base">
            <li>User-Friendly Tools</li>
            <li>Resource Management</li>
            <li>Task Assignment</li>
            <li>Robust Control</li>
          </ul>
        </div>

        <div class="order-first lg:order-last">
          <div
            class="overflow-hidden rounded-lg bg-base-200 shadow-md transition-all hover:shadow-xl flex flex-row space-x-2"
          >
            <img
              alt="saas img"
              class="overflow-hidden rounded-ss-lg"
              :src="retailerDashboard1Image"
            />
            <img
              alt="saas img"
              class="overflow-hidden rounded-ss-lg"
              :src="balanceSheetImage"
            />
          </div>
        </div>
      </div>

      <div class="mt-8 grid gap-8 lg:mt-20 lg:grid-cols-2 lg:gap-12">
        <div
          class="overflow-hidden rounded-lg bg-base-200 shadow-md transition-all hover:shadow-xl flex flex-row space-x-2"
        >
          <img
            alt="saas img"
            class="overflow-hidden rounded-ss-lg"
            :src="productsListImage"
          />
          <img
            alt="saas img"
            class="overflow-hidden rounded-ss-lg"
            :src="paymentsListImage"
          />
        </div>

        <div class="lg:mt-8">
          <div class="badge badge-primary">Data</div>
          <h3 class="mt-2 text-3xl font-semibold">Own your data</h3>
          <p class="mt-2 text-base">
            Connect key tools seamlessly with our SaaS platform, streamlining
            your processes and boosting productivity. Experience a cohesive
            digital ecosystem that empowers your business for innovation and
            growth.
          </p>

          <ul class="mt-4 list-inside list-disc text-base">
            <li>Real-time chat with Slack</li>
            <li>Engage your customer with Email</li>
            <li>Getting order from Amazon</li>
            <li>Using Ai from OpenAI</li>
          </ul>
        </div>
      </div>

      <div class="mt-8 grid gap-8 lg:mt-20 lg:grid-cols-2 lg:gap-12">
        <div>
          <div class="badge badge-primary">UI</div>
          <h3 class="mt-2 text-3xl font-semibold">Light and dark themes</h3>
          <p class="mt-2 text-base">
            Our SaaS platform offers seamless management, allowing you to
            effortlessly oversee users, projects, and resources in one
            centralized hub. Gain real-time insights, streamline workflows, and
            optimize resource allocation for unparalleled efficiency.
          </p>

          <ul class="mt-4 list-inside list-disc text-base">
            <li>User-Friendly Tools</li>
            <li>Resource Management</li>
            <li>Task Assignment</li>
            <li>Robust Control</li>
          </ul>
        </div>

        <div class="order-first lg:order-last">
          <div
            class="overflow-hidden rounded-lg bg-base-200 shadow-md transition-all hover:shadow-xl flex flex-row space-x-2"
          >
            <img
              alt="saas img"
              class="overflow-hidden rounded-ss-lg"
              :src="lightThemeImage"
            />
            <img
              alt="saas img"
              class="overflow-hidden rounded-ss-lg"
              :src="darkThemeImage"
            />
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
