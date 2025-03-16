<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  router.push("/login"); //  Redirection après déconnexion
}
</script>

<template>
  <button @click="logout">Se déconnecter</button>
</template>
<style scoped>
@import '../styles/views/logout-button.css';
</style>