<script setup>
import { ref, onMounted } from "vue";
import { fetchUserProfile, updateUserProfile } from "../services/apiService";

const profile = ref({ username: "", email: "", profile_picture: null });
const errorMessage = ref("");
const successMessage = ref("");

const loadProfile = async () => {
  try {
    profile.value = await fetchUserProfile();
  } catch (error) {
    errorMessage.value = "Erreur lors de la récupération du profil.";
  }
};

const updateProfile = async () => {
  const formData = new FormData();
  formData.append("nom", userProfile.nom);
  formData.append("email", userProfile.email);
  if (profilePicture.value) {
    formData.append("profile_picture", profilePicture.value);
  }

  try {
    await updateUserProfile(formData);
    console.log(" Profil mis à jour !");
  } catch (error) {
    console.error(" Erreur lors de la mise à jour :", error);
  }
};


onMounted(loadProfile);
</script>

<template>
  <div class="profile-container">
    <h1 class="profile-title">Modifier mon Profil</h1>

    <div v-if="errorMessage" class="message error-message">
      <span class="message-icon"></span>
      {{ errorMessage }}
    </div>
    <div v-if="successMessage" class="message success-message">
      <span class="message-icon"></span>
      {{ successMessage }}
    </div>

    <form @submit.prevent="updateProfile" class="profile-form">
      <div class="form-group">
        <label for="username">Nom d'utilisateur :</label>
        <input id="username" v-model="profile.username" type="text" class="form-control" />
      </div>

      <div class="form-group">
        <label for="email">Email :</label>
        <input id="email" v-model="profile.email" type="email" class="form-control" />
      </div>

      <div class="form-actions">
        <button type="submit" class="btn-save">Enregistrer</button>
      </div>
    </form>
  </div>
</template>

<style scoped>
:root {
  --primary-color: #4a6bdf;
  --primary-hover: #3a5bd0;
  --success-color: #34c759;
  --error-color: #ff3b30;
  --text-color: #333;
  --text-light: #666;
  --border-color: #e1e4e8;
  --bg-color: #f9fafc;
  --card-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  --input-shadow: 0 2px 5px rgba(0, 0, 0, 0.06);
  --transition: all 0.3s ease;
}

.profile-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2.5rem;
  background-color: white;
  border-radius: 12px;
  box-shadow: var(--card-shadow);
  color: var(--text-color);
}

.profile-title {
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  color: var(--text-color);
  text-align: center;
  font-weight: 600;
  position: relative;
  padding-bottom: 0.8rem;
}

.profile-title::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 3px;
  background: linear-gradient(to right, var(--primary-color), #8a94e2);
  border-radius: 3px;
}

.message {
  margin: 1.2rem 0;
  padding: 0.8rem 1rem;
  border-radius: 8px;
  display: flex;
  align-items: center;
  animation: fadeIn 0.5s ease-in-out;
}

.message-icon {
  margin-right: 0.8rem;
  font-size: 1.2rem;
}

.error-message {
  background-color: rgba(255, 59, 48, 0.1);
  border-left: 4px solid var(--error-color);
  color: #d32f2f;
}

.success-message {
  background-color: rgba(52, 199, 89, 0.1);
  border-left: 4px solid var(--success-color);
  color: #2e7d32;
}

.profile-form {
  margin-top: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-color);
  font-size: 0.95rem;
}

.form-control {
  width: 100%;
  padding: 0.8rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  font-size: 1rem;
  transition: var(--transition);
  background-color: var(--bg-color);
  color: var(--text-color);
  box-shadow: var(--input-shadow);
}

.form-control:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(74, 107, 223, 0.2);
}

.form-actions {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
}

.btn-save {
  background-color: var(--primary-color);
  color: white;
  border: none;
  padding: 0.8rem 2.5rem;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  transition: var(--transition);
  box-shadow: 0 4px 14px rgba(74, 107, 223, 0.4);
}

.btn-save:hover {
  background-color: var(--primary-hover);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(74, 107, 223, 0.5);
}

.btn-save:active {
  transform: translateY(0);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Animation pour les transitions de focus */
input {
  transition: border-color 0.25s ease-in-out, box-shadow 0.25s ease-in-out;
}

/* Responsive design */
@media (max-width: 768px) {
  .profile-container {
    padding: 1.5rem;
    margin: 1rem;
    max-width: 100%;
  }
  
  .profile-title {
    font-size: 1.5rem;
  }
  
  .btn-save {
    width: 100%;
  }
}
</style>