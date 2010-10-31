from PIL import Image
from zope.component import getUtility
from plone.app.imaging.interfaces import IImageTransformation


def applyTransforms(image, transforms):
    """ see `interfaces.py` """
    if not isinstance(image, Image.Image):
        image = Image.open(image)
    format = image.format                   # remember original format
    for name, parameters in transforms:
        transform = getUtility(IImageTransformation, name=name)
        image = transform(image, **parameters)
    return image, format



