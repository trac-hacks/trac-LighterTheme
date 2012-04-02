from pkg_resources import resource_filename

from genshi.builder import tag
from genshi.filters import Transformer
from genshi.filters.transform import StreamBuffer

from trac.core import *
from trac.web.chrome import Chrome, add_stylesheet, add_script
from trac.web.chrome import ITemplateProvider
from trac.web.api import IRequestFilter, ITemplateStreamFilter

class Theme(Component):
    implements(IRequestFilter, ITemplateStreamFilter, ITemplateProvider)

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
        stream |= filter.wrap(tag.div(id="banner_wrapper")).end(
            ).select("//div[@id='mainnav']").cut(buffer, accumulate=True).end().buffer(
            ).select("//div[@id='banner_wrapper']").append(tag.hr()).append(buffer).end()

        return stream

    def get_htdocs_dirs(self):
        """
        Return a list of directories with static resources (such as style
        sheets, images, etc.)
        Each item in the list must be a `(prefix, abspath)` tuple. The
        `prefix` part defines the path in the URL that requests to these
        resources are prefixed with.
       
        The `abspath` is the absolute path to the directory containing the
        resources on the local file system.
        """
        return [("lightertheme", resource_filename(__name__, 'htdocs'))]

    def get_templates_dirs(self):
        """Return a list of directories containing the provided template
        files.
        """
        return []


