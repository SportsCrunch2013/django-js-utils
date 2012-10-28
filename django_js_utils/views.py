import re
import sys
import types
import django.utils.simplejson as json
from django.conf import settings
from django.core.urlresolvers import RegexURLPattern, RegexURLResolver
from django.http import HttpResponse
from django.utils.datastructures import SortedDict

ALLOWED_NAMESPACES = getattr(settings, 'JS_UTILS_ALLOWED_NAMESPACES', None)


def jsurls(request):

    # Pattern for recognizing named parameters in urls
    RE_KWARG = re.compile(r"(\(\?P\<(.*?)\>.*?\))")
    # Pattern for recognizing unnamed url parameters
    RE_ARG = re.compile(r"(\(.*?\))")

    def handle_url_module(js_patterns, module_name, prefix="", namespace=""):
        """
        Load the module and output all of the patterns
        Recurse on the included modules
        """
        if isinstance(module_name, basestring):
            __import__(module_name)
            root_urls = sys.modules[module_name]
            patterns = root_urls.urlpatterns
        elif isinstance(module_name, types.ModuleType):
            root_urls = module_name
            patterns = root_urls.urlpatterns
        else:
            root_urls = module_name
            patterns = root_urls

        for pattern in patterns:
            if issubclass(pattern.__class__, RegexURLPattern):
                if pattern.name:
                    pattern_name = u':'.join((namespace, pattern.name)) if \
                                                    namespace else pattern.name
                    full_url = prefix + pattern.regex.pattern
                    for chr in ["^", "$"]:
                        full_url = full_url.replace(chr, "")
                    # Handle kwargs, args
                    kwarg_matches = RE_KWARG.findall(full_url)
                    if kwarg_matches:
                        for el in kwarg_matches:
                            # Prepare the output for JS resolver
                            full_url = full_url.replace(el[0], "<%s>" % el[1])
                    # After processing all kwargs try args
                    args_matches = RE_ARG.findall(full_url)
                    if args_matches:
                        for el in args_matches:
                            # Replace by a empty parameter name
                            full_url = full_url.replace(el, "<>")
                    js_patterns[pattern_name] = "/" + full_url
            elif issubclass(pattern.__class__, RegexURLResolver):
                if ALLOWED_NAMESPACES is None:
                    pass
                elif pattern.namespace not in ALLOWED_NAMESPACES:
                    continue

                if pattern.urlconf_name:
                    handle_url_module(js_patterns, pattern.urlconf_name,
                                      prefix=pattern.regex.pattern,
                                      namespace=pattern.namespace)

    js_patterns = SortedDict()
    handle_url_module(js_patterns, settings.ROOT_URLCONF)

    from django.template.loader import get_template

    response = HttpResponse(mimetype='text/javascript')
    response.write('django_js_utils_urlconf = ')
    json.dump(js_patterns, response)
    return response
