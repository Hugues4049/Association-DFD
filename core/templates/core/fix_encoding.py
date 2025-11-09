# fix_encoding.py
import os
from pathlib import Path

templates_dir = Path('core/templates/core')

for html_file in templates_dir.glob('*.html'):
    with open(html_file, 'r', encoding='ISO-8859-1') as f:
        content = f.read()
    
    with open(html_file, 'w', encoding='UTF-8') as f:
        f.write(content)
    
    print(f"✅ Converti : {html_file.name}")

print("\n🎉 Tous les fichiers ont été convertis en UTF-8")
