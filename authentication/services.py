import secrets
import string

from authentication.models import Account
from utils.service.email import EmailService
from utils.service.logging import LoggerService
from django.conf import settings


class CreateUserService(LoggerService):
    alphabet = string.ascii_letters + string.digits

    def __init__(self, user_data):
        self.password = self.generate_password()
        self.username = self.generate_username(user_data['role'])
        self.email = user_data['email']
        self.role = user_data['role']

    def create(self):
        try:
            account = self._create()
            self.info(f'Successfully created user {self.username}.')
        except Exception:
            self.exception("Error while creating user.")
            raise self.CreateException()

        self._send_email()
        return account

    def _create(self):
        return Account.objects.create_user(
            username=self.username,
            password=self.password,
            role=self.role,
            email=self.email
        )

    def _send_email(self):
        email = EmailService(
            subject=f'Приглашение от {settings.SITE_URL}',
            body=f'логин и пароль для smola20.ru\nusername: {self.username}\npassword: {self.password}',
            destination_email=self.email
        )
        email.send()

    @classmethod
    def get_role_name(cls, role):
        if role == 10:
            return 'DEFAULT'
        if role == 20:
            return 'STORAGE-WORKER'
        if role == 30:
            return 'OFFICE-WORKER'
        if role == 40:
            return 'ADMIN'
        else:
            return 'UNEXPECTED'

    @classmethod
    def generate_password(cls):
        return ''.join(secrets.choice(cls.alphabet) for _ in range(20))

    @classmethod
    def generate_username(cls, role):
        return f"{cls.get_role_name(role)}-{''.join(secrets.choice(cls.alphabet) for _ in range(6))}"

    class CreateException(Exception):

        def __init__(self, msg='Error while creating user.'):
            self.message = msg
            super().__init__(self.message)