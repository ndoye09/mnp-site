import os, re
from pathlib import Path

root = Path('.')
count = 0
changed_files = []

# mapping of old filenames to new normalized filenames (common cases)
mapping = {
    'deenr\u00e9e_alimentaire.jpg': 'denree-alimentaire.jpg',
    'deenrée_alimentaire.jpg': 'denree-alimentaire.jpg',
    'don de sang.jpg': 'don-de-sang.jpg',
    'don de sang2.jpg': 'don-de-sang2.jpg',
    'don_daara.jpg': 'don-daara.jpg',
    'don_daara2.jpg': 'don-daara2.jpg',
    'synth\u00e9se.jpg': 'synthese.jpg',
    'synthése.jpg': 'synthese.jpg',
    'WhatsApp Image 2025-12-31 at 23.32.28.jpeg': 'whatsapp-image-2025-12-31-23-32-28.jpeg'
}

def make_alt_from_src(src):
    name = os.path.basename(src)
    name_noext = os.path.splitext(name)[0]
    alt = re.sub(r'[_\-]+', ' ', name_noext)
    alt = re.sub(r'%20', ' ', alt)
    alt = re.sub(r'\s+', ' ', alt).strip()
    if not alt:
        alt = 'image'
    return alt.capitalize()

for p in root.rglob('*.html'):
    if '\\backup\\' in str(p) or '/backup/' in str(p):
        continue
    text = p.read_text(encoding='utf-8')

    # first replace any leftover old filenames
    for old, new in mapping.items():
        if old in text:
            text = text.replace(old, new)

    # then ensure img tags have non-empty alt attributes
    def repl(match):
        tag = match.group(0)
        src_match = re.search(r'src\s*=\s*"([^"]+)"', tag)
        if not src_match:
            return tag
        src = src_match.group(1)
        alt_text = make_alt_from_src(src)
        # if alt present but empty, replace
        if re.search(r'\balt\s*=\s*"\s*"', tag, re.IGNORECASE):
            return re.sub(r'\balt\s*=\s*"\s*"', f' alt="{alt_text}"', tag, flags=re.IGNORECASE)
        # if alt present with value, keep it
        if re.search(r'\balt\s*=\s*"[^"]+"', tag, re.IGNORECASE):
            return tag
        # no alt -> insert
        if tag.endswith('/>'):
            return tag[:-2] + f' alt="{alt_text}" />'
        else:
            return tag[:-1] + f' alt="{alt_text}">'

    new_text, n = re.subn(r'<img\b[^>]*>', repl, text, flags=re.IGNORECASE)
    if n > 0 and new_text != text:
        p.write_text(new_text, encoding='utf-8')
        count += 1
        changed_files.append(str(p))

print(f"Processed files: {count}")
for f in changed_files:
    print(f)
