from zope.interface import Interface
from zope.schema import List, TextLine, Int
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('plone.app.imaging')


class IImagingSchema(Interface):
    """ schema for configlet form """

    allowed_sizes = List(title=_(u'Allowed image sizes'),
        description = _(u'Specify all allowed maximum image dimensions, one per line. '
                         'The required format is "<name> <width>:<height>".'),
        value_type = TextLine(), default = [], required = False)

    quality = Int(title=_(u'Quality'),
        description = _(u'Specify the quality used when scaling images'),
        default = 88, required = False)


class IImageScaleHandler(Interface):
    """ handler for retrieving scaled versions of an image """

    def getScale(instance, scale):
        """ return scaled and aq-wrapped version for given image data """

    def createScales(instance):
        """ create all scales for this field on an instance"""

    def removeScales(instance):
        """ remove all scales for this field on an instance"""
        
