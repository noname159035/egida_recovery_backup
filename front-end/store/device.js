import { defineStore } from 'pinia'

export const useDeviceStore = defineStore('device', {
  state: () => ({
    // по-умолчанию — false, на сервере у window нет
    isMobile: false
  }),
  actions: {
    setMobile(val) {
      this.isMobile = val
    }
  }
})
