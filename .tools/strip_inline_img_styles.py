from pathlib import Path
import re
root = Path('.')
html_files = [p for p in root.rglob('*.html') if '/backup/' not in str(p).replace('\\','/') and '.tools' not in str(p).replace('\\','/')]
updated = []
pattern = re.compile(r'(<img[^>]*?)\s+style="[^"]*"([^>]*>)', flags=re.IGNORECASE)
for p in html_files:
    text = p.read_text(encoding='utf-8')
    new_text, n = pattern.subn(r"\1\2", text)
    if n>0:
        p.write_text(new_text, encoding='utf-8')
        updated.append((str(p), n))
        print(f'Updated {p}: removed {n} inline img styles')
print('Done. Files updated:', len(updated))
for f,n in updated:
    print(f, n)
