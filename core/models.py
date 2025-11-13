from django.db import models

class Campaign(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    collected_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title

class Volunteer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name

# core/models.py - Modèle Donation amélioré avec PayPal
class Donation(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('paypal', 'PayPal'),
        ('card', 'Carte bancaire'),
        ('virement', 'Virement'),
        ('other', 'Autre'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('completed', 'Complété'),
        ('failed', 'Échoué'),
        ('refunded', 'Remboursé'),
    ]
    
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True)
    donor_name = models.CharField(max_length=100, verbose_name="Nom du donateur")
    donor_email = models.EmailField(verbose_name="Email du donateur")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date")
    
    # Informations paiement
    payment_method = models.CharField(
        max_length=20, 
        choices=PAYMENT_METHOD_CHOICES, 
        default='paypal',
        verbose_name="Méthode de paiement"
    )
    payment_status = models.CharField(
        max_length=20, 
        choices=PAYMENT_STATUS_CHOICES, 
        default='pending',
        verbose_name="Statut du paiement"
    )
    
    # PayPal specific fields
    paypal_transaction_id = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name="ID Transaction PayPal"
    )
    paypal_payer_id = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name="ID Payeur PayPal"
    )
    paypal_payment_date = models.DateTimeField(
        blank=True, 
        null=True,
        verbose_name="Date paiement PayPal"
    )
    
    # Informations supplémentaires
    message = models.TextField(
        blank=True, 
        null=True, 
        help_text="Message du donateur",
        verbose_name="Message"
    )
    is_anonymous = models.BooleanField(
        default=False, 
        help_text="Don anonyme",
        verbose_name="Anonyme"
    )
    
    def __str__(self):
        return f"{self.donor_name} - {self.amount}€ ({self.get_payment_status_display()})"
    
    class Meta:
        ordering = ['-date']
        verbose_name = "Don"
        verbose_name_plural = "Dons"


# Modèle pour les produits de la boutique
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('goodies', 'Goodies DFD'),
        ('artisanat', 'Artisanat Local'),
        ('livres', 'Livres & Publications'),
        ('cadeaux', 'Cadeaux Solidaires'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Nom du produit")
    description = models.TextField(verbose_name="Description")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="Catégorie")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Image")
    stock = models.IntegerField(default=0, verbose_name="Stock disponible")
    is_available = models.BooleanField(default=True, verbose_name="Disponible")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.price}€"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Produit"
        verbose_name_plural = "Produits"


# Modèle pour les commandes de la boutique
class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('paid', 'Payé'),
        ('processing', 'En préparation'),
        ('shipped', 'Expédié'),
        ('delivered', 'Livré'),
        ('cancelled', 'Annulé'),
    ]
    
    order_number = models.CharField(max_length=50, unique=True, verbose_name="Numéro de commande")
    customer_name = models.CharField(max_length=100, verbose_name="Nom du client")
    customer_email = models.EmailField(verbose_name="Email")
    customer_phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    
    # Adresse de livraison
    shipping_address = models.TextField(verbose_name="Adresse de livraison")
    shipping_city = models.CharField(max_length=100, verbose_name="Ville")
    shipping_postal_code = models.CharField(max_length=20, verbose_name="Code postal")
    shipping_country = models.CharField(max_length=100, default="France", verbose_name="Pays")
    
    # Informations de paiement
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant total")
    payment_method = models.CharField(max_length=20, default='paypal', verbose_name="Méthode de paiement")
    payment_status = models.CharField(max_length=20, default='pending', verbose_name="Statut du paiement")
    
    # PayPal
    paypal_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    paypal_payer_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Statut de la commande
    order_status = models.CharField(
        max_length=20, 
        choices=ORDER_STATUS_CHOICES, 
        default='pending',
        verbose_name="Statut de la commande"
    )
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    paid_at = models.DateTimeField(blank=True, null=True, verbose_name="Date de paiement")
    shipped_at = models.DateTimeField(blank=True, null=True, verbose_name="Date d'expédition")
    
    # Notes
    customer_notes = models.TextField(blank=True, null=True, verbose_name="Notes du client")
    admin_notes = models.TextField(blank=True, null=True, verbose_name="Notes admin")
    
    def __str__(self):
        return f"Commande #{self.order_number} - {self.customer_name}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"


# Modèle pour les articles d'une commande
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200, verbose_name="Nom du produit")
    product_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix unitaire")
    quantity = models.IntegerField(default=1, verbose_name="Quantité")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Sous-total")
    
    def save(self, *args, **kwargs):
        self.subtotal = self.product_price * self.quantity
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
    
    class Meta:
        verbose_name = "Article de commande"
        verbose_name_plural = "Articles de commande"