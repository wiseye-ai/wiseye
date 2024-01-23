import pytest

from wis.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_user_count(settings):
    UserFactory.create_batch(3)
    settings.CELERY_TASK_ALWAYS_EAGER = True
