#!/usr/bin/env python
"""
Script de diagnostic pour identifier les problèmes de déploiement Render
Usage: python diagnostic_render.py
"""

import os
import sys
from pathlib import Path

def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def check_template_exists():
    """Vérifier si le template departement.html existe"""
    print_header("1. VÉRIFICATION DES TEMPLATES")
    
    template_path = Path('core/templates/core/departement.html')
    
    if template_path.exists():
        print(f"✅ Template trouvé : {template_path}")
        print(f"   Taille : {template_path.stat().st_size} bytes")
        
        # Vérifier les premières lignes
        with open(template_path, 'r', encoding='utf-8') as f:
            first_lines = f.readlines()[:5]
        print(f"   Premières lignes :")
        for i, line in enumerate(first_lines, 1):
            print(f"     {i}: {line.rstrip()}")
    else:
        print(f"❌ Template MANQUANT : {template_path}")
        print(f"   Chemin absolu attendu : {template_path.absolute()}")
        
        # Chercher le fichier ailleurs
        print("\n   Recherche du fichier...")
        for root, dirs, files in os.walk('core'):
            if 'departement.html' in files:
                found_path = Path(root) / 'departement.html'
                print(f"   ⚠️  Trouvé ailleurs : {found_path}")

def check_git_status():
    """Vérifier si le fichier est tracé par Git"""
    print_header("2. STATUT GIT")
    
    import subprocess
    
    try:
        # Vérifier si le fichier est dans Git
        result = subprocess.run(
            ['git', 'ls-files', 'core/templates/core/departement.html'],
            capture_output=True,
            text=True
        )
        
        if result.stdout.strip():
            print("✅ Fichier tracé par Git")
            print(f"   Chemin Git : {result.stdout.strip()}")
        else:
            print("❌ Fichier NON tracé par Git")
            print("   Le fichier existe localement mais n'a jamais été commité !")
            
        # Vérifier les fichiers non suivis
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True
        )
        
        untracked = [line for line in result.stdout.split('\n') 
                    if line.startswith('??') and 'departement' in line.lower()]
        
        if untracked:
            print("\n   ⚠️  Fichiers non suivis contenant 'departement' :")
            for line in untracked:
                print(f"     {line}")
                
    except FileNotFoundError:
        print("⚠️  Git non disponible")

def check_django_settings():
    """Vérifier les paramètres Django"""
    print_header("3. CONFIGURATION DJANGO")
    
    settings_path = Path('AssociationDFD/settings.py')
    
    if not settings_path.exists():
        print("❌ settings.py non trouvé !")
        return
    
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier TEMPLATES
    if "'APP_DIRS': True" in content:
        print("✅ APP_DIRS est activé")
    else:
        print("❌ APP_DIRS n'est pas activé")
    
    # Vérifier INSTALLED_APPS
    if "'core'" in content or '"core"' in content:
        print("✅ App 'core' dans INSTALLED_APPS")
    else:
        print("❌ App 'core' NON listée dans INSTALLED_APPS")
    
    # Vérifier DEBUG
    if "DEBUG = True" in content and "os.getenv" not in content.split("DEBUG")[1].split("\n")[0]:
        print("⚠️  DEBUG est hardcodé à True (problème potentiel)")
    else:
        print("✅ DEBUG configuré correctement")

def check_views():
    """Vérifier le fichier views.py"""
    print_header("4. VÉRIFICATION DE VIEWS.PY")
    
    views_path = Path('core/views.py')
    
    if not views_path.exists():
        print("❌ views.py non trouvé !")
        return
    
    with open(views_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Chercher departement_view
    if 'def departement_view' in content:
        print("✅ Fonction departement_view trouvée")
        
        # Extraire la fonction
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'def departement_view' in line:
                print(f"\n   Ligne {i+1} : {line}")
                # Afficher les 10 lignes suivantes
                for j in range(i+1, min(i+11, len(lines))):
                    print(f"   Ligne {j+1} : {lines[j]}")
                break
    else:
        print("❌ Fonction departement_view NON trouvée")

def check_template_syntax():
    """Vérifier la syntaxe du template"""
    print_header("5. VÉRIFICATION SYNTAXE TEMPLATE")
    
    template_path = Path('core/templates/core/departement.html')
    
    if not template_path.exists():
        print("❌ Template non trouvé, impossible de vérifier")
        return
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifications basiques
        checks = {
            "{% extends": content.count('{% extends'),
            "{% block": content.count('{% block'),
            "{% endblock": content.count('{% endblock'),
            "{% load": content.count('{% load'),
            "{{ variable }}": content.count('{{'),
        }
        
        print("📊 Statistiques du template :")
        for key, count in checks.items():
            print(f"   {key:20} : {count}")
        
        # Vérifier l'équilibre des blocks
        block_count = content.count('{% block')
        endblock_count = content.count('{% endblock')
        
        if block_count == endblock_count:
            print(f"\n✅ Blocks équilibrés ({block_count} blocks)")
        else:
            print(f"\n❌ Blocks NON équilibrés !")
            #print(f"   {% block %} : {block_count}")
            #print(f"   {% endblock %} : {endblock_count}")
            
    except UnicodeDecodeError:
        print("❌ Erreur d'encodage du fichier !")
        print("   Le fichier contient des caractères invalides")

def check_requirements():
    """Vérifier requirements.txt"""
    print_header("6. VÉRIFICATION REQUIREMENTS")
    
    req_path = Path('requirements.txt')
    
    if not req_path.exists():
        print("❌ requirements.txt non trouvé !")
        return
    
    with open(req_path, 'r') as f:
        requirements = f.read()
    
    packages = {
        'Django': 'Django' in requirements,
        'gunicorn': 'gunicorn' in requirements,
        'python-decouple': 'decouple' in requirements,
    }
    
    for package, present in packages.items():
        if present:
            print(f"✅ {package} présent")
        else:
            print(f"❌ {package} MANQUANT")

def generate_solution():
    """Générer une solution basée sur les problèmes trouvés"""
    print_header("7. SOLUTION RECOMMANDÉE")
    
    template_exists = Path('core/templates/core/departement.html').exists()
    
    if not template_exists:
        print("🔧 SOLUTION : Le template departement.html est MANQUANT")
        print("\nÉtapes à suivre :")
        print("1. Créez le fichier : core/templates/core/departement.html")
        print("2. Ajoutez le contenu du template (voir fichier fourni)")
        print("3. Commitez : git add core/templates/core/departement.html")
        print("4. Commitez : git commit -m 'fix: ajout departement.html'")
        print("5. Pushez : git push origin main")
    else:
        print("🔧 Le template existe localement")
        print("\nVérifiez si le fichier est dans Git :")
        print("   git ls-files core/templates/core/departement.html")
        print("\nSi vide, le fichier n'est pas tracé. Ajoutez-le :")
        print("   git add core/templates/core/departement.html")
        print("   git commit -m 'fix: ajout departement.html manquant'")
        print("   git push origin main")

def main():
    """Fonction principale"""
    print("\n" + "="*60)
    print("  DIAGNOSTIC COMPLET - DÉPLOIEMENT RENDER DFD")
    print("="*60)
    
    # Vérifier qu'on est dans le bon dossier
    if not Path('manage.py').exists():
        print("\n❌ ERREUR : manage.py non trouvé")
        print("   Exécutez ce script depuis la racine du projet Django\n")
        sys.exit(1)
    
    # Exécuter les vérifications
    check_template_exists()
    check_git_status()
    check_django_settings()
    check_views()
    check_template_syntax()
    check_requirements()
    generate_solution()
    
    print("\n" + "="*60)
    print("  FIN DU DIAGNOSTIC")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()