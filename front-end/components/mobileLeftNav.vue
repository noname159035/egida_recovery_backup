<template>
  <div>
    <!-- Toggle button: видим только когда меню закрыто -->
    <button
      v-if="!isOpen"
      class="menu-toggle-button main_text"
      @click="isOpen = true"
      aria-label="Toggle menu"
    >
      ☰
    </button>

    <div
      v-if="isOpen"
      class="overlay"
      @click="isOpen = false"
    ></div>

    <nav
      :class="['nav_panel', { 'is-open': isOpen }]"
      @touchstart="handleTouchStart"
      @touchend="handleTouchEnd"
    >
      <div class="nav_header">
        <nuxt-link
          to="/"
          class="nav_user_link"
          @click.native="isOpen = false"
        >
          <button class="nav_user_button" @click="handleLoginClick">
            <svg width="30" height="30" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="15" cy="15" r="15" fill="#D9D9D9"/>
              <g opacity="0.5">
                <path d="M20.5163 16.2393L17.548 14.7601L18.6671 13.1871C18.9279 12.8198 19.0648 12.4083 19.0652 11.99V9.5C19.0652 8.57174 18.5842 7.6815 17.7281 7.02513C16.872 6.36875 15.7108 6 14.5 6C13.2892 6 12.1281 6.36875 11.2719 7.02513C10.4158 7.6815 9.93479 8.57174 9.93479 9.5V11.99C9.93519 12.4083 10.0721 12.8198 10.3329 13.1872L11.452 14.7601L8.4837 16.2393C8.02751 16.4657 7.65266 16.7762 7.39346 17.1424C7.13426 17.5086 6.99898 17.9187 7.00001 18.3354V21H22V18.3354C22.001 17.9187 21.8657 17.5086 21.6065 17.1424C21.3473 16.7762 20.9725 16.4657 20.5163 16.2393ZM20.6956 20H8.30435V18.3354C8.30374 18.0854 8.38492 17.8393 8.54044 17.6196C8.69597 17.3998 8.92089 17.2135 9.19461 17.0777L13.1753 15.094L11.478 12.7083C11.3215 12.4879 11.2394 12.241 11.2391 11.99V9.5C11.2391 8.83696 11.5827 8.20107 12.1942 7.73223C12.8057 7.26339 13.6352 7 14.5 7C15.3648 7 16.1943 7.26339 16.8058 7.73223C17.4173 8.20107 17.7609 8.83696 17.7609 9.5V11.99C17.7606 12.241 17.6785 12.4879 17.522 12.7083L15.8247 15.094L19.8055 17.0777C20.0792 17.2135 20.3041 17.3999 20.4596 17.6196C20.6151 17.8393 20.6963 18.0854 20.6956 18.3354V20Z" fill="#A626C6"/>
              </g>
            </svg>
            <span class="nav_user_text main_text">Войти</span>
          </button>
        </nuxt-link>
      </div>

      <ul class="nav_links">
        <li v-for="link in links" :key="link.id">
          <NavButton
            class="nav_link_button main_text"
            @click="onLinkClick(link.id)"
          >
            {{ link.text }}
          </NavButton>
        </li>
      </ul>

      <div class="nav_footer">
        <NavButton
          class="nav_settings_button"
          :disable="clickedButton === 'settings'"
          @click="onLinkClick('settings')"
        >
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
            <g opacity="0.5">
              <path d="M7.99986 5.06665C7.38607 5.06665 6.78607 5.23869 6.27572 5.56101C5.76537 5.88332 5.3676 6.34145 5.13272 6.87744C4.89783 7.41344 4.83637 8.00324 4.95612 8.57225C5.07586 9.14126 5.37143 9.66393 5.80544 10.0742C6.23946 10.4844 6.79243 10.7638 7.39442 10.877C7.99642 10.9901 8.62041 10.932 9.18747 10.71C9.75454 10.488 10.2392 10.112 10.5802 9.62965C10.9212 9.14727 11.1032 8.58014 11.1032 7.99998C11.1023 7.22229 10.775 6.47669 10.1932 5.92678C9.61146 5.37686 8.82264 5.06753 7.99986 5.06665ZM7.99986 9.86665C7.60927 9.86665 7.22745 9.75717 6.90268 9.55206C6.57791 9.34695 6.32479 9.05541 6.17531 8.71432C6.02584 8.37324 5.98673 7.99791 6.06293 7.63581C6.13913 7.27372 6.32722 6.94111 6.60341 6.68005C6.87961 6.41899 7.23149 6.24121 7.61458 6.16918C7.99767 6.09716 8.39475 6.13412 8.75561 6.27541C9.11648 6.41669 9.42491 6.65595 9.64191 6.96292C9.85891 7.26989 9.97474 7.63079 9.97474 7.99998C9.97415 8.49488 9.76589 8.96935 9.39566 9.3193C9.02543 9.66925 8.52345 9.86609 7.99986 9.86665Z" fill="#EDDCF5"/>
              <path d="M15.7425 10.2106L14.6221 9.33887C14.8207 8.45616 14.8207 7.54384 14.6221 6.66113L15.7425 5.78937C15.8717 5.68929 15.959 5.54901 15.9887 5.39364C16.0185 5.23826 15.9888 5.07795 15.9049 4.9414L14.7548 3.05863C14.6717 2.92164 14.5396 2.81712 14.3824 2.76379C14.2251 2.71047 14.0529 2.71183 13.8965 2.76764L12.5367 3.2492C11.8283 2.64423 10.9925 2.18766 10.0843 1.90947L9.84569 0.557102C9.81868 0.401247 9.73382 0.259579 9.60633 0.157492C9.47884 0.0554051 9.31705 -0.000427226 9.14997 2.46178e-06H6.84987C6.68279 -0.000421757 6.52101 0.0554083 6.39352 0.157487C6.26604 0.259567 6.18118 0.401222 6.15415 0.557069L5.91568 1.90947C5.00745 2.18766 4.17172 2.64422 3.46331 3.2492L2.10329 2.76757C1.94699 2.7118 1.77479 2.71046 1.61754 2.76379C1.46029 2.81712 1.32827 2.92163 1.24514 3.0586L0.0950886 4.9415C0.0112133 5.07806 -0.0184898 5.23837 0.0112993 5.39374C0.0410884 5.54911 0.128424 5.68938 0.257663 5.78943L1.37795 6.66113C1.17933 7.54384 1.17933 8.45616 1.37795 9.33887L0.257557 10.2106C0.128338 10.3107 0.041027 10.451 0.0112579 10.6064C-0.0185112 10.7617 0.0112062 10.922 0.0950886 11.0586L1.24517 12.9414C1.32832 13.0784 1.46036 13.1829 1.61763 13.2362C1.7749 13.2895 1.94712 13.2882 2.10343 13.2324L3.46335 12.7508C4.17175 13.3558 5.00749 13.8123 5.91572 14.0905L6.15419 15.4429C6.1812 15.5987 6.26605 15.7404 6.39353 15.8425C6.52102 15.9446 6.68279 16.0004 6.84987 16H9.14997C9.31705 16.0004 9.47883 15.9446 9.60632 15.8425C9.73381 15.7404 9.81867 15.5988 9.84569 15.4429L10.0842 14.0905C10.9924 13.8123 11.8282 13.3558 12.5366 12.7508L13.8965 13.2324C14.0528 13.2882 14.225 13.2895 14.3823 13.2362C14.5395 13.1829 14.6716 13.0784 14.7547 12.9414L15.9047 11.0585C15.9886 10.922 16.0183 10.7617 15.9886 10.6064C15.9589 10.451 15.8716 10.3107 15.7425 10.2106ZM13.9567 12.1146L12.2601 11.5138L12.0032 11.7583C11.2964 12.4317 10.4123 12.9147 9.44207 13.1574L9.08942 13.2453L8.7916 14.9333H7.20852L6.91081 13.2453L6.55815 13.1574C5.58796 12.9147 4.70383 12.4317 3.99699 11.7583L3.74008 11.5138L2.0432 12.1146L1.2518 10.8187L2.64934 9.73127L2.55413 9.39883C2.29227 8.4827 2.29227 7.5173 2.55413 6.60117L2.64934 6.26877L1.2518 5.1813L2.04337 3.88537L3.73997 4.48617L3.99688 4.2417C4.70373 3.56829 5.58785 3.08531 6.55805 2.8426L6.9107 2.75473L7.20838 1.06667H8.7916L9.08931 2.75473L9.44197 2.8426C10.4122 3.08531 11.2963 3.56829 12.0031 4.2417L12.26 4.48617L13.9566 3.88537L14.7482 5.18127L13.3507 6.26877L13.4459 6.60117C13.7078 7.5173 13.7078 8.4827 13.4459 9.39883L13.3507 9.73127L14.7482 10.8187L13.9567 12.1146Z" fill="#EDDCF5"/>
            </g>
          </svg>
          <span class="main_text nav_settings_button_text">Настройки</span>
        </NavButton>
      </div>
    </nav>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const isOpen = ref(false)
const clickedButton = ref(null)
const links = [
  { id: 'button1', text: 'Функционал' },
  { id: 'button2', text: 'Команда' }
]

// Для поддержки свайпа
const touchStartX = ref(0)

function handleTouchStart(e) {
  touchStartX.value = e.touches[0].clientX
}

function handleTouchEnd(e) {
  const touchEndX = e.changedTouches[0].clientX
  if (touchStartX.value - touchEndX > 50) {
    isOpen.value = false
  }
}

function onLinkClick(id) {
  clickedButton.value = id
  isOpen.value = false
}

const emit = defineEmits([ 'open-mobile-modal' ])

const isOpenModal = ref(false)

function handleLoginClick() {
  isOpenModal.value = false        // закрываем меню
  emit('open-mobile-modal')   // шлём событие наверх
}
</script>

<style scoped>
.menu-toggle-button {
  position: fixed;
  top: 20px;
  left: 20px;
  z-index: 1100;
  background: transparent;
  border: none;
  font-size: 1.8rem;
  cursor: pointer;
  user-select: none;
  display: none;
}
@media (max-width: 1070px) {
  .menu-toggle-button {
    display: block;
  }
}

.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  z-index: 1000;
}

.nav_panel {
  position: fixed;
  top: 0;
  left: -320px;
  width: 280px;
  max-width: 50%;
  height: 100%;
  background: linear-gradient(0deg, #333379 0%, #080813 40%, #080813 100%);
  padding: 30px 20px;
  display: flex;
  flex-direction: column;
  transition: left 0.3s ease-in-out;
  z-index: 1001;
}
.nav_panel.is-open {
  left: 0;
}

.nav_header {
  margin-bottom: 40px;
}

.nav_settings_button {
  background: transparent;
  border: none;
  padding: 0;
  font-size: 18px;
  color: #B0ACC0;
  cursor: pointer;
  margin-bottom: 50px;
}

.nav_settings_button span {
  margin-left: 20px;
  color: #B0ACC0;
}

.nav_settings_button:hover {
  color: #fff;
}

.nav_user_link {
  text-decoration: none;
}

.nav_user_button {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 20px;
  border: none;
  border-radius: 30px;
  background: linear-gradient(90deg,#251c4e 0%,#6950af 100%);
  cursor: pointer;
}
.nav_user_icon {
  flex-shrink: 0;
}
.nav_user_text {
  color: #fff;
  font-size: 16px;
  font-weight: 500;
}

.nav_links {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 0;
}
.nav_link_button {
  background: transparent;
  border: none;
  padding: 0;
  text-align: left;
  font-size: 18px;
  color: #B0ACC0;
  cursor: pointer;
}
.nav_link_button:hover {
  color: #fff;
}

.nav_footer {
  margin-top: auto;
}

.nav_settings_icon {
  flex-shrink: 0;
}
</style>
