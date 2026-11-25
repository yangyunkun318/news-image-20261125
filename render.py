#!/usr/bin/env python3
"""Render the 25 November 2026 world-news front page (1024x1024 PNG).

Stories are all first reported on Wednesday 25 November 2026 (UTC),
taken from the day's wire reporting. Drawn with Pillow only: flat vector
illustrations + real text, so every word is legible and nothing is garbled.
Deterministic: same input -> same bytes.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (18, 30, 58)
NAVY = (16, 32, 66)
RED = (178, 28, 28)
GOLD = (180, 83, 9)
TEAL = (14, 74, 92)
GREY = (90, 96, 110)
LIGHT = (233, 228, 214)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def vgrad(draw, box, top, bottom):
    x0, y0, x1, y1 = box
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0 - 1)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        draw.line([(x0, y), (x1, y)], fill=c)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, width, leading=None):
    x, y = xy
    lh = leading or int(fnt.size * 1.18)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def sun(draw, cx, cy, r, color):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)


def burst(draw, cx, cy, r, color):
    pts = []
    for k in range(16):
        a = math.pi * k / 8
        rr = r if k % 2 == 0 else r * 0.45
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    draw.polygon(pts, fill=color)


def skyline(draw, x0, y_base, x1, color, seed=0):
    import random
    rnd = random.Random(seed)
    x = x0
    while x < x1:
        w = rnd.randint(22, 46)
        h = rnd.randint(18, 46)
        draw.rectangle([x, y_base - h, x + w, y_base], fill=color)
        x += w + rnd.randint(4, 10)


def courthouse(draw, x0, y0, x1, y1):
    # flat courthouse: pediment, five columns, steps, on a navy sky
    vgrad(draw, (x0, y0, x1, y1), (24, 48, 92), (12, 24, 56))
    sun(draw, x1 - 70, y0 + 42, 20, (232, 200, 120))
    # building block
    draw.rectangle([x0 + 60, y0 + 120, x1 - 60, y1 - 46], fill=(216, 210, 192))
    # pediment
    draw.polygon([(x0 + 50, y0 + 122), ((x0 + x1) // 2, y0 + 62),
                  (x1 - 50, y0 + 122)], fill=(233, 228, 214))
    draw.ellipse([((x0 + x1) // 2) - 14, y0 + 82, ((x0 + x1) // 2) + 14,
                  y0 + 110], fill=(178, 28, 28))
    # columns
    for i in range(5):
        cx = x0 + 108 + i * 84
        draw.rectangle([cx - 12, y0 + 128, cx + 12, y1 - 78], fill=(248, 244, 232))
        draw.rectangle([cx - 17, y0 + 122, cx + 17, y0 + 130], fill=(248, 244, 232))
        draw.rectangle([cx - 17, y1 - 84, cx + 17, y1 - 76], fill=(248, 244, 232))
    # door
    draw.rectangle([((x0 + x1) // 2) - 26, y1 - 120, ((x0 + x1) // 2) + 26,
                    y1 - 78], fill=(24, 32, 54))
    # steps
    for k in range(3):
        draw.rectangle([x0 + 30 + k * 12, y1 - 46 + k * 12,
                        x1 - 30 - k * 12, y1 - 34 + k * 12],
                       fill=(180, 174, 156))
    # flag
    draw.line([(x0 + 66, y0 + 62), (x0 + 66, y0 + 18)], fill=(233, 228, 214),
              width=4)
    draw.polygon([(x0 + 66, y0 + 18), (x0 + 106, y0 + 28), (x0 + 66, y0 + 38)],
                 fill=(178, 28, 28))


def rocket(draw, x0, y0, x1, y1):
    # night launch: stars, rocket rising, flame, earth arc
    vgrad(draw, (x0, y0, x1, y1), (10, 18, 44), (4, 8, 22))
    for sx, sy in [(28, 16), (90, 30), (170, 12), (250, 26), (130, 44),
                   (210, 48), (60, 52)]:
        draw.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3],
                     fill=(240, 240, 220))
    cx = (x0 + x1) // 2
    # flame
    burst(draw, cx, y1 - 26, 22, (232, 120, 40))
    burst(draw, cx, y1 - 22, 12, (248, 200, 90))
    # rocket body
    draw.rectangle([cx - 12, y0 + 12, cx + 12, y1 - 34], fill=(233, 228, 214))
    draw.polygon([(cx - 12, y0 + 12), (cx + 12, y0 + 12), (cx, y0 - 2)],
                 fill=(178, 28, 28))
    draw.rectangle([cx - 22, y1 - 52, cx - 12, y1 - 34], fill=(178, 28, 28))
    draw.rectangle([cx + 12, y1 - 52, cx + 22, y1 - 34], fill=(178, 28, 28))
    draw.ellipse([cx - 6, y0 + 22, cx + 6, y0 + 34], fill=(24, 96, 122))
    # earth arc
    pts = [(x0, y1 - 2)]
    for k in range(25):
        t = k / 24
        x = x0 + t * (x1 - x0)
        y = y1 - 2 - 14 * math.sin(math.pi * t)
        pts.append((x, y))
    pts.append((x1, y1 - 2))
    draw.polygon(pts, fill=(24, 96, 122))


def pearl_tower(draw, x0, y0, x1, y1):
    # dusk Shanghai skyline with the Oriental Pearl Tower
    vgrad(draw, (x0, y0, x1, y1), (196, 120, 66), (96, 52, 66))
    sun(draw, x1 - 44, y0 + 22, 16, (248, 236, 200))
    cx = x0 + 70
    # pearl tower: needle + two spheres
    draw.rectangle([cx - 3, y0 + 8, cx + 3, y1 - 6], fill=(40, 34, 44))
    draw.ellipse([cx - 16, y0 + 14, cx + 16, y0 + 46], fill=(178, 28, 28))
    draw.ellipse([cx - 22, y0 + 34, cx + 22, y0 + 78], fill=(216, 210, 192))
    draw.rectangle([cx - 26, y1 - 22, cx + 26, y1 - 6], fill=(40, 34, 44))
    # neighbouring towers
    skyline(draw, x0 + 110, y1 - 6, x1 - 8, (30, 26, 34), seed=5)
    # red seal
    draw.rectangle([x1 - 52, y0 + 10, x1 - 14, y0 + 48], fill=(178, 28, 28))
    draw.ellipse([x1 - 44, y0 + 18, x1 - 22, y0 + 40], fill=(248, 244, 232))


def sea_drone(draw, x0, y0, x1, y1):
    # night sea: drone boat, burning ship, waves
    vgrad(draw, (x0, y0, x1, y1), (12, 30, 58), (6, 14, 34))
    for sx, sy in [(36, 14), (120, 26), (210, 12), (270, 30)]:
        draw.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3],
                     fill=(240, 240, 220))
    # burning ship silhouette
    draw.polygon([(x0 + 150, y1 - 26), (x0 + 290, y1 - 26), (x0 + 268, y1 - 8),
                  (x0 + 172, y1 - 8)], fill=(16, 18, 28))
    draw.rectangle([x0 + 196, y1 - 44, x0 + 224, y1 - 26], fill=(16, 18, 28))
    burst(draw, x0 + 230, y1 - 52, 20, (232, 120, 40))
    burst(draw, x0 + 230, y1 - 52, 11, (248, 200, 90))
    # drone boat
    draw.polygon([(x0 + 30, y1 - 18), (x0 + 92, y1 - 18), (x0 + 80, y1 - 6),
                  (x0 + 42, y1 - 6)], fill=(200, 205, 220))
    draw.line([(x0 + 60, y1 - 18), (x0 + 60, y1 - 34)], fill=(200, 205, 220),
              width=3)
    draw.ellipse([x0 + 56, y1 - 40, x0 + 64, y1 - 32], fill=(232, 120, 40))
    for yy in (y1 - 12,):
        for xx in range(x0 + 8, x1 - 8, 40):
            draw.arc([xx, yy, xx + 30, yy + 12], 0, 180,
                     fill=(160, 200, 220), width=2)


def dusk_city(draw, x0, y0, x1, y1):
    # dusk skyline, tallest tower hit, smoke
    vgrad(draw, (x0, y0, x1, y1), (150, 84, 96), (52, 38, 62))
    sun(draw, x0 + 46, y0 + 24, 15, (248, 200, 120))
    skyline(draw, x0 + 8, y1 - 6, x1 - 90, (26, 22, 32), seed=9)
    # tallest tower
    tx = x1 - 64
    draw.rectangle([tx - 16, y0 + 6, tx + 16, y1 - 6], fill=(22, 18, 28))
    draw.rectangle([tx - 4, y0 - 2, tx + 4, y0 + 8], fill=(22, 18, 28))
    burst(draw, tx, y0 + 22, 16, (232, 120, 40))
    burst(draw, tx, y0 + 22, 8, (248, 200, 90))
    for ox, oy, r in [(tx - 26, y0 + 10, 7), (tx + 24, y0 + 4, 6)]:
        draw.ellipse([ox - r, oy - r, ox + r, oy + r], fill=(200, 200, 200))


def circuit(draw, x0, y0, x1, y1):
    # dark blue circuit board + padlock
    vgrad(draw, (x0, y0, x1, y1), (16, 34, 70), (8, 16, 40))
    for (ax, ay, bx, by) in [(14, 14, 90, 14), (90, 14, 90, 44),
                             (200, 50, 280, 50), (280, 50, 280, 18),
                             (40, 48, 40, 20), (150, 30, 150, 54)]:
        draw.line([(x0 + ax, y0 + ay), (x0 + bx, y0 + by)], fill=(60, 110, 180),
                  width=2)
    for (nx, ny) in [(14, 14), (90, 44), (200, 50), (280, 18), (40, 20),
                     (150, 54)]:
        draw.ellipse([x0 + nx - 4, y0 + ny - 4, x0 + nx + 4, y0 + ny + 4],
                     fill=(232, 164, 66))
    # padlock
    cx, cy = (x0 + x1) // 2 + 40, y0 + 34
    draw.arc([cx - 16, cy - 26, cx + 16, cy + 2], 180, 360,
             fill=(200, 205, 220), width=5)
    draw.rounded_rectangle([cx - 24, cy - 6, cx + 24, cy + 26], radius=4,
                           fill=(232, 164, 66))
    draw.ellipse([cx - 4, cy + 4, cx + 4, cy + 12], fill=(16, 32, 66))
    draw.line([(cx, cy + 10), (cx, cy + 18)], fill=(16, 32, 66), width=3)

# ---------------------------------------------------------------- canvas
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# masthead
d.rectangle([0, 0, W, 128], fill=NAVY)
d.text((28, 18), "THE WORLD", font=font(SERIF_B, 92), fill=(248, 244, 232))
d.text((620, 30), "WEDNESDAY 25 NOVEMBER 2026", font=font(SANS_B, 24),
       fill=(248, 244, 232))
d.rectangle([620, 72, 996, 76], fill=(180, 83, 9))
d.text((620, 86), "ONE DAY  ·  SIX STORIES", font=font(SANS, 20),
       fill=(200, 205, 220))
d.rectangle([0, 128, W, 134], fill=RED)

# ------------------------------------------------------------- hero image
hx0, hy0, hx1, hy1 = 28, 152, 560, 470
courthouse(d, hx0, hy0, hx1, hy1)
d.rectangle([hx0, hy1 - 4, hx1, hy1], fill=(18, 30, 58))

# hero text
tx = 584
d.text((tx, 158), "NEW YORK", font=font(SANS_B, 26), fill=RED)
y = text_block(d, (tx, 192), "HUAWEI GUILTY IN U.S. FRAUD TRIAL",
               font(SANS_B, 46), INK, 412, leading=52)
y += 8
text_block(d, (tx, y),
           "A Brooklyn jury convicts Huawei on 10 of 12 counts — bank "
           "fraud, wire fraud, sanctions breaches and trade-secret theft. "
           "It is acquitted of racketeering.",
           font(SANS, 22), (40, 52, 84), 412, leading=29)

d.rectangle([28, 486, W - 28, 490], fill=INK)

# ------------------------------------------------------------- grid
ART = {"rocket": rocket, "gate": pearl_tower, "sea": sea_drone,
       "dusk": dusk_city, "circuit": circuit}

row1 = [
    ("JIUQUAN", "PAKISTAN'S FIRST ASTRONAUT IN ORBIT",
     "Shenzhou-24 lifts off with Muhammad Zeeshan Ali — the first "
     "Pakistani in orbit and the first foreigner aboard Tiangong.",
     "rocket"),
    ("BEIJING", "XI PURGES SHANGHAI BOSS",
     "Chen Jining, Shanghai party chief and Politburo member, is placed "
     "under a graft probe — the fourth to fall since 2025.",
     "gate"),
    ("BENGHAZI", "UKRAINE'S DRONES SINK RUSSIAN SHIP",
     "Sea drones sink the corvette Merkury and hit a cargo ship off "
     "Libya; Zelensky calls it self-defence. Two Libyan officers die.",
     "sea"),
]
row2 = [
    ("RIYADH", "HOUTHIS HIT RIYADH TOWER",
     "A drone strikes a tower in the capital's financial district, "
     "injuring 11. The coalition orders Hodeidah evacuated; Jeddah is "
     "threatened. A container ship hits a mine in Hormuz.",
     "dusk"),
    ("WASHINGTON", "CIA, SPY CHIEFS HACKED",
     "Intruders breach an unclassified network used by the CIA and ODNI "
     "for open-source intelligence. No classified data is hit; signs "
     "point to China.",
     "circuit"),
]

for i, (kicker, head, body, kind) in enumerate(row1):
    cx = 28 + i * (312 + 16)
    cy = 504
    ix0, iy0, ix1, iy1 = cx, cy, cx + 312, cy + 64
    ART[kind](d, ix0, iy0, ix1, iy1)
    d.rectangle([ix0, iy1 - 3, ix1, iy1], fill=RED)
    d.text((cx, cy + 70), kicker, font=font(SANS_B, 16), fill=RED)
    y = text_block(d, (cx, cy + 92), head, font(SANS_B, 22), INK, 312,
                   leading=24)
    text_block(d, (cx, y + 3), body, font(SANS, 16), (52, 60, 80), 312,
               leading=19)

for i, (kicker, head, body, kind) in enumerate(row2):
    cx = 28 + i * (476 + 16)
    cy = 718
    ix0, iy0, ix1, iy1 = cx, cy, cx + 476, cy + 64
    ART[kind](d, ix0, iy0, ix1, iy1)
    d.rectangle([ix0, iy1 - 3, ix1, iy1], fill=RED)
    d.text((cx, cy + 70), kicker, font=font(SANS_B, 16), fill=RED)
    y = text_block(d, (cx, cy + 92), head, font(SANS_B, 22), INK, 476,
                   leading=24)
    text_block(d, (cx, y + 3), body, font(SANS, 16), (52, 60, 80), 476,
               leading=19)

# footer ticker
d.rectangle([0, 924, W, 928], fill=INK)
d.rectangle([0, 928, W, H], fill=NAVY)
d.text((28, 942), "ALSO:  Trump pardons the Thanksgiving turkeys  ·  Nvidia "
       "slides despite Huang's return  ·  Seoul subway strike called off",
       font=font(SANS, 16), fill=(220, 224, 232))
d.text((28, 972), "WEDNESDAY 25 NOVEMBER 2026  ·  SIX STORIES, ONE DAY",
       font=font(SANS_B, 16), fill=(180, 190, 205))

img.save("entry.png", optimize=True)
print("saved entry.png")
from PIL import Image as _I
_im = _I.open("entry.png")
print(_im.size, _im.format, len(open("entry.png", "rb").read()), "bytes")
