<script setup lang="js">
import axios from "axios";

const props = defineProps([
  'modalFunctionAuth',
  'modalFunctionReg'
]);

async function registration() {
  const name = document.querySelector("#reg_name").value;
  const surname = document.querySelector("#reg_surname").value;
  const email = document.querySelector("#reg_email").value;
  const comp_name = document.querySelector("#reg_corp_name").value;
  const politics_status = document.querySelector("#politics_checkbox").checked;

  const payload = {
    first_name: name,
    second_name: surname,
    email: email,
    company_name: comp_name,
  };

  if (politics_status) {
    try {
      const runtimeConfig = useRuntimeConfig();
      const response = await axios.post(`${runtimeConfig.public.apiBase}/register`, payload);

      console.log(data, pending, error);
    } catch (err) {
      console.error(err);
    }
  } else {
    document.querySelector("#politics_checkbox_visible").style.borderColor = "red";
  }
}
</script>

<template>
  <header class="main_header">
    <h1 class="main_text main_header__tite">EGIDA</h1>
    <nav class="main_header_nav">
<!--      <div class="main_header_nav__list">-->
<!--        <p class="main_text main_header_nav__text">что-то</p>-->
<!--        <svg width="13" height="6" viewBox="0 0 13 6" fill="none" xmlns="http://www.w3.org/2000/svg">-->
<!--          <path d="M1 0.5L6.29875 4.52706" stroke="white" stroke-width="1.5"/>-->
<!--          <line y1="-0.75" x2="7.36762" y2="-0.75" transform="matrix(-0.7759 0.630856 -0.7759 -0.630856 11 0)" stroke="white" stroke-width="1.5"/>-->
<!--        </svg>-->
<!--      </div>-->
<!--      <div class="main_header_nav__list">-->
<!--        <p class="main_text main_header_nav__text">функционал</p>-->
<!--        <svg width="13" height="6" viewBox="0 0 13 6" fill="none" xmlns="http://www.w3.org/2000/svg">-->
<!--          <path d="M1 0.5L6.29875 4.52706" stroke="white" stroke-width="1.5"/>-->
<!--          <line y1="-0.75" x2="7.36762" y2="-0.75" transform="matrix(-0.7759 0.630856 -0.7759 -0.630856 11 0)" stroke="white" stroke-width="1.5"/>-->
<!--        </svg>-->
<!--      </div>-->
<!--      <div class="main_header_nav__list">-->
<!--        <p class="main_text main_header_nav__text">команда</p>-->
<!--        <svg width="13" height="6" viewBox="0 0 13 6" fill="none" xmlns="http://www.w3.org/2000/svg">-->
<!--          <path d="M1 0.5L6.29875 4.52706" stroke="white" stroke-width="1.5"/>-->
<!--          <line y1="-0.75" x2="7.36762" y2="-0.75" transform="matrix(-0.7759 0.630856 -0.7759 -0.630856 11 0)" stroke="white" stroke-width="1.5"/>-->
<!--        </svg>-->
<!--      </div>-->
<!--      <nuxt-link class="main_text" to="/models" :key="$route.path">МОДЕЛИ (временная кнопка)</nuxt-link>-->
    </nav>
    <div class="main_header__auth_btns">
      <button class="main_header__auth_login main_text" id="modal_reg_btn_text" @click="props.modalFunctionAuth">Войти</button>
      <colored-button-center class="main_header__auth_get_token" @click="props.modalFunctionReg">
        <p class="main_header__auth_get_token_text">Получить токен</p>
      </colored-button-center>
    </div>
  </header>
</template>

<style scoped>
  .main_header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 100px;
  }

  .main_header__tite {
    width: 320px;
    font-size: 50px;
  }

  .main_header_nav {
    display: flex;
    align-items: center;
    gap: 30px;
  }

  .main_header_nav__list {
    display: flex;
    align-items: center;
    gap: 5px;
    cursor: pointer;
    transition: transform 0.1s ease-in-out;
  }

  .main_header_nav__list:hover {
    transform: scale(1.05);

  }

  .main_header_nav__list:active {
    transition: transform 0.01s ease-in-out;
    transform: scale(1.1);
  }

  .main_header_nav__text {
    font-size: 20px;
    user-select: none;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
  }

  .main_header__auth_btns {
    width: 320px;
    display: flex;
    gap: 30px;
  }

  .main_header__auth_login {
    border: none;
    background: none;
    font-size: 20px;
    cursor: pointer;
    transition: transform 0.1s ease-in-out;
  }

  .main_header__auth_login:hover {
    transform: scale(1.05);
  }

  .main_header__auth_login:active {
    transition: transform 0.01s ease-in-out;
    transform: scale(1.1);
  }

  .main_header__auth_get_token {
    width: 240px;
    padding: 16px 30px 16px 30px;
    font-size: 20px;
    height: 50px !important;
    cursor: pointer;
    transition: transform 0.1s ease-in-out;
  }

  .main_header__auth_get_token:hover {
    transform: scale(1.025);
  }

  .main_header__auth_get_token:active {
    transition: transform 0.01s ease-in-out;
    transform: scale(1.05);
  }

  .main_header__auth_get_token p {
    width: 100%;
    text-align: center;
  }

  @media (max-width: 700px) {
    .main_header {
      flex-direction: column;
      justify-content: center;
    }

    .main_header__tite {
      text-align: center;
    }
  }
</style>
