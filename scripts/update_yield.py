#!/usr/bin/env python3
"""Refresh the live farm "crop yield" graph and the repository table.

    python3 scripts/update_yield.py                 # uses $GITHUB_TOKEN if set, else public pages
    python3 scripts/update_yield.py --login someone --dump data.json
    python3 scripts/update_yield.py --fixture data.json   # render offline from a dump

Writes  assets/yield.svg                      (contribution "fields": a grass tuft per active day)
Updates README.md between <!-- REPOS:START --> and <!-- REPOS:END --> (if the markers exist).

Pure standard library; designed to run inside the scheduled GitHub Action.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from farmlib import (P, f, svg_doc, text, text_width, cap_height, wheat, tuft, ico_wheat_bundle,  # noqa: E402
                     ico_sprout_big, ico_sunflower, ico_barn, ico_tractor, catmull, hill_path, rng)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_LOGIN = "monishrajax"

# Hand-written one-liners for the repo table (anything not listed falls back to the GitHub description).
REPO_NOTES = {
    "normalize-website": ("Storefront for a single-product launch with Razorpay checkout", "React · Express · Supabase"),
    "Dont-touch-the-ground": ("Prison-break arcade platformer with multiplayer races", "JavaScript · Canvas"),
    "visa": ("VisaGuard: agentic-AI PCI / PII compliance platform demo", "Next.js · TypeScript"),
    "Smart-Resume-Job-Matching-Information-Retrieval-System": ("Ranks resumes against a job description (TF-IDF + cosine)", "Flask · React · scikit-learn"),
    "ID-scanner": ("OCR attendance scanner for student IDs", "React · Tesseract.js · Supabase"),
    "microservices-ci-cd": ("Commit → build → Docker → Kubernetes delivery pipeline", "GitHub Actions · Docker · K8s"),
}


# ------------------------------------------------------------------- http ---
def http(url, token=None, data=None, accept="application/vnd.github+json", retries=3):
    headers = {"User-Agent": "farm-yield-bot", "Accept": accept}
    if token:
        headers["Authorization"] = "Bearer " + token
    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=body, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as err:
            last = err
            if err.code in (429, 500, 502, 503, 504):
                time.sleep(2 * (attempt + 1))
                continue
            raise
        except urllib.error.URLError as err:
            last = err
            time.sleep(2 * (attempt + 1))
    raise last


# ------------------------------------------------------------ data sources ---
GQL_YEARS = "query($login:String!){user(login:$login){createdAt contributionsCollection{contributionYears}}}"
GQL_YEAR = ("query($login:String!,$from:DateTime!,$to:DateTime!){user(login:$login){contributionsCollection(from:$from,to:$to)"
            "{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}")


def gql(query, variables, token):
    out = json.loads(http("https://api.github.com/graphql", token, {"query": query, "variables": variables}))
    if out.get("errors") or not (out.get("data") or {}).get("user"):
        raise RuntimeError("GraphQL error: " + json.dumps(out)[:300])
    return out["data"]["user"]


def calendar_graphql(login, token, now):
    years = sorted(gql(GQL_YEARS, {"login": login}, token)["contributionsCollection"]["contributionYears"])
    days = {}
    for y in years:
        frm = "%d-01-01T00:00:00Z" % y
        to = "%d-12-31T23:59:59Z" % y if y < now.year else now.strftime("%Y-%m-%dT%H:%M:%SZ")
        cal = gql(GQL_YEAR, {"login": login, "from": frm, "to": to}, token)["contributionsCollection"]["contributionCalendar"]
        for week in cal["weeks"]:
            for d in week["contributionDays"]:
                days[d["date"]] = int(d["contributionCount"])
    return days


def parse_calendar_html(page, lo, hi):
    """Parse GitHub's public contribution-calendar HTML fragment -> {date: count}."""
    cells = {}
    for m in re.finditer(r"<td\b[^>]*>", page):
        tag = m.group(0)
        d = re.search(r'data-date="(\d{4}-\d{2}-\d{2})"', tag)
        i = re.search(r'\bid="([^"]+)"', tag)
        if d and i:
            cells[i.group(1)] = d.group(1)
    days = {}
    for m in re.finditer(r'<tool-tip\b[^>]*\bfor="([^"]+)"[^>]*>([^<]*)</tool-tip>', page):
        date = cells.get(m.group(1))
        if not date or not (lo <= date <= hi):
            continue
        n = re.match(r"\s*(\d[\d,]*)\s+contribution", m.group(2))
        days[date] = int(n.group(1).replace(",", "")) if n else 0
    return days


def calendar_html(login, first_year, today):
    days = {}
    for y in range(first_year, today.year + 1):
        lo = "%d-01-01" % y
        hi = "%d-12-31" % y if y < today.year else today.isoformat()
        url = "https://github.com/users/%s/contributions?from=%s&to=%s" % (urllib.parse.quote(login), lo, hi)
        got = parse_calendar_html(http(url, accept="text/html"), lo, hi)
        if not got:
            raise RuntimeError("no calendar cells found for %d" % y)
        days.update(got)
    return days


def fetch_all(login, token, now):
    today = now.date()
    user = json.loads(http("https://api.github.com/users/" + urllib.parse.quote(login), token))
    repos = json.loads(http("https://api.github.com/users/%s/repos?per_page=100&type=owner&sort=pushed" % urllib.parse.quote(login), token))
    first_year = int(user["created_at"][:4])
    days = None
    if token:
        try:
            days = calendar_graphql(login, token, now)
        except Exception as err:  # fall back to the public page
            print("graphql failed (%s); falling back to public calendar page" % err, file=sys.stderr)
    if days is None:
        days = calendar_html(login, first_year, today)
    slim = [{k: r.get(k) for k in ("name", "description", "html_url", "homepage", "language", "fork", "pushed_at", "archived")} for r in repos]
    return {"login": login, "public_repos": user["public_repos"], "days": days, "repos": slim,
            "fetched": now.strftime("%Y-%m-%dT%H:%M:%SZ")}


# -------------------------------------------------------------------- stats ---
def compute(days, today):
    one = dt.timedelta(days=1)
    d = today if days.get(today.isoformat(), 0) > 0 else today - one  # today may still be empty
    cur = 0
    while days.get(d.isoformat(), 0) > 0:
        cur += 1
        d -= one
    longest = run = 0
    if days:
        d = dt.date.fromisoformat(min(days))
        while d <= today:
            run = run + 1 if days.get(d.isoformat(), 0) > 0 else 0
            longest = max(longest, run)
            d += one
    start = today - dt.timedelta(days=364)
    total = sum(c for k, c in days.items() if start.isoformat() <= k <= today.isoformat())
    return {"current": cur, "longest": longest, "total": total, "start": start}


def thresholds(days, start, today):
    vals = sorted(c for k, c in days.items() if c > 0 and start.isoformat() <= k <= today.isoformat())
    if not vals:
        return (1, 2, 3)

    def q(p):
        return vals[min(len(vals) - 1, int(p * (len(vals) - 1) + 0.5))]
    return (q(.25), q(.5), q(.75))


def level_of(count, thr):
    if count <= 0:
        return 0
    return 1 if count <= thr[0] else 2 if count <= thr[1] else 3 if count <= thr[2] else 4


# ---------------------------------------------------------------- rendering ---
GRASS = {
    1: ('<path d="M8 13.5V9.2" stroke="#53c26a" stroke-width="1.3" stroke-linecap="round"/>'
        '<path d="M8 9.6C5.2 9.8 3.8 8.2 3.6 6.2C6.2 6.1 7.9 7.5 8 9.6Z" fill="#6fd47f"/>'
        '<path d="M8 10.6C10.8 10.8 12.2 9.2 12.4 7.2C9.8 7.1 8.1 8.5 8 10.6Z" fill="#4bb862"/>'),
    2: ('<path d="M4.6 13.5C4.4 10.2 4 8 3 5.5C5.6 7.2 6.6 10 6.6 13.5Z" fill="#3fa557"/>'
        '<path d="M7 13.5C7 9.5 7.2 6.2 8 2.8C8.8 6.2 9 9.5 9 13.5Z" fill="#6fd47f"/>'
        '<path d="M9.4 13.5C9.4 10 10.4 7.2 13 5.2C12.4 8 12 10.5 11.6 13.5Z" fill="#4bb862"/>'),
    3: ('<path d="M3 13.5C2.8 10.8 2.2 9 1.4 7C3.8 8.4 4.8 10.6 4.8 13.5Z" fill="#3fa557"/>'
        '<path d="M5 13.5C5 10 5.4 6.8 5.8 4.2C7 7 7.2 10 7 13.5Z" fill="#4bb862"/>'
        '<path d="M7.2 13.5C7.2 9 7.4 5.6 8 2C8.7 5.6 8.9 9 8.9 13.5Z" fill="#8fe05a"/>'
        '<path d="M9.1 13.5C9 10 9.2 7 10.2 4.4C10.8 7.2 11 10 11 13.5Z" fill="#5fd06f"/>'
        '<path d="M11.2 13.5C11.2 10.6 12 8.4 14.6 7C13.8 9 13.2 10.8 13 13.5Z" fill="#3fa557"/>'),
    4: ('<path d="M3 13.5C2.8 10.8 2.2 9 1.4 7C3.8 8.4 4.8 10.6 4.8 13.5Z" fill="#5fd06f"/>'
        '<path d="M5 13.5C5 10 5.4 6.8 5.8 4.2C7 7 7.2 10 7 13.5Z" fill="#8fe05a"/>'
        '<path d="M7.2 13.5C7.2 9 7.4 5.6 8 2C8.7 5.6 8.9 9 8.9 13.5Z" fill="#c8f26b"/>'
        '<path d="M9.1 13.5C9 10 9.2 7 10.2 4.4C10.8 7.2 11 10 11 13.5Z" fill="#8fe05a"/>'
        '<path d="M11.2 13.5C11.2 10.6 12 8.4 14.6 7C13.8 9 13.2 10.8 13 13.5Z" fill="#5fd06f"/>'
        '<ellipse cx="8" cy="2.6" rx=".95" ry="1.9" fill="#f5c542"/><ellipse cx="5.8" cy="4.8" rx=".8" ry="1.5" fill="#f5c542"/>'
        '<ellipse cx="10.2" cy="5" rx=".8" ry="1.5" fill="#f5c542"/>'),
}
CELL = {  # fill, stroke per level
    0: ("#08170e", "#10301d"), 1: ("#0d2a18", "#17482a"), 2: ("#11361f", "#1f6a37"),
    3: ("#164426", "#2a8a47"), 4: ("#1b5530", "#3aa85c"),
}
MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]


def render_svg(data, today, stats):
    W, H = 1000, 410
    days = data["days"]
    thr = thresholds(days, stats["start"], today)
    start_sunday = stats["start"] - dt.timedelta(days=(stats["start"].weekday() + 1) % 7)
    cols = ((today - start_sunday).days // 7) + 1
    gx0, gx1, gy0 = 66.0, 976.0, 180.0
    pitch = (gx1 - gx0) / cols
    cell = pitch - 2.6
    k = cell / 16.0

    defs = ['<linearGradient id="pn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0a2414"/><stop offset="1" stop-color="#06180d"/></linearGradient>',
            '<linearGradient id="pl" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0f3320"/><stop offset="1" stop-color="#0a2414"/></linearGradient>',
            '<linearGradient id="gr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#14672f"/><stop offset="1" stop-color="#0c4420"/></linearGradient>']
    for lv, (fill, stroke) in CELL.items():
        defs.append('<rect id="c%d" width="%s" height="%s" rx="3" fill="%s" stroke="%s" stroke-width="1"/>' % (lv, f(cell), f(cell), fill, stroke))
    for lv, art in GRASS.items():
        defs.append('<g id="g%d">%s</g>' % (lv, art))
    css = (".sw{animation:swy 3.8s ease-in-out infinite;transform-origin:8px 14px}"
           "@keyframes swy{0%,100%{transform:rotate(-5deg)}50%{transform:rotate(5deg)}}"
           ".drv{animation:drv 24s linear infinite}@keyframes drv{from{transform:translateX(-90px)}to{transform:translateX(1040px)}}")

    b = ['<rect x="1" y="1" width="998" height="408" rx="18" fill="url(#pn)" stroke="#1b5233" stroke-width="2"/>']

    # ---- stat plates
    plates = [
        ("CONTRIBUTIONS", "{:,}".format(stats["total"]), "", "SEEDS SOWN · PAST YEAR", P["gold"], lambda: ico_wheat_bundle()),
        ("CURRENT STREAK", str(stats["current"]), "DAYS" if stats["current"] != 1 else "DAY", "DAYS GROWING IN A ROW", P["g4"], ico_sprout_big),
        ("LONGEST STREAK", str(stats["longest"]), "DAYS" if stats["longest"] != 1 else "DAY", "BEST GROWING RUN EVER", P["orange"], ico_sunflower),
        ("PUBLIC REPOS", str(data["public_repos"]), "", "FIELDS OPEN TO VISITORS", "#ff7a59", ico_barn),
    ]
    pw, gap, px0 = 226, 16, 24
    for i, (label, value, unit, sub, accent, icon) in enumerate(plates):
        x = px0 + i * (pw + gap)
        b.append('<rect x="%d" y="20" width="%d" height="116" rx="14" fill="url(#pl)" stroke="#1f6f3a" stroke-width="1.6"/>' % (x, pw))
        b.append('<path d="M%d 34Q%d 20 %d 20H%d" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round" opacity=".9"/>' % (x, x, x + 14, x + 56, accent))
        b.append(text("mono", label, x + 18, 50, 13, accent, tracking=2.4))
        b.append('<g transform="translate(%d 62) scale(.74)">%s</g>' % (x + pw - 42, icon()))
        vs = 54 if len(value) <= 4 else 44
        b.append(text("display", value, x + 18, 100, vs, P["cream"]))
        if unit:
            b.append(text("mono", unit, x + 18 + text_width("display", value, vs) + 8, 100, 16, accent, tracking=2))
        b.append(text("mono", sub, x + 18, 123, 10.5, P["mist"], tracking=1.4))

    # ---- grid labels
    prev_month, last_label_col = None, -10
    for c in range(cols):
        d0 = start_sunday + dt.timedelta(days=7 * c)
        if d0.month != prev_month:
            if c - last_label_col >= 3 or last_label_col < 0:
                if not (c == 0 and cols > 3 and (start_sunday + dt.timedelta(days=21)).month != d0.month):
                    b.append(text("mono", MONTHS[d0.month - 1], gx0 + c * pitch, 168, 11.5, P["mist"], tracking=1.2))
                    last_label_col = c
            prev_month = d0.month
    for row, label in ((1, "MON"), (3, "WED"), (5, "FRI")):
        b.append(text("mono", label, 24, gy0 + row * pitch + cell / 2 + 4, 10.5, P["mist"], tracking=1.2))

    # ---- grass cells
    r = rng(3)
    cells, glyphs = [], []
    for c in range(cols):
        for row in range(7):
            d = start_sunday + dt.timedelta(days=7 * c + row)
            if d > today:
                continue
            x, y = gx0 + c * pitch, gy0 + row * pitch
            count = days.get(d.isoformat(), 0)
            lv = level_of(count, thr)
            cells.append('<use href="#c%d" x="%s" y="%s"/>' % (lv, f(x), f(y)))
            if lv:
                glyphs.append('<g transform="translate(%s %s) scale(%s)"><use href="#g%d" class="sw" style="animation-delay:%ss"/></g>'
                              % (f(x), f(y), "%.4f" % k, lv, f(-((c * 0.09 + row * 0.04) % 3.8))))
            if d == today:
                cells.append('<rect x="%s" y="%s" width="%s" height="%s" rx="3" fill="none" stroke="%s" stroke-width="1.6"/>'
                             % (f(x - 1), f(y - 1), f(cell + 2), f(cell + 2), P["gold"]))
    b.append("".join(cells))
    b.append("".join(glyphs))

    # ---- legend + caption
    ly = gy0 + 7 * pitch + 26
    b.append(text("mono", "CROP YIELD  ·  LAST 12 MONTHS  ·  SYNCED %s UTC" % today.isoformat(), 24, ly + 4, 11, P["mist"], tracking=1.6))
    lx = 976 - (5 * (cell + 4)) - text_width("mono", "MORE", 11, 1.6) - 10
    b.append(text("mono", "LESS", lx - text_width("mono", "LESS", 11, 1.6) - 10, ly + 4, 11, P["mist"], tracking=1.6))
    for lv in range(5):
        x = lx + lv * (cell + 4)
        b.append('<use href="#c%d" x="%s" y="%s"/>' % (lv, f(x), f(ly - cell / 2 + 1)))
        if lv:
            b.append('<g transform="translate(%s %s) scale(%s)"><use href="#g%d"/></g>' % (f(x), f(ly - cell / 2 + 1), "%.4f" % k, lv))
    b.append(text("mono", "MORE", lx + 5 * (cell + 4) + 6, ly + 4, 11, P["mist"], tracking=1.6))

    # ---- farm strip (hills, wheat, a tractor tilling the yield)
    gh = catmull([(0, 372), (200, 362), (440, 370), (680, 360), (880, 368), (1000, 362)], 10)
    b.append('<g clip-path="url(#strip)"><path d="%s" fill="url(#gr)"/>' % hill_path(gh, 1000, 410))
    rows = "".join('<path d="M500 330L%d 410"/>' % xb for xb in range(-900, 1900, 70))
    b.append('<g stroke="#0b4a20" stroke-width="2.4" opacity=".7">%s</g>' % rows)
    b.append('<g transform="translate(0 404) scale(.36)"><g class="drv">%s</g></g>' % ico_tractor())
    for i in range(26):
        b.append(wheat(14 + i * 38 + r.uniform(-8, 8), 412, h=r.uniform(20, 34), lean=r.uniform(-5, 5), delay=r.uniform(0, 4), dur=r.uniform(3.8, 5.6)))
    for i in range(18):
        b.append(tuft(r.uniform(0, 1000), 412, s=r.uniform(.5, .9), delay=r.uniform(0, 4)))
    b.append("</g>")
    defs.append('<clipPath id="strip"><path d="M1 340H999V391Q999 409 981 409H19Q1 409 1 391Z"/></clipPath>')

    title = ("Crop yield: %s contributions in the last 12 months, current streak %d days, longest streak %d days, %s public repos"
             % ("{:,}".format(stats["total"]), stats["current"], stats["longest"], data["public_repos"]))
    return svg_doc(W, H, "".join(b), "".join(defs), css, title)


# --------------------------------------------------------------- repo table ---
def repo_table(repos, skip=()):
    rows = ["| Repo | What's growing | Stack | Live | Updated |", "|:--|:--|:--|:--:|:--:|"]
    for r in repos:
        if r["name"] in skip or r.get("archived"):
            continue
        note, stack = REPO_NOTES.get(r["name"], (None, None))
        desc = note or (r.get("description") or "—")
        if r.get("fork") and not note:
            desc += " *(fork)*"
        desc = desc.replace("|", "/")
        if len(desc) > 110:
            desc = desc[:107].rstrip() + "..."
        stack = stack or r.get("language") or "—"
        live = "[open](%s)" % r["homepage"] if r.get("homepage") else "—"
        upd = (r.get("pushed_at") or "")[:10] or "—"
        rows.append("| [**%s**](%s) | %s | %s | %s | `%s` |" % (r["name"], r["html_url"], desc, stack, live, upd))
    return "\n".join(rows)


def update_readme(path, table):
    if not os.path.exists(path):
        return False
    src = open(path, encoding="utf-8").read()
    pat = re.compile(r"(<!-- REPOS:START -->)(.*?)(<!-- REPOS:END -->)", re.S)
    if not pat.search(src):
        return False
    new = pat.sub(lambda m: "%s\n%s\n%s" % (m.group(1), table, m.group(3)), src, count=1)
    if new != src:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(new)
    return True


# --------------------------------------------------------------------- main ---
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--login", default=os.environ.get("GH_LOGIN") or os.environ.get("GITHUB_REPOSITORY_OWNER") or DEFAULT_LOGIN)
    ap.add_argument("--svg", default=os.path.join(ROOT, "assets", "yield.svg"))
    ap.add_argument("--readme", default=os.path.join(ROOT, "README.md"))
    ap.add_argument("--dump", help="save the fetched data as JSON")
    ap.add_argument("--fixture", help="render from a previously dumped JSON file (no network)")
    args = ap.parse_args()

    now = dt.datetime.utcnow()
    today = now.date()
    if args.fixture:
        data = json.load(open(args.fixture, encoding="utf-8"))
    else:
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        data = fetch_all(args.login, token, now)
    if args.dump:
        with open(args.dump, "w", encoding="utf-8") as fh:
            json.dump(data, fh)

    stats = compute(data["days"], today)
    svg = render_svg(data, today, stats)
    os.makedirs(os.path.dirname(args.svg), exist_ok=True)
    with open(args.svg, "w", encoding="utf-8") as fh:
        fh.write(svg)

    own_repo = (os.environ.get("GITHUB_REPOSITORY") or "").split("/")[-1]
    skip = {own_repo, data["login"]} - {""}
    changed = update_readme(args.readme, repo_table(data["repos"], skip))
    print("login=%s total=%d current=%d longest=%d repos=%s svg=%s readme_table=%s" % (
        data["login"], stats["total"], stats["current"], stats["longest"], data["public_repos"],
        os.path.relpath(args.svg, ROOT), "updated" if changed else "no markers"))


if __name__ == "__main__":
    main()
