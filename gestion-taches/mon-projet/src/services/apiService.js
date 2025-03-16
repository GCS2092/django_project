import { getToken } from "./authService";
import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api";

// Fonction générique pour les requêtes API
const apiRequest = async (url, method = "GET", body = null) => {
  const token = getToken();
  if (!token) throw new Error("Token manquant. Veuillez vous reconnecter.");

  const headers = { 
    "Accept": "application/json", //  Pour éviter des erreurs de parsing
    "Authorization": `Bearer ${token}`
  };

  const options = { method, headers };
  if (body) {
    headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(body);
  }

  const response = await fetch(`${API_BASE_URL}${url}`, options);
  if (!response.ok) throw new Error(`Erreur API: ${response.status}`);

  return response.json();
};

//  Récupérer les statistiques du tableau de bord
export const fetchDashboardData = () => apiRequest("/dashboard/");

//  Récupérer toutes les tâches
export const fetchTasks = () => apiRequest("/tasks/");

//  Récupérer les projets
export const fetchProjects = () => apiRequest("/projects/");


//  Récupérer les tâches d'un projet
export const fetchCalendarTasks = async () => {
  const token = getToken();  // Vérifie si le token est bien stocké
  if (!token) throw new Error("Token manquant");

  const response = await fetch("http://127.0.0.1:8000/api/tasks/calendar/", {
    headers: { Authorization: `Bearer ${token}` }, // Assure-toi que le token est bien inclus
  });

  if (!response.ok) throw new Error(`Erreur API: ${response.status}`);

  return response.json();
};


//  Télécharger le PDF
export const downloadPDF = async () => {
  const token = getToken();
  const url = `${API_BASE_URL}/generate-report/`;

  try {
    const response = await fetch(url, { headers: { Authorization: `Bearer ${token}` } });

    console.log(" Réponse de l'API PDF :", response);

    if (!response.ok) {
      throw new Error(`Erreur lors du téléchargement - Code: ${response.status}`);
    }

    const blob = await response.blob();
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "rapport_taches.pdf";
    link.click();
  } catch (error) {
    console.error(" Erreur PDF:", error);
  }
};

//  Ajouter un commentaire
export const addComment = (content) => apiRequest("/comments/", "POST", { content });

//  Récupérer les statistiques
export const fetchStats = async () => apiRequest("/dashboard/");

//  Récupérer le rôle de l'utilisateur
export async function fetchUserRole() {
  const token = getToken();
  console.log(" Token utilisé dans fetchUserRole:", token); // Vérifier ce qui est récupéré

  if (!token) {
    console.error(" Erreur: Token non disponible");
    return null;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/user-role/`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!response.ok) throw new Error("Erreur API lors de la récupération du rôle");

    const data = await response.json();
    console.log(" Rôle utilisateur récupéré:", data.role);
    return data.role;
  } catch (error) {
    console.error(" Erreur lors de la récupération du rôle:", error);
    return null;
  }
}

//  Récupérer les primes des enseignants
export const fetchTeacherBonuses = () => apiRequest("/teacher-bonus/");

//  Récupérer les informations du profil utilisateur
export const fetchUserProfile = async () => {
  const token = getToken();
  try {
    const response = await fetch(`${API_BASE_URL}/profile/`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!response.ok) throw new Error("Erreur lors de la récupération du profil");

    return response.json();
  } catch (error) {
    console.error(" Erreur lors de la récupération du profil :", error);
    return null;
  }
};

//  Mettre à jour le profil utilisateur (y compris l'image)
export const updateProfile = async (formData) => {
  const token = getToken();
  
  try {
    const response = await fetch(`${API_BASE_URL}/profile/`, {
      method: "PUT",
      headers: { Authorization: `Bearer ${token}` }, //  Pas de "Content-Type"
      body: formData, //  Supporte les fichiers
    });

    if (!response.ok) throw new Error("Erreur lors de la mise à jour du profil");

    return response.json();
  } catch (error) {
    console.error(" Erreur lors de la mise à jour du profil :", error);
    throw error;
  }
};

export const fetchUserProfileView = async () => {
  const token = getToken();
  const response = await fetch(`${API_BASE_URL}/profile/view/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!response.ok) throw new Error("Erreur lors de la récupération du profil");
  return response.json();
};
export const updateUserProfile = async (formData) => {
  const token = getToken();
  const response = await fetch(`${API_BASE_URL}/profile/`, {
      method: "PUT",
      headers: { Authorization: `Bearer ${token}` },
      body: formData, // FormData pour supporter les fichiers
  });
  if (!response.ok) throw new Error("Erreur lors de la mise à jour du profil");
  return response.json();
}

export const fetchProfile = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/api/profile/", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      },
    });
    return response.data;
  } catch (error) {
    console.error("❌ Erreur lors de la récupération du profil :", error);
    throw error;
  }
};