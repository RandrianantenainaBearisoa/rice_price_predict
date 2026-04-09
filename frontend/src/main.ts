import { createApp } from 'vue'
import App from './App.vue'
import router from './router'


import '@fontsource-variable/geologica/full.css';

import "../assets/styles/theme.scss"

const app = createApp(App)

app.use(router)

app.mount('#app')