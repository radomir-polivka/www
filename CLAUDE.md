# radekpolivka.cz – personal web site

## Layout

```
D:\project\www\
  CLAUDE.md        this file (in the public git repo – never put secrets here)
  .gitignore       keeps info.txt, upload.ps1, __old_version\, resources\, originals\ out of the repo
  info.txt         old hosting notes incl. FTP password – never read it into a conversation, never commit it
  upload.ps1       old curl-based FTP upload script, unused
  __old_version\   old site, archived, not published
  originals\       full-size source photos (not published; web-size copies go into the article dir)
  build.py         static generator: home.html -> index.html, <name>/article.html -> <name>/index.html,
                   + 404.html; <title> from the first <h1>, footer date from the fragment's mtime;
                   GoatCounter statistics script (https://radekp.goatcounter.com)
  .github\workflows\pages.yml   on push to main, publishes www_root to GitHub Pages
  .vscode\         settings.json: build.py on save (Run on Save ext.), Live Server root = www_root;
                   tasks.json "Publish site" -> publish.ps1 (bound to Ctrl+F9 in the user keybindings)
  www_root\        the web root – published 1:1
    .htaccess      leftover from the PHP hosting, unused
    index.php      leftover from the PHP hosting (layout now lives in build.py), unused
    index.html     GENERATED from home.html; <name>/index.html GENERATED from article.html – never edit
    404.html       GENERATED
    home.html      home page fragment (list of article links; grouping lives only here)
    style.css      all formatting (light/dark, tables scroll sideways on narrow screens)
    robots.txt     allows everything
    <article>\     one directory per article: article.html (+ its images)
```

## Articles

- An article is `www_root/<name>/article.html`: a plain HTML fragment (h1–h3, p, ul/ol, img, figure,
  table, a, abbr). No `<html>`/`<head>`, no class names; all formatting is in `style.css`.
- Adding an article = new directory + `article.html` + a link in `home.html`. Nothing else changes.
- Article directories are flat (one level) on purpose: articles get regrouped often, the grouping lives
  only in `home.html`, and URLs must never change. `<name>` must match `[A-Za-z0-9-]+` (e.g. `Thorens-TP-90`), be unique and
  descriptive, and must not be renamed once published.
- Relative links/images in a fragment resolve against the article's own directory (GitHub Pages
  redirects `/name` to `/name/`). Layout links are root-absolute (`/style.css`, `/`).
- Photos: web-size copies only (GitHub Pages site limit 1 GB, repo keeps every version); no GPS EXIF.
- Language: English or Czech. Style of articles can vary, some are intended as a general resource, other are
  more presonal (first-person).
- Footer shows the contact e-mail and the fragment's modification date (set in `build.py`).

## Testing

Saving a fragment in VS Code runs `build.py` automatically; otherwise run `python build.py` after editing.
Preview locally with Live Server ("Go Live", http://127.0.0.1:5500/) or
`python -m http.server 8000 -d www_root` – opening files via file:// breaks the root-absolute links.

## Publish

Hosting: GitHub Pages, repo https://github.com/radomir-polivka/www (public), custom domain
radekpolivka.cz (DNS at Subreg/Gransy: 4 A records to GitHub, `www` CNAME, verification TXT;
`mail` CNAME and MX/SPF are for e-mail – leave them). Git is portable: `D:\app-portable\git\cmd\git.exe`
(not on PATH); push auth via Git Credential Manager (stored).

`.vscode\publish.ps1` (Ctrl+F9): build.py, `git add -A`, commit "Update <changed dirs>", push. The
workflow deploys in ~30 s. Pushing publishes – Claude runs it only when the user says so; check
`git status` first that nothing private would be committed.

The old PHP hosting (FTP, WinSCP saved site `radekpolivka.cz`) is retired; it still holds the remote-only
`download/` and `yum.log`.

## Article: Thorens-TP-90 (phono cartridges for the Thorens TP90 arm)

- Source research notes: `D:\project\gramofon\thorens\cartridge\ai\cartridge-260929.txt` (older; the article
  has newer data – the article is the current state).
- Scope: stylus ML / FL / SL / SH (no elliptical, conical, spherical), price below 750 EUR, well-known makers.
  Two tables: MM and MC. Rows grouped by maker alphabetically; notes numbered in order of appearance.
- TP90 effective mass 17 g = medium-heavy arm; target resonance 8–12 Hz.
- Resonance: f = 159 / sqrt((17 + cartridge weight + 2 g screws) × compliance@10 Hz), rounded.
- Compliance at 100 Hz (Japanese makers, Sumiko) × 1.7 = value at 10 Hz. Ortofon values taken as 10 Hz.
  Static-only (Goldring): dynamic ≈ static × 0.6, marked `*`.
- Price: lowest retail incl. VAT in DE (geizhals.de) or CZ (heureka.cz, CZK / 24.35), linked to the offers.
  "+" = replacement stylus only (VM500 body + VMN stylus rows).
- geizhals.de shows a bot check (Cloudflare) after a few quick requests – do not try to bypass it; slow down
  or use heureka.cz / shop pages / web search instead. WebFetch gets 403 on geizhals, heureka and
  audio-technica.com; the built-in browser works.
