<script setup>
import {useAsyncData, useNuxtApp, useRuntimeConfig} from '#app';
import {onMounted, ref} from 'vue';
import {useAuthStore} from "~/store/auth.js";
import axios from "axios";

const route = useRoute()

const {$axios} = useNuxtApp();
const authStore = useAuthStore();
const is_auth = ref(authStore.isAuthenticated);

const logs = ref(null);
const error = ref(null);
const error_reason = ref("");

const runtimeConfig = useRuntimeConfig();
onMounted(async () => {
  route.meta.layout = 'navlayout-colorless'
  try {
    const response = await axios.get(
      `${runtimeConfig.public.apiUrl}/logs`,
      { headers: { Authorization: `Bearer ${authStore.getToken()}` } }
    )
    logs.value = response.data.logs || []
    // console.log(logs.value);
  } catch (e) {
    if (e.response && e.response.status === 422) {
      error_reason.value = "Пожалуйста, авторизуйтесь для получения доступа к моделям";
      // console.error("Ошибка 422: ", e.response.data);
    } else {
      // console.error("Ошибка: ", e);
    }
  }
})
</script>

<template>
  <div class="page_container">
    <h1 class="page_header main_text">Логи</h1>
    <div v-if="error_reason" class="error main_text">
      Ошибка загрузки: {{ error_reason }}
    </div>
    <div v-else class="logs_content">
      <h2 class="main_text" v-if="!is_auth">Пожалуйста, авторизуйтесь для получения доступа к моделям</h2>
      <rounded-container class="logs_container">
        <gradient-container :colored="true" class="logs__title_container">
          <div class="logs_element_container">
            <h2 class="logs_element main_text">User ID</h2>
            <h2 class="logs_element main_text">IP-адрес</h2>
            <h2 class="logs_element main_text">Дата и время</h2>
            <h2 class="logs_element logs_element_text main_text">Текст запроса</h2>
            <h2 class="logs_element main_text">Тип</h2>
          </div>
        </gradient-container>
        <gradient-container :colored="false" v-for="log in logs" :key="log.id" class="logs__block">
          <div class="logs_element_container">
            <h2 class="logs_element logs_element_log main_text">{{ log.user_id }}</h2>
            <h2 class="logs_element logs_element_log main_text">{{ log.ip }}</h2>
            <h2 class="logs_element logs_element_log main_text">{{ log.ts }}</h2>
            <h2 class="logs_element logs_element_log logs_element_text main_text">{{ log.content }}</h2>
            <h2 class="logs_element logs_element_log main_text">{{ log.label }}</h2>
          </div>
        </gradient-container>



        <gradient-container :colored="true" class="logs_mobile__title_container">
          <div class="logs_mobile__element_container">
            <h2 class="main_text">Логи</h2>
          </div>
        </gradient-container>
        <div :colored="false" v-for="log in logs" :key="log.id">
          <gradient-container class="logs_mobile__block">
            <div class="logs_mobile__element_container">
              <h2 class="main_text">{{ log.label }}</h2>
              <svg width="4" height="16" viewBox="0 0 4 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                <ellipse cx="1.99579" cy="2.30158" rx="1.6999" ry="1.47394" fill="#8E8D9D"/>
                <ellipse cx="1.99579" cy="8.19757" rx="1.6999" ry="1.47394" fill="#8E8D9D"/>
                <ellipse cx="1.99579" cy="14.0936" rx="1.6999" ry="1.47394" fill="#8E8D9D"/>
              </svg>
            </div>
          </gradient-container>
          <gradient-container class="main_text logs_mobile__info">
            <h2 class="main_text">{{log.user_id}}</h2>
            <h2 class="main_text">{{log.ip}}</h2>
            <h2 class="main_text">{{log.ts}}</h2>
            <h2 class="main_text">{{log.content}}</h2>
          </gradient-container>
        </div>
      </rounded-container>
    </div>
  </div>
</template>

<style scoped>
.page_container {
  min-height: 100vh;
  width: calc(100% - 67px);
  padding-top: 25px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}

.page_header {
  margin: 0;
  font-size: 26px;
  margin-bottom: 47px;
}

.logs_content {
  display: flex;
  flex-wrap: wrap;
  flex: 1;
  padding-bottom: 100px;
}

.logs_container {
  display: flex;
  flex-direction: column;
  gap: 5px;
  width: 100%;
  padding: 65px 30px 10px 30px;
}

.logs_element_container {
  padding: 0px 20px 0px 20px;
  width: 100%;
  display: flex;
  gap: 10px;
  justify-content: space-between;
}

.logs_element {
  font-size: 20px;
  text-wrap: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
}

.logs_element:first-child {
  min-width: 70px;
}

.logs_element:not(:first-child) {
  width: 150px;
}

.logs_element:last-child {
  flex: 1;
  max-width: 150px;
}

.logs_element:nth-child(4) {
  width: 300px;
}

.logs_element_log {
  font-size: 16px;
  color: var(--component_content_text);
}

.logs_mobile__title_container {
  display: none;
}

.logs_mobile__element_container {
  padding: 0px 20px 0px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.logs__block {
  display: flex;
}

.logs_mobile__element_container {
  display: flex;
  gap: 10px;
}

.logs_mobile__title_container {
  display: none;
}

.logs_mobile__block {
  display: none;
  border-left: solid 1px var(--border_color);
  border-right: solid 1px var(--border_color);
}

.logs_mobile__info {
  display: none;
}

@media (max-width: 1300px) {
  .logs_element_text {
    display: none;
  }
  .logs_element {
    font-size: 16px;
    max-width: 20%;
    overflow-x: clip;
  }

  .logs_element:last-child {
    max-width: 10%;
  }

  .logs_element:first-child {
    max-width: 5%;
  }

  .logs_element_container {
    gap: 0;
  }
}

@media (max-width: 700px) {
  .logs_container {
    width: 100%;
  }

  .page_container {
    width: 100%;
  }

  .logs_mobile__block {
    display: flex;
    font-size: 10px;
    flex-direction: column;
    justify-content: center;
    padding: 0px 20px 0px 20px;
  }

  .logs__block {
    display: none;
  }

  .logs_mobile__title_container {
    display: flex;
  }

  .logs__title_container {
    display: none;
  }

  .logs_mobile__info {
    height: auto !important;
    display: flex !important;
    flex-direction: column;
    align-items: flex-start !important;
    padding: 10px 20px;
    font-size: 10px;
    border: solid 1px var(--border_color);
    border-top: none;
    border-bottom-right-radius: 10px;
    border-bottom-left-radius: 10px;
  }
}
</style>
