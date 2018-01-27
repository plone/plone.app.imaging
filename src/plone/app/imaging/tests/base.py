# -*- coding: utf-8 -*-
from os.path import dirname
from os.path import join
from plone.app.imaging import testing
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing.bbb import PloneTestCase
from plone.registry.interfaces import IRegistry
from plone.testing.z2 import Browser
from Products.CMFPlone.interfaces.controlpanel import IImagingSchema
from six import StringIO
from zope.component import queryUtility


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
