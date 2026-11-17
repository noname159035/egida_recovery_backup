<script setup>
import { ref, onMounted, defineProps, defineEmits, watch} from 'vue';

const props = defineProps({
  mode: {
    type: Boolean,
    required: true
  }
});

const emit = defineEmits(['update:mode']);

const active = ref(props.mode);
const elF = ref(null);
const elS = ref(null);

watch(() => props.mode, (newValue) => {
  active.value = newValue;
});

function do_switch() {
  if (active.value) {
    elF.value.style.borderColor = 'transparent';
    elF.value.querySelector('.bg-overlay').style.opacity = 0;

    elS.value.style.borderColor = 'var(--border_color)';
    elS.value.querySelector('.bg-overlay').style.opacity = 1;

    active.value = false;
  } else {
    elS.value.style.borderColor = 'transparent';
    elS.value.querySelector('.bg-overlay').style.opacity = 0;

    elF.value.style.borderColor = 'var(--border_color)';
    elF.value.querySelector('.bg-overlay').style.opacity = 1;

    active.value = true;
  }

  emit('update:mode', active.value);
}

onMounted(() => {
  if (elF.value && elS.value) {
    elF.value.style.borderColor = 'var(--border_color)';
    elF.value.querySelector('.bg-overlay').style.opacity = 1;
    elS.value.style.borderColor = 'transparent';
    elS.value.querySelector('.bg-overlay').style.opacity = 0;
  }
});
</script>

<template>
  <rounded-container class="switcher_container">
    <div ref="elF" @click="do_switch" id="first_elem" class="switcher_element">
      <div class="bg-overlay"></div>
      <div class="switcher_element_inner">
        <slot name="first"></slot>
      </div>
    </div>
    <div ref="elS" @click="do_switch" id="second_elem" class="switcher_element">
      <div class="bg-overlay"></div>
      <div class="switcher_element_inner">
        <slot name="second"></slot>
      </div>
    </div>
  </rounded-container>
</template>

<style scoped>
.switcher_container {
  display: flex;
  padding: 5px;
  background: linear-gradient(86deg, var(--switcher_background_start) 22.67%, var(--switcher_background_end) 61.74%);
  border-radius: 35px;
  justify-content: space-between;
}

.switcher_element {
  padding: 5px;
  width: 43%;
  position: relative;
  border: solid 2px transparent;
  border-radius: 10px;
  background: transparent;
  transition: border-color 0.15s ease-in-out;
  border-radius: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.bg-overlay {
  z-index: 2;
  position: absolute;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(79deg, #151325 26.69%, #321F3E 62.71%);
  opacity: 0;
  transition: opacity 0.15s ease-in-out;
  pointer-events: none;
  border-radius: 30px;
}

.switcher_element_inner {
  cursor: pointer;
  position: relative;
  z-index: 2;
  display: flex;
  gap: 10px;
  align-items: center;
  width: 100%;
  justify-content: center;
}


</style>
