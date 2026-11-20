"""Shared drawing helpers for the farm-themed README assets (pure stdlib).

Text is converted to vector paths (glyph data in farm_glyphs.json) so every SVG
renders identically everywhere without fonts, and works when GitHub loads the
file through an <img> tag (no scripts, no external requests).

Fonts: Alfa Slab One + Space Mono Bold (SIL Open Font License 1.1).
Logos: Simple Icons (CC0 1.0).  See scripts/README.md.
"""
import json
import math
import os
import random
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(HERE, "farm_glyphs.json"), encoding="utf-8") as _fh:
    GLYPHS = json.load(_fh)
with open(os.path.join(HERE, "farm_icons.json"), encoding="utf-8") as _fh:
    ICONS = json.load(_fh)

# ----------------------------------------------------------------- palette --
P = {
    "pitch": "#03100a", "deep": "#06180d", "panel": "#0a2414", "raised": "#0f3320",
    "edge": "#1b5233",
    "g1": "#1f6f3a", "g2": "#2e9b4a", "g3": "#4cc35a", "g4": "#8fe05a", "g5": "#c8f26b",
    "gold": "#f5c542", "gold2": "#e8a825", "cream": "#fff3d6", "mist": "#9cc7a0",
    "barn": "#c0392b", "barn2": "#8e2a20", "sky": "#7fd6e8", "orange": "#ff9f43",
    "wood": "#6b4423", "wood2": "#8a5a2e", "wood3": "#4a2e17",
    "soil": "#5a3a1e", "soil2": "#2b1b0e",
}

CSS_BASE = (
    ".sway{animation:sway 4.6s ease-in-out infinite}"
    "@keyframes sway{0%,100%{transform:rotate(-4deg)}50%{transform:rotate(4deg)}}"
    ".spin{animation:spin 12s linear infinite}"
    "@keyframes spin{to{transform:rotate(360deg)}}"
    ".tw{animation:tw 3s ease-in-out infinite}"
    "@keyframes tw{0%,100%{opacity:.18}50%{opacity:1}}"
    ".bob{animation:bob 3.4s ease-in-out infinite}"
    "@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}"
    ".pulse{animation:pulse 2.2s ease-in-out infinite}"
    "@keyframes pulse{0%,100%{opacity:.3}50%{opacity:1}}"
)
CSS_REDUCED = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"


def f(n):
    """Compact number formatting."""
    s = ("%.2f" % n).rstrip("0").rstrip(".")
    return "0" if s in ("", "-0") else s


def svg_doc(w, h, body, defs="", css="", title="", rounded=0):
    """Wrap content into a standalone SVG document string."""
    t = escape(title)
    if rounded:
        defs += '<clipPath id="rc"><rect width="%s" height="%s" rx="%s"/></clipPath>' % (w, h, rounded)
        body = '<g clip-path="url(#rc)">%s</g>' % body
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %s %s" width="%s" height="%s" '
        'role="img" aria-label="%s"><title>%s</title><defs>%s</defs><style>%s%s%s</style>%s</svg>\n'
        % (w, h, w, h, t, t, defs, CSS_BASE, css, CSS_REDUCED, body)
    )


# -------------------------------------------------------------------- text --
def _glyph(font, ch):
    table = GLYPHS[font]["g"]
    return table.get(ch) or table.get("?") or [500, ""]


def text_width(font, s, size, tracking=0.0):
    sc = size / GLYPHS[font]["upem"]
    return sum(_glyph(font, ch)[0] for ch in s) * sc + tracking * max(len(s) - 1, 0)


def fit_size(font, s, size, max_w, tracking=0.0):
    """Largest size <= `size` so the string fits in max_w."""
    w = text_width(font, s, size, tracking)
    return size if w <= max_w else size * max_w / w


def text(font, s, x, y, size, fill, anchor="start", tracking=0.0, opacity=None, extra=""):
    """Vector text. `y` is the baseline. Returns a <g> element string."""
    sc = size / GLYPHS[font]["upem"]
    w = text_width(font, s, size, tracking)
    x0 = x - w / 2 if anchor == "middle" else (x - w if anchor == "end" else x)
    adv = 0.0
    paths = []
    for ch in s:
        a, d = _glyph(font, ch)
        if d:
            paths.append('<path transform="translate(%d 0)" d="%s"/>' % (round(adv), d))
        adv += a + tracking / sc
    op = ' fill-opacity="%s"' % opacity if opacity is not None else ""
    return '<g transform="translate(%s %s) scale(%s %s)" fill="%s"%s %s>%s</g>' % (
        f(x0), f(y), "%.5f" % sc, "%.5f" % -sc, fill, op, extra, "".join(paths))


def cap_height(font, size):
    g = GLYPHS[font]
    return g["cap"] * size / g["upem"]


# ------------------------------------------------------------------ shapes --
def catmull(points, steps=8):
    """Dense smooth polyline through points (Catmull-Rom)."""
    pts = [points[0]] + list(points) + [points[-1]]
    out = []
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        for k in range(steps):
            t = k / float(steps)
            t2, t3 = t * t, t * t * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2
                       + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2
                       + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    out.append(points[-1])
    return out


def y_at(samples, x):
    for (x0, y0), (x1, y1) in zip(samples, samples[1:]):
        if x0 <= x <= x1 and x1 > x0:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return samples[-1][1] if x > samples[-1][0] else samples[0][1]


def hill_path(samples, w, h):
    d = "M%s %s" % (f(samples[0][0]), f(samples[0][1]))
    for x, y in samples[1:]:
        d += "L%s %s" % (f(x), f(y))
    return d + "L%s %sL0 %sZ" % (w, h, h)


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def wheat(x, y, h=60, lean=6, delay=0.0, dur=4.6, animate=True, stalk="#c9a24a", g1="#f5c542", g2="#d9962a"):
    """A wheat stalk rooted at (x, y), swaying around its base."""
    p0, p1, p2, p3 = (0, 0), (lean * .2, -h * .35), (lean * .7, -h * .7), (lean, -h)
    out = ['<path d="M0 0C%s %s %s %s %s %s" fill="none" stroke="%s" stroke-width="2" stroke-linecap="round"/>'
           % (f(p1[0]), f(p1[1]), f(p2[0]), f(p2[1]), f(p3[0]), f(p3[1]), stalk)]
    for i in range(6):
        t = 0.55 + i * 0.075
        px, py = bez(p0, p1, p2, p3, t)
        col = g1 if i % 2 else g2
        out.append('<ellipse cx="%s" cy="%s" rx="2.5" ry="6.2" transform="rotate(-36 %s %s)" fill="%s"/>'
                   % (f(px - 3.1), f(py), f(px - 3.1), f(py), col))
        out.append('<ellipse cx="%s" cy="%s" rx="2.5" ry="6.2" transform="rotate(36 %s %s)" fill="%s"/>'
                   % (f(px + 3.1), f(py), f(px + 3.1), f(py), col))
    out.append('<ellipse cx="%s" cy="%s" rx="2.6" ry="6.8" fill="%s"/>' % (f(lean), f(-h - 4), g1))
    inner = "".join(out)
    if animate:
        inner = '<g class="sway" style="transform-origin:0px 0px;animation-delay:%ss;animation-duration:%ss">%s</g>' % (
            f(-delay), f(dur), inner)
    return '<g transform="translate(%s %s)">%s</g>' % (f(x), f(y), inner)


def tuft(x, y, s=1.0, delay=0.0, dur=4.2, shades=("#1f7a3a", "#2fa04d", "#4cc35a", "#2a9347", "#3db554"), animate=True):
    """A tuft of grass whose base sits at (x, y)."""
    blades = [(-9, 17, 6), (-4, 27, 3), (1, 34, -1), (6, 25, -4), (11, 16, -7)]
    out = []
    for i, (dx, h, c) in enumerate(blades):
        out.append('<path d="M%s 0Q%s %s %s %sQ%s %s %s 0Z" fill="%s"/>' % (
            f(dx - 2.8), f(dx - 1), f(-h * .6), f(dx + c), f(-h), f(dx + 1.8), f(-h * .45), f(dx + 2.8),
            shades[i % len(shades)]))
    inner = "".join(out)
    if animate:
        inner = '<g class="sway" style="transform-origin:0px 0px;animation-delay:%ss;animation-duration:%ss">%s</g>' % (
            f(-delay), f(dur), inner)
    return '<g transform="translate(%s %s) scale(%s)">%s</g>' % (f(x), f(y), f(s), inner)


def sprout(x, y, s=1.0, color1="#6fd47f", color2="#4bb862", stem="#53c26a"):
    return ('<g transform="translate(%s %s) scale(%s)">'
            '<path d="M0 0V-9" stroke="%s" stroke-width="1.8" stroke-linecap="round"/>'
            '<path d="M0 -8.6C-4.6 -8.2 -6.6 -11 -6.8 -14.4C-2.6 -14.6 -0.2 -12.2 0 -8.6Z" fill="%s"/>'
            '<path d="M0 -6.2C4.6 -5.8 6.6 -8.6 6.8 -12C2.6 -12.2 0.2 -9.8 0 -6.2Z" fill="%s"/></g>'
            % (f(x), f(y), f(s), stem, color1, color2))


def icon_path(slug, x, y, size, fill):
    """Simple Icons logo (24x24 box) drawn at top-left (x, y)."""
    d = ICONS[slug]["d"]
    return '<g transform="translate(%s %s) scale(%s)"><path d="%s" fill="%s"/></g>' % (
        f(x), f(y), "%.4f" % (size / 24.0), d, fill)


# ------------------------------------------------------------------- icons --
# All icons are drawn around (0,0), roughly within +-32 px, ready for translate()/scale().
def ico_barn():
    return (
        '<path d="M-26 22V-4L-16 -16L0 -24L16 -16L26 -4V22Z" fill="#c0392b"/>'
        '<path d="M-26 -4L-16 -16L0 -24L16 -16L26 -4" fill="none" stroke="#5c1d17" stroke-width="3.4" stroke-linejoin="round"/>'
        '<path d="M-26 22V-4L-16 -16L0 -24L16 -16L26 -4V22Z" fill="none" stroke="#fff3d6" stroke-width="1.3" opacity=".55"/>'
        '<rect x="-9" y="2" width="18" height="20" fill="#8e2a20" stroke="#fff3d6" stroke-width="1.6"/>'
        '<path d="M-9 2L9 22M9 2L-9 22" stroke="#fff3d6" stroke-width="1.5"/>'
        '<rect x="-5" y="-13" width="10" height="7" fill="#ffd166"/>'
        '<path d="M-5 -9.5H5M0 -13V-6" stroke="#8e2a20" stroke-width="1"/>'
    )


def ico_sunflower():
    petals = "".join(
        '<ellipse cx="0" cy="-14" rx="4.3" ry="9.5" transform="rotate(%d)" fill="%s"/>' % (k * 30 + (15 if k % 2 else 0), "#f5c542" if k % 2 else "#e8a825")
        for k in range(12))
    seeds = "".join('<circle cx="%s" cy="%s" r="1" fill="#8a5a2e"/>' % (f(math.cos(a) * r), f(math.sin(a) * r))
                    for a, r in [(0.3, 3), (2.4, 4), (4.2, 3.4), (5.5, 5), (1.3, 5.4), (3.3, 5.8), (0, 0)])
    return petals + '<circle r="8.2" fill="#4a2e17"/>' + seeds


def ico_sprout_big():
    return (
        '<path d="M-16 20Q0 8 16 20Z" fill="#5a3a1e"/>'
        '<path d="M0 14V-6" stroke="#53c26a" stroke-width="3" stroke-linecap="round"/>'
        '<path d="M0 -4C-12 -3 -18 -11 -18 -20C-7 -21 -1 -14 0 -4Z" fill="#8fe05a"/>'
        '<path d="M0 3C11 4 17 -3 18 -12C8 -13 1 -7 0 3Z" fill="#4cc35a"/>'
    )


def ico_wheat_bundle(animate=False):
    out = ""
    for i, (dx, lean) in enumerate([(-9, -9), (0, 0), (9, 9)]):
        out += wheat(dx * .5, 22, h=40, lean=lean, delay=i * .5, animate=animate)
    return out


def ico_idcard():
    return (
        '<rect x="-32" y="-21" width="64" height="42" rx="6" fill="#fff3d6"/>'
        '<path d="M-32 -15Q-32 -21 -26 -21H26Q32 -21 32 -15V-9H-32Z" fill="#8fe05a"/>'
        '<circle cx="-18" cy="3" r="8" fill="#4cc35a"/>'
        '<path d="M-18 8V-1" stroke="#04110a" stroke-width="1.6" stroke-linecap="round"/>'
        '<path d="M-18 -.4C-22 0 -23.5 -2.4 -23.6 -4.6C-20 -4.8 -18.2 -3 -18 -.4Z" fill="#04110a"/>'
        '<path d="M-18 1.4C-14 1.8 -12.6 -.4 -12.4 -2.6C-16 -2.8 -17.8 -1.2 -18 1.4Z" fill="#04110a"/>'
        '<rect x="-4" y="-2" width="28" height="4" rx="2" fill="#0a2414" opacity=".85"/>'
        '<rect x="-4" y="6" width="20" height="3.4" rx="1.7" fill="#0a2414" opacity=".55"/>'
        '<rect x="-4" y="13" width="26" height="3" rx="1.5" fill="#0a2414" opacity=".35"/>'
    )


def ico_pitchfork():
    return (
        '<g transform="rotate(18)">'
        '<path d="M0 30V-2" stroke="#8a5a2e" stroke-width="5.4" stroke-linecap="round"/>'
        '<path d="M-12 -26V-9Q-12 0 0 0Q12 0 12 -9V-26M0 0V-30" fill="none" stroke="#dfe8dc" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M-14.4 -26L-12 -33L-9.6 -26ZM-2.4 -30L0 -37L2.4 -30ZM9.6 -26L12 -33L14.4 -26Z" fill="#dfe8dc"/>'
        '</g>'
        '<g transform="translate(-22 4) rotate(-32)"><path d="M0 24V-12" stroke="#8a5a2e" stroke-width="4.4" stroke-linecap="round"/>'
        '<path d="M-9 -12H9L7 -22Q0 -26 -7 -22Z" fill="#dfe8dc"/></g>'
    )


def ico_rosette():
    scallops = "".join('<circle cx="%s" cy="%s" r="5.2" fill="#f5c542"/>' % (
        f(math.cos(k * math.pi / 6) * 15), f(-6 + math.sin(k * math.pi / 6) * 15)) for k in range(12))
    return (
        '<path d="M-10 6L-17 30L-8 25L-3 31L1 8Z" fill="#c0392b"/>'
        '<path d="M10 6L17 30L8 25L3 31L-1 8Z" fill="#8fe05a"/>'
        + scallops +
        '<circle cx="0" cy="-6" r="13.5" fill="#e8a825"/><circle cx="0" cy="-6" r="10" fill="#fff3d6"/>'
        '<path d="M0 -13L2.4 -7.4L8.4 -7L3.8 -3.2L5.2 2.6L0 -.4L-5.2 2.6L-3.8 -3.2L-8.4 -7L-2.4 -7.4Z" fill="#e8a825"/>'
    )


def ico_scroll():
    return (
        '<rect x="-27" y="-20" width="54" height="40" rx="3" fill="#fff3d6"/>'
        '<rect x="-23" y="-16" width="46" height="32" rx="1.5" fill="none" stroke="#c9a24a" stroke-width="1.4" stroke-dasharray="3 2"/>'
        '<rect x="-17" y="-10" width="34" height="3.6" rx="1.8" fill="#0a2414" opacity=".75"/>'
        '<rect x="-17" y="-3" width="26" height="3" rx="1.5" fill="#0a2414" opacity=".4"/>'
        '<rect x="-17" y="3" width="20" height="3" rx="1.5" fill="#0a2414" opacity=".4"/>'
        '<path d="M10 12L6 26L12 22L17 27L16 12Z" fill="#c0392b"/>'
        '<circle cx="12" cy="9" r="8" fill="#c0392b"/><circle cx="12" cy="9" r="5.4" fill="none" stroke="#fff3d6" stroke-width="1.2"/>'
        '<path d="M12 5.4L13.1 8L15.8 8.2L13.7 9.9L14.4 12.5L12 11.1L9.6 12.5L10.3 9.9L8.2 8.2L10.9 8Z" fill="#fff3d6"/>'
    )


def ico_mailbox():
    return (
        '<rect x="-3" y="2" width="6" height="30" fill="#8a5a2e"/>'
        '<path d="M-24 2V-10Q-24 -22 -10 -22H10Q24 -22 24 -10V2Z" fill="#c0392b"/>'
        '<path d="M-24 2H24" stroke="#5c1d17" stroke-width="3"/>'
        '<rect x="-18" y="-10" width="16" height="4" rx="2" fill="#04110a" opacity=".55"/>'
        '<g transform="translate(24 -8)"><g class="flag" style="transform-origin:0px 6px"><rect x="-2" y="-22" width="4" height="28" fill="#dfe8dc"/>'
        '<path d="M2 -22H16V-12H2Z" fill="#f5c542"/></g></g>'
    )


def ico_pots():
    out = ""
    for i, (x, stage) in enumerate([(-22, 1), (0, 2), (22, 3)]):
        out += '<path d="M%s 8L%s 8L%s 28L%s 28Z" fill="#b5603a"/><rect x="%s" y="5" width="20" height="5" rx="1.5" fill="#cf7447"/>' % (
            x - 9, x + 9, x + 7, x - 7, x - 10)
        out += '<path d="M%s 8H%s" stroke="#5a3a1e" stroke-width="3"/>' % (x - 8, x + 8)
        if stage == 1:
            out += sprout(x, 6, 1.0)
        elif stage == 2:
            out += sprout(x, 6, 1.5)
        else:
            out += ('<g transform="translate(%s 6)"><path d="M0 0V-24" stroke="#53c26a" stroke-width="2.4" stroke-linecap="round"/>'
                    '<path d="M0 -8C-9 -8 -13 -13 -13 -19C-5 -19 -1 -15 0 -8Z" fill="#8fe05a"/>'
                    '<path d="M0 -14C8 -14 12 -19 12 -25C5 -25 1 -21 0 -14Z" fill="#4cc35a"/>'
                    '<circle cx="0" cy="-28" r="5" fill="#f5c542"/><circle cx="0" cy="-28" r="2" fill="#8a5a2e"/></g>' % x)
    return out


def ico_sun(rays=10):
    r = "".join('<path d="M0 -19L-2.6 -27L2.6 -27Z" transform="rotate(%d)" fill="#f5c542"/>' % (k * 360 // rays) for k in range(rays))
    return ('<g class="spin" style="transform-origin:0px 0px;animation-duration:30s">' + r + '</g>'
            '<circle r="13" fill="#ffd45a"/><circle r="9" fill="#fff0a8" opacity=".7"/>')


def ico_tractor():
    """Realistic red tractor, side view, facing right. Ground line at y=0; spans x 0..175, about 130 tall."""
    def tyre(cx, cy, r, rim, dur, lugs=0):
        p = []
        if lugs:  # drive tyre with chunky tread lugs
            p.append('<circle r="%s" fill="#15171a"/>' % f(r - 5))
            for k in range(lugs):
                p.append('<path d="M-3.4 %sL3.4 %sL4.8 %sL-4.8 %sZ" transform="rotate(%s)" fill="#0a0b0d"/>' % (
                    f(-(r - 6)), f(-(r - 6)), f(-(r + 1)), f(-(r + 1)), f(k * 360.0 / lugs)))
            p.append('<circle r="%s" fill="none" stroke="#262a2f" stroke-width="2"/>' % f(r - 10))
        else:     # front tyre with longitudinal ribs
            p.append('<circle r="%s" fill="#15171a"/>' % f(r))
            for rr in (r - 4, r - 8):
                p.append('<circle r="%s" fill="none" stroke="#2a2e33" stroke-width="1.5"/>' % f(rr))
        p.append('<circle r="%s" fill="#e8e2cf"/><circle r="%s" fill="#d6cfb6"/>' % (f(rim), f(rim - 2.6)))
        n = 8 if lugs else 6
        for k in range(n):
            a = k * 2 * math.pi / n
            p.append('<circle cx="%s" cy="%s" r="%s" fill="#8a8470"/>' % (
                f(math.cos(a) * rim * .64), f(math.sin(a) * rim * .64), f(max(1.1, rim * .08))))
        p.append('<circle r="%s" fill="#c4302b"/><circle r="%s" fill="#7e1d1a"/>' % (f(rim * .36), f(rim * .15)))
        return ('<g transform="translate(%s %s)"><g class="spin" style="transform-origin:0px 0px;animation-duration:%ss">%s</g></g>'
                % (f(cx), f(cy), f(dur), "".join(p)))

    defs = (
        '<defs>'
        '<linearGradient id="trRed" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e0524a"/><stop offset=".45" stop-color="#c4302b"/><stop offset="1" stop-color="#8f2420"/></linearGradient>'
        '<linearGradient id="trGlass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#d4eef6"/><stop offset=".55" stop-color="#8cc3d6"/><stop offset="1" stop-color="#5e9fb8"/></linearGradient>'
        '<linearGradient id="trRoof" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6f1e2"/><stop offset="1" stop-color="#cfc8b2"/></linearGradient>'
        '</defs>')
    hitch = ('<path d="M36 -30L5 -24M40 -62L9 -50" stroke="#3b4046" stroke-width="4.5" stroke-linecap="round" fill="none"/>'
             '<circle cx="5" cy="-24" r="3" fill="#5b6168"/><circle cx="9" cy="-50" r="2.6" fill="#5b6168"/>')
    chassis = ('<rect x="30" y="-44" width="40" height="16" rx="7" fill="#3a3f45"/>'
               '<rect x="60" y="-33" width="108" height="7" rx="3" fill="#2b2f34"/>')
    cab = (
        '<path d="M22 -44L26 -112Q26 -119 33 -119L85 -119Q91 -119 93 -112L99 -50L99 -44Z" fill="#b32a25"/>'
        '<rect x="31" y="-110" width="58" height="60" fill="#1e2a2f"/>'
        '<path d="M33 -52V-72Q33 -75 36 -75H44V-52Z" fill="#2d3338"/>'
        '<rect x="39" y="-86" width="19" height="34" rx="8" fill="#3a6ea5"/>'
        '<circle cx="50" cy="-96" r="7.6" fill="#f0c7a2"/>'
        '<ellipse cx="50" cy="-101" rx="13" ry="3.3" fill="#e6cb86"/>'
        '<path d="M41 -101Q50 -115 59 -101Z" fill="#f0d994"/><path d="M41.6 -102.4Q50 -105.4 58.4 -102.4" stroke="#b5483a" stroke-width="2.2" fill="none"/>'
        '<path d="M62 -52L72 -74" stroke="#171a1d" stroke-width="3" stroke-linecap="round"/>'
        '<ellipse cx="73" cy="-76" rx="2.8" ry="9" transform="rotate(24 73 -76)" fill="none" stroke="#171a1d" stroke-width="2.6"/>'
        '<path d="M55 -80L72 -77" stroke="#3a6ea5" stroke-width="5.5" stroke-linecap="round"/>'
        '<path d="M31 -52L34 -110H86L91 -52Z" fill="url(#trGlass)" opacity=".5"/>'
        '<path d="M38 -110H54L44 -52H33Z" fill="#fff" opacity=".16"/><path d="M66 -110H72L66 -52H60Z" fill="#fff" opacity=".1"/>'
        '<path d="M60 -110H64V-50H60Z" fill="#b32a25"/>'
        '<path d="M86 -110L92 -50" stroke="#b32a25" stroke-width="5"/>'
        '<rect x="15" y="-124" width="92" height="11" rx="4" fill="url(#trRoof)"/><rect x="15" y="-115" width="92" height="2.4" fill="#a9a28c" opacity=".7"/>'
        '<g class="t-beacon"><ellipse cx="62" cy="-127" rx="5.5" ry="3.2" fill="#f5a623"/></g>'
        '<path d="M92 -100L104 -97" stroke="#23272b" stroke-width="2.4"/><rect x="103" y="-105" width="4.5" height="12" rx="1.6" fill="#23272b"/>'
        '<rect x="82" y="-68" width="5.5" height="2.2" rx="1" fill="#e4dec8"/><rect x="19" y="-62" width="3.4" height="7" rx="1.2" fill="#ff5a4d"/>')
    hood = (
        '<path d="M99 -62H148Q160 -62 163 -52L166 -34Q166 -30 162 -30H99Z" fill="url(#trRed)"/>'
        '<path d="M101 -60H148Q157 -60 160 -53" fill="none" stroke="#ee7b72" stroke-width="1.8" stroke-linecap="round" opacity=".85"/>'
        '<path d="M106 -52H124M106 -47H124M106 -42H124" stroke="#85201c" stroke-width="1.6" stroke-linecap="round"/>'
        '<rect x="134" y="-52" width="15" height="5.5" rx="1.6" fill="#dcdcdc"/>'
        '<rect x="159" y="-59" width="7" height="27" rx="1.8" fill="#2b2f34"/><path d="M161 -56V-35M164 -56V-35" stroke="#6b7178" stroke-width="1"/>'
        '<circle cx="163" cy="-55" r="9" fill="#fff5c4" opacity=".22"/><circle cx="162.5" cy="-55" r="4" fill="#fff5c4" stroke="#8b9096" stroke-width="1.2"/>'
        '<rect x="131" y="-93" width="5.6" height="32" fill="#3a3f45"/><path d="M127.4 -95H140.2L138 -92H129.6Z" fill="#4a5056"/>'
        '<rect x="164" y="-43" width="9" height="13" rx="2.5" fill="#2b2f34"/>')
    front = (tyre(160, -21, 21, 11.5, 2.3)
             + '<path d="M140 -21C140 -58 180 -58 180 -21" fill="none" stroke="#b32a25" stroke-width="3.6" stroke-linecap="round"/>')
    rear = (tyre(56, -34, 35, 18.5, 3.9, lugs=18)
            + '<path d="M16 -34C16 -94 96 -94 96 -34L88 -34C88 -88 24 -88 24 -34Z" fill="#c4302b"/>'
            + '<path d="M16 -34C16 -94 96 -94 96 -34" fill="none" stroke="#ee7b72" stroke-width="1.5" opacity=".7" transform="translate(0 -.8)"/>')
    smoke = "".join('<circle cx="133.8" cy="-99" r="4.6" fill="#d8ece0" class="puff" style="animation-delay:%ss"/>' % f(-i * .9) for i in range(3))
    return (
        '<style>.puff{transform-box:fill-box;transform-origin:center;animation:puff 2.7s ease-out infinite}'
        '@keyframes puff{0%{transform:translate(0,0) scale(.4);opacity:.7}100%{transform:translate(-30px,-46px) scale(1.7);opacity:0}}'
        '.t-vib{animation:t-vib .34s ease-in-out infinite alternate}@keyframes t-vib{from{transform:translateY(0)}to{transform:translateY(-.9px)}}'
        '.t-beacon{animation:t-beacon 1.1s steps(1) infinite}@keyframes t-beacon{0%{opacity:1}50%{opacity:.25}}</style>'
        + defs + '<g class="t-vib">' + hitch + chassis + cab + hood + front + rear + smoke + '</g>')


def ico_wheelbarrow():
    """Wheelbarrow full of produce (banner icon for the experience section)."""
    return (
        '<path d="M-6 12L-10 27M12 12L16 27" stroke="#6b4423" stroke-width="3.2" stroke-linecap="round"/>'
        '<path d="M14 -2L36 -12M14 6L36 -4" stroke="#8a5a2e" stroke-width="3.4" stroke-linecap="round"/>'
        '<path d="M-28 -6H22L13 14H-19Z" fill="#c0392b"/><path d="M-28 -6H22" stroke="#8e2a20" stroke-width="3.4" stroke-linecap="round"/>'
        '<path d="M-20 1H17" stroke="#8e2a20" stroke-width="1.6" opacity=".6"/>'
        '<circle cx="-15" cy="-11" r="7" fill="#e5483b"/><circle cx="-3" cy="-14" r="7.6" fill="#f0a732"/><circle cx="10" cy="-11" r="7" fill="#e5483b"/>'
        '<path d="M-15 -18Q-13 -23 -9 -22M-3 -21Q-1 -26 3 -25M10 -18Q12 -23 16 -22" stroke="#4cc35a" stroke-width="2" fill="none" stroke-linecap="round"/>'
        '<path d="M-33 14L-26 4" stroke="#6b4423" stroke-width="2.6" stroke-linecap="round"/>'
        '<circle cx="-33" cy="14" r="9.5" fill="#23272b"/><circle cx="-33" cy="14" r="4.6" fill="#d8d2bd"/>'
        '<path d="M-33 8.4V19.6M-38.6 14H-27.4" stroke="#8a8470" stroke-width="1.2"/>'
    )


def windmill(x, y, wheel_dur=9):
    """Farm windmill with tower base at (x, y)."""
    blades = "".join(
        '<path d="M0 -7L-3.6 -46H3.6Z" transform="rotate(%s)" fill="#ead9a8" fill-opacity=".92"/>' % f(k * 22.5)
        for k in range(16))
    lattice = ('<path d="M-12 0L-5 -88M12 0L5 -88" stroke="#a8b8a8" stroke-width="3" fill="none"/>'
               '<path d="M-10 -10L9 -34M10 -10L-9 -34M-8 -34L7 -58M8 -34L-7 -58M-6 -58L5 -80M6 -58L-5 -80" stroke="#7d8f7e" stroke-width="1.6"/>')
    return (
        '<g transform="translate(%s %s)">%s'
        '<rect x="-7" y="-98" width="14" height="10" rx="2" fill="#7d8f7e"/>'
        '<path d="M6 -94L44 -94L38 -104L44 -94L38 -84Z" fill="#c8d6c8"/>'
        '<g transform="translate(0 -94)"><g class="spin" style="transform-origin:0px 0px;animation-duration:%ss">'
        '%s<circle r="47" fill="none" stroke="#bfa56a" stroke-width="1.5" opacity=".7"/><circle r="5" fill="#8a7a4a"/></g></g></g>'
        % (f(x), f(y), lattice, f(wheel_dur), blades)
    )


def rng(seed):
    return random.Random(seed)
