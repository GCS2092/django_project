<template>
  <div class="projects-container">
    <h1 class="projects-title">Liste des Projets</h1>
    
    <div v-if="loading" class="loading-spinner">
      <div class="spinner"></div>
      <p>Chargement des projets...</p>
    </div>
    
    <div v-else-if="error" class="error-message">
      <p>{{ error }}</p>
      <button @click="fetchProjects" class="retry-button">Réessayer</button>
    </div>
    
    <ul v-else-if="projects.length" class="projects-list">
      <li v-for="project in projects" :key="project.id" class="project-item">
        <div class="project-card">
          <h3 class="project-title">{{ project.title }}</h3>
          <p v-if="project.description" class="project-description">{{ project.description }}</p>
          <div class="project-meta">
            <span v-if="project.date" class="project-date">{{ project.date }}</span>
            <span v-if="project.status" :class="['project-status', `status-${project.status.toLowerCase()}`]">
              {{ project.status }}
            </span>
          </div>
        </div>
      </li>
    </ul>
    
    <div v-else class="empty-state">
      <p>Aucun projet disponible pour le moment.</p>
    </div>
  </div>
</template>

<script>
import apiClient from '../axios.js';

export default {
  data() {
    return {
      projects: [],
      loading: true,
      error: null
    };
  },
  created() {
    this.fetchProjects();
  },
  methods: {
    async fetchProjects() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await apiClient.get('projects/');
        this.projects = response.data;
      } catch (error) {
        console.error("⛔ Erreur lors de la récupération des projets :", error);
        this.error = "Impossible de charger les projets. Veuillez réessayer plus tard.";
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>.projects-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2.5rem;
  font-family: 'Poppins', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #2c3e50;
  background-color: #f9fafc;
}

.projects-title {
  font-size: 2.5rem;
  margin-bottom: 2.5rem;
  color: #2c3e50;
  text-align: center;
  font-weight: 700;
  position: relative;
  padding-bottom: 1rem;
}

.projects-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 4px;
  background: linear-gradient(90deg, #3498db, #2980b9);
  border-radius: 2px;
}

.projects-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2.5rem;
  padding: 0;
  list-style-type: none;
}

.project-item {
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  perspective: 1000px;
}

.project-item:hover {
  transform: translateY(-10px);
}

.project-card {
  background: linear-gradient(135deg, #ffffff, #f5f7fa);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 1.8rem;
  transition: all 0.3s ease;
  border: 1px solid rgba(52, 152, 219, 0.1);
  position: relative;
}

.project-card:hover {
  box-shadow: 0 15px 35px rgba(52, 152, 219, 0.15);
  border-color: rgba(52, 152, 219, 0.2);
}

.project-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 5px;
  background: linear-gradient(90deg, #3498db, #2980b9);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.3s ease;
}

.project-card:hover::before {
  transform: scaleX(1);
}

.project-title {
  font-size: 1.4rem;
  margin-top: 0;
  margin-bottom: 1.2rem;
  color: #2c3e50;
  font-weight: 600;
  line-height: 1.3;
  position: relative;
  padding-bottom: 0.6rem;
}

.project-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 50px;
  height: 2px;
  background-color: rgba(52, 152, 219, 0.5);
  transition: width 0.3s ease;
}

.project-card:hover .project-title::after {
  width: 80px;
}

.project-description {
  flex-grow: 1;
  margin-bottom: 1.2rem;
  color: #5d6778;
  line-height: 1.7;
  font-size: 0.95rem;
}

.project-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
  font-size: 0.9rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(44, 62, 80, 0.1);
}

.project-date {
  color: #7f8c8d;
  font-weight: 500;
  display: flex;
  align-items: center;
}

.project-date::before {
  content: '📅';
  margin-right: 0.4rem;
  font-size: 0.9rem;
}

.project-status {
  padding: 0.35rem 0.85rem;
  border-radius: 30px;
  font-weight: 500;
  text-align: center;
  text-transform: capitalize;
  letter-spacing: 0.5px;
  font-size: 0.8rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.project-card:hover .project-status {
  transform: scale(1.05);
}

.status-actif, .status-active {
  background: linear-gradient(135deg, #e3f7ea, #d4f8e8);
  color: #27ae60;
  border: 1px solid rgba(39, 174, 96, 0.2);
}

.status-terminé, .status-completed {
  background: linear-gradient(135deg, #e8f4f8, #d6edf7);
  color: #3498db;
  border: 1px solid rgba(52, 152, 219, 0.2);
}

.status-pause, .status-onhold {
  background: linear-gradient(135deg, #fef5e7, #fdebd0);
  color: #f39c12;
  border: 1px solid rgba(243, 156, 18, 0.2);
}

.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 250px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(52, 152, 219, 0.1);
  border-radius: 50%;
  border-top-color: #3498db;
  border-left-color: #3498db;
  animation: spin 1.2s ease-in-out infinite;
  margin-bottom: 1.5rem;
  box-shadow: 0 0 15px rgba(52, 152, 219, 0.1);
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-spinner p {
  color: #3498db;
  font-weight: 500;
  letter-spacing: 0.5px;
  animation: pulse 1.5s infinite ease-in-out;
}

@keyframes pulse {
  0%, 100% { opacity: 0.8; }
  50% { opacity: 1; }
}

.error-message {
  text-align: center;
  padding: 2.5rem;
  background: linear-gradient(135deg, #fee, #ffdfdf);
  border-radius: 12px;
  color: #e74c3c;
  box-shadow: 0 8px 20px rgba(231, 76, 60, 0.1);
  border: 1px solid rgba(231, 76, 60, 0.2);
}

.retry-button {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  color: white;
  border: none;
  padding: 0.6rem 1.5rem;
  border-radius: 30px;
  cursor: pointer;
  font-weight: 600;
  margin-top: 1.5rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 10px rgba(231, 76, 60, 0.3);
  letter-spacing: 0.5px;
}

.retry-button:hover {
  background: linear-gradient(135deg, #c0392b, #e74c3c);
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(231, 76, 60, 0.4);
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: linear-gradient(135deg, #f8f9fa, #f1f3f5);
  border-radius: 12px;
  color: #7f8c8d;
  border: 1px dashed #bdc3c7;
  margin: 2rem auto;
  max-width: 600px;
}

.empty-state p {
  font-size: 1.1rem;
  margin-bottom: 0;
  color: #7f8c8d;
  font-weight: 500;
}

.empty-state p::before {
  content: '📂';
  display: block;
  font-size: 3rem;
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .projects-container {
    padding: 1.5rem;
  }
  
  .projects-title {
    font-size: 1.8rem;
    margin-bottom: 1.8rem;
  }
  
  .projects-list {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .project-card {
    padding: 1.2rem;
  }
}

@media (max-width: 480px) {
  .projects-title {
    font-size: 1.6rem;
  }
  
  .project-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.8rem;
  }
  
  .project-status {
    align-self: flex-start;
  }
}

/* Animation pour l'apparition des cartes */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.project-item {
  animation: fadeIn 0.5s ease-out forwards;
}

.project-item:nth-child(1) { animation-delay: 0.1s; }
.project-item:nth-child(2) { animation-delay: 0.2s; }
.project-item:nth-child(3) { animation-delay: 0.3s; }
.project-item:nth-child(4) { animation-delay: 0.4s; }
.project-item:nth-child(5) { animation-delay: 0.5s; }
.project-item:nth-child(6) { animation-delay: 0.6s; }
</style>