<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { getToken } from "../services/authService";

const route = useRoute();
const router = useRouter();
const projectTasks = ref([]);  
const projectTitle = ref("");  
const isLoading = ref(true);
const errorMessage = ref("");
const loadingTaskId = ref(null); 

const showError = (message) => {
  errorMessage.value = message;
  setTimeout(() => {
    errorMessage.value = "";
  }, 3000);
};

const updateTaskStatus = async (task) => {
  const token = getToken();
  if (!token) {
    errorMessage.value = "Vous devez être connecté !";
    return;
  }

  const newStatus = task.status;
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/tasks/${task.id}/`, {
      method: "PATCH",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ status: newStatus }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Impossible de mettre à jour la tâche.");
    }

    task.status = newStatus;
    alert("Statut mis à jour !");
  } catch (error) {
    errorMessage.value = "Erreur : " + error.message;
  }
};

const fetchProjectTasks = async () => {
  const token = getToken();
  if (!token) {
    router.push("/login");
    return;
  }

  try {
    const response = await fetch(`http://127.0.0.1:8000/api/tasks/?project=${route.params.id}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) throw new Error(`Erreur HTTP: ${response.status}`);

    const data = await response.json();
    projectTasks.value = data;  
  } catch (error) {
    showError("Impossible de récupérer les tâches du projet.");
    console.error("Erreur API:", error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(fetchProjectTasks);
</script>

<template>
  <div class="project-tasks-container">
    <div class="header">
      <button class="back-button" @click="router.push('/projects')">← Retour</button>
      <h2 class="page-title">Tâches du Projet</h2>
    </div>

    <div v-if="errorMessage" class="error-message">
      <span class="error-icon">⚠️</span> {{ errorMessage }}
    </div>

    <div v-if="isLoading" class="loading">
      <div class="spinner"></div>
      <span>Chargement...</span>
    </div>

    <div v-else class="tasks-content">
      <h3 class="project-title">{{ projectTitle }}</h3>

      <ul v-if="projectTasks.length > 0" class="task-list">
        <li v-for="task in projectTasks" :key="task.id" :class="{ done: task.status === 'done' }">
          <strong>{{ task.title }}</strong> - {{ task.description || "Pas de description" }}
          <span class="status">Statut : <b>{{ task.status }}</b></span>

          <label for="status">Modifier le statut :</label>
          <select v-model="task.status">
            <option value="todo">À faire</option>
            <option value="in_progress">En cours</option>
            <option value="done">Terminé</option>
          </select>
          <button @click="updateTaskStatus(task)">Mettre à jour</button>
        </li>
      </ul>

      <p v-else class="no-tasks">Aucune tâche n'est assignée à ce projet.</p>
    </div>
  </div>
</template>

<style>
/* project-task.css */
:root {
  --light-color: #f5f7fa;
  --border-radius: 8px;
  --primary-color: #3498db;
  --secondary-color: #2ecc71;
  --danger-color: #e74c3c;
  --warning-color: #f39c12;
}

.tasks-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.task-column {
  background-color: var(--light-color);
  border-radius: var(--border-radius);
  padding: 15px;
}

.column-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ddd;
}

.column-title {
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 5px;
}

.tasks-count {
  background-color: #ddd;
  border-radius: 12px;
  padding: 2px 8px;
  font-size: 0.8rem;
}

.task-card {
  background-color: white;
  border-radius: var(--border-radius);
  padding: 15px;
  margin-bottom: 10px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.task-title {
  font-weight: bold;
  margin-bottom: 10px;
}

.task-due-date {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 10px;
}

.task-assigned {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
}

.assigned-avatar {
  width: 25px;
  height: 25px;
  border-radius: 50%;
  background-color: var(--primary-color);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  font-weight: bold;
}

.task-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid #eee;
}

.task-actions {
  display: flex;
  gap: 10px;
}

.task-priority {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 0.8rem;
  font-weight: bold;
}

.priority-high {
  background-color: rgba(231, 76, 60, 0.2);
  color: var(--danger-color);
}

.priority-medium {
  background-color: rgba(241, 196, 15, 0.2);
  color: var(--warning-color);
}

.priority-low {
  background-color: rgba(46, 204, 113, 0.2);
  color: var(--secondary-color);
}

/* Styles pour les éléments spécifiques au template */
.project-tasks-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.back-button {
  background-color: var(--light-color);
  border: none;
  padding: 8px 15px;
  border-radius: var(--border-radius);
  cursor: pointer;
  margin-right: 15px;
}

.page-title {
  font-size: 1.5rem;
  margin: 0;
}

.error-message {
  background-color: rgba(231, 76, 60, 0.1);
  color: var(--danger-color);
  padding: 10px;
  border-radius: var(--border-radius);
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.error-icon {
  margin-right: 10px;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 50px 0;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top: 4px solid var(--primary-color);
  width: 30px;
  height: 30px;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.project-title {
  margin-bottom: 20px;
  color: var(--primary-color);
}

.task-list {
  list-style: none;
  padding: 0;
}

.task-list li {
  background-color: white;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: var(--border-radius);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.task-list li.done {
  background-color: rgba(46, 204, 113, 0.1);
  border-left: 4px solid var(--secondary-color);
}

.status {
  display: inline-block;
  padding: 3px 8px;
  background-color: var(--light-color);
  border-radius: 4px;
  font-size: 0.9rem;
}

.no-tasks {
  text-align: center;
  padding: 30px;
  background-color: var(--light-color);
  border-radius: var(--border-radius);
  color: #666;
}

select {
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ddd;
  margin-top: 5px;
}

button {
  background-color: var(--primary-color);
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  margin-top: 10px;
}

button:hover {
  opacity: 0.9;
}
</style>