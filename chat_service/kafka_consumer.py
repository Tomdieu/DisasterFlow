from json import loads
import logging,os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alert_service.settings")
django.setup()


logging.basicConfig(level=logging.INFO)

from kafka import KafkaConsumer
from json import loads

consumer = KafkaConsumer(
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
        enable_auto_commit=False,
        value_deserializer=lambda x: loads(x.decode("utf-8")),
)