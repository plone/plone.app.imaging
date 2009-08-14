from zope.component import adapts
from zope.interface import implements
from zope.app.file.image import Image
from plone.scale.storage import IImageData
from plone.scale.storage import AnnotationStorage
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
        return "http://farm4.static.flickr.com/3663/buddyicons/996019@N24.jpg"

