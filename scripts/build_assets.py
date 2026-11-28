#!/usr/bin/env python3
"""Builds the static farm-themed SVG assets into ../assets.

    python3 scripts/build_assets.py

Edit the CONFIG block below (name, tagline, projects, tags, tech lists), re-run,
commit the regenerated SVGs.  The live "crop yield" graph is built separately by
scripts/update_yield.py (run by the GitHub Action).
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from farmlib import (P, f, svg_doc, text, text_width, fit_size, cap_height, catmull, y_at, hill_path,  # noqa: E402
                     wheat, tuft, sprout, icon_path, rng, ico_barn, ico_sunflower, ico_sprout_big,
                     ico_wheat_bundle, ico_idcard, ico_pitchfork, ico_rosette, ico_scroll, ico_mailbox,
                     ico_pots, ico_tractor, ico_wheelbarrow, ico_shark, windmill, ICONS)
from farm_animals import ANIMAL_CSS, animal  # noqa: E402

ROOT =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")

# =============================================================== CONFIG ======
HANDLE = "MONISHRAJAX"
TAGLINE = "FULL-STACK  ·  APPLIED AI  ·  CLOUD"

# number, title, subtitle, accent, icon fn, file, animals perched on top of the sign: (kind, x, scale, mirrored)
SECTIONS = [
    ("01", "FARMER'S DOSSIER", "WHO RUNS THIS FARM", "lime", ico_idcard, "sec-01-dossier",
     [("rooster", 660, .5, False)]),
    ("02", "EXPERIENCE & LEADERSHIP", "FIELD WORK // THE WORK LOG", "gold", ico_wheelbarrow, "sec-02-experience",
     [("cow", 640, .46, False)]),
    ("03", "PROJECTS", "THE FIELDS // WHAT'S GROWING", "lime", ico_pots, "sec-03-projects",
     [("hen", 600, .62, False), ("chick", 640, .9, True)]),
    ("04", "TECH ARSENAL", "THE TOOLSHED // TOOLS OF THE TRADE", "orange", ico_pitchfork, "sec-04-arsenal",
     [("sheep", 680, .55, True)]),
    ("05", "ACHIEVEMENTS", "COUNTY FAIR RIBBONS", "gold", ico_rosette, "sec-05-achievements",
     [("duck", 700, .7, False)]),
    ("06", "CERTIFICATIONS", "SEED CERTIFICATES", "sky", ico_scroll, "sec-06-certifications",
     [("hen-brown", 640, .62, True), ("chick", 604, .9, False)]),
    ("07", "SYSTEM METRICS", "CROP YIELD // LIVE FROM THE FIELD", "lime", ico_wheat_bundle, "sec-07-metrics",
     [("pig", 660, .52, False)]),
    ("08", "ESTABLISH CONNECTION", "VISIT THE FARM // SEND A MESSAGE", "gold", ico_mailbox, "sec-08-connect",
     [("dog", 680, .6, False)]),
]

ACCENT = {"lime": P["g4"], "gold": P["gold"], "orange": P["orange"], "sky": P["sky"], "red": "#ff7a59"}

TAGS = [  # file, label, accent
    ("tag-professional", "PROFESSIONAL", "lime"),
    ("tag-leadership", "LEADERSHIP", "gold"),
    ("tag-education", "EDUCATION", "sky"),
    ("tag-featured", "FEATURED FIELDS", "lime"),
    ("tag-barn", "THE BARN // ALL REPOSITORIES", "orange"),
    ("tag-stack", "ON THE FIELD", "gold"),
    # date tags for the professional roles in section 02
    ("tag-date-normalize", "JUL 2026 — PRESENT · FULL-TIME", "lime"),
    ("tag-date-stitch", "JUN — JUL 2026 · INTERNSHIP", "gold"),
    ("tag-date-codsoft", "NOV — DEC 2024 · REMOTE INTERNSHIP", "sky"),
    ("tag-hackathons", "HACKATHON RESULTS", "gold"),
]

PROJECTS = [
    dict(file="project-01-normalize", num="01", name="NORMALIZE",
         tagline="STOREFRONT FOR A SINGLE-PRODUCT LAUNCH", badge="LIVE · 2026",
         stack=[("react", "REACT"), ("vite", "VITE"), ("tailwindcss", "TAILWIND"), ("express", "EXPRESS"), ("supabase", "SUPABASE")]),
    dict(file="project-02-floor", num="02", name="DON'T TOUCH THE FLOOR",
         tagline="PRISON-BREAK ARCADE PLATFORMER // MULTIPLAYER", badge="LIVE · 2026",
         stack=[("html5", "CANVAS"), ("javascript", "JAVASCRIPT"), ("css3", "CSS3"), ("vercel", "VERCEL")]),
    dict(file="project-03-visaguard", num="03", name="VISAGUARD",
         tagline="AGENTIC-AI PCI / PII COMPLIANCE PLATFORM", badge="LIVE · 2026",
         stack=[("nextdotjs", "NEXT.JS"), ("typescript", "TYPESCRIPT"), ("tailwindcss", "TAILWIND"), ("framer", "FRAMER"), ("vercel", "VERCEL")]),
    dict(file="project-04-resume", num="04", name="SMART RESUME MATCHER",
         tagline="TF-IDF + COSINE SIMILARITY RETRIEVAL SYSTEM", badge="SOURCE · 2026",
         stack=[("python", "PYTHON"), ("flask", "FLASK"), ("react", "REACT"), ("typescript", "TYPESCRIPT"), ("scikitlearn", "SCIKIT-LEARN")]),
    dict(file="project-05-idscanner", num="05", name="ID SCANNER",
         tagline="OCR ATTENDANCE SYSTEM FOR STUDENT IDS", badge="SOURCE · 2025",
         stack=[("react", "REACT"), ("vite", "VITE"), ("supabase", "SUPABASE"), ("javascript", "TESSERACT.JS")]),
    dict(file="project-06-cicd", num="06", name="MICROSERVICES CI/CD",
         tagline="COMMIT > BUILD > CONTAINER > CLUSTER", badge="SOURCE · 2026",
         stack=[("githubactions", "ACTIONS"), ("docker", "DOCKER"), ("kubernetes", "KUBERNETES"), ("nodedotjs", "NODE.JS")]),
]

# award cards for section 05 (original artwork; GitHub's own badge images are not reused)
# art: which medallion scene to draw, see ACHIEVEMENT_ART ("shark" | "pair")
ACHIEVEMENTS = [
    dict(file="achievement-pull-shark", art="shark", title="PULL SHARK", tagline="OPENED PULL REQUESTS THAT GOT MERGED", badge="EARNED",
         chips=[("github", "GITHUB ACHIEVEMENT"), (None, "MERGED PULL REQUESTS")]),
    dict(file="achievement-pair-extraordinaire", art="pair", title="PAIR EXTRAORDINAIRE", tagline="CO-AUTHORED COMMITS ON MERGED PULL REQUESTS", badge="EARNED",
         chips=[("github", "GITHUB ACHIEVEMENT"), (None, "CO-AUTHORED COMMITS")]),
]

# certificate cards for section 06 (the README links each card to its PDF in certificates/)
CERTIFICATES = [
    dict(file="cert-blockchain", title="BLOCKCHAIN DEVELOPER TRAINING", tagline="CERTIFICATE OF COMPLETION // SIMPLILEARN SKILLUP",
         badge="COMPLETED", chips=["ISSUED BY SIMPLILEARN", "20 OCT 2026", "CODE 10916987"]),
]

# a small animal on each project's soil tile: file -> (kind, scale)
PROJECT_PETS = {
    "project-01-normalize": ("chick", .95),
    "project-02-floor": ("sheep", .55),
    "project-03-visaguard": ("cow", .42),
    "project-04-resume": ("pig", .5),
    "project-05-idscanner": ("hen", .62),
    "project-06-cicd": ("duck", .7),
}

TECH_ROW_1 = [("javascript", "JAVASCRIPT"), ("typescript", "TYPESCRIPT"), ("python", "PYTHON"), ("html5", "HTML5"),
              ("css3", "CSS3"), ("react", "REACT"), ("nextdotjs", "NEXT.JS"), ("tailwindcss", "TAILWIND"),
              ("vite", "VITE"), ("framer", "FRAMER")]
TECH_ROW_2 = [("nodedotjs", "NODE.JS"), ("express", "EXPRESS"), ("flask", "FLASK"), ("supabase", "SUPABASE"),
              ("postgresql", "POSTGRES"), ("scikitlearn", "SCIKIT-LEARN"), ("docker", "DOCKER"),
              ("kubernetes", "KUBERNETES"), ("githubactions", "ACTIONS"), ("vercel", "VERCEL"),
              ("git", "GIT"), ("github", "GITHUB")]

BADGES = [  # file, label, accent, icon (simple-icons slug | custom kind)
    ("badge-github", "GITHUB", "lime", "github"),
    ("badge-linkedin", "LINKEDIN", "sky", "linkedin"),
    ("badge-portfolio", "PORTFOLIO", "gold", "sunflower"),
    ("badge-email", "EMAIL", "orange", "mail"),
]
# =============================================================================


def write(name, content):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8") as fh:
        fh.write(content)
    print("  %-26s %5.1f KB" % (name + ".svg", len(content.encode("utf-8")) / 1024.0))


# ================================================================== HERO =====
def hero():
    W, H = 1000, 440
    r = rng(11)
    defs = [
        '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#020b06"/><stop offset=".36" stop-color="#05170c"/>'
        '<stop offset=".64" stop-color="#0c3d20"/><stop offset=".84" stop-color="#1f7037"/><stop offset="1" stop-color="#2f9447"/></linearGradient>',
        '<radialGradient id="sunf"><stop offset="0" stop-color="#fff4bf"/><stop offset=".55" stop-color="#ffd45a"/><stop offset="1" stop-color="#f0a21a"/></radialGradient>',
        '<radialGradient id="halo"><stop offset="0" stop-color="#ffd45a" stop-opacity=".62"/><stop offset=".4" stop-color="#ffb938" stop-opacity=".18"/>'
        '<stop offset="1" stop-color="#ffb938" stop-opacity="0"/></radialGradient>',
        '<linearGradient id="fieldN" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1d8140"/><stop offset="1" stop-color="#0c4420"/></linearGradient>',
        '<linearGradient id="fieldM" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#16702f"/><stop offset="1" stop-color="#0d4a22"/></linearGradient>',
        '<linearGradient id="wood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8f5e30"/><stop offset=".5" stop-color="#6b4423"/><stop offset="1" stop-color="#53341a"/></linearGradient>',
        '<linearGradient id="fence" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a06c38"/><stop offset="1" stop-color="#5a3a1e"/></linearGradient>',
        '<radialGradient id="vig" cx=".5" cy=".5" r=".78"><stop offset=".62" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".5"/></radialGradient>',
    ]
    css = (
        ".ff{animation:ff 7s ease-in-out infinite}"
        "@keyframes ff{0%{transform:translate(0,0);opacity:0}15%{opacity:1}50%{transform:translate(16px,-20px);opacity:.85}85%{opacity:1}100%{transform:translate(-10px,-38px);opacity:0}}"
        ".cl{animation:cl 100s linear infinite}"
        "@keyframes cl{from{transform:translateX(-320px)}to{transform:translateX(1320px)}}"
        ".drive{animation:drive 28s linear infinite}"
        "@keyframes drive{from{transform:translateX(-250px)}to{transform:translateX(1180px)}}"
        ".swing{animation:swing 7s ease-in-out infinite}"
        "@keyframes swing{0%,100%{transform:rotate(-1.1deg)}50%{transform:rotate(1.1deg)}}"
        ".bird{animation:bird 44s linear infinite}"
        "@keyframes bird{from{transform:translateX(-90px)}to{transform:translateX(1120px)}}"
    ) + ANIMAL_CSS
    b = ['<rect width="%d" height="%d" fill="url(#sky)"/>' % (W, H)]

    # stars
    for i in range(48):
        x, y, rad = r.uniform(8, 992), r.uniform(6, 215), r.choice([.7, .9, 1.1, 1.4])
        attr = ''
        if i % 3 == 0:
            attr = ' class="tw" style="animation-delay:%ss;animation-duration:%ss"' % (f(-r.uniform(0, 4)), f(r.uniform(2.2, 4.6)))
        b.append('<circle cx="%s" cy="%s" r="%s" fill="#fff3d6" opacity="%s"%s/>' % (f(x), f(y), rad, f(r.uniform(.35, .9)), attr))

    # sun, halo, rays
    sx, sy = 662, 282
    b.append('<circle cx="%d" cy="%d" r="240" fill="url(#halo)"/>' % (sx, sy))
    rays = ""
    for k in range(18):
        a, d = math.radians(k * 20), math.radians(3.0)
        rays += '<path d="M%d %dL%s %sL%s %sZ"/>' % (
            sx, sy, f(sx + 540 * math.cos(a - d)), f(sy + 540 * math.sin(a - d)),
            f(sx + 540 * math.cos(a + d)), f(sy + 540 * math.sin(a + d)))
    b.append('<g fill="#ffd45a" opacity=".08"><g class="spin" style="transform-origin:%dpx %dpx;animation-duration:150s">%s</g></g>' % (sx, sy, rays))
    b.append('<circle cx="%d" cy="%d" r="54" fill="url(#sunf)"/>' % (sx, sy))

    # clouds + birds
    def cloud(cy, s, op, dur, delay):
        shapes = ('<ellipse rx="62" ry="15"/><ellipse cx="-28" cy="-12" rx="30" ry="17"/>'
                  '<ellipse cx="14" cy="-18" rx="34" ry="21"/><ellipse cx="42" cy="-6" rx="24" ry="13"/>')
        return ('<g class="cl" style="animation-duration:%ss;animation-delay:%ss"><g transform="translate(0 %d) scale(%s)" fill="#2f7a4b" opacity="%s">%s</g></g>'
                % (dur, -delay, cy, s, op, shapes))
    b.append(cloud(86, 1.0, .34, 110, 20))
    b.append(cloud(196, 1.35, .28, 140, 85))
    b.append(cloud(150, .8, .3, 95, 52))
    flock = "".join('<path transform="translate(%d %d)" d="M0 0Q6 -7 12 0Q18 -7 24 0" fill="none" stroke="#9cc7a0" stroke-width="1.8" stroke-linecap="round"/>' % (dx, dy)
                    for dx, dy in [(0, 0), (30, 10), (-26, 14)])
    b.append('<g class="bird" opacity=".7" style="animation-delay:-18s"><g transform="translate(0 214)">%s</g></g>' % flock)

    # far hills + treeline
    far = catmull([(0, 292), (110, 270), (240, 262), (380, 280), (520, 268), (650, 290), (790, 262), (900, 276), (1000, 264)], 10)
    b.append('<path d="%s" fill="#0d4222"/>' % hill_path(far, W, H))
    for x in range(-6, 1012, 13):
        yy = y_at(far, min(max(x, 0), 1000)) + r.uniform(0, 4)
        b.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (
            f(x + r.uniform(-3, 3)), f(yy), f(r.uniform(5.5, 10)), r.choice(["#0a3318", "#0b381b", "#093016"])))

    # silo, barn, windmill
    b.append('<g transform="translate(806 5)"><rect x="-13" y="228" width="26" height="78" fill="#8fb39a"/>'
             '<rect x="-13" y="228" width="9" height="78" fill="#6f947c" opacity=".55"/><path d="M-14 228Q0 206 14 228Z" fill="#5d7f68"/>'
             '<path d="M-13 246H13M-13 264H13M-13 282H13" stroke="#5d7f68" stroke-width="2"/></g>')
    b.append('<g transform="translate(880 267) scale(1.95)">%s</g>' % ico_barn())
    b.append('<g transform="translate(0 5)"><path d="M880 216V203M872 207H888" stroke="#dfe8dc" stroke-width="1.6" stroke-linecap="round"/><path d="M888 207L894 204.5V209.5Z" fill="#dfe8dc"/></g>')
    b.append(windmill(80, 304))

    # mid hills with crop rows
    mid = catmull([(0, 326), (120, 310), (300, 322), (480, 308), (640, 320), (800, 306), (1000, 318)], 10)
    defs.append('<clipPath id="cm"><path d="%s"/></clipPath>' % hill_path(mid, W, H))
    b.append('<path d="%s" fill="url(#fieldM)"/>' % hill_path(mid, W, H))
    rows = "".join('<path d="M470 262L%d 440"/>' % xb for xb in range(-900, 1900, 54))
    rows2 = "".join('<path d="M470 262L%d 440"/>' % (xb + 27) for xb in range(-900, 1900, 54))
    b.append('<g clip-path="url(#cm)"><g stroke="#0a3d1c" stroke-width="1.8" opacity=".9">%s</g>'
             '<g stroke="#2a8f48" stroke-width="1" opacity=".32">%s</g></g>' % (rows, rows2))

    # pasture on the far hill: a few sheep and cows grazing (kept sparse so the scene stays calm)
    for kind, x, s, flip, d in [("sheep", 232, .46, False, .4), ("sheep", 280, .40, True, 1.9),
                                ("cow", 470, .50, False, .8), ("cow", 562, .44, True, 2.6)]:
        b.append(animal(kind, x, y_at(mid, x) + 9, s, flip, d))

    # near field with crop rows
    near = catmull([(0, 356), (200, 346), (420, 354), (620, 344), (820, 352), (1000, 342)], 10)
    defs.append('<clipPath id="cn"><path d="%s"/></clipPath>' % hill_path(near, W, H))
    b.append('<path d="%s" fill="url(#fieldN)"/>' % hill_path(near, W, H))
    nrows = "".join('<path d="M520 292L%d 440"/>' % xb for xb in range(-1400, 2400, 78))
    nrows2 = "".join('<path d="M520 292L%d 440"/>' % (xb + 39) for xb in range(-1400, 2400, 78))
    b.append('<g clip-path="url(#cn)"><g stroke="#0b4a20" stroke-width="3" opacity=".85">%s</g>'
             '<g stroke="#3fbd62" stroke-width="1.2" opacity=".4">%s</g></g>' % (nrows, nrows2))

    # tractor (scaled), driving left -> right; the near field is left clear for it
    b.append('<g transform="translate(0 396) scale(.86)"><g class="drive">%s</g></g>' % ico_tractor())

    # fireflies
    ff = ""
    for _ in range(9):
        x, y = r.uniform(30, 970), r.uniform(205, 395)
        ff += ('<g class="ff" style="animation-delay:%ss;animation-duration:%ss"><circle cx="%s" cy="%s" r="7" fill="#d8ff7a" opacity=".16"/>'
               '<circle cx="%s" cy="%s" r="2" fill="#eaffa6"/></g>' % (f(-r.uniform(0, 7)), f(r.uniform(5, 9)), f(x), f(y), f(x), f(y)))
    b.append(ff)

    # fence in front
    fence = ('<rect x="-4" y="402" width="1008" height="8" fill="url(#fence)"/><rect x="-4" y="402" width="1008" height="1.6" fill="#d9a066" opacity=".5"/>'
             '<rect x="-4" y="424" width="1008" height="8" fill="url(#fence)"/><rect x="-4" y="424" width="1008" height="1.6" fill="#d9a066" opacity=".5"/>')
    for px in range(14, 1010, 84):
        fence += '<path d="M%d 440V398L%d 391L%d 398V440Z" fill="url(#fence)"/>' % (px, px + 7, px + 14)
        fence += '<path d="M%d 440V398L%d 391" stroke="#d9a066" stroke-width="1" opacity=".5" fill="none"/>' % (px, px + 7)
    b.append(fence)
    # a dog by the fence on the left, and a rooster crowing on the post by the barn
    b.append(animal("dog", 64, 440, .9, False, .3))
    b.append(animal("rooster", 861, 392, .9, False, .5))
    for i in range(14):
        b.append(tuft(r.uniform(-6, 1004), 442, s=r.uniform(.6, 1.0), delay=r.uniform(0, 4), dur=r.uniform(3.4, 5.4)))

    # hanging wooden sign (swings gently)
    size = fit_size("display", HANDLE, 90, 590)
    cap = cap_height("display", size)
    base = 62 + cap + 10
    grain = "".join('<path d="M130 %d Q310 %d 500 %d T870 %d" fill="none" stroke="#2f1c0c" stroke-width="1.4" opacity=".2"/>'
                    % (52 + i * 17, 52 + i * 17 - 3, 52 + i * 17, 52 + i * 17 + 1) for i in range(8))
    sign = (
        '<ellipse cx="500" cy="192" rx="372" ry="9" fill="#000" opacity=".25"/>'
        '<path d="M232 0V50M768 0V50" stroke="#d9b873" stroke-width="3.4"/><path d="M232 0V50M768 0V50" stroke="#8a6a2e" stroke-width="3.4" stroke-dasharray="2 5"/>'
        '<rect x="128" y="38" width="744" height="146" rx="12" fill="url(#wood)" stroke="#2f1c0c" stroke-width="2.4"/>'
        + grain +
        '<rect x="142" y="52" width="716" height="118" rx="7" fill="none" stroke="#c28a4f" stroke-width="2" opacity=".5"/>'
        '<g fill="#2a1a0c"><circle cx="146" cy="56" r="4.4"/><circle cx="854" cy="56" r="4.4"/><circle cx="146" cy="166" r="4.4"/><circle cx="854" cy="166" r="4.4"/></g>'
        '<g fill="#d9a066" opacity=".7"><circle cx="145" cy="55" r="1.4"/><circle cx="853" cy="55" r="1.4"/><circle cx="145" cy="165" r="1.4"/><circle cx="853" cy="165" r="1.4"/></g>'
        + text("display", HANDLE, 503, base + 4, size, "#1c0f05", anchor="middle", opacity=.7)
        + text("display", HANDLE, 500, base, size, P["cream"], anchor="middle")
        + text("mono", TAGLINE, 500, base + 38, 18, P["g4"], anchor="middle", tracking=3)
    )
    b.append('<g class="swing" style="transform-origin:500px 0px">%s</g>' % sign)
    b.append('<rect width="%d" height="%d" fill="url(#vig)"/>' % (W, H))
    return svg_doc(W, H, "".join(b), "".join(defs), css, "%s - farm hero banner" % HANDLE, rounded=18)


# ============================================================ SECTION BANNER =
def banner(num, title, sub, accent_key, icon_fn, pets=()):
    W, H, OFF = 1000, 146, 22  # OFF = headroom above the sign for the perched animals
    accent = ACCENT[accent_key]
    defs = ('<linearGradient id="bar" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0f3320"/><stop offset=".6" stop-color="#0a2414"/><stop offset="1" stop-color="#071a0e"/></linearGradient>'
            '<linearGradient id="acc" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s" stop-opacity="0"/></linearGradient>' % (accent, accent))
    css = ".flag{animation:flag 3.2s ease-in-out infinite}@keyframes flag{0%,100%{transform:rotate(0)}50%{transform:rotate(-16deg)}}" + ANIMAL_CSS
    b = ['<rect x="2" y="16" width="996" height="86" rx="12" fill="url(#bar)" stroke="#1b5233" stroke-width="2"/>']
    dots = "".join('<circle cx="%d" cy="%d" r="1.7"/>' % (808 + cx * 17 + (8 if cy % 2 else 0), 32 + cy * 18) for cx in range(11) for cy in range(4))
    b.append('<g fill="#1b5233" opacity=".95">%s</g>' % dots)
    # number tab
    b.append('<path d="M16 16H196L170 102H16Q2 102 2 90V28Q2 16 16 16Z" fill="%s"/>' % accent)
    b.append('<path d="M20 22H187L164.5 96H20Q8 96 8 90V30Q8 22 20 22Z" fill="none" stroke="#04110a" stroke-opacity=".32" stroke-width="1.4" stroke-dasharray="5 4"/>')
    b.append(text("display", num, 90, 59 + cap_height("display", 60) / 2, 60, "#04110a", anchor="middle"))
    # title
    tsize = fit_size("display", title, 40, 556)
    b.append(text("mono", "// " + sub, 228, 44, 14, accent, tracking=2.2))
    b.append(text("display", title, 226, 84, tsize, P["cream"]))
    # furrow line with sprouts
    b.append('<rect x="2" y="106" width="996" height="3" rx="1.5" fill="url(#acc)"/>')
    for i, x in enumerate(range(260, 980, 150)):
        b.append(sprout(x, 106, 1.0 + (i % 3) * .12))
    # farm decoration
    b.append(wheat(846, 100, h=54, lean=5, delay=.3))
    b.append(wheat(986, 100, h=48, lean=-4, delay=1.4))
    b.append('<g transform="translate(920 58) scale(1.05)">%s</g>' % icon_fn())
    body = '<g transform="translate(0 %d)">%s</g>' % (OFF, "".join(b))
    for i, (kind, x, s, flip) in enumerate(pets):  # animals perched on the top edge of the sign
        body += animal(kind, x, OFF + 17, s, flip, d=i * 1.1 + .3)
    return svg_doc(W, H, body, defs, css, "%s %s" % (num, title))


# ================================================================== TAG ======
def tag(label, accent_key):
    accent = ACCENT[accent_key]
    size, tr = 15, 2.4
    tw = text_width("mono", label, size, tr)
    W, H = int(tw + 50 + 24), 40
    d = ('<path d="M18 3H%d L%d 37H3Z" fill="#0a2414" stroke="%s" stroke-width="1.6" stroke-linejoin="round"/>'
         '<path d="M3 37L18 3H33L18 37Z" fill="%s"/>' % (W - 3, W - 17, accent, accent))
    d += text("mono", label, 48, 20 + cap_height("mono", size) / 2, size, P["cream"], tracking=tr)
    return svg_doc(W, H, d, "", "", label)


# ============================================================ PROJECT HEADER =
def project(p):
    W, H = 1000, 156
    live = p["badge"].startswith("LIVE")
    defs = ('<linearGradient id="soil" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6b4423"/><stop offset="1" stop-color="#3b2514"/></linearGradient>'
            '<linearGradient id="pnl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0f3320"/><stop offset="1" stop-color="#071a0e"/></linearGradient>')
    b = ['<rect x="2" y="2" width="996" height="152" rx="16" fill="url(#pnl)" stroke="#1b5233" stroke-width="2"/>']
    b.append('<path d="M18 2H178V154H18Q2 154 2 138V18Q2 2 18 2Z" fill="url(#soil)"/>')
    b.append('<g stroke="#2b1b0e" stroke-width="3" opacity=".55"><path d="M2 112H178M2 128H178M2 144H178"/></g>')
    b.append(text("mono", "PLOT", 90, 36, 13, P["cream"], anchor="middle", tracking=5, opacity=.8))
    b.append(text("display", p["num"], 90, 90, 52, P["cream"], anchor="middle"))
    b.append(sprout(90, 152, 2.1))
    # status pill
    pill_w = text_width("mono", p["badge"], 13, 2) + 52
    px = W - 16 - pill_w
    b.append('<rect x="%s" y="18" width="%s" height="28" rx="14" fill="#04110a" stroke="%s" stroke-width="1.6"/>' % (f(px), f(pill_w), P["g4"] if live else P["gold"]))
    b.append('<circle cx="%s" cy="32" r="5" fill="%s" class="pulse"/>' % (f(px + 17), P["g4"] if live else P["gold"]))
    b.append(text("mono", p["badge"], px + 31, 37, 13, P["cream"], tracking=2))
    # title + tagline
    tsize = fit_size("display", p["name"], 44, 590)
    b.append(text("display", p["name"], 206, 72, tsize, P["cream"]))
    b.append(text("mono", p["tagline"], 207, 100, 16, P["mist"], tracking=1.2))
    # chips
    cx = 206
    for slug, label in p["stack"]:
        cw = 10 + 18 + 7 + text_width("mono", label, 13.5, 1.2) + 13
        b.append('<rect x="%s" y="110" width="%s" height="32" rx="10" fill="#0f3320" stroke="#1f6f3a" stroke-width="1.4"/>' % (f(cx), f(cw)))
        b.append(icon_path(slug, cx + 10, 117, 18, P["cream"]))
        b.append(text("mono", label, cx + 35, 130.6, 13.5, P["cream"], tracking=1.2))
        cx += cw + 8
    pet = PROJECT_PETS.get(p["file"])
    if pet:  # a little animal on the soil tile, facing the sprout
        b.append(animal(pet[0], 150, 152, pet[1], True, d=int(p["num"]) * .7))
    css = ANIMAL_CSS
    return svg_doc(W, H, "".join(b), defs, css, "%s - %s" % (p["name"], p["tagline"]))


# ============================================================ ACHIEVEMENT CARD =
_PANEL_DEF = ('<linearGradient id="pnl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0f3320"/>'
              '<stop offset="1" stop-color="#071a0e"/></linearGradient>')
_GOLD_DEF = ('<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd966"/>'
             '<stop offset="1" stop-color="#d9962a"/></linearGradient>')
_POOL_DEF = '<clipPath id="pool"><circle cx="90" cy="70" r="31"/></clipPath>'


def _medal(tile_fill, scene, extra=""):
    """Left tile of an award card: coloured tile, two ribbon tails, a gold scalloped medallion and its glass glint.
    `scene` is drawn inside the medallion (clipped to url(#pool)); `extra` sits on the tile around the medallion."""
    dots = "".join('<circle cx="%s" cy="%s" r="6.2" fill="url(#gold)"/>' % (f(90 + math.cos(k * math.pi / 8) * 41), f(70 + math.sin(k * math.pi / 8) * 41)) for k in range(16))
    return ('<path d="M18 2H178V154H18Q2 154 2 138V18Q2 2 18 2Z" fill="%s"/>' % tile_fill
            + '<path d="M72 104L58 148L76 139L84 152L92 108Z" fill="#c0392b"/><path d="M108 104L122 148L104 139L96 152L88 108Z" fill="#8fe05a"/>'
            + dots
            + '<circle cx="90" cy="70" r="40" fill="url(#gold)"/><circle cx="90" cy="70" r="35" fill="#fff3d6"/>'
            + extra
            + '<g clip-path="url(#pool)">%s</g>' % scene
            + '<path d="M63 53A31 31 0 0 1 82 40" stroke="#fff" stroke-width="3" opacity=".3" fill="none" stroke-linecap="round"/>')


def _art_shark():
    """Pull Shark: a friendly shark cruising through rippling water."""
    defs = ('<linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a6a8c"/><stop offset="1" stop-color="#0a2c40"/></linearGradient>'
            + _GOLD_DEF
            + '<linearGradient id="shk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7fa6c6"/><stop offset="1" stop-color="#4b7090"/></linearGradient>'
            + _POOL_DEF)
    css = ".wv{animation:wv 3.6s linear infinite}@keyframes wv{from{transform:translateX(0)}to{transform:translateX(-26px)}}"
    waves = "".join('<path d="M%d %dq6.5 -6 13 0t13 0" fill="none" stroke="#bfe6f2" stroke-width="2" opacity="%s"/>' % (x, y, op)
                    for y, op in ((88, .8), (98, .5)) for x in range(36, 170, 26))
    scene = ('<rect x="50" y="36" width="80" height="70" fill="#0f5b7c"/><g class="wv">%s</g>'
             '<g class="bob"><g transform="translate(90 66) scale(.58)">%s</g></g>' % (waves, ico_shark()))
    return dict(defs=defs, css=css, tile="url(#sea)", scene=scene)


def _art_pair():
    """Pair Extraordinaire: two chicks beak to beak under a beating heart, hopping in turn."""
    defs = ('<linearGradient id="mdw" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3aa859"/><stop offset="1" stop-color="#134f2c"/></linearGradient>'
            + _GOLD_DEF
            + '<linearGradient id="sk2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6fc9ea"/><stop offset="1" stop-color="#e4f6dc"/></linearGradient>'
            + _POOL_DEF)
    css = (ANIMAL_CSS + ".beat{transform-box:fill-box;transform-origin:center;animation:beat 1.8s ease-in-out infinite}"
           "@keyframes beat{0%,100%{transform:scale(1)}45%{transform:scale(1.2)}}")
    sparkles = "".join(  # twinkling sparkles in the corners of the tile
        '<path transform="translate(%d %d) scale(%s)" class="tw" style="animation-delay:%ss" '
        'd="M0 -6L1.6 -1.6L6 0L1.6 1.6L0 6L-1.6 1.6L-6 0L-1.6 -1.6Z" fill="#fff3d6"/>' % (x, y, s, f(-d))
        for x, y, s, d in ((32, 34, 1.0, 0), (148, 30, .8, 1.1), (30, 118, .8, 2.2), (150, 116, .9, .6)))
    heart = ('<g transform="translate(90 53) scale(1.15)"><g class="beat">'
             '<path d="M0 6C-8 0 -10 -6 -5.5 -8.2C-2.6 -9.6 0 -7.4 0 -5C0 -7.4 2.6 -9.6 5.5 -8.2C10 -6 8 0 0 6Z" fill="#ff6a5c"/>'
             '<path d="M-5.6 -6.6C-7 -5.6 -7.4 -4 -6.8 -2.6" stroke="#ffd2cb" stroke-width="1.2" fill="none" stroke-linecap="round"/>'
             '</g></g>')
    scene = ('<rect x="50" y="36" width="80" height="70" fill="url(#sk2)"/>'
             '<path d="M50 84C68 76 84 82 96 84C108 86 120 78 134 80V108H50Z" fill="#4cc35a"/>'
             '<path d="M50 92C70 87 88 90 100 91C114 92 124 88 134 90V108H50Z" fill="#2e9b4a"/>'
             + animal("chick", 73, 91, 1.2, False, d=0)
             + animal("chick", 107, 91, 1.2, True, d=.75)
             + heart)
    return dict(defs=defs, css=css, tile="url(#mdw)", scene=scene, extra=sparkles)


ACHIEVEMENT_ART = {"shark": _art_shark, "pair": _art_pair}  # medallion scene per card; pick one with art="..." in ACHIEVEMENTS


def achievement(a):
    W, H = 1000, 156
    art = ACHIEVEMENT_ART[a.get("art", "shark")]()
    defs = _PANEL_DEF + art["defs"]
    css = art["css"]
    b = ['<rect x="2" y="2" width="996" height="152" rx="16" fill="url(#pnl)" stroke="#1b5233" stroke-width="2"/>',
         _medal(art["tile"], art["scene"], art.get("extra", ""))]
    # status pill, title, tagline, chips (same layout as the project cards)
    pill_w = text_width("mono", a["badge"], 13, 2) + 52
    px = W - 16 - pill_w
    b.append('<rect x="%s" y="18" width="%s" height="28" rx="14" fill="#04110a" stroke="%s" stroke-width="1.6"/>' % (f(px), f(pill_w), P["gold"]))
    b.append('<circle cx="%s" cy="32" r="5" fill="%s" class="pulse"/>' % (f(px + 17), P["gold"]))
    b.append(text("mono", a["badge"], px + 31, 37, 13, P["cream"], tracking=2))
    b.append(text("display", a["title"], 206, 72, fit_size("display", a["title"], 46, 590), P["cream"]))
    b.append(text("mono", a["tagline"], 207, 100, 16, P["mist"], tracking=1.2))
    cx = 206
    for slug, label in a["chips"]:
        cw = (10 + 18 + 7 if slug else 14) + text_width("mono", label, 13.5, 1.2) + 13
        b.append('<rect x="%s" y="110" width="%s" height="32" rx="10" fill="#0f3320" stroke="#1f6f3a" stroke-width="1.4"/>' % (f(cx), f(cw)))
        if slug:
            b.append(icon_path(slug, cx + 10, 117, 18, P["cream"]))
        b.append(text("mono", label, cx + (35 if slug else 14), 130.6, 13.5, P["cream"], tracking=1.2))
        cx += cw + 8
    return svg_doc(W, H, "".join(b), defs, css, "%s - %s" % (a["title"], a["tagline"]))


# ============================================================ CERTIFICATE CARD =
def certificate(c):
    W, H = 1000, 156
    defs = ('<linearGradient id="pnl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0f3320"/><stop offset="1" stop-color="#071a0e"/></linearGradient>'
            '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b6a8e"/><stop offset="1" stop-color="#0c3249"/></linearGradient>')
    b = ['<rect x="2" y="2" width="996" height="152" rx="16" fill="url(#pnl)" stroke="#1b5233" stroke-width="2"/>',
         '<path d="M18 2H178V154H18Q2 154 2 138V18Q2 2 18 2Z" fill="url(#sky)"/>']
    for x, y, s, d in ((34, 34, 1.0, 0), (146, 44, .8, 1.1), (142, 122, .9, 2.2), (38, 124, .7, .6)):  # twinkling sparkles
        b.append('<path transform="translate(%d %d) scale(%s)" class="tw" style="animation-delay:%ss" '
                 'd="M0 -6L1.6 -1.6L6 0L1.6 1.6L0 6L-1.6 1.6L-6 0L-1.6 -1.6Z" fill="#fff3d6"/>' % (x, y, s, f(-d)))
    b.append('<g transform="translate(90 80) scale(2.1)"><g class="bob">%s</g></g>' % ico_scroll())
    pill_w = text_width("mono", c["badge"], 13, 2) + 52
    px = W - 16 - pill_w
    b.append('<rect x="%s" y="18" width="%s" height="28" rx="14" fill="#04110a" stroke="%s" stroke-width="1.6"/>' % (f(px), f(pill_w), P["g4"]))
    b.append('<circle cx="%s" cy="32" r="5" fill="%s" class="pulse"/>' % (f(px + 17), P["g4"]))
    b.append(text("mono", c["badge"], px + 31, 37, 13, P["cream"], tracking=2))
    b.append(text("display", c["title"], 206, 72, fit_size("display", c["title"], 44, 590), P["cream"]))
    b.append(text("mono", c["tagline"], 207, 100, 16, P["mist"], tracking=1.2))
    cx = 206
    for label in c["chips"]:
        cw = 14 + text_width("mono", label, 13.5, 1.2) + 13
        b.append('<rect x="%s" y="110" width="%s" height="32" rx="10" fill="#0f3320" stroke="#1f6f3a" stroke-width="1.4"/>' % (f(cx), f(cw)))
        b.append(text("mono", label, cx + 14, 130.6, 13.5, P["cream"], tracking=1.2))
        cx += cw + 8
    return svg_doc(W, H, "".join(b), defs, "", "%s - %s" % (c["title"], c["tagline"]))


# ============================================================= TECH CAROUSEL =
def toolshed():
    W, H = 1000, 252
    pitch, tw_, th_ = 138, 124, 92
    rows = [(TECH_ROW_1, 24, P["g3"], "m1"), (TECH_ROW_2, 136, P["gold2"], "m2")]
    defs = ('<linearGradient id="fl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#06180d"/><stop offset="1" stop-color="#06180d" stop-opacity="0"/></linearGradient>'
            '<linearGradient id="fr" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#06180d"/><stop offset="1" stop-color="#06180d" stop-opacity="0"/></linearGradient>'
            '<linearGradient id="plank" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6b4423"/><stop offset="1" stop-color="#4a2e17"/></linearGradient>')
    css = ""
    b = ['<rect x="2" y="2" width="996" height="248" rx="16" fill="#06180d" stroke="#1b5233" stroke-width="2"/>']
    b.append('<g stroke="#0d2a18" stroke-width="2"><path d="M2 236H998M2 244H998"/></g>')

    def tile(i, slug, label, y, accent):
        x = i * pitch
        return (
            '<g transform="translate(%d %d)"><rect width="%d" height="%d" rx="12" fill="#0c2a18" stroke="%s" stroke-opacity=".75" stroke-width="1.6"/>'
            '<path d="M1 %d H%d V%d Q%d %d %d %d H13 Q1 %d 1 %d Z" fill="url(#plank)"/>'
            '<path d="M1 %d H%d" stroke="#a06c38" stroke-width="1.4" opacity=".7"/>%s%s</g>'
            % (x, y, tw_, th_, accent, th_ - 26, tw_ - 1, th_ - 13, tw_ - 1, th_ - 1, tw_ - 13, th_ - 1, th_ - 1, th_ - 13,
               th_ - 26, tw_ - 1,
               icon_path(slug, tw_ / 2 - 19, 14, 38, P["cream"]),
               text("mono", label, tw_ / 2, th_ - 9, 12, P["cream"], anchor="middle", tracking=.9)))

    for idx, (items, y, accent, anim) in enumerate(rows):
        n = len(items)
        total = n * pitch
        copy = "".join(tile(i, s, l, y, accent) for i, (s, l) in enumerate(items))
        copy2 = "".join(tile(i + n, s, l, y, accent) for i, (s, l) in enumerate(items))
        if idx == 0:
            css += ".%s{animation:%s %ds linear infinite}@keyframes %s{from{transform:translateX(0)}to{transform:translateX(-%dpx)}}" % (anim, anim, int(total / 26), anim, total)
        else:
            css += ".%s{animation:%s %ds linear infinite}@keyframes %s{from{transform:translateX(-%dpx)}to{transform:translateX(0)}}" % (anim, anim, int(total / 30), anim, total)
        b.append('<g class="%s"><g transform="translate(18 0)">%s%s</g></g>' % (anim, copy, copy2))
    b.append('<rect x="2" y="2" width="90" height="248" rx="16" fill="url(#fl)"/><rect x="908" y="2" width="90" height="248" rx="16" fill="url(#fr)"/>')
    return svg_doc(W, H, "".join(b), defs, css, "Tech arsenal carousel")


# ================================================================ GROWTH BAR ==
def growth():
    W, H = 1000, 74
    stages = [("SEED", 40), ("SPROUT", 270), ("GROW", 500), ("BLOOM", 730), ("HARVEST", 960)]
    T = 9.0
    css = ".bar{animation:fill %ss ease-in-out infinite}@keyframes fill{0%%{transform:scaleX(0)}70%%,92%%{transform:scaleX(1)}100%%{transform:scaleX(0)}}" % T
    defs = '<linearGradient id="gb" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4cc35a"/><stop offset=".7" stop-color="#c8f26b"/><stop offset="1" stop-color="#f5c542"/></linearGradient>'
    b = ['<rect x="40" y="32" width="920" height="8" rx="4" fill="#0f3320" stroke="#1b5233" stroke-width="1.4"/>']
    b.append('<g class="bar" style="transform-origin:40px 36px"><rect x="40" y="32" width="920" height="8" rx="4" fill="url(#gb)"/></g>')
    for i, (label, x) in enumerate(stages):
        start = 0.70 * i / 4.0 * 100
        css += "@keyframes st%d{0%%,%s%%{opacity:0;transform:scale(.6)}%s%%,92%%{opacity:1;transform:scale(1)}100%%{opacity:0;transform:scale(.6)}}" % (i, f(start), f(start + 2.5))
        css += ".st%d{animation:st%d %ss ease-out infinite;transform-origin:%dpx 36px}" % (i, i, T, x)
        b.append('<circle cx="%d" cy="36" r="12" fill="#06180d" stroke="#1f6f3a" stroke-width="2.6"/>' % x)
        glyph = '<circle cx="%d" cy="36" r="6.2" fill="%s"/>' % (x, P["g4"] if i < 4 else P["gold"])
        b.append('<g class="st%d">%s</g>' % (i, glyph))
        b.append(text("mono", label, x, 66, 12, P["mist"], anchor="middle", tracking=3))
    return svg_doc(W, H, "".join(b), defs, css, "Growth progress: seed, sprout, grow, bloom, harvest")


# ===================================================================== FOOTER =
def footer():
    W, H = 1000, 210
    r = rng(5)
    defs = ('<linearGradient id="fs" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#06180d"/><stop offset=".55" stop-color="#0c3d20"/><stop offset="1" stop-color="#1f7037"/></linearGradient>'
            '<radialGradient id="fh"><stop offset="0" stop-color="#ffd45a" stop-opacity=".55"/><stop offset="1" stop-color="#ffd45a" stop-opacity="0"/></radialGradient>')
    b = ['<rect width="1000" height="210" fill="url(#fs)"/>']
    for i in range(24):
        b.append('<circle cx="%s" cy="%s" r="%s" fill="#fff3d6" opacity="%s"%s/>' % (
            f(r.uniform(10, 990)), f(r.uniform(8, 110)), r.choice([.7, 1, 1.3]), f(r.uniform(.3, .85)),
            ' class="tw" style="animation-delay:%ss"' % f(-r.uniform(0, 3)) if i % 3 == 0 else ""))
    b.append('<circle cx="170" cy="168" r="120" fill="url(#fh)"/><circle cx="170" cy="168" r="40" fill="#ffd45a"/>')
    h1 = catmull([(0, 170), (160, 150), (330, 162), (520, 148), (700, 160), (860, 146), (1000, 158)], 10)
    b.append('<path d="%s" fill="#0d4a22"/>' % hill_path(h1, 1000, 210))
    h2 = catmull([(0, 190), (200, 178), (420, 188), (640, 176), (840, 186), (1000, 178)], 10)
    b.append('<path d="%s" fill="#14672f"/>' % hill_path(h2, 1000, 210))
    b.append(text("display", "THANKS FOR VISITING THE FARM", 500, 74, fit_size("display", "THANKS FOR VISITING THE FARM", 38, 800), P["cream"], anchor="middle"))
    b.append(text("mono", "BUILT WITH SOIL, SUN & A LOT OF COMMITS", 500, 104, 14, P["g4"], anchor="middle", tracking=3.2))
    # a lighter field of wheat with a small herd standing in front of it (spaced out so nothing overlaps)
    for i in range(16):
        x = 22 + i * 62 + r.uniform(-10, 10)
        b.append(wheat(x, 212, h=r.uniform(40, 68), lean=r.uniform(-8, 8), delay=r.uniform(0, 4), dur=r.uniform(3.8, 5.6)))
    herd = [("cow", 300, 1.0, False), ("sheep", 438, .92, True), ("pig", 586, .92, False),
            ("hen", 716, .96, True), ("chick", 756, 1.0, False), ("dog", 880, .96, True)]
    for i, (kind, x, s, flip) in enumerate(herd):
        b.append(animal(kind, x, 207, s, flip, d=i * .9))
    for i in range(10):
        b.append(tuft(r.uniform(0, 1000), 212, s=r.uniform(.7, 1.1), delay=r.uniform(0, 4)))
    return svg_doc(1000, 210, "".join(b), defs, ANIMAL_CSS, "Thanks for visiting the farm", rounded=18)


# ===================================================================== BADGES =
def badge(label, accent_key, icon):
    accent = ACCENT[accent_key]
    size, tr = 15, 2.6
    tw = text_width("mono", label, size, tr)
    W, H = int(tw + 78), 46
    b = ['<rect x="1.5" y="1.5" width="%d" height="43" rx="12" fill="#0a2414" stroke="%s" stroke-width="2"/>' % (W - 3, accent)]
    b.append('<rect x="1.5" y="1.5" width="42" height="43" rx="12" fill="%s"/><rect x="30" y="1.5" width="14" height="43" fill="%s"/>' % (accent, accent))
    cx, cy = 22, 23
    if icon in ICONS:
        b.append(icon_path(icon, cx - 11, cy - 11, 22, "#04110a"))
    elif icon == "linkedin":
        b.append('<rect x="%d" y="%d" width="22" height="22" rx="4" fill="#04110a"/>' % (cx - 11, cy - 11))
        b.append(text("display", "in", cx, cy + 6.2, 17, accent, anchor="middle"))
    elif icon == "mail":
        b.append('<rect x="%d" y="%d" width="24" height="17" rx="3" fill="#04110a"/><path d="M%d %dL%d %dL%d %d" fill="none" stroke="%s" stroke-width="2" stroke-linejoin="round"/>'
                 % (cx - 12, cy - 8, cx - 11, cy - 6, cx, cy + 2, cx + 11, cy - 6, accent))
    elif icon == "sunflower":  # drawn as a globe: reads clearly at 22px
        b.append('<g transform="translate(%d %d)" fill="none" stroke="#04110a" stroke-width="2.1" stroke-linecap="round">'
                 '<circle r="10.5"/><ellipse rx="4.6" ry="10.5"/><path d="M-10.5 0H10.5M-8.6 -5.6H8.6M-8.6 5.6H8.6"/></g>' % (cx, cy))
    b.append(text("mono", label, 58, 23 + cap_height("mono", size) / 2, size, P["cream"], tracking=tr))
    return svg_doc(W, H, "".join(b), "", "", label)


# ===================================================================== MAIN ===
def main():
    print("building assets ->", OUT)
    write("hero", hero())
    write("growth", growth())
    for num, title, sub, accent, icon, name, pets in SECTIONS:
        write(name, banner(num, title, sub, accent, icon, pets))
    for name, label, accent in TAGS:
        write(name, tag(label, accent))
    for p in PROJECTS:
        write(p["file"], project(p))
    for a in ACHIEVEMENTS:
        write(a["file"], achievement(a))
    for c in CERTIFICATES:
        write(c["file"], certificate(c))
    write("arsenal", toolshed())
    for name, label, accent, icon in BADGES:
        write(name, badge(label, accent, icon))
    write("footer", footer())


if __name__ == "__main__":
    main()
