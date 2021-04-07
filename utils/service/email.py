from django.core.mail import send_mail
from django.conf import settings

from utils.service.logging import LoggerService


class EmailService(LoggerService):
    sender = settings.EMAIL_HOST_USER

    def __init__(self, subject, body, destination_email):
        self.subject = subject
        self.body = body
        self.destination = destination_email

    def send(self):
        try:
            send_mail(self.subject, self.body, self.sender, [self.destination], fail_silently=False)
            self.info(f"Successfully sent email to {self.destination}.")
        except Exception:
            self.exception("Error while sending email.")
