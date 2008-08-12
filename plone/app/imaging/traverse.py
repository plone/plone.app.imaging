from zope.component import adapts
from zope.publisher.interfaces import IRequest
from Products.Archetypes.interfaces import IBaseObject
from Products.Archetypes.Field import ImageField, Image, HAS_PIL
from ZPublisher.BaseRequest import DefaultPublishTraverse


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
        if field is not None and isinstance(field, ImageField):
            instance = self.context
            available = field.getAvailableSizes(instance)
            if scale in available or scale is None:
                image = field.getScale(instance, scale=scale)
                if not image:       # create the scale if it doesn't exist
                    width, height = available[scale]
                    image = self.createScale(field, scale, width, height)
                    self.storeScale(field, image)
                    image = field.getScale(instance, scale=scale)
                if image is not None and not isinstance(image, basestring):
                    return image
        return self.fallback(request, name)

    def createScale(self, field, scale, width, height):
        """ create a scaled version of the image """
        instance = self.context
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

    def storeScale(self, field, image):
        """ store a scaled version of the image """
        instance = self.context
        field.getStorage(instance).set(image.getId(), instance, image,
            mimetype=image.content_type, filename=image.filename)

