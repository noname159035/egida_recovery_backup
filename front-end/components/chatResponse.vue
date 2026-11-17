<script setup>

</script>


<template>
  <div class="response_block">
    <slot></slot>
  </div>
</template>

<style scoped>
.response_block {
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  border-bottom-left-radius: 10px;
  padding: 10px;
  word-wrap: break-word;
  background-color: var(--chat_block_color);
  max-width: 43%;
  width: auto;
  margin-left: auto;
}
</style>
