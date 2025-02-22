<script setup>
import { onMounted, ref } from "vue";

const atTop = ref(false);

onMounted(() => {
  const onWindowScroll = () => {
    atTop.value = window.pageYOffset < 30;
  };

  window.addEventListener("scroll", onWindowScroll);

  onWindowScroll();
});
</script>

<template>
  <!--  <div class="bg-neutral py-1.5 text-center text-xs text-neutral-content md:text-sm">-->
  <!--    <span>-->
  <!--      Revamp Your Control: Code-->
  <!--      <span class="font-semibold text-warning">DAISYUI</span>-->
  <!--      for a 20% SaaS discount 🚀-->
  <!--    </span>-->
  <!--  </div>-->

  <div
    id="navbar-wrapper"
    class="sticky top-0 z-10 border-b bg-base-100 lg:bg-opacity-95 lg:backdrop-blur-sm"
    :class="atTop ? 'border-transparent' : 'border-base-content/10'"
  >
    <div class="container">
      <nav class="navbar px-0">
        <div class="navbar-start gap-2">
          <div class="flex-none lg:hidden">
            <label
              for="my-drawer"
              aria-label="open sidebar"
              class="btn btn-square btn-ghost"
            >
              <i class="inline-block text-xl">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                  stroke="currentColor"
                  height="1em"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
                  />
                </svg>
              </i>
            </label>
          </div>

          <!-- Navbar Brand logo -->
          <a href="#" class="text-xl font-bold tracking-tighter"
            ><span class="text-amber-500">Gold</span> Ledger</a
          >
        </div>

        <div class="navbar-center hidden lg:flex">
          <ul class="menu menu-horizontal menu-sm gap-2 px-1">
            <li class="font-medium"><a href="#home">Home</a></li>
            <li class="font-medium"><a href="#features">Features</a></li>
            <li class="font-medium"><a href="#pricing">Pricing</a></li>
            <li class="font-medium"><a href="#faq">FAQ</a></li>
          </ul>
        </div>

        <div class="navbar-end gap-3">
          <a
            class="btn btn-ghost btn-sm"
            href="https://app.goldledger.in/register"
            >Register</a
          >
          <a
            class="btn btn-primary btn-sm"
            href="https://app.goldledger.in/login"
            >Login</a
          >
        </div>
      </nav>

      <!-- sm screen menu (drawer) -->
      <div class="drawer">
        <input id="my-drawer" type="checkbox" class="drawer-toggle" />
        <div class="drawer-side">
          <label
            for="my-drawer"
            aria-label="close sidebar"
            class="drawer-overlay"
          ></label>

          <ul
            class="menu min-h-full w-80 gap-2 bg-base-100 p-4 text-base-content"
          >
            <!-- Navbar Brand logo -->
            <li class="font-medium">
              <a href="index.html" class="text-xl font-bold"
                ><span class="text-amber-500">Gold</span> Ledger</a
              >
            </li>

            <li class="font-medium"><a href="#home">Home</a></li>
            <li class="font-medium"><a href="#features">Features</a></li>
            <li class="font-medium"><a href="#pricing">Pricing</a></li>
            <li class="font-medium"><a href="#faq">FAQ</a></li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>
