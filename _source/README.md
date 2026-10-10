# Source des pages

Les pages HTML du site sont générées par `build.py` à partir de `portfolio.json` (liste et légendes des photos de la page Pictures).

    python3 _source/build.py . _source/portfolio.json

Le CSS (`assets/css/site.css`) et le JS (`assets/js/site.js`) se modifient directement.
`robots.txt` et `sitemap.xml` sont écrits à la main.
