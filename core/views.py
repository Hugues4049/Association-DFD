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