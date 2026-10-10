# Chantier jekyllnhyde.com — état au 10 octobre 2026

## Fait
- Site WordPress reconstruit en statique (5 pages + Legal notice + 404), hébergé sur statichost.eu
- Adresse provisoire : https://jekyllnhyde.statichost.page — publication automatique à chaque push (webhook GitHub)
- Référencement technique : indexable, titres/descriptions, données structurées, sitemap, robots.txt
- Fiche Google Business mise à jour par Fred (reste : photos)

## À faire
1. **Terminer la migration**
   - Bruno modifie le DNS chez Infomaniak (A 95.217.26.94, AAAA 2a01:4f9:c01f:8002::, www CNAME jekyllnhyde.statichost.page.) — demander si ALIAS est possible pour le domaine nu
   - Domaines déjà ajoutés dans statichost
   - Vérifier : HTTPS sur les deux adresses, MX/SPF intacts, pages indexables
   - Installer Google Search Console + déclarer le sitemap
   - Garder Bluehost 1–2 semaines, puis résilier
   - Ensuite : fredlabeye.com
2. **Page Studio** — photos du studio (pleine résolution), surface, hauteur, fond/cyclo, équipement, formules et tarifs (ou « on request »), location à des tiers ou non. Photos réutilisées pour la fiche Google.
3. **Mise à jour photos et vidéos** (premier chantier test du nouveau fonctionnement) — nouvelles images en pleine résolution + agence/projet ; nouvelles vidéos = lien Vimeo + agence/projet. Les photos se gèrent dans `_source/portfolio.json`.
4. **Tour des concurrents** — studios photo / production vidéo à Bruxelles : ce qu'ils montrent et que le site n'a pas. Piste déjà identifiée : version française (et néerlandaise ?) du site.
