from django.urls import path

from authentication.views.authentication_view import LoginView, RegisterView



urlpatterns = [
    path(
        "register",
        RegisterView.as_view(),
        name="register",
    ),
    path(
        "login",
        LoginView.as_view(),
        name="login",
    ),
]