from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import get_language
from django.contrib import messages
from .models import Campaign, Volunteer, Donation
from .forms import ContactForm, VolunteerForm, DonationForm

# PAGE D'ACCUEIL
def home(request):
    # Récupérer les campagnes actives
    campaigns = Campaign.objects.all().order_by('-start_date')[:3]
    context = {
        'campaigns': campaigns
    }
    return render(request, 'core/home.html', context)

# PAGE "À PROPOS"
def apropos(request):
    return render(request, 'core/apropos.html')

# PAGE ÉQUIPE
def equipe(request):
    return render(request, 'core/equipe.html')

# PAGE PROJETS
def projets(request):
    return render(request, 'core/projets.html')

# PAGE CAMPAGNES
def campagnes(request):
    campaigns = Campaign.objects.all().order_by('-start_date')
    
    # Calculer le pourcentage de progression pour chaque campagne
    for campaign in campaigns:
        if campaign.goal_amount > 0:
            campaign.progress = (campaign.collected_amount / campaign.goal_amount) * 100
        else:
            campaign.progress = 0
    
    return render(request, 'core/campagnes.html', {'campaigns': campaigns})

# PAGE POUR PARTICIPER
def participer(request):
    if request.method == 'POST':
        # Déterminer quel formulaire a été soumis
        form_type = request.POST.get('form_type')
        
        if form_type == 'volunteer':
            form = VolunteerForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Merci ! Votre candidature a été enregistrée.')
                return redirect('participer')
        
        elif form_type == 'member':
            # Logique pour l'inscription comme membre
            nom = request.POST.get('nom')
            email = request.POST.get('email')
            
            # Envoyer un email de confirmation
            send_mail(
                subject='Nouvelle inscription membre - DFD',
                message=f"Nouvelle inscription :\nNom : {nom}\nEmail : {email}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
            )
            
            messages.success(request, f'Merci {nom} ! Votre inscription a été enregistrée.')
            return redirect('participer')
    
    volunteer_form = VolunteerForm()
    return render(request, 'core/participer.html', {'volunteer_form': volunteer_form})

# PAGE BLOG
def blog(request):
    return render(request, 'core/blog.html')

# PAGE DOCUMENTS
def documents(request):
    return render(request, 'core/documents.html')

# PAGE PARTENAIRES
def partenaires(request):
    return render(request, 'core/partenaires.html')

# PAGE DE DON
def don(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            # Créer la donation
            donation = Donation.objects.create(
                donor_name=form.cleaned_data['name'],
                donor_email=form.cleaned_data['email'],
                amount=form.cleaned_data['amount'],
                payment_status='pending'
            )
            
            # TODO: Intégrer le système de paiement (Stripe, PayPal, etc.)
            
            # Envoyer un email de confirmation
            send_mail(
                subject='Merci pour votre don - DFD',
                message=f"Bonjour {donation.donor_name},\n\nMerci pour votre généreux don de {donation.amount}€.\n\nCordialement,\nL'équipe DFD",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[donation.donor_email],
            )
            
            messages.success(request, f'Merci pour votre don de {donation.amount}€ !')
            return redirect('confirmation', donation_id=donation.id)
    else:
        form = DonationForm()
    
    return render(request, 'core/don.html', {'form': form})

# FORMULAIRE DE CONTACT
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data['nom']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Envoyer l'email
            try:
                send_mail(
                    subject=f'Nouveau message de {nom} via le site DFD',
                    message=f"Nom : {nom}\nEmail : {email}\n\nMessage :\n{message}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.EMAIL_HOST_USER],
                )
                messages.success(request, f'Merci {nom} ! Votre message a été envoyé.')
                return redirect('merci', nom=nom)
            except Exception as e:
                messages.error(request, 'Une erreur est survenue. Veuillez réessayer.')
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})

# PAGE DE REMERCIEMENT
def merci(request, nom):
    return render(request, 'core/merci.html', {'nom': nom})

# PAGE DE CONFIRMATION DE DON
def confirmation(request, donation_id):
    try:
        donation = Donation.objects.get(id=donation_id)
        return render(request, 'core/confirmation.html', {'donation': donation})
    except Donation.DoesNotExist:
        messages.error(request, 'Don introuvable.')
        return redirect('home')

# CHANGEMENT DE LANGUE
from django.utils.translation import activate
from django.http import HttpResponseRedirect

def set_language(request):
    if request.method == 'POST':
        language = request.POST.get('language')
        if language:
            activate(language)
            response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
            return response
    return redirect('home')

from django.shortcuts import render, redirect
from django.contrib import messages

def inscription(request):
    if request.method == 'POST':
        # Logique d'inscription ici (à compléter selon vos besoins)
        # Par exemple : traiter un formulaire d'inscription
        messages.success(request, "Inscription réussie !")
        return redirect('core:home')  # ou une autre page
    
    return render(request, 'core/inscription.html')


# views.py - A ajouter a votre fichier views.py existant

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

# ===================================
# DONNEES DES DEPARTEMENTS
# ===================================

DEPARTEMENTS_DATA = {
    'education': {
        'titre': 'Education',
        'slogan': 'Construire l\'avenir par le savoir',
        'icone': 'fas fa-graduation-cap',
        'image_hero': 'images/hero/education.jpg',
        'description': 'Le departement Education de DFD œuvre pour garantir l\'acces a une education de qualite pour tous. Nous croyons que l\'education est la cle du developpement et de l\'epanouissement personnel.',
        'missions': [
            {
                'icone': 'fas fa-book-reader',
                'titre': 'Scolarisation',
                'description': 'Faciliter l\'acces a l\'ecole pour les enfants defavorises'
            },
            {
                'icone': 'fas fa-chalkboard-teacher',
                'titre': 'Formation',
                'description': 'Former des enseignants qualifies et engages'
            },
            {
                'icone': 'fas fa-laptop',
                'titre': 'Numerique',
                'description': 'Developper les competences numeriques des eleves'
            },
        ],
        'projets': [
            {
                'titre': 'Programme Ecole pour Tous',
                'description': 'Distribution de fournitures scolaires a 500 enfants',
                'lieu': 'Yaounde, Cameroun',
                'date': 'Septembre 2024',
                'beneficiaires': '500 enfants',
                'status': 'En cours',
                'image': 'images/projets/education1.jpg'
            },
        ],
        'equipe': [
            {
                'nom': 'Marie Dupont',
                'role': 'Responsable Education',
                'bio': 'Enseignante depuis 15 ans, passionnee par l\'education inclusive',
                'photo': 'images/equipe/marie.jpg'
            },
        ]
    },
    'sante': {
        'titre': 'Sante',
        'slogan': 'La sante pour tous, partout',
        'icone': 'fas fa-heartbeat',
        'image_hero': 'images/hero/sante.jpg',
        'description': 'Notre departement Sante travaille pour garantir l\'acces aux soins de sante primaires et promouvoir le bien-etre des communautes vulnerables.',
        'missions': [
            {
                'icone': 'fas fa-hospital',
                'titre': 'Soins primaires',
                'description': 'Acces aux soins de base pour tous'
            },
            {
                'icone': 'fas fa-syringe',
                'titre': 'Prevention',
                'description': 'Campagnes de vaccination et sensibilisation'
            },
            {
                'icone': 'fas fa-pills',
                'titre': 'Medicaments',
                'description': 'Distribution de medicaments essentiels'
            },
        ],
        'projets': [
            {
                'titre': 'Campagne de Sante Gratuite',
                'description': 'Consultations et soins gratuits a Etam Bafia',
                'lieu': 'Etam Bafia, Cameroun',
                'date': '19-20 Septembre 2025',
                'beneficiaires': '1000 personnes',
                'status': 'A venir',
                'image': 'images/projets/sante1.jpg'
            },
        ],
        'equipe': []
    },
    'environnement': {
        'titre': 'Environnement',
        'slogan': 'Proteger notre planete pour les generations futures',
        'icone': 'fas fa-leaf',
        'image_hero': 'images/hero/environnement.jpg',
        'description': 'Le departement Environnement œuvre pour la preservation de l\'environnement et la promotion du developpement durable.',
        'missions': [
            {
                'icone': 'fas fa-tree',
                'titre': 'Reboisement',
                'description': 'Planter des arbres pour lutter contre la deforestation'
            },
            {
                'icone': 'fas fa-recycle',
                'titre': 'Recyclage',
                'description': 'Promouvoir le recyclage et la gestion des dechets'
            },
            {
                'icone': 'fas fa-sun',
                'titre': 'Energies renouvelables',
                'description': 'Developper l\'acces aux energies propres'
            },
        ],
        'projets': [],
        'equipe': []
    },
    'humanitaire': {
        'titre': 'Humanitaire',
        'slogan': 'L\'humain au cœur de nos actions',
        'icone': 'fas fa-hands-helping',
        'image_hero': 'images/hero/humanitaire.jpg',
        'description': 'Notre departement Humanitaire intervient aupres des populations en situation de vulnerabilite pour leur apporter un soutien immediat et durable.',
        'missions': [
            {
                'icone': 'fas fa-home',
                'titre': 'Aide d\'urgence',
                'description': 'Intervention rapide en cas de crise'
            },
            {
                'icone': 'fas fa-utensils',
                'titre': 'Securite alimentaire',
                'description': 'Distribution de vivres aux familles demunies'
            },
            {
                'icone': 'fas fa-tshirt',
                'titre': 'Aide vestimentaire',
                'description': 'Distribution de vetements et articles de premiere necessite'
            },
        ],
        'projets': [],
        'equipe': []
    },
    'communication': {
        'titre': 'Communication',
        'slogan': 'Amplifier les voix pour un monde meilleur',
        'icone': 'fas fa-bullhorn',
        'image_hero': 'images/hero/communication.jpg',
        'description': 'Le departement Communication assure la visibilite de nos actions et sensibilise le public a nos causes.',
        'missions': [
            {
                'icone': 'fas fa-camera',
                'titre': 'Reportages',
                'description': 'Documenter nos actions sur le terrain'
            },
            {
                'icone': 'fas fa-share-alt',
                'titre': 'Reseaux sociaux',
                'description': 'Communiquer sur nos projets et campagnes'
            },
            {
                'icone': 'fas fa-newspaper',
                'titre': 'Publications',
                'description': 'Rediger des articles et rapports'
            },
        ],
        'projets': [],
        'equipe': []
    },
    'developpement-durable': {
        'titre': 'Developpement Durable',
        'slogan': 'Batir un avenir durable ensemble',
        'icone': 'fas fa-seedling',
        'image_hero': 'images/hero/developpement.jpg',
        'description': 'Notre departement Developpement Durable promeut des projets economiques et sociaux respectueux de l\'environnement.',
        'missions': [
            {
                'icone': 'fas fa-industry',
                'titre': 'Entrepreneuriat',
                'description': 'Soutenir les entrepreneurs locaux'
            },
            {
                'icone': 'fas fa-tractor',
                'titre': 'Agriculture durable',
                'description': 'Promouvoir des pratiques agricoles responsables'
            },
            {
                'icone': 'fas fa-coins',
                'titre': 'Micro-credit',
                'description': 'Faciliter l\'acces au financement'
            },
        ],
        'projets': [],
        'equipe': []
    },
    'innovation': {
        'titre': 'Innovation & Numerique',
        'slogan': 'Innover pour mieux servir',
        'icone': 'fas fa-lightbulb',
        'image_hero': 'images/hero/innovation.jpg',
        'description': 'Le departement Innovation & Numerique developpe des solutions technologiques pour amplifier l\'impact de nos actions.',
        'missions': [
            {
                'icone': 'fas fa-code',
                'titre': 'Developpement web',
                'description': 'Creer des outils numeriques pour nos projets'
            },
            {
                'icone': 'fas fa-mobile-alt',
                'titre': 'Applications mobiles',
                'description': 'Developper des apps pour faciliter l\'acces a nos services'
            },
            {
                'icone': 'fas fa-database',
                'titre': 'Gestion de donnees',
                'description': 'Optimiser la collecte et l\'analyse de donnees'
            },
        ],
        'projets': [],
        'equipe': []
    },
    'administration': {
        'titre': 'Administration & Finances',
        'slogan': 'Une gestion transparente et efficace',
        'icone': 'fas fa-chart-line',
        'image_hero': 'images/hero/administration.jpg',
        'description': 'Le departement Administration & Finances assure la bonne gestion des ressources de l\'association.',
        'missions': [
            {
                'icone': 'fas fa-calculator',
                'titre': 'Comptabilite',
                'description': 'Gestion rigoureuse des finances'
            },
            {
                'icone': 'fas fa-file-invoice',
                'titre': 'Reporting',
                'description': 'Transparence et rapports financiers'
            },
            {
                'icone': 'fas fa-users-cog',
                'titre': 'Ressources humaines',
                'description': 'Gestion des benevoles et du personnel'
            },
        ],
        'projets': [],
        'equipe': []
    },
}

# ===================================
# DONNEES DES ANTENNES
# ===================================

ANTENNES_DATA = {
    'cameroun': {
        'titre': 'DFD Cameroun',
        'pays': 'Cameroun',
        'drapeau': '🇨🇲',
        'status': 'active',
        'description': 'Notre antenne principale au Cameroun coordonne l\'ensemble de nos actions sur le terrain.',
        'adresse': 'Yaounde face Hotel SOMMATEL, palais de sport',
        'telephone': '+237 xxx xxx xxx',
        'email': 'cameroun@dfd.org',
        'responsable': 'Nathanael Toukea',
        'equipe': 15,
        'beneficiaires': '5000+',
        'projets_actifs': 12,
    },
    'diaspora': {
        'titre': 'DFD Diaspora',
        'pays': 'International',
        'drapeau': '🌍',
        'status': 'active',
        'description': 'Notre reseau diaspora mobilise les camerounais et amis du Cameroun a travers le monde.',
        'responsable': 'En cours de nomination',
        'equipe': 8,
        'beneficiaires': '2000+',
        'projets_actifs': 5,
    },
    'france': {
        'titre': 'DFD France',
        'pays': 'France',
        'drapeau': '🇫🇷',
        'status': 'a_venir',
        'description': 'L\'antenne France est en cours de creation. Elle permettra de renforcer nos actions et notre collecte de fonds en Europe.',
        'date_prevue': 'T2 2026',
    },
    'italie': {
        'titre': 'DFD Italie',
        'pays': 'Italie',
        'drapeau': '🇮🇹',
        'status': 'a_venir',
        'description': 'L\'antenne Italie est en projet. Elle nous permettra de developper notre reseau europeen.',
        'date_prevue': 'T4 2026',
    },
}

# ===================================
# VUES DEPARTEMENTS
# ===================================

def departement_view(request, slug):
    """Vue pour afficher un departement"""
    # Vérifier si le département existe
    departement = DEPARTEMENTS_DATA.get(slug)
    
    if not departement:
        # Log pour debug
        print(f"❌ Département '{slug}' non trouvé dans DEPARTEMENTS_DATA")
        print(f"✅ Départements disponibles: {list(DEPARTEMENTS_DATA.keys())}")
        
        # Rediriger vers l'accueil avec un message
        from django.contrib import messages
        messages.warning(request, f"Le département '{slug}' n'existe pas.")
        return redirect('home')
    
    context = {
        'departement': departement,
        'slug': slug
    }
    
    try:
        return render(request, 'core/departement.html', context)
    except Exception as e:
        # Si erreur de template, afficher le détail
        print(f"❌ Erreur template: {str(e)}")
        from django.http import HttpResponse
        return HttpResponse(f"Erreur: {str(e)}<br>Département: {slug}<br>Context: {context}", status=500)

# ===================================
# VUES ANTENNES
# ===================================
def antenne_view(request, slug):
    """Vue pour afficher une antenne avec gestion d'erreur robuste"""
    
    if slug not in ANTENNES_DATA:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Antenne '{slug}' non trouvée. Disponibles: {list(ANTENNES_DATA.keys())}")
        
        messages.warning(request, f"L'antenne '{slug}' n'existe pas.")
        return redirect('home')
    
    antenne = ANTENNES_DATA[slug]
    context = {
        'antenne': antenne,
        'slug': slug
    }
    
    try:
        return render(request, 'core/antenne.html', context)
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Erreur rendering antenne '{slug}': {str(e)}")
        
        messages.error(request, "Une erreur est survenue. Veuillez réessayer.")
        return redirect('home')

# ===================================
# NOUVELLES PAGES
# ===================================

def galerie_view(request):
    """Vue pour la galerie photos/videos/podcasts"""
    context = {
        'title': 'Galerie',
    }
    return render(request, 'core/galerie.html', context)

def temoignages_view(request):
    """Vue pour les temoignages"""
    context = {
        'title': 'Temoignages',
    }
    return render(request, 'core/temoignages.html', context)

def boutique_view(request):
    """Vue pour la boutique solidaire"""
    context = {
        'title': 'Boutique Solidaire',
    }
    return render(request, 'core/boutique.html', context)



from django.shortcuts import render, redirect
from django.contrib import messages

# DÉPARTEMENTS
def education(request):
    return render(request, 'core/education.html')

def sante(request):
    return render(request, 'core/sante.html')

def environnement(request):
    return render(request, 'core/environnement.html')

def humanitaire(request):
    return render(request, 'core/humanitaire.html')

def communication(request):
    return render(request, 'core/communication.html')

def developpement_durable(request):
    return render(request, 'core/developpement-durable.html')

def innovation(request):
    return render(request, 'core/innovation.html')

def administration(request):
    return render(request, 'core/administration.html')

# ANTENNES
def cameroun_antenne(request):
    return render(request, 'core/cameroun-antenne.html')

def diaspora_antenne(request):
    return render(request, 'core/diaspora-antenne.html')

def france_antenne(request):
    return render(request, 'core/france-antenne.html')

def italie_antenne(request):
    return render(request, 'core/italie-antenne.html')

# RESSOURCES
def temoignages(request):
    return render(request, 'core/temoignages.html')

def galerie(request):
    return render(request, 'core/galerie.html')

def boutique(request):
    return render(request, 'core/boutique.html')

# FORMULAIRES
def soumettre_temoignage(request):
    if request.method == 'POST':
        # Traiter le formulaire de témoignage
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        role = request.POST.get('role')
        temoignage = request.POST.get('temoignage')
        
        # TODO: Enregistrer en base de données ou envoyer par email
        messages.success(request, 'Merci pour votre témoignage ! Il sera examiné avant publication.')
        return redirect('temoignages')
    return redirect('temoignages')

def pre_inscription_france(request):
    if request.method == 'POST':
        # Traiter le formulaire de pré-inscription France
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        ville = request.POST.get('ville')
        interet = request.POST.get('interet')
        
        # TODO: Enregistrer en base de données
        messages.success(request, 'Merci ! Vous serez informé(e) dès l\'ouverture de DFD France.')
        return redirect('france_antenne')
    return redirect('france_antenne')

def pre_iscrizione_italia(request):
    if request.method == 'POST':
        # Traiter le formulaire de pré-inscription Italie
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        citta = request.POST.get('citta')
        interesse = request.POST.get('interesse')
        
        # TODO: Enregistrer en base de données
        messages.success(request, 'Grazie! Sarai informato/a all\'apertura di DFD Italia.')
        return redirect('italie_antenne')
    return redirect('italie_antenne')