<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { fetchDashboardData, fetchTasks, downloadPDF } from "../services/apiService";
import { fetchUserRole } from "../services/authService";

const router = useRouter();
const userRole = ref(null);
const stats = ref({ total_projects: 0, total_tasks: 0, completed_tasks: 0 });
const tasks = ref([]);
const filterStatus = ref("");
const isLoading = ref(true);

const filteredTasks = computed(() => {
  return filterStatus.value
    ? tasks.value.filter(task => task.status === filterStatus.value)
    : tasks.value;
});

const isAdmin = computed(() => userRole.value === 'admin');
const isTeacher = computed(() => userRole.value === 'professeur');
const canManageContent = computed(() => isAdmin.value || isTeacher.value);

const getStatusLabel = (status) => {
  const statusMap = {
    'todo': 'À faire',
    'in_progress': 'En cours',
    'done': 'Terminée'
  };
  return statusMap[status] || status;
};

const fetchData = async () => {
  isLoading.value = true;
  try {
    userRole.value = await fetchUserRole();
    console.log("🔍 Rôle utilisateur :", userRole.value); // Vérifie le rôle dans la console
    stats.value = await fetchDashboardData();
    tasks.value = await fetchTasks();
  } catch (error) {
    console.error("Erreur lors du chargement des données :", error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(fetchData);
</script>

<template>
  <div class="dashboard">
    <h1>Tableau de Bord</h1>
    
    <div class="actions">
      <router-link to="/projects" class="btn">
        📂 Voir les projets
      </router-link>
      
      <!-- Bouton Ajouter un projet (Seulement Admin & Professeur) -->
      <router-link v-if="canManageContent" to="/add-project" class="btn">
        ➕ Ajouter un projet
      </router-link>

      <!-- Bouton Ajouter une tâche (Seulement Admin & Professeur) -->
      <router-link v-if="canManageContent" to="/add-task" class="btn">
        ✅ Ajouter une tâche
      </router-link>

      <!-- Lien vers le profil utilisateur -->
      <router-link to="/profile/view" class="btn-profile">
        👤 Voir mon Profil
      </router-link>
      
      
      <router-link to="/profile/view" class="btn">
        ✏️ Modifier mon profil
      </router-link>
    </div>
    
    <div v-if="isLoading" class="loading">
      <span>Chargement en cours...</span>
    </div>

    <div v-else class="dashboard-content">
      <div class="stats">
        <p>
          <strong>Nombre de projets</strong> 
          {{ stats.total_projects }}
        </p>
        <p>
          <strong>Nombre de tâches</strong> 
          {{ stats.total_tasks }}
        </p>
        <p>
          <strong>Tâches terminées</strong> 
          {{ stats.completed_tasks }}
        </p>
      </div>

      <div class="task-section">
        <div class="filter-container">
          <select v-model="filterStatus" aria-label="Filtrer par statut">
            <option value="">Toutes les tâches</option>
            <option value="todo">À faire</option>
            <option value="in_progress">En cours</option>
            <option value="done">Terminées</option>
          </select>
        </div>

        <ul class="task-list">
          <li 
            v-for="task in filteredTasks" 
            :key="task.id"
            :data-status="task.status"
          >
            <div class="task-title">{{ task.title }}</div>
            <div class="task-status">{{ getStatusLabel(task.status) }}</div>
          </li>
        </ul>
        
        <div v-if="filteredTasks.length === 0" class="no-tasks">
          Aucune tâche trouvée
        </div>
      </div>

      <div class="action-buttons">
        <button @click="downloadPDF" class="btn btn-primary">
          📄 Télécharger le Rapport PDF
        </button>
        
        <router-link to="/advanced-dashboard" class="btn btn-secondary">
          📊 Voir les Statistiques
        </router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Variables globales */
:root {
  /* Couleurs */
  --primary-color: #4361ee;
  --success-color: #2ecc71;
  --warning-color: #f39c12;
  --neutral-color: #6c757d;
  --light-color: #ffffff;
  --border-color: #e2e8f0;
  --bg-light: #f8f9fa;
  
  /* Espacements */
  --spacing-xs: 0.5rem;
  --spacing-sm: 0.75rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.2rem;
  --spacing-xl: 1.5rem;
  --spacing-xxl: 2rem;
  
  /* Bordures et ombres */
  --border-radius: 8px;
  --box-shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.05);
  --box-shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  
  /* Typographie */
  --font-size-sm: 0.85rem;
  --font-size-base: 0.95rem;
  --font-weight-medium: 500;
}

/* Base */
.dashboard {
  padding: var(--spacing-lg);
}

.dashboard h1 {
  margin-bottom: var(--spacing-xl);
}

.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xl);
}

/* Barre d'actions */
.actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
}

/* Boutons */
.btn {
  display: inline-flex;
  align-items: center;
  padding: var(--spacing-xs) var(--spacing-lg);
  border-radius: var(--border-radius);
  font-weight: var(--font-weight-medium);
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: var(--primary-color);
  color: var(--light-color);
  border: none;
  font-size: var(--font-size-base);
}

.btn:hover {
  transform: translateY(-2px);
  opacity: 0.95;
}

.btn-secondary {
  background-color: var(--success-color);
}

.btn-profile {
  background-color: var(--light-color);
  color: #2d3748;
  border: 1px solid var(--border-color);
}

.btn-profile:hover {
  background-color: var(--bg-light);
}

/* État de chargement */
.loading {
  display: flex;
  justify-content: center;
  padding: var(--spacing-xl);
  font-style: italic;
}

/* Statistiques */
.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-xl);
  margin-bottom: var(--spacing-xxl);
}

.stats p {
  background-color: var(--light-color);
  padding: var(--spacing-lg);
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow-md);
  text-align: center;
}

/* Section des tâches */
.task-section {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

/* Filtre */
.filter-container select {
  padding: var(--spacing-xs) var(--spacing-md);
  border-radius: var(--border-radius);
  border: 1px solid var(--border-color);
  background-color: var(--light-color);
  width: 100%;
  max-width: 300px;
  font-size: var(--font-size-base);
}

/* Liste des tâches */
.task-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.task-list li {
  padding: var(--spacing-md);
  border-radius: var(--border-radius);
  margin-bottom: var(--spacing-sm);
  background-color: var(--light-color);
  box-shadow: var(--box-shadow-sm);
  border-left: 4px solid var(--border-color);
}

.task-title {
  font-weight: var(--font-weight-medium);
}

.task-status {
  font-size: var(--font-size-sm);
  color: var(--neutral-color);
  margin-top: var(--spacing-xs);
}

/* Indicateurs de statut pour les tâches */
li[data-status="todo"] {
  border-left-color: var(--neutral-color);
}

li[data-status="in_progress"] {
  border-left-color: var(--warning-color);
}

li[data-status="done"] {
  border-left-color: var(--success-color);
}

/* Message vide */
.no-tasks {
  text-align: center;
  padding: var(--spacing-xl);
  color: var(--neutral-color);
  font-style: italic;
}

/* Boutons d'action en bas */
.action-buttons {
  display: flex;
  gap: var(--spacing-md);
  flex-wrap: wrap;
  margin-top: var(--spacing-lg);
}

/* Responsive */
@media (max-width: 768px) {
  .actions {
    flex-direction: column;
  }
  
  .btn, .btn-profile {
    width: 100%;
    justify-content: center;
  }
  
  .stats {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    flex-direction: column;
  }
}
</style>
