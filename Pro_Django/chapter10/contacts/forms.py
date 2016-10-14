from django import forms
from django.contrib.localflavor.us import forms as us_forms
from django.contrib.auth.models import User

from chapter10.contacts.models import Contact

class UserEditorForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class ContactEditorForm(forms.ModelForm):
    phone_number = us_forms.USPhoneNumberField(required=False)
    state = us_forms.USStateField(widget=us_forms.USStateSelect, required=False)
    zip_code = us_forms.USZipCodeField(label='ZIP Code', required=False)

    class Meta:
        model = Contact
        exclude = ('user',)
