from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('a-propos/', views.apropos, name='apropos'),
    path('projets/', views.projets, name='projets'),
    path('participer/', views.participer, name='participer'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
]
