from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import UserCreateView, UserListView, UserEditView, UserChangePasswordView, UserDeleteView, \
    CheckView, AccountDetailView, TokenObtainPairWithRoleView

urlpatterns = [
    path('token/', TokenObtainPairWithRoleView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('account/check/', CheckView.as_view(), name='user_check'),
    path('account/', AccountDetailView.as_view(), name='user_detail'),
    path('account/create/', UserCreateView.as_view(), name='user_create'),
    path('account/list/', UserListView.as_view(), name='user_list'),
    path('account/edit/', UserEditView.as_view(), name='user_edit'),
    path('account/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('account/change-password/', UserChangePasswordView.as_view(), name='user_change_password'),
]
