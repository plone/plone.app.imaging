from Products.CMFCore.permissions import setDefaultRoles
from plone.app.imaging.monkey import patchImageField
from plone.app.imaging.monkey import patchSchemas

setDefaultRoles('Plone Site Setup: Imaging', ('Manager', 'Site Administrator'))

def initialize(context):
    patchImageField()       # patch ImageField's `getAvailableSizes` method
    patchSchemas()          # patch ATCT schemas with `sizes` attribute
