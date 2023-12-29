<template>
  <v-card :min-width="500">
    <v-toolbar flat color="blue-grey" dark>
      <v-toolbar-title>カテゴリエディット</v-toolbar-title>
    </v-toolbar>

    <v-card-text>
      <v-text-field
        variant="filled"
        label="Category"
        v-model="newCategory"
      ></v-text-field>

      <v-divider class="my-2"></v-divider>

      <v-item-group
        multiple
        v-model="selectedCategories"
        selected-class="bg-purple selected"
      >
        <div class="text-caption mb-2">登録一覧</div>
        <v-item
          v-for="category in categories"
          :key="category.recordNumber"
          v-slot="{ selectedClass, toggle }"
        >
          <v-chip :class="selectedClass" @click="toggle">
            {{ category.name }}
          </v-chip>
        </v-item>
      </v-item-group>
    </v-card-text>

    <v-divider></v-divider>

    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="success" @click="postCategory"> Post </v-btn>
      <v-btn color="error" @click="deleteSelectedCategories"> Delete </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts" setup>
import axios from "axios";
import { ref } from "vue";

const newCategory = ref("");
const categories = ref([]);
const selectedCategories = ref([]);

const runtimeConfig = useRuntimeConfig();

const fetchCategories = async () => {
  const response = await axios.get(
    `${runtimeConfig.public.apiUrl}/api/get-categories`
  );
  categories.value = response.data.map((name: string, index: number) => ({
    name,
    recordNumber: index,
  }));
};

const postCategory = async () => {
  await axios.post(`${runtimeConfig.public.apiUrl}/api/save-category`, {
    name: newCategory.value,
  });
  fetchCategories();
};

const deleteSelectedCategories = async () => {
  const selectedCategoryNames = selectedCategories.value.map(
    (selectedIndex) => categories.value[selectedIndex].name
  );

  await axios.delete(`${runtimeConfig.public.apiUrl}/api/delete-category`, {
    data: { selectedNames: selectedCategoryNames },
  });
  fetchCategories();
};

fetchCategories();
</script>
