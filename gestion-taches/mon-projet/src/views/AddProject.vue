<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { getToken } from "../services/authService";

const router = useRouter();
const newProject = ref({ title: "", description: "", tasks: [] });
const errorMessage = ref("");

const addTask = () => {
  newProject.value.tasks.push({ title: "", description: "", due_date: "", assigned_to: "", status: "todo" });
};

const removeTask = (index) => {
  newProject.value.tasks.splice(index, 1);
};

const addProject = async () => {
  let token = getToken();
  if (!token) {
    errorMessage.value = "Vous devez être connecté !";
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:8000/api/projects/", {
      method: "POST",
      headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
      body: JSON.stringify(newProject.value),
    });

    if (!response.ok) throw new Error("Erreur lors de l'ajout du projet");

    router.push("/projects");  
  } catch (error) {
    errorMessage.value = error.message;
  }
};
</script>

<template>
  <div>
    <h2>Créer un Projet avec Tâches</h2>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

    <form @submit.prevent="addProject">
      <input v-model="newProject.title" placeholder="Titre du projet" required />
      <textarea v-model="newProject.description" placeholder="Description"></textarea>

      <h3>Ajouter des Tâches :</h3>
      <div v-for="(task, index) in newProject.tasks" :key="index">
        <input v-model="task.title" placeholder="Titre de la tâche" required />
        <textarea v-model="task.description" placeholder="Description"></textarea>
        <input type="date" v-model="task.due_date" required />
        <input v-model="task.assigned_to" placeholder="ID utilisateur" required />
        <select v-model="task.status">
          <option value="todo">À faire</option>
          <option value="in_progress">En cours</option>
          <option value="done">Terminé</option>
        </select>
        <button @click.prevent="removeTask(index)">Supprimer</button>
      </div>
      <button @click.prevent="addTask">+ Ajouter une Tâche</button>

      <button type="submit">Créer le projet avec les tâches</button>
    </form>
  </div>
</template>

<style>
/* add-project.css - Styles pour la page d'ajout de projet */

:root {
  --primary-color: #1e88e5;
  --primary-dark: #1565c0;
  --secondary-color: #f5f5f5;
  --success-color: #43a047;
  --warning-color: #ffb300;
  --danger-color: #e53935;
  --text-color: #333333;
  --text-light: #757575;
  --border-radius: 8px;
  --box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  --transition: all 0.3s ease;
}

div {
  max-width: 800px;
  margin: 2rem auto;
  padding: 20px;
  font-family: 'Roboto', sans-serif;
  color: var(--text-color);
}

h2 {
  font-size: 2rem;
  font-weight: 600;
  color: var(--primary-color);
  margin-bottom: 2rem;
  text-align: center;
}

h3 {
  font-size: 1.2rem;
  margin: 1.5rem 0 1rem;
  color: var(--primary-dark);
  border-bottom: 2px solid var(--primary-color);
  padding-bottom: 8px;
  font-weight: 600;
}

form {
  background-color: white;
  padding: 2rem;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
}

input, textarea, select {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #e0e0e0;
  border-radius: var(--border-radius);
  font-size: 1rem;
  transition: var(--transition);
  margin-bottom: 1rem;
}

input:focus, textarea:focus, select:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(30, 136, 229, 0.2);
  outline: none;
}

textarea {
  height: 120px;
  resize: vertical;
  line-height: 1.5;
}

input[type="date"] {
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="%23757575" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>');
  background-repeat: no-repeat;
  background-position: right 12px center;
  padding-right: 40px;
}

button {
  padding: 10px 20px;
  border-radius: var(--border-radius);
  font-weight: 500;
  font-size: 1rem;
  cursor: pointer;
  transition: var(--transition);
  border: none;
  text-align: center;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 120px;
  background-color: var(--primary-color);
  color: white;
  margin-right: 10px;
  margin-bottom: 10px;
}

button:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
}

button[type="submit"] {
  margin-top: 1.5rem;
  background-color: var(--success-color);
  width: 100%;
}

button[type="submit"]:hover {
  background-color: #388e3c;
}

.error-message {
  color: var(--danger-color);
  background-color: #ffebee;
  padding: 12px;
  border-radius: var(--border-radius);
  margin-bottom: 1.5rem;
  font-weight: 500;
  text-align: center;
}

/* Styles pour les tâches */
div[v-for] {
  background-color: var(--secondary-color);
  border-radius: var(--border-radius);
  padding: 15px;
  margin-bottom: 15px;
  border: 1px solid #e0e0e0;
}

/* Styles responsive */
@media (max-width: 768px) {
  div {
    padding: 15px;
  }
  
  form {
    padding: 1.5rem;
  }
  
  button {
    width: 100%;
  }
}
</style>