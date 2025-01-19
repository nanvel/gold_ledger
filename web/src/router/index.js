import { useAuthStore } from "@/stores/auth";
import { createRouter, createWebHistory } from "vue-router";
import AccountView from "@/views/AccountView.vue";
import HomeView from "@/views/HomeView.vue";
import LoginView from "@/views/LoginView.vue";
import RegisterView from "@/views/RegisterView.vue";
import RetailerView from "@/views/RetailerView.vue";
import RetailersView from "@/views/RetailersView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
    },
    {
      path: "/register",
      name: "register",
      component: RegisterView,
    },
    {
      path: "/account",
      name: "account",
      component: AccountView,
    },
    {
      path: "/retailers",
      name: "retailers",
      component: RetailersView,
    },
    {
      path: "/retailers/:id",
      name: "retailer",
      component: RetailerView,
    },
  ],
});

router.beforeEach(async (to) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const loginPath = "/login";
  const registerPath = "/register";
  const publicPages = [loginPath, registerPath];
  const authRequired = !publicPages.includes(to.path);
  const { loggedIn, setReturnUrl } = useAuthStore();

  if (loggedIn && (to.path === loginPath || to.path === registerPath)) {
    return "/";
  }

  if (authRequired && !loggedIn) {
    setReturnUrl(to.fullPath);
    return loginPath;
  }
});

export default router;
