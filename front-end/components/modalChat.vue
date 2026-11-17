<template>
  <transition name="modal-fade">
    <div class="modal" v-if="modelValue">
      <div class="modal-background" @click.self="closeModal"></div>
      <div class="modal-content">
        <slot></slot>
      </div>
    </div>
  </transition>
</template>

<script setup>
import {watch, toRef} from 'vue';

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
});

const emit = defineEmits(['update:modelValue']);

const closeModal = () => {
  // console.log("Закрытие модального окна");
  emit('update:modelValue', false);
};

const isModalOpen = toRef(props, 'modelValue');

watch(isModalOpen, (newVal) => {
  // console.log("Состояние модального окна:", newVal);
  document.body.style.overflowY = newVal ? 'hidden' : '';
});
</script>


<style scoped>

.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.2s;
}

.modal-fade-enter, .modal-fade-leave-to {
  opacity: 0;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.modal-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
}

.modal-content {
  display: flex;
  padding: 15px;
  width: 512px;
  height: 512px;
  background-color: var(--main_page_color);
  position: relative;
  animation: fade_modal 0.2s;
  border-radius: 14px;
}
</style>
