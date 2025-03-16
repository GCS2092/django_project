<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { getToken, refreshToken } from "../services/authService";

const router = useRouter();
const projects = ref([]);
const selectedProjectTasks = ref([]); // 🔹 Stocke les tâches d'un projet sélectionné
const editingProject = ref(null);
const editedTitle = ref("");
const editedDescription = ref("");
const isLoading = ref(true);
const errorMessage = ref("");
const selectedProject = ref(null); // 🔹 Stocke le projet actuellement sélectionné
const newMemberId = ref(""); // 🔹 Stocke l'ID du nouvel utilisateur à ajouter

// Fonction pour afficher les erreurs
const showError = (message) => {
  errorMessage.value = message;
  setTimeout(() => {
    errorMessage.value = "";
  }, 3000);
};

// Récupération des projets
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
        "Content-Type": "application/json",
      },
    });

    if (response.status === 401) {
      token = await refreshToken();
      if (token) {
        response = await fetch("http://127.0.0.1:8000/api/projects/", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });
      } else {
        router.push("/login");
        return;
      }
    }

    if (!response.ok) throw new Error(`Erreur HTTP: ${response.status}`);

    projects.value = await response.json();
  } catch (error) {
    showError("Impossible de récupérer les projets");
    console.error("Erreur API :", error);
  } finally {
    isLoading.value = false;
  }
};

// Récupérer les tâches associées à un projet spécifique
const fetchProjectTasks = async (projectId) => {
  let token = getToken();
  if (!token) {
    router.push("/login");
    return;
  }

  try {
    let response = await fetch(`http://127.0.0.1:8000/api/projects/${projectId}/tasks/`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) throw new Error(`Erreur HTTP: ${response.status}`);

    selectedProjectTasks.value = await response.json();
    selectedProject.value = projects.value.find((p) => p.id === projectId);
  } catch (error) {
    showError("Erreur lors de la récupération des tâches");
    console.error("Erreur API :", error);
  }
};

// Supprimer un projet
const deleteProject = async (id) => {
  if (!confirm("Êtes-vous sûr de vouloir supprimer ce projet ?")) return;

  let token = getToken();
  if (!token) return;

  try {
    const response = await fetch(`http://127.0.0.1:8000/api/projects/${id}/`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!response.ok) throw new Error("Échec de la suppression");

    projects.value = projects.value.filter((project) => project.id !== id);
    showError("Projet supprimé avec succès");
  } catch (error) {
    showError("Erreur lors de la suppression");
    console.error("Erreur API :", error);
  }
};

// Modifier un projet
const startEditing = (project) => {
  editingProject.value = { ...project };
  editedTitle.value = project.title;
  editedDescription.value = project.description || "";
};

// Mettre à jour un projet
const updateProject = async () => {
  let token = getToken();
  if (!token || !editingProject.value) return;

  try {
    console.log("Données envoyées :", {
      title: editedTitle.value,
      description: editedDescription.value
    });

    const response = await fetch(
      `http://127.0.0.1:8000/api/projects/${editingProject.value.id}/`,
      {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          title: editedTitle.value,
          description: editedDescription.value,
        }),
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Erreur API :", errorData);
      throw new Error("Échec de la modification");
    }

    const updatedProject = await response.json();
    const index = projects.value.findIndex((p) => p.id === updatedProject.id);
    projects.value[index] = updatedProject;

    editingProject.value = null;
    alert("Projet mis à jour !");
  } catch (error) {
    console.error("Erreur lors de la modification :", error);
  }
};


// Voir les détails d'un projet
const viewProject = (id) => {
  router.push(`/projects/${id}`);
};

// Ajouter un membre au projet
const addMember = async () => {
  let token = getToken();
  if (!token || !selectedProject.value) return;

  try {
    const response = await fetch(`http://127.0.0.1:8000/api/projects/${selectedProject.value.id}/add_member/`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ user_id: newMemberId.value }),
    });

    if (!response.ok) throw new Error("Échec de l'ajout du membre");

    showError("Membre ajouté avec succès");
    newMemberId.value = "";
  } catch (error) {
    showError("Erreur lors de l'ajout du membre");
    console.error("Erreur API :", error);
  }
};

onMounted(fetchProjects);
</script>

<template>
  <div>
    <h2>Gestion des Projets</h2>

    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>

    <div v-if="isLoading">Chargement...</div>

    <div v-else>
      <ul>
        <li v-for="project in projects" :key="project.id">
          <strong>{{ project.title }}</strong> - {{ project.description || "Pas de description" }}

          <!-- Bouton pour voir les détails du projet -->
          <button @click="viewProject(project.id)">Voir</button>

          <!-- Bouton pour voir les tâches du projet -->
          <button @click="fetchProjectTasks(project.id)">Voir les tâches</button>

          <!-- Bouton pour modifier le projet -->
          <button @click="startEditing(project)">Modifier</button>

          <!-- Bouton pour supprimer le projet -->
          <button @click="deleteProject(project.id)">Supprimer</button>
        </li>
      </ul>
    </div>

    <!-- Affichage des tâches du projet sélectionné -->
    <div v-if="selectedProject">
      <h3>Tâches du projet : {{ selectedProject.title }}</h3>
      <ul v-if="selectedProjectTasks.length > 0">
        <li v-for="task in selectedProjectTasks" :key="task.id">
          <strong>{{ task.title }}</strong> - {{ task.status }}
        </li>
      </ul>
      <p v-else>Aucune tâche assignée à ce projet.</p>
      <input v-model="newMemberId" placeholder="ID utilisateur" />
      <button @click="addMember()">Ajouter au projet</button>
    </div>

    <!-- Formulaire de modification du projet -->
    <div v-if="editingProject">
      <h3>Modifier le projet</h3>
      <input v-model="editedTitle" placeholder="Titre" required />
      <textarea v-model="editedDescription" placeholder="Description"></textarea>
      <button @click="updateProject">Enregistrer</button>
      <button @click="editingProject = null">Annuler</button>
    </div>
  </div>
</template>

<style>
/* project-detail.css */
:root {
  --primary-color: #3498db;
  --light-color: #f5f7fa;
  --border-radius: 8px;
}

.project-detail {
  padding: 20px;
}

.project-detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.project-title {
  font-size: 1.8rem;
  font-weight: bold;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.btn {
  padding: 8px 15px;
  border-radius: var(--border-radius);
  border: none;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s;
}

.btn-primary {
  background-color: var(--primary-color);
  color: white;
}

.btn-secondary {
  background-color: white;
  color: var(--primary-color);
  border: 1px solid var(--primary-color);
}

.project-description {
  background-color: white;
  padding: 20px;
  border-radius: var(--border-radius);
  margin-bottom: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.project-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.project-tab {
  padding: 10px 20px;
  background-color: white;
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.project-tab.active {
  background-color: var(--primary-color);
  color: white;
}

.tab-content {
  background-color: white;
  padding: 20px;
  border-radius: var(--border-radius);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.members-list {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.member-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background-color: var(--light-color);
  border-radius: var(--border-radius);
}

.member-info {
  flex-grow: 1;
}

.member-role {
  font-size: 0.8rem;
  color: #666;
}
</style>