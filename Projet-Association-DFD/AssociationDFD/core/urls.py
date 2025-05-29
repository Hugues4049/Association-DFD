from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('a-propos/', views.apropos, name='apropos'),
    path('equipe/', views.equipe, name='equipe'),
    path('projets/', views.projets, name='projets'),
    path('campagnes/', views.campagnes, name='campagnes'),
    path('participer/', views.participer, name='participer'),
    path('blog/', views.blog, name='blog'),
    path('documents/', views.documents, name='documents'),
    path('partenaires/', views.partenaires, name='partenaires'),
    path('don/', views.don, name='don'),
    path('contact/', views.contact, name='contact'),
]
