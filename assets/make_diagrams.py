"""Generate the README diagrams as static SVGs — light + dark pair per diagram.

Why not mermaid: GitHub renders every ```mermaid block with its own pan/zoom toolbar in the
corner. Nothing in markdown turns that off, so the diagrams are committed as images and
referenced through <picture> + prefers-color-scheme, which GitHub supports natively.

    python assets/make_diagrams.py        # rewrites assets/*.svg
"""
from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).resolve().parent

FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"

THEMES = {
    "light": dict(fill="#f6f8fa", stroke="#d0d7de", title="#1f2328",
                  sub="#59636e", accent="#0969da", arrow="#8c959f", note="#6e7781"),
    "dark":  dict(fill="#161b22", stroke="#30363d", title="#e6edf3",
                  sub="#8b949e", accent="#58a6ff", arrow="#6e7681", note="#7d8590"),
}


def box(x, y, w, h, title, lines, t, *, num=None, lead=17, title_size=14, sub_size=11.5):
    """A rounded box: bold title, then muted lines under it."""
    cx = x + w / 2
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
           f'fill="{t["fill"]}" stroke="{t["stroke"]}" stroke-width="1.2"/>']
    ty = y + 27
    label = title if num is None else f"{num}&#160;&#160;{title}"
    out.append(f'<text x="{cx}" y="{ty}" text-anchor="middle" font-family="{FONT}" '
               f'font-size="{title_size}" font-weight="600" fill="{t["title"]}">{label}</text>')
    for i, line in enumerate(lines):
        out.append(f'<text x="{cx}" y="{ty + 22 + i * lead}" text-anchor="middle" '
                   f'font-family="{FONT}" font-size="{sub_size}" fill="{t["sub"]}">{line}</text>')
    return "\n  ".join(out)


def arrow(x1, y1, x2, y2, t, dashed=False, path=None):
    d = path or f"M{x1},{y1} L{x2},{y2}"
    dash = ' stroke-dasharray="4 4"' if dashed else ""
    return (f'<path d="{d}" fill="none" stroke="{t["arrow"]}" stroke-width="1.4"'
            f'{dash} marker-end="url(#a)"/>')


def svg(w, h, body, t):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" '
            f'height="{h}" role="img">\n'
            f'  <defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
            f'markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,1 L9,5 L0,9 z" fill="{t["arrow"]}"/></marker></defs>\n'
            f'  {body}\n</svg>\n')


# ── 1. four layers ────────────────────────────────────────────────────────────
def four_layer(t):
    W, BX, Y, H = 212, [8, 230, 452, 674], 12, 112
    cells = [
        ("&#9312;", "Data", ["each agent lists its sources",
                             "history read as of that date",
                             "undeclared source &#8658; empty"]),
        ("&#9313;", "Strategy", ["mandate + parameters",
                                 "a variant inherits and",
                                 "writes only what differs"]),
        ("&#9314;", "Evaluation", ["proposer is not approver",
                                   "checks done in code",
                                   "scanned for hindsight"]),
        ("&#9315;", "Memory", ["separate per market",
                               "learns from live runs only",
                               "a person approves each lesson"]),
    ]
    parts = [box(x, Y, W, H, title, lines, t, num=num)
             for x, (num, title, lines) in zip(BX, cells)]
    for x in BX[:-1]:
        parts.append(arrow(x + W + 3, Y + H / 2, x + W + 15, Y + H / 2, t))
    back = f"M{674 + W / 2},{Y + H + 6} L{674 + W / 2},162 L{8 + W / 2},162 L{8 + W / 2},{Y + H + 8}"
    parts.append(arrow(0, 0, 0, 0, t, dashed=True, path=back))
    parts.append(f'<text x="443" y="157" text-anchor="middle" font-family="{FONT}" '
                 f'font-size="11" fill="{t["note"]}">next session&#8217;s recall</text>')
    return svg(894, 176, "\n  ".join(parts), t)


# ── 2. the harness ────────────────────────────────────────────────────────────
def harness(t):
    parts = []
    inputs = [("Session transcript", "what has happened in this run"),
              ("Session state", "the day&#8217;s inputs, frozen"),
              ("Memory", "past lessons, not raw numbers"),
              ("Policy and tools", "what it may do, and use")]
    for i, (title, sub) in enumerate(inputs):
        y = 8 + i * 58
        parts.append(box(8, y, 236, 48, title, [], t, title_size=12.5))
        parts.append(f'<text x="126" y="{y + 39}" text-anchor="middle" font-family="{FONT}" '
                     f'font-size="10.5" font-style="italic" fill="{t["sub"]}">{sub}</text>')
        parts.append(arrow(248, y + 24, 300, 122, t,
                           path=f"M248,{y + 24} C275,{y + 24} 278,122 296,122"))
    parts.append(box(302, 68, 168, 112, "Working set", ["the only thing", "the model sees"], t))
    parts.append(arrow(474, 124, 500, 124, t))
    parts.append(box(506, 68, 156, 112, "Model call", ["K independent tries", "on the same input"], t))
    parts.append(arrow(666, 124, 692, 124, t))
    parts.append(box(698, 68, 188, 112, "Saved + receipt",
                     ["what was used", "which settings", "what survived"], t))
    return svg(894, 248, "\n  ".join(parts), t)


# ── 3. crowding pipeline ──────────────────────────────────────────────────────
def crowding(t):
    parts = []
    for i, name in enumerate(["Social mentions", "Peer-group spillover",
                              "Encyclopedia pageviews"]):
        y = 12 + i * 58
        parts.append(box(8, y, 214, 44, name, [], t, title_size=12.5))
        parts.append(arrow(226, y + 22, 268, 96, t,
                           path=f"M226,{y + 22} C250,{y + 22} 252,96 264,96"))
    parts.append(box(270, 34, 196, 124, "Signal construction",
                     ["normalised to a share", "decayed over time",
                      "compared to its own base", "bot traffic excluded"], t))
    parts.append(arrow(470, 96, 496, 96, t))
    parts.append(box(502, 34, 196, 124, "Two-stage scoring",
                     ["ranked only against", "the names active that day",
                      "&#8212; the rest stay unranked"], t))
    parts.append(arrow(702, 96, 728, 96, t))
    parts.append(box(734, 34, 152, 124, "Dated file",
                     ["written once a day", "a replay reads it", "or records it missing"], t))
    return svg(894, 186, "\n  ".join(parts), t)


for name, fn in [("four-layer", four_layer), ("harness", harness), ("crowding", crowding)]:
    for theme, palette in THEMES.items():
        (OUT / f"{name}-{theme}.svg").write_text(fn(palette), encoding="utf-8")
        print(f"wrote assets/{name}-{theme}.svg")
