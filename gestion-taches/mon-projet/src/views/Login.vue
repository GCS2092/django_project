<template>
  <div class="auth-container">
    <div class="auth-form">
      <h2 class="auth-title">Connexion</h2>
      <form @submit.prevent="login">
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
        
        <div class="auth-actions">
          <button type="submit" class="btn btn-primary btn-block">
            <span class="btn-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"></path>
                <polyline points="10 17 15 12 10 7"></polyline>
                <line x1="15" y1="12" x2="3" y2="12"></line>
              </svg>
            </span>
            Se connecter
          </button>
        </div>
      </form>
      
      <div v-if="errorMessage" class="error-message">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
        {{ errorMessage }}
      </div>
      
      <div class="auth-footer">
        <p>Pas encore de compte ? <router-link to="/register">Inscrivez-vous ici</router-link></p>
        <a href="#" class="auth-link auth-link-small">Mot de passe oublié ?</a>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from "vue-router";
import axios from '../axios';

export default {
  data() {
    return {
      email: '',  
      password: '',
      errorMessage: ''
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('token/', {
          email: this.email, 
          password: this.password
        });

        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);

        console.log(" Connexion réussie, token enregistré !");
        
        //  Récupération du rôle après connexion
        const userRole = await this.fetchUserRole();

        if (userRole === "admin") {
          this.$router.push("/dashboard");
        } else {
          this.$router.push("/projects");
        }
      } catch (error) {
        this.errorMessage = " Identifiants incorrects !";
        console.error("Erreur de connexion :", error);
      }
    },
    async fetchUserRole() {
      try {
        const token = localStorage.getItem("access_token");
        if (!token) return null;

        const response = await axios.get("http://127.0.0.1:8000/api/user-role/", {
          headers: { Authorization: `Bearer ${token}` },
        });

        return response.data.role;
      } catch (error) {
        console.error("Erreur récupération rôle utilisateur :", error);
        return null;
      }
    }
  }
};
</script>
