from django.conf.urls.defaults import *

from chapter10.contacts import models, views

urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^$', 'object_list', {
        'queryset': models.Contact.objects.all(),
        'template_name': 'contacts/list.html',
        'paginate_by': 25,
    }, name='contact_list'),
    url(r'^add/$', views.edit_contact, {
        'template_name': 'contacts/editor_form.html',
    }, name='contact_add_form'),
    url(r'^(?P<slug>[\w-]+)/$', 'object_detail', {
        'queryset': models.Contact.objects.all(),
        'slug_field': 'user__username',
        'template_name': 'contacts/detail.html',
    }, name='contact_detail'),
    url(r'^(?P<username>[\w-]+)/edit/$', views.edit_contact, {
        'template_name': 'contacts/editor_form.html',
    }, name='contact_edit_form'),
)
