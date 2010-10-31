from PIL import Image
from zope.interface import implements
from zope.component import getUtility
from plone.app.imaging.interfaces import IImageTransformation
from plone.scale.scale import scalePILImage


def applyTransforms(image, transforms):
    """ see `interfaces.py` """
    if not isinstance(image, Image.Image):
        image = Image.open(image)
    format = image.format                   # remember original format
    for name, parameters in transforms:
        transform = getUtility(IImageTransformation, name=name)
        image = transform(image, **parameters)
    return image, format


class Scale(object):
    """ scale the given `PIL.Image` using the provided parameters """
    implements(IImageTransformation)

    def __call__(self, image, **parameters):
        return scalePILImage(image, **parameters)
