from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from chapter10.contacts import forms, models

def edit_contact(request, username=None, template_name='contacts/editor_form.html'):
    # Set up some default objects if none were defined.
    if username:
        user = get_object_or_404(models.User, username=username)
        try:
            contact = user.contact
        except models.Contact.DoesNotExist:
            contact = models.Contact(user=user)
    else:
        user = models.User()
        contact = models.Contact(user=user)

    if request.method == 'POST':
        user_form = forms.UserEditorForm(request.POST, instance=user)
        contact_form = forms.ContactEditorForm(request.POST, instance=contact)
        if user_form.is_valid() and contact_form.is_valid():
            user = user_form.save()
            contact_form.cleaned_data['user'] = user
            contact = contact_form.save()
            return HttpResponseRedirect(reverse('contact_detail',
                                                kwargs={'slug': user.username}))
    else:
        user_form = forms.UserEditorForm(instance=user)
        contact_form = forms.ContactEditorForm(instance=contact)
    return render_to_response(template_name, {
        'username': username,
        'user_form': user_form,
        'contact_form': contact_form,
    }, context_instance=RequestContext(request))
