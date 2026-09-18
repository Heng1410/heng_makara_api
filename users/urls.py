from django.urls import path

from users.views.user_view import MeView



urlpatterns = [
    path(
        "me",
        MeView.as_view(),
        name="me",
    ),
]

