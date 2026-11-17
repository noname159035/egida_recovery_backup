<script setup lang="js">
import { useAsyncData, useNuxtApp, useRuntimeConfig } from '#app'
import { computed, onMounted, ref, reactive, nextTick } from 'vue'
import { useAuthStore } from '~/store/auth.js'
import { useDeviceStore } from '~/store/device.js'
import axios from 'axios'
import { useRoute } from 'vue-router'

const route        = useRoute()
const device       = useDeviceStore()
const isMobile     = computed(() => device.isMobile)
const key_list     = ref([])
const isDisabled   = ref(true)
const error_reason = ref('')
const showModal    = ref(false)

// состояние выпадающих списков
const expandedKeys = reactive({})
function isExpanded(id) {
  return !!expandedKeys[id]
}
function toggleKey(id) {
  expandedKeys[id] = !expandedKeys[id]
}

function openModal()  { showModal.value = true }
function closeModal() { showModal.value = false }

const { $axios }     = useNuxtApp()
const authStore      = useAuthStore()
const runtimeConfig  = useRuntimeConfig()

const editingKey = ref(null)
const editingValue = ref('')

async function init() {
  const { data, error } = await useAsyncData('api_keys', async () => {
    const token = authStore.getToken()
    const response = await $axios.get(
      `${runtimeConfig.public.apiUrl}/api_keys`,
      { headers: { Authorization: `Bearer ${token}` } }
    )
    response.data.api_keys.forEach(k => {
      if (k.last_used == null) k.last_used = 'Никогда'
    })
    key_list.value = response.data.api_keys
    return response.data
  })
  if (error.value) {
    error_reason.value = 'Не удалось загрузить ключи'
  }
}

async function add_key() {
  await useAsyncData('api_keys', async () => {
    const keyName = document.querySelector('#key_name_input').value
    const response = await $axios.post(
      `${runtimeConfig.public.apiUrl}/api_keys`,
      { key_name: keyName },
      { headers: { Authorization: `Bearer ${authStore.getToken()}` } }
    )
    await init()
    closeModal()
    return response.data
  })
}

function startEditing(key) {
  editingKey.value = key.api_key_id
  editingValue.value = key.key_name
  isDisabled.value = false
  nextTick(() => {
    const inp = document.querySelector(`#key-${key.api_key_id}`)
    if (inp) inp.focus()
  })
}

async function saveEdit() {
  if (!editingKey.value || !editingValue.value.trim()) return
  
  try {
    await axios.put(
      `${runtimeConfig.public.apiUrl}/api_keys/${editingKey.value}`,
      { key_name: editingValue.value.trim() },
      { headers: { Authorization: `Bearer ${authStore.getToken()}` } }
    )
    await init()
  } catch (error) {
    console.error('Failed to update key name:', error)
  } finally {
    editingKey.value = null
    editingValue.value = ''
    isDisabled.value = true
  }
}

function cancelEdit() {
  editingKey.value = null
  editingValue.value = ''
  isDisabled.value = true
  init()
}

async function deleteKey(apiKeyId) {
  await axios.delete(
    `${runtimeConfig.public.apiUrl}/api_keys/${apiKeyId}`,
    { headers: { Authorization: `Bearer ${authStore.getToken()}` } }
  )
  await init()
}

function copyText(event) {
  const txt = event.target.innerText
  navigator.clipboard.writeText(txt).then(
    () => alert('Ключ скопирован'),
    () => {}
  )
}

async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text)
    alert('Ключ сохранен в буфер обмена');
  } catch (err) {
    console.error('Не удалось скопировать текст:', err)
  }
}


onMounted(() => {
  route.meta.layout = 'navlayout-colorless'
  init()
})
</script>

<template>
  <div class="page_container">
    <div v-if="error_reason" class="error main_text">
      Ошибка загрузки: {{ error_reason }}
    </div>
    <div v-else>
      <div class="page_header_container">
        <h1 class="page_header main_text">API</h1>
        <rounded-button class="api_add_btn" @click="openModal">
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="8" width="1.3" height="18" rx="0.65" fill="#5C5A67"/>
            <rect y="8" width="18" height="1.3" rx="0.65" fill="#5C5A67"/>
          </svg>
          <p class="main_text">Создать новый API key</p>
        </rounded-button>
      </div>

      <div class="api_main__container">
        <rounded-container class="api_main__element api_docs__container">
          <h2 class="main_text api_main__element_title">Документация</h2>
          <p class="main_text api_docs__text">Чтобы начать пользоваться API, выполните три простых шага:</p>
          <p class="main_text api_docs__text">
            <strong>1. Создайте API ключ</strong><br>
            Перейдите в раздел управления ключами, нажмите «Создать ключ» и укажите любое понятное название (например, Telegram-bot). Скопируйте получившуюся строку.
          </p>
          <p class="main_text api_docs__text">
            <strong>2. Добавьте ключ в заголовок запроса</strong><br>
            При каждом запросе в HTTP заголовке Authorization передавайте ваш ключ в формате<br>
            <code>Authorization: Bearer &lt;ВАШ_API_КЛЮЧ&gt;</code>
          </p>
          <p class="main_text api_docs__text">
            <strong>3. Отправьте POST запрос</strong><br>
            Все запросы отправляются на эндпоинт <code>https://secure-llm.auditory.ru/api/v1/llm-proxy</code> с заголовком Content-Type: application/json и телом в формате JSON.
          </p>
          <rounded-container class="api_docs__code">
            <p class="main_text">
              Пример на Python:<br>
              <code>
                import os<br>
                import requests<br><br>
                os.environ["API_KEY"] = "&lt;ВАШ_API_КЛЮЧ&gt;"<br>
                api_key = os.getenv("API_KEY")<br><br>
                url = "https://secure-llm.auditory.ru/api/v1/llm-proxy"<br>
                headers = {<br>
                &nbsp;&nbsp;"Authorization": f"Bearer {api_key}",<br>
                &nbsp;&nbsp;"Content-Type": "application/json"<br>
                }<br>
                data = {<br>
                &nbsp;&nbsp;"content": "Hello, World!",<br>
                &nbsp;&nbsp;"session_id": "session-1234",<br>
                &nbsp;&nbsp;"ts": "2025-04-30T15:27:41.240776+00:00",<br>
                &nbsp;&nbsp;"role": "user",<br>
                &nbsp;&nbsp;"llm": "gigachat",<br>
                &nbsp;&nbsp;"ip": "89.322.322.322"<br>
                &nbsp;&nbsp;"tokens": "456"<br>
                }<br><br>
                response = requests.post(url, headers=headers, json=data)<br>
                print("Статус:", response.status_code)<br>
                print("Ответ сервера:", response.json())
              </code>
            </p>
          </rounded-container>
          <rounded-container class="api_docs__code">
            <p class="main_text">
              Пример с помощью curl:<br>
              <code>
                export API_KEY="&lt;ВАШ_API_КЛЮЧ&gt;"<br><br>
                curl -X POST https://secure-llm.auditory.ru/api/v1/llm-proxy \<br>
                -H "Authorization: Bearer $API_KEY" \<br>
                -H "Content-Type: application/json" \<br>
                -d '{<br>
                &nbsp;&nbsp;"content": "Hello, World!",<br>
                &nbsp;&nbsp;"session_id": "session-1234",<br>
                &nbsp;&nbsp;"ts": "2025-04-30T15:27:41.240776+00:00",<br>
                &nbsp;&nbsp;"role": "user",<br>
                &nbsp;&nbsp;"llm": "gigachat",<br>
                &nbsp;&nbsp;"ip": "89.322.322.322"<br>
                &nbsp;&nbsp;"tokens": "456"<br>
                }'
              </code>
            </p>
          </rounded-container>
        </rounded-container>

        <!-- Ключи -->
        <rounded-container class="api_main__element api_keys__container">
          <h2 class="main_text api_main__element_title">Политика</h2>

          <!-- Таблица для десктопа -->
          <table v-if="!isMobile" class="main_text table_container">
            <thead class="table__line_active">
            <tr>
              <th>Название</th>
              <th>Ключ</th>
              <th>Дата создания</th>
              <th>Дата обращения</th>
              <th>Действия</th>
            </tr>
            </thead>
            <tbody class="table__line">
            <tr v-for="key in key_list" :key="key.api_key_id">
              <td>
                <input
                  v-if="editingKey === key.api_key_id"
                  type="text"
                  class="table_title_element main_text table__key"
                  v-model="editingValue"
                  @keydown.enter.prevent="saveEdit"
                  @keydown.escape.prevent="cancelEdit"
                  @blur="saveEdit"
                  :id="`key-${key.api_key_id}`"
                />
                <input
                  v-else
                  type="text"
                  class="table_title_element main_text table__key"
                  :value="key.key_name"
                  disabled
                  :id="`key-${key.api_key_id}`"
                />
              </td>
              <td @click="copyToClipboard(key.key_value)" class="key_name">{{ key.key_value }}</td>
              <td>{{ key.ts }}</td>
              <td>{{ key.last_used }}</td>
              <td id="key_actions">
                <svg @click="startEditing(key)" class="key_svg key_edit_svg" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M10.2503 5.14146L1.02686 14.3805V19L5.63856 19L14.862 9.76096M10.2503 5.14146L13.5576 1.82851L13.5596 1.82655C14.0148 1.3705 14.2429 1.14208 14.5058 1.05652C14.7373 0.981159 14.9868 0.981159 15.2183 1.05652C15.481 1.14202 15.7088 1.37018 16.1634 1.82558L18.1693 3.83483C18.6258 4.29218 18.8542 4.52097 18.9398 4.78466C19.015 5.01661 19.015 5.26646 18.9397 5.49841C18.8543 5.76191 18.6262 5.99035 18.1703 6.44704L18.1693 6.44803L14.862 9.76096M10.2503 5.14146L14.862 9.76096" stroke="#8E8D9D" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <svg @click="deleteKey(key.api_key_id)" class="key_svg key_bin_svg" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12.2098 8V15M7.7175 8V15M3.22517 4V15.8C3.22517 16.9201 3.22517 17.4798 3.46999 17.9076C3.68534 18.2839 4.02871 18.5905 4.45135 18.7822C4.93136 19 5.56005 19 6.81557 19H13.1118C14.3673 19 14.9951 19 15.4751 18.7822C15.8977 18.5905 16.2422 18.2839 16.4576 17.9076C16.7022 17.4802 16.7022 16.921 16.7022 15.8031V4M3.22517 4H5.47134M3.22517 4H0.979004M5.47134 4H14.456M5.47134 4C5.47134 3.06812 5.47134 2.60241 5.64232 2.23486C5.87029 1.74481 6.30727 1.35523 6.85764 1.15224C7.27042 1 7.794 1 8.84059 1H11.0868C12.1333 1 12.6566 1 13.0694 1.15224C13.6198 1.35523 14.0569 1.74481 14.2849 2.23486C14.4559 2.6024 14.456 3.06812 14.456 4M14.456 4H16.7022M16.7022 4H18.9483" stroke="#8E8D9D" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </td>
            </tr>
            </tbody>
          </table>

          <div v-if="isMobile" class="mobile_key_container">
            <div v-for="key in key_list" :key="key.api_key_id" class="main_text">
              <div class="key_elem_container">
                <input
                  v-if="editingKey === key.api_key_id"
                  type="text"
                  class="table_title_element main_text table__key"
                  v-model="editingValue"
                  @keydown.enter.prevent="saveEdit"
                  @keydown.escape.prevent="cancelEdit"
                  @blur="saveEdit"
                  :id="`key-${key.api_key_id}`"
                />
                <input
                  v-else
                  type="text"
                  class="table_title_element main_text table__key"
                  :value="key.key_name"
                  disabled
                  :id="`key-${key.api_key_id}`"
                />
                <div class="key_elem__actions">
                  <svg @click="startEditing(key)" class="key_svg key_edit_svg" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M10.2503 5.14146L1.02686 14.3805V19L5.63856 19L14.862 9.76096M10.2503 5.14146L13.5576 1.82851L13.5596 1.82655C14.0148 1.3705 14.2429 1.14208 14.5058 1.05652C14.7373 0.981159 14.9868 0.981159 15.2183 1.05652C15.481 1.14202 15.7088 1.37018 16.1634 1.82558L18.1693 3.83483C18.6258 4.29218 18.8542 4.52097 18.9398 4.78466C19.015 5.01661 19.015 5.26646 18.9397 5.49841C18.8543 5.76191 18.6262 5.99035 18.1703 6.44704L18.1693 6.44803L14.862 9.76096M10.2503 5.14146L14.862 9.76096" stroke="#8E8D9D" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <svg @click="deleteKey(key.api_key_id)" class="key_svg key_bin_svg" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12.2098 8V15M7.7175 8V15M3.22517 4V15.8C3.22517 16.9201 3.22517 17.4798 3.46999 17.9076C3.68534 18.2839 4.02871 18.5905 4.45135 18.7822C4.93136 19 5.56005 19 6.81557 19H13.1118C14.3673 19 14.9951 19 15.4751 18.7822C15.8977 18.5905 16.2422 18.2839 16.4576 17.9076C16.7022 17.4802 16.7022 16.921 16.7022 15.8031V4M3.22517 4H5.47134M3.22517 4H0.979004M5.47134 4H14.456M5.47134 4C5.47134 3.06812 5.47134 2.60241 5.64232 2.23486C5.87029 1.74481 6.30727 1.35523 6.85764 1.15224C7.27042 1 7.794 1 8.84059 1H11.0868C12.1333 1 12.6566 1 13.0694 1.15224C13.6198 1.35523 14.0569 1.74481 14.2849 2.23486C14.4559 2.6024 14.456 3.06812 14.456 4M14.456 4H16.7022M16.7022 4H18.9483" stroke="#8E8D9D" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <p class="toggle-arrow" @click="toggleKey(key.api_key_id)">
                  <svg
                    v-if="isExpanded(key.api_key_id)"
                    width="10" height="5"
                    viewBox="0 0 10 5"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M5 0L10 4.22482L9.08258 5L5 1.55047L0.91742 5L0 4.22482L5 0Z"
                      fill="white"
                    />
                  </svg>

                  <!-- стрелка вниз, когда закрыто -->
                  <svg
                    v-else
                    width="10" height="5"
                    viewBox="0 0 10 5"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M5 5L0 0.775182L0.917422 0L5 3.44953L9.08258 0L10 0.775182L5 5Z"
                      fill="white"
                    />
                  </svg>
                </p>
              </div>
              <transition name="slide-fade">
                <div v-if="isExpanded(key.api_key_id)" class="key_elem_drop_container">
                  <div class="key_elem_drop__elem key_elem_drop__key">
                    <p>Ключ</p>
                    <p @click="copyToClipboard(key.key_value)" class="key_name">{{ key.key_value }}</p>
                  </div>
                  <div class="key_elem_drop__elem">
                    <p>Дата создания</p>
                    <p>{{ key.ts }}</p>
                  </div>
                  <div class="key_elem_drop__elem">
                    <p>Дата обращения</p>
                    <p>{{ key.last_used }}</p>
                  </div>
                </div>
              </transition>
            </div>
          </div>
        </rounded-container>
      </div>

      <transition name="modal" appear>
        <modal-input v-if="showModal" @close="closeModal">
          <div class="modal_create_key">
            <h2 class="main_text">Создать новый API Key</h2>
            <input
              type="text"
              placeholder="Имя ключа"
              class="main_text modal_key_name"
              name="key_name"
              id="key_name_input"
            />
            <colored-button-center @click="add_key" class="modal_create_btn">
              Создать
            </colored-button-center>
          </div>
        </modal-input>
      </transition>
    </div>
  </div>
</template>

<style scoped>
.page_container {
  min-height: 100vh;
  width: 100%;
  padding: 25px 30px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}

.page_header_container {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.page_header {
  margin: 0;
  font-size: 26px;
  margin-bottom: 47px;
}

.api_add_btn p {
  color: #5C5A67;
  font-weight: 600;
  transition: color 0.07s ease-in-out;
}

.api_add_btn rect {
  transition: fill 0.07s ease-in-out;
}

.api_add_btn {
  height: 50px;
  width: 260px;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: normal;
  column-gap: 10px;
  border-radius: 120px;
  user-select: none;
  background: linear-gradient(79deg, #151325 26.69%, #321F3E 62.71%);
  transition: transform 0.05s ease-in-out, color 0.15s ease-in-out;
}

.api_add_btn:hover {
  background: linear-gradient(79deg, #151325 26.69%, #321F3E 62.71%) !important;
  transform: scale(1.01);
  transition: transform 0.01s ease-in-out;
}

.api_add_btn:active {
  transform: scale(1.02);
}

.api_add_btn:hover p,
.api_add_btn:hover rect {
  color: white;
  fill: white;
}

.api_main__container {
  display: flex;
  gap: 15px;
}

.api_main__element {
  min-height: calc(100vh - 200px);
  margin-bottom: 40px;
}

.api_docs__container {
  flex: 1;
}

.api_keys__container {
  flex: 2;
}

.api_main__element_title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 23px;
}

.api_docs__text {
  font-size: 16px;
  line-height: 1.5;
}

.api_docs__code {
  margin-top: 20px;
  display: inline-block;
  line-height: 1.5;
}

.table_container {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0 10px;
  margin: 0;
  padding: 0;
  table-layout: fixed;
}

.table_container th,
.table_container td {
  padding: 5px;
  height: 35px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.table_container th:nth-child(1),
.table_container td:nth-child(1) {
  width: 18.75%;
}

.table_container th:nth-child(2),
.table_container td:nth-child(2) {
  width: 12.5%;
}

.table_container th:nth-child(3),
.table_container td:nth-child(3) {
  width: 25%;
}

.table_container th:nth-child(4),
.table_container td:nth-child(4) {
  width: 25%;
}

.table_container th:nth-child(5),
.table_container td:nth-child(5) {
  width: 18.75%;
}

.table__line_active {
  text-align: start;
  background: linear-gradient(90deg, rgba(37,28,78,1) 0%, rgba(105,80,175,1) 100%);
}

.table__line_active th {
  text-align: start;
}

.table__line:hover {
  background: linear-gradient(90deg, rgba(37,28,78,1) 0%, rgba(105,80,175,1) 100%);
}

.api_keys__table_title {
  margin-bottom: 10px;
  box-sizing: border-box;
  transition: background 0.1s ease;
  padding: 0 15px;
}

.api_keys__table_title:hover {
  background: linear-gradient(90deg, rgba(37,28,78,1) 0%, rgba(105,80,175,1) 100%);
}

.api_keys__table_title:hover .table__key {
  color: #fff;
}

.table__key {
  color: #8E8D9D;
  transition: color 0.1s ease;
}

.table__key {
  background: transparent;
  border: none;
}

.table__key:focus,
.table__key:focus-visible {
  outline: none;
  border-bottom: 1px solid var(--filter_text);
}

.table_title_container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: space-between;
  gap: 10px;
  align-items: center;
}

.table_title_element {
  width: 100%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.table_keys__table {
  overflow-y: auto;
  height: 85%;
}

#key_name {
  width: 80px;
  background-color: transparent;
  outline: none;
  border: none;
}

#key_name:focus {
  color: var(--main_text_not_selected);
  text-decoration: underline;
}

#key_value {
  cursor: pointer;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

#key_date {
  width: 140px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

#key_date_appeal {
  width: 130px;
}

#key_actions {
  display: flex;
  gap: 15px;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.key_svg {
  cursor: pointer;
  width: 24px;
  height: 24px;
  transition: color 0.3s ease, transform 0.3s ease;
  fill: transparent;
}

.key_svg:hover {
  fill: white;
  transform: scale(1.1);
  transition: transform 0.1s ease;
}

.key_svg:active {
  transform: scale(1.15);
}

.modal_create_key {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 35px;
}

.modal_key_name {
  width: 80%;
  background-color: transparent;
  border: none;
  outline: none;
  text-align: center;
  border-top: 1px solid var(--filter_text);
  border-bottom: 1px solid var(--filter_text);
  box-sizing: border-box;
  padding: 10px;
}

.modal_key_name::placeholder {
  font-size: 20px;
}

.modal_create_btn {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 30%;
  transition: transform 0.15s ease;
}

.modal_create_btn:hover {
  transform: scale(1.025);
  transition: transform 0.05s ease;
}

.modal_create_btn:active {
  transform: scale(1.1);
}

.key_name {
  cursor: pointer;
}

@media (max-width: 1300px) {
  .page_container {
    width: 100%;
    padding: 25px 20px;
    padding-bottom: 40px;
  }
  .api_main__container {
    flex-direction: column;
  }
  .api_main__element {
    margin-bottom: 0;
  }
  .api_docs__container,
  .api_keys__container {
    flex: 1;
  }
}

@media (max-width: 700px) {
  #key_date {
    display: none;
  }
  .modal_create_btn {
    width: 80%;
  }
}

@media (max-width: 530px) {
  .page_container {
    padding: 25px 15px;
  }
  .api_docs__container {
    min-height: 800px;
  }
  .page_header_container {
    flex-direction: column;
    margin-bottom: 10px;
  }
  .api_add_btn {
    width: 100%;
  }
  #key_date_appeal {
    display: none;
  }
}

@media (max-width: 430px) {
  #key_name {
    width: 20%;
  }
  #key_actions {
    width: 40px;
  }
  .api_main__element {
    padding: 20px 20px 40px 20px;
  }
  .api_docs__text {
    font-size: 14px;
  }
  .api_docs__code {
    font-size: 14px;
  }
  .key_elem_container {
    background: linear-gradient(90deg, #251C4E 0%, #6950AF 100%);
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 15px;
    box-sizing: border-box;
  }
  .key_elem_container p {
    user-select: none;
  }
  .key_elem__actions {
    display: flex;
    gap: 15px;
  }
  .key_elem_drop_container {
    margin-top: 10px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .key_elem_drop__elem {
    display: flex;
    justify-content: space-between;
    background: #17162B;
    height: 40px;
    padding: 0 10px;
    box-sizing: border-box;
    font-size: 10px;
    align-items: center;
    border-bottom: 1px solid #8E8D9D;
  }
  .key_elem_drop__elem p:nth-child(1) {
    color: #8E8D9D;
  }
  .key_elem_drop__elem p:nth-child(2) {
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    width: 40%;
  }
  .api_main__container {
    box-sizing: border-box;
  }
  .page_container {
    width: 85vw;
    padding-right: 20px;
  }
  .mobile_key_container {
    display: flex;
    flex-direction: column;
    row-gap: 10px;
  }

  .table__key {
    background: transparent;
    border: none;
  }

  .table_title_element {
    width: 33%;
  }

  .table__key:focus,
  .table__key:focus-visible {
    outline: none;
    border-bottom: 1px solid var(--filter_text);
  }

  .modal_create_key h2 {
    text-align: center;
  }
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease;
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
.slide-fade-enter-to,
.slide-fade-leave-from {
  opacity: 1;
  transform: translateY(0);
}

/* Стиль для стрелки-переключателя */
.toggle-arrow {
  cursor: pointer;
  user-select: none;
}
</style>
