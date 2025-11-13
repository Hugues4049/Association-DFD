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

#def don(request):
 #   """Page de don"""
  #  if request.method == 'POST':
   #     form = DonationForm(request.POST)
    #    if form.is_valid():
     #       donation = Donation.objects.create(
      #          donor_name=form.cleaned_data['name'],
     #  ""         donor_email=form.cleaned_data['email'],
        #        amount=form.cleaned_data['amount'],
         #       payment_status='pending'
          #  )
          # "" 
            #send_mail(
           #     subject='Merci pour votre don - DFD',
            #    message=f"Bonjour {donation.donor_name},\n\nMerci pour votre généreux don de {donation.amount}€.\n\nCordialement,\nL'équipe DFD",
             #   from_email=settings.EMAIL_HOST_USER,
              #  recipient_list=[donation.donor_email],
            #)
            
            #messages.success(request, f'Merci pour votre don de {donation.amount}€ !')
            #return redirect('confirmation', donation_id=donation.id)
    #else:
     #   form = DonationForm()
    
    #return render(request, 'core/don.html', {'form': form})

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


from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import get_language, activate
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
import uuid

from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

from .models import Campaign, Volunteer, Donation, Product, Order, OrderItem
from .forms import ContactForm, VolunteerForm, DonationForm

# ===================================
# VUE DON AVEC PAYPAL
# ===================================

def don(request):
    """Page de don avec intégration PayPal"""
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            # Créer le don
            donation = Donation.objects.create(
                donor_name=form.cleaned_data['name'],
                donor_email=form.cleaned_data['email'],
                amount=form.cleaned_data['amount'],
                payment_method='paypal',
                payment_status='pending'
            )
            
            # Préparer le formulaire PayPal
            paypal_dict = {
                "business": settings.PAYPAL_RECEIVER_EMAIL,
                "amount": str(donation.amount),
                "item_name": f"Don à DFD - Dreams Family of Development",
                "invoice": f"DON-{donation.id}-{uuid.uuid4().hex[:8]}",
                "currency_code": "EUR",
                "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
                "return_url": request.build_absolute_uri(reverse('paypal_return', kwargs={'donation_id': donation.id})),
                "cancel_return": request.build_absolute_uri(reverse('paypal_cancel')),
                "custom": f"donation_{donation.id}",  # Identifiant personnalisé
            }
            
            # Créer le formulaire PayPal
            form = PayPalPaymentsForm(initial=paypal_dict)
            
            context = {
                'donation': donation,
                'paypal_form': form,
            }
            
            return render(request, 'core/paypal_redirect.html', context)
    else:
        form = DonationForm()
    
    return render(request, 'core/don.html', {'form': form})


# ===================================
# CALLBACKS PAYPAL POUR DONS
# ===================================

def paypal_return(request, donation_id):
    """Page de retour après paiement PayPal réussi"""
    donation = get_object_or_404(Donation, id=donation_id)
    
    # Le statut sera mis à jour par l'IPN
    # Mais on peut afficher un message de succès provisoire
    messages.success(request, f'Merci pour votre don de {donation.amount}€ ! Nous vérifions votre paiement...')
    
    # Envoyer email de confirmation
    try:
        send_mail(
            subject='Merci pour votre don - DFD',
            message=f"""Bonjour {donation.donor_name},

Merci pour votre généreux don de {donation.amount}€ à Dreams Family of Development.

Votre paiement est en cours de vérification. Vous recevrez un email de confirmation dès que le paiement sera validé.

Cordialement,
L'équipe DFD""",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[donation.donor_email],
            fail_silently=True,
        )
    except Exception as e:
        print(f"Erreur envoi email: {e}")
    
    return render(request, 'core/paypal_success.html', {'donation': donation})


def paypal_cancel(request):
    """Page d'annulation PayPal"""
    messages.warning(request, 'Votre paiement a été annulé. Vous pouvez réessayer quand vous le souhaitez.')
    return render(request, 'core/paypal_cancel.html')


@csrf_exempt
def paypal_webhook(request):
    """
    Webhook pour recevoir les notifications IPN de PayPal
    Cette vue est appelée automatiquement par PayPal
    """
    # Le traitement est géré par django-paypal via le signal valid_ipn_received
    return JsonResponse({'status': 'ok'})


# ===================================
# SIGNAL HANDLER POUR IPN PAYPAL
# ===================================

def paypal_payment_received(sender, **kwargs):
    """
    Signal handler appelé quand un paiement PayPal est confirmé
    """
    ipn_obj = sender
    
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # Vérifier que le paiement est pour nous
        if ipn_obj.receiver_email == settings.PAYPAL_RECEIVER_EMAIL:
            
            # Extraire l'ID de la donation depuis le champ custom
            try:
                custom_data = ipn_obj.custom
                if custom_data.startswith('donation_'):
                    donation_id = int(custom_data.split('_')[1])
                    donation = Donation.objects.get(id=donation_id)
                    
                    # Mettre à jour le don
                    donation.payment_status = 'completed'
                    donation.paypal_transaction_id = ipn_obj.txn_id
                    donation.paypal_payer_id = ipn_obj.payer_id
                    donation.paypal_payment_date = ipn_obj.payment_date
                    donation.save()
                    
                    # Envoyer email de confirmation finale
                    send_mail(
                        subject='✅ Votre don a été confirmé - DFD',
                        message=f"""Bonjour {donation.donor_name},

Votre don de {donation.amount}€ a été confirmé avec succès !

Numéro de transaction : {ipn_obj.txn_id}
Date : {ipn_obj.payment_date}

Merci infiniment pour votre générosité. Grâce à vous, nous pouvons continuer nos actions sur le terrain.

Cordialement,
L'équipe DFD
Dreams Family of Development""",
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[donation.donor_email],
                        fail_silently=True,
                    )
                    
                    print(f"✅ Don #{donation.id} confirmé - Transaction: {ipn_obj.txn_id}")
                    
                elif custom_data.startswith('order_'):
                    # Traitement pour les commandes boutique
                    order_id = int(custom_data.split('_')[1])
                    order = Order.objects.get(id=order_id)
                    
                    order.payment_status = 'paid'
                    order.order_status = 'processing'
                    order.paypal_transaction_id = ipn_obj.txn_id
                    order.paypal_payer_id = ipn_obj.payer_id
                    order.paid_at = ipn_obj.payment_date
                    order.save()
                    
                    # Email de confirmation
                    send_mail(
                        subject=f'✅ Commande #{order.order_number} confirmée - DFD',
                        message=f"""Bonjour {order.customer_name},

Votre commande #{order.order_number} a été payée avec succès !

Montant : {order.total_amount}€
Transaction : {ipn_obj.txn_id}

Votre commande est en cours de préparation. Vous recevrez un email dès son expédition.

Cordialement,
L'équipe DFD""",
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[order.customer_email],
                        fail_silently=True,
                    )
                    
                    print(f"✅ Commande #{order.order_number} confirmée")
                    
            except Exception as e:
                print(f"❌ Erreur traitement IPN: {e}")
        else:
            print(f"⚠️ Email destinataire incorrect: {ipn_obj.receiver_email}")
    else:
        print(f"⚠️ Statut paiement: {ipn_obj.payment_status}")

# Connecter le signal
valid_ipn_received.connect(paypal_payment_received)


# ===================================
# BOUTIQUE AVEC PAYPAL
# ===================================

def boutique(request):
    """Page boutique avec produits"""
    products = Product.objects.filter(is_available=True)
    
    context = {
        'products': products,
    }
    
    return render(request, 'core/boutique.html', context)


def product_detail(request, product_id):
    """Détail d'un produit"""
    product = get_object_or_404(Product, id=product_id, is_available=True)
    
    return render(request, 'core/product_detail.html', {'product': product})


def checkout(request):
    """Page de paiement pour la boutique"""
    if request.method == 'POST':
        # Récupérer les données du formulaire
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        customer_phone = request.POST.get('customer_phone', '')
        
        shipping_address = request.POST.get('shipping_address')
        shipping_city = request.POST.get('shipping_city')
        shipping_postal_code = request.POST.get('shipping_postal_code')
        shipping_country = request.POST.get('shipping_country', 'France')
        
        # Récupérer les produits du panier (depuis la session par exemple)
        cart_items = request.session.get('cart', [])
        
        if not cart_items:
            messages.error(request, 'Votre panier est vide.')
            return redirect('boutique')
        
        # Calculer le total
        total_amount = Decimal('0.00')
        order_items_data = []
        
        for item in cart_items:
            product = Product.objects.get(id=item['product_id'])
            quantity = item['quantity']
            subtotal = product.price * quantity
            total_amount += subtotal
            
            order_items_data.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            })
        
        # Créer la commande
        order_number = f"CMD-{uuid.uuid4().hex[:8].upper()}"
        
        order = Order.objects.create(
            order_number=order_number,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            shipping_address=shipping_address,
            shipping_city=shipping_city,
            shipping_postal_code=shipping_postal_code,
            shipping_country=shipping_country,
            total_amount=total_amount,
            payment_method='paypal',
            payment_status='pending',
            order_status='pending',
        )
        
        # Créer les articles de commande
        for item_data in order_items_data:
            OrderItem.objects.create(
                order=order,
                product=item_data['product'],
                product_name=item_data['product'].name,
                product_price=item_data['product'].price,
                quantity=item_data['quantity'],
                subtotal=item_data['subtotal'],
            )
        
        # Préparer le formulaire PayPal
        paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": str(order.total_amount),
            "item_name": f"Commande DFD #{order.order_number}",
            "invoice": order.order_number,
            "currency_code": "EUR",
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return_url": request.build_absolute_uri(reverse('order_success', kwargs={'order_id': order.id})),
            "cancel_return": request.build_absolute_uri(reverse('paypal_cancel')),
            "custom": f"order_{order.id}",
        }
        
        form = PayPalPaymentsForm(initial=paypal_dict)
        
        context = {
            'order': order,
            'paypal_form': form,
        }
        
        return render(request, 'core/paypal_redirect.html', context)
    
    return redirect('boutique')


def order_success(request, order_id):
    """Page de succès après commande"""
    order = get_object_or_404(Order, id=order_id)
    
    # Vider le panier
    if 'cart' in request.session:
        del request.session['cart']
    
    messages.success(request, f'Merci pour votre commande #{order.order_number} !')
    
    return render(request, 'core/order_success.html', {'order': order})