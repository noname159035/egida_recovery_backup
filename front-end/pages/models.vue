<script setup>
import {useAsyncData, useNuxtApp, useRuntimeConfig} from '#app';
import {onMounted, ref} from 'vue';
import {useAuthStore} from "~/store/auth.js";

const route = useRoute()

const {$axios} = useNuxtApp();
const authStore = useAuthStore();
const is_auth = ref(authStore.isAuthenticated);
const error_reason = ref("");

const runtimeConfig = useRuntimeConfig();
const {data, pending, error} = await useAsyncData('models', async () => {
  const token = authStore.getToken();
  // console.log("Передаваемый токен: ", token);

  try {
    const response = await $axios.get(`${runtimeConfig.public.apiUrl}/models`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    // console.log("Модели приняли", response.data);
    return response.data;
  } catch (e) {
    if (e.response && e.response.status === 422) {
      error_reason.value = "Пожалуйста, авторизуйтесь для получения доступа к моделям";
      // console.error("Ошибка 422: ", e.response.data);
    } else {
      // console.error("Ошибка: ", e);
    }
  }
});


const get_alerts = (prompts) => {
  var buff_data = {
    "critical": 0,
    "high": 0,
    "middle": 0,
    "low": 0
  };
  var k = 0;
  var is_empty = true;

  for (var arr in prompts) {
    buff_data[prompts[arr].severity.toLowerCase()] += 1;
    k += 1;
  }
  var result = "" + k + " (";
  // console.log(buff_data);
  for (var elem in buff_data) {
    if (buff_data[elem] != 0) {
      // console.log(buff_data[elem]);
      result += elem + " " + buff_data[elem] + ", ";
      is_empty = false;
    }
  }
  if (!is_empty) {
    result = result.slice(0, -2) + ")";
  } else {
    result = "0";
  }
  // console.log(result)
  return result;
}

onMounted(() => {
  route.meta.layout = "navlayout";
});
</script>

<template>
  <div class="page_container">
    <h1 class="page_header main_text">Модели LLM</h1>

<!--    <div v-if="pending" class="loading main_text">-->
<!--      Загрузка моделей...-->
<!--    </div>-->

    <div v-if="error_reason" class="error main_text">
      Ошибка загрузки: {{ error_reason }}
    </div>

    <div v-else class="models_content">
      <nuxt-link
        v-if="is_auth"
        v-for="(model, model_name) in data"
        :key="model_name"
        :to="{ name: 'dashboard-model_name', params: { model_name } }"
        class="models_link"
      >
        <rounded-container class="models_button main_text">
          <critical-circle :class="[{have_new_prompt: model.have_new_prompt}, 'model_crit_circle']" crit-level="critical"></critical-circle>
          {{ model_name }}
        </rounded-container>

        <model-description
          :Alerts="get_alerts(model['prompts']) || 'Нет данных'"
          :RiskLevel="model.risk_level || 'Нет данных'"
          :ApiCalls="model.api_calls || 'Нет данных'"
          :Uptime="model.uptime || 'Нет данных'"
          :Latency="model.latency || 'Нет данных'"
          class="models_article"
        />
      </nuxt-link>
    </div>
  </div>
</template>

<style scoped>
.page_container {
  min-height: 100vh;
  width: calc(100% - 67px);
  padding-top: 25px;
  box-sizing: border-box;
}

.page_header {
  margin: 0;
  font-size: 26px;
  margin-bottom: 47px;
}

.models_content {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 20px;
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
  gap: 10px;
}

.models_article {
  background: transparent;
  margin-top: 25px;
  height: 280px;
  width: 100%;
}

.models_link {
  flex-basis: calc(50% - 50px);
  text-decoration: none;
  color: inherit;
}

.models_link:hover .models_button,
.models_link:hover .models_article{
  background: rgb(37, 28, 78);
  background: linear-gradient(90deg, rgba(37, 28, 78, 1) 0%, rgba(105, 80, 175, 1) 100%);
}

.model_crit_circle {
  opacity: 0;
}

.have_new_prompt {
  opacity: 1 !important;
}



@media (max-width: 1000px) {
  .models_content {
    row-gap: 40px;
    margin-bottom: 20px;
  }

  .models_link {
    flex-basis: 100%;
  }
}

@media (max-width: 431px) {

}
</style>
