<template>
  <v-container>
    <v-sheet class="sheet-grid">
      <v-sheet class="ma-2 text-right">
        <v-btn icon class="me-2" @click="toggleDialog">
          <v-icon>mdi-magnify</v-icon>
        </v-btn>
        <v-btn icon class="me-2" @click="toggleSort">
          <v-icon>mdi-sort</v-icon>
        </v-btn>
      </v-sheet>
      <v-sheet class="ma-2 text-right">
        <nuxt-link to="/new-agenda">
          <v-btn icon class="me-2">
            <v-icon> mdi-pencil </v-icon>
          </v-btn>
        </nuxt-link>
      </v-sheet>
    </v-sheet>

    <v-row
      no-gutters
      v-for="(chunk, chunkIndex) in chunkedCards"
      :key="'row-' + chunkIndex"
    >
      <v-col v-for="(card, index) in chunk" :key="(card as any).recordNumber">
        <v-sheet class="ma-2">
          <AgendaCard :data="card" />
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
  <Dialog
    v-model="showDialog"
    :isSearchButtonPressed="isSearchButtonPressed"
  ></Dialog>
</template>

<script setup lang="ts">
import axios from "axios";
import { computed, onMounted, ref } from "vue";
import AgendaCard from "~/components/card/AgendaCard.vue";
import Dialog from "~/components/dialog.vue";

const cards = ref([]);
const isSorted = ref(false);
const showDialog = ref(false);
const isSearchButtonPressed = ref(false);

const toggleDialog = () => {
  isSearchButtonPressed.value = true; // 検索ボタンが押された
  showDialog.value = !showDialog.value;
};

const runtimeConfig = useRuntimeConfig();

onMounted(async () => {
  try {
    const response = await axios.get(
      `${runtimeConfig.public.apiUrl}/api/get-agendas`
    );
    cards.value = response.data.agendas;
  } catch (error) {
    console.error("An error occurred while fetching data:", error);
  }
});

const toggleSort = () => {
  isSorted.value = !isSorted.value;
};

const sortedCards = computed(() => {
  if (isSorted.value) {
    return [...cards.value].sort(
      (a: any, b: any) =>
        new Date(b.date).getTime() - new Date(a.date).getTime()
    );
  }
  return cards.value;
});

const chunkedCards = computed(() => {
  const chunkSize = 3;
  return Array.from(
    { length: Math.ceil(sortedCards.value.length / chunkSize) },
    (_, i) => sortedCards.value.slice(i * chunkSize, i * chunkSize + chunkSize)
  );
});
</script>

<style scoped lang="scss">
.sheet-grid {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
:deep(.v-row) {
  display: grid !important;
  grid-template-columns: repeat(3, 1fr) !important;
}
.v-sheet {
  background: none !important;
}
.new-agenda-btn-conteiner {
  display: flex;
  justify-content: flex-end;
}
.v-btn {
  color: aqua;
  background-color: #292b2f !important;
}
</style>
