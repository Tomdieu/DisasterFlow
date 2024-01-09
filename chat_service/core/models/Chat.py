from django.db import models

class Chat(models.Model):

    name = models.CharField(max_length=255, blank=True, null=True)
    is_group = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str_(self):
        return f"{self.name} - {self.is_group}"