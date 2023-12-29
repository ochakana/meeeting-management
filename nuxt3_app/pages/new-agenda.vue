<template>
  <NuxtLayout name="custom">
    <Form />
  </NuxtLayout>
</template>

<script setup lang="ts">
import Form from "~/components/form.vue";

definePageMeta({
  layout: false,
});
</script>
