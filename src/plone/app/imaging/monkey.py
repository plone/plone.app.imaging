from Acquisition import aq_base
from Products.Archetypes.Field import ImageField
from Products.Archetypes.utils import shasattr
from Products.ATContentTypes.content.image import ATImageSchema
from plone.app.imaging.interfaces import IImageScaleHandler
from plone.app.imaging.utils import getAllowedSizes


def getAvailableSizes(self, instance):
    """ get available sizes for scaled down images;  this uses the new,
        user-configurable settings, but still support instance methods
        and other callables;  see Archetypes/Field.py """
    sizes = getattr(aq_base(self), 'sizes', None)
    if isinstance(sizes, dict):
        return sizes
    elif isinstance(sizes, basestring):
        assert(shasattr(instance, sizes))
        method = getattr(instance, sizes)
        data = method()
        assert(isinstance(data, dict))
        return data
    elif callable(sizes):
        return sizes()
    else:
        sizes = getAllowedSizes()
        if sizes is None:
            sizes = self.original_getAvailableSizes(instance)
        return sizes


def createScales(self, instance, value=None):
    """ creates scales and stores them; largely based on the version from
        `Archetypes.Field.ImageField` """
    sizes = self.getAvailableSizes(instance)
    handler = IImageScaleHandler(self)
    for name, size in sizes.items():
        width, height = size
        data = handler.createScale(instance, name, width, height, data=value)
        if data is not None:
            handler.storeScale(instance, name, **data)


def patchImageField():
    """ monkey patch `ImageField` methods """
    ImageField.original_getAvailableSizes = ImageField.getAvailableSizes
    ImageField.getAvailableSizes = getAvailableSizes
    ImageField.original_createScales = ImageField.createScales
    ImageField.createScales = createScales


def unpatchImageField():
    """ revert monkey patch regarding `ImageField` methods """
    ImageField.getAvailableSizes = ImageField.original_getAvailableSizes
    ImageField.createScales = ImageField.original_createScales


def patchImageSchema():
    """ monkey patch `sizes` attribute in `ATImageSchema` to make it
        possible to detect whether the sizes has been overridden """
    ATImageSchema['image'].sizes = None
