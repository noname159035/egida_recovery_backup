<script setup>

</script>

<template>
  <div class="border_cont">
    <slot></slot>
  </div>
</template>


<style scoped>
  .border_cont {
    border: solid var(--border_color) 2px;
    border-radius: 20px;
    padding: 16px 21px 16px 21px;
    background-color: #131222;
  }
</style>
