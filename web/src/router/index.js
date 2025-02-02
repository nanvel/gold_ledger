import { useAuthStore } from "@/stores/auth";
import { createRouter, createWebHistory } from "vue-router";
import DueView from "@/views/DueView.vue";
import HomeView from "@/views/HomeView.vue";
import LoginView from "@/views/LoginView.vue";
import PaymentsView from "@/views/PaymentsView.vue";
import PaymentView from "@/views/PaymentView.vue";
import ProductsView from "@/views/ProductsView.vue";
import ProductView from "@/views/ProductView.vue";
import RegisterView from "@/views/RegisterView.vue";
import SettingsView from "@/views/SettingsView.vue";

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
      path: "/settings",
      name: "settings",
      component: SettingsView,
    },
    {
      path: "/products",
      name: "products",
      component: ProductsView,
    },
    {
      path: "/products/:id",
      name: "product",
      component: ProductView,
    },
    {
      path: "/payments",
      name: "payments",
      component: PaymentsView,
    },
    {
      path: "/payments/:id",
      name: "payment",
      component: PaymentView,
    },
    {
      path: "/due",
      name: "due",
      component: DueView,
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
