#!/usr/bin/env python3
"""Render the SVG assets used by the profile README.

Every asset is written twice, as assets/<name>-dark.svg and
assets/<name>-light.svg, so the README can follow the viewer's GitHub theme.
Pull request statuses are read from the GitHub API (set GITHUB_TOKEN to avoid
rate limits), so the open source rows stay current when this runs daily.
"""
import base64
import json
import os
import pathlib
import time
import urllib.request
from html import escape

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
W = 840

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
MONO_EM = 0.61  # advance width of one monospace character, in em

THEMES = {
    "dark": dict(
        bg="#0B0E14", panel="#10141C", border="#242B37", hair="#1A202A",
        text="#E6EDF3", soft="#C2CAD3", muted="#8B949E", faint="#5C6672",
        a1="#8B6CFF", a2="#2DD4EE", a3="#F472B6",
        merged="#A371F7", open="#3FB950", closed="#8B949E",
        name1="#FFFFFF", name2="#C9C2FF", grid=0.08, glow=0.5,
    ),
    "light": dict(
        bg="#FFFFFF", panel="#F6F8FA", border="#D8DEE4", hair="#EAEEF2",
        text="#1F2328", soft="#3D444D", muted="#59636E", faint="#8C959F",
        a1="#6A48F5", a2="#0891B2", a3="#DB2777",
        merged="#8250DF", open="#1A7F37", closed="#6E7781",
        name1="#1F2328", name2="#4A36C8", grid=0.07, glow=0.2,
    ),
}

BASE_CSS = """
.sans { font-family: %s; }
.mono { font-family: %s; }
@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }
""" % (SANS, MONO)


def mono_w(text, size, spacing=0.0):
    return len(text) * (size * MONO_EM + spacing)


def svg(width, height, body, css="", defs=""):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        'width="%d" height="%d" viewBox="0 0 %d %d" fill="none">\n'
        "<style>%s%s</style>\n<defs>%s</defs>\n%s\n</svg>\n"
        % (width, height, width, height, BASE_CSS, css, defs, body)
    )


def text(x, y, s, size, fill, cls="sans", weight=400, anchor="start", spacing=0, extra=""):
    return (
        '<text x="%s" y="%s" class="%s" font-size="%s" font-weight="%s" fill="%s" '
        'text-anchor="%s" letter-spacing="%s" %s>%s</text>'
        % (x, y, cls, size, weight, fill, anchor, spacing, extra, escape(s))
    )


def chip(x, y, label, t, size=12, pad=12, h=28, border=None, color=None, dot=None):
    """A rounded tag. Returns (svg, width). y is the top edge."""
    w = mono_w(label, size) + 2 * pad + (16 if dot else 0)
    parts = [
        '<rect x="%.1f" y="%s" width="%.1f" height="%s" rx="%s" fill="%s" stroke="%s"/>'
        % (x, y, w, h, h / 2, t["panel"], border or t["border"])
    ]
    tx = x + pad
    if dot:
        cy = y + h / 2
        parts.append('<circle class="halo" cx="%.1f" cy="%s" r="4" fill="%s"/>' % (tx + 4, cy, dot))
        parts.append('<circle cx="%.1f" cy="%s" r="4" fill="%s"/>' % (tx + 4, cy, dot))
        tx += 16
    parts.append(text("%.1f" % tx, y + h / 2 + size * 0.36, label, size, color or t["soft"], "mono"))
    return "".join(parts), w


HALO_CSS = """
.halo { transform-box: fill-box; transform-origin: center; animation: halo 2.4s ease-out infinite; }
@keyframes halo { 0% { transform: scale(1); opacity: .55; } 100% { transform: scale(3); opacity: 0; } }
"""


# --- hero -------------------------------------------------------------------

def hero(t):
    h = 330
    cx, cy = 716, 150
    css = HALO_CSS + """
.b1 { animation: d1 18s ease-in-out infinite alternate; }
.b2 { animation: d2 22s ease-in-out infinite alternate; }
.b3 { animation: d3 26s ease-in-out infinite alternate; }
@keyframes d1 { to { transform: translate(-70px, 40px); } }
@keyframes d2 { to { transform: translate(50px, -40px); } }
@keyframes d3 { to { transform: translate(60px, -30px); } }
.spin { transform-origin: %dpx %dpx; animation: spin 16s linear infinite; }
.spin2 { transform-origin: %dpx %dpx; animation: spin 28s linear infinite reverse; }
@keyframes spin { to { transform: rotate(360deg); } }
.bar { transform-box: fill-box; transform-origin: center; animation: eq 1.3s ease-in-out infinite; }
@keyframes eq { 0%%, 100%% { transform: scaleY(.3); } 50%% { transform: scaleY(1); } }
""" % (cx, cy, cx, cy)
    defs = """
<clipPath id="c"><rect width="%(w)d" height="%(h)d" rx="18"/></clipPath>
<filter id="blur" x="-50%%" y="-50%%" width="200%%" height="200%%"><feGaussianBlur stdDeviation="55"/></filter>
<pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="%(text)s" opacity="%(grid)s"/></pattern>
<radialGradient id="fadeg" cx="70%%" cy="45%%" r="75%%"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>
<mask id="fade"><rect width="%(w)d" height="%(h)d" fill="url(#fadeg)"/></mask>
<linearGradient id="name" x1="0" x2="1"><stop offset="0" stop-color="%(name1)s"/><stop offset="1" stop-color="%(name2)s"/></linearGradient>
<linearGradient id="arc" x1="0" x2="1"><stop offset="0" stop-color="%(a1)s"/><stop offset="1" stop-color="%(a2)s"/></linearGradient>
""" % dict(t, w=W, h=h)
    body = [
        '<g clip-path="url(#c)">',
        '<rect width="%d" height="%d" fill="%s"/>' % (W, h, t["bg"]),
        '<g filter="url(#blur)" opacity="%s">' % t["glow"],
        '<circle class="b1" cx="640" cy="40" r="150" fill="%s"/>' % t["a1"],
        '<circle class="b2" cx="800" cy="270" r="120" fill="%s"/>' % t["a2"],
        '<circle class="b3" cx="430" cy="350" r="110" fill="%s" opacity=".55"/>' % t["a3"],
        "</g>",
        '<rect width="%d" height="%d" fill="url(#grid)" mask="url(#fade)"/>' % (W, h),
        "</g>",
        '<rect x=".5" y=".5" width="%d" height="%d" rx="18" stroke="%s"/>' % (W - 1, h - 1, t["border"]),
    ]
    # Rings with a voice waveform: a nod to Aina Ring.
    for r, o in ((52, 0.9), (78, 0.7), (104, 0.5)):
        body.append('<circle cx="%d" cy="%d" r="%d" stroke="%s" opacity="%s"/>' % (cx, cy, r, t["border"], o))
    body.append(
        '<circle class="spin" cx="%d" cy="%d" r="78" stroke="url(#arc)" stroke-width="2.5" '
        'stroke-linecap="round" stroke-dasharray="110 380"/>' % (cx, cy)
    )
    body.append('<g class="spin2"><circle cx="%d" cy="%d" r="4" fill="%s"/></g>' % (cx + 104, cy, t["a2"]))
    for i, bh in enumerate((14, 26, 40, 30, 44, 24, 12)):
        x = cx - 27 + i * 8
        body.append(
            '<rect class="bar" x="%d" y="%.1f" width="4" height="%d" rx="2" fill="url(#arc)" '
            'style="animation-delay:-%.2fs"/>' % (x, cy - bh / 2, bh, i * 0.17)
        )
    body.append(text(56, 88, "SOFTWARE ENGINEER  ·  BENGALURU, INDIA", 12.5, t["muted"], "mono", spacing=2))
    body.append(text(53, 154, "Saswat Samal", 62, "url(#name)", weight=700, spacing=-1.8))
    body.append(text(56, 198, "I build AI agents, backends and cloud", 20, t["soft"]))
    body.append(text(56, 226, "infrastructure that hold up in production.", 20, t["soft"]))
    x = 56
    for label, dot in (
        ("Open to remote roles worldwide", t["open"]),
        ("Now · Aina, AI voice agent", None),
        ("OSS · Lima · Jaeger · Dynamo", None),
    ):
        s, w = chip(x, 262, label, t, dot=dot)
        body.append(s)
        x += w + 10
    return svg(W, h, "\n".join(body), css, defs)


# --- contact pills ------------------------------------------------------------

ICONS = {
    "linkedin": '<path fill="{c}" d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 1 1 0-4.125 2.062 2.062 0 0 1 0 4.125zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>',
    "email": '<rect x="2" y="4.5" width="20" height="15" rx="3" stroke="{c}" stroke-width="2"/><path d="M3 7l9 6.5L21 7" stroke="{c}" stroke-width="2" stroke-linejoin="round"/>',
    "blog": '<path fill="{c}" d="M22.351 8.019l-6.37-6.37a5.63 5.63 0 0 0-7.962 0l-6.37 6.37a5.63 5.63 0 0 0 0 7.962l6.37 6.37a5.63 5.63 0 0 0 7.962 0l6.37-6.37a5.63 5.63 0 0 0 0-7.962zM12 15.953a3.953 3.953 0 1 1 0-7.906 3.953 3.953 0 0 1 0 7.906z"/>',
    "x": '<path fill="{c}" d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"/>',
    "resume": '<path d="M6 2.5h8l5 5v14H6z" stroke="{c}" stroke-width="2" stroke-linejoin="round"/><path d="M14 2.5v5h5M9.5 13h6M9.5 17h6" stroke="{c}" stroke-width="2" stroke-linecap="round"/>',
}


def pill(name, label, t):
    size = 13
    w = int(42 + mono_w(label, size) + 30)
    h = 38
    icon = ICONS[name].replace("{c}", t["text"])
    body = [
        '<rect x=".5" y=".5" width="%d" height="%d" rx="19" fill="%s" stroke="%s"/>' % (w - 1, h - 1, t["panel"], t["border"]),
        '<g transform="translate(15 11) scale(.667)">%s</g>' % icon,
        text(40, 23.5, label, size, t["text"], "mono", weight=600),
        text(w - 16, 23.5, "↗", 12, t["muted"], "mono", anchor="end"),
    ]
    return svg(w, h, "\n".join(body))


# --- section titles -------------------------------------------------------------

def section(num, title, t):
    size, sp = 12, 2.4
    label = "%s  %s" % (num, title.upper())
    end = 2 + mono_w(label, size, sp)
    body = [
        '<text x="2" y="25" class="mono" font-size="%s" letter-spacing="%s">'
        '<tspan fill="%s" font-weight="700">%s</tspan><tspan fill="%s">  %s</tspan></text>'
        % (size, sp, t["a1"], num, t["muted"], escape(title.upper())),
        '<line x1="%.1f" y1="21" x2="%d" y2="21" stroke="%s"/>' % (end + 14, W, t["border"]),
    ]
    return svg(W, 36, "\n".join(body))


# --- impact metrics ---------------------------------------------------------------

METRICS = [
    ("DATABASE", "1,500×", ["faster query: 30 s → 20 ms", "(was 23% of prod DB time)"]),
    ("LATENCY", "−2.4 s", ["removed from every", "voice command"]),
    ("LLM COST", "~95%", ["of prompt tokens hit", "the prompt cache"]),
    ("AGENT", "20+", ["tools the voice agent", "calls, plus MCP"]),
]


def metrics(t):
    h, gap = 146, 12
    tw = (W - 3 * gap) / 4
    defs = '<linearGradient id="num" x1="0" x2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>' % (t["a1"], t["a2"])
    body = []
    for i, (kicker, num, lines) in enumerate(METRICS):
        x = i * (tw + gap)
        body.append('<rect x="%.1f" y=".5" width="%.1f" height="%d" rx="14" fill="%s" stroke="%s"/>' % (x + 0.5, tw - 1, h - 1, t["panel"], t["border"]))
        body.append(text("%.1f" % (x + 20), 32, kicker, 10.5, t["muted"], "mono", spacing=1.6))
        body.append(text("%.1f" % (x + 19), 76, num, 34, "url(#num)", weight=700, spacing=-0.8))
        for j, line in enumerate(lines):
            body.append(text("%.1f" % (x + 20), 106 + j * 18, line, 12.5, t["muted"]))
    return svg(W, h, "\n".join(body), "", defs)


# --- career timeline ---------------------------------------------------------------

JOURNEY = [
    ("2020", "IIIT Bhubaneswar", "B.Tech, Computer Science", "2020 – 2024"),
    ("2023", "UniStack", "SDE Intern", "Nov 2023 – Sep 2024"),
    ("2024", "Badho", "Full-Stack Developer", "Oct 2024 – Nov 2025"),
    ("NOW", "Aina", "Software Engineer", "Nov 2025 – present"),
]


def journey(t):
    h = 150
    xs = [110, 317, 523, 730]
    css = HALO_CSS
    # userSpaceOnUse: a horizontal line has a zero-height box, so a bounding-box gradient would not paint.
    defs = ('<linearGradient id="line" gradientUnits="userSpaceOnUse" x1="%d" y1="48" x2="%d" y2="48">'
            '<stop offset="0" stop-color="%s" stop-opacity=".25"/><stop offset="1" stop-color="%s"/></linearGradient>'
            % (xs[0], xs[-1], t["a1"], t["a1"]))
    body = ['<line x1="%d" y1="48" x2="%d" y2="48" stroke="url(#line)" stroke-width="2"/>' % (xs[0], xs[-1])]
    for i, (year, place, role, dates) in enumerate(JOURNEY):
        x = xs[i]
        last = i == len(JOURNEY) - 1
        if last:
            body.append('<circle class="halo" cx="%d" cy="48" r="7" fill="%s"/>' % (x, t["a1"]))
            body.append('<circle cx="%d" cy="48" r="7" fill="%s"/>' % (x, t["a1"]))
        else:
            body.append('<circle cx="%d" cy="48" r="6" fill="%s" stroke="%s" stroke-width="2"/>' % (x, t["bg"], t["muted"]))
        body.append(text(x, 26, year, 11.5, t["a1"] if last else t["muted"], "mono", weight=700 if last else 400, anchor="middle", spacing=1.5))
        body.append(text(x, 86, place, 15.5, t["text"], weight=650, anchor="middle"))
        body.append(text(x, 106, role, 12.5, t["soft"], anchor="middle"))
        body.append(text(x, 126, dates, 11, t["faint"], "mono", anchor="middle"))
    return svg(W, h, "\n".join(body), css, defs)


# --- open source rows ----------------------------------------------------------------

CONTRIBUTIONS = [
    ("lima-vm/lima", 5675, "Lima", "CNCF · Go", "Shell opens the matching guest directory for remapped mounts"),
    ("lima-vm/lima", 5602, "Lima", "CNCF · Go", "Keeps the progress line intact while host agent logs stream in"),
    ("lima-vm/lima", 5771, "Lima", "CNCF · Go", "Keeps port 22 privileged so non-root users can't fake sshd"),
    ("jaegertracing/jaeger", 9930, "Jaeger", "CNCF · Go", "Retries failed Cassandra name inserts, no more 12 h gaps"),
    ("ai-dynamo/dynamo", 16127, "NVIDIA Dynamo", "LLM serving · Python", "Deprecates --mm-prompt-template, a vLLM flag that did nothing"),
    ("topoteretes/cognee", 5674, "cognee", "AI memory · Python", "Returns 409 instead of 500 for a duplicate role name"),
]


def fetch(req, attempts=3):
    for i in range(attempts):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read()
        except OSError:
            if i == attempts - 1:
                raise
            time.sleep(2 * (i + 1))


def api(path):
    req = urllib.request.Request("https://api.github.com/" + path, headers={"Accept": "application/vnd.github+json"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    return json.loads(fetch(req))


def status_of(repo, number):
    pr = api("repos/%s/pulls/%d" % (repo, number))
    if pr.get("merged_at"):
        return "merged"
    return "open" if pr["state"] == "open" else "closed"


def oss_row(repo, number, name, meta, summary, status, avatar, t):
    h = 72
    label = {"merged": "Merged", "open": "In review", "closed": "Closed"}[status]
    color = t[status]
    pw = 104
    px = W - 20 - pw
    defs = '<clipPath id="av"><rect x="20" y="20" width="32" height="32" rx="8"/></clipPath>'
    body = [
        '<rect x=".5" y=".5" width="%d" height="%d" rx="14" fill="%s" stroke="%s"/>' % (W - 1, h - 1, t["panel"], t["border"]),
        '<image x="20" y="20" width="32" height="32" clip-path="url(#av)" href="data:image/png;base64,%s" xlink:href="data:image/png;base64,%s"/>' % (avatar, avatar),
        '<rect x="20.5" y="20.5" width="31" height="31" rx="7.5" stroke="%s"/>' % t["border"],
        text(68, 32, name, 15, t["text"], weight=650),
        text(68, 52, meta, 11, t["muted"], "mono"),
        text(232, 32, summary, 13.5, t["soft"]),
        text(232, 52, "%s  #%d" % (repo, number), 11, t["faint"], "mono"),
        '<rect x="%d" y="23" width="%d" height="26" rx="13" fill="%s" fill-opacity=".14" stroke="%s" stroke-opacity=".45"/>' % (px, pw, color, color),
        '<circle cx="%d" cy="36" r="3.5" fill="%s"/>' % (px + 16, color),
        text(px + 27, 40, label, 12, color, "mono", weight=600),
    ]
    return svg(W, h, "\n".join(body), "", defs)


# --- project cards -------------------------------------------------------------------

def art_snapshell(t):
    # A shaded sphere drawn with ASCII ramps, like a webcam frame in the terminal.
    ramp = " .:-=+*#%@"
    rows = []
    for r in range(9):
        line = ""
        for c in range(15):
            dx, dy = (c - 7) / 7.0, (r - 4) / 4.2
            d = (dx * dx + dy * dy) ** 0.5
            v = 0 if d > 1 else (1 - d) * 0.85 + max(0, -dx - dy) * 0.25
            line += ramp[min(len(ramp) - 1, int(v * (len(ramp) - 1) + 0.5))]
        rows.append(line)
    parts = []
    for i, line in enumerate(rows):
        parts.append(text(0, i * 10, line, 9.5, t["a2"], "mono", extra='xml:space="preserve"'))
    css = ".scan { animation: scan 3.2s linear infinite; } @keyframes scan { from { transform: translateY(-14px); } to { transform: translateY(92px); } }"
    body = '<g transform="translate(300 40)">%s<rect class="scan" x="-4" y="0" width="96" height="6" fill="%s" opacity=".25"/></g>' % ("".join(parts), t["a2"])
    return body, css


def art_circle(t):
    css = (".draw { stroke-dasharray: 260; animation: draw 5s ease-in-out infinite; }"
           "@keyframes draw { 0% { stroke-dashoffset: 260; opacity: 1; } 30%, 88% { stroke-dashoffset: 0; opacity: 1; }"
           " 100% { stroke-dashoffset: 0; opacity: 0; } }")
    lines = "".join('<rect x="%d" y="%d" width="%d" height="4" rx="2" fill="%s" opacity=".55"/>' % (304, 48 + i * 12, w, t["muted"]) for i, w in enumerate((70, 56, 74, 48)))
    path = '<path class="draw" d="M352 44c26-6 44 8 43 26s-22 34-50 32-42-17-38-34 18-24 42-25" stroke="%s" stroke-width="2.4" stroke-linecap="round"/>' % t["a1"]
    marks = text(372, 128, "??", 22, t["a3"], "sans", weight=700, extra='font-style="italic" transform="rotate(-8 384 120)"')
    return lines + path + marks, css


def art_diary(t):
    css = (".ink { stroke-dasharray: 60; animation: ink 4.5s ease-in-out infinite; }"
           "@keyframes ink { 0% { stroke-dashoffset: 60; } 40%, 85% { stroke-dashoffset: 0; } 100% { stroke-dashoffset: 0; opacity: 0; } }"
           ".spark { transform-box: fill-box; transform-origin: center; animation: tw 2.6s ease-in-out infinite; }"
           "@keyframes tw { 0%, 100% { transform: scale(.6); opacity: .4; } 50% { transform: scale(1); opacity: 1; } }")
    book = ('<path d="M300 52c18-8 34-8 48 0v66c-14-8-30-8-48 0z" stroke="%s" stroke-width="1.6"/>'
            '<path d="M396 52c-18-8-34-8-48 0v66c14-8 30-8 48 0z" stroke="%s" stroke-width="1.6"/>') % (t["muted"], t["muted"])
    ink = "".join(
        '<path class="ink" d="M356 %d q5 -5 10 0 t10 0 t10 0" stroke="%s" stroke-width="1.8" stroke-linecap="round" style="animation-delay:%.1fs"/>'
        % (70 + i * 14, t["a1"], i * 0.4) for i in range(3)
    )
    spark = '<path class="spark" d="M392 36l3 7 7 3-7 3-3 7-3-7-7-3 7-3z" fill="%s"/>' % t["a3"]
    return '<g transform="translate(6 -10)">%s</g>' % (book + ink + spark), css


def art_vessl(t):
    css = (".box { animation: bob 3.4s ease-in-out infinite; }"
           "@keyframes bob { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-4px); } }")
    parts = []
    for i, (x, y, c) in enumerate(((304, 86, t["a1"]), (350, 86, t["a2"]), (327, 52, t["a3"]))):
        ridges = "".join('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-opacity=".7"/>' % (x + k, y + 6, x + k, y + 24, c) for k in (10, 20, 30))
        parts.append('<g class="box" style="animation-delay:-%.1fs"><rect x="%d" y="%d" width="40" height="30" rx="4" fill="%s" fill-opacity=".16" stroke="%s"/>%s</g>' % (i * 0.7, x, y, c, c, ridges))
    return "".join(parts), css


def art_telepilot(t):
    css = (".dot { animation: blink 1.4s ease-in-out infinite; }"
           "@keyframes blink { 0%, 100% { opacity: .25; } 40% { opacity: 1; } }")
    you = ('<rect x="304" y="26" width="98" height="24" rx="12" fill="%s"/>' % t["a1"]
           + text(314, 42, "make the website", 8.5, "#FFFFFF", "mono"))
    typing = '<rect x="296" y="58" width="54" height="24" rx="12" fill="%s" stroke="%s"/>' % (t["bg"], t["border"])
    typing += "".join('<circle class="dot" cx="%d" cy="70" r="2.6" fill="%s" style="animation-delay:%.2fs"/>' % (311 + i * 12, t["muted"], i * 0.2) for i in range(3))
    done = ('<rect x="296" y="90" width="106" height="24" rx="12" fill="%s" stroke="%s"/>' % (t["bg"], t["border"])
            + text(306, 106, "✓ done, 19 images", 8.5, t["open"], "mono"))
    return you + typing + done, css


def art_button(t):
    css = (".key { animation: press 3s ease-in-out infinite; }"
           "@keyframes press { 0%, 22%, 100% { transform: translateY(0); } 8% { transform: translateY(3px); } }")
    parts = []
    for i, c in enumerate((t["a3"], t["a2"], t["open"])):
        x = 298 + i * 38
        parts.append(
            '<g class="key" style="animation-delay:%.1fs">'
            '<rect x="%d" y="52" width="30" height="30" rx="7" fill="%s" stroke="%s"/>'
            '<rect x="%d" y="52" width="30" height="26" rx="7" fill="%s" stroke="%s"/>'
            '<circle cx="%d" cy="65" r="5" fill="%s"/></g>'
            % (i, x, t["border"], t["border"], x, t["panel"], t["border"], x + 15, c)
        )
    return "".join(parts), css


PROJECTS = {
    "snapshell": ("GO · WEBRTC · OPENCV", "SnapShell", [
        "Video calls between two terminals. It",
        "streams your webcam as ASCII art over",
        "WebRTC in under 100 ms. On Homebrew.",
    ], ["Go", "WebRTC", "OpenCV", "Redis"], art_snapshell),
    "circle": ("RUST · PYTHON · CLAUDE", "Circle to Explain", [
        "What if your notebook could explain",
        "itself? Circle a paragraph, draw ??,",
        "and Claude handwrites the answer.",
    ], ["Rust", "Python", "Claude", "SSE"], art_circle),
    "diary": ("PYTHON · RUST · CLAUDE", "Enchanted Diary", [
        "A handwritten diary on an e-ink",
        "tablet, backed by Claude over an SSE",
        "API, with a Spotify player in Rust.",
    ], ["Python", "Rust", "Claude", "SSH"], art_diary),
    "telepilot": ("TYPESCRIPT · MCP · TELEGRAM", "telepilot", [
        "Text any Claude Code session from",
        "Telegram or iMessage. It works on your",
        "Mac, and nothing runs without your yes.",
    ], ["TypeScript", "MCP", "Telegram", "iMessage"], art_telepilot),
    "vessl": ("GO · DOCKER", "Vessl", [
        "Docker from one fast CLI: containers,",
        "images, live stats, logs and exec.",
        "Built with Go and Cobra, on Homebrew.",
    ], ["Go", "Docker", "Cobra", "Homebrew"], art_vessl),
    "button": ("HARDWARE · AI AGENTS", "Food Button", [
        "A Mac key that orders my dinner: KFC",
        "when the brain is off, pizza after a",
        "long day, salad when the guilt hits.",
    ], ["Dune", "AI agents", "Hardware"], art_button),
}


def card(key, t):
    w, h = 414, 232
    kicker, title, lines, chips, art = PROJECTS[key]
    art_body, art_css = art(t)
    defs = '<radialGradient id="glow" cx="85%" cy="20%" r="60%"><stop offset="0" stop-color="{0}" stop-opacity=".22"/><stop offset="1" stop-color="{0}" stop-opacity="0"/></radialGradient>'.format(t["a1"])
    body = [
        '<rect x=".5" y=".5" width="%d" height="%d" rx="16" fill="%s" stroke="%s"/>' % (w - 1, h - 1, t["panel"], t["border"]),
        '<rect x=".5" y=".5" width="%d" height="%d" rx="16" fill="url(#glow)"/>' % (w - 1, h - 1),
        art_body,
        text(24, 38, kicker, 10.5, t["muted"], "mono", spacing=1.6),
        text(24, 70, title, 22, t["text"], weight=700, spacing=-0.4),
    ]
    for i, line in enumerate(lines):
        body.append(text(24, 104 + i * 20, line, 13.5, t["soft"]))
    x = 24
    for label in chips:
        s, cw = chip(x, 182, label, t, size=11, pad=10, h=26)
        body.append(s)
        x += cw + 8
    return svg(w, h, "\n".join(body), art_css, defs)


# --- toolkit ---------------------------------------------------------------------

STACK = [
    ("LANGUAGES", ["Python", "Go", "TypeScript", "Rust", "SQL", "Bash", "C++"], False),
    ("AI", ["LLM agents", "Tool calling", "MCP", "RAG", "pgvector", "Prompt caching", "Claude", "OpenAI"], True),
    ("BACKEND", ["FastAPI", "Celery", "SQLAlchemy", "Node.js", "Temporal", "PostgreSQL", "Redis", "MongoDB"], False),
    ("CLOUD & OPS", ["AWS: ECS, RDS, Kinesis, Glue, Athena", "Azure", "Docker", "GitHub Actions", "Prometheus", "Grafana", "OpenTelemetry", "Linux"], False),
]


def toolkit(t):
    x0, y, gap, ch, size, pad = 140, 0, 7, 28, 11.5, 11
    body = []
    for label, items, accent in STACK:
        body.append(text(2, y + 18, label, 11, t["muted"], "mono", spacing=1.6))
        x = x0
        for item in items:
            cw = mono_w(item, size) + 2 * pad
            if x + cw > W:
                x = x0
                y += ch + gap
            s, _ = chip(x, y, item, t, size=size, pad=pad, border=t["a1"] if accent else None, color=t["a1"] if accent else None)
            body.append(s)
            x += cw + gap
        y += ch + 18
    return svg(W, int(y), "\n".join(body))


# --- recognition -----------------------------------------------------------------

AWARDS = [
    ("WINNER", "Hedera Hashgraph India", "Web 3.0 Hackathon"),
    ("GRAND FINALIST", "Smart India Hackathon 2022", "and the HarbourX Hackathon"),
    ("SEMI-FINALIST", "Flipkart Grid 5.0", "2023"),
    ("SCHOLAR", "Linux Foundation LiFT", "Training scholarship, 2022"),
    ("FELLOW", "MLH Prep Fellowship", "2022"),
    ("MENTEE", "Microsoft Engage", "Mentorship program"),
]


def recognition(t):
    gap, th, cols = 12, 86, 3
    tw = (W - (cols - 1) * gap) / cols
    body = []
    for i, (kicker, title, sub) in enumerate(AWARDS):
        x = (i % cols) * (tw + gap)
        y = (i // cols) * (th + gap)
        body.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%d" rx="14" fill="%s" stroke="%s"/>' % (x + 0.5, y + 0.5, tw - 1, th - 1, t["panel"], t["border"]))
        body.append('<path d="M%.1f %.1fl2.6 5.6 6 .7-4.5 4.1 1.2 6-5.3-3-5.3 3 1.2-6-4.5-4.1 6-.7z" fill="%s" opacity=".85"/>' % (x + tw - 34, y + 22, t["a1"]))
        body.append(text("%.1f" % (x + 20), y + 30, kicker, 10.5, t["a1"], "mono", weight=700, spacing=1.6))
        body.append(text("%.1f" % (x + 20), y + 54, title, 14.5, t["text"], weight=650))
        body.append(text("%.1f" % (x + 20), y + 73, sub, 12.5, t["muted"]))
    rows = (len(AWARDS) + cols - 1) // cols
    return svg(W, int(rows * th + (rows - 1) * gap), "\n".join(body))


# --- main --------------------------------------------------------------------------

def write(name, theme, content):
    (OUT / ("%s-%s.svg" % (name, theme))).write_text(content, encoding="utf-8")


def main():
    OUT.mkdir(exist_ok=True)
    statuses, avatars = {}, {}
    for repo, number, *_ in CONTRIBUTIONS:
        statuses[(repo, number)] = status_of(repo, number)
        if repo not in avatars:
            url = api("repos/" + repo)["owner"]["avatar_url"]
            avatars[repo] = base64.b64encode(fetch(url + ("&" if "?" in url else "?") + "s=64")).decode()
    for theme, t in THEMES.items():
        write("hero", theme, hero(t))
        for name, label in (("linkedin", "LinkedIn"), ("email", "Email"), ("blog", "Blog"), ("x", "X"), ("resume", "Résumé")):
            write("pill-" + name, theme, pill(name, label, t))
        for num, title in (("01", "Impact at Aina"), ("02", "Journey"), ("03", "Open source"),
                           ("04", "Selected work"), ("05", "Toolkit"), ("06", "Recognition"), ("07", "Activity")):
            write("section-" + num, theme, section(num, title, t))
        write("metrics", theme, metrics(t))
        write("journey", theme, journey(t))
        # File names follow the PR, not the position, so README links stay right.
        for repo, number, name, meta, summary in CONTRIBUTIONS:
            write("oss-%s-%d" % (repo.split("/")[1], number), theme,
                  oss_row(repo, number, name, meta, summary, statuses[(repo, number)], avatars[repo], t))
        for key in PROJECTS:
            write("card-" + key, theme, card(key, t))
        write("toolkit", theme, toolkit(t))
        write("recognition", theme, recognition(t))


if __name__ == "__main__":
    main()
