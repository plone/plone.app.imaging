from cStringIO import StringIO
import PIL.Image

from Acquisition import aq_base
from Products.Archetypes.Field import ImageField
from Products.Archetypes.utils import shasattr
from Products.ATContentTypes.content.image import ATImageSchema
from Products.ATContentTypes.content.newsitem import ATNewsItemSchema
from plone.app.imaging.interfaces import IImageScaleHandler
from plone.app.imaging.utils import getAllowedSizes
from plone.app.imaging.utils import getScalingStrategies as globalScalingStrategies


def getAvailableSizes(self, instance):
    """ get available sizes for scaled down images;  this uses the new,
        user-configurable settings, but still support instance methods
        and other callables;  see Archetypes/Field.py """
    sizes = getattr(aq_base(self), 'sizes', None)
    if isinstance(sizes, dict):
        return sizes
    elif isinstance(sizes, basestring):
        assert(shasattr(instance, sizes))
        method = getattr(instance, sizes)
        data = method()
        assert(isinstance(data, dict))
        return data
    elif callable(sizes):
        return sizes()
    else:
        sizes = getAllowedSizes()
        if sizes is None:
            sizes = self.original_getAvailableSizes(instance)
        return sizes


def getScalingStrategies(self, instance):
    strategies = getattr(aq_base(self), 'scaling_strategies', None)
    if isinstance(strategies, dict):
        return strategies
    elif isinstance(strategies, basestring):
        assert(shasattr(instance, strategies))
        method = getattr(instance, strategies)
        data = method()
        assert(isinstance(data, dict))
        return data
    elif callable(strategies):
        return strategies()
    else:
        strategies = globalScalingStrategies()
        return strategies


def scale(self, data, w, h, scaling_strategy='fit', default_format = 'PNG'):
    """ scale image (with material from ImageTag_Hotfix)"""
    #make sure we have valid int's
    size = int(w), int(h)

    original_file=StringIO(data)
    image = PIL.Image.open(original_file)
    # consider image mode when scaling
    # source images can be mode '1','L,','P','RGB(A)'
    # convert to greyscale or RGBA before scaling
    # preserve palletted mode (but not pallette)
    # for palletted-only image formats, e.g. GIF
    # PNG compression is OK for RGBA thumbnails
    original_mode = image.mode
    if original_mode == '1':
        image = image.convert('L')
    elif original_mode == 'P':
        image = image.convert('RGBA')

    if scaling_strategy == 'fill':
        curr_size = image.size
        curr_ratio = float(curr_size[0])/float(curr_size[1])
        scale_ratio = float(w)/float(h)
        approx_curr_ratio = int(100.0*curr_ratio)
        approx_scale_ratio = int(100.0*scale_ratio)
        box = None
        if approx_curr_ratio > approx_scale_ratio: # Need to crop on x
            new_width = int(float(curr_size[1])*scale_ratio)
            margin = (curr_size[0] - new_width)
            # Let's always do modulo 2 arithmetic to keep things simple;)
            if margin % 2 != 0:
                margin = margin - 1
            margin = margin / 2
            box = (margin, 0, curr_size[0] - margin, curr_size[1])
        elif approx_curr_ratio < approx_scale_ratio:
            new_height = int(float(curr_size[0])/scale_ratio)
            margin = (curr_size[1] - new_height)
            if margin % 2 != 0:
                margin = margin - 1
            margin = margin / 2
            box = (0, margin, curr_size[0], curr_size[1] - margin)
        if box:
            image = image.crop(box)

    image.thumbnail(size, self.pil_resize_algo)
    format = image.format and image.format or default_format
    # decided to only preserve palletted mode
    # for GIF, could also use image.format in ('GIF','PNG')
    if original_mode == 'P' and format == 'GIF':
        image = image.convert('P')
    thumbnail_file = StringIO()
    # quality parameter doesn't affect lossless formats
    image.save(thumbnail_file, format, quality=self.pil_quality)
    thumbnail_file.seek(0)
    return thumbnail_file, format.lower()


def createScales(self, instance, value=None):
    """ creates scales and stores them; largely based on the version from
        `Archetypes.Field.ImageField` """
    sizes = self.getAvailableSizes(instance)
    strategies = self.getScalingStrategies(instance)
    handler = IImageScaleHandler(self)
    for name, size in sizes.items():
        width, height = size
        strategy = 'fit'
        if name in strategies:
            strategy = strategies[name]
        data = handler.createScale(instance, name, width, height, scaling_strategy=strategy, data=value)
        if data is not None:
            handler.storeScale(instance, name, **data)


def patchImageField():
    """ monkey patch `ImageField` methods """
    ImageField.original_getAvailableSizes = ImageField.getAvailableSizes
    ImageField.getAvailableSizes = getAvailableSizes
    ImageField.getScalingStrategies = getScalingStrategies
    ImageField.original_createScales = ImageField.createScales
    ImageField.createScales = createScales
    ImageField.original_scale = ImageField.scale
    ImageField.scale = scale


def unpatchImageField():
    """ revert monkey patch regarding `ImageField` methods """
    ImageField.getAvailableSizes = ImageField.original_getAvailableSizes
    ImageField.createScales = ImageField.original_createScales
    ImageField.scale = ImageField.original_scale


def patchSchemas():
    """ monkey patch `sizes` attribute in `ATImageSchema` and
        `ATNewsItemSchema` to make it possible to detect whether the
        sizes has been overridden """
    ATImageSchema['image'].sizes = None
    ATNewsItemSchema['image'].sizes = None
