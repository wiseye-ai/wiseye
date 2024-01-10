import pickle

from django.contrib.auth import get_user_model
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC

from config import celery_app
from wis.users.models import UserImage

User = get_user_model()


@celery_app.task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()


@celery_app.task()
def training_task():
    encoder = LabelEncoder()
    user_images = (
        UserImage.objects.filter(embedding__isnull=False)
        .exclude(embedding=[])
        .values_list("embedding", "user__uuid")
        .distinct()
    )
    embeddings, user_uuids = zip(*user_images)

    encoder.fit(user_uuids)
    Y = encoder.transform(user_uuids)
    model = SVC(kernel="linear", probability=True)
    model.fit(embeddings, Y)
    pickle.dump(model, open("model.pkl", "wb"))
    pickle.dump(encoder, open("encoder.pkl", "wb"))
