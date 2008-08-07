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
ptc.setupPloneSite()


class ImagingTestCase(ptc.PloneTestCase):
    """ base class for integration tests """

    def getImage(self, name='image.gif'):
        return getData(name)


class ImagingFunctionalTestCase(ptc.FunctionalTestCase):
    """ base class for functional tests """

    def getBrowser(self, loggedIn=True):
        """ instantiate and return a testbrowser for convenience """
        browser = Browser()
        if loggedIn:
            user = ptc.default_user
            pwd = ptc.default_password
            browser.addHeader('Authorization', 'Basic %s:%s' % (user, pwd))
        return browser

