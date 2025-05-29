import pdfkit
import os

import pdfkit

html_folder = '/home/roland/Bureau/pages web'
pdf_folder = '/home/roland/Bureau/pages web'

os.makedirs(pdf_folder, exist_ok=True)

config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')  # adapte le chemin si besoin
options = {
    'enable-local-file-access': None
}

for file in os.listdir(html_folder):
    if file.endswith('.html'):
        html_path = os.path.join(html_folder, file)
        pdf_path = os.path.join(pdf_folder, file.replace('.html', '.pdf'))
        try:
            pdfkit.from_file(html_path, pdf_path, configuration=config, options=options)
            print(f"✅ {file} converti avec succès.")
        except Exception as e:
            print(f"❌ Erreur avec {file} : {e}")



#https://myaccount.google.com

#https://myaccount.google.com/apppasswords

#https://myaccount.google.com/apppasswords