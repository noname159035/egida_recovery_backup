<script setup>
import { defineProps, onMounted, ref } from "vue";

const props = defineProps({
  Alerts: { type: String, required: true },
  RiskLevel: { type: String, required: true },
  ApiCalls: { type: String, required: true },
  Uptime: { type: String, required: true },
  Latency: { type: String, required: true },
});
</script>


<template>
  <rounded-container class="model-description_container">
    <div class="main_text">
      <span class="gray_text">Alerts: </span>
      <span>{{ Alerts }}</span>
    </div>
    <div class="main_text">
      <span class="gray_text">Risk Level: </span>
      <span>{{ RiskLevel }}</span>
    </div>
    <div class="main_text">
      <span class="gray_text">API Calls (24h): </span>
      <span>{{ ApiCalls }}</span>
    </div>
    <div class="main_text">
      <span class="gray_text">Uptime: </span>
      <span>{{ Uptime }}%</span>
    </div>
    <div class="main_text">
      <span class="gray_text">Latency: </span>
      <span>{{ Latency }}ms (avg)</span>
    </div>
  </rounded-container>
</template>

<style scoped>
  .model-description_container {
    display: flex;
    flex-direction: column;
    gap: 20px;
    justify-content: center;
  }

  .gray_text {
    color: var(--component_content_text);
    font-size: 20px;
  }

  .main_text {
    font-size: 20px;
  }
</style>
