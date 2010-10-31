from cgi import escape
from webdav.common import rfc1123_date
from zope.interface import implements
from Products.Five import BrowserView
from Products.Archetypes.Field import Image
from plone.app.imaging.interfaces import IImageScale


class ImageScale(BrowserView):
    """ view used for rendering image scales """
    implements(IImageScale)

    __name__ = 'scale'
    __allow_access_to_unprotected_subobjects__ = True

    def __init__(self, context, request, id, data, **info):
        self.context = context
        self.request = request
        self.id = id
        self.data = data
        # width, height, mimetype, url, size should be passed in...
        self.__dict__.update(**info)

    def absolute_url(self):
        return self.url

    def tag(self, height=None, width=None, alt=None, title=None,
            css_class=None, **kw):
        """ prepare the image tag """
        if height is None:
            height = self.height
        if width is None:
            width = self.width
        if alt is None:
            alt = self.context.Title()
        if title is None:
            title = self.context.Title()
        values = dict(src=self.url, height=height, width=width,
            alt=escape(alt, quote=True), title=escape(title, quote=True))
        tag = '<img src="%(src)s" alt="%(alt)s" title="%(title)s" ' \
              'height="%(height)s" width="%(width)s"' % values
        if css_class is not None:
            tag += ' class="%s"' % css_class
        for key, value in kw.items():
            if value:
                tag += ' %s="%s"' % (key, value)
        return tag + ' />'

    def set_headers(self, name=None, modified=None):
        if not self.request:
            return
        header = self.request.RESPONSE.setHeader
        header('Content-Type', self.content_type)
        header('Content-Length', self.size)
        header('Accept-Ranges', 'bytes')
        if modified:
            header('Last-Modified', rfc1123_date(modified))
        if name:
            header('Content-Disposition', 'attachment; filename="%s"' % name)

    def index_html(self):
        """ download the image """
        self.set_headers(self.filename, self.context.modified())
        data = self.data
        if not isinstance(data, str):
            data = data.open('r').read()    # assume it's file-like
        return data

    def __call__(self, *args, **kw):
        """ calling the scale returns itself, so "nocall:" can be skipped """
        return self


class ATImageScale(Image):
    """ extend image class from `Archetypes.Field` by making sure the title
        gets always computed and not calling `_get_content_type` even though
        an explicit type has been passed """
    implements(IImageScale)

    def __init__(self, id, data, content_type, **kw):
        self.__name__ = id
        self.__dict__.update(kw)
        self.precondition = ''
        # `OFS.Image` has no proper support for file objects or iterators,
        # so we'll require `data` to be a string or a file-like object...
        if not isinstance(data, str):
            data = data.open('r').read()    # assume it's file-like
        self.update_data(data, content_type, size=len(data))

    def absolute_url(self):
        """ return the url for new-style scales, but fall back for others """
        if 'url' in self.__dict__:
            return self.url
        else:
            return super(ATImageScale, self).absolute_url()

    def __call__(self, *args, **kw):
        """ calling the scale returns itself, so "nocall:" can be skipped """
        return self
