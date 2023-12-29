<template>
  <v-layout>
    <v-app-bar
      app
      absolute
      color="#36383b"
      dark
      hide-on-scroll
      prominent
      scroll-behavior="elevate"
      class="mx-auto overflow-hidden"
      height="70"
    >
      <template v-slot:prepend>
        <v-app-bar-nav-icon
          variant="text"
          @click.stop="drawer = !drawer"
        ></v-app-bar-nav-icon>
        <nuxt-link to="/">
          <v-btn icon="mdi-home"> </v-btn>
        </nuxt-link>
      </template>

      <v-app-bar-title>{{ title }}</v-app-bar-title>

      <template v-slot:append>
        <v-btn icon="mdi-dots-vertical"></v-btn>
      </template>
    </v-app-bar>
    <v-navigation-drawer
      v-model="drawer"
      location="bottom"
      temporary
      color="#2c2d2f"
    >
      <v-list :items="items"></v-list>
    </v-navigation-drawer>
  </v-layout>
</template>

<script lang="ts">
export default defineComponent({
  data() {
    return {
      title: "議事録管理アプリ",
      drawer: false,
      group: null,
      items: [
        {
          title: "Foo",
          value: "foo",
        },
        {
          title: "Bar",
          value: "bar",
        },
        {
          title: "Fizz",
          value: "fizz",
        },
        {
          title: "Buzz",
          value: "buzz",
        },
      ],
    };
  },

  watch: {
    group() {
      this.drawer = false;
    },
  },
});
</script>

<style scoped lang="scss">
.header {
  background: rgba(48, 50, 55, 0.8) !important;
  opacity: 0.8;
  position: sticky;
  top: 0vh;
  z-index: 1;
}
.v-toolbar {
  position: sticky !important;
  // opacity: 0.5;
  .v-toolbar-title,
  :deep(.v-icon) {
    color: aqua !important;
  }
}
.v-navigation-drawer {
  box-shadow: 0.3em 0 0.5em #111;
  :deep(.v-list-item-title) {
    color: aqua !important;
  }
}
</style>
