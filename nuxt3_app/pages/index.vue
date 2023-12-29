<template>
  <NuxtLayout name="custom">
    <Grid />
  </NuxtLayout>
</template>

<script setup lang="ts">
import Grid from "~/layouts/grid.vue";

definePageMeta({
  layout: false,
});
</script>
