from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Volunteer

class ContactForm(forms.Form):
    nom = forms.CharField(
        label=_("Nom"),
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Votre nom')})
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('votre@email.com')})
    )
    message = forms.CharField(
        label=_("Message"),
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': _('Votre message...'), 'rows': 5})
    )

class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['name', 'email', 'message']
        labels = {
            'name': _('Nom'),
            'email': _('Email'),
            'message': _('Message')
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Votre nom')}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('votre@email.com')}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': _('Pourquoi voulez-vous devenir bénévole ?'), 'rows': 5})
        }

class DonationForm(forms.Form):
    name = forms.CharField(
        label=_("Nom"),
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Votre nom')})
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('votre@email.com')})
    )
    amount = forms.DecimalField(
        label=_("Montant"),
        min_value=1,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': _('Montant en €'), 'step': '0.01'})
    )