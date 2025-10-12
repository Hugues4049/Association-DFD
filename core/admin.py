from django.contrib import admin
from .models import Campaign, Volunteer

admin.site.register(Campaign)
admin.site.register(Volunteer)

from django import forms

from django.utils.translation import gettext_lazy as _

class ContactForm(forms.Form):
    name = forms.CharField(label=_("Nom"))
