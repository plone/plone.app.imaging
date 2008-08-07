from zope.component import adapts
from zope.publisher.interfaces import IRequest
from Products.Archetypes.interfaces import IBaseObject
from Products.Archetypes.atapi import ImageField
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
            available = field.getAvailableSizes(self.context)
            if scale in available or scale is None:
                image = field.getScale(self.context, scale=scale)
                if image is not None and not isinstance(image, basestring):
                    return image
        return self.fallback(request, name)

