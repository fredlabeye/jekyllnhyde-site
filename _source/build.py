#!/usr/bin/env python3
"""Génère les pages HTML statiques du site Jekyll N' Hyde."""
import json, sys, html, os

R = sys.argv[1]
META = json.load(open(sys.argv[2], encoding="utf8"))
SITE = "https://jekyllnhyde.com"
V = "4"  # version des assets (cache)

ICONS = {
    "mail": '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M2 5h20v14H2V5zm2 2v.5l8 5 8-5V7H4zm16 2.8-8 5-8-5V17h16V9.8z"/></svg>',
    "instagram": '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.8.1 3.3.1 4.8 1.7 4.9 4.9.1 1.3.1 1.6.1 4.8s0 3.6-.1 4.8c-.1 3.2-1.7 4.8-4.9 4.9-1.3.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-3.3-.1-4.8-1.7-4.9-4.9C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.8C2.4 3.9 3.9 2.4 7.2 2.3 8.4 2.2 8.8 2.2 12 2.2zM12 0C8.7 0 8.3 0 7.1.1 2.7.3.3 2.7.1 7.1 0 8.3 0 8.7 0 12s0 3.7.1 4.9c.2 4.4 2.6 6.8 7 7 1.2.1 1.6.1 4.9.1s3.7 0 4.9-.1c4.4-.2 6.8-2.6 7-7 .1-1.2.1-1.6.1-4.9s0-3.7-.1-4.9c-.2-4.4-2.6-6.8-7-7C15.7 0 15.3 0 12 0zm0 5.8a6.2 6.2 0 1 0 0 12.4 6.2 6.2 0 0 0 0-12.4zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.4-11.8a1.4 1.4 0 1 0 0 2.9 1.4 1.4 0 0 0 0-2.9z"/></svg>',
    "facebook": '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 8H6v4h3v12h5V12h3.6l.4-4h-4V6.3c0-1 .2-1.3 1.1-1.3H18V0h-3.8C10.6 0 9 1.6 9 4.6V8z"/></svg>',
    "vimeo": '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M22.4 6.9c-.1 2.1-1.6 5-4.4 8.7-2.9 3.8-5.3 5.7-7.3 5.7-1.2 0-2.3-1.1-3.1-3.4L6 11.7C5.4 9.4 4.8 8.3 4.1 8.3c-.1 0-.7.3-1.6 1L1.5 8c1-.9 2-1.8 3-2.7 1.4-1.2 2.4-1.8 3-1.9 1.6-.2 2.6.9 3 3.3.4 2.6.7 4.2.9 4.8.5 2.1 1 3.2 1.5 3.2.4 0 1.1-.7 1.9-2 .9-1.4 1.3-2.4 1.4-3.1.1-1.2-.3-1.8-1.4-1.8-.5 0-1 .1-1.5.3 1-3.3 3-4.9 5.9-4.8 2.1.1 3.1 1.4 3 4z"/></svg>',
}
SOCIAL = [
    ("instagram", "Instagram", "https://www.instagram.com/jekyllnhydestudio/"),
    ("facebook", "Facebook", "https://www.facebook.com/everythingartificial"),
    ("vimeo", "Vimeo", "https://vimeo.com/jekyllnhyde"),
]
NAV = [("", "Home"), ("showreel/", "Showreel"), ("pictures/", "Pictures"), ("videos/", "Videos"), ("contact/", "Contact")]

ORG = {
    "@context": "https://schema.org",
    "@type": "ProfessionalService",
    "@id": SITE + "/#org",
    "name": "Jekyll N' Hyde",
    "alternateName": "Jekyll N Hyde",
    "description": "Boutique creative studio in Brussels producing photography and films for agencies, brands, artists, rock bands and TV shows.",
    "url": SITE + "/",
    "logo": SITE + "/apple-touch-icon.png",
    "image": SITE + "/assets/img/og-image.jpg",
    "email": "info@jekyllnhyde.com",
    "telephone": "+32478760289",
    "address": {"@type": "PostalAddress", "streetAddress": "Rue des Glands 70", "postalCode": "1190",
                "addressLocality": "Bruxelles", "addressRegion": "Brussels-Capital", "addressCountry": "BE"},
    "areaServed": "Europe",
    "knowsAbout": ["Advertising photography", "Commercial film production", "Post-production", "Photo retouching"],
    "sameAs": [s[2] for s in SOCIAL],
}


def esc(s):
    return html.escape(s, quote=True)


def social(cls):
    return "".join(f'<a href="{u}" rel="noopener" target="_blank" aria-label="{n}">{ICONS[k]}</a>' for k, n, u in SOCIAL)


def page(path, title, desc, body, extra_ld=None, cls="", lightbox=False, og_img="/assets/img/og-image.jpg"):
    depth = path.count("/")
    pre = "/" if path.endswith(".html") else "../" * depth
    canonical = SITE + "/" + ("" if path.endswith(".html") else path)
    nav = "".join(
        f'<a href="{pre}{p}"{" aria-current=\"page\"" if p == path else ""}>{n}</a>' for p, n in NAV)
    ld = [ORG] + (extra_ld or [])
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    lb = ('<div class="lightbox" role="dialog" aria-modal="true" aria-label="Visionneuse">'
          '<button class="lb-btn lb-close" aria-label="Fermer">&times;</button>'
          '<button class="lb-btn lb-prev" aria-label="Précédent">&#8249;</button>'
          '<button class="lb-btn lb-next" aria-label="Suivant">&#8250;</button>'
          '<div class="lb-stage"></div><div class="lb-cap"></div></div>') if lightbox else ""
    out = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Jekyll N' Hyde">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}{og_img}">
<meta property="og:locale" content="en_GB">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="32x32" href="{pre}favicon-32.png">
<link rel="apple-touch-icon" href="{pre}apple-touch-icon.png">
<link rel="preload" href="{pre}assets/fonts/montserrat-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{pre}assets/css/site.css?v={V}">
{ld_html}
</head>
<body class="{cls}">
<div class="topbar"><div class="wrap">
<div class="topbar-left"><span>Let’s talk</span><a href="mailto:info@jekyllnhyde.com">{ICONS["mail"]}info@jekyllnhyde.com</a></div>
<div class="topbar-right">{social("top")}</div>
</div></div>
<header class="header"><div class="wrap">
<a class="logo" href="{pre}" aria-label="Jekyll N' Hyde – home"><img src="{pre}assets/img/logo.svg" width="70" height="60" alt="Jekyll N' Hyde"></a>
<nav class="nav" id="nav" aria-label="Main">{nav}</nav>
<button class="burger" aria-label="Menu" aria-controls="nav" aria-expanded="false"><span></span></button>
</div></header>
<main>
{body}
</main>
<footer class="footer"><div class="wrap">
<address>★ Rue des Glands 70 • 1190 Bruxelles • Belgium • <a href="tel:+32478760289">+32 (0) 478 76 02 89</a> • <a href="mailto:info@jekyllnhyde.com">info@jekyllnhyde.com</a></address>
<div class="footer-right"><a class="footer-legal" href="{pre}legal-notice/">Legal notice</a><div class="footer-social">{social("foot")}</div></div>
</div></footer>
{lb}
<script src="{pre}assets/js/site.js?v={V}" defer></script>
</body>
</html>
'''
    if path.endswith(".html"):
        fp = os.path.join(R, path)
    else:
        os.makedirs(os.path.join(R, path), exist_ok=True)
        fp = os.path.join(R, path, "index.html")
    open(fp, "w", encoding="utf8").write(out)


def more(pre, a, b):
    return (f'<section class="more wrap"><h2>I want to see more</h2><div class="more-links">'
            f'<a href="{pre}{a[0]}">{a[1]}</a><p class="star" aria-hidden="true">★</p><a href="{pre}{b[0]}">{b[1]}</a></div></section>')


# ---------------- Accueil ----------------
home = '''<section class="home-hero wrap">
<a class="hero-media" href="showreel/" aria-label="Watch our showreel">
<img src="assets/img/hero.webp" width="600" height="500" fetchpriority="high" alt="Jekyll N' Hyde logo animated with our photography">
</a>
<h1 class="home-title">Jekyll N’ Hyde is a boutique creative studio. We produce photography and films for agencies, brands, <span class="typed" data-words="artists.|rock bands.|TV shows.">artists.</span><span class="sr-only"> rock bands, TV shows.</span></h1>
</section>
<div class="star-sep"><p class="star" aria-hidden="true">★</p></div>
<p class="home-tagline wrap">Our passion is crafting captivating and authentic visuals and films that tell your story.</p>'''
page("", "Jekyll N' Hyde | Photography & film production studio in Brussels",
     "Jekyll N' Hyde is a boutique creative studio in Brussels. We produce advertising photography, commercial films and post-production for agencies, brands, artists and TV shows.",
     home, cls="home")

# ---------------- Showreel ----------------
bs_files = ['01', '03', '04', '06', '10', '14', '15', '18', '20', '21', '22', '23', '24', '25', '26']
backstage = "".join(
    f'<img src="../assets/img/backstage/backstage-{n}.webp" width="700" height="466" loading="lazy" alt="Behind the scenes of a Jekyll N\' Hyde shoot">'
    for n in bs_files)
showreel = f'''<h1 class="sr-only">Jekyll N' Hyde showreel – photography, film and post-production</h1>
<section class="wrap">
<div class="player" data-vimeo="935913014" data-title="Jekyll N' Hyde showreel">
<img src="../assets/img/showreel-poster.webp" width="1280" height="720" alt="Jekyll N' Hyde showreel" fetchpriority="high">
<button class="player-btn" aria-label="Play the showreel"><span class="play"></span></button>
</div>
<div class="services">
<div><h2>Photography</h2><p>With years of expertise in photo retouching, moving into photography was a natural progression for us. From small projects to managing national and international campaigns, we collaborate closely with advertising agencies, creatives and more. No project is too small or too big for us. Teamwork is at the heart of everything we do, and we are just as enthusiastic about creating stunning product shots in our studio as we are about orchestrating grand outdoor shoots.</p></div>
<div><h2>Film</h2><p>Driven by strong client demand, we made film our next step. Our extensive experience in photographic production and lighting gave us the confidence to dive into the world of filmmaking. We primarily craft compelling commercials, and also venture into music videos and fiction. Telling beautiful stories with stunning visuals is a daily joy for us.</p></div>
<div><h2>Post-production</h2><p>Post-production is our foundation. Over the years, our strength has been our ability to seamlessly blend photo and video production, and we are equally confident in both. It is the crucial step that elevates a good project into a breathtaking final product. This phase allows us to explore new creative possibilities and refine our vision. Ultimately, it’s where the magic happens, adding that special touch to every project.</p></div>
</div>
</section>
<div class="backstage" aria-label="Behind the scenes"><div class="backstage-track">{backstage}</div></div>
{more("../", ("pictures/", "Pictures"), ("videos/", "Videos"))}'''
page("showreel/", "Showreel | Jekyll N' Hyde – photography, film & post-production",
     "Watch the Jekyll N' Hyde showreel: advertising photography, commercial films, music videos and post-production made in Brussels for agencies and brands.",
     showreel)

# ---------------- Pictures ----------------
cells, blocks = [], []
for i, m in enumerate(META):
    t, c = m["t"], m["c"]
    alt = f"{t} – {c}, advertising photography by Jekyll N' Hyde" if c else f"{t}, photography by Jekyll N' Hyde"
    capt = f'<span class="a">{esc(t)}</span><span class="s">★</span>' + (f'<span class="p">{esc(c)}</span>' if c else "")
    lazy = ' loading="lazy"' if i >= 6 else (' fetchpriority="high"' if i < 3 else "")
    cells.append(
        f'<a href="../assets/img/work/full/{m["s"]}.webp"><figure style="margin:0">'
        f'<img src="../assets/img/work/{m["s"]}-800.webp" srcset="../assets/img/work/{m["s"]}-480.webp 480w, ../assets/img/work/{m["s"]}-800.webp 800w" '
        f'sizes="(max-width:767px) 100vw, 33vw" width="800" height="580"{lazy} decoding="async" alt="{esc(alt)}">'
        f'<figcaption>{capt}</figcaption></figure></a>')
for k in range(0, len(cells), 9):
    blocks.append('<div class="gallery">' + "".join(cells[k:k + 9]) + "</div>")
pictures = ('<h1 class="sr-only">Advertising photography portfolio – Jekyll N\' Hyde, Brussels</h1><section class="wrap">'
            + '<div class="star-sep"><p class="star" aria-hidden="true">★</p></div>'.join(blocks)
            + "</section>" + more("../", ("showreel/", "Showreel"), ("videos/", "Videos")))
gallery_ld = {"@context": "https://schema.org", "@type": "ImageGallery", "name": "Jekyll N' Hyde – photography portfolio",
              "url": SITE + "/pictures/", "author": {"@id": SITE + "/#org"}}
page("pictures/", "Pictures | Advertising photography portfolio – Jekyll N' Hyde",
     "Advertising photography portfolio of Jekyll N' Hyde, Brussels: campaigns for BMW, Hoegaarden, Orange, Walibi, Crelan, Renault, Lidl, Pepsi and more.",
     pictures, extra_ld=[gallery_ld], lightbox=True)

# ---------------- Videos ----------------
VIDS = [("1046795435", "trema", "Just Let Minot", "TreM.a Museum"),
        ("953077558", "jupiler", "BBDO", "Jupiler crashed glass"),
        ("953067755", "commetogether", "RBFA", "Come together"),
        ("953069338", "fairebel", "Shake", "Fairebel"),
        ("672671663", "bruxellesmobilite", "Mortier Brigade", "Bruxelles Mobilité"),
        ("953082221", "yongo", "Shake", "Yongo"),
        ("665645134", "citejardin", "Visit.Brussels", "Cités jardin")]
cards = "".join(
    f'<article class="video-card"><button data-lb-vimeo="{vid}" aria-label="Play {esc(a)} – {esc(b)}">'
    f'<img src="../assets/img/videos/{img}.webp" width="800" height="450" loading="lazy" alt="{esc(a)} – {esc(b)}, film by Jekyll N\' Hyde"><span class="play"></span></button>'
    f'<h3>{esc(a)}</h3><p>{esc(b)}</p></article>' for vid, img, a, b in VIDS)
videos = (f'<h1 class="sr-only">Commercial films and videos – Jekyll N\' Hyde, Brussels</h1><section class="wrap"><div class="video-grid">{cards}</div>'
          f'<a class="vimeo-more" href="https://vimeo.com/jekyllnhyde" rel="noopener" target="_blank">Watch more on <img src="../assets/img/vimeo-logo.svg" alt="Vimeo" width="100" height="30"></a></section>')
page("videos/", "Videos | Commercial films – Jekyll N' Hyde",
     "Commercial films by Jekyll N' Hyde, Brussels: Jupiler, RBFA, Fairebel, Visit.Brussels, Bruxelles Mobilité, TreM.a Museum and more.",
     videos, lightbox=True)

# ---------------- Contact ----------------
contact = '''<section class="wrap contact">
<div class="contact-map"><img src="../assets/img/carte-europe.webp" width="450" height="500" alt="Map of Europe showing Jekyll N' Hyde in Brussels, Belgium"></div>
<div>
<h1>Let's shoot together</h1>
<hr>
<p>We are located in Brussels, Belgium.<br>We love to visit new villages, cities, countries and continents!</p>
<hr>
<p>Rue des Glands 70<br>1190 Bruxelles<br>Belgium</p>
<hr>
<p>Fred: <a href="tel:+32478760289">+32 478 76 02 89</a><br><a href="mailto:info@jekyllnhyde.com">info@jekyllnhyde.com</a></p>
</div>
</section>'''
page("contact/", "Contact | Jekyll N' Hyde – Brussels photography & film studio",
     "Contact Jekyll N' Hyde, photography and film production studio, Rue des Glands 70, 1190 Brussels (Forest), Belgium. +32 478 76 02 89 – info@jekyllnhyde.com",
     contact)


# ---------------- Mentions légales ----------------
legal = """<section class="wrap legal">
<h1>Legal notice</h1>
<h2>Publisher</h2>
<p>Jekyll N'Hyde SRL<br>Registered office: Rue des Glands 70, 1190 Forest, Belgium<br>Company number: 0894.334.159 – RPM Bruxelles<br>VAT: BE 0894.334.159<br>Email: <a href="mailto:info@jekyllnhyde.com">info@jekyllnhyde.com</a> – Phone: <a href="tel:+32478760289">+32 478 76 02 89</a><br>Website: jekyllnhyde.com</p>
<h2>Hosting</h2>
<p>This website is hosted in the European Union by statichost.eu (Sweden), on servers located in Europe.</p>
<h2>Copyright and image rights</h2>
<p>All content on this website – photographs, films, videos, texts, logos and graphic elements – is protected by copyright and related rights, in particular under Book XI of the Belgian Code of Economic Law. It is the property of Jekyll N'Hyde or of its clients and partners, and is shown here for portfolio purposes only.</p>
<p>None of this content is royalty-free. Any reproduction, representation, adaptation, distribution or use, in whole or in part, by any means and on any medium, is strictly prohibited without the prior written consent of Jekyll N'Hyde. Requests can be sent to <a href="mailto:info@jekyllnhyde.com">info@jekyllnhyde.com</a>.</p>
<p>Brands, logos and product names shown in the portfolio belong to their respective owners. Their presence on this website illustrates work carried out for or with these clients and does not imply any other affiliation.</p>
<h2>Privacy and cookies</h2>
<p>This website does not use cookies, analytics or tracking tools, and does not collect any personal data. Videos are hosted on Vimeo: the Vimeo player is only loaded when you choose to play a video, at which point Vimeo’s own privacy policy applies. If you contact us by email or phone, your details are used only to answer your request.</p>
<h2>Liability</h2>
<p>Jekyll N'Hyde takes care to keep the information on this website accurate and up to date, but cannot guarantee that it is complete or free of errors. Links to external websites are provided for convenience; Jekyll N'Hyde is not responsible for their content.</p>
<p class="legal-date">Last updated: October 2026</p>
</section>"""
page("legal-notice/", "Legal notice | Jekyll N' Hyde",
     "Legal notice of Jekyll N'Hyde SRL, Brussels: company details, copyright and image rights, privacy.",
     legal)

# ---------------- 404 ----------------
nf = '<section class="wrap notfound"><h1>Page not found</h1><p>This page doesn’t exist anymore. <a href="/">Back to the homepage</a>.</p></section>'
page("404.html", "Page not found | Jekyll N' Hyde", "This page could not be found.", nf)
print("built")
