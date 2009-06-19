from plone.app.blob.tests.base import ReplacementTestCase   # import first!

from unittest import defaultTestLoader
from Products.ATContentTypes.interface.file import IFileContent
from Products.ATContentTypes.interface.image import IImageContent
from plone.app.blob.markings import unmarkAs


class MaintenanceViewTests(ReplacementTestCase):

    def afterSetUp(self):
        # ignore any generated logging output
        self.portal.REQUEST.RESPONSE.write = lambda x: x

    def testResetSubtypes(self):
        foo = self.folder[self.folder.invokeFactory('File', 'foo')]
        bar = self.folder[self.folder.invokeFactory('Image', 'bar')]
        # try to re-create the state of blob content created with pre-beta3
        unmarkAs(foo, 'File')
        unmarkAs(bar, 'Image')
        self.failIf(IFileContent.providedBy(foo), 'already IFileContent?')
        self.failIf(IImageContent.providedBy(bar), 'already IImageContent?')
        self.failIf(foo.Schema().getField('file'), 'has field "file"?')
        self.failIf(bar.Schema().getField('image'), 'has field "image"?')
        # then fix again using the respective view...
        maintenance = self.portal.unrestrictedTraverse('blob-maintenance')
        maintenance.resetSubtypes()
        self.failUnless(IFileContent.providedBy(foo), 'no IFileContent?')
        self.failUnless(IImageContent.providedBy(bar), 'no IImageContent?')
        self.failUnless(foo.Schema().getField('file'), 'no field "file"?')
        self.failUnless(bar.Schema().getField('image'), 'no field "image"?')


def test_suite():
    return defaultTestLoader.loadTestsFromName(__name__)