/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [require("@tailwindcss/typography"), require("daisyui")],
  daisyui: {
    themes: ["light", "dark", "cupcake"],
  },
  safelist: [
    "badge-success",
    "badge-info",
    "badge-warning",
    "badge-error",
    "badge-lg",
    "badge-md",
    "table-sm",
    "table-md",
  ],
};
