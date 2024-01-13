from django.db import models

# Create your models here.

class User(models.Model):
    
    pass


class Notifications(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="notifications")
    content = models.TextField()