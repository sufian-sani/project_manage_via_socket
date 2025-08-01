# bugs/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from tracker.utils import send_bug_assignment_email
from .models import Bug  # or from bugs.models import Bug if needed

@receiver(post_save, sender=Bug)
def bug_created_handler(sender, instance, created, **kwargs):
    if created and instance.assigned_to:
        send_bug_assignment_email(instance)
