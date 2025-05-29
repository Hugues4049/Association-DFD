from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import get_language

# PAGE D'ACCUEIL
def home(request):
    return render(request, 'core/home.html')

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
    campaigns = [
        {
            'title': 'Aide aux orphelins',
            'description': 'Distribution des denrées alimentaires',
            'goal_amount': 500,
            'collected_amount': 120
        },
        {
            'title': 'Soutien scolaire',
            'description': 'Fournitures et tutorat pour enfants',
            'goal_amount': 300,
            'collected_amount': 900
        },
    ]
    return render(request, 'core/campagnes.html', {'campaigns': campaigns})

# PAGE POUR PARTICIPER
def participer(request):
    return render(request, 'core/participer.html')

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
        montant = request.POST.get('amount')
        return render(request, 'core/don.html', {'message': f"Merci pour votre don de {montant} € !"})

    return render(request, 'core/don.html')

# FORMULAIRE DE CONTACT
def contact(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        message = request.POST.get('message')

        contenu = f"Nom : {nom}\nEmail : {email}\nMessage :\n{message}"

        send_mail(
            subject='Nouveau message via le site',
            message=contenu,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['rolandcontactpro@gmail.com'],
        )

        return render(request, 'core/merci.html', {'nom': nom})

    return render(request, 'core/contact.html')



def my_view(request):
    current_language = get_language()
    return render(request, 'core/base.html', {'LANGUAGE_CODE': current_language})