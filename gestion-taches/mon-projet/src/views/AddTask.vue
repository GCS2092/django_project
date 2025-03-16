<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { getToken, getUserRole } from "../services/authService";

const router = useRouter();
const taskTitle = ref("");
const taskDescription = ref("");
const dueDate = ref("");
const assignedTo = ref("");
const projectId = ref(""); // Stocke l'ID du projet sélectionné
const userRole = ref("");
const errorMessage = ref("");

//  Vérifie si l'utilisateur a le droit d'ajouter une tâche
onMounted(async () => {
  userRole.value = await getUserRole();
  if (!userRole.value || !["admin", "professeur"].includes(userRole.value)) {
    alert("Accès refusé !");
    router.push("/dashboard");
  }
});

//  Fonction pour ajouter une tâche
const addTask = async () => {
  const token = getToken();
  if (!token) {
    alert("Accès refusé !");
    router.push("/login");
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:8000/api/tasks/", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title: taskTitle.value,
        description: taskDescription.value,
        due_date: dueDate.value,
        assigned_to: assignedTo.value,
        project: projectId.value,
        status: "in_progress", //  Correction ici
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(JSON.stringify(errorData, null, 2));
    }

    alert("Tâche ajoutée !");
    router.push("/dashboard");
  } catch (error) {
    errorMessage.value = "Erreur lors de l'ajout de la tâche : " + error.message;
  }
};

</script>

<template>
  <div>
    <h2>Ajouter une Tâche</h2>

    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>

    <form @submit.prevent="addTask">
      <label for="title">Titre :</label>
      <input v-model="taskTitle" id="title" required />

      <label for="description">Description :</label>
      <textarea v-model="taskDescription" id="description"></textarea>

      <label for="dueDate">Date d'échéance :</label>
      <input type="date" v-model="dueDate" id="dueDate" required />

      <label for="assignedTo">Assigner à :</label>
      <input type="number" v-model="assignedTo" id="assignedTo" required placeholder="ID utilisateur" />

      <label for="project">Projet :</label>
      <input type="number" v-model="projectId" id="project" required placeholder="ID du projet" />

      <button type="submit">Ajouter</button>
    </form>
  </div>
</template>