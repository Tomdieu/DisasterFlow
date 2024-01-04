from django.db import models

# Create your models here.

class User(models.Model):
    id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    profile_image = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)


    def __str__(self):
        return f"{self.username} - {self.type}"

class Chat(models.Model):

    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    is_group = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ChatUser(models.Model):

    id = models.BigIntegerField(primary_key=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="chat_users")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Message(models.Model):

    id = models.BigIntegerField(primary_key=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)