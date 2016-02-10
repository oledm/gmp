from rest_framework import permissions

class IsEmployeeIdent(permissions.BasePermission):
    def has_objects_permission(self, request, view, employee):
        if request.user:
            return request.user == employee
        return False
