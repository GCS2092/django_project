from rest_framework import serializers
from core.models import Project, Task, User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "profile_picture"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['email', 'nom', 'role', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            nom=validated_data['nom'],
            role=validated_data['role'],
            password=validated_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'nom', 'role']


class ProjectSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    members = UserSerializer(many=True, read_only=True)
    completion_rate = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'creator', 'members', 'completion_rate']

    def get_completion_rate(self, obj):
        total_tasks = Task.objects.filter(project=obj).count()
        completed_tasks = Task.objects.filter(project=obj, status='done').count()
        return round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 2)

    def validate_title(self, value):
        if Project.objects.filter(title=value).exists():
            raise serializers.ValidationError("Un projet avec ce titre existe déjà.")
        return value


class TaskSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'status_display', 'due_date', 'assigned_to', 'project']

    def get_status_display(self, obj):
        return obj.get_status_display()

    def validate_due_date(self, value):
        if value < serializers.DateField().to_representation(serializers.datetime.date.today()):
            raise serializers.ValidationError("La date d'échéance ne peut pas être dans le passé.")
        return value
