from zope.component import adapts
from zope.interface import implements
from zope.publisher.interfaces import IRequest
from Products.Archetypes.interfaces import IImageField
from Products.Archetypes.Field import Image, HAS_PIL
from ZPublisher.BaseRequest import DefaultPublishTraverse
from plone.app.imaging.interfaces import IBaseObject
from plone.app.imaging.interfaces import IImageScaleHandler


class ImageScale(Image):
    """ extend image class from `Archetypes.Field` by making sure the title
        gets always computed and not calling `_get_content_type` even though
        an explicit type has been passed """

    def __init__(self, id, data, content_type, filename):
        self.__name__ = id
        self.filename = filename
        self.precondition = ''
        # `OFS.Image` has no proper support for file objects or iterators,
        # so we'll require `data` to be a string for now...
        assert isinstance(data, str), 'data must be a string'
        self.update_data(data, content_type, size=len(data))


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
