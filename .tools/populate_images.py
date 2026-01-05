import re
from pathlib import Path
import os

root = Path('.')
photos_dir = root / 'photos'
photos = [p.name for p in photos_dir.iterdir() if p.is_file()]
photos = sorted(photos)
if not photos:
    print('No photos found in photos/'); exit(1)

photo_idx = 0
changed = []

html_files = [p for p in root.rglob('*.html') if '/backup/' not in str(p).replace('\\','/') and '.tools' not in str(p).replace('\\','/')]

for p in html_files:
    text = p.read_text(encoding='utf-8')
    orig = text

    # replace activity-img blocks
    def activity_repl(m):
        global photo_idx
        photo = photos[photo_idx % len(photos)]
        photo_idx += 1
        alt = os.path.splitext(photo)[0].replace('-', ' ').replace('_', ' ').capitalize()
        return f'<div class="activity-img" style="padding:0;"><img src="photos/{photo}" alt="{alt}" style="width:100%; height:220px; object-fit:cover; display:block;"></div>'

    text, n1 = re.subn(r'<div\s+class="activity-img"[^>]*>.*?</div>', activity_repl, text, flags=re.DOTALL|re.IGNORECASE)

    # replace article-image blocks (.article-image)
    def article_repl(m):
        global photo_idx
        photo = photos[photo_idx % len(photos)]
        photo_idx += 1
        alt = os.path.splitext(photo)[0].replace('-', ' ').replace('_', ' ').capitalize()
        return f'<div class="article-image p-0" style="padding:0;"><img src="photos/{photo}" alt="{alt}" style="width:100%; height:220px; object-fit:cover; display:block;"></div>'

    text, n2 = re.subn(r'<div\s+class="article-image"[^>]*>.*?</div>', article_repl, text, flags=re.DOTALL|re.IGNORECASE)

    # replace event header icons (i tags inside .event-header)
    def event_header_repl(m):
        global photo_idx
        header = m.group(0)
        photo = photos[photo_idx % len(photos)]
        photo_idx += 1
        alt = os.path.splitext(photo)[0].replace('-', ' ').replace('_', ' ').capitalize()
        # replace the icon <i ...></i> or keep existing img
        header = re.sub(r'<i[^>]*>.*?</i>', f'<img src="photos/{photo}" alt="{alt}" style="height:60px; width:auto; border-radius:8px;">', header, flags=re.IGNORECASE)
        header = re.sub(r'<img[^>]*>', lambda mm: mm.group(0), header, flags=re.IGNORECASE)
        return header

    text, n3 = re.subn(r'<div\s+class="event-header"[^>]*>.*?</div>', event_header_repl, text, flags=re.DOTALL|re.IGNORECASE)

    # replace responsible-card icon <i class="fas fa-user-circle"...> with img
    def responsible_repl(m):
        global photo_idx
        content = m.group(0)
        photo = photos[photo_idx % len(photos)]
        photo_idx += 1
        alt = os.path.splitext(photo)[0].replace('-', ' ').replace('_', ' ').capitalize()
        # if already has img, skip
        if 'img src' in content:
            return content
        return re.sub(r'<i[^>]*></i>', f'<img src="photos/{photo}" alt="{alt}" style="width:80px;height:80px;object-fit:cover;border-radius:50%;display:block;margin:0 auto;">', content, flags=re.IGNORECASE)

    text, n4 = re.subn(r'<div\s+class="responsible-card"[^>]*>.*?</div>', responsible_repl, text, flags=re.DOTALL|re.IGNORECASE)

    # replace small avatar placeholders like <div ...><i class="fas fa-user"></i></div>
    def small_avatar_repl(m):
        global photo_idx
        photo = photos[photo_idx % len(photos)]
        photo_idx += 1
        alt = os.path.splitext(photo)[0].replace('-', ' ').replace('_', ' ').capitalize()
        # keep outer div style, replace inner with img
        outer_open = m.group(1)
        outer_close = m.group(3)
        return f"{outer_open}<img src=\"photos/{photo}\" alt=\"{alt}\" style=\"width:150px;height:150px;object-fit:cover;display:block;\">{outer_close}"

    text, n5 = re.subn(r'(<div[^>]*>)[\s\n]*<i[^>]*class="fas fa-user"[^>]*></i>[\s\n]*(</div>)', small_avatar_repl, text, flags=re.IGNORECASE)

    if text != orig:
        p.write_text(text, encoding='utf-8')
        changed.append(str(p))
        print(f'Updated: {p} (activity:{n1} article:{n2} event:{n3} responsible:{n4} avatars:{n5})')

print('Done. Files updated:', len(changed))
for f in changed:
    print(f)
