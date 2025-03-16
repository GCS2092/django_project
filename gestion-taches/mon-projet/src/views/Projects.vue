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
  /* 🎨 CSS amélioré pour le Dashboard */
.dashboard-container {
  padding: 2rem;
  font-family: 'Roboto', sans-serif;
  background-color: #f8f9fa;
  min-height: 100vh;
  color: #333;
}

/* 🔹 Entête du tableau de bord - Design plus moderne */
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e9ecef;
}

.main-title {
  font-size: 2.2rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
}

.logout-button {
  background-color: #e74c3c;
  color: white;
  padding: 0.7rem 1.2rem;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.logout-button:hover {
  background-color: #c0392b;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 🔹 Notifications améliorées */
.notification {
  padding: 1rem;
  border-radius: 6px;
  margin-bottom: 1.5rem;
  font-size: 1rem;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.success {
  background-color: rgba(46, 204, 113, 0.15);
  color: #27ae60;
  border-left: 5px solid #27ae60;
}

.error {
  background-color: rgba(231, 76, 60, 0.15);
  color: #c0392b;
  border-left: 5px solid #c0392b;
}

/* 🔹 Contenu du tableau de bord - Plus d'espace et meilleure organisation */
.dashboard-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
}

/* 🔹 Section des projets - Style plus distinctif */
.projects-section {
  margin-top: 1.5rem;
}

.section-title {
  font-size: 1.6rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #3498db;
  padding-bottom: 0.5rem;
  display: inline-block;
}

/* 🔹 Animation de chargement améliorée */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 0;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(52, 152, 219, 0.1);
  border-left-color: #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 🔹 Grille de projets responsive et moderne */
.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

/* 🔹 Carte projet - Design plus élégant */
.project-card {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  border: 1px solid #f1f1f1;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.project-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
  border-color: #e0e0e0;
}

.project-title {
  font-size: 1.4rem;
  font-weight: 600;
  margin-bottom: 0.8rem;
  color: #3498db;
}

.project-description {
  font-size: 1rem;
  color: #7f8c8d;
  margin-bottom: 1.5rem;
  flex-grow: 1;
  line-height: 1.5;
}

/* 🔹 Actions des projets - Boutons plus stylés */
.project-actions {
  display: flex;
  justify-content: space-between;
  gap: 0.8rem;
  margin-top: auto;
}

.btn-view-tasks,
.btn-view-details {
  flex: 1;
  padding: 0.8rem 1rem;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  border: none;
}

.btn-view-tasks {
  background: #3498db;
  color: white;
}

.btn-view-tasks:hover {
  background: #2980b9;
  transform: translateY(-2px);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
}

.btn-view-details {
  background: #ecf0f1;
  color: #34495e;
}

.btn-view-details:hover {
  background: #dce4e8;
  transform: translateY(-2px);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
}

/* 🔹 État vide - Plus attrayant */
.empty-state {
  text-align: center;
  padding: 3rem 1.5rem;
  border-radius: 8px;
  background: #f7f9fc;
  border: 1px dashed #cbd5e0;
}

.empty-state p:first-child {
  font-size: 1.2rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.empty-subtitle {
  color: #7f8c8d;
  font-size: 1rem;
}

/* 🔹 Responsive design amélioré */
@media (max-width: 768px) {
  .dashboard-container {
    padding: 1rem;
  }
  
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .main-title {
    font-size: 1.8rem;
  }
  
  .projects-grid {
    grid-template-columns: 1fr;
  }
  
  .dashboard-content {
    padding: 1.2rem;
  }
}

@media (max-width: 480px) {
  .project-actions {
    flex-direction: column;
  }
}

</style>