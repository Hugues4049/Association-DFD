from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import get_language, activate
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Campaign, Volunteer, Donation
from .forms import ContactForm, VolunteerForm, DonationForm

# ===================================
# PAGES PRINCIPALES
# ===================================

def home(request):
    """Page d'accueil"""
    campaigns = Campaign.objects.all().order_by('-start_date')[:3]
    context = {'campaigns': campaigns}
    return render(request, 'core/home.html', context)

def apropos(request):
    """Page À propos"""
    return render(request, 'core/apropos.html')

def equipe(request):
    """Page Équipe"""
    return render(request, 'core/equipe.html')

def projets(request):
    """Page Projets"""
    return render(request, 'core/projets.html')

def campagnes(request):
    """Page Campagnes avec progression"""
    campaigns = Campaign.objects.all().order_by('-start_date')
    
    for campaign in campaigns:
        if campaign.goal_amount > 0:
            campaign.progress = (campaign.collected_amount / campaign.goal_amount) * 100
        else:
            campaign.progress = 0
    
    return render(request, 'core/campagnes.html', {'campaigns': campaigns})

def blog(request):
    """Page Blog"""
    return render(request, 'core/blog.html')

def partenaires(request):
    """Page Partenaires"""
    return render(request, 'core/partenaires.html')

# ===================================
# DÉPARTEMENTS (Templates HTML séparés)
# ===================================

def dept_education(request):
    """Département Éducation"""
    return render(request, 'core/departements/education.html')

def dept_sante(request):
    """Département Santé"""
    return render(request, 'core/departements/sante.html')

def dept_environnement(request):
    """Département Environnement"""
    return render(request, 'core/departements/environnement.html')

def dept_humanitaire(request):
    """Département Humanitaire"""
    return render(request, 'core/departements/humanitaire.html')

def dept_communication(request):
    """Département Communication"""
    return render(request, 'core/departements/communication.html')

def dept_developpement(request):
    """Département Développement Durable"""
    return render(request, 'core/departements/developpement.html')

def dept_innovation(request):
    """Département Innovation & Numérique"""
    return render(request, 'core/departements/innovation.html')

def dept_administration(request):
    """Département Administration & Finances"""
    return render(request, 'core/departements/administration.html')

# ===================================
# ANTENNES (Templates HTML séparés)
# ===================================

def antenne_cameroun(request):
    """Antenne Cameroun"""
    return render(request, 'core/antennes/cameroun.html')

def antenne_diaspora(request):
    """Antenne Diaspora"""
    return render(request, 'core/antennes/diaspora.html')

def antenne_france(request):
    """Antenne France (À venir)"""
    return render(request, 'core/antennes/france.html')

def antenne_italie(request):
    """Antenne Italie (À venir)"""
    return render(request, 'core/antennes/italie.html')

# ===================================
# RESSOURCES
# ===================================

def galerie(request):
    """Galerie photos/vidéos/podcasts"""
    return render(request, 'core/ressources/galerie.html')

def documents(request):
    """Bibliothèque documentaire"""
    return render(request, 'core/ressources/documents.html')

def temoignages(request):
    """Témoignages"""
    return render(request, 'core/ressources/temoignages.html')

def boutique(request):
    """Boutique solidaire"""
    return render(request, 'core/boutique.html')

# ===================================
# FORMULAIRES
# ===================================

def participer(request):
    """Page Participer (bénévole/membre)"""
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'volunteer':
            form = VolunteerForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Merci ! Votre candidature a été enregistrée.')
                return redirect('participer')
        
        elif form_type == 'member':
            nom = request.POST.get('nom')
            email = request.POST.get('email')
            
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

def don(request):
    """Page de don"""
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = Donation.objects.create(
                donor_name=form.cleaned_data['name'],
                donor_email=form.cleaned_data['email'],
                amount=form.cleaned_data['amount'],
                payment_status='pending'
            )
            
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

def contact(request):
    """Formulaire de contact"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data['nom']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

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

def soumettre_temoignage(request):
    """Soumettre un témoignage"""
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        role = request.POST.get('role')
        temoignage = request.POST.get('temoignage')
        
        # TODO: Enregistrer en base de données
        messages.success(request, 'Merci pour votre témoignage ! Il sera examiné avant publication.')
        return redirect('temoignages')
    return redirect('temoignages')

# ===================================
# PAGES UTILITAIRES
# ===================================

def merci(request, nom):
    """Page de remerciement après contact"""
    return render(request, 'core/merci.html', {'nom': nom})

def confirmation(request, donation_id):
    """Page de confirmation de don"""
    try:
        donation = Donation.objects.get(id=donation_id)
        return render(request, 'core/confirmation.html', {'donation': donation})
    except Donation.DoesNotExist:
        messages.error(request, 'Don introuvable.')
        return redirect('home')

def inscription(request):
    """Page d'inscription"""
    if request.method == 'POST':
        messages.success(request, "Inscription réussie !")
        return redirect('home')
    
    return render(request, 'core/inscription.html')

# ===================================
# INTERNATIONALISATION
# ===================================

def set_language(request):
    """Changer la langue du site"""
    if request.method == 'POST':
        language = request.POST.get('language')
        if language:
            activate(language)
            response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
            return response
    return redirect('home')