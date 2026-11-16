#!/usr/bin/env python3
"""Build the profile artwork in assets/ from code.

GitHub shows README images through a proxy that blocks external fonts, so all
type is converted to outlines here, and the avatar is printed as a duotone and
embedded. Edit the copy or colours below, then run:

    python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt
    .venv/bin/python scripts/build.py
"""

from __future__ import annotations

import base64
import io
import math
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from PIL import Image, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
FONT = ROOT / "fonts" / "Archivo-Variable.ttf"
AVATAR = ASSETS / "avatar.jpg"

# One spot colour, one ink, cream only for reversed type.
SPOT = "#F2A516"
INK = "#15120E"
CREAM = "#FFF4DC"
# Where the avatar sits on the 1600x1000 poster: the face fully in frame,
# the body cut by the right and bottom edges.
AVATAR_X, AVATAR_Y, AVATAR_H = 690, -40, 1250
SLANT = -7  # degrees; every slanted line on the sleeve shares it

W = 1600  # every asset is drawn on a 1600-wide canvas


class Face:
    """One static instance of the variable font, able to set text as paths."""

    def __init__(self, wdth: float, wght: float):
        font = instantiateVariableFont(TTFont(FONT), {"wdth": wdth, "wght": wght})
        self.glyphs = font.getGlyphSet()
        self.cmap = font.getBestCmap()
        self.hmtx = font["hmtx"]
        self.upm = font["head"].unitsPerEm
        self.cap = font["OS/2"].sCapHeight

    def width(self, text: str, size: float, track: float = 0) -> float:
        s = size / self.upm
        adv = sum(self.hmtx[self.cmap[ord(c)]][0] for c in text)
        return adv * s + track * size * (len(text) - 1)

    def path(self, text: str, x: float, y: float, size: float, track: float = 0) -> str:
        """SVG path data for text whose baseline starts at (x, y)."""
        s = size / self.upm
        pen = SVGPathPen(self.glyphs, ntos=lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
        cx = x
        for c in text:
            name = self.cmap[ord(c)]
            self.glyphs[name].draw(TransformPen(pen, (s, 0, 0, -s, cx, y)))
            cx += self.hmtx[name][0] * s + track * size
        return pen.getCommands()

    def size_for_cap(self, cap_px: float) -> float:
        return cap_px * self.upm / self.cap


DISPLAY = Face(wdth=62, wght=900)
LABEL = Face(wdth=75, wght=700)
BODY = Face(wdth=88, wght=500)


def text(face: Face, s: str, x: float, y: float, cap: float, fill: str,
         track: float = 0, anchor: str = "start") -> str:
    size = face.size_for_cap(cap)
    if anchor == "end":
        x -= face.width(s, size, track)
    return f'<path fill="{fill}" d="{face.path(s, x, y, size, track)}"/>'


def svg(h: int, body: str, label: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" '
        f'width="{W}" height="{h}" role="img" aria-label="{label}">'
        f"<title>{label}</title>{body}</svg>\n"
    )


def duotone_avatar(height: int) -> tuple[str, int, int]:
    """Print the avatar in ink on the spot colour, three flat tones."""
    gray = Image.open(AVATAR).convert("L")
    scale = height / gray.height
    size = (round(gray.width * scale), height)
    img = gray.resize(size, Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.2))
    ink, spot = _rgb(INK), _rgb(SPOT)
    mid = tuple(round(a * 0.55 + b * 0.45) for a, b in zip(ink, spot))
    # Levels picked by eye: outlines, hair and glasses go to ink, the jacket
    # and trousers to the mid tone, the yellow ground and skin drop into the field.
    lut = [0 if v < 92 else 1 if v < 168 else 2 for v in range(256)]
    idx = img.point(lut)
    out = Image.new("P", img.size)
    out.putpalette([*ink, *mid, *spot] + [0] * (256 - 3) * 3)
    out.putdata(list(idx.tobytes()))
    buf = io.BytesIO()
    out.save(buf, "PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode(), img.width, img.height


# The avatar's glasses are a pale khaki frame that the duotone loses in the
# field, so the poster redraws them at their own weight in cream. Corners are traced
# in the 460px source image (assets/avatar.jpg) and scaled with the avatar.
GLASSES = [
    [(193.8, 171.3), (256.3, 163.8), (255.0, 207.5), (198.8, 213.8)],  # left lens
    [(263.8, 163.8), (317.5, 156.3), (320.0, 196.3), (268.8, 201.3)],  # right lens
]
GLASSES_ARMS = [((256.3, 171.0), (263.8, 170.0)), ((193.8, 190.0), (176.0, 194.0))]


def glasses(x0: float, y0: float, scale: float) -> str:
    """Thin pale frames like the avatar's own, with a hairline ink edge."""
    def pt(p):
        return f"{x0 + p[0] * scale:.1f},{y0 + p[1] * scale:.1f}"
    shapes = "".join(f'<polygon points="{" ".join(pt(p) for p in lens)}"/>' for lens in GLASSES)
    shapes += "".join(f'<polyline points="{pt(a)} {pt(b)}"/>' for a, b in GLASSES_ARMS)
    layer = ('<g fill="none" stroke="{c}" stroke-width="{w}" '
             'stroke-linejoin="round" stroke-linecap="round">' + shapes + "</g>")
    return layer.format(c=INK, w=15) + layer.format(c=CREAM, w=9)


def _rgb(hex_: str) -> tuple[int, int, int]:
    return tuple(int(hex_[i : i + 2], 16) for i in (1, 3, 5))


def rule(x1: float, y: float, length: float, weight: float, colour: str) -> str:
    """A straight rule at the sleeve's slant, starting at (x1, y)."""
    a = math.radians(SLANT)
    x2, y2 = x1 + length * math.cos(a), y + length * math.sin(a)
    return (f'<line x1="{x1}" y1="{y}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{colour}" stroke-width="{weight}"/>')


def sleeve() -> str:
    h = 1000
    parts = [f'<rect width="{W}" height="{h}" fill="{SPOT}"/>']

    # Session photograph: the avatar, cropped hard into the right edge.
    data, aw, ah = duotone_avatar(AVATAR_H)
    parts.append(
        f'<image x="{AVATAR_X}" y="{AVATAR_Y}" width="{aw}" height="{ah}" '
        f'href="data:image/png;base64,{data}"/>'
    )
    parts.append(glasses(AVATAR_X, AVATAR_Y, ah / 460))

    # Catalogue box, top left, like a label's logotype.
    bw = LABEL.width("0xFANGO", LABEL.size_for_cap(30), 0.04)
    parts.append(
        f'<g transform="rotate({SLANT} 70 100)">'
        f'<rect x="64" y="64" width="{bw + 36:.0f}" height="64" fill="none" '
        f'stroke="{INK}" stroke-width="4"/>'
        + text(LABEL, "0xFANGO", 82, 111, 30, INK, track=0.04)
        + text(LABEL, "FULL STACK SESSIONS  No. 0x7EA", bw + 124, 108, 19, INK, track=0.08)
        + "</g>"
    )

    # The name in two stacked slabs, FANGO / OOOOO, at the shared slant.
    cap = 236
    g = f'<g transform="rotate({SLANT} 70 470)">'
    g += text(DISPLAY, "FANGO", 70, 470, cap, INK, track=-0.005)
    g += text(DISPLAY, "OOOOO", 70, 470 + cap + 34, cap, INK, track=-0.005)
    width = DISPLAY.width("FANGO", DISPLAY.size_for_cap(cap), -0.005)
    y = 470 + cap + 34 + 52
    g += f'<line x1="74" y1="{y}" x2="{74 + width:.0f}" y2="{y}" stroke="{INK}" stroke-width="5"/>'
    g += text(LABEL, "FULL STACK ENGINEER", 76, y + 56, 28, INK, track=0.07)
    g += text(LABEL, "SMALL TOOLS FOR AI AGENTS, AUDIO & VIDEO", 76, y + 100, 28, INK, track=0.07)
    parts.append(g + "</g>")

    # Credits along the foot, straight, like the small print on a sleeve.
    a = "FORMERLY MARSWAVE AI / LISTENHUB"
    aw2 = BODY.width(a, BODY.size_for_cap(17), 0.1)
    parts.append(text(BODY, a, 70, 950, 17, INK, 0.1))
    parts.append(text(BODY, "PREVIOUSLY TIKTOK, DIDI", 70 + aw2 + 48, 950, 17, INK, 0.1))

    return svg(h, "".join(parts),
               "Fangoooooo (0xFANGO): full stack engineer, small tools for AI agents, "
               "audio and video. Formerly MarsWave AI / ListenHub, previously TikTok and DiDi.")


def main() -> None:
    (ASSETS / "sleeve.svg").write_text(sleeve())
    print("wrote", ", ".join(p.name for p in sorted(ASSETS.glob("*.svg"))))


if __name__ == "__main__":
    main()
