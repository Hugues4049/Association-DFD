from django.urls import path
from . import views

urlpatterns = [
    # Pages principales
    path('', views.home, name='home'),
    path('apropos/', views.apropos, name='apropos'),
    path('equipe/', views.equipe, name='equipe'),
    path('projets/', views.projets, name='projets'),
    path('campagnes/', views.campagnes, name='campagnes'),
    path('blog/', views.blog, name='blog'),
    path('partenaires/', views.partenaires, name='partenaires'),
    
    # Départements (templates HTML séparés)
    path('departements/education/', views.dept_education, name='dept_education'),
    path('departements/sante/', views.dept_sante, name='dept_sante'),
    path('departements/environnement/', views.dept_environnement, name='dept_environnement'),
    path('departements/humanitaire/', views.dept_humanitaire, name='dept_humanitaire'),
    path('departements/communication/', views.dept_communication, name='dept_communication'),
    path('departements/developpement/', views.dept_developpement, name='dept_developpement'),
    path('departements/innovation/', views.dept_innovation, name='dept_innovation'),
    path('departements/administration/', views.dept_administration, name='dept_administration'),
    
    # Antennes (templates HTML séparés)
    path('antennes/cameroun/', views.antenne_cameroun, name='antenne_cameroun'),
    path('antennes/diaspora/', views.antenne_diaspora, name='antenne_diaspora'),
    path('antennes/france/', views.antenne_france, name='antenne_france'),
    path('antennes/italie/', views.antenne_italie, name='antenne_italie'),
    
    # Ressources
    path('galerie/', views.galerie, name='galerie'),
    path('documents/', views.documents, name='documents'),
    path('temoignages/', views.temoignages, name='temoignages'),
    path('boutique/', views.boutique, name='boutique'),
    
    # Formulaires
    path('participer/', views.participer, name='participer'),
    path('don/', views.don, name='don'),
    path('contact/', views.contact, name='contact'),
    path('soumettre-temoignage/', views.soumettre_temoignage, name='soumettre_temoignage'),
    
    # Pages utilitaires
    path('merci/<str:nom>/', views.merci, name='merci'),
    path('confirmation/<int:donation_id>/', views.confirmation, name='confirmation'),
    path('inscription/', views.inscription, name='inscription'),
    
    # Internationalisation
    path('set-language/', views.set_language, name='set_language'),
]