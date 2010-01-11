from Acquisition import aq_base
from Products.Archetypes.Field import ImageField
from Products.Archetypes.utils import shasattr
from Products.ATContentTypes.content.image import ATImageSchema
from plone.app.imaging.utils import getAllowedSizes

NOT_OVERRIDDEN_KEY = '_not_overridden_'

def getAvailableSizes(self, instance):
    """ get available sizes for scaled down images;  this uses the new,
        user-configurable settings, but still support instance methods
        and other callables;  see Archetypes/Field.py """
    sizes = getattr(aq_base(self), 'sizes', None)
    if isinstance(sizes, dict) and not sizes.has_key(NOT_OVERRIDDEN_KEY):
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

def patchATImageSchema():
    """ monkey patch the ATImageSchema 'sizes' attribute, to make it possible
        to detect whether the sizes has been overridden
    """
    ATImageSchema['image'].sizes[NOT_OVERRIDDEN_KEY] = (0,0)

def patchAvailableSizes():
    """ monkey patch ImageField's `getAvailableSizes` method """
    ImageField.original_getAvailableSizes = ImageField.getAvailableSizes
    ImageField.getAvailableSizes = getAvailableSizes

