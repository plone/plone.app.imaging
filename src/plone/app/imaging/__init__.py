from plone.app.imaging.monkey import patchATImageSchema
from plone.app.imaging.monkey import patchAvailableSizes
patchATImageSchema()    # patch ATImageSchema 'sizes' attrribute
patchAvailableSizes()   # patch ImageField's `getAvailableSizes` method
