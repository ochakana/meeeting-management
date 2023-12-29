<template>
  <v-hover>
    <template v-slot:default="{ isHovering, props }">
      <v-card
        class="mx-auto"
        :class="{ 'hovered-card': isHovering }"
        variant="tonal"
        v-bind="props"
      >
        <v-card-item>
          <div>
            <div class="sub-title">
              <div class="text-overline">{{ data.date }}</div>
              <div class="text-overline text-right">
                <v-chip class="" color="cyan" size="x-small" label>
                  <v-icon
                    start
                    :icon="getIconByCategory(data.category)"
                  ></v-icon>
                  {{ data.category }}
                </v-chip>
              </div>
            </div>

            <div class="text-h6">
              <div class="sub-title">
                <div class="text-overflow text-left">
                  {{ data.agendaTitle }}
                </div>
                <div class="text-overflow text-overline text-right">
                  {{ data.proposerName }}
                </div>
              </div>
            </div>
            <v-divider class="mb-2"></v-divider>
            <div class="text-caption text-overflow">{{ data.content }}</div>
          </div>
        </v-card-item>
        <v-card-actions>
          <nuxt-link :to="`/view-agenda/${data.recordNumber}`">
            <v-btn variant="tonal"> View </v-btn>
          </nuxt-link>
        </v-card-actions>
      </v-card>
    </template>
  </v-hover>
</template>

<script setup lang="ts">
import { cardType } from "types/types";

// プロパティからデータを受け取る
const props = defineProps<{
  data: cardType;
}>();

// カテゴリに応じてアイコンを返す関数
const getIconByCategory = (category: string) => {
  switch (category) {
    case "agenda":
      return "mdi-view-agenda-outline";
    case "meeting":
      return "mdi-gift-outline";
    case "document":
      return "mdi-file-document-outline";
    case "category":
      return "mdi-icon-name2";
    default:
      return "mdi-emoticon-cool-outline";
  }
};
</script>

<style scoped lang="scss">
.v-card {
  // max-width: 350px !important;
  background-color: #292b2f !important;
  color: aqua;
}

.v-card-actions {
  a {
    color: aqua;
  }
}
.sub-title {
  display: grid;
  grid-template-columns: 70% 30%;
  align-items: center;
}
.text-overflow {
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
}
.v-card-actions {
  justify-content: right;
}

.v-chip {
  width: fit-content;
}

.v-card.hovered-card {
  background-color: #2b2d47 !important;
}
</style>
