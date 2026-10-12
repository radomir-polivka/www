"""Generates the static site in www_root: wraps every HTML fragment in the common layout.
    home.html                -> index.html
    <name>/article.html      -> <name>/index.html
    (built-in)               -> 404.html
Static replacement of index.php (same layout); the <title> comes from the first <h1>, the
"updated" date from the fragment's modification time. A file is written only when its content
changes, so unchanged pages keep their mtime and stay out of git diffs.
Run without arguments; it rebuilds the whole site (a few ms per page).
"""
import datetime
import pathlib
import re
import sys

SITE_NAME = 'radekpolivka.cz'
AUTHOR = 'Radomír Polívka'
EMAIL = 'radomir.polivka@gmail.com'

ROOT = pathlib.Path(__file__).resolve().parent / 'www_root'

LAYOUT = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <meta name="author" content="{author}">
  <title>{title}</title>
  <link rel="stylesheet" href="/style.css">
</head>
<body{body_class}>
  <header><a href="/">{site}</a></header>
  <main>
{content}
  </main>
  <footer>
    <a href="/">{site}</a>
    <span><a href="mailto:{email}">{email}</a>{updated}</span>
  </footer>
  <script>
    // Links to other sites open in a new tab; the article sources stay plain HTML.
    document.querySelectorAll('a[href]').forEach(function (a) {{
      if (a.host && a.host !== location.host) {{ a.target = '_blank'; a.rel = 'noopener'; }}
    }});
  </script>
</body>
</html>
'''

NOT_FOUND = ('<h1>Not found</h1><p>There is no such page. '
             'Try the <a href="/">home page</a>.</p>')


def render(content, title=None, updated=None, home=False):
    # Images load lazily (saves mobile data); done here so the fragments stay plain.
    content = re.sub(r'<img(?![^>]*\sloading=)', '<img loading="lazy"', content, flags=re.I)
    if title is None:
        title = SITE_NAME
        m = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.I | re.S)
        if m and not home:
            title = ' '.join(re.sub(r'<[^>]+>', '', m.group(1)).split()) + ' – ' + SITE_NAME
    return LAYOUT.format(
        author=AUTHOR, site=SITE_NAME, email=EMAIL, title=title, content=content,
        body_class=' class="home"' if home else '',
        updated=f' · updated {updated}' if updated else '')


def build_page(fragment, target, home=False):
    content = fragment.read_text(encoding='utf-8')
    updated = datetime.date.fromtimestamp(fragment.stat().st_mtime).isoformat()
    return write(target, render(content, updated=updated, home=home))


def write(target, text):
    data = text.encode('utf-8')
    if target.is_file() and target.read_bytes() == data:
        return False
    target.write_bytes(data)
    return True


def main():
    changed = []
    if build_page(ROOT / 'home.html', ROOT / 'index.html', home=True):
        changed.append('index.html')
    if write(ROOT / '404.html', render(NOT_FOUND, title=f'Not found – {SITE_NAME}')):
        changed.append('404.html')
    for fragment in sorted(ROOT.glob('*/article.html')):
        name = fragment.parent.name
        if not re.fullmatch(r'[A-Za-z0-9-]+', name):
            print(f'skipped (invalid name): {name}', file=sys.stderr)
            continue
        if build_page(fragment, fragment.parent / 'index.html'):
            changed.append(f'{name}/index.html')
    print('written: ' + (', '.join(changed) if changed else 'nothing changed'))


if __name__ == '__main__':
    main()
