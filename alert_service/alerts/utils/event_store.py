from alerts.models import Event

def create_event_store(event_type:str,data:dict):
    event = Event.objects.create(event_type=event_type,data=data)
    return event