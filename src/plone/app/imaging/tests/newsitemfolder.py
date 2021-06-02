"""
A folderish content type with an image field for testing such edge cases.
"""

from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import newsitem

ATNewsItemFolderSchema = (
    folder.ATBTreeFolderSchema.copy() + newsitem.ATNewsItemSchema.copy()
)

schemata.finalizeATCTSchema(ATNewsItemFolderSchema)


class ATNewsItemFolder(folder.ATBTreeFolder, newsitem.ATNewsItem):
    """
    A folderish content type with an image field for testing such edge cases.
    """

    schema = ATNewsItemFolderSchema

    portal_type = 'News Item Folder'
    archetype_name = 'News Item Folder'
    _atct_newTypeFor = {
        'portal_type': 'CMF News Item Folder',
        'meta_type': 'News Item Folder',
    }
    assocFileExt = ()


base.registerATCT(ATNewsItemFolder, "plone.app.imaging.tests")
