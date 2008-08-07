from unittest import defaultTestLoader
from plone.app.imaging.tests.base import ImagingTestCase
from plone.app.imaging.traverse import ImageTraverser


class ImageTraverseTests(ImagingTestCase):

    def afterSetUp(self):
        self.counter = 0        # wrap `publishTraverse` with a counter
        self.original = ImageTraverser.publishTraverse
        def publishTraverse(adapter, request, name):
            self.counter += 1
            return self.original(adapter, request, name)
        ImageTraverser.publishTraverse = publishTraverse

    def beforeTearDown(self):
        ImageTraverser.publishTraverse = self.original

    def testImageThumb(self):
        data = self.getImage()
        folder = self.folder
        image = folder[folder.invokeFactory('Image', id='foo', image=data)]
        # make sure traversing works as is and with scaling
        traverse = folder.REQUEST.traverseName
        self.assertEqual(traverse(image, 'image').data, data)
        sizes = image.getField('image').getAvailableSizes(image)
        self.failUnless('thumb' in sizes.keys())
        thumb = traverse(image, 'image_thumb')
        self.assertEqual(thumb.getContentType(), 'image/png')
        self.assertEqual(thumb.data[:4], '\x89PNG')
        width, height = sizes['thumb']
        self.assertEqual(thumb.width, width)
        self.assertEqual(thumb.height, height)
        # also check the generated tag
        url = image.absolute_url() + '/image_thumb'
        tag = '<img src="%s" alt="foo" title="foo" height="%d" width="%d" />'
        self.assertEqual(thumb.tag(), tag % (url, height, width))
        # make sure the traversal adapter was call in fact
        self.assertEqual(self.counter, 2)


def test_suite():
    return defaultTestLoader.loadTestsFromName(__name__)

