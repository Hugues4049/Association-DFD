# core/urls.py
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
    path('merci/<str:nom>/', views.merci, name='merci'),
    path('confirmation/<int:donation_id>/', views.confirmation, name='confirmation'),
    path('set-language/', views.set_language, name='set_language'),
    path('inscription/', views.inscription, name='inscription'),
        # ===================================
    # DEPARTEMENTS
    # ===================================
    path('departements/education/', views.departement_view, {'slug': 'education'}, name='dept_education'),
    path('departements/sante/', views.departement_view, {'slug': 'sante'}, name='dept_sante'),
    path('departements/environnement/', views.departement_view, {'slug': 'environnement'}, name='dept_environnement'),
    path('departements/humanitaire/', views.departement_view, {'slug': 'humanitaire'}, name='dept_humanitaire'),
    path('departements/communication/', views.departement_view, {'slug': 'communication'}, name='dept_communication'),
    path('departements/developpement-durable/', views.departement_view, {'slug': 'developpement-durable'}, name='dept_developpement'),
    path('departements/innovation/', views.departement_view, {'slug': 'innovation'}, name='dept_innovation'),
    path('departements/administration/', views.departement_view, {'slug': 'administration'}, name='dept_administration'),
    
    # ===================================
    # ANTENNES
    # ===================================
    path('antennes/cameroun/', views.antenne_view, {'slug': 'cameroun'}, name='antenne_cameroun'),
    path('antennes/diaspora/', views.antenne_view, {'slug': 'diaspora'}, name='antenne_diaspora'),
    path('antennes/france/', views.antenne_view, {'slug': 'france'}, name='antenne_france'),
    path('antennes/italie/', views.antenne_view, {'slug': 'italie'}, name='antenne_italie'),
    
    # ===================================
    # NOUVELLES PAGES (RESSOURCES)
    # ===================================
    path('galerie/', views.galerie_view, name='galerie'),
    path('temoignages/', views.temoignages_view, name='temoignages'),
    path('boutique/', views.boutique_view, name='boutique'),
        # ============================================
    # ACTIONS (formulaires)
    # ============================================
    path('soumettre-temoignage/', views.soumettre_temoignage, name='soumettre_temoignage'),
    path('pre-inscription-france/', views.pre_inscription_france, name='pre_inscription_france'),
    path('pre-iscrizione-italia/', views.pre_iscrizione_italia, name='pre_iscrizione_italia'),
]