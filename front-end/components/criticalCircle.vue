<script setup>
import {defineProps, onMounted, ref} from "vue";

const props = defineProps({
  critLevel: {type: String, required: true},
});

const color = ref("");

onMounted(() => {
  if (props.critLevel === "critical") {
    color.value = "var(--stat_red)";
  } else if (props.critLevel === "high") {
    color.value = "var(--stat_gold)";
  } else if (props.critLevel === "medium") {
    color.value = "var(--stat_purp)";
  } else if (props.critLevel === "low") {
    color.value = "var(--stat_green)";
  } else if (props.critLevel === "critical_new") {
    color.value = "var(--stat_critical_color)";
  } else if (props.critLevel === "high_new") {
    color.value = "var(--stat_high_color)";
  } else if (props.critLevel === "medium_new") {
    color.value = "var(--stat_normal_color)";
  } else if (props.critLevel === "low_new") {
    color.value = "var(--stat_low_color)";
  }
  // console.error("Цвет: " + color.value);
});
</script>


<template>
  <div class="critical_circle" :style="{ backgroundColor: color }"></div>
</template>

<style scoped>
.critical_circle {
  width: 20px;
  height: 20px;
  border-radius: 50%;
}
</style>
