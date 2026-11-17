<script setup>

</script>


<template>
  <div class="request_block">
    <slot></slot>
  </div>
</template>

<style scoped>
.request_block {
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  border-bottom-right-radius: 10px;
  padding: 10px;
  word-wrap: break-word;
  background-color: var(--chat_block_color);
  width: auto;
  max-width: 43%;
  margin-right: auto;
}

</style>
