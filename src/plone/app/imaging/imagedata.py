from zope.component import adapts
from zope.interface import implements
from zope.app.file.image import Image
from plone.scale.storage import IImageData
from plone.scale.storage import AnnotationStorage
from plone.scale.storage import IImageScaleStorage
from plone.dexterity.interfaces import IDexterityContent


class ZopeAppFileImageData(object):
    """Adapter to retrieve image data from a :class:`zope.app.file.iamge.Image`
    instance.
    """
    implements(IImageData)
    adapts(Image)

    def __init__(self, image):
        self.image=image

    @property
    def data(self):
        return self.image.data



class DexterityScaleStorage(AnnotationStorage):
    """Adapter to retrieve image data from a :class:`zope.app.file.iamge.Image`
    instance.
    """
    adapts(IDexterityContent)

    def _url(self, id):
        return "%s/++image++%s" % (self.context.absolute_url(), id)


    def _wrapImageData(self, fieldname, data, details):
        """Store images as a Image class, which the Zope publisher knows how to
        handle."""
        return Image(data, details["mimetype"])



from zope.publisher.interfaces import IRequest
from zope.traversing.interfaces import ITraversable
try:
    from zope.location.interfaces import LocationError
except ImportError:
    from zope.traversing.interfaces import TraversalError as LocationError

class ScaleTraverser(object):
    implements(ITraversable)
    adapts(IDexterityContent, IRequest)

    def __init__(self, context, request):
        self.context=context
        self.request=request

    def traverse(self, name, remaining):
        storage=IImageScaleStorage(self.context, None)
        if storage is None:
            raise LocationError

        image=storage.get(name, None)
        if image is None:
            return image[1]

        raise LocationError


