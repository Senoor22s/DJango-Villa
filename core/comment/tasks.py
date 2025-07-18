from celery import shared_task
from comment.models import Contact

@shared_task
def delete_all_contacts():
    count, _ = Contact.objects.all().delete()
    return f"Deleted {count} contacts."
