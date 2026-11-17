<script setup lang="ts">

</script>

<template>
  <button class="nav_user_button main_text link_to_user">
    <slot></slot>
  </button>
</template>

<style scoped>
.nav_user_button {
  gap: 15px;
  display: flex;
  background-color: transparent;
  border: none;
  outline: none;
  align-items: center;
  font-size: 16px;
  color: var(--main_text_selected);
  text-decoration: none;
}

.link_to_user {
  display: flex;
  border-radius: 100px;
  background: linear-gradient(90deg, #251C4E 0%, #6950AF 42.5%, #544091 82%, #31255F 92.5%);
  height: 60px;
  padding: 10px 15px 10px 15px;
}
</style>

