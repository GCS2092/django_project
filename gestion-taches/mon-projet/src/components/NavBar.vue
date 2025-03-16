<template>
  
  <nav class="navbar">
    <div class="navbar-container">
      <div class="navbar-links">
        <router-link to="/dashboard" class="navbar-link">
          <span class="icon">🏠</span>
          <span class="text">Accueil</span>
        </router-link>
        <router-link to="/projects" class="navbar-link">
          <span class="icon">📂</span>
          <span class="text">Projets</span>
        </router-link>
      </div>
      <button @click="handleLogout" class="navbar-button">
        <span class="icon">🚪</span>
        <span class="text">Déconnexion</span>
      </button>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from "vue-router";
import { logout } from "../services/authService";

const router = useRouter();
const handleLogout = () => {
  logout();
  router.push("/login");
};
</script>

<style scoped>
/* Variables sophistiquées */
:root {
  /* Palette de couleurs élégante */
  --primary-gradient: linear-gradient(135deg, #4568DC, #B06AB3);
  --secondary-gradient: linear-gradient(135deg, #f46b45, #eea849);
  --button-gradient: linear-gradient(135deg, #ff416c, #ff4b2b);
  --button-hover-gradient: linear-gradient(135deg, #f32170, #ff6b08);
  --text-color: #ffffff;
  --highlight-color: #FFD700;
  
  /* Effets et animations */
  --glass-effect: rgba(255, 255, 255, 0.1);
  --glass-border: 1px solid rgba(255, 255, 255, 0.18);
  --glass-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
  --deep-shadow: 0 10px 20px rgba(0, 0, 0, 0.19), 0 6px 6px rgba(0, 0, 0, 0.23);
  --hover-shadow: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);
  --hover-transform: translateY(-5px);
  --active-transform: translateY(0);
  
  /* Formes et dimensions */
  --border-radius: 12px;
  --soft-curve: 50px;
  --navbar-height: 70px;
  --button-height: 45px;
}

/* Base de la navbar avec effet glassmorphism */
.navbar {
  width: 100%;
  background: var(--primary-gradient);
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: var(--deep-shadow);
  height: var(--navbar-height);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-bottom: var(--glass-border);
}

/* Container avec forme ondulée */
.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  padding: 0 2rem;
  position: relative;
}

/* Effet ondulé au bas de la navbar */
.navbar-container::after {
  content: "";
  position: absolute;
  bottom: -15px;
  left: 0;
  width: 100%;
  height: 20px;
  background: var(--primary-gradient);
  border-radius: 0 0 var(--soft-curve) var(--soft-curve);
  opacity: 0.7;
  z-index: -1;
  filter: blur(5px);
}

/* Design des liens */
.navbar-links {
  display: flex;
  gap: 1.5rem;
  position: relative;
  z-index: 10;
}

.navbar-link {
  text-decoration: none;
  background: var(--glass-effect);
  border-radius: var(--border-radius);
  padding: 0.7rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.5px;
  color: var(--text-color);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: var(--glass-border);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: var(--glass-shadow);
  position: relative;
  overflow: hidden;
}

/* Effet de brillance sur hover */
.navbar-link::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 60%);
  opacity: 0;
  transition: opacity 0.4s ease;
  transform: scale(0.5);
}

.navbar-link:hover::before {
  opacity: 1;
  transform: scale(1);
}

.navbar-link:hover {
  transform: var(--hover-transform);
  box-shadow: var(--hover-shadow);
  color: var(--highlight-color);
}

/* Style actif avec un indicateur élégant */
.navbar-link.router-link-active {
  background: linear-gradient(to right, var(--glass-effect), rgba(255, 255, 255, 0.25));
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.navbar-link.router-link-active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 10%;
  width: 80%;
  height: 3px;
  background: var(--highlight-color);
  border-radius: 10px;
  box-shadow: 0 0 10px var(--highlight-color), 0 0 20px var(--highlight-color);
  animation: pulse 1.5s infinite alternate;
}

/* Bouton de déconnexion spectaculaire */
.navbar-button {
  border: none;
  cursor: pointer;
  background: var(--button-gradient);
  color: var(--text-color);
  font-weight: 600;
  letter-spacing: 0.5px;
  padding: 0.7rem 1.8rem;
  border-radius: var(--border-radius);
  display: flex;
  align-items: center;
  gap: 0.7rem;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: var(--deep-shadow);
  position: relative;
  overflow: hidden;
  height: var(--button-height);
  font-size: 1rem;
}

.navbar-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: 0.5s;
}

.navbar-button:hover::before {
  left: 100%;
}

.navbar-button:hover {
  background: var(--button-hover-gradient);
  transform: var(--hover-transform);
  box-shadow: var(--hover-shadow);
}

.navbar-button:active {
  transform: var(--active-transform);
}

/* Style amélioré des icônes */
.icon {
  font-size: 1.3rem;
  filter: drop-shadow(0 0 2px rgba(0, 0, 0, 0.3));
  transition: transform 0.3s ease;
}

.navbar-link:hover .icon,
.navbar-button:hover .icon {
  transform: scale(1.2);
  animation: wiggle 0.5s ease;
}

/* Animation de texte */
.text {
  position: relative;
  transition: all 0.3s ease;
}

.navbar-link:hover .text,
.navbar-button:hover .text {
  transform: translateX(3px);
}

/* Animations */
@keyframes pulse {
  from { opacity: 0.6; }
  to { opacity: 1; }
}

@keyframes wiggle {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(10deg); }
  75% { transform: rotate(-10deg); }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

.navbar {
  animation: fadeIn 0.6s ease-out;
}

/* Version responsive luxueuse */
@media (max-width: 768px) {
  .navbar {
    height: auto;
    padding: 1rem 0;
  }
  
  .navbar-container {
    padding: 0 1rem;
    flex-direction: row;
    justify-content: space-between;
  }
  
  .navbar-links {
    gap: 0.8rem;
  }
  
  .text {
    display: none;
  }
  
  .navbar-link, 
  .navbar-button {
    padding: 0.8rem;
    border-radius: 50%;
    width: 45px;
    height: 45px;
    display: flex;
    justify-content: center;
  }
  
  .icon {
    font-size: 1.5rem;
    margin: 0;
  }
  
  /* Effet circulaire en responsive */
  .navbar-link.router-link-active::after {
    width: 10px;
    height: 10px;
    left: 50%;
    bottom: -5px;
    transform: translateX(-50%);
    border-radius: 50%;
  }
}

/* Animations avancées et hover states */
.navbar-link, .navbar-button {
  position: relative;
  z-index: 1;
}

.navbar-link::after {
  z-index: -1;
}

/* Un tout petit avion en papier qui vole quand on survole le bouton déconnexion */
.navbar-button:hover .icon {
  animation: fly 1s forwards;
}

@keyframes fly {
  0% { transform: translateX(0) rotate(0); }
  50% { transform: translateX(-5px) rotate(-10deg); }
  100% { transform: translateX(3px) rotate(0); }
}
</style>