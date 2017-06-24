# -*- coding: utf-8 -*-
from plone.app.imaging.tests.base import ImagingTestCase
from plone.app.imaging.utils import getAllowedSizes, getQuality
from unittest import defaultTestLoader
from plone.app.imaging.tests.base import getSettings


class PropertiesTests(ImagingTestCase):

    def testAllowedSizes(self):
        # test the defaults
        # for readability, pep8 is not applied to the dict below
        self.assertEqual(getAllowedSizes(), dict(
            large=(1200, 1200),
            preview=(768, 768),
            mini=(400, 400),
            thumb=(200, 200),
            tile=(64, 64),
            icon=(32, 32),
            listing=(16, 16)))
        # override and test again
        settings = getSettings()
        settings.allowed_sizes = [u'foo bar 23:23']
        self.assertEqual(getAllowedSizes(), dict(foo_bar=(23, 23)))

    def testQuality(self):
        self.assertEqual(getQuality(), 88)
        settings = getSettings()
        settings.quality = 42
        self.assertEqual(getQuality(), 42)


def test_suite():
    return defaultTestLoader.loadTestsFromName(__name__)
