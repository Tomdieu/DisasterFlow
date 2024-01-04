import pika,json
import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat_service.settings")
django.setup()

from django.conf import settings

from core.models import User, Chat, Message