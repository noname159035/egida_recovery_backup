<template>
  <div class="container">
    <LeftNav />
    <main class="main">
      <NuxtPage />
    </main>
  </div>
</template>

<script setup>
</script>

<style scoped>
.container {
  background: #070712;
  display: flex;
}

.main {
  margin-right: 37px;
  margin-left: 300px;
  display: flex;
  flex: 1;
  height: 100%;
}

@media (max-width: 1070px) {
  .main {
    margin-left: 37px;
  }
}
</style>
