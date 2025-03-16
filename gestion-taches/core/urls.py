from django.urls import path, include
from core.views import get_tasks_calendar, profile_view, update_teacher_bonuses
from core.views import generate_report, teacher_bonus
from core.views import get_task_statistics
from core.views import UserProfileView
from rest_framework.routers import DefaultRouter
from core.views import (
    dashboard_stats, ProjectViewSet, TaskViewSet, UserViewSet, get_task_statistics,
    get_user_role, register_user
)

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')  # Ajout de basename
router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'users', UserViewSet, basename='users')
 
urlpatterns = [
    path('api/', include(router.urls)),  # <- Ceci doit être bien présent !
    path('api/user-role/', get_user_role, name='get_user_role'),
    path("api/update-bonuses/", update_teacher_bonuses, name="update_bonuses"),
    path('api/dashboard/', dashboard_stats, name='dashboard_stats'),
    path('api/register/', register_user, name='register_user'),
    path('api/task-stats/', get_task_statistics, name='task_stats'),
    path("api/teacher-bonus/", teacher_bonus, name="teacher-bonus"),
    path('api/generate-report/', generate_report, name='generate_report'),
    path("api/profile/", profile_view, name="profile"),
    path("api/profile/", UserProfileView.as_view(), name="profile"),
    path('tasks/calendar/', get_tasks_calendar, name='tasks-calendar'),
    path("api/task-statistics/", get_task_statistics, name="task-statistics"),
]
