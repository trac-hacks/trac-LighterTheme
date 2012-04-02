from genshi.builder import tag
from genshi.filters import Transformer
from genshi.filters.transform import StreamBuffer

from trac.core import *
from trac.web.chrome import Chrome, add_stylesheet, add_script
from trac.web.api import IRequestFilter, ITemplateStreamFilter

class Theme(Component):
    implements(IRequestFilter, ITemplateStreamFilter)

    def pre_process_request(self, req, handler):
        add_stylesheet(req, 'http://fonts.googleapis.com/css?family=Ubuntu')
        add_stylesheet(req, 'lightertheme/theme.css')
        return handler

    def post_process_request(self, req, template, data, content_type):
        return template, data, content_type

    def filter_stream(self, req, method, filename, stream, data):
        """
        Wrap the banner and mainnav in a single banner_wrapper div
        """
        buffer = StreamBuffer()
        filter = Transformer("//div[@id='banner']")
        stream |= filter.wrap(tag.div(id="banner_wrapper")).end().select("//div[@id='mainnav']").cut(buffer, accumulate=True).end().buffer().select("//div[@id='banner_wrapper']").append(tag.hr()).a\
ppend(buffer).end()

        return stream



