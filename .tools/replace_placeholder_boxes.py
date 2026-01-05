from pathlib import Path
import re
root = Path('.')
photos_dir = root / 'photos'
photos = [p.name for p in photos_dir.iterdir() if p.is_file()]
photos = sorted(photos)
if not photos:
    print('No photos found in photos/'); exit(1)

photo_idx = 0
html_files = [p for p in root.rglob('*.html') if '/backup/' not in str(p).replace('\\','/') and '.tools' not in str(p).replace('\\','/')]
pattern = re.compile(r'<div\s+class="placeholder-box"[^>]*>.*?</div>', flags=re.DOTALL|re.IGNORECASE)
updated = []
for p in html_files:
    text = p.read_text(encoding='utf-8')
    orig = text
    def repl(m):
        global photo_idx
        photo = photos[photo_idx % len(photos)]
        photo_idx += 1
        alt = photo.rsplit('.',1)[0].replace('-', ' ').replace('_',' ').capitalize()
        return f'<div class="activity-img" style="padding:0;"><img src="photos/{photo}" alt="{alt}"></div>'
    new_text, n = pattern.subn(repl, text)
    if n>0 and new_text!=orig:
        p.write_text(new_text, encoding='utf-8')
        updated.append((str(p), n))
        print(f'Updated {p}: replaced {n} placeholder-box')
print('Done. Files updated:', len(updated))
for f,n in updated:
    print(f, n)
