import os

# Mets ici le chemin exact existant
repertoire = '/home/roland/Bureau/SERIES_PROJETS/Projet-Association-DFD/AssociationDFD/static/images/Photo-DFD-Foyer/Video-DFD-foyer'

# Vérifie d'abord si le dossier existe
if os.path.exists(repertoire):
    fichiers = [f for f in os.listdir(repertoire) if os.path.isfile(os.path.join(repertoire, f))]
    for fichier in fichiers:
        print(fichier)
else:
    print(f"Le dossier spécifié n'existe pas : {repertoire}")