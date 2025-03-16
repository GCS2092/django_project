from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from core.models import Project, Task, User
from core.serializers import ProjectSerializer, TaskSerializer, UserSerializer, RegisterSerializer
from core.permissions import IsAdminOrProfessor, IsTaskAssigneeOrAdmin, IsProjectOwnerOrAdmin
from core.services import generate_task_report
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from django.db.models.functions import ExtractMonth, ExtractYear
from datetime import datetime
from django.core.files.storage import default_storage
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from core.serializers import UserProfileSerializer
from django.contrib.auth import get_user_model

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            if "profile_picture" in request.FILES:
                image = request.FILES["profile_picture"]
                file_path = f"profile_pictures/{request.user.id}_{image.name}"
                default_storage.save(file_path, image)
                request.user.profile_picture = file_path
            request.user.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task_statistics(request):
    current_year = datetime.now().year
    tasks = Task.objects.filter(status="done", due_date__year=current_year)
    quarterly_stats = tasks.annotate(year=ExtractYear("due_date"), month=ExtractMonth("due_date"))\
        .values("year", "month").annotate(count=Count("id"))
    stats_by_quarter = {}
    for entry in quarterly_stats:
        year, month, quarter = entry["year"], entry["month"], (entry["month"] - 1) // 3 + 1
        stats_by_quarter.setdefault(year, {1: 0, 2: 0, 3: 0, 4: 0})[quarter] += entry["count"]
    return Response({"year": current_year, "quarterly_stats": stats_by_quarter})

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]  # Vérifie bien que les permissions sont OK

    def perform_create(self, serializer):
        """ Empêche les étudiants de créer un projet """
        if self.request.user.role not in ["admin", "professeur"]:
            return Response({"error": "Seuls les admins et professeurs peuvent créer un projet."}, status=403)

        serializer.save(creator=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Project.objects.all() if user.role == "admin" else Project.objects.filter(members=user)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsTaskAssigneeOrAdmin]

    def perform_create(self, serializer):
        project = get_object_or_404(Project, id=self.request.data.get("project"))
        assigned_user = get_object_or_404(User, id=self.request.data.get("assigned_to"))
        if self.request.user.role == "etudiant":
            return Response({"error": "Les étudiants ne peuvent pas assigner des professeurs."}, status=403)
        serializer.save(project=project, assigned_to=assigned_user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    user = request.user
    if user.role not in ["admin", "professeur"]:
        return Response({"message": "Accès refusé"}, status=403)
    stats = {
        "total_projects": Project.objects.count(),
        "total_tasks": Task.objects.count(),
        "completed_tasks": Task.objects.filter(status="done").count()
    }
    return Response(stats)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_report(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="rapport_taches.pdf"'
    return generate_task_report(response)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def teacher_bonus(request):
    if request.user.role not in ["admin", "professeur"]:
        return Response({"message": "Accès refusé"}, status=403)
    teachers = User.objects.filter(role="professeur")
    bonuses = {}
    for teacher in teachers:
        total_tasks = Task.objects.filter(assigned_to=teacher).count()
        completed_tasks = Task.objects.filter(assigned_to=teacher, status="done").count()
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        bonuses[teacher.nom] = "100K" if completion_rate == 100 else "30K" if completion_rate >= 90 else "0K"
    return JsonResponse({"bonuses": bonuses})

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    if request.method == 'GET':
        return Response({"id": user.id, "nom": user.nom, "email": user.email, "role": user.role, "prime": user.prime})
    elif request.method == 'PUT':
        data = request.data
        user.nom = data.get("nom", user.nom)
        user.email = data.get("email", user.email)
        if "password" in data and data["password"]:
            user.set_password(data["password"])
        if "profile_picture" in request.FILES:
            image = request.FILES["profile_picture"]
            file_path = f"profile_pictures/{user.id}_{image.name}"
            default_storage.save(file_path, image)
            user.profile_picture = file_path
        user.save()
        return Response({"message": "Profil mis à jour"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_role(request):
    """Retourne le rôle de l'utilisateur connecté."""
    return Response({"role": request.user.role})

@api_view(['POST'])
def register_user(request):
    """Inscription d'un nouvel utilisateur"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Inscription réussie !"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def update_teacher_bonuses(request):
    """Met à jour les primes des enseignants en fonction du taux d'achèvement des tâches"""
    
    teachers = User.objects.filter(role="professeur")
    bonuses = {}

    for teacher in teachers:
        total_tasks = Task.objects.filter(assigned_to=teacher).count()
        completed_tasks = Task.objects.filter(assigned_to=teacher, status="done").count()

        if total_tasks > 0:
            completion_rate = (completed_tasks / total_tasks) * 100
            if completion_rate == 100:
                teacher.prime = 100000  # Prime de 100K si 100% des tâches sont faites
            elif completion_rate >= 90:
                teacher.prime = 30000  # Prime de 30K si +90% des tâches sont faites
            else:
                teacher.prime = 0  # Pas de prime si moins de 90%
        else:
            teacher.prime = 0  # Aucun travail assigné

        teacher.save()
        bonuses[teacher.nom] = teacher.prime

    return JsonResponse({"bonuses": bonuses})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def view_profile(request):
    """Affiche le profil de l'utilisateur connecté."""
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tasks_calendar(request):
    """Récupère les tâches assignées à l'utilisateur connecté sous forme de calendrier"""
    tasks = Task.objects.filter(assigned_to=request.user).values('id', 'title', 'due_date', 'status')
    
    return Response(list(tasks))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """Affiche le profil de l'utilisateur connecté."""
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data)

 