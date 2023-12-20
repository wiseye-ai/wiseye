from django.urls import include, path

app_name = "face-id"
urlpatterns = [
    path("", include("wis.users.urls.recognition", namespace="recognition")),
]
