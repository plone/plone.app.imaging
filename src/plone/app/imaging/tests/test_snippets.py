from unittest import defaultTestLoader
from plone.scale.storage import AnnotationStorage
from plone.app.imaging.tests.base import ImagingFunctionalTestCase
from re import match, sub


class SnippetTests(ImagingFunctionalTestCase):

    def render(self, viewname, **kw):
        image = self.folder[self.folder.invokeFactory('Image', id='foo',
            image=self.getImage(), **kw)]
        url = '/'.join(image.getPhysicalPath()) + '/@@' + viewname
        response = self.publish(url, basic=self.getCredentials())
        tag = sub(r'\s+', ' ', response.body)
        self.assertEqual(response.getStatus(), 200)
        expected = r'<img src="%s/@@images/(?P<uid>[-0-9a-f]{36}).' \
            r'(?P<extention>jpeg|gif|png)" (alt="(?P<alt>[^"]*)" )?' \
            r'(title="(?P<title>[^"]*)" )?height="(?P<height>\d+)" ' \
            r'width="(?P<width>\d+)" />' % image.absolute_url()
        info = match(expected, tag).groupdict()
        self.failUnless(info, tag)
        return image, info

    def testExplicitTagGeneration(self):
        image, info = self.render('explicit-tag-generation')
        self.failUnless(info['uid'] in AnnotationStorage(image))
        self.assertEqual(int(info['width']), 64)
        self.assertEqual(int(info['height']), 64)

    def testAutomaticTagGeneration(self):
        image, info = self.render('automatic-tag-generation', title='foo')
        self.failUnless(info['uid'] in AnnotationStorage(image))
        self.assertEqual(int(info['width']), 1200)
        self.assertEqual(int(info['height']), 800)
        self.assertEqual(info['title'], 'foo')
        self.assertEqual(info['alt'], 'foo')

    def testTagGenerationWithScaleName(self):
        image, info = self.render('tag-generation-with-scalename')
        self.failUnless(info['uid'] in AnnotationStorage(image))
        self.assertEqual(int(info['width']), 200)
        self.assertEqual(int(info['height']), 200)

    def testTagGenerationForScaleShortcut(self):
        image, info = self.render('shortcut-tag-for-scale')
        self.failUnless(info['uid'] in AnnotationStorage(image))
        self.assertEqual(int(info['width']), 200)
        self.assertEqual(int(info['height']), 200)

    def testTagGenerationForImageShortcut(self):
        image, info = self.render('shortcut-tag-for-image')
        self.failUnless(info['uid'] in AnnotationStorage(image))
        self.assertEqual(int(info['width']), 200)
        self.assertEqual(int(info['height']), 200)


def test_suite():
    return defaultTestLoader.loadTestsFromName(__name__)
