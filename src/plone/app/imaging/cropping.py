from cStringIO import StringIO
from zope.interface import providedBy
import PIL.Image

from Products.Five import BrowserView
from plone.app.blob.interfaces import IBlobImageField

from plone.app.imaging.interfaces import IImageScaleHandler


class CroppableImagesView(BrowserView):
    """
    Lists the image fields together with the scales that are specified
    with the 'fill' parameter to allow later recropping.
    """

    def __init__(self, context, request):
        super(CroppableImagesView, self).__init__(context, request)
        image_fields = [field
                        for field in self.context.Schema().fields()
                        if IBlobImageField in providedBy(field).interfaces()]
        self.image_fields = image_fields

    def imageFields(self):
        return [field.getName() for field in self.image_fields]

    def croppingScales(self, field_name):
        field = self.context.getField(field_name)
        strategies = field.getScalingStrategies(field)
        return [scale for scale in strategies
                if strategies[scale]=='fill']


class CropImageView(BrowserView):

    def __init__(self, context, request):
        super(CropImageView, self).__init__(context, request)
        self.field_name = request.get('field')
        self.scale_name = request.get('scale')

    def publishTraverse(self, request, name):
        if name=="cropImage":
            return self.cropImage
        return super(CropImageView, self).publishTraverse(request, name)

    def field(self):
        return self.field_name

    def scale(self):
        return self.scale_name

    def aspectRatio(self):
        field = self.context.getField(self.field_name)
        available_sizes = field.getAvailableSizes(field)
        if self.scale_name not in available_sizes:
            return 1.0
        w, h = available_sizes[self.scale_name]
        return float(w)/float(h)

    def cropImage(self, **kwargs):
        """ Crops the image
        """
        field_name = self.request['field']
        scale = self.request['scale']
        box = (int(self.request['x1']), int(self.request['y1']),
               int(self.request['x2']), int(self.request['y2']))

        field = self.context.getField(field_name)
        handler = IImageScaleHandler(field)

        data = field.get(self.context).data

        original_file=StringIO(data)
        image = PIL.Image.open(original_file)
        image = image.crop(box)

        image_file = StringIO()
        image.save(image_file, 'PNG', quality=88)
        image_file.seek(0)
        sizes = field.getAvailableSizes(self.context)
        w, h = sizes[scale]
        data = handler.createScale(self.context, scale, w, h,
                                   scaling_strategy='fit',
                                   data=image_file.read())
        handler.storeScale(self.context, scale, **data)
