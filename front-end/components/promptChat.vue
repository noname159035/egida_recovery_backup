<script setup>
import {toRefs} from "vue";
import {useNuxtApp} from "#app";
import {watch} from "vue";
import {useRouter} from 'vue-router';

const {$axios} = useNuxtApp();

const router = useRouter();

const props = defineProps({
  prompt: {
    type: Object,
    required: true,
  },
});
const {prompt} = toRefs(props);

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

// console.log("Модальное окно получило: ", prompt.value)

</script>

<template>
  <div class="modal_main_container">
    <h3 class="modal_title modal_main_title main_text">Information</h3>
    <h4 class="modal_title main_text">
      <span>Chain ID: </span>
      <span>{{ prompt.chain_id }}</span>
    </h4>
    <h4 class="modal_title main_text">
      <span>Timestamp: </span>
      <span>{{ formatDate(prompt.timestamp) }}</span>
    </h4>
    <h4 class="modal_title main_text">
      <span>Toolcall ID: </span>
      <span>{{ prompt.toolcall_id }}</span>
    </h4>
    <h4 class="modal_title main_text">
      <span>Status: </span>
      <span>{{ prompt.Status }}</span>
    </h4>
    <rounded-container class="modal_chat">
      <div class="modal_chat_header modal_title modal_chat_title main_text">{{ prompt.type }}</div>

      <scroll-chat :chat="prompt.chat_history"></scroll-chat>

      <div class="modal_chat_footer">
        <nuxt-link class="modal_more_info_btn main_text" :to="{
          name: 'dashboard-model_name-logs',
          query: { session_id: prompt.session_id },
          params: { model_name: $route.params.model_name },
          }">
          Подробнее
        </nuxt-link>

        <div class="modal_chat_footer_swapper">
          <svg class="modal_chat_footer_swapper_btn" width="17" height="18" viewBox="0 0 17 18" fill="none"
               xmlns="http://www.w3.org/2000/svg">
            <line y1="-1" x2="16.5571" y2="-1" transform="matrix(-0.876907 0.480661 0.580355 0.814364 16 2)"
                  stroke="#8E8D9D" stroke-width="2"/>
            <path d="M15.5191 17L1.00004 9.04166" stroke="#8E8D9D" stroke-width="2"/>
          </svg>


          <svg class="modal_chat_footer_swapper_btn" width="17" height="18" viewBox="0 0 17 18" fill="none"
               xmlns="http://www.w3.org/2000/svg">
            <line y1="-1" x2="16.5571" y2="-1" transform="matrix(0.876907 0.480661 -0.580355 0.814364 1 2)"
                  stroke="#8E8D9D" stroke-width="2"/>
            <path d="M1.48093 17L16 9.04166" stroke="#8E8D9D" stroke-width="2"/>
          </svg>
        </div>
      </div>
    </rounded-container>
  </div>
</template>


<style scoped>
.modal_main_container {
  display: flex;
  flex-direction: column;
  height: 100%;
  flex: 1;
}

.modal_title {
  font-size: 20px;
}

.modal_title:not(:last-of-type) {
  margin-bottom: 10px;
}

.modal_main_title {
  color: var(--main_text_selected);
  font-size: 28px;
  margin-bottom: 16px;
}

.modal_chat {
  border-color: var(--chat_border_color);
  display: flex;
  flex-direction: column;
  padding: 0;
  height: 100%;
  margin-top: 15px;
  max-height: 315px;
  border: none;
}

.modal_chat_header {
  display: flex;
  text-align: center;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
  border-top-right-radius: 16px;
  border-top-left-radius: 16px;
  height: 30px;
  background: linear-gradient(90deg, #251C4E 0%, #6950AF 100%);
}

.modal_chat_title {
  font-size: 14px;
  color: var(--main_text_selected);
}

.modal_chat_footer {
  padding-right: 22px;
  padding-left: 22px;
  align-items: center;
  display: flex;
  box-sizing: border-box;
  background: linear-gradient(90deg, #251C4E 0%, #6950AF 100%);
  margin-top: auto;
  border-bottom-right-radius: 16px;
  border-bottom-left-radius: 16px;
  height: 30px;
}

.description_btn {
  cursor: pointer;
  transition: transform 0.05s ease-in-out;
}

.description_btn:hover {
  transform: scale(1.03);
}

.description_btn:active {
  transform: scale(1.05);
}

.modal_chat_footer_swapper {
  margin-left: auto;
  display: flex;
  column-gap: 25px;
}

.modal_more_info_btn {
  text-decoration: none;
}

.modal_chat_footer_swapper_btn {
  cursor: pointer;
  transition: transform 0.05s ease-in-out;
}

.modal_chat_footer_swapper_btn:hover {
  transform: scale(1.05);
}

.modal_chat_footer_swapper_btn:active {
  transform: scale(1.07);
}

.modal_chat_swapper {
  cursor: pointer;
  transition: transform 0.15s ease-in-out;
}

.modal_chat_swapper:hover {
  transform: scale(1.1);
}

.modal_chat_swapper:active {
  transform: scale(1.15);
}
</style>
