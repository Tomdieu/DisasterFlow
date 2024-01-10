from django.contrib import admin
from django.http.request import HttpRequest
from typing import Any

# Register your models here.

from .models import User,Chat,ChatUser,Message


class ReadOnlyAdmin(admin.ModelAdmin):

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    
    def has_change_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        return False
    
    def has_delete_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        return False

@admin.register(User)
class UserAdmin(ReadOnlyAdmin):

    list_display = ['id','username','email','phone_number','type','gender','profile_image']

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):

    list_display = ['id','name','is_group','is_active','created_at']

@admin.register(ChatUser)
class ChatUserAdmin(admin.ModelAdmin):

    list_display = ['id','chat','user','is_admin','created_at']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    list_display = ['id','chat','sender','text','file_type','is_deleted','created_at']
