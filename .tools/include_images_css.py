from pathlib import Path
root = Path('.')
html_files = [p for p in root.rglob('*.html') if '/backup/' not in str(p).replace('\\','/') and '.tools' not in str(p).replace('\\','/')]
link_tag = '<link href="css/images.css" rel="stylesheet">'
for p in html_files:
    text = p.read_text(encoding='utf-8')
    if 'css/images.css' in text:
        continue
    # prefer insertion after </style> if exists
    if '</style>' in text:
        text = text.replace('</style>', '</style>\n    '+link_tag)
    else:
        text = text.replace('</head>', '    '+link_tag+'\n</head>')
    p.write_text(text, encoding='utf-8')
    print('Updated:', p)
print('Done')
