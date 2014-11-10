from unittest import defaultTestLoader
from Products.Archetypes.interfaces import IImageField
from Products.ATContentTypes.content.image import ATImageSchema, ATImage
from plone.app.imaging.tests.base import ImagingTestCase
from plone.app.imaging.monkey import getAvailableSizes
from plone.app.imaging.monkey import getScalingStrategies


class MonkeyPatchTests(ImagingTestCase):

    def afterSetUp(self):
        self.image = ATImage('test')
        self.field = self.image.getField('image')
        self.sizes = ATImageSchema['image'].sizes   # save original value

    def beforeTearDown(self):
        ATImageSchema['image'].sizes = self.sizes   # restore original value
        if hasattr(ATImageSchema['image'], 'scaling_strategies'):
            del ATImageSchema['image'].scaling_strategies

    def testAvailableSizes(self):
        # make sure the field was patched
        self.assertEqual(self.field.getAvailableSizes.func_code,
            getAvailableSizes.func_code)
        # set custom image sizes and check the helper
        iprops = self.portal.portal_properties.imaging_properties
        iprops.manage_changeProperties(allowed_sizes=['foo 23:23', 'bar 8:8'])
        self.assertEqual(self.field.getAvailableSizes(self.image),
            dict(foo = (23, 23), bar = (8, 8)))

    def testAvailableSizesInstanceMethod(self):
        marker = dict(foo=23)
        def foo(self):
            return marker
        ATImage.foo = foo                       # create new instance method
        ATImageSchema['image'].sizes = 'foo'    # restore original value
        self.assertEqual(self.field.getAvailableSizes(self.image), marker)

    def testAvailableSizesCallable(self):
        def foo():
            return 'foo!'
        ATImageSchema['image'].sizes = foo      # store method in schema
        self.assertEqual(self.field.getAvailableSizes(self.image), 'foo!')

    def testAvailableSizesOnField(self):
        marker = dict(foo=23)
        ATImageSchema['image'].sizes = marker   # store dict in schema
        self.assertEqual(self.field.getAvailableSizes(self.image), marker)

    def testScalingStrategies(self):
        # make sure the field was patched
        self.assertEqual(self.field.getScalingStrategies.func_code,
            getScalingStrategies.func_code)
        # set custom image sizes and check the helper
        iprops = self.portal.portal_properties.imaging_properties
        iprops.manage_changeProperties(
            allowed_sizes=['foo 23:23 fit', 'bar 8:8 fill'])
        self.assertEqual(self.field.getScalingStrategies(self.image),
            dict(foo = 'fit', bar = 'fill'))

    def testScalingStrategiesInstanceMethod(self):
        marker = dict(foo='fill')
        def foo(self):
            return marker
        ATImage.foo = foo
        ATImageSchema['image'].scaling_strategies = 'foo'
        self.assertEqual(self.field.getScalingStrategies(self.image), marker)

    def testScalingStrategiesCallable(self):
        def foo():
            return dict(foo='fill')
        ATImage.foo = foo
        ATImageSchema['image'].scaling_strategies = foo
        self.assertEqual(self.field.getScalingStrategies(self.image),
                         dict(foo='fill'))

    def testScalingStrategiesOnField(self):
        marker = dict(foo='fill')
        ATImageSchema['image'].scaling_strategies = marker
        self.assertEqual(self.field.getScalingStrategies(self.image), marker)


class RegistryTests(ImagingTestCase):

    def testImageFieldInterface(self):
        data = self.getImage()
        folder = self.folder
        image = folder[folder.invokeFactory('Image', id='foo', image=data)]
        field = image.getField('image')
        self.failUnless(IImageField.providedBy(field))


def test_suite():
    return defaultTestLoader.loadTestsFromName(__name__)
