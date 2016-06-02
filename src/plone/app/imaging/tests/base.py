from plone.app.testing.bbb import PloneTestCase
from plone.testing.z2 import Browser
from plone.app.imaging import testing
from StringIO import StringIO
from os.path import dirname, join
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.interfaces.controlpanel import IImagingSchema


def getSettings():
    registry = queryUtility(IRegistry)
    return registry.forInterface(IImagingSchema, prefix="plone", check=False)


def getData(filename):
    """ return contents of the file with the given name """
    filename = join(dirname(__file__), filename)
    return open(filename, 'r').read()


class ImagingTestCase(PloneTestCase):
    """ base class for integration tests """

    layer = testing.imaging

    def getImage(self, name='image.png'):
        return getData(name)

    def assertImage(self, data, format, size):
        import PIL.Image
        image = PIL.Image.open(StringIO(data))
        self.assertEqual(image.format, format)
        self.assertEqual(image.size, size)


class ImagingFunctionalTestCase(ImagingTestCase):
    """ base class for functional tests """

    def getCredentials(self):
        return '%s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD)

    def getBrowser(self, loggedIn=True):
        """ instantiate and return a testbrowser for convenience """
        browser = Browser(self.layer['app'])
        if loggedIn:
            auth = 'Basic %s' % self.getCredentials()
            browser.addHeader('Authorization', auth)
        return browser
