from django.contrib import admin
from django.urls import path, include
from django.urls import path, include
from core.views import generate_report, get_user_role, dashboard_stats, register_user, update_teacher_bonuses
from rest_framework.routers import DefaultRouter
from core.views import teacher_bonus, view_profile, get_tasks_calendar, ProjectViewSet, TaskViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename="projects")
router.register(r'tasks', TaskViewSet, basename="tasks")

def home_view(request):
    from django.http import JsonResponse
    return JsonResponse({"message": "Bienvenue sur l'API de gestion des tâches !"})

urlpatterns = [
    path('', home_view),  # Page d'accueil pour éviter le 404
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
     path('api/register/', register_user, name='register_user'),
    path("api/update-bonuses/", update_teacher_bonuses, name="update_bonuses"),
     path('api/generate-report/', generate_report, name='generate_report'),
    path('api/user-role/', get_user_role, name='get_user_role'),  # Vérifie que cette ligne est bien là
    path('api/dashboard/', dashboard_stats, name='dashboard_stats'),  # Vérifie que cette ligne est bien là
    path('api/tasks/calendar/', get_tasks_calendar, name='tasks-calendar'),
    path("api/profile/view/", view_profile, name="view-profile"),
    path("api/teacher-bonus/", teacher_bonus, name="teacher-bonus"),
    path("api/projects/<int:project_id>/tasks/", TaskViewSet.as_view({"get": "list"}), name="project-tasks"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]