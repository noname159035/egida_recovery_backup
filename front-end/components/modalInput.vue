<script setup lang="ts">
</script>

<template>
  <transition name="modal">
    <div class="modal-overlay" @click="$emit('close')">
      <div class="modal_try_demo" @click.stop>
        <slot />
      </div>
    </div>
  </transition>
</template>

<style scoped>
/* Затухание оверлея */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
.modal-enter-to,
.modal-leave-from {
  opacity: 1;
}

/* Появление и увод окна */
.modal-enter-active .modal_try_demo,
.modal-leave-active .modal_try_demo {
  transition: transform 0.3s ease, opacity 0.3s ease;
}
.modal-enter-from .modal_try_demo,
.modal-leave-to .modal_try_demo {
  transform: translateY(20px) scale(0.9);
  opacity: 0;
}
.modal-enter-to .modal_try_demo,
.modal-leave-from .modal_try_demo {
  transform: translateY(0) scale(1);
  opacity: 1;
}

/* Сам оверлей */
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
}

.modal_try_demo {
  position: relative;
  display: flex;
  flex-direction: column;
  border-radius: 30px;
  background: linear-gradient(
    90deg,
    rgba(37, 28, 78, 1) 0%,
    rgba(105, 80, 175, 1) 100%
  );
  padding: 40px 45px 30px;
  width: 700px;
  max-width: 80%;
  gap: 25px;
  box-sizing: border-box;
}

@media (max-width: 431px) {
  .modal_try_demo {
    padding: 20px 25px 15px;
  }
}
</style>
