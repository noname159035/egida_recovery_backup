<script setup>
import {defineProps, defineEmits, toRefs} from 'vue';

// Получаем пропсы
const props = defineProps({
  promptName: {type: String, required: true},
  promptClass: {type: String, required: true}
});

// Преобразуем пропсы в реактивные ссылки
const {promptName, promptClass} = toRefs(props);

// Определяем emit для передачи события в родительский компонент
const emit = defineEmits(["openModal"]);

// Функция для обработки клика и передачи данных в модальное окно
const handleClick = () => {
  const promptData = {prompt_text: promptName.value, severity: promptClass.value};
  // console.log("Передаём в openModal:", promptData);
  emit("openModal", promptData);
};
</script>

<template>
  <div class="prompt_element_container">
    <p class="prompt_text_name_class">{{ promptName }}</p>
    <p class="prompt_text_class">{{ promptClass }}</p>
    <button class="prompt_btn" @click="handleClick">
      <svg width="3" height="15" viewBox="0 0 3 15" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="1.5" cy="1.5" r="1.5" fill="#8E8D9D"/>
        <circle cx="1.5" cy="7.5" r="1.5" fill="#8E8D9D"/>
        <circle cx="1.5" cy="13.5" r="1.5" fill="#8E8D9D"/>
      </svg>
    </button>
  </div>
</template>

<style scoped>
.prompt_element_container, .prompt_left_container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: background-color 0.15s ease-in-out, background 0.15s ease-in-out;
}

.prompt_element_container {
  padding: 0px 56px 0px 15px;
  background: #17162B;
  height: 45px !important;
  gap: 20px;
  color: var(--component_content_text);
}

.prompt_btn {
  transition: color 0.15s ease-in-out, transform 0.15s ease-in-out;
}

.prompt_btn:hover {
  transform: scale(2);
}

.prompt_element_container:hover {
  background: rgb(37, 28, 78);
  background: linear-gradient(90deg, rgba(37, 28, 78, 1) 0%, rgba(105, 80, 175, 1) 100%);
  color: var(--main_text_selected);
}

.prompt_element_container:hover > .prompt_left_container > .prompt_btn {
  color: var(--main_text_selected);
}

.prompt_text_name_class {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 500px;
}

.prompt_left_container {
  display: flex;
  width: 369px;
}

.prompt_text_class {
  text-align: center;
  width: 66px;
}


.prompt_btn {
  cursor: pointer;
  background: none;
  outline: none;
  border: none;
  color: var(--main_text_not_selected);
  transition: transform 0.05s ease-in-out;
}

.prompt_btn:hover {
  transform: scale(1.05);
}

.prompt_btn:active {
  transform: scale(1.075);
}

@media (max-width: 1500px) {
  .prompt_text_name_class {
    max-width: 290px;
  }
}

@media (max-width: 1071px) {
  .prompt_text_name_class {
    max-width: 400px;
  }
}

@media (max-width: 650px) {
  .prompt_text_name_class {
    max-width: 200px;
  }
}


@media (max-width: 430px) {
  .prompt_btn {
    width: auto;
  }

  .prompt_element_container {
    padding-right: 10px;
    gap: 0;
  }

  .prompt_text_class, prompt_btn {
    width: auto;
  }

  .prompt_text_name_class {
    overflow: hidden;
    text-overflow: ellipsis;
    text-wrap: nowrap;
    max-width: 100px;
  }
}

</style>
