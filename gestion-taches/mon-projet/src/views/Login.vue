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
<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d);
  background-size: 400% 400%;
  animation: gradientBG 15s ease infinite;
  padding: 20px;
}

@keyframes gradientBG {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.auth-form {
  width: 100%;
  max-width: 420px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.auth-form:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.25);
}

.auth-title {
  font-size: 2.2rem;
  color: #333;
  margin-bottom: 30px;
  text-align: center;
  font-weight: 700;
  letter-spacing: 1px;
  position: relative;
}

.auth-title::after {
  content: '';
  position: absolute;
  width: 60px;
  height: 4px;
  background: linear-gradient(90deg, #1a2a6c, #b21f1f);
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  border-radius: 2px;
}

.form-group {
  margin-bottom: 25px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  color: #555;
  transition: color 0.3s ease;
}

.form-control {
  width: 100%;
  padding: 14px;
  border: 2px solid #ddd;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background-color: rgba(255, 255, 255, 0.8);
}

.form-control:focus {
  outline: none;
  border-color: #1a2a6c;
  box-shadow: 0 0 0 3px rgba(26, 42, 108, 0.2);
}

.form-group:focus-within label {
  color: #1a2a6c;
}

.auth-actions {
  margin-top: 35px;
}

.btn {
  cursor: pointer;
  padding: 14px 24px;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
}

.btn-primary {
  background: linear-gradient(135deg, #1a2a6c, #4a54bc);
  color: white;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #15215a, #3f47a0);
  transform: translateY(-2px);
  box-shadow: 0 7px 14px rgba(26, 42, 108, 0.3);
}

.btn-primary:active {
  transform: translateY(0);
  box-shadow: 0 3px 8px rgba(26, 42, 108, 0.3);
}

.btn-block {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.btn-icon {
  margin-right: 10px;
  display: flex;
  align-items: center;
}

.error-message {
  margin-top: 25px;
  padding: 12px 16px;
  background-color: rgba(255, 59, 48, 0.1);
  border-left: 4px solid #ff3b30;
  color: #d82b22;
  border-radius: 8px;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.error-message svg {
  margin-right: 10px;
  stroke: #ff3b30;
  flex-shrink: 0;
}

.auth-footer {
  margin-top: 30px;
  text-align: center;
  color: #555;
  font-size: 0.9rem;
}

.auth-link, .auth-footer a {
  color: #1a2a6c;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s ease;
}

.auth-link:hover, .auth-footer a:hover {
  color: #b21f1f;
  text-decoration: underline;
}

.auth-link-small {
  display: block;
  margin-top: 15px;
  font-size: 0.85rem;
  opacity: 0.8;
}

/* Animation de focus pour les champs */
.form-control:focus::placeholder {
  opacity: 0.5;
  transform: translateX(5px);
  transition: all 0.3s ease;
}

/* Responsive styles */
@media (max-width: 576px) {
  .auth-form {
    padding: 30px 20px;
  }
  
  .auth-title {
    font-size: 1.8rem;
  }
  
  .btn {
    padding: 12px 20px;
  }
}
</style>