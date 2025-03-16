<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const goToLogin = () => {
  router.push("/login");
};

const goToRegister = () => {
  router.push("/register");
};
</script>

<template>
  <div class="home-container">
    <!-- ✅ En-tête -->
    <header>
      <h1>Gestion des Tâches Collaboratives</h1>
      <nav>
        <button @click="goToLogin">Connexion</button>
        <button @click="goToRegister">Inscription</button>
      </nav>
    </header>

    <!-- ✅ Section principale -->
    <section class="hero">
      <h2>Organisez votre travail facilement</h2>
      <p>Créez, assignez et suivez vos tâches en équipe.</p>
      <button class="cta-btn" @click="goToRegister">Commencer maintenant</button>
    </section>

    <!-- ✅ Fonctionnalités -->
    <section class="features">
      <div class="feature">
        <h3>📌 Création de projets</h3>
        <p>Gérez vos projets avec une vue simplifiée.</p>
      </div>
      <div class="feature">
        <h3>📊 Statistiques avancées</h3>
        <p>Suivez l'évolution des tâches et la progression.</p>
      </div>
      <div class="feature">
        <h3>✅ Attribution des tâches</h3>
        <p>Assignez les tâches aux membres et suivez leurs statuts.</p>
      </div>
    </section>

    <!-- ✅ Pied de page -->
    <footer>
      <p>© 2025 Gestion des Tâches | Tous droits réservés</p>
    </footer>
  </div>
</template>

<style scoped>
/* ✅ Mise en page globale */
.home-container {
  font-family: 'Arial', sans-serif;
  text-align: center;
  padding: 20px;
}

/* ✅ En-tête */
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: #1e88e5;
  color: white;
}

nav button {
  margin: 0 10px;
  padding: 10px 15px;
  border: none;
  background: white;
  color: #1e88e5;
  cursor: pointer;
  border-radius: 5px;
  font-weight: bold;
}

nav button:hover {
  background: #e3f2fd;
}

/* ✅ Section hero */
.hero {
  margin: 40px 0;
}

.hero h2 {
  font-size: 2rem;
  color: #333;
}

.hero p {
  font-size: 1.2rem;
  color: #555;
}

.cta-btn {
  background: #2ecc71;
  color: white;
  padding: 12px 20px;
  border: none;
  font-size: 1.1rem;
  margin-top: 20px;
  cursor: pointer;
  border-radius: 5px;
}

.cta-btn:hover {
  background: #27ae60;
}

/* ✅ Section fonctionnalités */
.features {
  display: flex;
  justify-content: space-around;
  margin-top: 40px;
}

.feature {
  width: 30%;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* ✅ Pied de page */
footer {
  margin-top: 50px;
  padding: 10px;
  background: #333;
  color: white;
}
</style>
