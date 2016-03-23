from django.conf import settings
from django.core.mail import EmailMessage


class Email(object):

    def send_email(self, send_to, subject, attachment):
        email = EmailMessage(
            subject=subject,
            from_email=settings.EMAIL_FROM_ADDRESS,
            to=[send_to])
        email.attach_file(attachment)
        email.send(fail_silently=False)
