import doctest
from unittest import TestSuite

from plone.app.imaging import testing
from plone.testing import layered

optionflags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE)


def test_suite():
    suite = TestSuite()
    for testfile in ['traversal.txt', 'transforms.txt']:
        suite.addTest(layered(doctest.DocFileSuite(testfile,
                                           package='plone.app.imaging.tests',
                                           optionflags=optionflags),
                             layer=testing.imaging))
    return suite
