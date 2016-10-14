import re

from django.views.generic import list_detail

class ObjectView(object):
    """
    Takes a model and provides a couple views designed to work with it.
    """

    regex = re.compile(r'(\d+)/$')
    list = staticmethod(list_detail.object_list)
    detail = staticmethod(list_detail.object_detail)

    def __init__(self, model):
        self.queryset = model._default_manager.all()

    def __call__(self, request, url):
        match = self.regex.match(url)
        if match:
            return self.detail(request, queryset=self.queryset, \
                               object_id=int(match.group(1)))
        else:
            return self.list(request, queryset=self.queryset)
