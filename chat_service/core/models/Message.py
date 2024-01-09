from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from . import Chat,User

def get_file_type(file_path:str):
    """
    Determine the file type based on the file extension.

    Parameters:
    - file_path (str): The path or name of the file.

    Returns:
    - str: The file type based on its extension.
    """
    # Extract the file extension from the file path

    if file_path:
        file_extension = file_path.split('.')[-1].lower()
        return file_extension
    return 'Unknown'


class Message(models.Model):

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    file = models.FileField(upload_to='media_message/',blank=True,null=True)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.chat.name} - {self.sender.username} - {self.text}"
    
    @property
    def file_type(self):
        if self.file:
            return get_file_type(self.file.name)
        return 'No File'