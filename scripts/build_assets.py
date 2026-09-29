#!/usr/bin/env python3
"""Generates the README's SVG artwork into assets/ (a dark and a light variant of each).

Run from the repo root after changing any text below:  python3 scripts/build_assets.py
Everything is self-contained SVG (no external fonts, images or services), so nothing here can
break when a third-party README-widget service goes down. Animations are CSS inside the SVG and
switch off for viewers with "reduce motion" enabled.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', Helvetica, Arial, sans-serif"

# Matches emrecancioglu.com's palette so the profile and the website read as one brand.
PALETTES = {
    "dark": dict(bg1="#0a0d12", bg2="#0e1a18", card="#11161d", card_border="#1f2a33", grid="#1a2430",
                 text="#ececea", muted="#9aa3ab", accent="#34d399", accent2="#38bdf8", accent_soft="#34d39922"),
    "light": dict(bg1="#ffffff", bg2="#ecfdf5", card="#ffffff", card_border="#d7e3dd", grid="#e3ece8",
                  text="#17181a", muted="#5b6168", accent="#059669", accent2="#0284c7", accent_soft="#05966914"),
}

REDUCED_MOTION = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"


def svg(width, height, body, style, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
            f'role="img" aria-label="{escape(title)}"><title>{escape(title)}</title>'
            f'<style>text {{ font-family: {FONT}; }} {style} {REDUCED_MOTION}</style>{body}</svg>')


def t(x, y, s, size, fill, weight=400, anchor="start", extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{escape(s)}</text>'


# ---------------------------------------------------------------- hero banner
def hero(p):
    w, h = 1200, 380
    cx, cy, r = 930, 190, 120
    nodes = ["PLC", "SCADA", "MES", "SAP", "AI", "Cloud"]
    import math
    parts = []
    for i, name in enumerate(nodes):
        a = -math.pi / 2 + i * 2 * math.pi / len(nodes)
        nx, ny = cx + r * math.cos(a), cy + r * math.sin(a)
        d = f"M{nx:.1f},{ny:.1f} L{cx},{cy}"
        parts.append(f'<path d="{d}" stroke="{p["grid"]}" stroke-width="2"/>')
        parts.append(f'<path d="{d}" stroke="{p["accent"]}" stroke-width="2.5" stroke-linecap="round" class="pulse" style="animation-delay:{i * 0.45:.2f}s"/>')
        parts.append(f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="31" fill="{p["card"]}" stroke="{p["card_border"]}" stroke-width="1.5"/>')
        parts.append(t(f"{nx:.1f}", f"{ny + 5:.1f}", name, 14, p["text"], 600, "middle"))
    network = "".join(parts)
    body = f'''
    <defs>
      <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{p["bg1"]}"/><stop offset="1" stop-color="{p["bg2"]}"/></linearGradient>
      <radialGradient id="glow" cx="0.78" cy="0.5" r="0.45"><stop offset="0" stop-color="{p["accent"]}" stop-opacity="0.22"/><stop offset="1" stop-color="{p["accent"]}" stop-opacity="0"/></radialGradient>
      <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{p["grid"]}" stroke-width="1"/></pattern>
    </defs>
    <rect width="{w}" height="{h}" rx="18" fill="url(#bg)"/>
    <rect width="{w}" height="{h}" rx="18" fill="url(#grid)" opacity="0.55"/>
    <rect width="{w}" height="{h}" rx="18" fill="url(#glow)"/>
    <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="18" fill="none" stroke="{p["card_border"]}"/>
    <g class="fade" style="animation-delay:0s">{t(64, 104, "DIGITALIZATION &amp; AI SUPERVISOR".replace("&amp;", "&"), 15, p["accent"], 700, extra='letter-spacing="3"')}</g>
    <g class="fade" style="animation-delay:.15s">{t(62, 172, "Emre Çancıoğlu", 66, p["text"], 700)}</g>
    <g class="fade" style="animation-delay:.3s">{t(64, 216, "OT Digitalization · Unified Namespace · Industrial AI", 22, p["muted"])}</g>
    <g class="fade" style="animation-delay:.45s">{t(64, 250, "@ İnci GS Yuasa · İzmir, Türkiye", 18, p["muted"])}</g>
    <g class="fade" style="animation-delay:.6s">
      <rect x="64" y="282" width="236" height="42" rx="21" fill="{p["accent_soft"]}" stroke="{p["accent"]}" stroke-opacity="0.5"/>
      {t(182, 309, "emrecancioglu.com  →", 16, p["accent"], 600, "middle")}
    </g>
    {network}
    <circle cx="{cx}" cy="{cy}" r="46" fill="{p["accent"]}" fill-opacity="0.12" class="ring"/>
    <circle cx="{cx}" cy="{cy}" r="40" fill="{p["card"]}" stroke="{p["accent"]}" stroke-width="2.5"/>
    {t(cx, cy + 6, "UNS", 18, p["accent"], 800, "middle")}
    '''
    style = """
    .pulse { stroke-dasharray: 18 400; stroke-dashoffset: 418; animation: flow 2.7s linear infinite; }
    @keyframes flow { to { stroke-dashoffset: 0; } }
    .ring { transform-origin: %dpx %dpx; animation: ring 2.4s ease-in-out infinite; }
    @keyframes ring { 0%%,100%% { transform: scale(1); opacity: .9; } 50%% { transform: scale(1.35); opacity: .2; } }
    """ % (cx, cy)
    return svg(w, h, body, style, "Emre Çancıoğlu — Digitalization & AI Supervisor, OT digitalization, Unified Namespace and industrial AI")


# ---------------------------------------------------------------- stat tiles
STATS = [("9+", "years experience"), ("3", "manufacturing plants"), ("300+", "OT data channels"),
         ("57%", "cost reduction"), ("5", "publications"), ("6", "awards")]


def stats(p):
    w, h, gap = 1200, 136, 16
    tw = (w - gap * (len(STATS) - 1)) / len(STATS)
    tiles = []
    for i, (num, label) in enumerate(STATS):
        x = i * (tw + gap)
        tiles.append(f'''<g class="fade" style="animation-delay:{i * 0.12:.2f}s">
          <rect x="{x:.1f}" y="1" width="{tw:.1f}" height="{h - 2}" rx="14" fill="{p["card"]}" stroke="{p["card_border"]}"/>
          <rect x="{x + 18:.1f}" y="1" width="36" height="3" rx="1.5" fill="{p["accent"]}"/>
          {t(f"{x + tw / 2:.1f}", 76, num, 42, p["accent"], 700, "middle")}
          {t(f"{x + tw / 2:.1f}", 106, label, 15, p["muted"], 500, "middle")}
        </g>''')
    style = ""
    return svg(w, h, "".join(tiles), style, "9+ years experience, 3 manufacturing plants, 300+ OT data channels, 57% cost reduction, 5 publications, 6 awards")


# ---------------------------------------------------------------- "what I build" cards
def icon(kind, x, y, c):
    if kind == "network":
        return (f'<g stroke="{c}" stroke-width="2.4" fill="none"><circle cx="{x}" cy="{y}" r="6"/><circle cx="{x - 14}" cy="{y + 12}" r="4"/>'
                f'<circle cx="{x + 14}" cy="{y + 12}" r="4"/><circle cx="{x}" cy="{y - 15}" r="4"/>'
                f'<path d="M{x - 4},{y + 4}L{x - 11},{y + 9}M{x + 4},{y + 4}L{x + 11},{y + 9}M{x},{y - 6}L{x},{y - 11}"/></g>')
    if kind == "eye":
        return (f'<g stroke="{c}" stroke-width="2.4" fill="none"><path d="M{x - 17},{y} Q{x},{y - 15} {x + 17},{y} Q{x},{y + 15} {x - 17},{y}Z"/>'
                f'<circle cx="{x}" cy="{y}" r="5"/></g>')
    if kind == "spark":
        return (f'<path d="M{x},{y - 17} L{x + 4.5},{y - 4.5} L{x + 17},{y} L{x + 4.5},{y + 4.5} L{x},{y + 17} L{x - 4.5},{y + 4.5} '
                f'L{x - 17},{y} L{x - 4.5},{y - 4.5}Z" fill="none" stroke="{c}" stroke-width="2.4" stroke-linejoin="round"/>')
    return (f'<path d="M{x + 3},{y - 17} L{x - 9},{y + 2} L{x},{y + 2} L{x - 3},{y + 17} L{x + 9},{y - 2} L{x},{y - 2}Z" '
            f'fill="none" stroke="{c}" stroke-width="2.4" stroke-linejoin="round"/>')


CARDS = [
    ("network", "Unified Namespace & OT data", ["PLC, SCADA, MES, historian and SAP unified over", "OPC UA, MQTT and Kafka — the plant's digital twin."], "300+ data channels"),
    ("eye", "Computer vision for safety", ["YOLO models that stop robots near people (AI-ODS)", "and prevent forklift collisions at blind spots (AI-FDS)."], "4 yrs zero accidents"),
    ("spark", "GenAI & automation", ["RAG knowledge systems and multi-agent workflows", "(n8n, Copilot, GPT, Claude): day-long reports in seconds."], "25 AI projects"),
    ("bolt", "Energy & sustainability", ["200+ remote-read meters, machine-level energy and", "carbon dashboards on SAP, ML consumption forecasting."], "R² up to 0.944"),
]


def build(p):
    w, gap = 1200, 16
    cw, ch = (w - gap) / 2, 196
    h = ch * 2 + gap
    out = []
    for i, (kind, title, lines, metric) in enumerate(CARDS):
        x, y = (i % 2) * (cw + gap), (i // 2) * (ch + gap)
        mw = 22 + len(metric) * 8.6
        out.append(f'''<g class="fade" style="animation-delay:{i * 0.15:.2f}s">
          <rect x="{x + 0.5:.1f}" y="{y + 0.5:.1f}" width="{cw - 1:.1f}" height="{ch - 1}" rx="16" fill="{p["card"]}" stroke="{p["card_border"]}"/>
          <rect x="{x + 28:.1f}" y="{y + 28}" width="52" height="52" rx="14" fill="{p["accent_soft"]}"/>
          {icon(kind, round(x + 54), y + 54, p["accent"])}
          {t(f"{x + 100:.1f}", y + 62, title, 23, p["text"], 700)}
          {t(f"{x + 28:.1f}", y + 116, lines[0], 16, p["muted"])}
          {t(f"{x + 28:.1f}", y + 140, lines[1], 16, p["muted"])}
          <rect x="{x + 28:.1f}" y="{y + 156}" width="{mw:.1f}" height="28" rx="14" fill="{p["accent_soft"]}"/>
          {t(f"{x + 28 + mw / 2:.1f}", y + 175, metric, 14, p["accent"], 700, "middle")}
        </g>''')
    style = ""
    alt = "; ".join(f"{c[1]}: {' '.join(c[2])} ({c[3]})" for c in CARDS)
    return svg(w, h, "".join(out), style, alt)


# ---------------------------------------------------------------- career timeline
CAREER = [
    ("2017", "DİMES", "Part-time Project Engineer"),
    ("2018", "DVD Valves", "Software & Automation Eng."),
    ("2022", "DVD Valves", "Software & Automation Lead"),
    ("2022", "İnci GS Yuasa", "Senior OT Engineer"),
    ("2026", "İnci GS Yuasa", "Digitalization & AI Supervisor"),
]


def timeline(p):
    w, h, y0, pad = 1200, 230, 115, 150
    step = (w - 2 * pad) / (len(CAREER) - 1)
    out = [f'<line x1="{pad}" y1="{y0}" x2="{w - pad}" y2="{y0}" stroke="{p["grid"]}" stroke-width="4" stroke-linecap="round"/>',
           f'<line x1="{pad}" y1="{y0}" x2="{w - pad}" y2="{y0}" stroke="{p["accent"]}" stroke-width="4" stroke-linecap="round" class="draw"/>']
    for i, (year, org, role) in enumerate(CAREER):
        x = pad + i * step
        last = i == len(CAREER) - 1
        up = i % 2 == 0
        ty = y0 - 58 if up else y0 + 48
        if last:
            out.append(f'<circle cx="{x:.1f}" cy="{y0}" r="15" fill="{p["accent"]}" fill-opacity="0.25" class="ring" style="transform-origin:{x:.1f}px {y0}px"/>')
        out.append(f'<circle cx="{x:.1f}" cy="{y0}" r="9" fill="{p["accent"] if last else p["card"]}" stroke="{p["accent"]}" stroke-width="3" class="fade" style="animation-delay:{0.3 + i * 0.25:.2f}s"/>')
        out.append(f'''<g class="fade" style="animation-delay:{0.35 + i * 0.25:.2f}s">
          {t(f"{x:.1f}", ty, year + ("  ·  now" if last else ""), 15, p["accent"], 700, "middle")}
          {t(f"{x:.1f}", ty + 22, role, 16, p["text"], 700 if last else 600, "middle")}
          {t(f"{x:.1f}", ty + 42, org, 14, p["muted"], 400, "middle")}
        </g>''')
    style = """    .draw { stroke-dasharray: 1000; stroke-dashoffset: 1000; animation: draw 1.6s ease-out .2s forwards; }
    @keyframes draw { to { stroke-dashoffset: 0; } }
    .ring { animation: ring 2.4s ease-in-out infinite; }
    @keyframes ring { 0%,100% { transform: scale(1); opacity: .9; } 50% { transform: scale(1.6); opacity: .15; } }"""
    return svg(w, h, "".join(out), style, "Career: " + "; ".join(f"{y} {r} at {o}" for y, o, r in CAREER))


# ---------------------------------------------------------------- OT skill chips
OT = ["Siemens PLC", "Allen-Bradley", "Mitsubishi", "SCADA", "DCS", "HMI", "MES", "OPC UA", "MQTT", "Modbus TCP/RTU",
      "Profinet", "EtherNet/IP", "CC-Link", "Kepware", "Unified Namespace", "Digital Twin", "ISA-95", "IEC 62443", "SAP", "Power BI", "Grafana"]


def chips(p):
    w, ch, gx, gy, size = 1200, 38, 10, 12, 15
    x, y, out = 0.0, 0.0, []
    for i, label in enumerate(OT):
        cw = 42 + len(label) * 7.6
        if x + cw > w:
            x, y = 0.0, y + ch + gy
        out.append(f'''<g class="fade" style="animation-delay:{i * 0.04:.2f}s">
          <rect x="{x + 0.5:.1f}" y="{y + 0.5:.1f}" width="{cw - 1:.1f}" height="{ch - 1}" rx="19" fill="{p["card"]}" stroke="{p["card_border"]}"/>
          <circle cx="{x + 17:.1f}" cy="{y + ch / 2:.1f}" r="3.5" fill="{p["accent"]}"/>
          {t(f"{x + 27:.1f}", f"{y + ch / 2 + 5:.1f}", label, size, p["text"], 500)}
        </g>''')
        x += cw + gx
    h = int(y + ch + 1)
    style = ""
    return svg(w, h, "".join(out), style, "OT and industrial systems: " + ", ".join(OT))


# ---------------------------------------------------------------- footer
def footer(p):
    w, h = 1200, 150
    body = f'''<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{p["accent"]}"/><stop offset="1" stop-color="{p["accent2"]}"/></linearGradient></defs>
    <path class="wave" d="M0,70 C200,20 400,120 600,70 C800,20 1000,120 1200,70 L1200,150 L0,150Z" fill="url(#g)" opacity="0.18"/>
    <path d="M0,95 C200,55 400,135 600,95 C800,55 1000,135 1200,95 L1200,150 L0,150Z" fill="url(#g)" opacity="0.9"/>
    {t(600, 34, "“Be the change that you want to see in the world.”", 18, p["muted"], 400, "middle", 'font-style="italic"')}'''
    style = """.wave { animation: sway 6s ease-in-out infinite alternate; }
    @keyframes sway { to { transform: translateX(-40px); } }"""
    return svg(w, h, body, style, "Be the change that you want to see in the world.")


def main():
    OUT.mkdir(exist_ok=True)
    for name, fn in [("hero", hero), ("stats", stats), ("build", build), ("timeline", timeline), ("ot", chips), ("footer", footer)]:
        for mode, palette in PALETTES.items():
            (OUT / f"{name}-{mode}.svg").write_text(fn(palette), encoding="utf-8")
    print(f"wrote {len(list(OUT.glob('*.svg')))} files to {OUT}")


if __name__ == "__main__":
    main()
