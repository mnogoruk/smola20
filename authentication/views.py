from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Account
from .serializers import UserCreateSerializer, UserEditSerializer, UserSerializer, AccountSerializer, \
    TokenObtainPairWithRoleSerializer, ChangePasswordSerializer
from authentication.permissions import DefaultPermission, AdminPermission


class UserCreateView(CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = (IsAuthenticated, AdminPermission)


class UserEditView(UpdateAPIView):
    serializer_class = UserEditSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserListView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (AdminPermission,)

    def get_queryset(self):
        accounts = Account.objects.excluded_admins()
        return accounts


class UserChangePasswordView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user


class UserDeleteView(DestroyAPIView):
    permission_classes = (AdminPermission,)

    def get_object(self):
        data = self.request.data
        return


class CheckView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response(data={'correct': True}, status=status.HTTP_200_OK)


class AccountDetailView(RetrieveAPIView):
    permission_classes = (DefaultPermission,)
    serializer_class = AccountSerializer

    def get_object(self):
        return self.request.user


class TokenObtainPairWithRoleView(TokenObtainPairView):
    serializer_class = TokenObtainPairWithRoleSerializer