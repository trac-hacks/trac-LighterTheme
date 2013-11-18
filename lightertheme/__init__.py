from pkg_resources import resource_filename

from genshi.builder import tag
from genshi.filters import Transformer
from genshi.filters.transform import StreamBuffer

from trac.core import *
from trac.config import *
from trac.web.chrome import Chrome, add_stylesheet, add_script
from trac.web.chrome import ITemplateProvider
from trac.web.api import IRequestHandler, ITemplateStreamFilter

class Theme(Component):
    implements(ITemplateStreamFilter, ITemplateProvider, IRequestHandler)

    extra_stylesheets = ListOption(
        'lightertheme', 'extra_stylesheets',
        '//fonts.googleapis.com/css?family=Ubuntu')
    main_text_font_family = Option(
        'lightertheme', 'main_text_font_family', 'Ubuntu')
        
    def match_request(self, req):
        if req.path_info == "/lightertheme/theme.css":
            return True

    def process_request(self, req):
        data = {
            'main_text_font_family': self.main_text_font_family,
            }
        output = Chrome(self.env).render_template(req,
            "lightertheme/theme.css.tmpl", data, "text/plain")
        req.send(output, 'text/css')
    
    def filter_stream(self, req, method, filename, stream, data):
        """
        Wrap the banner and mainnav in a single banner_wrapper div
        """

        for href in self.extra_stylesheets:
            add_stylesheet(req, href)
        add_stylesheet(req, '/lightertheme/theme.css')

        stream |= Transformer("//div[@id='banner']").wrap(tag.div(class_="banner_wrapper banner_wrapper_first"))
        stream |= Transformer("//div[@id='mainnav']").wrap(tag.div(class_="banner_wrapper banner_wrapper_second"))
        stream |= Transformer("//div[@class='banner_wrapper banner_wrapper_first']").append(tag.hr())
        return stream


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
        return []

    def get_templates_dirs(self):
        """Return a list of directories containing the provided template
        files.
        """
        return ["lightertheme", resource_filename(__name__, 'templates')]


