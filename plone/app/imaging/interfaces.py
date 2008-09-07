from zope.interface import Interface
from zope.schema import List, TextLine
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('plone.app.imaging')


class IImagingSchema(Interface):
    """ schema for configlet form """

    allowed_sizes = List(title=_(u'Allowed image sizes'),
        description = _(u'Specify all allowed maximum image dimensions, one per line. '
                         'The required format is "<name> <width>:<height>".'),
        value_type = TextLine(), default = [], required = False)


class IImageScaleHandler(Interface):
    """ handler for retrieving scaled versions of an image """

    def getScale(instance, scale):
        """ return scaled and aq-wrapped version for given image data """


