from zope.component import adapts
from zope.interface import implements
from zope.publisher.interfaces import IRequest
from Products.Archetypes.interfaces import IBaseObject
from Products.Archetypes.interfaces import IImageField
from Products.Archetypes.Field import Image, HAS_PIL
from ZPublisher.BaseRequest import DefaultPublishTraverse
from plone.app.imaging.interfaces import IImageScaleHandler


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
                image = self.createScale(instance, scale, width, height)
                self.storeScale(instance, image)
                image = self.retrieveScale(instance, scale=scale)
            if image is not None and not isinstance(image, basestring):
                return image
        return None

    def createScale(self, instance, scale, width, height):
        """ create a scaled version of the image """
        field = self.context
        if HAS_PIL and width and height:
            image = field.getRaw(instance)
            if image:
                data = str(image.data)
                if data:
                    id = field.getName() + '_' + scale
                    imgdata, format = field.scale(data, width, height)
                    mimetype = 'image/%s' % format.lower()
                    image = Image(id, title=field.getName(), file=imgdata,
                        content_type=mimetype)
                    image.filename = field.getFilename(instance)
                    try:
                        delattr(image, 'title')
                    except (KeyError, AttributeError):
                        pass
                    return image
        return None

    def retrieveScale(self, instance, scale):
        """ retrieve a scaled version of the image """
        field = self.context
        return field.getScale(instance, scale=scale)

    def storeScale(self, instance, image):
        """ store a scaled version of the image """
        field = self.context
        field.getStorage(instance).set(image.getId(), instance, image,
            mimetype=image.content_type, filename=image.filename)

