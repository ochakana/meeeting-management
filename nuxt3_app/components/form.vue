<template>
  <v-sheet class="form-wrapper mt-5">
    <v-form ref="form" validate-on="submit lazy" @submit.prevent="submitForm">
      <v-container class="pa-0">
        <v-row no-gutters>
          <v-col class="mr-3">
            <v-select
              v-model="selectedCategory"
              :items="categories"
              :rules="selectedCategoryRules"
              item-text="name"
              item-value="recordNumber"
              variant="solo-filled"
              label="カテゴリ"
              @update:focused="fetchCategories"
            ></v-select>
          </v-col>
          <v-col cols="1">
            <v-btn @click="openCategorySetting">カテゴリ設定</v-btn>
          </v-col>
        </v-row>
      </v-container>

      <v-text-field
        v-model="proposerName"
        :rules="proposerNameRules"
        variant="solo-filled"
        label="登録者"
      ></v-text-field>

      <v-text-field
        v-model="agendaTitle"
        :rules="agendaTitleRules"
        variant="solo-filled"
        label="タイトル"
      ></v-text-field>

      <v-textarea
        v-model="content"
        variant="solo-filled"
        label="内容"
      ></v-textarea>

      <v-file-input
        v-if="isNewAgendaPage"
        label="添付ファイル"
        variant="solo-filled"
        @change="handleFileUpload"
      ></v-file-input>
      <div v-else class="file-download-container">
        <v-file-input
          label="添付ファイル"
          variant="solo-filled"
          @change="handleFileUpload"
          v-if="!isNewAgendaPage"
        ></v-file-input>
        <v-text-field
          v-model="selectedFileName"
          variant="solo-filled"
          :disabled="!isNewAgendaPage"
          label="添付ファイル"
        ></v-text-field>
        <v-btn @click="downloadFile" v-if="!isNewAgendaPage"
          >Download File</v-btn
        >
      </div>

      <div v-if="!isNewAgendaPage" class="btn-wrap pb-5">
        <v-textarea
          v-model="remarksOrQuestions"
          variant="solo-filled"
          label="備考/質問"
        ></v-textarea>
      </div>

      <div class="btn-wrap pb-5">
        <v-btn @click="handleReset" variant="tonal"> clear </v-btn>
        <v-btn
          :loading="loading"
          type="submit"
          variant="tonal"
          text="Submit"
        ></v-btn>
        <v-btn
          v-if="!isNewAgendaPage"
          color="red"
          @click="handleDelete"
          variant="tonal"
        >
          delete
        </v-btn>
      </div>
    </v-form>
  </v-sheet>
  <Dialog
    v-model="showDialog"
    :message="dialogMessage"
    :isSearchButtonPressed="false"
    :isDeleteButtonPressed="isDeleteButtonPressed"
    :isCategorySettingButtonPressed="isCategorySettingButtonPressed"
    @cardDelete="cardDelete"
    @cancelDelete="cancelDelete"
  ></Dialog>
</template>

<script lang="ts" setup>
import axios from "axios";
import { ref, toRaw, unref, watch } from "vue";
import { useRoute } from "vue-router";
import Dialog from "~/components/dialog.vue";

// Vue Router and Route
const router = useRouter();
const route = useRoute();

// Dialog
const showDialog = ref(false);
const dialogMessage = ref("");
const isDeleteButtonPressed = ref(false);
const isCategorySettingButtonPressed = ref(false);

// Form and Validation
const form = ref(null);
const isNewAgendaPage: Ref<boolean> = ref(route.path === "/new-agenda");
const selectedCategory: Ref<string> = ref("");
const proposerName: Ref<string> = ref("");
const agendaTitle: Ref<string> = ref("");
const content: Ref<string> = ref("");
const remarksOrQuestions: Ref<string> = ref("");
const selectedFile = ref(null);
const newSelectedFile = ref(null);
const selectedFileName: Ref<string> = ref("");
const loading = ref(false);
const isSubmitSuccessful = ref(false);
const newSelectedFileName: Ref<string> = ref("");

// Validation Rules
const notEmptyRule = (value: string) => !!value || "必須項目";
const selectedCategoryRules = ref([notEmptyRule]);
const proposerNameRules = ref([notEmptyRule]);
const agendaTitleRules = ref([notEmptyRule]);

// Items for v-select
const categories = ref([]);

if (route.path === "/new-agenda") {
  isNewAgendaPage.value = true;
} else {
  isNewAgendaPage.value = false;
}

const props = defineProps<{
  initialData?: any;
}>();

// 初期データがあればセットする
const setInitialData = () => {
  const initialData = toRaw(props.initialData) || unref(props.initialData);
  if (initialData && initialData.agenda) {
    selectedCategory.value = initialData.agenda.category;
    proposerName.value = initialData.agenda.proposerName;
    agendaTitle.value = initialData.agenda.agendaTitle;
    content.value = initialData.agenda.content;
    selectedFileName.value = initialData.agenda.file;
    if (initialData.agenda.remarksOrQuestions) {
      remarksOrQuestions.value = initialData.agenda.remarksOrQuestions;
    }
  }
};
const runtimeConfig = useRuntimeConfig();

// Methods
// コンポーネントがマウントされたらカテゴリデータを取得
onMounted(() => {
  fetchCategories();
});

const openCategorySetting = () => {
  // ここでダイアログを開く処理
  showDialog.value = true;
  isCategorySettingButtonPressed.value = true; // このフラグをtrueに設定
};

const fetchCategories = async () => {
  const response = await axios.get(
    `${runtimeConfig.public.apiUrl}/api/get-categories`
  );
  categories.value = response.data;
};

const handleFileUpload = (event: any) => {
  const file = event.target.files[0];
  const fileName = file?.name || "";

  const targetFile = isNewAgendaPage.value ? selectedFile : newSelectedFile;
  const targetFileName = isNewAgendaPage.value
    ? selectedFileName
    : newSelectedFileName;

  targetFile.value = file;
  targetFileName.value = fileName;
};

// フォームをリセットする
const handleReset = () => {
  if (form.value) {
    (form.value as any).reset();
  }
};

// ドキュメントを削除する処理
const handleDelete = () => {
  isDeleteButtonPressed.value = true;
  showDialog.value = true;
};

const downloadFile = () => {
  if (selectedFileName.value) {
    window.open(
      `${runtimeConfig.public.apiUrl}/api/download/${selectedFileName.value}`,
      "_blank"
    );
  }
};

const cardDelete = async () => {
  const record_id = route.params.id; // record_idを取得
  const apiUrl = `${runtimeConfig.public.apiUrl}/api/delete/${record_id}`; // APIエンドポイント

  try {
    const response = await axios.delete(apiUrl); // DELETEリクエストを送信

    if (response.status === 200) {
      dialogMessage.value = "ドキュメントが削除されました。";
      showDialog.value = false;
      router.push("/");
    }
  } catch (error) {
    console.error("ドキュメントの削除に失敗しました:", error);
  }

  return {
    showDialog,
    dialogMessage,
    handleDelete,
  };
};

const cancelDelete = () => {
  isDeleteButtonPressed.value = false;
};

const submitForm = async () => {
  if (form.value) {
    const validationResult = await (form.value as any).validate();
    if (validationResult?.valid) {
      loading.value = true;

      const formData = new FormData();
      const apiUrl = isNewAgendaPage.value
        ? `${runtimeConfig.public.apiUrl}/api/save`
        : `${runtimeConfig.public.apiUrl}/api/update`;

      formData.append("category", selectedCategory.value);
      formData.append("proposerName", proposerName.value);
      formData.append("agendaTitle", agendaTitle.value);
      formData.append("content", content.value);
      formData.append("remarksOrQuestions", remarksOrQuestions.value);

      const record_id = route.params.id;
      if (record_id) {
        formData.append("record_id", record_id as string);
      }

      if (selectedFile.value) {
        formData.append("file", selectedFile.value);
      }

      if (newSelectedFile.value) {
        formData.append("newFile", newSelectedFile.value);
      }

      try {
        const response = await axios.post(apiUrl, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          timeout: 10000,
        });

        dialogMessage.value = response.data.message;
        isSubmitSuccessful.value = true;
        isCategorySettingButtonPressed.value = false;
        showDialog.value = true;
      } catch (error) {
        console.error("An error occurred while sending data:", error);
      }

      loading.value = false;
    }
  }
};

const handleInitialDataAndReset = (
  // 初期データのセット
  newInitialData: any,
  newShowDialog: any,
  oldShowDialog: any
) => {
  if (newInitialData) {
    setInitialData();
  }

  if (!newShowDialog && oldShowDialog) {
    if (isSubmitSuccessful.value) {
      router.push("/");
      isSubmitSuccessful.value = false;
    }
  }
};

// props.initialDataが変更されたときに再セット
watch(
  [() => props.initialData, () => showDialog.value],
  ([newInitialData, newShowDialog], [oldInitialData, oldShowDialog]) => {
    handleInitialDataAndReset(newInitialData, newShowDialog, oldShowDialog);
  }
);

defineExpose({
  form,
});
</script>

<style lang="scss" scoped>
.form-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  .v-form {
    background-color: #111;
  }

  .v-btn,
  :deep(.v-field) {
    color: aqua;
    background-color: #292b2f !important;
  }

  :deep(.mdi-paperclip) {
    color: aqua;
  }

  .btn-wrap {
    display: flex;
    justify-content: flex-end;
    gap: 1em;
  }

  .file-download-container {
    display: flex;
    gap: 1rem;
  }
  .v-btn {
    height: 56px;
  }
  .v-col {
    display: flex;
    justify-content: flex-end;
  }
}
</style>
