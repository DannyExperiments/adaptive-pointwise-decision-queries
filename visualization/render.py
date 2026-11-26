"""Render the three lifted cost lanes and build the self-contained explorer ZIP."""

import argparse
from fractions import Fraction as F
from math import cos, pi, sin
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from PIL import Image, ImageDraw, ImageFont

SIZE = (704, 840)
PAPER = '#f4f7fb'
INK = '#162943'
MUTED = '#445d79'
COLORS = ('#007961', '#0067ac', '#8446a3')
FILL = ('#b9e5d8', '#c2e1f7', '#ead2f6')
FONT = '/System/Library/Fonts/Supplemental/Arial{}.ttf'


def text(draw, value, xy, size, *, color=INK, bold=False, anchor=None):
    face = ImageFont.truetype(FONT.format(' Bold' if bold else ''), size)
    box = draw.textbbox(xy, value, font=face, anchor=anchor)
    assert 0 <= box[0] < box[2] < SIZE[0] and 0 <= box[1] < box[3] < SIZE[1], (value, box)
    draw.text(xy, value, fill=color, font=face, anchor=anchor)


def project(t, lane, z, angle):
    x = t - 7
    y = 1.48 * (lane - 2)
    return (
        round(354 + 44 * (cos(angle) * x - sin(angle) * y)),
        round(381 + 42 * (sin(angle) * x + cos(angle) * y) - 62 * z),
    )


def render(t, answer, angle):
    image = Image.new('RGB', SIZE, PAPER)
    draw = ImageDraw.Draw(image)
    text(draw, 'One answer picks the next', (40, 31), 47, bold=True)
    text(draw, 'Three disjoint cost windows', (42, 95), 31, color=MUTED)
    draw.rounded_rectangle((39, 148, 665, 584), radius=19, fill='white', outline='#cddae9', width=2)
    for j in (3, 2, 1):
        a, b = 3 * j, 3 * j + 2
        axis = [project(x, j, 0, angle) for x in (2.3, 11.7)]
        draw.line(axis, fill='#bdccdc', width=3)
        for tick in range(3, 12):
            x, y = project(tick, j, 0, angle)
            draw.line((x, y - 3, x, y + 4), fill='#a0b0c0', width=2)
        shade = [project(x, j, z, angle) for x, z in ((a, 0), (b, 0), (a + 1, -1))]
        draw.polygon(shade, fill=FILL[j - 1])
        lower = [project(x, j, z, angle) for x, z in ((a - 1, 1), (a + 1, -1), (b + 1, 1))]
        draw.line(lower, fill=COLORS[j - 1], width=4, joint='curve')
        draw.line(shade[:2], fill=COLORS[j - 1], width=6)
        x, y = project(2.3, j, 0, angle)
        text(draw, f'z{j}', (x - 31, y - 13), 25, bold=True, color=COLORS[j - 1], anchor='rt')
    p = [project(float(t), j, 0, angle) for j in (1, 3)]
    draw.line(p, fill='#112942', width=4)
    for j in (1, 2, 3):
        x, y = project(float(t), j, 0, angle)
        draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill='#112942')
    active = next((j for j in (1, 2, 3) if 3 * j < t < 3 * j + 2), None)
    if active:
        x1, y1 = project(float(t), active, 0, angle)
        x2, y2 = project(float(t), active, float(answer), angle)
        color = COLORS[active - 1]
        draw.line((x1, y1, x2, y2), fill=color, width=5)
        draw.ellipse((x2 - 9, y2 - 9, x2 + 9, y2 + 9), fill=color, outline='white', width=2)
    y = 184
    for j in (1, 2, 3):
        x = 128 + (j - 1) * 190
        text(draw, f'z{j}  ({3*j}, {3*j+2})', (x, y), 26, color=COLORS[j - 1], bold=True, anchor='mt')
    text(draw, 'Colored wedges allow negative gaps.', (352, 551), 24, color=MUTED, anchor='mt')
    text(draw, f'First answer   t = {t}', (43, 606), 40, bold=True)
    if active:
        text(draw, f'Query only z{active} = {answer}', (45, 668), 34, bold=True, color=COLORS[active - 1])
        outcome = f'Choose x{active} = 1.' if answer < 0 else 'All-zero choice is optimal.'
        text(draw, outcome, (46, 722), 27, color=MUTED)
    else:
        text(draw, 'No second query', (45, 668), 34, bold=True)
        text(draw, 'All three gaps are positive.', (46, 722), 27, color=MUTED)
    text(draw, 'Worst case   2 adaptive · 3 fixed', (46, 782), 29, bold=True)
    return image.quantize(colors=96, method=Image.Quantize.MEDIANCUT)


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=here)
    destination = parser.parse_args().output
    destination.mkdir(parents=True, exist_ok=True)
    examples = [(F(4), F(-1, 2)), (F(5), F(0)), (F(7), F(0)), (F(10), F(1, 2))]
    schedule = [(t, outcome, .16 + .14 * sin(((group * 7 + k) / 28) * 2 * pi),
                 1850 if k == 6 else 105)
                for group, (t, outcome) in enumerate(examples) for k in range(7)]
    frames = [render(t, outcome, angle) for t, outcome, angle, _ in schedule]
    frames[0].save(destination / 'adaptive-cost-windows.gif', save_all=True, append_images=frames[1:],
                   duration=[duration for _, _, _, duration in schedule], loop=0, optimize=True)
    entry = ZipInfo('index.html', (1980, 1, 1, 0, 0, 0))
    entry.external_attr = 0o100644 << 16
    with ZipFile(destination / 'adaptive-cost-windows-explorer.zip', 'w') as archive:
        archive.writestr(entry, (here / 'index.html').read_bytes(), compress_type=ZIP_DEFLATED, compresslevel=9)


if __name__ == '__main__':
    main()
