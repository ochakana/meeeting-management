<template>
  <NuxtLayout name="custom">
    <Form :initialData="agendaData" />
  </NuxtLayout>
</template>

<script setup lang="ts">
import axios from "axios";
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import Form from "~/components/form.vue";

definePageMeta({
  layout: false,
});

const route = useRoute();
const id = route.params.id; // URLからidを取得

const agendaData = ref(null); // APIから取得するデータを格納するためのref
const runtimeConfig = useRuntimeConfig();

// ページが読み込まれたときにデータを取得
onMounted(async () => {
  try {
    const response = await axios.get(
      `${runtimeConfig.public.apiUrl}/api/get-agenda/${id}`
    );
    agendaData.value = response.data;
  } catch (error) {
    console.error("An error occurred:", error);
  }
});
</script>
