import os
import pickle

from django.contrib.auth import get_user_model
from django.core.files import File
from django.utils.translation import gettext_lazy as _
from filer.models import Image
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC

from config import celery_app
from wis.users.models import User, UserImage

User = get_user_model()  # noqa


@celery_app.task()
def training_task():
    """!
    Method used for training the model. It goes through every UserImage instance in the system and assigns to them user
     uuids. Then, SVC model is fitted to the data and pickled to model.pkl file.

    """
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


@celery_app.task()
def prepare_unknown_user_task():
    """
    Method used for creating user instance that is used to teach model to not recognize users that are not
    registered in the system. It looks for inactive user with email "unknown@unknown.com" if it's not found,
    it's created. Then, training photos from directory /opt/project/wis/media/unknown/ are used to create UserImage
    instances for the user.
    """
    user, created = User.objects.get_or_create(email="unknown@unknown.com", defaults={"is_active": False})

    if not created:
        raise ValueError(_("User already exist"))

    directory_path = r"/opt/project/wis/media/unknown/"

    for filename in os.listdir(directory_path):
        if filename.endswith(".jpg"):
            with open(os.path.join(directory_path, filename), "rb") as img_file:
                org_file = File(img_file, name=filename)
                file_obj = Image.objects.create(file=org_file, name=filename)
                UserImage.objects.create(user=user, image=file_obj)
                print(f"Image object created for {filename}")
