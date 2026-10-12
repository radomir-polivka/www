<?php
// Renders every page of the site: wraps an HTML fragment in the common layout.
//   /                          -> home.html
//   /?a=Thorens-TP-90          -> Thorens-TP-90/article.html
//   /Thorens-TP-90/            -> the same, via the rewrite rule in .htaccess
// Article pages are always redirected to the /name/ form, so relative links and images in a
// fragment resolve against the article's own directory. The <title> comes from the first <h1>.
// Fragments use plain HTML (h1-h3, p, ul, ol, img, figure, table, a).

const SITE_NAME = 'radekpolivka.cz';
const AUTHOR    = 'Radomír Polívka';
const EMAIL     = 'radomir.polivka@gmail.com';

$root = rtrim(str_replace('\\', '/', dirname($_SERVER['SCRIPT_NAME'])), '/') . '/';
$name = isset($_GET['a']) ? $_GET['a'] : '';

if ($name === '') {
    $fragment = __DIR__ . '/home.html';
} elseif (preg_match('~^[A-Za-z0-9-]+$~', $name) && is_file(__DIR__ . "/$name/article.html")) {
    $fragment = __DIR__ . "/$name/article.html";
    if (parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH) !== "$root$name/") {
        header("Location: $root$name/", true, 301);
        exit;
    }
} else {
    $fragment = null;
}

if ($fragment) {
    $content = file_get_contents($fragment);
    $updated = date('Y-m-d', filemtime($fragment));
} else {
    http_response_code(404);
    $content = '<h1>Not found</h1><p>There is no such page. Try the <a href="' . $root . '">home page</a>.</p>';
    $updated = null;
}

// Images load lazily (saves mobile data); done here so the fragments stay plain.
$content = preg_replace('~<img(?![^>]*\sloading=)~i', '<img loading="lazy"', $content);

$title = SITE_NAME;
if ($name !== '' && preg_match('~<h1[^>]*>(.*?)</h1>~is', $content, $m)) {
    $title = trim(preg_replace('~\s+~', ' ', strip_tags($m[1]))) . ' – ' . SITE_NAME;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <meta name="author" content="<?= AUTHOR ?>">
  <title><?= $title ?></title>
  <link rel="stylesheet" href="<?= $root ?>style.css">
</head>
<body<?= $name === '' ? ' class="home"' : '' ?>>
  <header><a href="<?= $root ?>"><?= SITE_NAME ?></a></header>
  <main>
<?= $content ?>
  </main>
  <footer>
    <a href="mailto:<?= EMAIL ?>"><?= EMAIL ?></a><?php if ($updated): ?> · updated <?= $updated ?><?php endif ?>
  </footer>
  <script>
    // Links to other sites open in a new tab; the article sources stay plain HTML.
    document.querySelectorAll('a[href]').forEach(function (a) {
      if (a.host && a.host !== location.host) { a.target = '_blank'; a.rel = 'noopener'; }
    });
  </script>
</body>
</html>
