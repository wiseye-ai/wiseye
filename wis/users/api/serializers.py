from django.contrib.auth import get_user_model
from rest_framework import serializers

from wis.users.models import User as UserType

User = get_user_model()


class UserSerializer(serializers.ModelSerializer[UserType]):
    class Meta:
        model = User
        fields = ["name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }


class UserLoginSerializer(serializers.Serializer):
    user_uuid = serializers.UUIDField()
    password = serializers.CharField()
