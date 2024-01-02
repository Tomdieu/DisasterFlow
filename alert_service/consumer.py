import pika,os,json
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alert_service.settings")
django.setup()

from django.conf import settings

from alerts.models import User,Profile

credentials = pika.PlainCredentials(settings.RABBITMQ_USERNAME, settings.RABBITMQ_PASSWORD)
parameters = pika.ConnectionParameters(settings.RABBITMQ_HOST, settings.RABBITMQ_PORT, settings.RABBITMQ_VHOST, credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='alert')


def callback(ch,method,properties,body):

    print(" [+] New Message Recieve")

channel.basic_consume(queue='alert',on_message_callback=callback,auto_ack=True)

print(" [+] Started Consuming")
channel.start_consuming()