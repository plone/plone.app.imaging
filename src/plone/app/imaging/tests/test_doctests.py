import doctest
from unittest import TestSuite

from plone.app.imaging import testing
from plone.testing import layered

optionflags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


def test_suite():
    suite = TestSuite()
    return suite
    for testfile in ['traversal.txt', 'transforms.txt', 'configlet.txt']:
        suite.addTest(layered(doctest.DocFileSuite(testfile,
                                           package='plone.app.imaging.tests'),
                             layer=testing.imaging))
    return suite
