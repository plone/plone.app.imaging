# base for integration and functional tests
# see http://plone.org/documentation/tutorial/testing/writing-a-plonetestcase-unit-integration-test
# for more information about the following setup

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.Five.testbrowser import Browser
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

from plone.app.imaging.tests.utils import getData


@onsetup
def setup_product():
    fiveconfigure.debug_mode = True
    import plone.app.imaging
    zcml.load_config('configure.zcml', plone.app.imaging)
    fiveconfigure.debug_mode = False

setup_product()
ptc.setupPloneSite(extension_profiles=(
    'plone.app.imaging:default',
))


class ImagingTestCaseMixin:
    """ mixin for integration and functional tests """

    def getImage(self, name='image.gif'):
        return getData(name)


class ImagingTestCase(ptc.PloneTestCase, ImagingTestCaseMixin):
    """ base class for integration tests """


class ImagingFunctionalTestCase(ptc.FunctionalTestCase, ImagingTestCaseMixin):
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

