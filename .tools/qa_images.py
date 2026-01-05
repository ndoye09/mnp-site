from pathlib import Path
import re
root = Path('.')
html_files = [p for p in root.rglob('*.html') if '/backup/' not in str(p).replace('\\','/') and '.tools' not in str(p).replace('\\','/')]
img_re = re.compile(r'<img[^>]*src\s*=\s*["\']([^"\']+)["\'][^>]*>', re.IGNORECASE)
alt_re = re.compile(r'alt\s*=\s*"([^"]*)"', re.IGNORECASE)

missing = []
no_alt = []
counts = []
for p in sorted(html_files):
    text = p.read_text(encoding='utf-8')
    imgs = img_re.findall(text)
    cnt = 0
    for src in imgs:
        cnt += 1
        # normalize path
        src_path = (Path(p.parent) / src).resolve()
        if not src_path.exists():
            missing.append((str(p), src))
        # check alt
        # find the specific img tag
        for m in re.finditer(r'<img[^>]*src\s*=\s*["\']'+re.escape(src)+r'["\'][^>]*>', text, re.IGNORECASE):
            tag = m.group(0)
            if 'alt=' not in tag.lower():
                no_alt.append((str(p), src))
    counts.append((str(p), cnt))

print('Image counts per page:')
for f,c in counts:
    print(f'{f}: {c} images')

print('\nMissing image files:')
if not missing:
    print('None')
else:
    for f,s in missing:
        print(f'{f} -> {s}')

print('\nImages missing alt attributes:')
if not no_alt:
    print('None')
else:
    for f,s in no_alt:
        print(f'{f} -> {s}')

# Quick recommendations
print('\nRecommendations:')
if missing:
    print('- Replace or add the missing files listed above in the photos/ folder or update the HTML src paths.')
else:
    print('- All image files referenced exist.')
if no_alt:
    print('- Add meaningful alt text to the images listed above.')
else:
    print('- All images have alt attributes.')
