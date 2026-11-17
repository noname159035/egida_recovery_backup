<script setup>
import {useNuxtApp} from '#app';
import axios from 'axios';
import {onMounted, ref} from "vue";
import {useAuthStore} from "~/store/auth.js";
import {useRoute, useRouter} from "#vue-router";

const route = useRoute();

const session_id = route.query?.session_id || null;
const model_name = route.params.model_name || 'unknown';

const prompt_description = ref(null);
const router = useRouter();

const authStore = useAuthStore();
const is_auth = ref(authStore.isAuthenticated);

// console.log("найденный промпт", prompt_description.value);

function formatDate(dateString) {
  const months = [
    'Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн',
    'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'
  ];

  const date = new Date(dateString);
  const month = months[date.getUTCMonth()] + " ";
  const day = date.getUTCDate();
  const hours = " " + String(date.getUTCHours()).padStart(2, '0');
  const minutes = String(date.getUTCMinutes()).padStart(2, '0');
  const seconds = String(date.getUTCSeconds()).padStart(2, '0');

  return `${month}${day},${hours}:${minutes}:${seconds}`;
}

async function mark_as_wrong() {
  const cfg = useRuntimeConfig()
  await axios.post(
    `${cfg.public.apiUrl}/misclassified`,
    { session_id },
    { headers: { Authorization: `Bearer ${authStore.getToken()}` } }
  )
}

onMounted(async () => {
  // ставим нужный layout
  route.meta.layout = 'navlayout'
  const cfg = useRuntimeConfig()

  // помечаем промпт как прочитанный
  await axios.post(
    `${cfg.public.apiUrl}/read_prompt`,
    { session_id },
    { headers: { Authorization: `Bearer ${authStore.getToken()}` } }
  )

  // загружаем данные модели
  const { data: modelData, error, pending } = await useAsyncData(
    `model-${model_name}`,
    async () => {
      const resp = await axios.get(
        `${cfg.public.apiUrl}/model/${model_name}`,
        { headers: { Authorization: `Bearer ${authStore.getToken()}` } }
      )
      // console.log(resp.data);
      return resp.data
    }
  )

  // ищем нужный prompt в полученных данных
  for (const elem of modelData.value.prompts) {
    if (elem.session_id === session_id) {
      prompt_description.value = elem
      break
    }
  }
})
</script>


<template>
  <div class="page_container">
    <h1 class="page_header main_text" v-if="prompt_description">{{ prompt_description.session_id }}</h1>
    <h2 class="main_text" v-if="!is_auth">Пожалуйста, авторизуйтесь для получения доступа к моделям</h2>
    <div class="page_gapper_cont" v-if="is_auth">
      <div class="top_info_container">
        <rounded-container class="quantity_background_date">
          <div>
                        <span class="time_date_container_start main_text">
                          <span v-if="prompt_description">{{ formatDate(prompt_description.timestamp) }}</span>
                        </span>
          </div>
        </rounded-container>
        <rounded-container class="frequency_background_date main_text">{{ model_name }}</rounded-container>
        <rounded-container class="quantity_find_background_date">
          <promt-status-circle v-if="prompt_description" :crit-level="prompt_description.severity.toLowerCase()"></promt-status-circle>
        </rounded-container>
      </div>

      <rounded-container>
        <h3 class="main_text chat_title">Чат</h3>
        <!--        <div style="background-color: transparent; height: 400px; width: 100%;"></div>-->
        <scroll-chat class="logs_chat" v-if="prompt_description" :chat="prompt_description.chat_history"></scroll-chat>
      </rounded-container>
      <div class="bottom_info_container" v-if="prompt_description">
        <rounded-container class="promt_actions">
          <h3 class="main_text">Доступные действия</h3>
          <rounded-button class="main_text">Переход к настройкам правил</rounded-button>
          <rounded-button class="main_text" @click="mark_as_wrong">Пометить как ложное срабатывание</rounded-button>
          <rounded-button class="main_text">Отметить рассмотренным</rounded-button>

        </rounded-container>
        <rounded-container class="promt_errors">
          <h3 class="main_text">Причина флага/ошибки</h3>
          <div class="promt_errors_container">
            <p class="main_text promt_errors_big_text" v-if="prompt_description">{{ prompt_description.type }}</p>
          </div>
        </rounded-container>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page_container {
  height: 100%;
  min-height: 100vh;
  padding-top: 0;
  padding-right: 21px;
  flex: 1;
}

.page_gapper_cont {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.top_info_container {
  display: flex;
  gap: 15px;
}

.chat_title {
  font-size: 20px;
}

.logs_chat {
  height: 300px;
  background-color: transparent !important;
}

.bottom_info_container {
  margin-bottom: 72px;
  display: flex;
  gap: 15px;
}

.promt_actions {
  display: flex;
  flex-direction: column;
  gap: 15px;
  width: 40%;
}

.promt_errors {
  flex: 1;
}

.promt_errors_container {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.promt_errors_big_text {
  font-size: 48px;
  color: var(--component_content_text);
}

.quantity_background_date {
  font-size: 20px;
  text-align: center;
  max-width: 280px;
  flex: 1;
  background: rgb(20, 19, 37);
  background: linear-gradient(37deg, rgba(20, 19, 37, 1) 0%, rgba(29, 25, 61, 1) 50%, rgba(33, 28, 71, 1) 100%);
}

.frequency_background_date {
  font-size: 20px;
  text-align: center;
  background: rgb(20, 19, 37);
  background: linear-gradient(37deg, rgba(20, 19, 37, 1) 0%, rgba(50, 31, 62, 1) 100%);
}

.quantity_find_background_date {
  font-size: 20px;
  text-align: center;
  background: rgb(20, 19, 39);
  background: linear-gradient(0deg, rgba(20, 19, 39, 1) 0%, rgba(32, 27, 70, 1) 67%);
}

@media (max-width: 1000px) {
  .bottom_info_container {
    flex-wrap: wrap;
  }

  .promt_actions {
    width: 100%;
  }

  .promt_errors {
    width: 100%;
    height: 130px;
  }
}

@media (max-width: 700px) {
  .top_info_container {
    flex-direction: column;
  }

  .quantity_background_date {
    max-width: 100%;
  }
}
</style>
