"""Cartoon farm animals for the README art (flat vector, CSS-animated, pure stdlib).

Every animal is drawn around the origin with its feet on y=0, facing right (+x).
Use place() to position, scale and mirror it. Animated parts rotate about explicit
pivot points, so they keep working when an animal is scaled or mirrored.
Add ANIMAL_CSS to the <style> of any SVG that uses them.
"""
from farmlib import f

ANIMAL_CSS = (
    ".a-tail{animation:a-tail 2.6s ease-in-out infinite}"
    "@keyframes a-tail{0%,100%{transform:rotate(-9deg)}50%{transform:rotate(11deg)}}"
    ".a-wag{animation:a-wag .45s ease-in-out infinite}"
    "@keyframes a-wag{0%,100%{transform:rotate(-26deg)}50%{transform:rotate(22deg)}}"
    ".a-graze{animation:a-graze 7s ease-in-out infinite}"
    "@keyframes a-graze{0%,8%,100%{transform:rotate(0)}22%,52%{transform:rotate(46deg)}68%{transform:rotate(0)}}"
    ".a-nod{animation:a-nod 3.6s ease-in-out infinite}"
    "@keyframes a-nod{0%,100%{transform:rotate(0)}50%{transform:rotate(9deg)}}"
    ".a-peckb{animation:a-peckb 2.8s ease-in-out infinite}"
    "@keyframes a-peckb{0%,100%{transform:rotate(0)}10%,18%{transform:rotate(26deg)}26%{transform:rotate(4deg)}34%,42%{transform:rotate(26deg)}52%{transform:rotate(0)}}"
    ".a-peckh{animation:a-peckh 2.8s ease-in-out infinite}"
    "@keyframes a-peckh{0%,100%{transform:rotate(0)}10%,18%{transform:rotate(34deg)}26%{transform:rotate(6deg)}34%,42%{transform:rotate(34deg)}52%{transform:rotate(0)}}"
    ".a-hop{animation:a-hop 1.5s ease-in-out infinite}"
    "@keyframes a-hop{0%,100%{transform:translateY(0)}45%{transform:translateY(-4px)}}"
    ".a-waddle{animation:a-waddle 1.3s ease-in-out infinite}"
    "@keyframes a-waddle{0%,100%{transform:rotate(-4deg)}50%{transform:rotate(4deg)}}"
    ".a-crow{animation:a-crow 5s ease-in-out infinite}"
    "@keyframes a-crow{0%,52%,100%{transform:rotate(0)}60%,78%{transform:rotate(-20deg)}}"
    ".a-snd{animation:a-snd 5s ease-in-out infinite}"
    "@keyframes a-snd{0%,56%,100%{opacity:0}62%,76%{opacity:1}}"
)


def _a(cls, ox, oy, d=0.0):
    """class + style for an animated part rotating about (ox, oy) in local coordinates."""
    return 'class="%s" style="transform-origin:%spx %spx;animation-delay:%ss"' % (cls, f(ox), f(oy), f(-d))


def place(fragment, x, y, s=1.0, flip=False):
    """Put an animal with its feet at (x, y), scaled by s, optionally mirrored to face left."""
    return '<g transform="translate(%s %s) scale(%s %s)">%s</g>' % (f(x), f(y), f(-s if flip else s), f(s), fragment)


def cow(d=0.0):
    W, S, PK, K = "#f7f3ea", "#e2dccf", "#f3b5ae", "#2a2420"
    tail = (f'<g {_a("a-tail", -37, -47, d)}><path d="M-37 -47C-48 -44 -50 -30 -47 -15" fill="none" stroke="{K}" stroke-width="3.2" stroke-linecap="round"/>'
            f'<path d="M-47 -15c-4-3-2-9 1-10c4 2 5 7 3 11z" fill="{K}"/></g>')
    legs = (f'<rect x="-33" y="-28" width="8" height="28" rx="3" fill="{S}"/><rect x="-34" y="-7" width="10" height="7" rx="2.5" fill="{K}"/>'
            f'<rect x="14" y="-28" width="8" height="28" rx="3" fill="{S}"/><rect x="13" y="-7" width="10" height="7" rx="2.5" fill="{K}"/>'
            f'<rect x="-21" y="-28" width="8" height="28" rx="3" fill="{W}"/><rect x="-22" y="-7" width="10" height="7" rx="2.5" fill="{K}"/>'
            f'<rect x="26" y="-28" width="8" height="28" rx="3" fill="{W}"/><rect x="25" y="-7" width="10" height="7" rx="2.5" fill="{K}"/>')
    udder = f'<ellipse cx="2" cy="-21" rx="8" ry="5" fill="{PK}"/>'
    body = f'<rect x="-40" y="-62" width="80" height="42" rx="18" fill="{W}"/>'
    patches = (f'<path d="M-31 -52c4-9 15-9 17 0c2 8-6 13-12 11c-4-2-7-6-5-11z" fill="{K}"/>'
               f'<path d="M-3 -42c2-7 12-8 14-1c2 6-3 11-9 10c-4-1-6-5-5-9z" fill="{K}"/>'
               f'<path d="M17 -58c5-4 14-2 14 4c0 5-6 8-11 7c-4-1-6-6-3-11z" fill="{K}"/>')
    head = (f'<g {_a("a-graze", 34, -48, d)}>'
            f'<ellipse cx="42" cy="-46" rx="14" ry="17" transform="rotate(-18 42 -46)" fill="{W}"/>'
            f'<ellipse cx="58" cy="-45" rx="15" ry="12.5" fill="{W}"/>'
            f'<path d="M49 -56c6-5 15-3 15 3c-4 4-11 5-16 2z" fill="{K}"/>'
            f'<ellipse cx="69" cy="-41" rx="8.5" ry="7.5" fill="{PK}"/>'
            f'<circle cx="71" cy="-42" r="1.3" fill="#c9857e"/><circle cx="66.5" cy="-40" r="1.3" fill="#c9857e"/>'
            f'<circle cx="59" cy="-49" r="2.2" fill="#1a1512"/><circle cx="59.8" cy="-49.8" r=".7" fill="#fff"/>'
            f'<ellipse cx="48" cy="-57" rx="8" ry="3.6" transform="rotate(-30 48 -57)" fill="{K}"/>'
            f'<path d="M53 -59q-1-8 -8-10q2 6 3 10z" fill="#eadfae"/></g>')
    return tail + legs + udder + body + patches + head


def sheep(d=0.0):
    WL, SH, K = "#f4f0e6", "#d8d0bd", "#2c2622"
    legs = "".join(f'<rect x="{x}" y="-17" width="5" height="17" rx="2" fill="{K}"/>' for x in (-16, -7, 9, 18))
    shade = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{SH}"/>' for x, y, r in [(-14, -22, 13), (0, -25, 15), (15, -22, 13), (-6, -16, 12), (8, -16, 12)])
    wool = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{WL}"/>' for x, y, r in [(-14, -27, 13), (0, -32, 15), (15, -27, 13), (-6, -22, 13.5), (8, -22, 13.5)])
    head = (f'<g {_a("a-graze", 22, -26, d)}>'
            f'<ellipse cx="22" cy="-27" rx="4" ry="6" transform="rotate(35 22 -27)" fill="{K}"/>'
            f'<ellipse cx="31" cy="-26" rx="9.5" ry="11" transform="rotate(14 31 -26)" fill="{K}"/>'
            f'<circle cx="27" cy="-38" r="7" fill="{WL}"/>'
            f'<circle cx="35" cy="-29" r="1.8" fill="{WL}"/><circle cx="35.3" cy="-29" r=".8" fill="#111"/></g>')
    return legs + shade + wool + head


def pig(d=0.0):
    P1, P2, P3, H = "#f4aaa4", "#e68d86", "#f08f89", "#8a4a46"
    tail = f'<g {_a("a-tail", -35, -31, d)}><path d="M-35 -31c-8-2-10-9-4-11c5-1 3 6-1 5" fill="none" stroke="{P2}" stroke-width="2.6" stroke-linecap="round"/></g>'
    legs = (f'<rect x="-26" y="-17" width="10" height="17" rx="3.5" fill="{P2}"/><rect x="-27" y="-5" width="12" height="5" rx="2" fill="{H}"/>'
            f'<rect x="14" y="-17" width="10" height="17" rx="3.5" fill="{P2}"/><rect x="13" y="-5" width="12" height="5" rx="2" fill="{H}"/>'
            f'<rect x="-14" y="-17" width="10" height="17" rx="3.5" fill="{P1}"/><rect x="-15" y="-5" width="12" height="5" rx="2" fill="{H}"/>'
            f'<rect x="25" y="-17" width="10" height="17" rx="3.5" fill="{P1}"/><rect x="24" y="-5" width="12" height="5" rx="2" fill="{H}"/>')
    body = f'<ellipse cx="-1" cy="-29" rx="36" ry="20" fill="{P1}"/>'
    head = (f'<g {_a("a-nod", 28, -30, d)}>'
            f'<path d="M30 -44l5 -11l9 8z" fill="{P2}"/>'
            f'<ellipse cx="38" cy="-30" rx="15" ry="14" fill="#f6b2ac"/>'
            f'<ellipse cx="51" cy="-26" rx="8" ry="7" fill="{P3}"/>'
            f'<ellipse cx="49.5" cy="-26" rx="1.3" ry="2.2" fill="#a85b55"/><ellipse cx="53.5" cy="-26" rx="1.3" ry="2.2" fill="#a85b55"/>'
            f'<circle cx="42" cy="-35" r="2" fill="#1a1512"/></g>')
    return tail + legs + body + head


HEN_COLORS = {"white": ("#f8f3e4", "#e4d9bd", "#d4c8a4"), "brown": ("#c98545", "#a8672d", "#8a5224"), "black": ("#4a423b", "#352f2a", "#2b2622")}


def hen(kind="white", d=0.0):
    body, wing, tail = HEN_COLORS[kind]
    legs = '<path d="M-3 -10V-1M-3 -1l-5 1M-3 -1l5 0M6 -10V-1M6 -1l-5 1M6 -1l5 0" stroke="#f0a732" stroke-width="2.2" stroke-linecap="round" fill="none"/>'
    head = (f'<g {_a("a-peckh", 9, -25, d)}>'
            f'<path d="M4 -24C6 -33 11 -38 17 -38C22 -38 22 -31 18 -27C14 -23 8 -20 4 -24Z" fill="{body}"/>'
            f'<circle cx="18" cy="-38" r="7" fill="{body}"/>'
            '<circle cx="15" cy="-45" r="2.8" fill="#d6362c"/><circle cx="18.5" cy="-46.5" r="3" fill="#d6362c"/><circle cx="22" cy="-44.5" r="2.5" fill="#d6362c"/>'
            '<path d="M24.5 -39.5L31.5 -37L24.5 -34.8Z" fill="#f6b23c"/>'
            '<ellipse cx="22" cy="-31" rx="2" ry="3" fill="#d6362c"/>'
            '<circle cx="20.5" cy="-39.5" r="1.3" fill="#1a1512"/></g>')
    upper = (f'<g {_a("a-peckb", 2, -10, d)}>'
             f'<path d="M-14 -20C-24 -23 -28 -33 -25 -41C-17 -37 -11 -31 -7 -24Z" fill="{tail}"/>'
             f'<ellipse cx="0" cy="-18" rx="17" ry="12" fill="{body}"/>'
             f'<path d="M-9 -19c6-6 16-4 18 2c-4 8-16 9-22 3z" fill="{wing}"/>'
             + head + '</g>')
    return legs + upper


def rooster(d=0.0):
    legs = '<path d="M-4 -16V-1M-4 -1l-6 1.5M-4 -1l6 0M7 -16V-1M7 -1l-6 1.5M7 -1l6 0" stroke="#f0a732" stroke-width="2.8" stroke-linecap="round" fill="none"/>'
    tail = (f'<g {_a("a-tail", -14, -28, d)}>'
            '<path d="M-14 -28C-34 -26 -52 -34 -56 -50C-42 -46 -28 -38 -12 -30Z" fill="#d6362c"/>'
            '<path d="M-14 -28C-30 -30 -46 -44 -44 -62C-32 -54 -22 -44 -12 -32Z" fill="#2e8b57"/>'
            '<path d="M-14 -28C-26 -34 -36 -52 -30 -70C-22 -58 -16 -44 -10 -32Z" fill="#f0a732"/></g>')
    body = ('<ellipse cx="0" cy="-28" rx="20" ry="15" fill="#c0622a"/>'
            '<path d="M-10 -30c8-8 20-6 22 2c-5 9-19 11-26 3z" fill="#8f3f18"/>')
    head = (f'<g {_a("a-crow", 10, -38, d)}>'
            '<path d="M4 -34C6 -46 10 -56 18 -58C24 -54 24 -44 19 -38C14 -33 8 -30 4 -34Z" fill="#e8a02e"/>'
            '<circle cx="20" cy="-56" r="7.5" fill="#e8a02e"/>'
            '<circle cx="15" cy="-63" r="3.2" fill="#d6362c"/><circle cx="19.5" cy="-65.5" r="3.6" fill="#d6362c"/><circle cx="24" cy="-64" r="3.2" fill="#d6362c"/><circle cx="27" cy="-60.5" r="2.4" fill="#d6362c"/>'
            '<path d="M26.5 -58L34 -56.5L26.5 -54.8Z" fill="#f6b23c"/><path d="M26.5 -54L33 -52.4L26 -51.6Z" fill="#e3a02c"/>'
            '<ellipse cx="25.5" cy="-48.5" rx="2.6" ry="4.4" fill="#d6362c"/>'
            '<circle cx="22" cy="-58" r="1.6" fill="#1a1512"/>'
            f'<g {_a("a-snd", 10, -38, d)} fill="none" stroke="#fff3d6" stroke-width="1.8" stroke-linecap="round"><path d="M38 -64q5 6 0 12"/><path d="M43 -67q8 9 0 18"/></g>'
            '</g>')
    return legs + tail + body + head


def chick(d=0.0):
    return (f'<g {_a("a-hop", 0, 0, d)}>'
            '<path d="M-2 -5V-1M-2 -1l-3 .8M-2 -1l3 0M4 -5V-1M4 -1l-3 .8M4 -1l3 0" stroke="#f0a732" stroke-width="1.6" stroke-linecap="round" fill="none"/>'
            '<ellipse cx="0" cy="-10" rx="8.5" ry="7.5" fill="#ffd94a"/>'
            '<circle cx="6" cy="-17" r="5.6" fill="#ffd94a"/>'
            '<path d="M10.6 -17.5l4.4 1.4l-4.4 1.6z" fill="#f6a52f"/>'
            '<circle cx="7.8" cy="-18.6" r="1" fill="#1a1512"/>'
            '<path d="M-3 -11c3-3 7-1 7 2c-3 3-7 2-7-2z" fill="#f2c033"/></g>')


def duck(d=0.0):
    return (f'<g {_a("a-waddle", 0, 0, d)}>'
            '<path d="M-4 -7V-1M5 -7V-1" stroke="#f2993a" stroke-width="2.2" stroke-linecap="round"/>'
            '<path d="M-4 -1l-6 2h7zM5 -1l-6 2h7z" fill="#f2993a"/>'
            '<path d="M-18 -16c-6-2-8-8-6-12c6 0 10 4 12 8z" fill="#f0ebdc"/>'
            '<ellipse cx="0" cy="-14" rx="18" ry="10.5" fill="#fffaf0"/>'
            '<path d="M-8 -14c5-5 14-4 16 1c-4 6-13 7-18 1z" fill="#ece5d0"/>'
            '<path d="M8 -20C10 -30 14 -34 19 -34C24 -34 24 -27 21 -23C17 -19 11 -16 8 -20Z" fill="#fffaf0"/>'
            '<circle cx="17.5" cy="-31" r="7" fill="#fffaf0"/>'
            '<path d="M23 -32c5-1 9 0 10 2c-1 2-5 3-10 2z" fill="#f6a52f"/>'
            '<circle cx="20" cy="-33" r="1.3" fill="#1a1512"/></g>')


def dog(d=0.0):
    T, T2, Wh, E, K = "#c98a4b", "#b9783d", "#f7f1e5", "#7a4a24", "#2a2420"
    tail = (f'<g {_a("a-wag", -26, -26, d)}><path d="M-26 -26C-34 -30 -38 -38 -36 -46" fill="none" stroke="{T}" stroke-width="5" stroke-linecap="round"/>'
            f'<path d="M-36 -46c0-2 1-4 2-6" fill="none" stroke="{Wh}" stroke-width="5" stroke-linecap="round"/></g>')
    legs = "".join(f'<rect x="{x}" y="-18" width="6" height="18" rx="2.5" fill="{c}"/><rect x="{x - .5}" y="-5" width="7" height="5" rx="2" fill="{Wh}"/>'
                   for x, c in [(-22, T2), (-13, T), (8, T2), (17, T)])
    body = f'<rect x="-28" y="-35" width="46" height="23" rx="11" fill="{T}"/><path d="M6 -30c8 0 12 6 11 14c-7 2-13 0-15-6z" fill="{Wh}"/>'
    head = (f'<g {_a("a-nod", 18, -30, d)}>'
            f'<ellipse cx="27" cy="-34" rx="11" ry="10" fill="{T}"/>'
            f'<path d="M30 -44c3 4 3 9 1 12c-3-3-4-8-1-12z" fill="{Wh}"/>'
            f'<ellipse cx="37" cy="-31" rx="7" ry="5" fill="{Wh}"/>'
            f'<ellipse cx="42" cy="-32" rx="2.6" ry="2" fill="{K}"/>'
            f'<path d="M37 -27c0 5 4 5 4 0z" fill="#f08a8a"/>'
            f'<circle cx="31" cy="-36" r="1.7" fill="{K}"/>'
            f'<path d="M22 -43c-8 0-11 8-8 15c5-2 9-7 8-15z" fill="{E}"/></g>')
    return tail + legs + body + head


ANIMALS = {
    "cow": cow, "sheep": sheep, "pig": pig, "rooster": rooster, "chick": chick, "duck": duck, "dog": dog,
    "hen": lambda d=0.0: hen("white", d), "hen-brown": lambda d=0.0: hen("brown", d), "hen-black": lambda d=0.0: hen("black", d),
}


def animal(kind, x, y, s=1.0, flip=False, d=0.0):
    """Shortcut: an animal by name, placed with its feet at (x, y)."""
    return place(ANIMALS[kind](d), x, y, s, flip)
