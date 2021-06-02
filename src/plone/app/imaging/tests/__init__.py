"""
Tests for Plone's imaging support.
"""

from Products.CMFCore.utils import ContentInit

from . import newsitemfolder  # noqa

PROJECTNAME = "plone.app.imaging.tests"

permissions = {
    "News Item Folder": "plone.app.imaging.tests: Add News Item Folder",
}


# Copied from Products.ATContentTypes
def initialize(context):
    from Products.Archetypes.atapi import process_types
    from Products.Archetypes.atapi import listTypes

    listOfTypes = listTypes(PROJECTNAME)

    content_types, constructors, ftis = process_types(
        listOfTypes,
        PROJECTNAME)

    allTypes = zip(content_types, constructors)
    for atype, constructor in allTypes:
        kind = "%s: %s" % (PROJECTNAME, atype.archetype_name)
        ContentInit(
            kind,
            content_types=(atype,),
            permission=permissions[atype.portal_type],
            extra_constructors=(constructor,),
            ).initialize(context)
