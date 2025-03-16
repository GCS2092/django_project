<script setup>
import { ref, onMounted } from "vue";
import { fetchProfile } from "../services/apiService"; // ✅ Vérifie bien que cette fonction est bien importée !

const profile = ref({});
const errorMessage = ref("");

const fetchUserProfile = async () => {
  try {
    profile.value = await fetchProfile();
  } catch (error) {
    errorMessage.value = "Erreur lors du chargement du profil.";
    console.error("❌ Erreur lors du chargement du profil :", error);
  }
};

onMounted(fetchUserProfile);
</script>

<template>
  <div class="profile-container">
    <h1>👤 Mon Profil</h1>

    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>

    <div v-else>
      <div class="profile-info">
        <p><strong>Nom :</strong> {{ profile.nom }}</p>
        <p><strong>Email :</strong> {{ profile.email }}</p>
        <p><strong>Rôle :</strong> {{ profile.role }}</p>

        <div v-if="profile.profile_picture">
          <img :src="profile.profile_picture" alt="Photo de profil" class="profile-picture" />
        </div>
      </div>

      <router-link to="/profile/view" class="btn">
        ✏️ Modifier le profil
      </router-link>
    </div>
  </div>
</template>

<style scoped>
.profile-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.profile-info p {
  font-size: 1.1rem;
  margin-bottom: 0.8rem;
}

.profile-picture {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  margin-top: 1rem;
}

.btn {
  display: inline-block;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-weight: 500;
  text-decoration: none;
  cursor: pointer;
  background-color: #4361ee;
  color: white;
  margin-top: 1rem;
}

.btn:hover {
  background-color: #3a56d4;
}
</style>
