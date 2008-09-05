from zope.component import adapts
from zope.interface import implements
from zope.publisher.interfaces import IRequest
from Products.Archetypes.interfaces import IBaseObject
from Products.Archetypes.interfaces import IImageField
from Products.Archetypes.Field import Image, HAS_PIL
from ZPublisher.BaseRequest import DefaultPublishTraverse
from plone.app.imaging.interfaces import IImageScaleHandler
from utils import getAllowedSizes, scaleImage, getImageInfo
from cStringIO import StringIO

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

class BaseImageScaleHandler(object):
    """ default handler for creating and storing scaled version of images """
    implements(IImageScaleHandler)

    def __init__(self, context):
        self.context = context

    def getScale(self, instance, scale):
        """ return scaled and aq-wrapped version for given image data """
        field = self.context
        available = self.getAllowedSizes(instance)
        if scale in available or scale is None:
            image = self.retrieveScale(instance, scale=scale)
            if image is None or image is '':       # create the scale if it doesn't exist
                if scale is not None:
                    width, height = available[scale]
                else:
                    width, height = None, None
                handle, content_type, width, height = self.createScale(instance, scale, width, height)
                self.storeScale(instance, scale, handle, content_type, width, height)
                image = self.retrieveScale(instance, scale=scale)
            if image is not None and not isinstance(image, basestring):
                return image
        return None

    def createScale(self, instance, scale, width, height):
        """ create a scaled version of the image """
        raw = self.getRawStream(instance)
        if scale is None:
            content_type, width, height = getImageInfo(raw)
            return None, content_type, width, height
        if HAS_PIL and width and height:
            if raw is not None:
                stream, handle = self.newStream()
                format, width, height = scaleImage(raw, stream, width, height)
                content_type = 'image/%s' % format.lower()
                return handle, content_type, width, height
        return None, None, None, None

    def getAllowedSizes(self, instance):
        """ retrieve a list of allowed scales """
        return getAllowedSizes()
        
    def getRawStream(self, instance):
        """ return a file stream of the raw data """
        raise NotImplemented
    
    def newStream(self):
        """ return a tuple of the new stream and the handle to the stream  """
        raise NotImplemented
        
    def retrieveScale(self, instance, scale):
        """ retrieve a scaled version of the image """
        raise NotImplemented

    def storeScale(self, instance, scale, handle, content_type, width, height):
        """ store a scaled version of the image """
        raise NotImplemented

    def createScales(self, instance):
        """ create all scales """
        ignore = self.getScale(instance, None)
        for scale in self.getAllowedSizes(instance):
            ignore = self.getScale(instance, scale)

    def removeScales(self, instance):
        """ remove all scales """
        raise NotImplemented

class DefaultImageScaleHandler(BaseImageScaleHandler):
    """ handler for creating and storing scaled version of images """
    adapts(IImageField)

    def getAllowedSizes(self, instance):
        """ retrieve a list of allowed scales """
        field = self.context
        return field.getAvailableSizes(instance)

    def getRawStream(self, instance):
        """ return a file stream of the raw data """
        field = self.context
        raw = field.getRaw(instance)
        if raw is '':
            return None
        return StringIO(str(raw.data))

    def newStream(self):
        """ return a new stream and a handle to the stream  """
        stream = handle = StringIO()
        return stream, handle

    def retrieveScale(self, instance, scale):
        """ retrieve a scaled version of the image """
        field = self.context
        return field.getScale(instance, scale=scale)

    def storeScale(self, instance, scale, handle, content_type, width, height):
        """ store a scaled version of the image """
        field = self.context
        file = handle.getvalue()
        id = field.getName() + '_' + scale
        image = Image(id, title=field.getName(), file=file,
                      content_type=content_type)
        image.filename = field.getFilename(instance)
        try:
            delattr(image, 'title')
        except (KeyError, AttributeError):
            pass

        field.getStorage(instance).set(image.getId(), instance, image,
            mimetype=image.content_type, filename=image.filename)

    def createScales(self, instance):
        """ create all scales """
        field = self.context
        field.createScales(instance)
        
    def removeScales(self, instance):
        """ remove all scales """
        field = self.context
        field.removeScales(instance)
        
