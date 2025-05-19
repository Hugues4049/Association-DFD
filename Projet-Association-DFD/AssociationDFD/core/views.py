from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def mission(request):
    return render(request, 'core/mission.html')

def equipe(request):
    return render(request, 'core/equipe.html')

def campagnes(request):
    # Exemple de données fictives (remplace par une vraie base plus tard)
    campaigns = [
        {'title': 'Aide aux orphelins', 'description': 'Distribution des denrées alimentaires', 'goal_amount': 500, 'collected_amount': 120},
        {'title': 'Soutien scolaire', 'description': 'Fournitures et tutorat pour enfants', 'goal_amount': 300, 'collected_amount': 900},
    ]
    return render(request, 'core/campagnes.html', {'campaigns': campaigns})

def don(request):
    if request.method == 'POST':
        # Ici tu pourrais traiter et enregistrer le don
        montant = request.POST.get('amount')
        # logiquement tu ferais un traitement ici
        return render(request, 'core/don.html', {'message': f"Merci pour votre don de {montant} € !"})

    return render(request, 'core/don.html')

def contact(request):
    if request.method == 'POST':
        # traitement du formulaire de contact ou bénévolat
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        return render(request, 'core/contact.html', {'message': f"Merci {name}, nous vous contacterons bientôt."})
    
    return render(request, 'core/contact.html')

def projets(request):
    return render(request, 'core/projets.html')

def apropos(request):
    return render(request, 'core/apropos.html')

def participer(request):
    return render(request, 'core/participer.html')

def blog(request):
    return render(request, 'core/blog.html')