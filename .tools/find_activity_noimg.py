from pathlib import Path
import re
root = Path('.')
html_files = [p for p in root.rglob('*.html') if '.tools' not in str(p).replace('\\','/')]
pattern = re.compile(r'<div\s+class="activity-img"[^>]*>(.*?)</div>', flags=re.DOTALL|re.IGNORECASE)
noimg = []
for p in html_files:
    text = p.read_text(encoding='utf-8')
    for m in pattern.finditer(text):
        inner = m.group(1).strip()
        if '<img' not in inner.lower():
            noimg.append((str(p), inner[:120].replace('\n',' ')))
            break
print('Found', len(noimg), 'files with activity-img missing <img>:')
for f, snippet in noimg:
    print(f)
    print('  snippet:', snippet)
