from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import get_language, activate
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Campaign, Volunteer, Donation
from .forms import ContactForm, VolunteerForm, DonationForm
import json
from decimal import Decimal
import uuid
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from .models import Product, Order, OrderItem

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
            telephone = request.POST.get('telephone')
            localisation = request.POST.get('localisation')
            type_membre = request.POST.get('type_membre')   # correction ici
            message = request.POST.get('message', '')

            # email envoyé avec toutes les données
            send_mail(
                subject='Nouvelle inscription membre - DFD',
                message=(
                    f"Nouvelle inscription :\n"
                    f"Nom : {nom}\n"
                    f"Email : {email}\n"
                    f"Téléphone : {telephone}\n"
                    f"Localisation : {localisation}\n"
                    f"Type de membre : {type_membre}\n"
                    f"Message : {message}"
                ),
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
from django.template.loader import render_to_string
def paypal_payment_received(sender, **kwargs):
    """
    Signal handler appelé quand un paiement PayPal est confirmé (IPN)
    - Pour les dons : met à jour le don + envoie un mail texte
    - Pour les commandes boutique : met à jour la commande
      (et n'envoie un mail QUE si ce n'est pas déjà fait ailleurs)
    """
    ipn_obj = sender

    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # Vérifier que le paiement est pour nous
        if ipn_obj.receiver_email == settings.PAYPAL_RECEIVER_EMAIL:
            try:
                custom_data = ipn_obj.custom or ""

                # ========= DONATION =========
                if custom_data.startswith('donation_'):
                    donation_id = int(custom_data.split('_')[1])
                    donation = Donation.objects.get(id=donation_id)

                    # Mettre à jour le don
                    donation.payment_status = 'completed'
                    donation.paypal_transaction_id = ipn_obj.txn_id
                    donation.paypal_payer_id = ipn_obj.payer_id
                    donation.paypal_payment_date = ipn_obj.payment_date
                    donation.save()

                    # Email de confirmation finale (texte simple)
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

                # ========= COMMANDE BOUTIQUE =========
                elif custom_data.startswith('order_'):
                    order_id = int(custom_data.split('_')[1])
                    order = Order.objects.get(id=order_id)

                    # Est-ce que la commande avait déjà été marquée comme payée
                    # (par exemple dans order_success) ?
                    deja_payee = (order.payment_status == 'paid')

                    # Mettre à jour les infos paiement
                    order.payment_status = 'paid'
                    order.order_status = 'processing'
                    order.paypal_transaction_id = ipn_obj.txn_id
                    order.paypal_payer_id = ipn_obj.payer_id
                    order.paid_at = ipn_obj.payment_date
                    order.save()

                    # On n'envoie un mail via l'IPN QUE si ce n'est pas déjà fait ailleurs
                    if not deja_payee:
                        subject = f"✅ Commande #{order.order_number} confirmée - DFD"
                        html_message = render_to_string(
                            "core/emails/order_confirmation.html",
                            {"order": order},
                        )
                        # texte brut minimal au cas où
                        plain_message = (
                            f"Bonjour {order.customer_name},\n\n"
                            f"Votre commande #{order.order_number} a bien été confirmée.\n"
                            f"Montant : {order.total_amount}€\n"
                            f"Transaction : {ipn_obj.txn_id}\n\n"
                            "Merci pour votre soutien à l'association DFD."
                        )

                        send_mail(
                            subject,
                            plain_message,
                            settings.EMAIL_HOST_USER,
                            [order.customer_email],
                            html_message=html_message,
                            fail_silently=True,
                        )

                    print(f"✅ Commande #{order.order_number} confirmée via IPN")

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


from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm

from .models import Product, Order, OrderItem


def checkout(request):
    """Page de paiement pour la boutique (passage à PayPal)"""
    if request.method != 'POST':
        return redirect('boutique')

    # 1) Infos client
    customer_name = request.POST.get('customer_name')
    customer_email = request.POST.get('customer_email')
    customer_phone = request.POST.get('customer_phone', '')

    shipping_address = request.POST.get('shipping_address')
    shipping_city = request.POST.get('shipping_city')
    shipping_postal_code = request.POST.get('shipping_postal_code')
    shipping_country = request.POST.get('shipping_country', 'France')

    if not customer_name or not customer_email or not shipping_address or not shipping_city or not shipping_postal_code:
        messages.error(request, "Merci de remplir toutes les informations de livraison.")
        return redirect('boutique')

    # 2) Récupérer le panier depuis cart_json (envoyé par la boutique)
    cart_json = request.POST.get('cart_json')
    if not cart_json:
        messages.error(request, "Votre panier est vide ou invalide.")
        return redirect('boutique')

    try:
        raw_cart = json.loads(cart_json)
    except json.JSONDecodeError:
        messages.error(request, "Erreur lors de la lecture du panier.")
        return redirect('boutique')

    # raw_cart attendu : [{id, name, price, quantity, ...}, ...]
    if not isinstance(raw_cart, list) or not raw_cart:
        messages.error(request, "Votre panier est vide.")
        return redirect('boutique')

    total_amount = Decimal('0.00')
    order_items_data = []

    for item in raw_cart:
        try:
            product_id = int(item.get('id'))
            name = item.get('name')
            price = Decimal(str(item.get('price')))
            quantity = int(item.get('quantity', 1))
        except (TypeError, ValueError, Decimal.InvalidOperation):
            continue  # on ignore les lignes invalides

        if not name or quantity <= 0 or price <= 0:
            continue

        line_total = price * quantity
        total_amount += line_total

        # On essaie de retrouver un Product en base, mais c'est facultatif
        product_obj = Product.objects.filter(id=product_id).first()

        order_items_data.append({
            'product_obj': product_obj,   # peut être None
            'product_name': name,
            'product_price': price,
            'quantity': quantity,
            'subtotal': line_total,
        })

    if total_amount <= 0 or not order_items_data:
        messages.error(request, "Votre panier est vide ou invalide.")
        return redirect('boutique')

    # 3) Créer la commande
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

    # 4) Créer les OrderItem
    for item_data in order_items_data:
        OrderItem.objects.create(
            order=order,
            product=item_data['product_obj'],      # None si pas trouvé, ça passe si null=True dans le modèle
            product_name=item_data['product_name'],
            product_price=item_data['product_price'],
            quantity=item_data['quantity'],
            subtotal=item_data['subtotal'],
        )

    # 5) Préparer le formulaire PayPal
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": str(order.total_amount),
        "item_name": f"Commande DFD #{order.order_number}",
        "invoice": order.order_number,
        "currency_code": "EUR",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return_url": request.build_absolute_uri(
            reverse('order_success', kwargs={'order_id': order.id})
        ),
        "cancel_return": request.build_absolute_uri(reverse('paypal_cancel')),
        "custom": f"order_{order.id}",
    }

    paypal_form = PayPalPaymentsForm(initial=paypal_dict)

    context = {
        'order': order,
        'paypal_form': paypal_form,
    }

    return render(request, 'core/paypal_redirect.html', context)


def order_success(request, order_id):
    order = Order.objects.get(id=order_id)

    if order.payment_status != "paid":
        order.payment_status = "paid"
        order.order_status = "processing"
        order.save()

        subject = f"Confirmation de votre commande #{order.order_number}"
        message = render_to_string("core/emails/order_confirmation.html", {"order": order})

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [order.customer_email],
            html_message=message
        )

    # 👉 Vider le panier en session (au cas où il existe encore)
    request.session.pop("cart", None)

    return render(request, "core/order_success.html", {"order": order})
