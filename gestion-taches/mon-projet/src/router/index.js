import { createRouter, createWebHistory } from "vue-router";
import { getToken, fetchUserRole } from "../services/authService";
import AdvancedDashboard from "../views/AdvancedDashboard.vue";
import Dashboard from "../views/Dashboard.vue";
import Projects from "../views/Projects.vue";
import ProjectDetail from "../views/ProjectDetail.vue";
import ProjectTasks from "../views/ProjectTasks.vue";
import AddProject from "../views/AddProject.vue";
import AddTask from "../views/AddTask.vue";
import Login from "../views/Login.vue";
import ProfileView from "../views/ProfileView.vue";
import Register from "../views/Register.vue"; 
import ProfileDashboard from "../views/ProfileDashboard.vue";
const routes = [
  { path: "/", redirect: "/dashboard" },
  { path: "/dashboard", component: Dashboard },
  { path: "/projects", component: Projects },
  { path: "/profile/view", component: ProfileView, meta: { requiresAuth: true } },
  { path: "/projects/:id", component: ProjectDetail },
  { path: "/projects/:id/tasks", component: ProjectTasks },
  { path: "/add-project", component: AddProject, meta: { requiresRole: "admin" } },
  { path: "/add-task", component: AddTask, meta: { requiresRole: "admin" } },
  { path: "/register", component: Register },
  { path: "/profile", component: ProfileDashboard },
  { path: "/advanced-dashboard", component: AdvancedDashboard },
  { path: "/login", component: Login }
];
 
export default createRouter({
  history: createWebHistory(),
  routes,
});
