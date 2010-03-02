from Testing.ZopeTestCase import installPackage
from Products.Five import zcml
from Products.Five import fiveconfigure
from collective.testcaselayer.ptc import BasePTCLayer, ptc_layer


class ImagingLayer(BasePTCLayer):
    """ layer for integration tests """

    def afterSetUp(self):
        fiveconfigure.debug_mode = True
        from plone.app import imaging
        zcml.load_config('testing.zcml', imaging)
        fiveconfigure.debug_mode = False
        installPackage('plone.app.imaging', quiet=True)
        self.addProfile('plone.app.imaging:default')


imaging = ImagingLayer(bases=[ptc_layer])
