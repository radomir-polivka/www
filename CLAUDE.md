# radekpolivka.cz – personal web site

## Layout

```
D:\project\www\
  CLAUDE.md        this file (not uploaded)
  info.txt         hosting notes incl. FTP password – never read it into a conversation, never upload it
  upload.ps1       old curl-based upload script, superseded by WinSCP (below)
  gen1\            old site, archived, not uploaded
  build.py         static generator (replaces index.php): fragment -> index.html, + 404.html
  .vscode\         settings.json: run build.py on save (Run on Save ext.), Live Server root = www_root
  www_root\        the web root – synced 1:1 to the server
    .htaccess      one rewrite rule: /name/ -> index.php?a=name (+ adds missing trailing slash)
    index.php      renders every page: wraps a fragment in header/footer, <title> from the first <h1>
    index.html     GENERATED from home.html; <name>/index.html GENERATED from article.html – never edit
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
- Relative links/images in a fragment resolve against the article's own directory (index.php redirects
  every article URL to the canonical `/name/`).
- Language: English or Czech. Style of articles can vary, some are intended as a general resource, other are
  more presonal (first-person).
- Footer shows the contact e-mail and the fragment's modification date (set in `index.php`).

## Testing

Moving from PHP hosting (15 MB quota exceeded) to static hosting (GitHub Pages planned). `build.py`
generates the static pages; saving a fragment in VS Code runs it automatically, otherwise run
`python build.py` after editing a fragment. Preview locally with Live Server ("Go Live",
http://127.0.0.1:5500/). Layout changes go into both `build.py` and `index.php` while the PHP site lives.

## Upload (sync to server)

WinSCP portable is at `D:\app-portable\winscp` (WinSCP.com was extracted there from the zip for scripting).
The site is saved in WinSCP as `radekpolivka.cz` with the password stored – never type or read the password.
The saved site has a stale local directory, hence the `option batch continue` around `open`.

1. Preview (changes nothing) and show the result to the user:
   ```
   & 'D:\app-portable\winscp\WinSCP.com' /command "option batch continue" "open radekpolivka.cz" "option batch abort" "synchronize remote -preview D:\project\www\www_root /" "exit"
   ```
2. Upload only after the user says so, without `-delete`:
   ```
   & 'D:\app-portable\winscp\WinSCP.com' /command "option batch continue" "open radekpolivka.cz" "option batch abort" "synchronize remote D:\project\www\www_root /" "exit"
   ```

The remote web root is `/`. Keep the remote-only `download/` and `yum.log` – never delete them.

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
