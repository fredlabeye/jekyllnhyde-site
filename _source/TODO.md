# Chantier jekyllnhyde.com — état au 12 octobre 2026

## Fait
- Site WordPress reconstruit en statique (5 pages + Legal notice + 404), hébergé sur statichost.eu
- Adresse provisoire : https://jekyllnhyde.statichost.page — publication automatique à chaque push (webhook GitHub)
- Référencement technique : indexable, titres/descriptions, données structurées, sitemap, robots.txt
- Fiche Google Business mise à jour par Fred (reste : photos)

## À faire
1. **Terminer la migration**
   - ✅ 11/10/2026 : DNS basculé par Bruno (A 95.217.26.94, AAAA 2a01:4f9:c01f:8002::, www CNAME jekyllnhyde.statichost.page.) — vérifié : HTTPS OK, www et http redirigent vers https://jekyllnhyde.com/, MX et SPF intacts, pages indexables
   - ✅ 11/10/2026 : Search Console validé (via le TXT google-site-verification — ne jamais le supprimer). sitemap.xml envoyé, indexation demandée pour /, /pictures/, /videos/ (propriété Search Console : https://jekyllnhyde.com/)
   - Quand l'outil casting sera supprimé : faire retirer par Bruno le CNAME casting + TXT casting= (et backstage + TXT backstage= s'il ne sert plus). Garder google-site-verification et SPF
   - Mettre à jour les profils tiers datés (Behance, LinkedIn : « Tim & Fred… 12 years »)
   - ✅ 12/10/2026 : sauvegarde WordPress téléchargée (home directory + base MySQL) et rangée par Fred ; résiliation Bluehost lancée par Fred (fredlabeye.com n'y est pas hébergé)
   - ✅ Migration jekyllnhyde.com terminée
   - Suivi : vérifier dans Search Console que le sitemap est lu (« Dernière lecture ») et que les pages s'indexent
   - fredlabeye.com : migré le 12/10/2026 — suivi dans le dépôt fredlabeye/fredlabeye-site (_source/TODO.md)
2. **Page Studio** — photos du studio (pleine résolution), surface, hauteur, fond/cyclo, équipement, formules et tarifs (ou « on request »), location à des tiers ou non. Photos réutilisées pour la fiche Google.
3. **Mise à jour photos et vidéos** (premier chantier test du nouveau fonctionnement) — nouvelles images en pleine résolution + agence/projet ; nouvelles vidéos = lien Vimeo + agence/projet. Les photos se gèrent dans `_source/portfolio.json`.
4. **Tour des concurrents** — studios photo / production vidéo à Bruxelles : ce qu'ils montrent et que le site n'a pas. Piste déjà identifiée : version française (et néerlandaise ?) du site.
