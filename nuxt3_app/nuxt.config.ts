// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  typescript: {
    shim: false,
  },
  ssr: true,
  css: [
    "assets/styles/main.scss",
    "vuetify/styles",
    "@mdi/font/css/materialdesignicons.css",
  ],
  app: {
    head: {
      title: "meeeting manager",
      meta: [{ name: "description", content: "Nuxt 3 for beginners" }],
      link: [{ rel: "icon", href: "/icon.png" }],
    },
  },
  build: {
    transpile: ["vuetify"],
  },
  runtimeConfig: {
    public: {
      apiUrl: process.env.API_URL || "http://localhost:5010",
    },
  },
  vite: {
    define: {
      "process.env.DEBUG": false,
    },
    server: {
      watch: {
        usePolling: true,
        interval: 500,
      },
    },
  },
});
