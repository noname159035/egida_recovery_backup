// plugins/device.client.js
import { defineNuxtPlugin } from '#app'
import { useDeviceStore } from '~/store/device'

export default defineNuxtPlugin(() => {
  const device = useDeviceStore()

  const update = () => {
    device.setMobile(window.innerWidth <= 430)
  }
  update()
  window.addEventListener('resize', update)
})
