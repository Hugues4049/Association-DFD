from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'


from django import forms

from django.utils.translation import gettext_lazy as _

class ContactForm(forms.Form):
    name = forms.CharField(label=_("Nom"))
