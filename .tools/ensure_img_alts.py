from pathlib import Path
import re
root = Path('.')
html_files = [p for p in root.rglob('*.html') if '/backup/' not in str(p).replace('\\','/') and '.tools' not in str(p).replace('\\','/')]
img_pattern = re.compile(r'<img\s+([^>]*?)>', flags=re.IGNORECASE)
alt_pattern = re.compile(r'\balt\s*=')
src_pattern = re.compile(r'src\s*=\s*"([^"]+)"', flags=re.IGNORECASE)
updated = []
for p in html_files:
    text = p.read_text(encoding='utf-8')
    def repl(m):
        attrs = m.group(1)
        if alt_pattern.search(attrs):
            return m.group(0)
        src_m = src_pattern.search(attrs)
        if src_m:
            src = src_m.group(1)
            filename = src.split('/')[-1]
            name = filename.rsplit('.',1)[0]
            alt = name.replace('-', ' ').replace('_',' ').capitalize()
        else:
            alt = 'image'
        # insert alt before closing
        new = f'<img {attrs} alt="{alt}">'
        return new
    new_text, n = img_pattern.subn(repl, text)
    if n>0 and new_text!=text:
        p.write_text(new_text, encoding='utf-8')
        updated.append((str(p), n))
        print(f'Updated {p}: added {n} missing alts')
print('Done. Files updated:', len(updated))
for f,n in updated:
    print(f, n)
