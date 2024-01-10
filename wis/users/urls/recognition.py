from django.urls import path

from wis.users.views import find_user_view, log_user_activity, login_view, training_model_view

app_name = "recognition"
urlpatterns = [
    path("face-login/", login_view, name="login"),
    path("classify/", find_user_view, name="classify"),
    path("training-model/", training_model_view, name="training"),
    path("log-activity/", log_user_activity, name="log-activity"),
]
