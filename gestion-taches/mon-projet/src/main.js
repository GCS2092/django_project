import { createApp } from 'vue';
import App from './App.vue';
import router from "./router/index.js";// 👈 Vérifie que le fichier routeur est bien importé
import "./assets/styles.css";

const app = createApp(App);
app.use(router);
app.mount('#app');
