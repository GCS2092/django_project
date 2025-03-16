<template>
  <div class="auth-container">
    <div class="auth-form">
      <h2 class="auth-title">Inscription</h2>
      <form @submit.prevent="register">
        <div class="form-group">
          <label for="nom">Nom</label>
          <input 
            id="nom"
            v-model="nom" 
            class="form-control" 
            placeholder="Entrez votre nom" 
            required 
          />
        </div>

        <div class="form-group">
          <label for="email">Email</label>
          <input 
            id="email"
            v-model="email" 
            class="form-control" 
            placeholder="Entrez votre email" 
            required 
          />
        </div>

        <div class="form-group">
          <label for="password">Mot de passe</label>
          <input 
            id="password"
            v-model="password" 
            type="password" 
            class="form-control" 
            placeholder="Entrez votre mot de passe" 
            required 
          />
        </div>

        <div class="form-group">
          <label for="role">Rôle</label>
          <select id="role" v-model="role" class="form-control" required>
            <option value="professeur">Professeur</option>
            <option value="etudiant">Étudiant</option>
          </select>
        </div>

        <div class="auth-actions">
          <button type="submit" class="btn btn-primary btn-block">S'inscrire</button>
        </div>
      </form>

      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

      <div class="auth-footer">
        <p>Déjà un compte ? <router-link to="/login">Connectez-vous ici</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from "vue-router";
import axios from "../axios";

export default {
  data() {
    return {
      nom: "",
      email: "",
      password: "",
      role: "etudiant",
      errorMessage: "",
    };
  },
  methods: {
    async register() {
      try {
        const response = await axios.post("register/", {
          email: this.email,
          nom: this.nom,
          role: this.role,
          password: this.password,
        });

        console.log(" Inscription réussie !");
        this.$router.push("/login");
      } catch (error) {
        this.errorMessage = " Échec de l'inscription.";
        console.error("Erreur :", error);
      }
    },
  },
};
</script>

<style>
.register-container {
  max-width: 500px;
  margin: 50px auto;
  padding: 30px;
  background-color: white;
  border-radius: var(--border-radius);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-row {
  display: flex;
  gap: 15px;
}

.form-row .form-group {
  flex: 1;
}

.register-title {
  text-align: center;
  margin-bottom: 20px;
  color: var(--primary-color);
}

.user-type-selector {
  display: flex;
  gap: 15px;
  margin-bottom: 15px;
}

.user-type-selector label {
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
}

/* Styles pour les éléments auth- qui sont utilisés dans le template */
.auth-container {
  max-width: 500px;
  margin: 50px auto;
  padding: 30px;
  background-color: white;
  border-radius: var(--border-radius);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.auth-title {
  text-align: center;
  margin-bottom: 20px;
  color: var(--primary-color);
}

.auth-actions {
  margin-top: 20px;
}

.auth-footer {
  margin-top: 20px;
  text-align: center;
}

.form-group {
  margin-bottom: 15px;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.btn {
  padding: 10px 15px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  font-weight: bold;
}

.btn-primary {
  background-color: var(--primary-color);
  color: white;
}

.btn-block {
  width: 100%;
}

.error-message {
  color: #e74c3c;
  margin-top: 10px;
  text-align: center;
}
</style>