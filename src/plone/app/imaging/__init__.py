
def initialize(context):
    """ initializer called when used as a zope2 product """

    from plone.app.imaging.monkey import patchAvailableSizes
    patchAvailableSizes()   # patch ImageField's `getAvailableSizes` method
