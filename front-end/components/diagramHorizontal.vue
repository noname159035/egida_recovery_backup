<script setup lang="ts">

</script>

<template>
            <div class="analys_risk_container">
              <div class="risk_progress">
                <p class="risk_progress_text">Критические</p>
                <progress class="risk_progress_bar red_bar" id="file" max="100" value="30"></progress>
              </div>
              <div class="risk_progress">
                <p class="risk_progress_text">Высокие</p>
                <progress class="risk_progress_bar gold_bar" id="file" max="100" value="50"></progress>
              </div>
              <div class="risk_progress">
                <p class="risk_progress_text">Средние</p>
                <progress class="risk_progress_bar purp_bar" id="file" max="100" value="20"></progress>
              </div>
              <div class="risk_progress">
                <p class="risk_progress_text">Низкие</p>
                <progress class="risk_progress_bar green_bar" id="file" max="100" value="90"></progress>
              </div>
            </div>
</template>

<style scoped>
.analys_risk_container {
  display: flex;
  flex-direction: column;
  row-gap: 12px;
}

.risk_progress {
  display: flex;
  align-items: center;
  color: var(--main_text_not_selected);
}


.risk_progress_bar {
  width: 100%;
  height: 20px;
  border: 0;
  border-radius: 9px;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
}

.risk_progress_text {
  width: 170px;
  font-size: 18px;
}

.red_bar::-webkit-progress-bar {
  background-color: var(--stat_red_light);
}
.red_bar::-webkit-progress-value {
  background-color: var(--stat_red);
}
.red_bar::-moz-progress-bar {
  background-color: var(--stat_red);
}

.gold_bar::-webkit-progress-bar {
  background-color: var(--stat_gold_light);
}
.gold_bar::-webkit-progress-value {
  background-color: var(--stat_gold);
}
.gold_bar::-moz-progress-bar {
  background-color: var(--stat_gold);
}

.purp_bar::-webkit-progress-bar {
  background-color: var(--stat_purp_light);
}
.purp_bar::-webkit-progress-value {
  background-color: var(--stat_purp);
}
.purp_bar::-moz-progress-bar {
  background-color: var(--stat_purp);
}

.green_bar::-webkit-progress-bar {
  background-color: var(--stat_green_light);
}
.green_bar::-webkit-progress-value {
  background-color: var(--stat_green);
}
.green_bar::-moz-progress-bar {
  background-color: var(--stat_green);
}
</style>
