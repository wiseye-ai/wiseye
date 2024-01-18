from django.conf import settings
from django.contrib import admin, messages
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import decorators, get_user_model
from django.shortcuts import redirect
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import ClockedSchedule, CrontabSchedule, IntervalSchedule, PeriodicTask, SolarSchedule
from rest_framework.authtoken.models import TokenProxy

from wis.users.forms import UserAdminChangeForm, UserAdminCreationForm
from wis.users.models import UserImage, UserLogs
from wis.users.tasks import prepare_unknown_user_task, training_task

User = get_user_model()

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    # Force the `admin` sign in process to go through the `django-allauth` workflow:
    # https://django-allauth.readthedocs.io/en/stable/advanced.html#admin
    admin.site.login = decorators.login_required(admin.site.login)  # type: ignore[method-assign]


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    change_list_template = "users/users_lists.html"
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["email", "name", "is_superuser"]
    search_fields = ["name"]
    ordering = ["id"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("start-training/", self.train_model, name="start_training"),
            path("prepare-unknown-user/", self.prepare_unknown_user, name="prepare-unknown-user"),
        ]
        return my_urls + urls

    def train_model(self, request):
        training_task()
        messages.add_message(request, messages.SUCCESS, _("Started training."))

        return redirect(
            reverse(
                "admin:users_user_changelist",
            )
        )

    def prepare_unknown_user(self, request):
        try:
            prepare_unknown_user_task()
        except ValueError as e:
            messages.add_message(request, messages.ERROR, str(e))
            return redirect(
                reverse(
                    "admin:users_user_changelist",
                )
            )

        messages.add_message(request, messages.SUCCESS, _("Started preparing unknown user."))
        return redirect(
            reverse(
                "admin:users_user_changelist",
            )
        )


@admin.register(UserImage)
class UserImageAdmin(admin.ModelAdmin):
    list_display = ["user"]
    search_fields = ["user_email"]
    autocomplete_fields = ["user"]


@admin.register(UserLogs)
class UserLogsAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(ClockedSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(PeriodicTask)
admin.site.unregister(SolarSchedule)
admin.site.unregister(TokenProxy)
