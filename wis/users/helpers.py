import cv2 as cv
import numpy as np
from django.core.exceptions import ValidationError
from keras_facenet import FaceNet
from mtcnn import MTCNN

## Used for getting the embeddings of faces from photos. # noqa
embedder = FaceNet()


def detect_faces(image):
    """!
    Function used for detecting user face on the image. It uses MTCNN as a detector and then checks if there is a face.
    If so, an embedding is created using function get_embedding.

    @param image Image which is used for detecting a face.
    @return Embedding of the face image.
    """
    detector = MTCNN()
    image = (
        cv.imread(image)
        if isinstance(image, str)
        else cv.imdecode(np.asarray(bytearray(image.read()), dtype=np.uint8), cv.IMREAD_COLOR)
    )
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    if detector.detect_faces(image):
        x, y, w, h = detector.detect_faces(image)[0]["box"]
        image = image[y : y + h, x : x + w]
        image = cv.resize(image, (160, 160))
        embedding_ = get_embedding(image)

        return embedding_.tolist()
    raise ValidationError("No faces detected")


def get_embedding(face_img):
    """!
    Method used for getting the embedding for the image. In order to do that FaceNet class from keras_facenet is user.
    @param face_img Image of size 160x160px.
    @return Embeddings for the image.
    """
    face_img = face_img.astype("float32")
    face_img = np.expand_dims(face_img, axis=0)
    yhat = embedder.embeddings(face_img)
    return yhat[0]


def get_user_by_uuid(user_uuid):
    """!
    Function that looks for a User model instance with the given uuid.

    @param user_uuid User's uuid.
    @return User instance.
    """
    from wis.users.models import User

    return User.objects.filter(uuid=user_uuid, is_active=True).first()
