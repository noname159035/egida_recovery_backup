<template>
  <div>
    <h1 class="main_text">Тестовая страничка пользователя, сюда мы не смотрим :/</h1>
    <button @click="fetchData">Получить данные</button>
    <p v-if="data" class="main_text">Ответ от API: {{ data }}</p>
    <p v-if="error" class="main_text">Ошибка: {{ error }}</p>
  </div>
</template>

<script setup>
import {ref} from 'vue';

const route = useRoute()
route.meta.layout = "navlayout"

const data = ref(null);
const error = ref(null);


const fetchData = async () => {
  const { $axios } = useNuxtApp();
  const runtimeConfig = useRuntimeConfig(); // Получаем runtime-конфигурацию
  try {
    const response = await $axios.get(`${runtimeConfig.public.apiUrl}/model/gigachat`);
    data.value = response.data;
  } catch (err) {
    // console.error(err);
    error.value = err.message;
  }
};
</script>


<style scoped>
.page_container {
  min-height: 100vh;
  width: calc(100% - 67px);
  padding-top: 25px;
}

.page_header {
  margin: 0;
  font-size: 26px;
  margin-bottom: 47px;
}

.models_content {
  padding-right: 20px;
  padding-bottom: 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 100px;
  justify-content: space-between;
}

.models_link {
  flex-basis: calc(50% - 100px);
  text-decoration: none;
  color: inherit;
}

.models_button {
  background: rgb(20, 19, 37);
  background: linear-gradient(90deg, rgba(20, 19, 37, 1) 0%, rgba(33, 28, 71, 1) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  border-radius: 24px !important;
  height: 60px;
  width: 100%;
  text-align: center;
  transition: transform 0.07s ease-in-out, background 0.05s ease-in-out;
}

.models_button:hover {
  transform: scale(1.03);
}

.models_button:active {
  transform: scale(1.05);
}

.models_article {
  margin-top: 25px;
  height: 280px;
  width: 100%;
}
</style>
