"""이름 인장(설재원) SVG 를 만든다.

네 칸 인장: 설·재 / 원·눈송이. 왼쪽 위부터 가로로 읽는다(설 = 눈, 아이디 snowjaewon).
세로로 긴 「설」 한 열 배치는 「서」와 「ㄹ」이 따로 읽혀서(재서/원ㄹ) 버렸다.
글자는 폰트 윤곽선을 경로로 바꿔 넣으므로 보는 기기에 폰트가 없어도 똑같이 보인다.

폰트: Black Han Sans (SIL Open Font License 1.1)
  https://github.com/google/fonts/raw/main/ofl/blackhansans/BlackHanSans-Regular.ttf

사용: python tools/make_seal.py <BlackHanSans-Regular.ttf>
출력: assets/seal.svg (선명한 판, 파비콘·머리글용)
      assets/seal-stamp.svg (인주 질감 판, 큰 크기용)
"""
import math
import os
import sys

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

SEAL = "#c2402d"
PAPER = "#f7f7f4"

# viewBox 0 0 100 100 안의 칸 (x0, y0, x1, y1).
MARGIN, GAP = 11, 5
LO, HI = MARGIN, 100 - MARGIN
A, B = 50 - GAP / 2, 50 + GAP / 2
CELLS = {
    "설": (LO, LO, A, A),
    "재": (B, LO, HI, A),
    "원": (LO, B, A, HI),
}
SNOW_CELL = (B, B, HI, HI)
ARM_W, TWIG_W = 5.4, 3.6


def num(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s == "-0" else s


def glyph_path(font, ch, box):
    glyphs = font.getGlyphSet()
    glyph = glyphs[font.getBestCmap()[ord(ch)]]
    bounds = BoundsPen(glyphs)
    glyph.draw(bounds)
    xmin, ymin, xmax, ymax = bounds.bounds
    x0, y0, x1, y1 = box
    sx = (x1 - x0) / (xmax - xmin)
    sy = (y1 - y0) / (ymax - ymin)
    pen = SVGPathPen(glyphs, ntos=num)
    # 폰트 좌표(y 위로) → SVG 좌표(y 아래로), 칸을 꽉 채우게 맞춘다.
    glyph.draw(TransformPen(pen, (sx, 0, 0, -sy, x0 - xmin * sx, y1 + ymin * sy)))
    return pen.getCommands()


def snowflake(box):
    """가지 6개, 가지마다 곁가지 2개. (굵은 가지 경로, 가는 곁가지 경로)."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    r = (x1 - x0) / 2 - ARM_W / 2
    arms, twigs = [], []
    for k in range(6):
        a = math.radians(90 + 60 * k)
        ux, uy = math.cos(a), -math.sin(a)
        arms.append(f"M{num(cx)} {num(cy)}L{num(cx + ux * r)} {num(cy + uy * r)}")
        px, py = cx + ux * r * 0.56, cy + uy * r * 0.56
        for side in (-1, 1):
            b = a + side * math.radians(48)
            vx, vy = math.cos(b), -math.sin(b)
            twigs.append(f"M{num(px)} {num(py)}L{num(px + vx * r * 0.42)} {num(py + vy * r * 0.42)}")
    return "".join(arms), "".join(twigs)


def marks(d, arms, twigs, color):
    return (
        f'<path fill="{color}" d="{d}"/>'
        f'<g fill="none" stroke="{color}" stroke-linecap="round">'
        f'<path stroke-width="{ARM_W}" d="{arms}"/><path stroke-width="{TWIG_W}" d="{twigs}"/></g>'
    )


def main(font_path):
    font = TTFont(font_path)
    d = " ".join(glyph_path(font, ch, box) for ch, box in CELLS.items())
    arms, twigs = snowflake(SNOW_CELL)
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

    crisp = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-label="설재원 인장">'
        f'<rect width="100" height="100" rx="8" fill="{SEAL}"/>'
        + marks(d, arms, twigs, PAPER)
        + "</svg>\n"
    )

    # 인주 질감: 가장자리를 살짝 흔들고, 잉크가 덜 묻은 자리를 군데군데 비운다.
    # 글자는 마스크로 뚫어서 바탕이 비쳐 보이게 한다(백문 인장).
    stamp = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-4 -4 108 108" role="img" aria-label="설재원 인장">'
        "<defs>"
        '<filter id="ink" x="-4%" y="-4%" width="108%" height="108%">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.6" numOctaves="2" seed="11" result="edge"/>'
        '<feDisplacementMap in="SourceGraphic" in2="edge" scale="1.5" xChannelSelector="R" yChannelSelector="G" result="rough"/>'
        '<feTurbulence type="fractalNoise" baseFrequency="0.12" numOctaves="3" seed="4" result="blot"/>'
        '<feColorMatrix in="blot" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -10 8.1" result="cover"/>'
        '<feComposite in="rough" in2="cover" operator="in"/>'
        "</filter>"
        '<mask id="cut"><rect x="-4" y="-4" width="108" height="108" fill="#fff"/>'
        + marks(d, arms, twigs, "#000")
        + "</mask></defs>"
        f'<g filter="url(#ink)"><rect width="100" height="100" rx="8" fill="{SEAL}" mask="url(#cut)"/></g>'
        "</svg>\n"
    )

    for name, body in (("seal.svg", crisp), ("seal-stamp.svg", stamp)):
        path = os.path.join(root, name)
        with open(path + ".tmp", "w", encoding="utf-8", newline="\n") as f:
            f.write(body)
        os.replace(path + ".tmp", path)
        print(name, len(body), "bytes")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
