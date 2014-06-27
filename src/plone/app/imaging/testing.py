from plone.app.imaging.monkey import unpatchImageField
from plone.app import testing
from plone.app.testing.bbb import PloneTestCaseFixture, PloneTestCase
from plone.testing import z2


class ImagingFixture(PloneTestCaseFixture):
    """ Test fixture for plone.app.imaging """

    def setUpZope(self, app, configurationContext):
        super(PloneTestCaseFixture, self).setUpZope(app, configurationContext)
        import plone.app.imaging
        self.loadZCML(package=plone.app.imaging)
        z2.installProduct(app, 'plone.app.imaging')

    def setUpPloneSite(self, portal):
        super(PloneTestCaseFixture, self).setUpPloneSite(portal)
        # install sunburst theme
        testing.applyProfile(portal, 'plone.app.imaging:default')

    def tearDownZope(self, app):
        super(PloneTestCaseFixture, self).tearDownZope(app)
        unpatchImageField()
        z2.uninstallProduct(app, 'plone.app.imaging')



PTC_FIXTURE = ImagingFixture()
imaging = testing.FunctionalTesting(
    bases=(PTC_FIXTURE,), name='ImagingTestCase:Functional')
