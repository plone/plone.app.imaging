from plone.app.imaging.monkey import patchImageField
from plone.app.imaging.monkey import patchImageSchema


def initialize(context):
    patchImageField()       # patch ImageField's `getAvailableSizes` method
    patchImageSchema()      # patch ATImageSchema's `sizes` attrribute
