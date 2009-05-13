from Acquisition import aq_base
from Products.Archetypes.Field import ImageField
from Products.Archetypes.utils import shasattr
from plone.app.imaging.utils import getAllowedSizes


def getAvailableSizes(self, instance):
    """ get available sizes for scaled down images;  this uses the new,
        user-configurable settings, but still support instance methods
        and other callables;  see Archetypes/Field.py """
    sizes = getattr(aq_base(self), 'sizes', None)
    if isinstance(sizes, basestring):
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


def patchAvailableSizes():
    """ monkey patch ImageField's `getAvailableSizes` method """
    ImageField.original_getAvailableSizes = ImageField.getAvailableSizes
    ImageField.getAvailableSizes = getAvailableSizes

