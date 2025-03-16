import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
  headers: { 'Content-Type': 'application/json' }
});

//  Ajout automatique du token à chaque requête
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

//  Intercepteur pour rafraîchir le token en cas d'erreur 401
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (!error.response) {
      console.error(" Erreur réseau ou serveur injoignable.");
      return Promise.reject(error);
    }

    if (error.response.status === 401) {
      console.warn(" Token expiré, tentative de rafraîchissement...");

      const refreshToken = localStorage.getItem('refresh_token');
      if (!refreshToken) {
        console.error(" Aucun refresh token trouvé.");
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(error);
      }

      try {
        const refreshResponse = await axios.post(
          'http://127.0.0.1:8000/api/token/refresh/',
          { refresh: refreshToken }
        );

        localStorage.setItem('access_token', refreshResponse.data.access);
        
        //  Réessaye la requête initiale avec le nouveau token
        error.config.headers.Authorization = `Bearer ${refreshResponse.data.access}`;
        return apiClient(error.config);
        
      } catch (refreshError) {
        console.error(" Échec du rafraîchissement du token :", refreshError);
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);

export default apiClient;
