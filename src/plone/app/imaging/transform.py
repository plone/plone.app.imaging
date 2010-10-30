import PIL
from zope.component._api import getUtility

from zope.interface.declarations import implements
from plone.app.imaging.interfaces import ITransform

def apply_transforms(image, transforms):
    
    for name, parameters in transforms:
        transform = getUtility(ITransform, name=name)
        image = transform(image, **dict(parameters))
    

    return image


class BaseTransform(object):
    implements(ITransform)
    
class Crop(BaseTransform):
    
    description = u"""XXX briefely describe how this transform works
"""

    def __call__(width, height):
        return self