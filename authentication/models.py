from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, User
from django.db import models

from authentication.manager import AccountManager, OperatorManager


class Account(AbstractBaseUser, PermissionsMixin):
    class RoleChoice(models.IntegerChoices):
        ADMIN = 40, 'Admin'
        OFFICE_WORKER = 30, 'Office worker'
        STORAGE_WORKER = 20, 'Storage worker'
        DEFAULT = 10, 'Default'

    username = models.CharField(max_length=100, unique=True)

    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    is_banned = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(max_length=200, null=True)
    role = models.IntegerField(choices=RoleChoice.choices, default=RoleChoice.DEFAULT)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = AccountManager()

    @property
    def is_active(self):
        return not self.is_banned

    def __str__(self):
        return self.username


class Operator(models.Model):
    class OperatorTypeChoice(models.TextChoices):
        USER = 'USR', 'User'
        ANONYMOUS = 'ANS', 'Anonymous'
        SYSTEM = 'STM', 'System'
        DEFAULT = 'DFT', 'Default'

    user = models.OneToOneField(Account,
                                on_delete=models.SET_NULL,
                                related_name='operator',
                                null=True,
                                blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    type = models.CharField(max_length=3, default=OperatorTypeChoice.DEFAULT)

    objects = OperatorManager()

    def __str__(self):
        return self.name
