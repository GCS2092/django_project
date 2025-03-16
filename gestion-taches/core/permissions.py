from rest_framework.permissions import BasePermission

class IsAdminOrProfessor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ["admin", "professeur"]

class IsProjectMemberOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.members.all() or request.user == obj.creator or request.user.role == "admin"

class IsTaskAssigneeOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.assigned_to or request.user.role == "admin"

class IsProjectOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.creator or request.user.role == "admin"
