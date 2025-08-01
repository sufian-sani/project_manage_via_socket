# bugs/utils.py (create this file)

from django.core.mail import send_mail

from bugtracker import settings

def send_bug_assignment_email(bug):
    if bug.assigned_to:
        send_mail(
            subject="Bug Assigned",
            message="You have been assigned a new bug.",
            from_email=settings.DEFAULT_FROM_EMAIL,                # or use settings.DEFAULT_FROM_EMAIL
            recipient_list=["abu5suffian@gmail.com",],     # real recipient
            fail_silently=False,
        )
