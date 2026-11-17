<script setup lang="ts">
const props = defineProps([
  'modalFunctionAuth',
  'modalFunctionReg'
]);

const emit = defineEmits([ 'open-mobile-modal' ])

// пробросим дальше
function emitOpenModal() {
  emit('open-mobile-modal')
}
</script>

<template>
  <div class="main_header_mobile__container">
<!--    <button class="main_text main_header_mobile__burger">☰</button>-->
    <mobile-left-nav @open-mobile-modal="emitOpenModal"></mobile-left-nav>
    <h1 class="main_text">EGIDA</h1>
  </div>
</template>

<style scoped>
.main_header_mobile__container {
  display: flex;
  justify-content: center;
  position: relative;
  width: 100%;
  margin-bottom: 120px;
}

.main_header_mobile__container h1 {
  margin: 0;
  font-size: 28px;
}

.main_header_mobile__burger {
  background: transparent;
  border: none;
  position: absolute;
  top: 0;
  left: 0;
  font-size: 22px;
}
</style>
