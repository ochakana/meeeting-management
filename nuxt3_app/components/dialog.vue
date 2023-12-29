<template>
  <v-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    @click:outside="closeDialog"
    transition="dialog-top-transition"
    width="auto"
  >
    <template v-slot:default="{ isActive }">
      <SearchCard v-if="isSearchButtonPressed" />
      <DeleteCard
        v-else-if="isDeleteButtonPressed"
        @cardDelete="cardDelete"
        @cancelDelete="cancelDelete"
      />
      <CategorySetting v-else-if="isCategorySettingButtonPressed" />
      <InfoCard v-else :message="message" @closeDialog="closeDialog" />
    </template>
  </v-dialog>
</template>

<script lang="ts" setup>
import DeleteCard from "~/components/card/DeleteCard.vue";
import InfoCard from "~/components/card/InfoCard.vue";
import SearchCard from "~/components/card/SearchCard.vue";
import CategorySetting from "~/components/card/CategorySettingCard.vue";

const props = defineProps<{
  modelValue?: boolean;
  message?: string;
  isSearchButtonPressed?: boolean;
  isDeleteButtonPressed?: boolean;
  isCategorySettingButtonPressed?: boolean;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: boolean): void;
  (e: "cardDelete"): void;
}>();

const closeDialog = () => {
  emit("update:modelValue", false);
};

const cardDelete = () => {
  emit("cardDelete");
  closeDialog();
};

const cancelDelete = () => {
  closeDialog();
};
</script>

<style lang="scss" scoped>
:deep(.v-toolbar-title) {
  color: aqua;
}
</style>
