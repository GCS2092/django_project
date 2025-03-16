<script setup>
import NavBar from './components/NavBar.vue';
import { RouterView } from 'vue-router';
</script>

<template>
  <div class="app-wrapper">
    <NavBar />
    <RouterView />  <!-- C'est ici que les pages s'afficheront -->
  </div>
</template>

<style>
:root {
  --primary-color: #3498db;
  --primary-dark: #2980b9;
  --secondary-color: #2ecc71;
  --dark-color: #2c3e50;
  --light-color: #ecf0f1;
  --danger-color: #e74c3c;
  --warning-color: #f39c12;
  --text-color: #333;
  --border-radius: 6px;
  --box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  --transition: all 0.3s ease;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Roboto', sans-serif;
  background-color: #f8f9fa;
  color: var(--text-color);
  line-height: 1.6;
}

/* Layout principal */
.app-container {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 280px;
  background-color: var(--dark-color);
  color: white;
  padding: 20px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  transition: var(--transition);
  z-index: 1000;
}

.sidebar-collapsed {
  width: 80px;
}

.main-content {
  flex-grow: 1;
  padding: 20px;
  background-color: #f8f9fa;
  transition: var(--transition);
}

/* Navigation */
.top-navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 25px;
  background-color: white;
  box-shadow: var(--box-shadow);
  border-radius: var(--border-radius);
  margin-bottom: 20px;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--primary-color);
  display: flex;
  align-items: center;
}

.logo img {
  height: 32px;
  margin-right: 10px;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 10px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid var(--primary-color);
}

/* Menu sidebar */
.nav-menu {
  margin-top: 30px;
  list-style-type: none;
}

.nav-item {
  margin-bottom: 10px;
}

.nav-link {
  display: flex;
  align-items: center;
  color: rgba(255, 255, 255, 0.8);
  padding: 12px 15px;
  border-radius: var(--border-radius);
  text-decoration: none;
  transition: var(--transition);
}

.nav-link:hover, .nav-link.active {
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
}

.nav-link i {
  margin-right: 15px;
  font-size: 18px;
}

/* Cards et conteneurs */
.card {
  background-color: white;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  padding: 20px;
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--light-color);
}

.card-title {
  font-size: 1.25rem;
  font-weight: 500;
  color: var(--dark-color);
}

/* Grilles et tableaux */
.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th, .table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid var(--light-color);
}

.table th {
  background-color: var(--light-color);
  font-weight: 500;
}

.table tr:hover {
  background-color: rgba(0, 0, 0, 0.02);
}

/* Éléments de formulaires */
.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

.form-control {
  width: 100%;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: var(--border-radius);
  font-size: 16px;
  transition: var(--transition);
}

.form-control:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.2);
}

/* Boutons */
.btn {
  display: inline-block;
  padding: 10px 20px;
  border: none;
  border-radius: var(--border-radius);
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: var(--transition);
  text-align: center;
  text-decoration: none;
}

.btn-primary {
  background-color: var(--primary-color);
  color: white;
}

.btn-primary:hover {
  background-color: var(--primary-dark);
}

.btn-secondary {
  background-color: var(--secondary-color);
  color: white;
}

.btn-secondary:hover {
  background-color: #27ae60;
}

.btn-danger {
  background-color: var(--danger-color);
  color: white;
}

.btn-danger:hover {
  background-color: #c0392b;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 14px;
}

.btn-lg {
  padding: 12px 24px;
  font-size: 18px;
}

/* Badges et status */
.badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 50px;
  font-size: 12px;
  font-weight: 500;
  text-align: center;
}

.badge-primary {
  background-color: var(--primary-color);
  color: white;
}

.badge-success {
  background-color: var(--secondary-color);
  color: white;
}

.badge-warning {
  background-color: var(--warning-color);
  color: white;
}

.badge-danger {
  background-color: var(--danger-color);
  color: white;
}

/* Status des tâches */
.status-todo {
  background-color: var(--light-color);
}

.status-in-progress {
  background-color: var(--warning-color);
  color: white;
}

.status-completed {
  background-color: var(--secondary-color);
  color: white;
}

/* Alertes et notifications */
.alert {
  padding: 15px;
  border-radius: var(--border-radius);
  margin-bottom: 20px;
  border-left: 4px solid;
}

.alert-success {
  background-color: rgba(46, 204, 113, 0.1);
  border-left-color: var(--secondary-color);
}

.alert-warning {
  background-color: rgba(243, 156, 18, 0.1);
  border-left-color: var(--warning-color);
}

.alert-danger {
  background-color: rgba(231, 76, 60, 0.1);
  border-left-color: var(--danger-color);
}

/* Utilitaires */
.text-center {
  text-align: center;
}

.text-right {
  text-align: right;
}

.d-flex {
  display: flex;
}

.align-items-center {
  align-items: center;
}

.justify-content-between {
  justify-content: space-between;
}

.ml-2 {
  margin-left: 0.5rem;
}

.mr-2 {
  margin-right: 0.5rem;
}

.mt-3 {
  margin-top: 1rem;
}

.mb-3 {
  margin-bottom: 1rem;
}

/* Responsive */
@media screen and (max-width: 768px) {
  .app-container {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    position: sticky;
    top: 0;
  }
  
  .nav-link {
    justify-content: center;
  }
  
  .grid-container {
    grid-template-columns: 1fr;
  }
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.fade-in {
  animation: fadeIn 0.3s ease-in;
}

/* Thème spécifique ESMT */
.esmt-header {
  background-color: #004b87; /* Couleur ESMT bleue */
  color: white;
  padding: 10px 20px;
  text-align: center;
}

.professor-section {
  border-left: 3px solid var(--primary-color);
}

.student-section {
  border-left: 3px solid var(--secondary-color);
}

/* Tableaux de statistiques */
.stats-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background-color: white;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  padding: 20px;
  text-align: center;
  transition: var(--transition);
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: var(--primary-color);
  margin: 10px 0;
}

.stat-label {
  color: #777;
  font-size: 1rem;
}

/* Progression bars */
.progress-container {
  background-color: #e9ecef;
  border-radius: 4px;
  height: 8px;
  width: 100%;
  margin-bottom: 10px;
}

.progress-bar {
  height: 100%;
  border-radius: 4px;
  background-color: var(--primary-color);
}

.progress-completed {
  background-color: var(--secondary-color);
}

/* Tooltip */
.tooltip {
  position: relative;
  display: inline-block;
}

.tooltip .tooltip-text {
  visibility: hidden;
  width: 120px;
  background-color: var(--dark-color);
  color: white;
  text-align: center;
  border-radius: var(--border-radius);
  padding: 5px;
  position: absolute;
  z-index: 1;
  bottom: 125%;
  left: 50%;
  margin-left: -60px;
  opacity: 0;
  transition: opacity 0.3s;
}

.tooltip:hover .tooltip-text {
  visibility: visible;
  opacity: 1;
}

/* Améliorations et modernisations */
.app-wrapper {
  min-height: 100vh;
  background: linear-gradient(to bottom right, #f8f9fa, #ecf0f1);
}

/* Effets de glassmorphism pour les cartes importantes */
.glass-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

/* Boutons modernes avec effets de survol améliorés */
.btn-modern {
  background: linear-gradient(to right, var(--primary-color), var(--primary-dark));
  border-radius: 50px;
  box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
  transition: all 0.3s ease;
}

.btn-modern:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(52, 152, 219, 0.4);
}

.btn-modern:active {
  transform: translateY(-1px);
}

/* Amélioration des animations */
@keyframes slideInFromLeft {
  0% {
    transform: translateX(-30px);
    opacity: 0;
  }
  100% {
    transform: translateX(0);
    opacity: 1;
  }
}

.slide-in {
  animation: slideInFromLeft 0.4s ease-out;
}

/* Amélioration des barres de progression */
.progress-bar-animated {
  position: relative;
  overflow: hidden;
}

.progress-bar-animated::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 0.2) 50%,
    rgba(255, 255, 255, 0) 100%
  );
  animation: shine 1.5s infinite;
}

@keyframes shine {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

/* Améliorations pour le mode sombre */
.dark-mode {
  --text-color: #f8f9fa;
  --light-color: #343a40;
  background-color: #212529;
  color: #f8f9fa;
}

.dark-mode .card,
.dark-mode .top-navbar {
  background-color: #343a40;
  color: #f8f9fa;
}

.dark-mode .table th {
  background-color: #495057;
  color: #f8f9fa;
}

.dark-mode .form-control {
  background-color: #495057;
  color: #f8f9fa;
  border-color: #6c757d;
}

/* Amélioration des scrollbars */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>