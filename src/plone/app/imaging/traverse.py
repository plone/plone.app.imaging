import logging
from zope.component import adapts
from zope.globalrequest import getRequest
from zope.interface import implements
from zope.interface import alsoProvides
from zope.publisher.interfaces import IRequest
from Products.Archetypes.interfaces import IImageField
from Products.Archetypes.Field import HAS_PIL
from ZODB.POSException import ConflictError
from ZPublisher.BaseRequest import DefaultPublishTraverse
from plone.app.imaging.interfaces import IBaseObject
from plone.app.imaging.interfaces import IImageScaleHandler
from plone.app.imaging.scale import ImageScale

try:
    from plone.protect.interfaces import IDisableCSRFProtection
    HAS_AUTO_CSRF = True
except ImportError:
    logging.info("plone.protect < 3.0.0 no auto csrf protection")
    HAS_AUTO_CSRF = False


class ImageTraverser(DefaultPublishTraverse):
    """ traversal adapter for scaled down versions of image content """
    adapts(IBaseObject, IRequest)

    def fallback(self, request, name):
        return super(ImageTraverser, self).publishTraverse(request, name)

    def publishTraverse(self, request, name):
        schema = self.context.Schema()
        if '_' in name:
            fieldname, scale = name.split('_', 1)
        else:
            fieldname, scale = name, None
        field = schema.get(fieldname)
        handler = IImageScaleHandler(field, None)
        if handler is not None:
            image = handler.getScale(self.context, scale)
            if image is not None:
                return image
        return self.fallback(request, name)


class DefaultImageScaleHandler(object):
    """ default handler for creating and storing scaled version of images """
    implements(IImageScaleHandler)
    adapts(IImageField)

    def __init__(self, context):
        self.context = context

    def getScale(self, instance, scale):
        """ return scaled and aq-wrapped version for given image data """
        field = self.context
        available = field.getAvailableSizes(instance)
        if scale in available or scale is None:
            image = self.retrieveScale(instance, scale=scale)
            if not image:       # create the scale if it doesn't exist
                width, height = available[scale]
                data = self.createScale(instance, scale, width, height)
                if data is not None:
                    self.storeScale(instance, scale, **data)
                    image = self.retrieveScale(instance, scale=scale)
            if image is not None and not isinstance(image, basestring):
                return image
        return None

    def createScale(self, instance, scale, width, height, data=None):
        """ create & return a scaled version of the image as retrieved
            from the field or optionally given data """
        if HAS_AUTO_CSRF:
            # disable CRSF on scale generation (from 1.1/Plone 5 branch)
            req = getRequest()
            if req:
                alsoProvides(req, IDisableCSRFProtection)
        field = self.context
        if HAS_PIL and width and height:
            if data is None:
                image = field.getRaw(instance)
                if not image:
                    return None
                data = str(image.data)
            if data:
                id = field.getName() + '_' + scale
                try:
                    imgdata, format = field.scale(data, width, height)
                except (ConflictError, KeyboardInterrupt):
                    raise
                except Exception:
                    if not field.swallowResizeExceptions:
                        raise
                    else:
                        logging.exception('could not scale ImageField "%s" of %s',
                            field.getName(), instance.absolute_url())
                        return None
                content_type = 'image/%s' % format.lower()
                filename = field.getFilename(instance)
                return dict(id=id, data=imgdata.getvalue(),
                    content_type=content_type, filename=filename)
        return None

    def retrieveScale(self, instance, scale):
        """ retrieve a scaled version of the image """
        field = self.context
        return field.getScale(instance, scale=scale)

    def storeScale(self, instance, scale, **data):
        """ store a scaled version of the image """
        image = ImageScale(**data)
        field = self.context
        field.getStorage(instance).set(image.getId(), instance, image,
            mimetype=image.content_type, filename=image.filename)
