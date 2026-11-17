<script setup>

</script>


<template>
  <rounded-container class="clicable_promt_rounded">
    <slot></slot>
  </rounded-container>
</template>

<style scoped>
.clicable_promt_rounded {
  text-align: center;
  transition: background 0.15s ease-in-out, transform 0.02s ease-in-out;
  cursor: pointer;
  color: var(--component_content_text);
}

.clicable_promt_rounded:hover {
  background: rgb(37,28,78);
  background: linear-gradient(90deg, rgba(37,28,78,1) 0%, rgba(105,80,175,1) 100%);
  color: var(--main_text_selected);
}

.clicable_promt_rounded:active {
  background-color: var(--simpe_button_color_active);
  transform: scale(1.015);
}
</style>
