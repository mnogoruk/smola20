import secrets
import string

from authentication.models import Account, Operator
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
        self.user = None

    def create(self):
        try:
            account = self._create()
            self.info(f'Successfully created user {self.username}.')
        except Exception:
            self.exception("Error while creating user.")
            raise self.CreateException()

        self._send_email()
        self.user = account
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


class UpdateUserService(LoggerService):

    def __init__(self, user, user_data):
        self.user: Account = user
        self.user_data: dict = user_data

    def update(self):
        try:
            self._update()
        except Exception:
            self.exception(f"Error while updating user: {self.user}")
            raise self.UpdateUserError
        try:
            self._update_operator_name()
        except Exception:
            self.exception(f"Error while updating operator for user: {self.user}")
            raise self.UpdateOperatorError
        self.info(f"Successfully updated user: {self.user}")

    def change_password(self):
        old_password = self.user_data['old_password']
        new_password = self.user_data['password']

        if self.user.check_password(old_password):
            try:
                self.user.set_password(new_password)
                self.user.save()
            except Exception:
                self.ChangePasswordError(code=self.ChangePasswordError.CAN_NOT_SET_PASSWORD)
        else:
            self.info(f"Unsuccessful attempt to change password for user {self.user}")
            raise self.ChangePasswordError(code=self.ChangePasswordError.INCORRECT_OLD_PASSWORD)
        self.info(f"Successfully changed password for user {self.user}")

    def _update(self):
        if 'username' in self.user_data:
            self.user.username = self.user_data['username']
        if 'first_name' in self.user_data:
            self.user.first_name = self.user_data['first_name']
        if 'last_name' in self.user_data:
            self.user.last_name = self.user_data['last_name']
        if 'email' in self.user_data:
            self.user.email = self.user_data['email']

        self.user.save()

    def _update_operator_name(self):
        d = []
        if self.user.first_name:
            d.append(self.user.first_name)
        if self.user.last_name:
            d.append(self.user.last_name)

        if len(d) > 0:
            new_name = " ".join(d)
            if new_name:
                Operator.objects.filter(user=self.user).update(name=new_name)

    class UpdateUserError(Exception):
        def __init__(self, message="Error while updating user"):
            self.message = message
            super().__init__(self.message)

    class UpdateOperatorError(Exception):
        def __init__(self, message="Error while updating operator"):
            self.message = message
            super().__init__(self.message)

    class ChangePasswordError(Exception):
        INCORRECT_OLD_PASSWORD = 1
        CAN_NOT_SET_PASSWORD = 2

        def __init__(self, message="Error while changing password", code=CAN_NOT_SET_PASSWORD):
            self.message = message
            self.code = code
            super().__init__(self.message)
