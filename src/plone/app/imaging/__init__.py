from plone.app.imaging.monkey import patchImageField
from plone.app.imaging.monkey import patchSchemas


def initialize(context):
    patchImageField()       # patch ImageField's `getAvailableSizes` method
    patchSchemas()          # patch ATCT schemas with `sizes` attribute
