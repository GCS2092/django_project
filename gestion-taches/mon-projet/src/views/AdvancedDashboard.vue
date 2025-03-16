<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { fetchDashboardData, fetchProjects, fetchTasks, downloadPDF, fetchUserRole, fetchTeacherBonuses } from "../services/apiService";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

const userProfile = ref({});

const router = useRouter();
const stats = ref({});
const errorMessage = ref("");
const selectedProject = ref("");
const projects = ref([]);
const tasks = ref([]);
const userRole = ref(null);
const teacherBonuses = ref({});

const fetchBonuses = async () => {
  try {
    const response = await fetchTeacherBonuses();
    teacherBonuses.value = response.bonuses; // Assurez-vous que la clé "bonuses" est bien présente dans l'API
    console.log("Primes reçues :", teacherBonuses.value);
  } catch (error) {
    console.error(" Erreur lors du chargement des primes :", error);
  }
};

const fetchData = async () => {
  try {
    console.log(" Token avant fetchUserRole:", localStorage.getItem("access_token"));

    userRole.value = await fetchUserRole();
    if (!userRole.value) {
      errorMessage.value = " Rôle utilisateur introuvable.";
      return;
    }

    stats.value = await fetchDashboardData();
    projects.value = await fetchProjects();
    tasks.value = await fetchTasks();
    
    renderCharts();
  } catch (error) {
    console.error(" Erreur lors du chargement des données :", error);
    errorMessage.value = "Erreur lors de la récupération des données.";
  }
};

const renderCharts = () => {
  setTimeout(() => {
    const tasksChart = document.getElementById("tasksChart");
    const projectsChart = document.getElementById("projectsChart");

    if (tasksChart) {
      new Chart(tasksChart.getContext("2d"), {
        type: "pie",
        data: {
          labels: ["Tâches Terminées", "Tâches en Cours"],
          datasets: [
            {
              data: [stats.value.completed_tasks, stats.value.total_tasks - stats.value.completed_tasks],
              backgroundColor: ["#2ecc71", "#f39c12"],
            },
          ],
        },
      });
    }

    if (projectsChart) {
      new Chart(projectsChart.getContext("2d"), {
        type: "bar",
        data: {
          labels: ["Total Projets"],
          datasets: [
            {
              data: [stats.value.total_projects],
              backgroundColor: ["#3498db"],
            },
          ],
        },
      });
    }
  }, 500);
};

onMounted(async () => {
  const role = await fetchUserRole();
  
  if (!role) {
    router.push("/login");
    return;
  }

  await fetchData();
  await fetchBonuses(); // Ajout correct de l'appel pour récupérer les primes
});
</script>

<template>
  <div class="advanced-dashboard">
    <h1 class="dashboard-title">Tableau de Bord Avancé 📊</h1>

    <button 
      @click="downloadPDF" 
      v-if="userRole === 'admin' || userRole === 'professeur'" 
      class="profile-btn primary">
       Télécharger le Rapport PDF
    </button>

    <h2 class="chart-title">💰 Primes des Enseignants</h2>
    <p v-if="userProfile">Prime : {{ userProfile.prime ? userProfile.prime : 'Non définie' }} FCFA</p>

    <ul class="profile-stats">
      <li v-for="(bonus, teacher) in teacherBonuses" :key="teacher" class="stat-item">
        <span class="stat-label">{{ teacher }}</span>
        <span class="stat-value bonus-amount">{{ bonus }}</span>
      </li>
    </ul>

    <div v-if="errorMessage" class="error-message">
      <span>{{ errorMessage }}</span>
    </div>

    <div v-else>
      <div class="dashboard-grid">
        <div class="chart-container medium">
          <canvas id="tasksChart"></canvas>
        </div>
        <div class="chart-container medium">
          <canvas id="projectsChart"></canvas>
        </div>
      </div>

      <h3 class="chart-title">Filtrer les Tâches par Projet :</h3>
      <select v-model="selectedProject" class="filter-select">
        <option value="">Tous les Projets</option>
        <option v-for="project in projects" :key="project.id" :value="project.id">
          {{ project.title }}
        </option>
      </select>

      <ul class="task-list">
        <li v-for="task in tasks" :key="task.id" class="timeline-item">
          <div class="timeline-content">
            <div class="timeline-header">
              <span class="timeline-title">{{ task.title }}</span>
              <span class="timeline-date">{{ task.status }}</span>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<style>
:root {
  --primary-color: #1e88e5;
  --primary-light: #bbdefb;
  --primary-dark: #1565c0;
  --secondary-color: #26a69a;
  --success-color: #43a047;
  --warning-color: #ff9800;
  --danger-color: #e53935;
  --info-color: #00acc1;
  --todo-color: #757575;
  --progress-color: #ff9800;
  --done-color: #4caf50;
  --gray-100: #f8f9fa;
  --gray-200: #e9ecef;
  --gray-300: #dee2e6;
  --gray-400: #ced4da;
  --gray-500: #adb5bd;
  --gray-600: #6c757d;
  --gray-700: #495057;
  --gray-800: #343a40;
  --text-color: #333333;
  --text-light: #757575;
  --border-color: #e0e0e0;
  --border-radius: 8px;
  --card-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  --transition: all 0.3s ease;
}

.advanced-dashboard {
  padding: 1.5rem;
  font-family: 'Roboto', sans-serif;
  color: var(--text-color);
}

/* Dashboard header */
.dashboard-title {
  font-size: 1.8rem;
  font-weight: 600;
  color: var(--primary-dark);
  margin-bottom: 2rem;
}

.dashboard-controls {
  display: flex;
  gap: 15px;
  align-items: center;
}

.time-period-selector {
  display: flex;
  align-items: center;
  background-color: white;
  border-radius: var(--border-radius);
  padding: 5px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
}

.period-option {
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: var(--transition);
}

.period-option.active {
  background-color: var(--primary-color);
  color: white;
}

/* Chart containers */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 20px;
  margin-bottom: 2rem;
}

.chart-container {
  background-color: white;
  padding: 1.5rem;
  border-radius: var(--border-radius);
  box-shadow: var(--card-shadow);
  transition: var(--transition);
}

.chart-container:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.chart-container.large {
  grid-column: span 12;
}

.chart-container.medium {
  grid-column: span 6;
}

.chart-container.small {
  grid-column: span 4;
}

@media (max-width: 992px) {
  .chart-container.medium,
  .chart-container.small {
    grid-column: span 6;
  }
}

@media (max-width: 768px) {
  .chart-container.medium,
  .chart-container.small {
    grid-column: span 12;
  }
}

.chart-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 1.2rem;
}

/* Profile stats */
.profile-stats {
  margin-top: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 15px;
  list-style: none;
  padding: 0;
  margin-bottom: 2rem;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid var(--border-color);
}

.stat-item:last-child {
  border-bottom: none;
}

.stat-label {
  color: var(--text-color);
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}

.stat-value {
  font-weight: 500;
}

.bonus-amount {
  background-color: rgba(67, 160, 71, 0.1);
  color: var(--success-color);
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9rem;
}

/* Button styles */
.profile-btn {
  padding: 10px 16px;
  border-radius: var(--border-radius);
  text-align: center;
  font-weight: 500;
  cursor: pointer;
  transition: var(--transition);
  border: none;
  display: inline-block;
  margin-bottom: 1.5rem;
}

.profile-btn.primary {
  background-color: var(--primary-color);
  color: white;
}

.profile-btn.primary:hover {
  background-color: var(--primary-dark);
}

/* Filter select */
.filter-select {
  padding: 8px 12px;
  border-radius: var(--border-radius);
  border: 1px solid var(--border-color);
  background-color: white;
  margin-bottom: 1.5rem;
  font-size: 1rem;
  width: 100%;
  max-width: 400px;
}

/* Task list */
.task-list {
  list-style: none;
  padding: 0;
}

.timeline-item {
  position: relative;
  margin-bottom: 1rem;
}

.timeline-content {
  background-color: var(--gray-100);
  padding: 15px;
  border-radius: var(--border-radius);
  transition: var(--transition);
}

.timeline-content:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transform: translateY(-2px);
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.timeline-title {
  font-weight: 500;
}

.timeline-date {
  font-size: 0.85rem;
  color: var(--text-light);
  padding: 4px 8px;
  border-radius: 4px;
  background-color: var(--gray-200);
}

/* Error message */
.error-message {
  padding: 1rem;
  background-color: rgba(229, 57, 53, 0.1);
  color: var(--danger-color);
  border-radius: var(--border-radius);
  margin-bottom: 1.5rem;
  font-weight: 500;
}
</style>