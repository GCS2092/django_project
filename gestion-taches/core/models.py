from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class UserManager(BaseUserManager):
    def create_user(self, email, nom, role, password=None):
        if not email:
            raise ValueError("L'utilisateur doit avoir un email")
        user = self.model(email=self.normalize_email(email), nom=nom, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nom, password):
        user = self.create_user(email=email, nom=nom, role="admin", password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    
    ROLES = (
        ('admin', 'Admin'),
        ('professeur', 'Professeur'),
        ('etudiant', 'Etudiant')
    )
    prime = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    username = None  
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLES)
    is_professor = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom']

    def __str__(self):
        return f"{self.nom} - {self.role}"

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    members = models.ManyToManyField(User, related_name="project_members", blank=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'À faire'),
        ('in_progress', 'En cours'),
        ('done', 'Terminé')
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    due_date = models.DateField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")

    class Meta:
        ordering = ["due_date"]

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

@receiver(post_migrate)
def create_default_users(sender, **kwargs):
    if sender.name == 'core':
        User.objects.create_superuser(email="admin@scolarite.com", nom="Admin", password="admin123")
        User.objects.create_user(email="prof1@scolarite.com", nom="Professeur1", role="professeur", password="prof123")
        User.objects.create_user(email="etud1@scolarite.com", nom="Etudiant1", role="etudiant", password="etud123")
