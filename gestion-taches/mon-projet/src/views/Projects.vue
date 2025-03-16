<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { getToken, refreshToken } from "../services/authService";

const router = useRouter();
const projects = ref([]);
const isLoading = ref(true);
const errorMessage = ref("");

const showError = (message) => {
  errorMessage.value = message;
  setTimeout(() => {
    errorMessage.value = "";
  }, 3000);
};

//  Récupération des projets
const fetchProjects = async () => {
  let token = getToken();
  if (!token) {
    router.push("/login");
    return;
  }

  try {
    isLoading.value = true;
    let response = await fetch("http://127.0.0.1:8000/api/projects/", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    });

    if (response.status === 401) {
      token = await refreshToken();
      if (token) {
        response = await fetch("http://127.0.0.1:8000/api/projects/", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json"
          }
        });
      } else {
        router.push("/login");
        return;
      }
    }

    if (!response.ok) throw new Error(`Erreur HTTP: ${response.status}`);

    projects.value = await response.json();
    console.log(" Projets récupérés :", projects.value);
  } catch (error) {
    showError("Impossible de récupérer les projets");
    console.error("Erreur API :", error);
  } finally {
    isLoading.value = false;
  }
};

// 🔹 Redirection vers les détails d'un projet
const viewProject = (id) => {
  router.push(`/projects/${id}`);
};

// 🔹 Redirection vers les tâches d'un projet
const viewTasks = (id) => {
  router.push(`/projects/${id}/tasks`);
};

onMounted(fetchProjects);
</script>

<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h2 class="main-title">Gestion de Projets</h2>
      <router-link to="/login" class="logout-button">🚪 Se déconnecter</router-link>
    </div>

    <div v-if="errorMessage" class="notification" :class="errorMessage.includes('succès') ? 'success' : 'error'">
      {{ errorMessage }}
    </div>

    <div class="dashboard-content">
      <div class="projects-section">
        <h3 class="section-title">Mes Projets</h3>

        <div v-if="isLoading" class="loading-container">
          <div class="loading-spinner"></div>
          <p>Chargement des projets...</p>
        </div>

        <div v-else>
          <div v-if="projects.length === 0" class="empty-state">
            <p>Vous n'avez pas encore de projets</p>
            <p class="empty-subtitle">Ajoutez votre premier projet</p>
          </div>
          
          <div v-else class="projects-grid">
            <div v-for="project in projects" :key="project.id" class="project-card">
              <h4 class="project-title">{{ project.title }}</h4>
              <p class="project-description">{{ project.description || "Pas de description" }}</p>

              <div class="project-actions">
                <button class="btn-view-tasks" @click="viewTasks(project.id)">
                   Voir les tâches
                </button>
                <button class="btn-view-details" @click="viewProject(project.id)">
                   Voir détails
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
 /* 🎨 Amélioration du style de la page Dashboard */
.dashboard-container {
  padding: 30px;
  font-family: 'Roboto', sans-serif;
  background-color: #f8f9fa;
  min-height: 100vh;
}

/* 🔹 Entête du tableau de bord */
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.main-title {
  font-size: 2rem;
  font-weight: 600;
  color: var(--primary-color);
}

.logout-button {
  background-color: var(--danger-color);
  color: white;
  padding: 10px 15px;
  border-radius: var(--border-radius);
  text-decoration: none;
  font-weight: 500;
  transition: background 0.3s ease;
}

.logout-button:hover {
  background-color: darkred;
}

/* 🔹 Notifications et messages */
.notification {
  padding: 15px;
  border-radius: var(--border-radius);
  margin-bottom: 20px;
  font-size: 0.95rem;
  text-align: center;
}

.success {
  background-color: rgba(46, 204, 113, 0.2);
  color: #27ae60;
  border-left: 5px solid #27ae60;
}

.error {
  background-color: rgba(231, 76, 60, 0.2);
  color: #c0392b;
  border-left: 5px solid #c0392b;
}

/* 🔹 Contenu du tableau de bord */
.dashboard-content {
  background: white;
  padding: 25px;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
}

/* 🔹 Section des projets */
.projects-section {
  margin-top: 20px;
}

.section-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--primary-dark);
  margin-bottom: 15px;
  border-bottom: 2px solid var(--primary-color);
  padding-bottom: 8px;
}

/* 🔹 Animation de chargement */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-left-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 🔹 Affichage des projets */
.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

/* 🔹 Carte projet */
.project-card {
  background-color: white;
  border-radius: var(--border-radius);
  padding: 20px;
  box-shadow: var(--box-shadow);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.project-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.project-title {
  font-size: 1.3rem;
  font-weight: bold;
  margin-bottom: 10px;
  color: var(--primary-color);
}

.project-description {
  font-size: 1rem;
  color: var(--text-light);
  margin-bottom: 15px;
}

/* 🔹 Actions des projets */
.project-actions {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.btn-view-tasks,
.btn-view-details {
  flex: 1;
  padding: 10px;
  border-radius: var(--border-radius);
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s ease, transform 0.2s ease;
  text-align: center;
  border: none;
}

.btn-view-tasks {
  background: var(--primary-color);
  color: white;
}

.btn-view-tasks:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
}

.btn-view-details {
  background: var(--secondary-color);
  color: var(--text-color);
}

.btn-view-details:hover {
  background: #e0e0e0;
  transform: translateY(-2px);
}

/* 🔹 État vide */
.empty-state {
  text-align: center;
  padding: 30px;
  border-radius: var(--border-radius);
  background: rgba(0, 0, 0, 0.03);
}

.empty-subtitle {
  color: var(--text-light);
  font-size: 0.9rem;
}
.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

@media (max-width: 768px) {
  .projects-grid {
    grid-template-columns: 1fr; /* 📌 Passe en colonne sur mobile */
  }
}


</style>