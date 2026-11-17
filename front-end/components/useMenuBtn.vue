<script>
  export default {
    props: {
      text: String,
      disable: Boolean
    },
    methods: {
      emitButtonClick() {
        if (!this.disable) {
          this.$emit('click');
        }
      },
    }
  }
</script>

<template>
  <button class="using_models_nav_element main_text" :disabled="disable">{{ text }}</button>
</template>


<style scoped>
.using_models_nav_element {
  cursor: pointer;
  flex: 1;
  max-width: 70px;
  border: none;
  color: var(--component_content_text);
  background: none;
  text-align: start;
  padding: 0;
  padding-right: 10px;
  box-sizing: content-box;
}

.using_models_nav_element:disabled {
  border-bottom: solid 1px var(--main_text_not_selected);
}

@media (max-width: 430px) {
  .using_models_nav_element {
    font-size: 10px;
  }
}
</style>
