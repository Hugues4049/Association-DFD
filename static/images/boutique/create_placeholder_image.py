#!/usr/bin/env python3
"""
Crée des images placeholder pour la boutique DFD
Dreams Family of Development
"""
from PIL import Image, ImageDraw, ImageFont
import os

# Configuration
OUTPUT_DIR = 'static/images/boutique'
WIDTH = 800
HEIGHT = 600
BG_COLOR = '#1f1451'  # Violet DFD
TEXT_COLOR = 'white'

# Produits
PRODUCTS = [
    ('tshirt-dfd.jpg', 'T-shirt DFD\n"La main tendue"', '#2d1d73'),
    ('casquette-dfd.jpg', 'Casquette DFD\nLogo brodé', '#1a73e8'),
    ('tote-bag.jpg', 'Tote Bag\nÉcologique', '#10b981'),
    ('panier-cameroun.jpg', 'Panier Artisanal\nCameroun', '#f59e0b'),
    ('rapport-annuel.jpg', 'Rapport Annuel\n2024', '#3b82f6'),
    ('parrainage.jpg', 'Parrainage\n1 enfant = 1 an', '#ec4899')
]

def hex_to_rgb(hex_color):
    """Convertit une couleur hex en RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_placeholder(filename, text, accent_color):
    """Crée une image placeholder professionnelle"""
    # Créer l'image avec dégradé
    img = Image.new('RGB', (WIDTH, HEIGHT), color=BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Ajouter un dégradé vertical subtil
    bg_rgb = hex_to_rgb(BG_COLOR)
    accent_rgb = hex_to_rgb(accent_color)
    
    for y in range(HEIGHT):
        # Interpolation linéaire
        ratio = y / HEIGHT
        r = int(bg_rgb[0] * (1 - ratio) + accent_rgb[0] * ratio * 0.3)
        g = int(bg_rgb[1] * (1 - ratio) + accent_rgb[1] * ratio * 0.3)
        b = int(bg_rgb[2] * (1 - ratio) + accent_rgb[2] * ratio * 0.3)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))
    
    # Dessiner un rectangle décoratif avec accent
    draw.rectangle([50, 50, WIDTH-50, HEIGHT-50], outline=accent_color, width=8)
    draw.rectangle([60, 60, WIDTH-60, HEIGHT-60], outline='white', width=2)
    
    # Charger la police
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 55)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
    except:
        try:
            font_title = ImageFont.truetype("arial.ttf", 55)
            font_small = ImageFont.truetype("arial.ttf", 28)
        except:
            font_title = ImageFont.load_default()
            font_small = font_title
    
    # Ajouter le texte principal (centré)
    lines = text.split('\n')
    y_offset = HEIGHT / 2 - (len(lines) * 35)
    
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font_title)
        text_width = bbox[2] - bbox[0]
        x = (WIDTH - text_width) / 2
        y = y_offset + (i * 70)
        
        # Ombre portée
        draw.text((x+3, y+3), line, fill='#00000088', font=font_title, align='center')
        # Texte principal
        draw.text((x, y), line, fill=TEXT_COLOR, font=font_title, align='center')
    
    # Ajouter logo DFD en haut
    logo_text = "DFD"
    bbox = draw.textbbox((0, 0), logo_text, font=font_title)
    logo_width = bbox[2] - bbox[0]
    draw.text(((WIDTH - logo_width) / 2, 80), logo_text, fill=accent_color, font=font_title)
    
    # Ajouter "PLACEHOLDER" en bas
    placeholder_text = "Image placeholder - À remplacer par photo réelle"
    bbox2 = draw.textbbox((0, 0), placeholder_text, font=font_small)
    text_width2 = bbox2[2] - bbox2[0]
    draw.text(((WIDTH - text_width2) / 2, HEIGHT - 90), 
              placeholder_text, fill='#ffffff66', font=font_small)
    
    # Ajouter icône (cercle coloré)
    circle_radius = 40
    circle_x = WIDTH / 2
    circle_y = HEIGHT - 160
    draw.ellipse([circle_x - circle_radius, circle_y - circle_radius,
                  circle_x + circle_radius, circle_y + circle_radius],
                 fill=accent_color, outline='white', width=3)
    
    # Sauvegarder
    filepath = os.path.join(OUTPUT_DIR, filename)
    img.save(filepath, 'JPEG', quality=90, optimize=True)
    return filepath

def main():
    """Crée toutes les images"""
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║                                                                   ║")
    print("║         🖼️  CRÉATION DES IMAGES PLACEHOLDER BOUTIQUE            ║")
    print("║              Dreams Family of Development                         ║")
    print("║                                                                   ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    print()
    
    # Créer le dossier
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"📁 Dossier créé : {OUTPUT_DIR}")
    print()
    
    # Créer les images
    print("🎨 Création des images placeholder professionnelles...")
    print()
    
    for filename, text, color in PRODUCTS:
        filepath = create_placeholder(filename, text, color)
        filesize = os.path.getsize(filepath) // 1024
        print(f"   ✓ {filename:<30} {filesize:>4} KB   {color}")
    
    print()
    print(f"✅ {len(PRODUCTS)} images créées avec succès !")
    print()
    print(f"📍 Emplacement : {os.path.abspath(OUTPUT_DIR)}")
    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  PROCHAINES ÉTAPES")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    print("  1️⃣  Copier le dossier dans votre projet Django")
    print("      cp -r static/images/boutique /chemin/vers/AssociationDFD/static/images/")
    print()
    print("  2️⃣  Collecter les fichiers statiques")
    print("      python manage.py collectstatic")
    print()
    print("  3️⃣  Rafraîchir la page boutique")
    print("      http://localhost:8000/boutique/")
    print()
    print("  4️⃣  Plus tard : Remplacer par vos vraies photos produits")
    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    print("💡 Guide complet : GESTION_IMAGES_BOUTIQUE.md")
    print()

if __name__ == '__main__':
    try:
        main()
    except ImportError:
        print("❌ Erreur : Le module Pillow n'est pas installé")
        print()
        print("   Installation :")
        print("   pip install Pillow")
        print()
        print("   Puis relancez ce script :")
        print("   python create_placeholder_images.py")
    except Exception as e:
        print(f"❌ Erreur : {e}")
        print()
        print("   Consultez GESTION_IMAGES_BOUTIQUE.md pour plus d'aide")