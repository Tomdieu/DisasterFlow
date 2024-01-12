from rest_framework.permissions import BasePermission


class IsCitizen(BasePermission):

    message = "You do not have the required role."

    def has_permission(self, request, view):
        # Implement your logic to check if the user has the required role
        return request.user and request.user.type == 'Citizen'
