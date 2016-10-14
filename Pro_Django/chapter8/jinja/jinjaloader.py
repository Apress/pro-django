from django.conf import settings
from django import template

try:
    import jinja2
except ImportError:
    jinja2 = None

def load_template_source(template_name, template_dirs=None):
    if template_dirs is None:
        template_dirs = settings.JINJA_TEMPLATE_DIRS

    loader = jinja2.FileSystemLoader(template_dirs)
    try:
        loader.get_source(jinja2.Environment(), template_name)
    except jinja2.TemplateNotFound:
        raise template.TemplateDoesNotExist

    directory_tags = ['{%% jinjadir "%s" %%}' % dir for dir in template_dirs]
    source = """{%% load jinja %%}
                {%% loadjinja "%s" %%}
                %s
                {%% endloadjinja %%}""" % (template_name,
                                           ''.join(directory_tags))
    return source, 'Jinja:%s' % template_name
load_template_source.is_usable = jinja2 is not None
