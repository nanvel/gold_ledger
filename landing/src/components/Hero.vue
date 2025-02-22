<script setup>
import heroImage from "@/assets/landing/saas-hero.png";
</script>

<template>
  <section class="py-8 lg:py-20" id="home">
    <div class="container">
      <div class="grid gap-12 lg:grid-cols-2">
        <div>
          <h1
            class="text-4xl font-black tracking-tighter lg:text-6xl lg:leading-none"
          >
            Streamline transactions and
            <span class="text-primary">financial tracking</span> for businesses
            in the <span class="text-amber-500">gold</span> trade.
          </h1>
          <p class="mt-8 text-lg">
            Includes tracking of product and payment statuses, and balance
            sheets that provide real-time insights into outstanding payments,
            due dates, and overall financial status.
          </p>
          <div class="mt-16 inline-flex gap-3">
            <a class="btn btn-primary" href="https://app.goldledger.in/register"
              >Get Started</a
            >
            <a class="btn btn-ghost" href="#features">Learn More</a>
          </div>
        </div>

        <div>
          <div
            class="rounded-2xl bg-gradient-to-r from-amber-700 via-amber-500 to-amber-300 p-2"
          >
            <img alt="SaaS" class="rounded-lg" :src="heroImage" />
          </div>
        </div>
      </div>

      <!--      <h2-->
      <!--        class="mt-12 text-center text-2xl font-semibold text-base-content/60 lg:mt-32"-->
      <!--      >-->
      <!--        Our Partners-->
      <!--      </h2>-->

      <!--      <div-->
      <!--        class="mt-12 grid grid-cols-2 justify-center gap-8 sm:grid-cols-3 md:grid-cols-5"-->
      <!--      >-->
      <!--        <img-->
      <!--          class="mx-auto h-8 cursor-pointer grayscale transition-all duration-500 hover:grayscale-0"-->
      <!--          :src="googleImage"-->
      <!--          alt="google logo"-->
      <!--        />-->
      <!--        <img-->
      <!--          class="mx-auto h-6 cursor-pointer grayscale transition-all duration-500 hover:grayscale-0"-->
      <!--          :src="microsoftImage"-->
      <!--          alt="microsoft logo"-->
      <!--        />-->
      <!--        <img-->
      <!--          class="mx-auto hidden h-6 cursor-pointer grayscale transition-all duration-500 hover:grayscale-0 md:inline"-->
      <!--          :src="netflixImage"-->
      <!--          alt="netflix logo"-->
      <!--        />-->
      <!--        <img-->
      <!--          class="mx-auto hidden h-8 cursor-pointer grayscale transition-all duration-500 hover:grayscale-0 md:inline"-->
      <!--          :src="spotifyImage"-->
      <!--          alt="spotify logo"-->
      <!--        />-->
      <!--        <img-->
      <!--          class="mx-auto hidden h-8 cursor-pointer grayscale transition-all duration-500 hover:grayscale-0 sm:inline"-->
      <!--          :src="paypalImage"-->
      <!--          alt="paypal logo"-->
      <!--        />-->
      <!--      </div>-->
    </div>
  </section>
</template>
