import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'
import './assets/main.css'
import App from './App.vue'
import router from './router'

const app = createApp(App)
const pinia = createPinia()

// Toast yapılandırması
const toastOptions = {
  position: 'top-right',
  timeout: 5000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: 'button',
  icon: true,
  rtl: false,
  toastClassName: 'custom-toast',
  bodyClassName: 'custom-toast-body',
  containerClassName: 'custom-toast-container'
}

app.use(pinia)
app.use(router)
app.use(Toast, toastOptions)

app.mount('#app')