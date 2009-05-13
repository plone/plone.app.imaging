from unittest import TestSuite
from zope.testing import doctest
from Testing import ZopeTestCase as ztc
from plone.app.controlpanel.tests.cptc import ControlPanelTestCase
from plone.app.imaging.tests.base import ImagingFunctionalTestCase

optionflags = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


def test_suite():
    return TestSuite([
        ztc.FunctionalDocFileSuite(
           'traversal.txt', package='plone.app.imaging.tests',
           test_class=ImagingFunctionalTestCase, optionflags=optionflags),
        ztc.FunctionalDocFileSuite(
           'configlet.txt', package='plone.app.imaging.tests',
           test_class=ControlPanelTestCase, optionflags=optionflags),
    ])

