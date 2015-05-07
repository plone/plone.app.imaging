from plone.app.imaging.monkey import unpatchImageField
from plone.app import testing
from plone.app.testing.bbb import PloneTestCaseFixture
from plone.testing import z2


class ImagingFixture(PloneTestCaseFixture):
    """ Test fixture for plone.app.imaging """

    def setUpZope(self, app, configurationContext):
        super(ImagingFixture, self).setUpZope(app, configurationContext)
        import plone.app.imaging
        self.loadZCML(package=plone.app.imaging)
        z2.installProduct(app, 'plone.app.imaging')

    def setUpPloneSite(self, portal):
        super(ImagingFixture, self).setUpPloneSite(portal)

    def tearDownZope(self, app):
        super(ImagingFixture, self).tearDownZope(app)
        unpatchImageField()
        z2.uninstallProduct(app, 'plone.app.imaging')



PTC_FIXTURE = ImagingFixture()
imaging = testing.FunctionalTesting(
    bases=(PTC_FIXTURE,), name='ImagingTestCase:Functional')
