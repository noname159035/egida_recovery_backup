<script setup>
import { ref, onMounted, computed, nextTick } from 'vue';
import MainHeader from "~/components/mainHeader.vue";
import ColoredButton from "~/components/coloredButton.vue";
import axios from 'axios';
import { useAuthStore } from '~/store/auth';
import { useRouter, useRoute } from 'vue-router';
import { useRuntimeConfig } from '#app';
import { useDeviceStore } from "~/store/device.js";
import monitorsSrc from '@/assets/monitors.png'

const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();

definePageMeta({
  layout: 'empty'
})

const switch_mode = ref(true);

const showLoginModal    = ref(false)
const showRegisterModal = ref(false)
const showMobileModal = ref(false)

const device = useDeviceStore()
const isMobile = computed(() => device.isMobile)

const email_ref = ref('');

function openLoginModal()    { showLoginModal.value = true }
function closeLoginModal()   { showLoginModal.value = false }
function openRegisterModal() { showRegisterModal.value = true }
function closeRegisterModal(){ showRegisterModal.value = false }
function openMobileModal() { showMobileModal.value = true }
function closeMobileModal(){ showMobileModal.value = false }

const showImage = ref(false);

async function registration() {
  const name = document.querySelector("#reg_name");
  const surname = document.querySelector("#reg_surname");
  const email = document.querySelector("#reg_email");
  const comp_name = document.querySelector("#reg_corp_name");
  const politics_status = document.querySelector("#politics_checkbox").checked;

  const payload = {
    first_name: name.value,
    second_name: surname.value,
    email: email.value,
    company_name: comp_name.value,
  };

  if (politics_status && input_is_valid(name) && input_is_valid(surname) && input_is_valid(email) && input_is_valid(comp_name)) {
    try {
      const runtimeConfig = useRuntimeConfig();
      const response = await axios.post(`${runtimeConfig.public.apiUrl}/register`, payload);
      const test_buffer = document.querySelector("#test_token");
      test_buffer.innerText = response.data.token;
      console.log("Ваш токен: ", response.data.token);
      closeRegisterModal();
    } catch (err) {
      console.error(err);
    }
  } else {
    document.querySelector("#politics_checkbox_visible").style.borderColor = "red";
  }
}

async function authorization() {
  console.log("Авторизация...")
  const email = document.querySelector("#auth_email").value;
  const tokenInput = document.querySelector("#auth_token").value;

  if (!email || !tokenInput) {
    console.error("Email and token are required");
    return;
  }

  const payload = { email, token: tokenInput };

  try {
    const runtimeConfig = useRuntimeConfig();
    const response = await axios.post(`${runtimeConfig.public.apiUrl}/login`, payload);

    const receivedToken = response.data.access_token;
    const userName = response.data.first_name;

    if (!receivedToken) {
      console.error("No token received from server");
      return;
    }

    // Update store first
    authStore.setToken(receivedToken);
    authStore.setUserName(userName);

    // Wait for store update
    await nextTick();
    
    // Close modal after store update
    closeLoginModal();
    
    // Small delay to ensure everything is updated
    await new Promise(resolve => setTimeout(resolve, 100));
    
    // Navigate last
    await router.push('/prompts');
    
    console.log("Login successful");
  } catch (err) {
    // console.error("Login error:", err);
    // const errorMsg = err.response?.data?.detail || "Login failed. Please try again.";
    // document.getElementById("auth_test_token").textContent = errorMsg;
  }
}

function input_is_valid(obj) {
  return true
}

onMounted(() => {
  showImage.value = true
})
</script>

<template>
  <div class="page_container">
    <mainHeader
      v-if="!isMobile"
      class="main_page_header"
      :modal-function-auth="openLoginModal"
      :modal-function-reg="openRegisterModal"
    >
    </mainHeader>
    <mobile-main-header v-if="isMobile" @open-mobile-modal="openMobileModal"></mobile-main-header>
    <main class="main_page_container">
      <transition name="modal" appear v-if="isMobile">
          <modal-input class="modal_reg_container modal_mobile" v-if="showMobileModal" @close="closeMobileModal">
            <switcher class="user_switcher" v-model:mode="switch_mode">
              <template #first class="user_switcher_element">
                <p class="main_text user_switcher_text swicher_test" @click="change_mode($event.target)">Регистрация</p>
              </template>
              <template #second class="user_switcher_element">
                <p class="main_text user_switcher_text swicher_example" @click="change_mode($event.target)">Вход</p>
              </template>
            </switcher>
            <div class="main_text mobile_modal_reg" v-if="switch_mode">
              <div class="modal_try_demo_input_fio_container">
                <div>
                  <p class="main_text modal_try_demo_title">Имя</p>
                  <input required id="reg_name" type="text" placeholder="Иван" class="modal_try_demo_input main_text">
                </div>
                <div>
                  <p class="main_text modal_try_demo_title">Фамилия</p>
                  <input required id="reg_surname" type="text" placeholder="Иванов" class="modal_try_demo_input main_text">
                </div>
              </div>
              <div class="modal_try_demo_input_data_container">
                <p class="main_text modal_try_demo_title">Корпоративный email</p>
                <input
                    required
                    id="reg_email"
                    type="text"
                    placeholder="Email"
                    class="modal_try_demo_input main_text"
                />
              </div>
              <div class="modal_try_demo_input_data_container">
                <p class="main_text modal_try_demo_title">Название компании</p>
                <input required id="reg_corp_name" type="text" placeholder="Иван и Ко" class="modal_try_demo_input main_text">
              </div>
              <div class="modal_try_demo_input_checkbox_container">
                <label class="modal_try_demo_input_checkbox">
                  <input id="politics_checkbox" type="checkbox" />
                  <span id="politics_checkbox_visible" class="modal_try_demo_input_checkbox_elem"></span>
                </label>
                <span class="main_text modal_try_demo_input_checkbox_text">Согласен с </span>
                <nuxt-link to="/userAgreement" class="main_text modal_try_demo_input_checkbox_text">Политикой персональных данных</nuxt-link>
              </div>
              <p id="test_token" class="main_text">Токен будет направлен на ваш Email адрес</p>
              <colored-button-center class="btn_get_demo" @click="registration">
                <p>Получить Токен</p>
              </colored-button-center>
            </div>
            <div class="main_text mobile_modal_reg mobile_modal_auth" v-if="!switch_mode">
              <div>
                <p class="main_text modal_try_demo_title">Email</p>
                <input
                    required
                    id="auth_email"
                    type="text"
                    placeholder="ivan@gmail.com"
                    class="modal_try_demo_input main_text"
                    v-model="email_ref"
                />
              </div>
              <div>
                <p class="main_text modal_try_demo_title">Токен</p>
                <input required id="auth_token" type="text" placeholder="Токен" class="modal_try_demo_input main_text">
              </div>
              <p id="auth_test_token"></p>
              <colored-button-center class="btn_get_demo" @click="authorization">
                <p>Войти</p>
              </colored-button-center>
            </div>
          </modal-input>
      </transition>
      <transition name="modal" appear>
        <modal-input class="modal_reg_container" v-if="showLoginModal" @close="closeLoginModal">
          <h4 class="main_text modal_reg_title">Вход</h4>
          <div>
            <p class="main_text modal_try_demo_title">Email</p>
            <input
              required
              id="auth_email"
              type="text"
              placeholder="ivan@gmail.com"
              class="modal_try_demo_input main_text"
              v-model="email_ref"
            />
          </div>
          <div>
            <p class="main_text modal_try_demo_title">Токен</p>
            <input required id="auth_token" type="text" placeholder="Токен" class="modal_try_demo_input main_text">
          </div>
          <p id="auth_test_token"></p>
          <colored-button-center class="btn_get_demo" @click="authorization">
            <p>Войти</p>
          </colored-button-center>
        </modal-input>
      </transition>
      <h2 class="main_text main_top_title">Проверьте безопасность своей <br> LLM-модели</h2>
      <h3 v-if="!isMobile" class="main_text main_page_reg_title">Быстрая интеграция</h3>
      <coloredButton v-if="!isMobile" class="main_page_try_demo">
        <input :value="email_ref" required type="text" class="main_text main_page_try_demo__input" placeholder="Введите свой email">
        <colored-button-center class="main_page_try_demo_btn" id="get_demo_btn" @click="openRegisterModal">
          <p id="get_demo_btn_text">Попробовать демо</p>
          <svg id="get_demo_btn_svg" width="30" height="30" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="1" y="1" width="28" height="28" rx="14" stroke="white" stroke-width="2"/>
            <line y1="-0.75" x2="13.1794" y2="-0.75" transform="matrix(0.630904 0.775861 -0.630904 0.775861 6 11.7744)" stroke="white" stroke-width="1.5"/>
            <line y1="-0.75" x2="13.1794" y2="-0.75" transform="matrix(-0.630904 0.775861 -0.630904 -0.775861 22 11)" stroke="white" stroke-width="1.5"/>
          </svg>
        </colored-button-center>
      </coloredButton>
      <transition name="modal" appear>
        <modal-input v-if="showRegisterModal" class="modal_try_demo_container" @close="closeRegisterModal">
          <div class="modal_try_demo_input_fio_container">
            <div>
              <p class="main_text modal_try_demo_title">Имя</p>
              <input required id="reg_name" type="text" placeholder="Иван" class="modal_try_demo_input main_text">
            </div>
            <div>
              <p class="main_text modal_try_demo_title">Фамилия</p>
              <input required id="reg_surname" type="text" placeholder="Иванов" class="modal_try_demo_input main_text">
            </div>
          </div>
          <div class="modal_try_demo_input_data_container">
            <p class="main_text modal_try_demo_title">Корпоративный email</p>
            <input
              required
              id="reg_email"
              type="text"
              placeholder="Email"
              class="modal_try_demo_input main_text"
            />
          </div>
          <div class="modal_try_demo_input_data_container">
            <p class="main_text modal_try_demo_title">Название компании</p>
            <input required id="reg_corp_name" type="text" placeholder="Иван и Ко" class="modal_try_demo_input main_text">
          </div>
          <div class="modal_try_demo_input_checkbox_container">
            <label class="modal_try_demo_input_checkbox">
              <input id="politics_checkbox" type="checkbox" />
              <span id="politics_checkbox_visible" class="modal_try_demo_input_checkbox_elem"></span>
            </label>
            <span class="main_text modal_try_demo_input_checkbox_text">Согласен с </span>
            <nuxt-link to="/userAgreement" class="main_text modal_try_demo_input_checkbox_text">Политикой персональных данных</nuxt-link>
          </div>
          <p id="test_token" class="main_text">Токен будет направлен на ваш Email адрес</p>
          <colored-button-center class="btn_get_demo" @click="registration">
            <p>Получить Токен</p>
          </colored-button-center>

        </modal-input>
      </transition>

      <p v-if="showImage" class="main_text"></p>
      <img
        v-if="!isMobile"
        :src="monitorsSrc"
        class="main_page_monitor"
        alt="Мониторы"
      />

      <div v-if="!isMobile" class="main_page_circle_container main_text">
        <article class="main_page_circle__text_container">
          <div class="main_page_circle__text_title_container">
            <svg class="main_page_circle__text_title_image" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect width="80" height="80" rx="40" fill="url(#paint0_radial_2448_10)"/>
              <line x1="24.7071" y1="39.2929" x2="35.3137" y2="49.8995" stroke="white" stroke-width="2"/>
              <line x1="34.2929" y1="49.5058" x2="55.5061" y2="28.2926" stroke="white" stroke-width="2"/>
              <defs>
                <radialGradient id="paint0_radial_2448_10" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(40 40) rotate(90) scale(40)">
                  <stop offset="0.245" stop-color="#080813"/>
                  <stop offset="0.645" stop-color="#231D3F"/>
                  <stop offset="0.875" stop-color="#52428C"/>
                  <stop offset="0.985" stop-color="#8E7CD1"/>
                </radialGradient>
              </defs>
            </svg>
            <h4 class="main_page_circle__text_title">Автоматическая детекция и блокировка атак</h4>
          </div>
          <p class="main_page_circle__text_content">Наши алгоритмы детектируют промпт инъектирующие запросы и блокируют их, не позволяя злоумышленникам манипулировать LLM-моделью.</p>
        </article>
        <article class="main_page_circle__text_container">
          <div class="main_page_circle__text_title_container">
            <svg class="main_page_circle__text_title_image" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect width="80" height="80" rx="40" fill="url(#paint0_radial_2448_10)"/>
              <line x1="24.7071" y1="39.2929" x2="35.3137" y2="49.8995" stroke="white" stroke-width="2"/>
              <line x1="34.2929" y1="49.5058" x2="55.5061" y2="28.2926" stroke="white" stroke-width="2"/>
              <defs>
                <radialGradient id="paint0_radial_2448_10" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(40 40) rotate(90) scale(40)">
                  <stop offset="0.245" stop-color="#080813"/>
                  <stop offset="0.645" stop-color="#231D3F"/>
                  <stop offset="0.875" stop-color="#52428C"/>
                  <stop offset="0.985" stop-color="#8E7CD1"/>
                </radialGradient>
              </defs>
            </svg>
            <h4 class="main_page_circle__text_title">Непрерывный мониторинг</h4>
          </div>
          <p class="main_page_circle__text_content">Система непрерывно отслеживает угрозы, предупреждая о потенциальных проблемах безопасности.</p>
        </article>
        <article class="main_page_circle__text_container">
          <div class="main_page_circle__text_title_container">
            <svg class="main_page_circle__text_title_image" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect width="80" height="80" rx="40" fill="url(#paint0_radial_2448_10)"/>
              <line x1="24.7071" y1="39.2929" x2="35.3137" y2="49.8995" stroke="white" stroke-width="2"/>
              <line x1="34.2929" y1="49.5058" x2="55.5061" y2="28.2926" stroke="white" stroke-width="2"/>
              <defs>
                <radialGradient id="paint0_radial_2448_10" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(40 40) rotate(90) scale(40)">
                  <stop offset="0.245" stop-color="#080813"/>
                  <stop offset="0.645" stop-color="#231D3F"/>
                  <stop offset="0.875" stop-color="#52428C"/>
                  <stop offset="0.985" stop-color="#8E7CD1"/>
                </radialGradient>
              </defs>
            </svg>
            <h4 class="main_page_circle__text_title">Консультации по безопасности AI-моделей</h4>
          </div>
          <p class="main_page_circle__text_content">Эксперты предоставляют рекомендации по настройке моделей для повышения их безопасности и соответствия стандартам.</p>
        </article>
      </div>
      <div v-if="isMobile" class="main_page_mobile__container">
        <colored-button class="main_page_mobile__btn_try main_text" @click="openMobileModal">Попробовать демо</colored-button>
        <img src="~/public/main_mobile.png" class="main_page_mobile__image" alt="Изображение мониторов">
      </div>
    </main>
  </div>
</template>

<style scoped>

.page_container {
  height: 100%;
  padding: 30px 0px 0px 0px;
}

.main_page_header {
  z-index: 100;
}

.main_page_container {
  display: flex;
  flex-direction: column;
  width: 100%;
  align-items: center;
}

.main_top_title {
  z-index: 100;
  max-width: 985px;
  font-size: 60px;
  text-align: center;
  justify-self: center;
  font-weight: 900;
  margin-bottom: 70px;
}

.main_page_reg_title {
  z-index: 100;
  text-align: center;
  font-size: 20px;
  margin-bottom: 25px;
}

.main_page_try_demo {
  z-index: 100;
  width: 600px;
  max-width: 100%;
  border-radius: 43px;
  display: flex;
  justify-content: space-between;
  padding: 10px 10px 10px 40px !important;
  box-sizing: content-box;
  margin-bottom: 20px;
}

.main_page_try_demo__input {
  border: none;
  background: transparent;
  outline: none;
  width: 50%;
  font-size: 20px;
}

.main_page_try_demo__input::placeholder {
  font-family: "NunitoSans";
  color: var(--main_text_selected);
  font-size: 20px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
}

.main_page_try_demo__input:focus::placeholder {
  color: transparent;
}

.main_page_try_demo_btn {
  cursor: pointer;
  width: 240px;
  display: flex;
  justify-content: space-between;
  padding: 15px 20px 15px 30px !important;
  transition: transform 0.1s ease-in-out;
}

.main_page_try_demo_btn:hover {
  transform: scale(1.015);
}

.main_page_try_demo_btn:active {
  transition: transform 0.01s ease-in-out;
  transform: scale(1.03);
}

.modal_background {
  width: 100%;
  height: 100vh;
  background: black;
  opacity: 0.5;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 0;
  cursor: pointer;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.modal_try_demo_container {
  box-sizing: border-box;
  padding: 0 25px;
}

.modal_try_demo_input_fio_container {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  width: 100%;
}

.modal_try_demo_input_data_container {
  width: 100%;
}

.modal_try_demo_input_checkbox_container {
  display: flex;
  align-items: center;
  width: 100%;
}

.modal_try_demo_input_checkbox_container input[type="checkbox"] {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.modal_try_demo_input_checkbox_elem {
  width: 30px;
  height: 30px;
  border: 2px solid #aaa;
  border-radius: 6px;
  display: inline-block;
  position: relative;
  cursor: pointer;
  vertical-align: middle;
  margin-right: 20px;
}

.modal_try_demo_input_checkbox_container input[type="checkbox"]:checked + .modal_try_demo_input_checkbox_elem::after {
  content: "";
  position: absolute;
  left: 38%;
  top: 18%;
  width: 6px;
  height: 12px;
  border: solid #aaa;         /* цвет и толщина линий галочки */
  border-width: 0 2px 2px 0;  /* правый и нижний бордеры */
  transform: rotate(45deg);   /* поворачиваем, чтобы был вид галочки */
}

.modal_try_demo_input_checkbox_text {
  font-size: 20px;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

.modal_try_demo_input_checkbox_text:nth-child(3) {
  cursor: pointer;
  text-decoration: underline;
  margin-left: 9px;
}


.modal_try_demo_title {
  font-size: 24px;
  font-weight: 400;
  margin-bottom: 10px;
}

.modal_try_demo_input {
  border-radius: 20px;
  border: 1px solid var(--input_color);
  opacity: 0.5;
  background: transparent;
  height: 44px;
  width: 96%;
  padding-left: 22px;
  color: #8E8D9D;
  font-size: 20px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
  outline: none;
}

.modal_try_demo_input:focus {
  color: white;
}

.btn_get_demo {
  margin-top: auto;
  cursor: pointer;
  align-self: center;
  display: flex;
  justify-content: center;
  width: 250px;
  height: 60px;
  transition: transform 0.05s ease-in-out;
}

.btn_get_demo:hover {
  transform: scale(1.02);
}

.btn_get_demo:active {
  transition: transform 0.01s ease-in-out;
  transform: scale(1.04);
}

.modal_reg_container {
  position: fixed;
  z-index: 999;
  top: 0%;
  width: 100%;
  display: flex;
}

.modal_reg_title {
  font-size: 24px;
  align-self: center;
  margin-bottom: 20px;
}

.main_page_monitor {
  width: 90%;
  margin-bottom: 100px;
}



.main_page_circle_container {
  display: flex;
  flex-direction: column;
  background: radial-gradient(50.06% 50.59% at 50% 50%, #3F3073 8.5%, #251C4E 53%, #1D173E 65%, #080813 100%);
  width: 100%;
  align-items: center;
  margin-bottom: 60px;
}

.main_page_circle__text_container {
  width: 60vw;
  margin-bottom: 40px;
  border-radius: 30px;
  border: 0.5px solid #4A4A4E;
  background: radial-gradient(116.12% 104.23% at 50% 50%, #090914 23.39%, #0D0D16 31.17%, #0C0C16 35.43%, #29292F 84%, #707070 100%);
  box-shadow: 0px 4px 4px 0px rgba(0, 0, 0, 0.25) inset;
  padding: 20px 40px 30px 40px;
  box-sizing: border-box;
}

.main_page_circle__text_title_container {
  display: flex;
  gap: 45px;
  flex: 1;
  align-items: center;
  margin-bottom: 30px;
}

.main_page_circle__text_title_image {
  width: 80px;
  height: 80px;
}

.main_page_circle__text_title {
  font-size: 30px;
  font-weight: 600;
  line-height: normal;
  margin-bottom: 10px;
  flex: 1;
}

.main_page_circle__text_content {
  font-size: 25px;
  font-weight: 400;
  line-height: normal;
}



@media (max-width: 860px) {
  .modal_try_demo_input_fio_container {
    flex-direction: column;
    row-gap: 20px;
  }
}

@media (max-width: 700px) {
  .main_top_title {
    font-size: 30px;
  }

  .main_page_circle__text_container {
    width: 100%;
  }

  .main_page_monitor {
    display: none;
  }

  .main_page_header {
    margin-bottom: 40px;
  }

  .main_page_circle__text_title_container {
    gap: 15px;
  }

  .main_page_circle__text_title {
    font-size: 20px;
  }

  .main_page_circle__text_content {
    font-size: 16px;
  }

  .main_page_circle__text_title_image {
    width: 60px;
    height: 60px;
    min-width: 30px;
    min-height: 30px;
  }

  .main_page_try_demo__input {
    font-size: 15px;
  }

  .main_page_try_demo__input::placeholder {
    font-size: 15px;
  }

  .main_page_circle_container {
    margin-top: 20px;
  }

  #get_demo_btn_text {
    font-size: 14px;
  }

  .modal_try_demo_input_checkbox_text {
    font-size: 16px;
    text-wrap: nowrap;
  }

  .modal_try_demo_input_checkbox_text:nth-child(3) {
    text-overflow: ellipsis;
    overflow-x: hidden;
  }
}

@media (max-width: 431px) {
  .main_top_title {
    font-size: 30px;
  }
  .main_page_mobile__container {
    width: 100%;
    display: flex;
    flex-direction: column;
  }

  .main_page_mobile__btn_try {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0 20%;
    margin-bottom: 50px;
    height: 45px;
    border-radius: 100px;
  }

  .main_page_mobile__image {
    margin-bottom: 40px;
  }

  .modal_mobile {
    .modal_try_demo_title {
      font-size: 13px;
    }

    .modal_try_demo_input {
      height: 30px;
      width: 100%;
    }
  }

  .mobile_modal_reg {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .mobile_modal_auth {
    width: 90%;
  }

  .modal_try_demo_input_checkbox_elem {
    width: 15px;
    height: 15px;
    margin-right: 5px;
  }

  .modal_try_demo_input_checkbox_container input[type="checkbox"]:checked + .modal_try_demo_input_checkbox_elem::after {
    content: "";
    position: absolute;
    left: 38%;
    top: 18%;
    width: 3px;
    height: 6px;
  }

  .modal_try_demo_input::placeholder {
    font-size: 15px;
  }

  .modal_try_demo_input_checkbox_text {
    margin-top: 4px;
    font-size: 13px;
  }

  #test_token {
    margin-top: 5px;
    margin-bottom: 5px;
    font-size: 13px;
  }

  .btn_get_demo {
    width: 180px;
    height: 40px;
  }

  .modal_try_demo_input {
    font-size: 15px;
  }
}
</style>
