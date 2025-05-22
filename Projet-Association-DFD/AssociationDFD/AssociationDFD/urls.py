"""
URL configuration for AssociationDFD project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # ← ajoute ceci
    path('i18n/', include('django.conf.urls.i18n')),
    
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


