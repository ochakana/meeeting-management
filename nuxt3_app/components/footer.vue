<template>
  <div class="scroll-top-wrapper ma-6">
    <v-icon @click="returnTop" start icon="mdi-arrow-up-right"></v-icon>
  </div>
</template>

<script setup lang="ts">
const returnTop = () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
};
</script>

<style scoped lang="scss">
.scroll-top-wrapper {
  position: fixed;
  bottom: 0vh;
  right: 0;
  color: aqua;
}
</style>
