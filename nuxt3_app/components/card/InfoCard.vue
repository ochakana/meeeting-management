<template>
  <v-card class="mx-auto" :min-width="200">
    <v-toolbar color="#363d4d" :height="50" :title="'お知らせ'"></v-toolbar>
    <v-card-text>
      <div class="">{{ message }}</div>
    </v-card-text>
    <v-card-actions class="justify-end">
      <v-btn variant="text" @click="closeDialog">Close</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts" setup>
const props = defineProps<{
  message?: string;
}>();

const emit = defineEmits<{
  (e: "closeDialog"): void;
}>();

const closeDialog = () => {
  emit("closeDialog");
};
</script>
