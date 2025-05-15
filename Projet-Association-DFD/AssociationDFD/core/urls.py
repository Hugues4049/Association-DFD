from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('mission/', views.mission, name='mission'),
    path('equipe/', views.equipe, name='equipe'),
    path('campagnes/', views.campagnes, name='campagnes'),
    path('don/', views.don, name='don'),
    path('contact/', views.contact, name='contact'),
]
