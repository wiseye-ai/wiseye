import cv2 as cv
import numpy as np
from django.core.exceptions import ValidationError
from keras_facenet import FaceNet
from mtcnn import MTCNN

embedder = FaceNet()


def detect_faces(image):
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
    face_img = face_img.astype("float32")
    face_img = np.expand_dims(face_img, axis=0)
    yhat = embedder.embeddings(face_img)
    return yhat[0]
