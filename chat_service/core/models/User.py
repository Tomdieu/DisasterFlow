from django.db import models

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