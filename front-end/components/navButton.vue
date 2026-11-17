<template>
  <button
    class="nav_button"
    :class="{ nav_disabled: disable }"
    @click="emitButtonClick"
  >
    <div class="nav_button__svg">
      <slot/>
    </div>
    <p class="nav_button__text main_text">{{ text }}</p>
  </button>

</template>

<style scoped>
.nav_button {
  background-color: transparent;
  padding-left: 13px;
  outline: none;
  border: none;
  display: flex;
  align-items: center;
  height: 70px;
  column-gap: 32px;
  width: 100%;
  border-radius: 15px;
  transition: background-color 0.15s ease-in-out, background 0.15s ease-in-out, color 0.15s ease-in-out;

  .nav_button__text {
    line-height: 24px;
    color: var(--main_text_not_selected);
  }
}

.nav_button:hover {
  background: rgb(37, 28, 78);
  background: linear-gradient(90deg, rgba(37, 28, 78, 1) 0%, rgba(105, 80, 175, 1) 100%);
  color: var(--main_text_selected);
}

.nav_disabled {
  cursor: pointer;
  background: rgb(37, 28, 78);
  background: linear-gradient(90deg, rgba(37, 28, 78, 1) 0%, rgba(105, 80, 175, 1) 100%);
  color: var(--main_text_selected);

  .nav_button__svg,
  .nav_button__text {
    color: var(--main_text_selected);
    transform: translateX(5px);
    transition: transform 0.15s ease-in-out;
  }
}

.nav_disabled:hover {
  .nav_button__svg,
  .nav_button__text {
    color: var(--main_text_selected);
    transform: translateX(8px) !important;
    transition: transform 0.15s ease-in-out;
  }
}

.nav_disabled:active {
  .nav_button__svg,
  .nav_button__text {
    color: var(--main_text_selected);
    transform: translateX(10px) !important;
    transition: transform 0.15s ease-in-out;
  }
}

.nav_button__svg,
.nav_button__text {
  transition: transform 0.15s ease-in-out, color 0.15s ease-in-out;
}

.navbar_element:hover .nav_button__svg,
.navbar_element:hover .nav_button__text {
  color: var(--main_text_selected);
  transform: translateX(5px);
  transition: transform 0.15s ease-in-out;
}

.navbar_element:active .nav_button__svg,
.navbar_element:active .nav_button__text {
  transform: translateX(7px);
  transition: transform 0.05s ease-in-out;
}
</style>

<script>
export default {
  props: {
    text: String,
    disable: Boolean
  },
  methods: {
    emitButtonClick() {
      if (this.disable) {
        return;
      }
      this.$emit('click');

    },
  }
}
</script>
