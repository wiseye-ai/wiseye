import base64
import io
import json
import logging
import pickle

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from rest_framework import status

from wis.users.api.serializers import UserLoginSerializer
from wis.users.helpers import detect_faces, get_user_by_uuid
from wis.users.models import UserLogs, UserLogsType
from wis.users.tasks import training_task

User = get_user_model()

logger = logging.getLogger(__name__)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert self.request.user.is_authenticated  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_redirect_view = UserRedirectView.as_view()


def login_view(request, *args, **kwargs) -> HttpResponse:
    """
    Login view
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    return render(template_name="account/face_login.html", request=request)


def find_user_view(request, *args, **kwargs):
    photo = request.POST.get("photo", None)
    if photo is not None:
        _, str_img = photo.split(";base64")
        decoded_file = base64.b64decode(str_img)
        file = io.BytesIO(decoded_file)
        try:
            detect_face = detect_faces(file)
        except ValidationError as e:
            return JsonResponse(
                {"error": e.messages},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if detect_face is not None:
            encoder = pickle.load(open("encoder.pkl", "rb"))
            model = pickle.load(open("model.pkl", "rb"))
            pred = model.predict([detect_face])
            predicted = max(model.predict_proba([detect_face])[0])

            print(predicted)
            user_uuid = encoder.inverse_transform(pred)[0]

            if predicted > 0.8 and User.objects.filter(uuid=user_uuid, is_active=True).exists():
                print(user_uuid)
                return JsonResponse({"success": True, "user_uuid": user_uuid})
        UserLogs.create_logs()
        return JsonResponse({"success": False}, status=status.HTTP_400_BAD_REQUEST)


def log_user_activity(request: WSGIRequest, *args, **kwargs):
    body_unicode = request.body.decode("utf-8")
    json_body = json.loads(body_unicode)

    serializer = UserLoginSerializer(json_body)
    user = get_user_by_uuid(serializer.data.get("user_uuid"))
    if not user:
        UserLogs.create_logs()
        return JsonResponse({"success": False}, status=status.HTTP_401_UNAUTHORIZED)
    if user := authenticate(request, username=user.email, password=serializer.data.get("password")):
        if user.is_active:
            UserLogs.create_logs(user, UserLogsType.RECOGNIZED)
            return JsonResponse({"success": True})
        UserLogs.create_logs()
        return JsonResponse({"success": False}, status=status.HTTP_401_UNAUTHORIZED)

    UserLogs.create_logs(log_type=UserLogsType.WRONG_PASSWORD)
    return JsonResponse({"success": False}, status=status.HTTP_401_UNAUTHORIZED)


def training_model_view(request, *args, **kwargs):
    training_task()
    return JsonResponse({"success": True})
