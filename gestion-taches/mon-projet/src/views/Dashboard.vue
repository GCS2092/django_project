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
/* Style des boutons */
.btn {
  display: inline-flex;
  align-items: center;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-weight: 500;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: #4361ee;
  color: white;
  border: none;
  font-size: 0.95rem;
}

.btn:hover {
  transform: translateY(-2px);
  opacity: 0.95;
}

.btn-secondary {
  background-color: #2ecc71;
}

.btn-profile {
  background-color: white;
  color: #2d3748;
  border: 1px solid #e2e8f0;
}

.btn-profile:hover {
  background-color: #f8f9fa;
}

/* Stats */
.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stats p {
  background-color: white;
  padding: 1.2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
}

/* Filtrage des tâches */
.filter-container select {
  padding: 0.6rem 1rem;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  background-color: white;
  width: 100%;
  max-width: 300px;
  font-size: 0.95rem;
}

/* Liste des tâches */
.task-list li {
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 0.75rem;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  border-left: 4px solid #e2e8f0;
}

.task-title {
  font-weight: 500;
}

.task-status {
  font-size: 0.85rem;
  color: #6c757d;
  margin-top: 0.5rem;
}

/* Tâches selon leur statut */
li[data-status="todo"] {
  border-left-color: #6c757d;
}

li[data-status="in_progress"] {
  border-left-color: #f39c12;
}

li[data-status="done"] {
  border-left-color: #2ecc71;
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
}
</style>
