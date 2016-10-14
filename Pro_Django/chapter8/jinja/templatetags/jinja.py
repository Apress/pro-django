from django.template import Library

from chapter6.templatetags.jinja import JinjaNode

register = Library()

def loadjinja(parser, token):
    """
    Loads a template in a Jinja environment.
    """
    bits = token.split_contents()
    if len(bits) != 2:
        raise TemplateSyntaxError, "'%s' tag takes exactly one argument" % bits[0]
    template_name = bits[1].strip('"')

    nodes = parser.parse('endloadjinja')
    parser.delete_first_token()
    directories = [n.dir for n in nodes if isinstance(n, JinjaDirectoryNode)]

    template_loader = jinja2.FileSystemLoader(directories)
    environment = jinja2.Environment(loader=template_loader)
    return JinjaNode(environment.get_template(template_name))
loadjinja = register.tag(loadjinja)
