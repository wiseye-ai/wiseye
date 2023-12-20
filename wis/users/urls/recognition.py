from django.urls import path

from wis.users.views import find_user_view, login_view

app_name = "recognition"
urlpatterns = [
    path("face-login/", login_view, name="login"),
    path("classify/", find_user_view, name="classify"),
]
