<script setup>
const props = defineProps({
  chat: {
    type: Object,
    required: true,
  },
});

// console.log("AAAAAAAAAAAAAAAAA", props.chat);
</script>


<template>
  <div class="chat_container">
    <div v-for="elem in props.chat" class="chat_req_resp">
      <chat-request v-if="elem.role == 'user'"><p class="main_text chat_text">{{ elem.content }}</p></chat-request>
      <chat-response v-else><p class="main_text chat_text">{{ elem.content }}</p></chat-response>
    </div>
  </div>
</template>

<style scoped>
.chat_text {
  color: var(--chat_text_color);
}

.chat_container {
  background-color: var(--modal_background);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  row-gap: 5px;
  overflow-y: auto;
  flex: 1;
  padding: 19px 7px 14px 7px;
}

.chat_req_resp {
  width: 100%;
  display: flex;
  flex-direction: column;
}
</style>
