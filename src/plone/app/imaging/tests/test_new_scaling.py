from plone.app.imaging.tests.base import ImagingTestCase
from plone.app.imaging.tests.base import ImagingFunctionalTestCase
from plone.app.imaging.tests.base import getSettings
from plone.app.imaging.scaling import ImageScaling
from re import match
from unittest import defaultTestLoader

import transaction


class ImageStandardTraverseTests(ImagingTestCase):
    # Note: this class is subclassed by ImageChameleonTraverseTests, which
    # inherits our tests but uses a different traverser.  We use the standard
    # Zope pagetemplate traverser.

    def traverser(self, view, path=''):
        # Standard Zope page template traversal uses a list as path.
        # This is a simplified version specialised for the scaling view.
        stack = path.split('/')
        while stack:
            name = stack.pop(0)
            view = view.traverse(name, stack)
        return view

    def afterSetUp(self):
        self.data = self.getImage()
        self.image = self.folder[self.folder.invokeFactory(
            'Image', id='foo', image=self.data)]
        field = self.image.getField('image')
        self.available = field.getAvailableSizes(self.image)

    def traverse(self, path=''):
        view = self.image.unrestrictedTraverse('@@images')
        tag = self.traverser(view, path)
        base = self.image.absolute_url()
        expected = r'<img src="%s/@@images/([-0-9a-f]{36}).(jpeg|gif|png)" ' \
            r'alt="foo" title="foo" height="(\d+)" width="(\d+)" />' % base
        groups = match(expected, tag).groups()
        self.assertTrue(groups, tag)
        uid, ext, height, width = groups
        return uid, ext, int(width), int(height)

    def testImageThumb(self):
        self.assertTrue('thumb' in self.available.keys())
        uid, ext, width, height = self.traverse('image/thumb')
        self.assertEqual((width, height), self.available['thumb'])
        self.assertEqual(ext, 'png')

    def testCustomSizes(self):
        # set custom image sizes
        settings = getSettings()
        settings.allowed_sizes = [u'foo 23:23']
        # make sure traversing works with the new sizes
        uid, ext, width, height = self.traverse('image/foo')
        self.assertEqual(width, 23)
        self.assertEqual(height, 23)

    def testScaleInvalidation(self):
        # first view the thumbnail of the original image
        uid1, ext, width1, height1 = self.traverse('image/thumb')
        # now upload a new one and make sure the thumbnail has changed
        self.image.update(image=self.getImage('image.jpg'))
        uid2, ext, width2, height2 = self.traverse('image/thumb')
        self.assertNotEqual(uid1, uid2, 'thumb not updated?')
        # the height also differs as the original image had a size of 200, 200
        # whereas the updated one has 500, 200...
        self.assertEqual(width1, width2)
        self.assertNotEqual(height1, height2)

    def testCustomSizeChange(self):
        # set custom image sizes & view a scale
        settings = getSettings()
        settings.allowed_sizes = [u'foo 23:23']
        uid1, ext, width, height = self.traverse('image/foo')
        self.assertEqual(width, 23)
        self.assertEqual(height, 23)
        # now let's update the scale dimensions, after which the scale
        # should also have been updated...
        settings.allowed_sizes = [u'foo 42:42']
        uid2, ext, width, height = self.traverse('image/foo')
        self.assertEqual(width, 42)
        self.assertEqual(height, 42)
        self.assertNotEqual(uid1, uid2, 'scale not updated?')


class ImageChameleonTraverseTests(ImageStandardTraverseTests):
    # This class inherits all test methods from its parent, but uses the
    # Chameleon/five.pt traverser.

    def traverser(self, view, path=''):
        # five.pt/chameleon uses a tuple as path.  This is a simplified
        # version of BoboAwareZopeTraverse.traverse from five.pt.expressions,
        # specialised for the scaling view.
        path_items = tuple(path.split('/'))
        length = len(path_items)
        if length:
            i = 0
            while i < length:
                name = path_items[i]
                i += 1
                view = view.traverse(name, path_items[i:])
        return view


class ImageTagTests(ImagingTestCase):

    def afterSetUp(self):
        self.data = self.getImage()
        self.image = self.folder[self.folder.invokeFactory(
            'Image', id='foo', image=self.data)]
        field = self.image.getField('image')
        self.available = field.getAvailableSizes(self.image)

    def testViewTagMethod(self):
        folder = self.folder
        image = folder['foo']
        traverse = folder.REQUEST.traverseName
        view = traverse(image, '@@images')
        self.assertEqual(image.tag(), view.tag())

    def testViewTagMethodCustomScale(self):
        folder = self.folder
        image = folder['foo']
        traverse = folder.REQUEST.traverseName
        view = traverse(image, '@@images')
        view_tag = view.tag(width=23, height=23, alt="foo", title="foo")
        base = self.image.absolute_url()
        expected = r'<img src="%s/@@images/([-0-9a-f]{36}).(jpeg|gif|png)" ' \
            r'height="(\d+)" width="(\d+)" alt="foo" title="foo" />' % base
        name, ext, height, width = match(expected, view_tag).groups()
        self.assertEqual(height, '23')
        self.assertEqual(width, '23')
        scale = view.publishTraverse(self.image.REQUEST, name + "." + ext)
        self.assertEqual(scale.height, 23)
        self.assertEqual(scale.width, 23)


class ImagePublisherTests(ImagingFunctionalTestCase):

    def afterSetUp(self):
        data = self.getImage()
        folder = self.folder
        foo = folder[folder.invokeFactory('Image', id='foo', image=data)]
        self.view = foo.unrestrictedTraverse('@@images')
        transaction.commit()

    def testPublishScaleViaUID(self):
        scale = self.view.scale('image', width=64, height=64)
        # make sure the referenced image scale is available
        url = scale.url.replace('http://nohost', '')
        response = self.publish(url, basic=self.getCredentials())
        self.assertEqual(response.getStatus(), 200)
        self.assertEqual(response.getHeader('Content-Type'), 'image/png')
        self.assertImage(response.getBody(), 'PNG', (64, 64))

    def testPublishWebDavScaleViaUID(self):
        scale = self.view.scale('image', width=64, height=64)
        # make sure the referenced image scale is available
        url = scale.url.replace('http://nohost', '') + '/manage_DAVget'
        response = self.publish(url, basic=self.getCredentials())
        self.assertEqual(response.getStatus(), 200)
        # We get a very different response.  In the end it works out.
        self.assertTrue(
            'text/plain; charset=' in response.getHeader('Content-Type')
        )
        self.assertImage(response.getBody(), 'PNG', (64, 64))

    def testPublishFTPScaleViaUID(self):
        scale = self.view.scale('image', width=64, height=64)
        # make sure the referenced image scale is available
        url = scale.url.replace('http://nohost', '') + '/manage_FTPget'
        response = self.publish(url, basic=self.getCredentials())
        self.assertEqual(response.getStatus(), 200)
        # We get a very different response.  In the end it works out.
        self.assertTrue(
            'text/plain; charset=' in response.getHeader('Content-Type')
        )
        self.assertImage(response.getBody(), 'PNG', (64, 64))

    def testPublishThumbViaUID(self):
        scale = self.view.scale('image', 'thumb')
        # make sure the referenced image scale is available
        url = scale.url.replace('http://nohost', '')
        response = self.publish(url, basic=self.getCredentials())
        self.assertEqual(response.getStatus(), 200)
        self.assertEqual(response.getHeader('Content-Type'), 'image/png')
        self.assertImage(response.getBody(), 'PNG', (128, 128))

    def testPublishCustomSizeViaUID(self):
        # set custom image sizes
        settings = getSettings()
        settings.allowed_sizes = [u'foo 23:23']
        scale = self.view.scale('image', 'foo')
        # make sure the referenced image scale is available
        url = scale.url.replace('http://nohost', '')
        response = self.publish(url, basic=self.getCredentials())
        self.assertEqual(response.getStatus(), 200)
        self.assertEqual(response.getHeader('Content-Type'), 'image/png')
        self.assertImage(response.getBody(), 'PNG', (23, 23))

    def testPublishThumbViaName(self):
        # make sure traversing works as is and with scaling
        base = self.folder.absolute_url()
        browser = self.getBrowser()
        # first the field without a scale name
        browser.open(base + '/foo/@@images/image')
        self.assertEqual(browser.headers['status'], '200 Ok')
        self.assertEqual(browser.contents, self.getImage())
        self.assertEqual(browser.headers['Content-Type'], 'image/png')
        # and last a scaled version
        browser.open(base + '/foo/@@images/image/thumb')
        self.assertEqual(browser.headers['status'], '200 Ok')
        self.assertImage(browser.contents, 'PNG', (128, 128))
        self.assertEqual(browser.headers['Content-Type'], 'image/png')

    def testPublishCustomSizeViaName(self):
        # set custom image sizes
        settings = getSettings()
        settings.allowed_sizes = [u'foo 23:23']
        # make sure traversing works as expected
        base = '/'.join(self.folder.getPhysicalPath())
        credentials = self.getCredentials()
        response = self.publish(base + '/foo/@@images/image/foo',
                                basic=credentials)
        self.assertEqual(response.getStatus(), 200)
        self.assertImage(response.getBody(), 'PNG', (23, 23))

    def testPublishScaleWithInvalidUID(self):
        scale = self.view.scale('image', width=64, height=64)
        url = scale.url.replace('http://nohost', '')
        # change the url so it's invalid...
        url = url.replace('.png', 'x.png')
        response = self.publish(url, basic=self.getCredentials())
        self.assertEqual(response.getStatus(), 404)

    def testPublishScaleWithInvalidScale(self):
        scale = self.view.scale('image', 'no-such-scale')
        self.assertEqual(scale, None)

    def test_getAvailableSizesWithInvalidScale(self):
        self.assertEqual(self.view.getAvailableSizes('no-such-scale'), {})

    def test_getImageSizeWithInvalidScale(self):
        self.assertEqual(self.view.getImageSize('no-such-scale'), (0, 0))


class ScalesAdapterTests(ImagingTestCase):

    def afterSetUp(self):
        data = self.getImage()
        folder = self.folder
        self.image = folder[folder.invokeFactory(
            'Image', id='foo', image=data)]
        self.adapter = ImageScaling(self.image, None)
        self.settings = getSettings()
        self.settings.allowed_sizes = [u'foo 60:60']

    def testCreateScale(self):
        foo = self.adapter.scale('image', width=100, height=80)
        self.assertTrue(foo.uid)
        self.assertEqual(foo.mimetype, 'image/png')
        self.assertEqual(foo.width, 80)
        self.assertEqual(foo.height, 80)
        self.assertImage(foo.data, 'PNG', (80, 80))

    def testCreateScaleWithoutData(self):
        folder = self.folder
        image = folder[folder.invokeFactory('Image', id='image')]
        adapter = ImageScaling(image, None)
        foo = adapter.scale('image', width=100, height=80)
        self.assertEqual(foo, None)

    def testCreateScaleWithPdata(self):
        data = self.getImage() + '\x00' * (1 << 16)
        from Products.ATContentTypes.content.image import ATImage
        image = ATImage('image').__of__(self.folder)
        image.setImage(data)
        field = image.getField('image')
        field.swallowResizeExceptions = False
        from OFS.Image import Pdata
        self.assertTrue(isinstance(image.getImage().data, Pdata))
        adapter = ImageScaling(image, None)
        foo = adapter.scale('image', width=100, height=80)
        self.assertFalse(foo is None)

    def testGetScaleByName(self):
        foo = self.adapter.scale('image', scale='foo')
        self.assertTrue(foo.uid)
        self.assertEqual(foo.mimetype, 'image/png')
        self.assertEqual(foo.width, 60)
        self.assertEqual(foo.height, 60)
        self.assertImage(foo.data, 'PNG', (60, 60))

    def testGetUnknownScale(self):
        foo = self.adapter.scale('image', scale='foo?')
        self.assertEqual(foo, None)

    def testScaleInvalidation(self):
        # first get the scale of the original image
        foo1 = self.adapter.scale('image', scale='foo')
        # now upload a new one and make sure the scale has changed
        self.image.update(image=self.getImage('image.jpg'))
        foo2 = self.adapter.scale('image', scale='foo')
        self.assertFalse(foo1.data == foo2.data, 'scale not updated?')

    def testCustomSizeChange(self):
        # set custom image sizes & view a scale
        self.settings.allowed_sizes = [u'foo 23:23']
        foo = self.adapter.scale('image', scale='foo')
        self.assertEqual(foo.width, 23)
        self.assertEqual(foo.height, 23)
        # now let's update the scale dimensions, after which the scale
        # shouldn't be the same...
        self.settings.allowed_sizes = [u'foo 42:42']
        foo = self.adapter.scale('image', scale='foo')
        self.assertEqual(foo.width, 42)
        self.assertEqual(foo.height, 42)

    def testQualityChange(self):
        settings = getSettings()
        self.image.update(image=self.getImage('image.jpg'))
        data = self.getImage('image.jpg') + '\x00' * (1 << 16)
        # get size of image scaled at default scaling quality
        self.assertEqual(settings.quality, 88)
        from Products.ATContentTypes.content.image import ATImage
        image = ATImage('image').__of__(self.folder)
        image.setImage(data)
        adapter = ImageScaling(image, None)
        img_high_quality = adapter.scale('image', width=100, height=80)
        size_high_quality = img_high_quality.size
        # lower scaling quality and get scaled image's size at that quality
        settings.quality = 20
        self.assertEqual(settings.quality, 20)
        image = ATImage('image').__of__(self.folder)
        image.setImage(data)
        adapter = ImageScaling(image, None)
        img_low_quality = adapter.scale('image', width=100, height=80)
        size_low_quality = img_low_quality.size
        # data should be smaller at lower quality
        self.assertTrue(size_high_quality > size_low_quality)

    def testScaleThatCausesErrorsCanBeSuppressed(self):
        field = self.image.getField('image')
        field.swallowResizeExceptions = False
        self.assertRaises(
            Exception, self.adapter.scale, 'image', width=-1, height=-1)
        # scaling exceptions should be "swallowed" when set on the field...
        field.swallowResizeExceptions = True
        self.assertEqual(self.adapter.scale('image', width=-1, height=-1),
                         None)

    def testGetAvailableSizes(self):
        assert self.adapter.getAvailableSizes('image') == {'foo': (60, 60)}

    def testGetImageSize(self):
        assert self.adapter.getImageSize('image') == (200, 200)


def test_suite():
    return defaultTestLoader.loadTestsFromName(__name__)
