<script>
import LeftNav from '~/components/LeftNav.vue';

export default {
  components: {
    LeftNav,
  },
};
</script>

<template>
  <div class="container">
    <LeftNav />
    <main class="main">
      <NuxtPage />
    </main>
  </div>
</template>


<style scoped>
.container {
  background: #070712;
  display: flex;
}

.main {
  border: solid 1px #323047;
  border-top-left-radius: 15px;
  border-top-right-radius: 15px;
  background-color: var(--local_page_color);
  margin-top: 25px;
  margin-right: 37px;
  margin-left: 300px;
  display: flex;
  flex: 1;
}

@media (max-width: 1070px) {
  .main {
    margin-left: 70px;
  }
}

@media (max-width: 431px) {
  .main {
    margin-left: 37px;
    background: transparent;
    border: none;
  }
}
</style>
