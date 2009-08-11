
from plone.app.imaging.monkey import patchAvailableSizes
patchAvailableSizes()   # patch ImageField's `getAvailableSizes` method
