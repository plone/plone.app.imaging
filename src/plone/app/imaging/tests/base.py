from plone.app.testing.bbb import PloneTestCase
from plone.testing.z2 import Browser
from plone.app.imaging import testing
from StringIO import StringIO
import unittest
from os.path import dirname, join


def getData(filename):
    """ return contents of the file with the given name """
    filename = join(dirname(__file__), filename)
    return open(filename, 'r').read()


class ImagingTestCase(PloneTestCase):
    """ base class for integration tests """

    layer = testing.imaging

    def getImage(self, name='image.gif'):
        return getData(name)

    def assertImage(self, data, format, size):
        import PIL.Image
        image = PIL.Image.open(StringIO(data))
        self.assertEqual(image.format, format)
        self.assertEqual(image.size, size)


class ImagingFunctionalTestCase(ImagingTestCase):
    """ base class for functional tests """

    def getCredentials(self):
        return '%s:%s' % (ptc.default_user, ptc.default_password)

    def getBrowser(self, loggedIn=True):
        """ instantiate and return a testbrowser for convenience """
        browser = Browser()
        if loggedIn:
            auth = 'Basic %s' % self.getCredentials()
            browser.addHeader('Authorization', auth)
        return browser
