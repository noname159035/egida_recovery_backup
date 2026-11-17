<script setup>
import {defineProps, onMounted, ref} from "vue";

const props = defineProps({
  critLevel: {type: String, required: true},
});

const text = ref("");


onMounted(() => {
  if (props.critLevel === "critical") {
    text.value = "Критический";
  } else if (props.critLevel === "high") {
    text.value = "Высокий";
  } else if (props.critLevel === "medium") {
    text.value = "Средний";
  } else if (props.critLevel === "low") {
    text.value = "Низкий";
  }
  // console.error("Текст: " + text.value);
});
</script>

<template>
  <div class="critical_circle_container main_text">
    <critical-circle :crit-level="props.critLevel"></critical-circle>
    <p> {{ text }} </p>
  </div>
</template>

<style scoped>
.critical_circle_container {
  display: flex;
  gap: 12px;
  align-items: center;
}
</style>
