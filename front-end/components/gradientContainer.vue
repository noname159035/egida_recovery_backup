<script setup>
import { ref, onMounted, watch } from 'vue';

const props = defineProps({
  colored: { type: Boolean, default: false }
});

const container = ref(null);

function updateContainerStyles() {
  if (container.value) {
    if (props.colored) {
      container.value.style.setProperty(
        '--gradiend_container_background',
        'linear-gradient(90deg, rgba(37, 28, 78, 1) 0%, rgba(105, 80, 175, 1) 100%)'
      );
      container.value.style.setProperty('--gradiend_container_text', '#FFFFFF');
    } else {
      // Здесь можно указать fallback-значения, если компонент не colored.
      container.value.style.setProperty('--gradiend_container_background', '#17162B');
      container.value.style.setProperty('--gradiend_container_text', '#000000');
    }
  }
}

onMounted(() => {
  updateContainerStyles();
});

watch(
  () => props.colored,
  () => {
    updateContainerStyles();
  }
);
</script>

<template>
  <div class="prompt_element_container" ref="container">
    <slot></slot>
  </div>
</template>

<style scoped>
.prompt_element_container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: background-color 0.15s ease-in-out, background 0.15s ease-in-out;
  /* Используем fallback-значения на случай, если CSS-переменные не установлены */
  background: var(--gradiend_container_background, #17162B);
  height: 45px !important;
  gap: 20px;
  color: var(--gradiend_container_text, #000000);
}
</style>
