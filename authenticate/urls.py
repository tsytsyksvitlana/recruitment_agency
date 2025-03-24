from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from authenticate.views import (
    RecruiterCreateView,
    UserLoginView,
    UserLogoutView,
    UserRegisterView, IndexView
)

urlpatterns = [
    path("auth/register/", UserRegisterView.as_view(), name="register"),
    path("auth/login/", UserLoginView.as_view(), name="login"),
    path("auth/logout/", UserLogoutView.as_view(), name="logout"),
    path('', IndexView.as_view(), name='index'),
    path("create-recruiter/", RecruiterCreateView.as_view(), name="create_recruiter"),

    path(
        "api/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/v1/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "api/v1/token/verify/", TokenVerifyView.as_view(), name="token_verify"
    ),
]
