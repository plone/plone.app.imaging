from unittest import defaultTestLoader
from plone.app.imaging.tests.base import ImagingTestCase
from plone.app.imaging.traverse import ImageTraverser


class ImageTraverseTests(ImagingTestCase):

    def testImageThumb(self):
        data = self.getImage()
        folder = self.folder
        image = folder[folder.invokeFactory('Image', id='foo', image=data)]
        # make sure traversing works as is and with scaling
        traverser = ImageTraverser(image, None)
        self.assertEqual(traverser.publishTraverse(None, 'image').data, data)
        sizes = image.getField('image').getAvailableSizes(image)
        self.failUnless('thumb' in sizes.keys())
        thumb = traverser.publishTraverse(None, 'image_thumb')
        self.assertEqual(thumb.getContentType(), 'image/png')
        self.assertEqual(thumb.data[:4], '\x89PNG')
        width, height = sizes['thumb']
        self.assertEqual(thumb.width, width)
        self.assertEqual(thumb.height, height)
        # also check the generated tag
        url = image.absolute_url() + '/image_thumb'
        tag = '<img src="%s" alt="foo" title="foo" height="%d" width="%d" />'
        self.assertEqual(thumb.tag(), tag % (url, height, width))


def test_suite():
    return defaultTestLoader.loadTestsFromName(__name__)

