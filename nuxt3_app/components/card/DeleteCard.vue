<template>
  <v-card>
    <v-card-text>
      <div>本当に削除しますか？</div>
    </v-card-text>
    <v-card-actions class="justify-end">
      <v-btn variant="text" @click="cardDelete">Yes</v-btn>
      <v-btn variant="text" @click="cancelDelete">No</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts" setup>
const emit = defineEmits<{
  (e: "cardDelete"): void;
  (e: "cancelDelete"): void;
}>();

const cardDelete = () => {
  emit("cardDelete");
};

const cancelDelete = () => {
  emit("cancelDelete");
};
</script>
