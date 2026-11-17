<script setup>

</script>

<template>
  <main class="main">
    <NuxtPage />
  </main>
</template>

<style scoped>
  .main {
    background-color: var(--main_page_background_color);
    padding: 0px 95px 0px 95px;
    min-height: 100vh;
  }

  @media (max-width: 431px) {
    .main {
      padding: 0 25px;
    }
  }
</style>
