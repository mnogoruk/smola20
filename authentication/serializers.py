from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Account
from .services import CreateUserService, UpdateUserService


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, read_only=True)
    username = serializers.CharField(max_length=100, read_only=True)
    email = serializers.EmailField(max_length=200)

    class Meta:
        model = Account
        fields = ['role', 'password', 'username', 'email']

    def create(self, validated_data):
        service = CreateUserService(validated_data)
        try:
            account = service.create()
        except service.CreateException() as ex:
            raise APIException(ex.message)
        return account


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username', 'last_name', 'first_name', 'email']

    def update(self, instance, validated_data):
        service = UpdateUserService(instance, validated_data)
        try:
            service.update()
        except service.UpdateUserError as ex:
            raise APIException(ex.message)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        service = UpdateUserService(instance, validated_data)
        try:
            service.change_password()
        except service.ChangePasswordError as ex:
            if ex.code == service.ChangePasswordError.INCORRECT_OLD_PASSWORD:
                raise serializers.ValidationError({"old_password": "Incorrect old password"})
            else:
                raise APIException(ex.message)

    def create(self, validated_data):
        pass


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username', 'role', 'first_name', 'last_name', 'email']


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username', 'first_name', 'last_name', 'is_banned', 'email', 'role']


class TokenObtainPairWithRoleSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['role'] = user.role

        return token
