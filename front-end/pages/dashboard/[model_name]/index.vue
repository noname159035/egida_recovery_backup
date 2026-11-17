<script setup>
import { computed, reactive, ref, onMounted, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useNuxtApp, useRuntimeConfig } from '#app';
import axios from 'axios';

import PromptInfoRounded     from '~/components/promptInfoRounded.vue';
import UseMenuBtn            from '~/components/useMenuBtn.vue';
import PromptChat            from '~/components/promptChat.vue';
import Diagram_mobile_circle from '~/components/diagram_mobile_circle.vue';
import { useAuthStore }      from '~/store/auth.js';
import { useDeviceStore }    from '~/store/device.js';

const { $axios } = useNuxtApp();

const device   = useDeviceStore();
const isMobile = computed(() => device.isMobile);

const route      = useRoute();
const router     = useRouter();
const model_name = route.params?.model_name || null;

const authStore = useAuthStore();
const is_auth   = ref(authStore.isAuthenticated);

const hide_use = ref(false);
function updateHideUse() {
  hide_use.value = window.innerWidth <= 1284;
}

const modalState = reactive({
  isVisible: false,
  selectedPrompt: null
});

const data    = ref(null);
const pending = ref(false);
const error   = ref(null);

// default using_text to zero; will be set to data.calls after fetch
const using_text = ref(0);

async function fetchModelData() {
  pending.value = true;
  error.value   = null;
  try {
    const runtimeConfig = useRuntimeConfig();
    const resp = await axios.get(
      `${runtimeConfig.public.apiUrl}/model/${model_name}`,
      { headers: { Authorization: `Bearer ${authStore.getToken()}` } }
    );
    // console.log("Dashboard получил:", resp.data);
    data.value = resp.data;
    // default using_text to calls count
    using_text.value = resp.data.calls;
  } catch (err) {
    console.error("Ошибка при загрузке данных модели:", err);
    error.value = err;
  } finally {
    pending.value = false;
  }
}

const useBtns = computed(() => {
  const d = data.value || { calls: 0, tokens: 0, costs: 0 };
  return [
    { id: "use_1", text: "Вызовы",   value: d.calls  },
    { id: "use_2", text: "Токены",    value: d.tokens },
    { id: "use_3", text: "Стоимость", value: d.costs  }
  ];
});

const activeBtn = ref("use_1");

function handleClick(id) {
  activeBtn.value = id;
  const btn = useBtns.value.find(b => b.id === id);
  using_text.value = btn ? btn.value : 0;
}

function openPrompt(prompt) {
  modalState.selectedPrompt = prompt;
  modalState.isVisible      = true;
}

function closeModal() {
  modalState.isVisible      = false;
  modalState.selectedPrompt = null;
}

onMounted(() => {
  updateHideUse();
  route.meta.layout = "navlayout";
  window.addEventListener('resize', updateHideUse);
  fetchModelData();
});

onUnmounted(() => {
  window.removeEventListener('resize', updateHideUse);
});
</script>

<template>
  <div class="page_container">
    <h2 class="main_text" v-if="!is_auth">
      Пожалуйста, авторизуйтесь для получения доступа к моделям
    </h2>

    <!-- Desktop Dashboard -->
    <div class="page_gapper_cont" v-if="is_auth && !isMobile">
      <!-- Header & Time Filter -->
      <div class="time_filter_container">
        <h1 class="page_header main_text">{{ model_name }}</h1>
        <span class="main_text filer_text">Данные за последние</span>
        <span class="main_text filer_text">24</span>
        <span class="main_text filer_text">часа /</span>
        <div class="time_filter_menu main_text filer_text">
          <p class="filer_menu">Выбрать дату и время</p>
          <svg width="14" height="8" viewBox="0 0 14 8" fill="none"
               xmlns="http://www.w3.org/2000/svg">
            <path d="M7 8L0 1.24029L1.28439 0L7 5.51925L12.7156 0L14 1.24029L7 8Z" fill="white"/>
          </svg>
        </div>
        <rounded-container class="filer_icon_container">
          <svg width="19" height="22" viewBox="0 0 19 22" fill="none"
               xmlns="http://www.w3.org/2000/svg">
            <path d="M8.65776 21.1928H6.8455V10.8723L0.315796 2.34892V0.736816H18.0393V2.33971L11.8205
                     10.863V17.725L8.65776 21.1928ZM8.08925 19.8291H8.14262L10.5768
                     17.1601V10.3847L16.621 2.10055H1.75L8.08925 10.3755V19.8291Z"
                  fill="white"/>
          </svg>
        </rounded-container>
      </div>

      <!-- Quantities -->
      <div class="quantity_container">
        <rounded-container class="quantity_cont_flex quantity_background">
          <h3 class="main_text">Количество запросов</h3>
          <p v-if="data" class="main_text dashboard_model_value">{{ data.total_requests }}</p>
        </rounded-container>
        <rounded-container class="quantity_cont_flex frequency_background">
          <h3 class="main_text">Общая частота обнаружения</h3>
          <p v-if="data" class="main_text">{{ data.detection_freq }}</p>
        </rounded-container>
        <rounded-container class="quantity_cont_flex quantity_find_background">
          <h3 class="quantity_title main_text">Количество обнаружений</h3>
          <div class="quantity_text_time_cont">
            <span v-if="data" class="quantity main_text">{{ data.detections_ph }}</span>
            <span class="quantity postfix main_text">/</span>
            <span class="quantity postfix main_text">час</span>
          </div>
        </rounded-container>
      </div>

      <!-- Analysis -->
      <div class="analys_container">
        <rounded-container class="score_cont_flex main_text">
          <h3 class="score_title main_text">Overall SydeScore</h3>
          <div class="sydeScore_container">
            <diagram-score/>
            <div class="sydeScore_content_container">
              <div class="sydeScore_content">
                <p>Метрика #xxxx</p>
                <p>Оценка 70</p>
              </div>
            </div>
          </div>
        </rounded-container>

        <rounded-container class="risk_analis_container main_text">
          <h3 class="analys_title main_text">Анализ рисков</h3>
          <div class="diagram_container">
            <diagram/>
            <div class="diagram_stat_container">
              <div class="diagram_stat_element">
                <div class="diagram_stat_element__left">
                  <critical-circle crit-level="Critical_new"/>
                  <p>Критические</p>
                </div>
                <p v-if="data">{{ data.quant['critical'] }}</p>
              </div>
              <div class="diagram_stat_element">
                <div class="diagram_stat_element__left">
                  <critical-circle crit-level="High_new"/>
                  <p>Высокие</p>
                </div>
                <p v-if="data">{{ data.quant['high'] }}</p>
              </div>
              <div class="diagram_stat_element">
                <div class="diagram_stat_element__left">
                  <critical-circle crit-level="Medium_new"/>
                  <p>Средние</p>
                </div>
                <p v-if="data">{{ data.quant['middle'] }}</p>
              </div>
              <div class="diagram_stat_element">
                <div class="diagram_stat_element__left">
                  <critical-circle crit-level="Low_new"/>
                  <p>Низкий</p>
                </div>
                <p v-if="data">{{ data.quant['low'] }}</p>
              </div>
            </div>
          </div>
        </rounded-container>

        <!-- Usage Buttons (hidden variant) -->
        <rounded-container class="using_models__inner" v-if="hide_use">
          <h3 class="main_text">Использование модели</h3>
          <div class="using_models_nav">
            <use-menu-btn
              v-for="btn in useBtns"
              :key="btn.id"
              :text="btn.text"
              :disable="activeBtn === btn.id"
              @click="handleClick(btn.id)"
            />
          </div>
          <p class="main_text">{{ using_text }}</p>
        </rounded-container>
      </div>

      <!-- Bottom Prompts & Usage (visible variant) -->
      <div class="bottom_promt_container">
        <rounded-container class="prompt_container main_text">
          <h3 class="prompt_title main_text">Уязвимости</h3>
          <div class="prompt_gap_cont">
            <prompt-info-rounded
              class="prompt_gap_cont__element"
              v-if="data"
              v-for="elem in data.prompts"
              :key="elem.id"
              :promptName="elem.prompt_text"
              :promptClass="elem.severity"
              @openModal="openPrompt(elem)"
            />
          </div>
        </rounded-container>

        <rounded-container class="using_models" v-if="!hide_use">
          <rounded-container class="using_models__inner">
            <h3 class="main_text">Использование модели</h3>
            <div class="using_models_nav">
              <use-menu-btn
                v-for="btn in useBtns"
                :key="btn.id"
                :text="btn.text"
                :disable="activeBtn === btn.id"
                @click="handleClick(btn.id)"
              />
            </div>
            <p class="main_text">{{ using_text }}</p>
          </rounded-container>
        </rounded-container>
      </div>
    </div>

    <!-- Mobile Dashboard -->
    <div class="dashboard_mobile_main_container" v-if="isMobile">
      <h1 class="main_text dashboard_mobile_main__header">EGIDA</h1>
      <h1 class="main_text dashboard_mobile_main__title">Dashboard</h1>

      <rounded-container class="dashboard_container">
        <div class="dashboard__stat main_text">
          <div class="dashboard__stat_elem dashboard__stat_blue">
            <p>Количество запросов</p>
            <p v-if="data" class="dashboard__stat_value">{{ data.total_requests }}</p>
          </div>
          <div class="dashboard__stat_elem dashboard__stat_red">
            <p>Общая частота обнаружения</p>
            <p v-if="data" class="dashboard__stat_value">{{ data.detection_freq }}</p>
          </div>
          <div class="dashboard__stat_elem dashboard__stat_blue_top">
            <p>Количество обнаружений</p>
            <div class="dashboard__stat_value">
              <p v-if="data">{{ data.detections_ph }}</p>
              <p>/час</p>
            </div>
          </div>
        </div>

        <rounded-container class="dashboard_analysis main_text">
          <h2>Анализ рисков</h2>
          <div class="dashboard_analysis_diagram__container">
            <diagram_mobile_circle/>
            <div class="diagram_stat_container">
              <div class="diagram_stat_element">
                <div class="diagram_stat_element__left">
                  <critical-circle crit-level="critical_new" class="mobile_crit_circle"/>
                  <p>Критические</p>
                </div>
                <p v-if="data">{{ data.quant['critical'] }}</p>
              </div>
              <div class="diagram_stat_element">
                <div class="diagram_stat_element__left">
                  <critical-circle crit-level="high_new" class="mobile_crit_circle"/>
                  <p>Высокие</p>
                </div>
                <p v-if="data">{{ data.quant['high'] }}</p>
              </div>
              <div class="diagram_stat_element">
                <div class="diagram_stat_element__left">
                  <critical-circle crit-level="medium_new" class="mobile_crit_circle"/>
                  <p>Средние</p>
                </div>
                <p v-if="data">{{ data.quant['middle'] }}</p>
              </div>
              <div class="diagram_stat_element">
                <div class="diagram_stat_element__left">
                  <critical-circle crit-level="low_new" class="mobile_crit_circle"/>
                  <p>Низкий</p>
                </div>
                <p v-if="data">{{ data.quant['low'] }}</p>
              </div>
            </div>
          </div>
        </rounded-container>

        <rounded-container class="dashboard_prompts main_text">
          <h2>Уязвимости</h2>
          <div class="prompt_gap_cont">
            <prompt-info-rounded
              class="prompt_gap_cont__element"
              v-if="data"
              v-for="elem in data.prompts"
              :key="elem.id"
              :promptName="elem.prompt_text"
              :promptClass="elem.severity"
              @openModal="openPrompt(elem)"
            />
          </div>
        </rounded-container>

        <rounded-container class="using_models__inner">
          <h3 class="main_text">Использование модели</h3>
          <div class="using_models_nav">
            <use-menu-btn
              v-for="btn in useBtns"
              :key="btn.id"
              :text="btn.text"
              :disable="activeBtn === btn.id"
              @click="handleClick(btn.id)"
            />
          </div>
          <p class="main_text">{{ using_text }}</p>
        </rounded-container>
      </rounded-container>
    </div>

    <!-- Modal Chat -->
    <ModalChat v-model="modalState.isVisible">
      <prompt-chat
        :prompt="modalState.selectedPrompt"
        @closeModal="closeModal"
      />
    </ModalChat>
  </div>
</template>

<style scoped>
.page_container {
  min-height: 100vh;
  padding-right: 21px;
  padding-top: 25px;
  flex: 1;
}

.page_header {
  font-size: 26px;
  margin: 0;
  margin-right: 40px;
  color: var(--main_text_selected);
}

.page_gapper_cont {
  display: flex;
  flex-direction: column;
  row-gap: 15px;
}

.time_filter_container {
  display: flex;
  column-gap: 10px;
  font-size: 25px;
  color: var(--main_text_selected);
  align-items: center;
  flex-wrap: wrap;
}

.filer_text {
  color: var(--filter_text);
  font-size: 16px;
}

.filer_menu {
  color: var(--main_text_selected);
  margin-right: 5px;
}

.filer_icon_container {
  transition: transform 0.05s ease-in-out;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  border-radius: 7px;
  width: 30px;
  height: 30px;
}

.filer_icon_container:hover {
  transform: scale(1.02);
}

.filer_icon_container:active {
  transform: scale(1.04);
}

.time_filter_menu {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.quantity_container {
  display: flex;
  column-gap: 10px;
  color: var(--main_text_selected);
}

.quantity_container h3 {
  font-size: 20px;
}

.quantity_container p,
.quantity {
  font-size: 48px;
  margin-top: auto;
}

.quantity_text_time_cont {
  margin-top: auto;
}

.postfix {
  font-size: 24px;
}

.quantity_cont_flex {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.score_cont_flex {
  flex: 1;
}

.quantity_background {
  background: rgb(20, 19, 37);
  background: linear-gradient(37deg, rgba(20, 19, 37, 1) 0%, rgba(29, 25, 61, 1) 50%, rgba(33, 28, 71, 1) 100%);
}

.frequency_background {
  background: rgb(20, 19, 37);
  background: linear-gradient(37deg, rgba(20, 19, 37, 1) 0%, rgba(50, 31, 62, 1) 100%);
}

.quantity_find_background {
  background: rgb(20, 19, 39);
  background: linear-gradient(0deg, rgba(20, 19, 39, 1) 0%, rgba(32, 27, 70, 1) 67%);
}

.analys_container {
  font-size: 20px;
  display: flex;
  column-gap: 10px;
  row-gap: 10px;
  color: var(--main_text_selected);
  flex-wrap: wrap;
  height: auto;
}

.score_title {
  margin-bottom: 15px;
}

.sydeScore_container {
  display: flex;
  padding-left: 20px;
  column-gap: 15px;
}

.sydeScore_content_container {
  display: flex;
  flex: 1;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  row-gap: 15px;
}

.sydeScore_content {
  display: flex;
  flex-direction: column;
  row-gap: 15px;
}

.analys_title {
  font-size: 20px;
  margin-bottom: 25px;
}

.diagram_container {
  display: flex;
  justify-content: space-between;
  gap: 0;
}

.diagram_stat_container {
  display: flex;
  flex-direction: column;
  margin-bottom: 13px;
  margin-top: 30px;
  gap: 20px;
}

.diagram_stat_element {
  display: flex;
  gap: 25px;
  justify-content: space-between;
}

.diagram_stat_element__left {
  display: flex;
  gap: 9px;
  color: var(--component_content_text);
}

.bottom_promt_container {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.prompt_container {
  flex: 1;
  font-size: 20px;
  color: var(--main_text_selected);
  margin-bottom: 24px;
}

.prompt_title {
  margin-bottom: 13px;
}

.prompt_gap_cont {
  overflow-y: auto;
  row-gap: 6px;
  height: 355px;
  box-sizing: border-box;
}

.promt_element:not(:last-of-type) {
  margin-bottom: 6px;
}

.using_models {
  position: relative;
  padding: 0;
  height: 426px;
  width: 350px;
}

.using_models__inner {
  width: calc(100% - 42px);
  position: absolute;
  top: -2px;
  left: -2px;
}

.using_models_nav {
  margin-top: 9px;
  border-bottom: solid 1px var(--component_content_text);
  display: flex;
  gap: 10px;
  justify-content: space-between;
}

@media (max-width: 1334px) {
  .risk_analis_container {
    flex: 1;
  }

  .diagram_container {
    justify-content: space-between;
    gap: 0;
  }

  .using_models__inner {
    position: relative;
    flex: 1;
  }
}

@media (max-width: 1050px) {
  .quantity_container p,
  .quantity {
    font-size: 27px;
  }

  .quantity_container h3 {
    height: 46px;
    overflow-y: hidden;
  }
}

@media (max-width: 800px) {
  .time_filter_container {
    justify-content: center;
  }

  .quantity_container {
    margin-top: 20px;
    flex-direction: column;
    gap: 10px;
  }

  .quantity_cont_flex {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .score_cont_flex,
  .diagram {
    display: none;
  }

  .diagram_stat_container {
    margin: 0;
  }

  .diagram_container {
    justify-content: center;
  }

  .prompt_container {
    width: 10px;
  }
}

@media (max-width: 650px) {
  .risk_analis_container {
    display: none;
  }
}

@media (max-width: 430px) {
  .page_container {
    padding: 0;
  }

  .dashboard_mobile_main__header {
    width: 100%;
    text-align: center;
    font-size: 28px;
  }

  .dashboard_mobile_main__title {
    font-size: 16px;
  }

  .dashboard_container {
    border-width: 1px;
  }

  .dashboard__stat {
    display: flex;
    flex-direction: column;
    row-gap: 10px;
  }

  .dashboard__stat_elem {
    font-size: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px;
    height: 35px;
    border: 1px solid #323047;
    border-radius: 25px;
    box-sizing: border-box;
  }

  .dashboard__stat_blue {
    background: linear-gradient(86deg, #141325 22.67%, #211C47 61.74%);
  }

  .dashboard__stat_red {
    background: linear-gradient(79deg, #151325 26.69%, #321F3E 62.71%);
  }

  .dashboard__stat_blue_top {
    background: linear-gradient(180deg, #201B46 0%, #141327 100%);
  }

  .dashboard__stat_value {
    display: flex;
    width: 60px;
    font-size: 13px;
  }

  .dashboard_analysis {
    margin-top: 10px;
    font-size: 13px;
  }

  .dashboard_analysis h2 {
    font-size: 13px;
    font-weight: normal;
  }

  .dashboard_analysis_diagram__container {
    margin-top: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
  }

  .diagram_stat_container {
    font-size: 10px;
    row-gap: 10px;
  }

  .diagram_stat_element {
    line-height: 12px !important;
    height: 12px !important;
  }

  .mobile_crit_circle {
    height: 10px;
    width: 10px;
  }

  .dashboard_prompts {
    margin-top: 10px;
  }

  .prompt_gap_cont {
    width: 100%;
    max-width: 260px;
    font-size: 10px;
    height: auto;
  }

  .dashboard_prompts h2 {
    margin-bottom: 10px;
    font-size: 13px;
    font-weight: normal;
  }

  .using_models__inner {
    margin-top: 10px;
  }

  .using_models__inner h3 {
    font-size: 13px;
  }

  .using_models__inner p {
    margin-top: 10px;
    font-size: 13px;
  }
}

@media (max-width: 380px) {
  .dashboard_analysis_diagram__container {
    justify-content: center;
  }
}
</style>
