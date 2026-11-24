#!/usr/bin/env python3
"""Generate original illustrative architectural sample SVGs.

These are marketing reference drawings for the Joe Mark Designs site.
They are not construction documents and do not depict a real project.
"""

import math
from pathlib import Path

OUT = Path(__file__).resolve().parent

# Blueprint sheet: luminous linework on deep navy, gold for proposed work.
NAVY = "#f4fbff"
MID = "#9fd4ea"
PAPER = "#0f2a52"
WHITE = "#14365f"
GOLD = "#e5b53b"
EXIST_FILL = "#1c5584"
EXIST_LINE = "#e7f6ff"
WASH_E = "#12345e"
WASH_P = "#3a3214"
MUTED = "#c5e4f5"
INK = "#f7fbff"

SANS = "Inter, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Cascadia Mono', ui-monospace, monospace"


def esc(value):
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


class Sheet:
    def __init__(self, w, h, title, desc):
        self.w = w
        self.h = h
        self.title = title
        self.desc = desc
        self.parts = []

    def add(self, fragment):
        self.parts.append(fragment)

    def save(self, name):
        body = "\n".join(self.parts)
        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" role="img" aria-labelledby="t d">
  <title id="t">{esc(self.title)}</title>
  <desc id="d">{esc(self.desc)}</desc>
  <defs>
    <pattern id="minor" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M20 0 H0 V20" fill="none" stroke="#1d5f8c" stroke-width="0.7"/>
    </pattern>
    <pattern id="major" width="100" height="100" patternUnits="userSpaceOnUse">
      <path d="M100 0 H0 V100" fill="none" stroke="#2f86b8" stroke-width="0.95"/>
    </pattern>
  </defs>
  <rect width="{self.w}" height="{self.h}" fill="{PAPER}"/>
  <rect width="{self.w}" height="{self.h}" fill="url(#minor)"/>
  <rect width="{self.w}" height="{self.h}" fill="url(#major)"/>
  {body}
</svg>
'''
        path = OUT / name
        path.write_text(svg)
        print(f"wrote {path} ({path.stat().st_size} bytes)")


def text(s, x, y, content, size=15, fill=INK, weight="400", anchor="start", family=None, spacing="0", extra=""):
    family = family or SANS
    s.add(
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-family="{family}" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}" letter-spacing="{spacing}" {extra}>'
        f'{esc(content)}</text>'
    )


def halo_text(s, x, y, content, size=14, fill=NAVY, anchor="middle", weight="500", rotate=None):
    transform = f' transform="rotate({rotate} {x:.1f} {y:.1f})"' if rotate is not None else ""
    s.add(
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" dominant-baseline="middle" '
        f'font-family="{MONO}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
        f'stroke="{PAPER}" stroke-width="5" paint-order="stroke fill"{transform}>'
        f'{esc(content)}</text>'
    )


def rect(s, x, y, w, h, fill, stroke="none", sw=0, extra=""):
    stroke_attr = f' stroke="{stroke}" stroke-width="{sw}"' if stroke != "none" else ""
    s.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}"{stroke_attr} {extra}/>')


def line(s, x1, y1, x2, y2, stroke=NAVY, sw=1.4, extra=""):
    s.add(
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{stroke}" stroke-width="{sw}" {extra}/>'
    )


def frame(s, x, y, w, h, t, fill, stroke):
    d = (
        f"M{x:.1f},{y:.1f} h{w:.1f} v{h:.1f} h{-w:.1f} z "
        f"M{x + t:.1f},{y + t:.1f} h{w - 2 * t:.1f} v{h - 2 * t:.1f} h{-(w - 2 * t):.1f} z"
    )
    s.add(
        f'<path d="{d}" fill="{fill}" fill-rule="evenodd" stroke="{stroke}" '
        f'stroke-width="1.3" stroke-linejoin="miter"/>'
    )


def u_wall(s, x, y, w, h, t, fill=GOLD):
    """Three-sided proposed wall. Open side is the bottom (south) edge."""
    d = (
        f"M{x:.1f},{y + h:.1f} V{y:.1f} H{x + w:.1f} V{y + h:.1f} "
        f"H{x + w - t:.1f} V{y + t:.1f} H{x + t:.1f} V{y + h:.1f} Z"
    )
    s.add(f'<path d="{d}" fill="{fill}" stroke="{fill}" stroke-width="0.6" stroke-linejoin="miter"/>')


def part(s, x, y, w, h, fill=EXIST_FILL, stroke=EXIST_LINE):
    rect(s, x, y, w, h, fill, stroke, 1)


def window_h(s, x, y, w, t=8):
    rect(s, x, y - 0.4, w, t + 0.8, PAPER)
    for i, gy in enumerate((y + 1.8, y + t / 2, y + t - 1.8)):
        line(s, x + 1.6, gy, x + w - 1.6, gy, NAVY, 1.7 if i == 1 else 1.05)
    line(s, x, y, x, y + t, NAVY, 1.8)
    line(s, x + w, y, x + w, y + t, NAVY, 1.8)


def window_v(s, x, y, h, t=8):
    rect(s, x - 0.4, y, t + 0.8, h, PAPER)
    for i, gx in enumerate((x + 1.8, x + t / 2, x + t - 1.8)):
        line(s, gx, y + 1.6, gx, y + h - 1.6, NAVY, 1.7 if i == 1 else 1.05)
    line(s, x, y, x + t, y, NAVY, 1.8)
    line(s, x, y + h, x + t, y + h, NAVY, 1.8)


def opening_h(s, x, y, w, t=8):
    rect(s, x, y - 0.6, w, t + 1.2, PAPER)
    line(s, x, y, x, y + t, NAVY, 1.8)
    line(s, x + w, y, x + w, y + t, NAVY, 1.8)


def opening_v(s, x, y, h, t=8):
    rect(s, x - 0.6, y, t + 1.2, h, PAPER)
    line(s, x, y, x + t, y, NAVY, 1.8)
    line(s, x, y + h, x + t, y + h, NAVY, 1.8)


def door(s, hx, hy, length, closed_deg, cw, stroke=NAVY):
    ca = math.radians(closed_deg)
    oa = ca + (math.pi / 2 if cw else -math.pi / 2)
    cx = hx + length * math.cos(ca)
    cy = hy + length * math.sin(ca)
    ox = hx + length * math.cos(oa)
    oy = hy + length * math.sin(oa)
    sweep = 1 if cw else 0
    s.add(
        f'<path d="M{cx:.2f},{cy:.2f} A{length:.2f},{length:.2f} 0 0 {sweep} {ox:.2f},{oy:.2f}" '
        f'fill="none" stroke="{MID}" stroke-width="1.25"/>'
    )
    line(s, hx, hy, ox, oy, stroke, 1.7)


def dim_h(s, x1, x2, y, label, ext_y, size=14):
    if x2 < x1:
        x1, x2 = x2, x1
    line(s, x1, ext_y, x1, y, MID, 1)
    line(s, x2, ext_y, x2, y, MID, 1)
    line(s, x1, y, x2, y, MID, 1.1)
    for x in (x1, x2):
        line(s, x - 4.5, y + 4.5, x + 4.5, y - 4.5, NAVY, 1.4)
    halo_text(s, (x1 + x2) / 2, y - 11, label, size=size)


def dim_v(s, y1, y2, x, label, ext_x, size=14):
    if y2 < y1:
        y1, y2 = y2, y1
    line(s, ext_x, y1, x, y1, MID, 1)
    line(s, ext_x, y2, x, y2, MID, 1)
    line(s, x, y1, x, y2, MID, 1.1)
    for y in (y1, y2):
        line(s, x - 4.5, y - 4.5, x + 4.5, y + 4.5, NAVY, 1.4)
    halo_text(s, x - 12, (y1 + y2) / 2, label, size=size, rotate=-90)


def room(s, x, y, name, size_label=None, name_size=16):
    text(s, x, y, name.upper(), size=name_size, fill=NAVY, weight="650", anchor="middle", spacing="0.12em")
    if size_label:
        text(
            s, x, y + name_size - 1, size_label, size=max(12, name_size - 4),
            fill=MUTED, anchor="middle", family=MONO, weight="500",
        )


def tag(s, x, y, letter):
    s.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="10" fill="{WHITE}" stroke="{NAVY}" stroke-width="1.2"/>')
    text(s, x, y + 4, letter, size=12, fill=NAVY, weight="650", anchor="middle", family=MONO)


def north_arrow(s, x, y, scale=1):
    r = 22 * scale
    s.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{WHITE}" stroke="{NAVY}" stroke-width="1.4"/>')
    s.add(
        f'<polygon points="{x},{y - r + 4} {x + 6 * scale},{y + 2} {x},{y - 2} {x - 6 * scale},{y + 2}" fill="{NAVY}"/>'
    )
    s.add(
        f'<polygon points="{x},{y + r - 4} {x + 6 * scale},{y - 2} {x},{y + 2} {x - 6 * scale},{y - 2}" '
        f'fill="none" stroke="{NAVY}" stroke-width="1.2"/>'
    )
    text(s, x, y - r - 8, "N", size=13 * scale, fill=NAVY, weight="700", anchor="middle", family=MONO)


def scale_bar(s, x, y, px_per_ft):
    """True 0–8 ft bar. Labels sit under the bar so they stay inside the title block."""
    seg = 4 * px_per_ft
    rect(s, x, y, seg, 7, NAVY)
    rect(s, x + seg, y, seg, 7, WHITE, NAVY, 1)
    for i, label in enumerate(("0", "4", "8")):
        tx = x + i * seg
        line(s, tx, y + 7, tx, y + 11, NAVY, 1)
        text(s, tx, y + 22, label, size=11, fill=NAVY, anchor="middle", family=MONO)
    text(s, x + 2 * seg + 10, y + 13, "FT", size=11, fill=MUTED, family=MONO, spacing="0.06em")


def notes_box(s, x, y, w, title, lines, line_h=20, size=13):
    h = 34 + len(lines) * line_h + 12
    rect(s, x, y, w, h, WHITE, NAVY, 1.25)
    text(s, x + 14, y + 22, title, size=12, fill=NAVY, weight="700", family=MONO, spacing="0.14em")
    for i, row in enumerate(lines):
        text(s, x + 14, y + 44 + i * line_h, row, size=size, fill=INK)
    return h


def swatches(s, x, y, items):
    """items: list of (fill, label)."""
    cy = y
    for fill, label in items:
        rect(s, x, cy - 11, 18, 14, fill, NAVY, 1)
        text(s, x + 26, cy, label, size=13, fill=INK)
        cy += 22
    return cy


def border(s, w, h):
    s.add(f'<rect x="16" y="16" width="{w - 32}" height="{h - 32}" fill="none" stroke="{NAVY}" stroke-width="2"/>')
    s.add(f'<rect x="22" y="22" width="{w - 44}" height="{h - 44}" fill="none" stroke="{NAVY}" stroke-width="0.7"/>')


def title_block(s, w, h, sheet_no, drawing_title, px_per_ft):
    y = h - 120
    block_h = 90
    rect(s, 28, y, w - 56, block_h, WHITE, NAVY, 1.5)
    line(s, 390, y, 390, y + block_h, NAVY, 1)
    line(s, 900, y, 900, y + block_h, NAVY, 1)
    text(s, 46, y + 34, "JOE MARK DESIGNS", size=18, fill=NAVY, weight="700", spacing="0.08em")
    text(s, 46, y + 58, "Architectural Draftsman", size=13, fill=MUTED)
    text(s, 408, y + 34, drawing_title, size=16, fill=NAVY, weight="600")
    text(s, 408, y + 58, "Illustrative sample drawing. Not for construction.", size=13, fill=MUTED)
    text(s, 918, y + 26, f"SHEET  {sheet_no}", size=15, fill=NAVY, weight="700", family=MONO, spacing="0.06em")
    scale_bar(s, 918, y + 40, px_per_ft)


def toilet(s, x, y, rot=0):
    """Simple tank + bowl. x,y is top-left of an upright symbol facing down (bowl toward +y)."""
    g_open = f'<g transform="translate({x:.1f},{y:.1f}) rotate({rot})">'
    s.add(g_open)
    s.add(f'<rect x="0" y="0" width="28" height="12" rx="1.5" fill="{WHITE}" stroke="{NAVY}" stroke-width="1.4"/>')
    s.add(f'<ellipse cx="14" cy="28" rx="14" ry="16" fill="{WHITE}" stroke="{NAVY}" stroke-width="1.4"/>')
    s.add(f'<ellipse cx="14" cy="28" rx="7" ry="8" fill="none" stroke="{MID}" stroke-width="1"/>')
    s.add("</g>")


def sink_oval(s, cx, cy, rx=16, ry=11):
    s.add(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{WHITE}" stroke="{NAVY}" stroke-width="1.4"/>')
    s.add(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx * 0.45:.1f}" ry="{ry * 0.45:.1f}" fill="none" stroke="{MID}" stroke-width="1"/>')
    line(s, cx, cy - ry - 4, cx, cy - ry + 1, NAVY, 1.3)


def range_symbol(s, x, y, w, h):
    rect(s, x, y, w, h, WHITE, NAVY, 1.4)
    inset = 6
    cols = 2
    rows = 2
    for r in range(rows):
        for c in range(cols):
            cx = x + inset + (w - 2 * inset) * (c + 0.5) / cols
            cy = y + inset + (h - 2 * inset) * (r + 0.5) / rows
            s.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.2" fill="none" stroke="{NAVY}" stroke-width="1.2"/>')


def fridge(s, x, y, w, h):
    rect(s, x, y, w, h, WHITE, NAVY, 1.4)
    line(s, x + w * 0.62, y, x + w * 0.62, y + h, NAVY, 1.1)
    # door swings hinted by a small arc notch
    line(s, x + 3, y + 4, x + 3, y + h - 4, MID, 1)


def tub(s, x, y, w, h):
    rect(s, x, y, w, h, WHITE, NAVY, 1.5)
    rect(s, x + 4, y + 4, w - 8, h - 8, "none", MID, 1)
    s.add(f'<circle cx="{x + w / 2:.1f}" cy="{y + 12:.1f}" r="3.5" fill="none" stroke="{NAVY}" stroke-width="1.2"/>')


# ---------------------------------------------------------------------------
# A1 — Home addition floor plan
# ---------------------------------------------------------------------------

def build_addition():
    s = Sheet(
        1280,
        900,
        "Sample home addition floor plan",
        "Illustrative sample floor plan showing an existing house and a proposed addition. Not for construction.",
    )
    S = 16
    T = 8
    ox, oy = 140, 292
    ow, oh = 36 * S, 26 * S
    ax, ay = ox, oy - 14 * S
    aw, ah = 20 * S, 14 * S

    ix, iy = ox + T, oy + T
    ir, ib = ox + ow - T, oy + oh - T

    # floors
    rect(s, ix, iy, ir - ix, ib - iy, WASH_E)
    rect(s, ax + T, ay + T, aw - 2 * T, oy - (ay + T), WASH_P)

    # existing shell and proposed U
    frame(s, ox, oy, ow, oh, T, EXIST_FILL, EXIST_LINE)
    u_wall(s, ax, ay, aw, ah + T, T, GOLD)

    # interior partitions — existing
    # vertical at 18'-0" from interior left
    vx = ix + 18 * S
    part(s, vx, iy, T, ib - iy)
    # horizontal at 15'-0" from interior top, left of the vertical wall (living / kitchen)
    hy = iy + 15 * S
    part(s, ix, hy, vx - ix, T)
    # horizontal continuing across the right side (bed / entry+bath)
    part(s, vx + T, hy, ir - (vx + T), T)
    # bath wall, 8'-0" clear from the interior right
    bx = ir - 8 * S - T
    part(s, bx, hy + T, T, ib - (hy + T))

    # closet in bedroom, northeast, 2'-0" x 5'-0"
    closet_front = ir - 2 * S - T
    part(s, closet_front, iy, T, 2 * S)  # above door
    part(s, closet_front, iy + 2 * S + 36, T, 5 * S - 2 * S - 36)

    # openings and windows -------------------------------------------------
    # cased opening, addition to living, 8'-0"
    add_cx = ax + aw / 2
    opening_h(s, add_cx - 4 * S, oy, 8 * S, T)

    # living / kitchen cased opening 6'-0"
    opening_h(s, ix + 4 * S, hy, 6 * S, T)

    # entry door 3'-0" in south wall of entry
    entry_x1, entry_x2 = vx + T, bx
    entry_mid = (entry_x1 + entry_x2) / 2
    opening_h(s, entry_mid - 1.5 * S, ib, 3 * S, T)
    door(s, entry_mid - 1.5 * S, ib, 3 * S, 0, False)

    # bedroom door 2'-6"
    opening_h(s, entry_x1 + 16, hy, 2.5 * S, T)
    door(s, entry_x1 + 16, hy, 2.5 * S, 0, False)

    # bath door 2'-6", swings into bath
    opening_v(s, bx, hy + T + 48, 2.5 * S, T)
    door(s, bx + T, hy + T + 48, 2.5 * S, 90, False)

    # closet door
    opening_v(s, closet_front, iy + 2 * S, 36, T)
    door(s, closet_front, iy + 2 * S, 36, 90, True)

    # addition yard door, east wall, swings in
    opening_v(s, ax + aw - T, ay + 9 * S, 3 * S, T)
    door(s, ax + aw - T, ay + 9 * S, 3 * S, 90, True)

    # windows
    window_v(s, ox, iy + 28, 4 * S, T)          # A living west
    window_v(s, ox, iy + 7 * S, 4 * S, T)       # A2 living west
    window_h(s, vx + T + 5 * S, oy, 4 * S, T)   # B bedroom north
    window_v(s, ir, iy + 8 * S, 4 * S, T)       # B bedroom east
    window_v(s, ox, hy + T + 28, 4 * S, T)      # C kitchen west
    window_h(s, ix + 4 * S, ib, 4 * S, T)       # C kitchen south
    window_v(s, ir, hy + T + 70, 2.5 * S, T)    # bath
    window_h(s, ax + 6 * S, ay, 5 * S, T)       # D addition north
    window_v(s, ax, ay + 4 * S, 3.5 * S, T)     # D addition west

    # kitchen counters and fixtures
    line(s, ix + 2 * S, hy + T, ix + 2 * S, ib, MUTED, 1.4)
    line(s, ix, ib - 2 * S, vx, ib - 2 * S, MUTED, 1.4)
    sink_oval(s, ix + 6.2 * S, ib - S, 18, 11)
    range_symbol(s, ix + 6, hy + T + 36, 26, 40)
    fridge(s, vx - 3 * S, hy + T, 3 * S, 2.2 * S)

    # bath fixtures
    tub(s, ir - 2.6 * S, hy + T + 36, 2.6 * S, 5 * S)
    toilet(s, bx + T + 16, hy + T + 58)
    rect(s, bx + T, ib - 2 * S, 5 * S, 2 * S, WHITE, NAVY, 1.3)
    sink_oval(s, bx + T + 2.4 * S, ib - S, 12, 9)

    # labels
    room(s, (ix + vx) / 2, (iy + hy) / 2 - 4, "Living", "18'-0\"  ×  15'-0\"", 18)
    room(s, (vx + T + ir) / 2 - 10, (iy + hy) / 2 + 8, "Bedroom", "16'-6\"  ×  15'-0\"", 18)
    room(s, (ix + vx) / 2, (hy + T + ib) / 2 - 6, "Kitchen", "18'-0\"  ×  9'-6\"", 16)
    room(s, (entry_x1 + entry_x2) / 2, (hy + T + ib) / 2 + 8, "Entry", "8'-0\"  ×  9'-6\"", 15)
    room(s, (bx + T + ir) / 2, hy + T + 16, "Bath", "8'-0\"  ×  9'-6\"", 13)
    room(s, (closet_front + T + ir) / 2 + 2, iy + 28, "Cl.", None, 12)
    room(s, (ax + T + ax + aw - T) / 2, (ay + T + oy) / 2 - 6, "Family Room", "19'-0\"  ×  13'-6\"", 18)
    text(
        s, (ax + T + ax + aw - T) / 2, (ay + T + oy) / 2 + 28,
        "PROPOSED ADDITION", size=12, fill=NAVY, weight="700", anchor="middle",
        family=MONO, spacing="0.14em",
    )

    # window tags
    tag(s, ix + 22, iy + 28 + 2 * S, "A")
    tag(s, vx + T + 7 * S, iy + 36, "B")
    tag(s, ix + 36, hy + T + 52, "C")
    tag(s, ax + 8 * S, ay + T + 28, "D")

    # a few callouts
    halo_text(s, add_cx, oy + T + 22, "8'-0\" CASED OPENING", size=12, fill=MID)
    # dimensions
    dim_h(s, ox, ox + ow, oy + oh + 36, "36'-0\"", oy + oh, 15)
    dim_h(s, ax, ax + aw, ay - 28, "20'-0\"", ay, 15)
    dim_v(s, ay, oy, ox - 46, "14'-0\"", ax, 14)
    dim_v(s, oy, oy + oh, ox - 46, "26'-0\"", ox, 14)
    dim_v(s, ay, oy + oh, ox - 92, "40'-0\"", ax, 15)

    north_arrow(s, 760, 150)

    notes_box(
        s, 790, 78, 450, "GENERAL NOTES",
        [
            "1   Illustrative sample. Not a client project.",
            "2   Not for construction and not for permit.",
            "3   Blue poche — existing walls to remain.",
            "4   Gold poche — proposed walls.",
            "5   Overall dimensions are outside face to face.",
            "6   Room sizes are inside face to inside face.",
            "7   Verify every condition in the field.",
            "8   Structure, energy, and site items are not",
            "     designed on this sample sheet.",
        ],
    )
    swatches(
        s, 804, 340,
        [
            (EXIST_FILL, "Existing wall"),
            (GOLD, "Proposed wall"),
            (WASH_P, "Proposed floor"),
            (WASH_E, "Existing floor"),
        ],
    )
    notes_box(
        s, 790, 448, 450, "WINDOW MARKS  ·  SAMPLE",
        [
            "A    Living — 4'-0\" wide",
            "B    Bedroom — 4'-0\" wide",
            "C    Kitchen — 4'-0\" wide",
            "D    Addition — 5'-0\" wide",
            "Marks are diagrammatic. No manufacturer.",
        ],
    )
    text(s, 804, 620, "DOOR SWINGS SHOWN INTO THE ROOM.", size=12, fill=MUTED, family=MONO, spacing="0.06em")
    text(s, 804, 642, "KITCHEN FIXTURES ARE SYMBOLS ONLY.", size=12, fill=MUTED, family=MONO, spacing="0.06em")

    title_block(s, 1280, 900, "A1.0", "HOME ADDITION  —  FLOOR PLAN", S)
    border(s, 1280, 900)
    s.save("addition-plan.svg")


# ---------------------------------------------------------------------------
# A2 — ADU & garage conversion
# ---------------------------------------------------------------------------

def build_adu():
    s = Sheet(
        1280,
        900,
        "Sample ADU and garage conversion plan",
        "Illustrative sample of a one-bedroom garage conversion. Not for construction.",
    )
    S = 22  # px per foot — larger so the small building fills the sheet
    T = 11  # 6 inches
    ox, oy = 96, 58
    ow, oh = 24 * S, 28 * S  # 528 x 616

    ix, iy = ox + T, oy + T
    ir, ib = ox + ow - T, oy + oh - T

    # interior clear: 23' x 27'
    north_clear = 12 * S
    wall_y = iy + north_clear
    bath_clear_w = 8 * S
    bath_clear_d = 8 * S
    bath_wall_x = ir - bath_clear_w - T

    rect(s, ix, iy, ir - ix, ib - iy, WASH_E)
    # gold wash on new infill zone is the whole plan; existing shell reads gray.
    # Tint the new rooms slightly warmer south of the bedroom wall? Keep one wash
    # so the open living area stays calm, and mark new walls in navy.

    frame(s, ox, oy, ow, oh, T, EXIST_FILL, EXIST_LINE)

    # new interior walls
    part(s, ix, wall_y, ir - ix, T, GOLD, GOLD)  # bed / living
    part(s, bath_wall_x, iy, T, north_clear, GOLD, GOLD)  # bed / bath+closet
    # closet bottom — 8' bath then 6" wall then 3'-6" closet = 12'
    closet_wall_y = iy + bath_clear_d
    part(s, bath_wall_x + T, closet_wall_y, ir - (bath_wall_x + T), T, GOLD, GOLD)

    # garage-door infill on the south wall, 16' centered
    infill_w = 16 * S
    infill_x = ox + (ow - infill_w) / 2
    rect(s, infill_x, ib, infill_w, T, GOLD)

    # dashed former overhead door, just outside the wall
    s.add(
        f'<rect x="{infill_x:.1f}" y="{ib + T + 6:.1f}" width="{infill_w:.1f}" height="18" '
        f'fill="none" stroke="{MID}" stroke-width="1.4" stroke-dasharray="7 5"/>'
    )
    text(
        s, infill_x + infill_w / 2, ib + T + 40,
        "(E) OVERHEAD DOOR  —  REMOVED AND INFILLED",
        size=12, fill=MUTED, anchor="middle", family=MONO, spacing="0.04em",
    )

    # doors
    # bedroom entry 3'-0" off the living side, swings into the bedroom
    bed_door_x = ix + 8 * S
    opening_h(s, bed_door_x, wall_y, 3 * S, T)
    door(s, bed_door_x, wall_y, 3 * S, 0, False)

    # bath door 2'-6", swings into bath
    opening_v(s, bath_wall_x, iy + 2.2 * S, 2.5 * S, T)
    door(s, bath_wall_x + T, iy + 2.2 * S, 2.5 * S, 90, False)

    # closet door 2'-4", swings into bedroom
    opening_v(s, bath_wall_x, closet_wall_y + T + 8, 2.3 * S, T)
    door(s, bath_wall_x, closet_wall_y + T + 8, 2.3 * S, 90, True)

    # new entry on the east wall, 3'-0", swings in
    entry_y = wall_y + T + 8 * S
    opening_v(s, ir, entry_y, 3 * S, T)
    door(s, ir, entry_y, 3 * S, 90, True)

    # windows
    # egress in bedroom north wall, 4'-0"
    bed_win_x = ix + 4 * S
    window_h(s, bed_win_x, oy, 4 * S, T)
    # west window to kitchen
    window_v(s, ox, wall_y + T + 2 * S, 4 * S, T)
    # two windows in the infilled garage door
    window_h(s, infill_x + 1.5 * S, ib, 3.5 * S, T)
    window_h(s, infill_x + 8 * S, ib, 4.5 * S, T)
    # small bath window on the east wall
    window_v(s, ir, iy + 0.8 * S, 2.5 * S, T)

    # kitchen counter along the west wall of the open room
    counter_x = ix + 2 * S
    line(s, counter_x, wall_y + T + 10, counter_x, ib - 2.2 * S, MUTED, 1.6)
    line(s, ix, ib - 2.2 * S, ix + 10 * S, ib - 2.2 * S, MUTED, 1.6)
    sink_oval(s, ix + S, wall_y + T + 4.5 * S, 12, 16)
    # sink oval is drawn axis-aligned; place a vertical-looking sink by swapping via a small rect symbol instead
    # The oval above may collide with the counter. Redraw a cleaner sink as a circle pair on the counter.
    range_symbol(s, ix + 4, wall_y + T + 1.2 * S, 2 * S - 6, 2.4 * S)
    fridge(s, ix + 4, ib - 2.2 * S - 3 * S, 2 * S - 6, 3 * S)

    # bath fixtures
    tub(s, ir - 2.7 * S, iy + 3.2 * S, 2.7 * S, 5 * S)
    toilet(s, bath_wall_x + T + 16, iy + 2.8 * S)
    rect(s, bath_wall_x + T + 8, iy + 8, 4.2 * S, 1.7 * S, WHITE, NAVY, 1.3)
    sink_oval(s, bath_wall_x + T + 2.4 * S, iy + 0.9 * S, 13, 10)

    # labels
    room(s, (ix + bath_wall_x) / 2, (iy + wall_y) / 2 + 6, "Bedroom", "14'-6\"  ×  12'-0\"", 20)
    room(s, (bath_wall_x + T + ir) / 2, iy + bath_clear_d * 0.62, "Bath", "8'-0\"  ×  8'-0\"", 16)
    room(s, (bath_wall_x + T + ir) / 2, closet_wall_y + T + 28, "Closet", "8'-0\"  ×  3'-6\"", 14)
    room(s, ix + 4.6 * S, wall_y + T + 7.2 * S, "Kitchen", None, 16)
    room(s, ix + 15 * S, wall_y + T + 6 * S, "Living", "Open to kitchen", 20)

    text(
        s, bed_win_x + 2 * S, iy + 26, "EGRESS WINDOW",
        size=12, fill=NAVY, weight="700", anchor="middle", family=MONO, spacing="0.08em",
    )
    text(
        s, ir - 8, entry_y + 3 * S + 18, "NEW ENTRY",
        size=12, fill=NAVY, weight="700", anchor="end", family=MONO, spacing="0.08em",
    )

    tag(s, bed_win_x + 2 * S, iy + 48, "E")

    # dimensions — outside faces
    dim_h(s, ox, ox + ow, oy + oh + 86, "24'-0\"", oy + oh, 15)
    dim_v(s, oy, oy + oh, ox - 48, "28'-0\"", ox, 15)
    north_arrow(s, 690, 120)

    notes_box(
        s, 742, 70, 490, "GENERAL NOTES",
        [
            "1   Illustrative sample of a garage conversion.",
            "2   Not a client project. Not for construction.",
            "3   Blue shell — existing garage walls.",
            "4   Gold walls — new partitions and door infill.",
            "5   Dashed rectangle — overhead door removed.",
            "6   One bedroom, kitchen, bath, and living.",
            "7   Egress window is a sample label only.",
            "     Confirm size with the local code.",
            "8   Overall size 24'-0\" × 28'-0\" outside.",
        ],
    )
    swatches(
        s, 756, 300,
        [
            (EXIST_FILL, "Existing garage wall"),
            (GOLD, "New wall / infill"),
        ],
    )
    notes_box(
        s, 742, 370, 490, "LAYOUT  ·  SAMPLE",
        [
            "Bedroom     14'-6\"  ×  12'-0\"",
            "Bath            8'-0\"  ×   8'-0\"",
            "Closet         8'-0\"  ×   3'-6\"",
            "Living / kitchen   23'-0\" × 14'-6\"",
            "New entry door on the east wall.",
            "Fixtures are symbols, not a fixture spec.",
        ],
    )

    title_block(s, 1280, 900, "A2.0", "ADU  &  GARAGE CONVERSION  —  FLOOR PLAN", S)
    border(s, 1280, 900)
    s.save("adu-plan.svg")


# ---------------------------------------------------------------------------
# A3 — Full remodel, open kitchen and living
# ---------------------------------------------------------------------------

def build_remodel():
    s = Sheet(
        1280,
        900,
        "Sample full remodel floor plan",
        "Illustrative sample of an open-concept kitchen and living remodel. Not for construction.",
    )
    S = 16
    T = 8
    ox, oy = 78, 96
    ow, oh = 38 * S, 28 * S

    ix, iy = ox + T, oy + T
    ir, ib = ox + ow - T, oy + oh - T

    rect(s, ix, iy, ir - ix, ib - iy, WASH_E)

    frame(s, ox, oy, ow, oh, T, EXIST_FILL, EXIST_LINE)

    # horizontal wall at 15' — a 4' piece remains, the rest is removed
    hy = iy + 15 * S
    remain_w = 4 * S
    part(s, ix, hy, remain_w, T)  # existing nib remains

    # dashed removed wall, both faces
    x_dash_1 = ix + remain_w
    x_dash_2 = ir
    line(s, x_dash_1, hy, x_dash_2, hy, MID, 1.6, 'stroke-dasharray="9 6"')
    line(s, x_dash_1, hy + T, x_dash_2, hy + T, MID, 1.6, 'stroke-dasharray="9 6"')
    # new beam centerline
    line(s, x_dash_1, hy + T / 2, x_dash_2, hy + T / 2, GOLD, 3.2)

    # powder room, southeast, 6' x 8' inside
    pw, pd = 6 * S, 8 * S
    powder_x = ir - pw
    powder_y = ib - pd
    part(s, powder_x - T, powder_y, T, pd)          # west wall
    part(s, powder_x, powder_y - T, pw, T)          # north wall

    # opening to the rest of the house, east wall
    opening_v(s, ir, iy + 3 * S, 5 * S, T)
    # break mark
    by = iy + 3 * S
    bh = 5 * S
    line(s, ir + T + 8, by - 6, ir + T + 8, by + bh + 6, NAVY, 1.2)
    line(s, ir + T + 4, by + 8, ir + T + 14, by + 16, NAVY, 1.2)
    line(s, ir + T + 14, by + 16, ir + T + 4, by + 24, NAVY, 1.2)

    # powder door, swings in
    opening_h(s, powder_x + 1.2 * S, powder_y - T, 2.5 * S, T)
    door(s, powder_x + 1.2 * S, powder_y, 2.5 * S, 0, True)

    # windows along the north living wall and the south kitchen wall
    window_h(s, ix + 3 * S, oy, 6 * S, T)
    window_h(s, ix + 16 * S, oy, 6 * S, T)
    window_h(s, ix + 28 * S, oy, 5 * S, T)
    window_h(s, ix + 6 * S, ib, 5 * S, T)  # over the sink

    # island 8' x 3'-0" with a 1' seating overhang on the living side
    isl_x, isl_y = ix + 6 * S, hy + T + 4.5 * S
    isl_w, isl_h = 8 * S, 3 * S
    rect(s, isl_x, isl_y - S, isl_w, S, "none", MID, 1.3, 'stroke-dasharray="5 4"')
    rect(s, isl_x, isl_y, isl_w, isl_h, WHITE, NAVY, 1.8)
    text(s, isl_x + isl_w / 2, isl_y + isl_h / 2 + 4, "ISLAND", size=13, fill=NAVY, weight="700", anchor="middle", family=MONO, spacing="0.12em")

    # south counter and fixtures, stopping before the powder
    counter_y = ib - 2 * S
    line(s, ix, counter_y, powder_x - T - 8, counter_y, MUTED, 1.5)
    fridge(s, ix + 8, counter_y - 0.4 * S, 3 * S, 2.4 * S)
    sink_oval(s, ix + 10 * S, counter_y + S, 20, 12)
    range_symbol(s, ix + 16 * S, counter_y, 2.6 * S, 2 * S)

    # pantry niche label along the remaining nib — the nib is a partial wall
    text(s, ix + remain_w / 2, hy - 16, "(E) NIB", size=11, fill=MUTED, anchor="middle", family=MONO)

    # labels — kept off the beam note, the island, and the powder fixtures
    room(s, ix + 14 * S, iy + 6 * S, "Living", "Open to kitchen", 22)
    room(s, ix + 28 * S, iy + 5 * S, "Dining", "Open — no wall", 16)
    room(s, ix + 7 * S, hy + T + 2.6 * S, "Kitchen", None, 18)
    room(s, powder_x + pw / 2, powder_y + pd * 0.55, "Powder", "6'-0\" × 8'-0\"", 13)

    # powder fixtures
    toilet(s, powder_x + 10, powder_y + 8)
    sink_oval(s, powder_x + pw - 28, powder_y + pd - 28, 12, 9)

    halo_text(s, ix + 18 * S, hy - 16, "(E) WALL REMOVED", size=13, fill=NAVY)
    text(
        s, ix + 20 * S, hy + T + 20,
        "NEW BEAM — SIZE BY PROJECT ENGINEER",
        size=12, fill=NAVY, weight="700", anchor="start", family=MONO, spacing="0.04em",
    )
    text(s, ir - 8, iy + 2.2 * S, "TO REST OF HOUSE", size=12, fill=MUTED, anchor="end", family=MONO, spacing="0.06em")

    # dimensions
    dim_h(s, ox, ox + ow, oy + oh + 34, "38'-0\"", oy + oh, 15)
    dim_v(s, oy, oy + oh, ox - 42, "28'-0\"", ox, 15)
    dim_v(s, iy, hy, ix - 28, "15'-0\"", ix, 13)

    north_arrow(s, 760, 78, 0.9)

    notes_box(
        s, 760, 130, 476, "GENERAL NOTES",
        [
            "1   Illustrative remodel sample. Not a real job.",
            "2   Not for construction and not for permit.",
            "3   Blue walls — existing to remain.",
            "4   Dashed wall — existing partition removed",
            "     for an open kitchen and living room.",
            "5   Gold line — new beam at the old wall.",
            "     Beam size is by a project engineer.",
            "     This sample does not size the beam.",
            "6   Dashed edge at the island is overhang.",
            "7   Area shown is the remodel zone only.",
        ],
    )
    swatches(
        s, 774, 400,
        [
            (EXIST_FILL, "Existing wall to remain"),
            (GOLD, "New beam — illustrative"),
            (NAVY, "New linework"),
        ],
    )
    notes_box(
        s, 760, 490, 476, "OPENING NOTE",
        [
            "Removed wall is about 33 ft long in this",
            "diagram, between the 4 ft nib and the",
            "east exterior wall. Powder room stays.",
            "Confirm structure before any demolition.",
        ],
    )

    title_block(s, 1280, 900, "A3.0", "FULL REMODEL  —  OPEN KITCHEN & LIVING", S)
    border(s, 1280, 900)
    s.save("remodel-plan.svg")


# ---------------------------------------------------------------------------
# A4 — Front elevation
# ---------------------------------------------------------------------------

def build_elevation():
    s = Sheet(
        1280,
        900,
        "Sample residential front elevation",
        "Illustrative front elevation with roof pitch, porch, windows, and height callouts. Not for construction.",
    )
    S = 20  # px per foot
    wall_l, wall_r = 150, 1030  # 44'-0"
    peak_x = (wall_l + wall_r) / 2  # 590
    ff_y = 590
    plate_y = ff_y - 9 * S          # 410
    # 6:12 over half-span plus 1' overhang: run = 23', rise = 11.5'
    overhang = 1 * S
    eave_l, eave_r = wall_l - overhang, wall_r + overhang
    rise = 11.5 * S
    peak_y = plate_y - rise         # 180
    foundation_top = ff_y + 0.4 * S
    grade_y = ff_y + 1.6 * S

    # ground
    rect(s, 70, grade_y, 1140, 36, "#0b2144")
    for gx in range(80, 1200, 14):
        line(s, gx, grade_y, gx - 8, grade_y + 12, "#7eb6d8", 1)

    # wall panel for siding clip
    s.add(
        f'<clipPath id="siding"><rect x="{wall_l}" y="{plate_y}" width="{wall_r - wall_l}" height="{foundation_top - plate_y}"/></clipPath>'
    )
    s.add(
        f'<clipPath id="roofclip"><path d="M{eave_l},{plate_y} L{peak_x},{peak_y} L{eave_r},{plate_y} Z"/></clipPath>'
    )

    # roof fill and shingle courses
    s.add(f'<path d="M{eave_l},{plate_y} L{peak_x},{peak_y} L{eave_r},{plate_y} Z" fill="#102c52" stroke="none"/>')
    s.add('<g clip-path="url(#roofclip)">')
    y = peak_y + 10
    while y < plate_y:
        line(s, eave_l, y, eave_r, y, "#6eb4d6", 1)
        y += 8
    s.add("</g>")
    s.add(
        f'<path d="M{eave_l},{plate_y} L{peak_x},{peak_y} L{eave_r},{plate_y}" '
        f'fill="none" stroke="{NAVY}" stroke-width="2.2" stroke-linejoin="miter"/>'
    )
    # fascia thickness
    s.add(
        f'<path d="M{eave_l},{plate_y} L{peak_x},{peak_y} L{eave_r},{plate_y} L{eave_r - 8},{plate_y + 8} '
        f'L{peak_x},{peak_y + 10} L{eave_l + 8},{plate_y + 8} Z" fill="none" stroke="{NAVY}" stroke-width="1"/>'
    )

    # siding
    rect(s, wall_l, plate_y, wall_r - wall_l, foundation_top - plate_y, "#14375f", NAVY, 1.6)
    s.add('<g clip-path="url(#siding)">')
    sy = plate_y + 8
    while sy < foundation_top:
        line(s, wall_l, sy, wall_r, sy, "#7eb8dc", 1)
        sy += 9
    s.add("</g>")

    # corner boards
    rect(s, wall_l, plate_y, 10, foundation_top - plate_y, WHITE, NAVY, 1.4)
    rect(s, wall_r - 10, plate_y, 10, foundation_top - plate_y, WHITE, NAVY, 1.4)

    # foundation
    rect(s, wall_l, foundation_top, wall_r - wall_l, grade_y + 8 - foundation_top, "#0c2444", NAVY, 1.4)
    line(s, wall_l - 30, grade_y, wall_r + 30, grade_y, NAVY, 1.6)

    # chimney on the right slope, in front of the roof
    # slope dy/dx = 0.5 from peak
    ch_x1, ch_x2 = peak_x + 150, peak_x + 210
    roof_at = peak_y + 0.5 * (ch_x1 - peak_x)
    ch_top = roof_at - 3.2 * S
    rect(s, ch_x1, ch_top, ch_x2 - ch_x1, (roof_at + 8) - ch_top, "#14375f", NAVY, 1.8)
    rect(s, ch_x1 - 6, ch_top, ch_x2 - ch_x1 + 12, 8, WHITE, NAVY, 1.4)
    line(s, ch_x1 + 8, ch_top + 8, ch_x1 + 8, roof_at, MID, 1)
    text(s, (ch_x1 + ch_x2) / 2, ch_top - 10, "CHIMNEY", size=11, fill=MUTED, anchor="middle", family=MONO, spacing="0.08em")

    # attic window in the gable
    aw, ah = 2.2 * S, 3.4 * S
    ax0 = peak_x - aw / 2
    ay0 = peak_y + 78
    draw_hung_window(s, ax0, ay0, aw, ah)

    # porch — shed seen from the front, beam at 8'-0" above finish floor
    porch_l, porch_r = peak_x - 6 * S, peak_x + 6 * S
    beam_y = ff_y - 8 * S
    # band
    rect(s, porch_l - 0.6 * S, beam_y - 10, (porch_r - porch_l) + 1.2 * S, 10, WHITE, NAVY, 1.6)
    line(s, porch_l - 0.6 * S, beam_y, porch_r + 0.6 * S, beam_y, NAVY, 2)
    # columns
    col_w = 14
    for cx0 in (porch_l, porch_r - col_w):
        rect(s, cx0, beam_y, col_w, ff_y - beam_y, WHITE, NAVY, 1.6)
        rect(s, cx0 - 4, beam_y, col_w + 8, 6, WHITE, NAVY, 1.3)          # capital
        rect(s, cx0 - 4, ff_y - 6, col_w + 8, 6, WHITE, NAVY, 1.3)        # base
    text(s, peak_x, beam_y - 18, "PORCH   8'-0\"", size=13, fill=NAVY, weight="650", anchor="middle", family=MONO, spacing="0.08em")

    # windows flanking the porch, head at 6'-8"
    head_y = ff_y - (6 + 8 / 12) * S
    win_h = 5 * S
    win_w = 3 * S
    sill_y = head_y + win_h
    gap = 0.7 * S

    def pair(center):
        total = win_w * 2 + gap
        x0 = center - total / 2
        draw_hung_window(s, x0, head_y, win_w, win_h)
        draw_hung_window(s, x0 + win_w + gap, head_y, win_w, win_h)

    left_center = (wall_l + porch_l) / 2
    right_center = (porch_r + wall_r) / 2
    pair(left_center)
    pair(right_center)

    # entry door 3'-0" x 6'-8"
    door_w = 3 * S
    door_h = (6 + 8 / 12) * S
    door_x = peak_x - door_w / 2
    door_y = ff_y - door_h
    rect(s, door_x, door_y, door_w, door_h, WHITE, NAVY, 2)
    # rails and panels
    rail_y = door_y + door_h * 0.42
    line(s, door_x, rail_y, door_x + door_w, rail_y, NAVY, 1.4)
    rect(s, door_x + 6, door_y + 8, door_w - 12, rail_y - door_y - 16, "none", MID, 1.2)
    rect(s, door_x + 6, rail_y + 8, door_w - 12, ff_y - rail_y - 16, "none", MID, 1.2)
    s.add(f'<circle cx="{door_x + door_w - 10:.1f}" cy="{rail_y + 4:.1f}" r="2.4" fill="{NAVY}"/>')
    # sill
    line(s, door_x - 6, ff_y, door_x + door_w + 6, ff_y, NAVY, 2)

    # steps
    step_w = 5 * S
    step_x = peak_x - step_w / 2
    for i in range(4):
        yy = ff_y + i * 8
        inset = i * 6
        line(s, step_x - inset, yy, step_x + step_w + inset, yy, NAVY, 1.4)

    # finish floor line across the wall
    line(s, wall_l, ff_y, wall_r, ff_y, GOLD, 1.5, 'stroke-dasharray="6 4"')
    text(s, wall_l + 16, ff_y - 8, "F.F.  0'-0\"", size=12, fill=NAVY, family=MONO, weight="650")

    # pitch diagram on the left slope
    tri_x, tri_y = eave_l + 70, plate_y - 70
    line(s, tri_x, tri_y, tri_x + 72, tri_y, NAVY, 1.4)
    line(s, tri_x + 72, tri_y, tri_x + 72, tri_y - 36, NAVY, 1.4)
    line(s, tri_x, tri_y, tri_x + 72, tri_y - 36, NAVY, 1.3)
    text(s, tri_x + 36, tri_y + 16, "12", size=13, fill=NAVY, anchor="middle", family=MONO, weight="650")
    text(s, tri_x + 80, tri_y - 18, "6", size=13, fill=NAVY, family=MONO, weight="650")

    # height string on the right
    dx = wall_r + 70
    dim_v(s, peak_y, ff_y, dx, "20'-6\"", wall_r, 13)
    # extra ticks for plate
    line(s, wall_r, plate_y, dx, plate_y, MID, 1)
    line(s, dx - 4.5, plate_y - 4.5, dx + 4.5, plate_y + 4.5, NAVY, 1.4)
    halo_text(s, dx + 58, plate_y, "PLATE  9'-0\"", size=12, anchor="start")
    line(s, wall_r, grade_y, dx, grade_y, MID, 1)
    halo_text(s, dx + 58, grade_y, "GRADE", size=12, anchor="start")
    halo_text(s, dx + 58, ff_y, "F.F.  0'-0\"", size=12, anchor="start")
    halo_text(s, dx + 58, peak_y, "RIDGE", size=12, anchor="start")

    # width dims
    dim_h(s, wall_l, wall_r, grade_y + 62, "44'-0\"", grade_y + 8, 15)
    dim_h(s, porch_l, porch_r, ff_y + 28, "12'-0\" PORCH", ff_y, 12)

    # local head callout
    text(s, wall_l + 18, head_y - 8, "HEAD  6'-8\"", size=12, fill=MUTED, family=MONO)
    text(s, left_center, sill_y + 18, "5'-0\"  ×  3'-0\"", size=12, fill=MUTED, anchor="middle", family=MONO)

    notes_box(
        s, 48, 48, 360, "ELEVATION NOTES",
        [
            "Illustrative front elevation.",
            "Not a client home. Not for construction.",
            "Main roof 6:12. Porch is a shed",
            "below the eave, drawn in elevation.",
            "Heights are from finish floor.",
            "Siding courses are diagrammatic.",
        ],
        line_h=18, size=13,
    )

    title_block(s, 1280, 900, "A4.0", "FRONT ELEVATION  —  SAMPLE RESIDENCE", S)
    border(s, 1280, 900)
    s.save("front-elevation.svg")


def draw_hung_window(s, x, y, w, h):
    rect(s, x, y, w, h, "#0c2748", NAVY, 1.8)
    # jamb thickness
    rect(s, x + 3.5, y + 3.5, w - 7, h - 7, "#163e68", MID, 1)
    line(s, x, y + h / 2, x + w, y + h / 2, NAVY, 1.4)
    line(s, x + w / 2, y, x + w / 2, y + h, MID, 1)
    # sill
    line(s, x - 5, y + h, x + w + 5, y + h, NAVY, 2)
    rect(s, x - 6, y + h, w + 12, 4, WHITE, NAVY, 1)


# ---------------------------------------------------------------------------
# Hero study — larger labels, same addition story, fewer notes
# ---------------------------------------------------------------------------

def build_hero():
    s = Sheet(
        720,
        720,
        "Sample home addition study",
        "Simplified illustrative plan of an existing house and a proposed addition. Not for construction.",
    )
    # 14.5 px = 1 ft. Outer sizes match the dimension labels exactly.
    T = 12
    ox, oy = 86, 268
    ow, oh = 522, 348  # 36'-0" x 24'-0"
    ax, ay, aw, ah = ox, oy - 203, 290, 203  # 20'-0" x 14'-0"

    ix, iy = ox + T, oy + T
    ir, ib = ox + ow - T, oy + oh - T

    rect(s, ix, iy, ir - ix, ib - iy, WASH_E)
    rect(s, ax + T, ay + T, aw - 2 * T, oy - ay - T, WASH_P)
    frame(s, ox, oy, ow, oh, T, EXIST_FILL, EXIST_LINE)
    u_wall(s, ax, ay, aw, ah + T, T, GOLD)

    # simple interior: living across the top, kitchen and bedroom below
    hy = iy + 190
    part(s, ix, hy, ir - ix, T)
    vx = ix + 250
    part(s, vx, hy + T, T, ib - (hy + T))

    # cased opening into the addition
    opening_h(s, ax + 70, oy, 120, T)
    # opening living to kitchen
    opening_h(s, ix + 70, hy, 90, T)
    # bedroom door
    opening_h(s, vx + T + 24, hy, 46, T)
    door(s, vx + T + 24, hy, 46, 0, False)
    # front door
    opening_h(s, vx + 70, ib, 52, T)
    door(s, vx + 70, ib, 52, 0, False)
    # addition side door, low enough to clear the room label
    opening_v(s, ax + aw - T, ay + 128, 48, T)
    door(s, ax + aw - T, ay + 128, 48, 90, True)

    # windows
    window_h(s, ax + 78, ay, 110, T)
    window_v(s, ax, ay + 40, 70, T)
    window_v(s, ox, iy + 40, 80, T)
    window_v(s, ox, iy + 140, 64, T)
    window_h(s, ix + 300, oy, 90, T)
    window_h(s, ix + 40, ib, 80, T)
    window_v(s, ir, hy + T + 30, 70, T)

    room(s, (ax + T + ax + aw - T) / 2, ay + 70, "Family Room", "Proposed addition", 22)
    room(s, (ix + ir) / 2, iy + 100, "Living", "Existing", 22)
    room(s, (ix + vx) / 2, (hy + ib) / 2 + 8, "Kitchen", "Existing", 18)
    room(s, (vx + ir) / 2, (hy + ib) / 2 + 8, "Bedroom", "Existing", 18)

    text(
        s, (ax + aw) / 2, ay + 28, "PROPOSED",
        size=13, fill=NAVY, weight="700", anchor="middle", family=MONO, spacing="0.18em",
    )

    dim_h(s, ox, ox + ow, oy + oh + 36, "36'-0\"  EXISTING", oy + oh, 14)
    dim_h(s, ax, ax + aw, ay - 26, "20'-0\"", ay, 14)
    dim_v(s, ay, oy, ox - 36, "14'-0\"", ax, 13)
    dim_v(s, oy, oy + oh, ox - 36, "24'-0\"", ox, 13)

    north_arrow(s, 640, 130, 0.9)

    rect(s, 24, 676, 672, 26, WHITE, NAVY, 1.2)
    text(
        s, 360, 694, "ILLUSTRATIVE SAMPLE  ·  HOME ADDITION STUDY  ·  NOT FOR CONSTRUCTION",
        size=11, fill=NAVY, anchor="middle", family=MONO, spacing="0.04em", weight="600",
    )
    s.add(f'<rect x="16" y="16" width="688" height="688" fill="none" stroke="{NAVY}" stroke-width="1.6"/>')
    s.save("hero-addition.svg")


def build_favicon():
    path = OUT.parent / "favicon.svg"
    path.write_text(
        f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" rx="4" fill="#122b52"/>
  <path fill="{GOLD}" fill-rule="evenodd" d="M16 5 L28 15 H24 V26 H8 V15 H4 Z M14 18 H18 V26 H14 Z"/>
</svg>
'''
    )
    print(f"wrote {path}")


if __name__ == "__main__":
    build_addition()
    build_adu()
    build_remodel()
    build_elevation()
    build_hero()
    build_favicon()
