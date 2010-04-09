from zope.interface import Interface, Attribute
from zope.schema import List, TextLine
from zope.i18nmessageid import MessageFactory
from Products.Archetypes.interfaces import IBaseObject as IATBaseObject

_ = MessageFactory('plone.app.imaging')


class IImagingSchema(Interface):
    """ schema for configlet form """

    allowed_sizes = List(title=_(u'Allowed image sizes'),
        description = _(u'Specify all allowed maximum image dimensions, one per line. '
                         'The required format is <name> <width>:<height>.'),
        value_type = TextLine(), default = [], required = False)


class IImageScale(Interface):
    """ representation of a scaled image, providing access to its metdata
        and actual payload data """

    id = Attribute('An identifier uniquely identifying this scale')
    width = Attribute('The pixel width of the image.')
    height = Attribute('The pixel height of the image.')
    url = Attribute('Absolute URL for this image.')
    mimetype = Attribute('The MIME-type of the image.')
    data = Attribute('The image data.')
    size = Attribute('The size of the image data in bytes.')
    filename = Attribute('The filename used for downloads.')


class IImageScaleFactory(Interface):
    """ adapter for image fields that allows generating scaled images """

    def create(context, **parameters):
        """ generate an image scale and return a tuple containing a
            representation of the actual image scale data (i.e. a string or
            file-like object) as well as the image's format and dimensions.
            for convenience, this happens to match the return value of
            `scaleImage`, but makes it possible to use different storages,
            i.e. zodb blobs """


class IImageScaling(Interface):
    """ adapter use for generating (and storing) image scales """

    def scale(fieldname, scalename=None, **parameters):
        """ retrieve a scale based on the given name or set of parameters.
            the parameters can be anything supported by `scaleImage` and
            would usually consist of at least a width & height.  returns
            either an object implementing `IImageScale` or `None` """


class IImageScaleHandler(Interface):
    """ handler for retrieving scaled versions of an image """

    def getScale(instance, scale):
        """ return scaled and aq-wrapped version for given image data """

    def createScale(instance, scale, width, height, data=None):
        """ create & return a scaled version of the image as retrieved
            from the field or optionally given data """


class IBaseObject(IATBaseObject):
    """ marker interface used to be able to avoid having to use
        `overrides.zcml` to register our version of the traversal adapter """
