import './assets/main.css'

// Bootstrap
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'


// Fontawesome
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faInfoCircle, faPlus, faChevronLeft, faXmark, faCaretDown} from '@fortawesome/free-solid-svg-icons';

library.add(faInfoCircle);
library.add(faPlus);
library.add(faChevronLeft);
library.add(faXmark);
library.add(faCaretDown);


// Toaster
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";

// Vue-loading overlay
import {LoadingPlugin} from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/css/index.css';

const options = {
    position: "top-center",
    timeout: 3000,
}

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Toast, options)
app.use(LoadingPlugin)
app.component('font-awesome-icon', FontAwesomeIcon)

app.mount('#app')
