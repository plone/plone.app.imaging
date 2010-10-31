from logging import exception
from StringIO import StringIO
from Acquisition import aq_base
from ZODB.POSException import ConflictError
from OFS.Image import Pdata
from zope.interface import implements
from zope.traversing.interfaces import ITraversable, TraversalError
from zope.publisher.interfaces import IPublishTraverse, NotFound
from plone.app.imaging.interfaces import IImageScaling, IImageScaleFactory
from plone.app.imaging.transform import applyTransforms
from plone.app.imaging.scale import ImageScale
from plone.scale.storage import AnnotationStorage
from Products.Five import BrowserView


class HashableDict(dict):
    """ a dictionary that can be used as a key in another one """

    def __hash__(self):
        return hash(tuple(sorted(self.items())))


class OpenableStringFile(StringIO):

    def open(self, mode):
        return self


class ImageScaleFactory(object):
    """ adapter for image fields that allows generating scaled images """
    implements(IImageScaleFactory)

    new = OpenableStringFile

    def __init__(self, field):
        self.field = field

    def data(self, context):
        value = self.field.get(context)
        data = getattr(aq_base(value), 'data', value)
        if isinstance(data, Pdata):
            data = str(data)
        if data:
            return StringIO(data)


class ImageScaling(BrowserView):
    """ view used for generating (and storing) image scales """
    implements(IImageScaling, ITraversable, IPublishTraverse)

    def publishTraverse(self, request, name):
        """ used for traversal via publisher, i.e. when using as a url """
        stack = request.get('TraversalRequestNameStack')
        if stack:
            # field and scale name were given...
            scale = stack.pop()
            image = self.scale(name, scale)             # this is aq-wrapped
        elif '.' in name:
            # we got a uid...
            uid, ext = name.rsplit('.', 1)
            storage = AnnotationStorage(self.context)
            info = storage.get(uid)
            image = None
            if info is not None:
                image = self.make(info).__of__(self.context)
        else:
            # otherwise `name` must refer to a field...
            field = self.field(name)
            image = field.get(self.context)             # this is aq-wrapped
        if image is not None:
            return image
        raise NotFound(self, name, self.request)

    def traverse(self, name, furtherPath):
        """ used for path traversal, i.e. in zope page templates """
        if not furtherPath:
            field = self.context.getField(name)
            return field.get(self.context).tag()
        image = self.scale(name, furtherPath.pop())
        if image is not None:
            return image.tag()
        raise TraversalError(self, name)

    def make(self, info):
        """ instantiate an object implementing `IImageScale` """
        mimetype = info['mimetype']
        info['content_type'] = mimetype
        info['filename'] = self.context.getFilename()
        scale = ImageScale(self.context, self.request, id=info['uid'], **info)
        scale.size = len(scale.data)
        url = self.context.absolute_url()
        extension = mimetype.split('/')[-1]
        scale.url = '%s/@@images/%s.%s' % (url, info['uid'], extension)
        return scale

    def field(self, fieldname):
        """ return the field for a given name """
        if fieldname:
            return self.context.getField(fieldname)
        else:
            return self.context.getPrimaryField()

    def create(self, fieldname, transforms, **parameters):
        """ factory for image scales, see `IImageScaleStorage.scale` """
        field = self.field(fieldname)
        factory = IImageScaleFactory(field)
        data = factory.data(self.context)
        try:
            if data:
                image, format = applyTransforms(data, transforms)
                if not format == 'PNG':
                    format = 'JPEG'
                value = factory.new()
                outfile = value.open('w')
                image.save(outfile, format, **parameters)
                if getattr(value, 'getvalue'):     # support for StringIO
                    value = value.getvalue()
                outfile.close()
                return value, format, image.size
        except (ConflictError, KeyboardInterrupt):
            raise
        except Exception:
            if not field.swallowResizeExceptions:
                raise
            else:
                exception('could not scale "%r" of %r',
                    field, self.context.absolute_url())

    def modified(self):
        """ provide a callable to return the modification time of content
            items, so stored image scales can be invalidated """
        return self.context.modified().millis()

    # TODO: this should be deprecated in plone 4.2, see PLIP 10174
    def scale(self, fieldname=None, scale=None, width=None, height=None,
            direction='keep', **parameters):
        if scale is not None:
            field = self.field(fieldname)
            available = field.getAvailableSizes(self.context)
            if not scale in available:
                return None
            width, height = available[scale]
        storage = AnnotationStorage(self.context, self.modified)
        scale = 'scale', HashableDict(width=width, height=height,
            direction=direction)
        info = storage.scale(factory=self.create,
            fieldname=fieldname, transforms=(scale,), **parameters)
        if info is not None:
            return self.make(info).__of__(self.context)
