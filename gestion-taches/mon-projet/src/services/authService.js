export function getToken() {
  const token = localStorage.getItem("access_token");
  console.log("🔍 Token récupéré :", token);

  if (!token) {
    console.error("❌ Aucun token trouvé ! Redirection vers login...");
    window.location.href = "/login";
  }

  return token;
}


export async function fetchUserRole() {
  const token = getToken();
  if (!token) return null; // Retourne null si aucun token n'est disponible.

  try {
    const response = await fetch("http://127.0.0.1:8000/api/user-role/", {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!response.ok) {
      console.error(" Erreur API lors de la récupération du rôle :", response.status);
      return null;
    }

    const data = await response.json();
    return data.role;

  } catch (error) {
    console.error(" Erreur réseau lors de la récupération du rôle :", error);
    return null;
  }
}




export const refreshToken = async () => {
  const refresh = localStorage.getItem("refresh_token");
  if (!refresh) {
      throw new Error("Refresh token non disponible");
  }

  const response = await fetch("http://127.0.0.1:8000/api/token/refresh/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh }),
  });

  if (!response.ok) {
      throw new Error("Erreur lors du rafraîchissement du token");
  }

  const data = await response.json();
  localStorage.setItem("access_token", data.access);
  return data.access;
};

export const getUserRole = async () => {
  const token = getToken();
  if (!token) {
      throw new Error("Aucun token disponible.");
  }

  const response = await fetch("http://127.0.0.1:8000/api/user-role/", {
      headers: { Authorization: `Bearer ${token}` },
  });

  if (!response.ok) {
      throw new Error("Erreur lors de la récupération du rôle utilisateur.");
  }

  const data = await response.json();
  return data.role;
};
export function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  window.location.href = "/login";
}
export const fetchProjects = async () => {
  const token = localStorage.getItem("access_token");
  if (!token) {
      throw new Error("Token non disponible");
  }

  const response = await fetch("http://127.0.0.1:8000/api/projects/", {
      headers: { Authorization: `Bearer ${token}` }
  });

  if (!response.ok) {
      throw new Error(`Erreur API: ${response.status}`);
  }

  return response.json();
};
