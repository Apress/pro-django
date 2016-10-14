from django.conf.urls.defaults import *

from properties import models, views

urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^$', 'object_list', {
        'template_name': 'properties/property_list.html',
        'paginate_by': 25,
        'queryset': models.Property.objects.listed(),
    }, name='property_list'),
    url(r'^(?P<slug>\d+-[\w-]+-\d+)/$', 'object_detail', {
        'queryset': models.Property.objects.listed(),
        'slug_field': 'slug',
        'template_name': 'properties/property_detail.html',
    }, name='property_detail'),
)
