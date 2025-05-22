from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('a-propos/', views.apropos, name='apropos'),
    path('projets/', views.projets, name='projets'),
    path('participer/', views.participer, name='participer'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('documents/', views.documents, name='documents'),
    path('partenaires/', views.partenaires, name='partenaires')

]

from django import forms

from django.utils.translation import gettext_lazy as _

class ContactForm(forms.Form):
    name = forms.CharField(label=_("Nom"))


from django.utils.translation import get_language

def my_view(request):
    current_language = get_language()
    # passe current_language au contexte
    return render(request, 'core/base.html', {'LANGUAGE_CODE': current_language})

from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include


