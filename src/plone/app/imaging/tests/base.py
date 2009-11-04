from Products.Five.testbrowser import Browser
from Products.PloneTestCase import ptc
from plone.app.imaging.tests.layer import ImagingLayer
from plone.app.imaging.tests.utils import getData


ptc.setupPloneSite()


class ImagingTestCaseMixin:
    """ mixin for integration and functional tests """

    def getImage(self, name='image.gif'):
        return getData(name)


class ImagingTestCase(ptc.PloneTestCase, ImagingTestCaseMixin):
    """ base class for integration tests """

    layer = ImagingLayer


class ImagingFunctionalTestCase(ptc.FunctionalTestCase, ImagingTestCaseMixin):
    """ base class for functional tests """

    layer = ImagingLayer

    def getCredentials(self):
        return '%s:%s' % (ptc.default_user, ptc.default_password)

    def getBrowser(self, loggedIn=True):
        """ instantiate and return a testbrowser for convenience """
        browser = Browser()
        if loggedIn:
            auth = 'Basic %s' % self.getCredentials()
            browser.addHeader('Authorization', auth)
        return browser
