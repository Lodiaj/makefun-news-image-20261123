#!/usr/bin/env python3
"""Draw the news poster for Monday 23 November 2026.

A newspaper front page, 1024x1024: masthead with the date, one lead story
(COP31 collapse) and eleven more stories from the day, each with a small
drawn pictogram, a kicker, a headline and a one-line deck. Deterministic:
the same bytes on every run.
"""
import hashlib
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 227)
INK = (17, 17, 17)
RED = (155, 27, 27)
GREY = (90, 86, 76)
RULE = (17, 17, 17)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# --- small pictograms, one per story (simple geometry, muted colours) ---
def icon_globe(d, x, y, s):
    d.ellipse([x, y, x + s, y + s], fill=(46, 110, 62))
    d.ellipse([x + s * 0.18, y + s * 0.15, x + s * 0.82, y + s * 0.85],
              outline=(246, 241, 227), width=3)
    d.line([x, y + s * 0.5, x + s, y + s * 0.5], fill=(246, 241, 227), width=3)


def icon_burst(d, x, y, s):
    cx, cy = x + s / 2, y + s / 2
    pts = []
    import math
    for i in range(12):
        r = s * 0.48 if i % 2 == 0 else s * 0.2
        a = math.pi * i / 6 - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=(196, 90, 20))
    d.ellipse([cx - s * 0.14, cy - s * 0.14, cx + s * 0.14, cy + s * 0.14],
              fill=(246, 241, 227))


def icon_waves(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(38, 84, 138))
    for k, yy in enumerate([0.28, 0.5, 0.72]):
        d.arc([x + s * 0.08, y + s * yy, x + s * 0.92, y + s * (yy + 0.34)],
              start=200, end=340, fill=(246, 241, 227), width=4)


def icon_city(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(96, 96, 100))
    for bx, bw, bh in [(0.08, 0.22, 0.62), (0.36, 0.26, 0.82), (0.68, 0.2, 0.5)]:
        d.rectangle([x + s * bx, y + s * (1 - bh), x + s * (bx + bw), y + s * 0.92],
                    fill=(246, 241, 227))


def icon_truck(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(155, 27, 27))
    d.rectangle([x + s * 0.12, y + s * 0.3, x + s * 0.58, y + s * 0.62],
                fill=(246, 241, 227))
    d.rectangle([x + s * 0.6, y + s * 0.42, x + s * 0.84, y + s * 0.62],
                fill=(246, 241, 227))
    for cx in (0.28, 0.72):
        d.ellipse([x + s * (cx - 0.09), y + s * 0.58, x + s * (cx + 0.09),
                   y + s * 0.76], fill=(17, 17, 17))


def icon_flame(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(196, 90, 20))
    d.polygon([(x + s * 0.5, y + s * 0.12), (x + s * 0.78, y + s * 0.55),
               (x + s * 0.62, y + s * 0.88), (x + s * 0.38, y + s * 0.88),
               (x + s * 0.22, y + s * 0.55)], fill=(246, 241, 227))


def icon_boat(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(38, 84, 138))
    d.polygon([(x + s * 0.14, y + s * 0.52), (x + s * 0.86, y + s * 0.52),
               (x + s * 0.72, y + s * 0.78), (x + s * 0.28, y + s * 0.78)],
              fill=(246, 241, 227))
    d.line([x + s * 0.5, y + s * 0.16, x + s * 0.5, y + s * 0.52],
           fill=(246, 241, 227), width=3)


def icon_star(d, x, y, s):
    import math
    cx, cy = x + s / 2, y + s / 2
    pts = []
    for i in range(10):
        r = s * 0.46 if i % 2 == 0 else s * 0.19
        a = math.pi * i / 5 - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.rectangle([x, y, x + s, y + s], fill=(110, 72, 32))
    d.polygon(pts, fill=(246, 241, 227))


def icon_chip(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(46, 110, 62))
    d.rectangle([x + s * 0.24, y + s * 0.24, x + s * 0.76, y + s * 0.76],
                fill=(246, 241, 227))
    for k in range(3):
        yy = y + s * (0.3 + 0.2 * k)
        d.line([x + s * 0.06, yy, x + s * 0.24, yy], fill=(246, 241, 227), width=3)
        d.line([x + s * 0.76, yy, x + s * 0.94, yy], fill=(246, 241, 227), width=3)


def icon_coin(d, x, y, s):
    d.ellipse([x, y, x + s, y + s], fill=(176, 138, 30))
    d.text((x + s * 0.5, y + s * 0.5), "$", font=font(SANS_B, int(s * 0.52)),
           fill=(246, 241, 227), anchor="mm")


def icon_shield(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(38, 56, 96))
    d.polygon([(x + s * 0.5, y + s * 0.1), (x + s * 0.85, y + s * 0.26),
               (x + s * 0.85, y + s * 0.55), (x + s * 0.5, y + s * 0.9),
               (x + s * 0.15, y + s * 0.55), (x + s * 0.15, y + s * 0.26)],
              fill=(246, 241, 227))


ICONS = {
    "globe": icon_globe, "burst": icon_burst, "waves": icon_waves,
    "city": icon_city, "truck": icon_truck, "flame": icon_flame,
    "boat": icon_boat, "star": icon_star, "chip": icon_chip,
    "coin": icon_coin, "shield": icon_shield,
}

STORIES = [
    # (icon, kicker, headline, deck) — 8 cards in the grid; 3 more run
    # as one-liners in the bottom strip (Seoul, Nvidia, FBI).
    ("burst", "IRAN WAR",
     "IRAN HITS US BASES IN BAHRAIN",
     "Missile and drone assault on US positions in Bahrain; two hurt."),
    ("waves", "UKRAINE",
     "SEA DRONES HIT RUSSIAN SHIPS",
     "Kyiv says naval drones struck two Russian ships off Libya."),
    ("city", "UKRAINE",
     "15 KILLED IN STRIKES AROUND KYIV",
     "Russian strikes hit the Kyiv region; a boy is pulled alive."),
    ("truck", "GAZA",
     "THREE KILLED AS ISRAEL HITS TRUCK",
     "Strike hits a food truck; settler arson called \u201cJewish terrorism\u201d."),
    ("flame", "INDONESIA",
     "FACTORY FIRE KILLS 24",
     "Blaze at a sweets factory leaves dozens missing."),
    ("boat", "NIGERIA",
     "24 DEAD AS BOAT CAPSIZES",
     "A boat carrying mourners to a funeral overturns in Bayelsa."),
    ("star", "MEXICO",
     "\u201cEL CHAPO ISIDRO\u201d CAPTURED",
     "Mexican forces seize a cartel boss on the FBI\u2019s most wanted list."),
    ("coin", "MARKETS",
     "BITCOIN REBOUNDS TO $61,000",
     "Crypto climbs back from a two-year low as futures recover."),
]


def build(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # outer frame
    d.rectangle([20, 20, W - 21, H - 21], outline=INK, width=3)
    d.rectangle([28, 28, W - 29, H - 29], outline=INK, width=1)

    # ---- masthead ----
    mast = font(SERIF_B, 96)
    d.text((W / 2, 44), "THE WORLD", font=mast, fill=INK, anchor="mt")
    d.line([48, 138, W - 48, 138], fill=RULE, width=3)
    date_f = font(SANS_B, 27)
    d.text((W / 2, 150), "MONDAY, 23 NOVEMBER 2026", font=date_f, fill=RED,
           anchor="mt")
    sub_f = font(SANS, 21)
    d.text((W / 2, 186), "ONE DAY  \u00b7  TWELVE STORIES  \u00b7  FROM AROUND THE GLOBE",
           font=sub_f, fill=GREY, anchor="mt")
    d.line([48, 218, W - 48, 218], fill=RULE, width=2)

    # ---- lead story: COP31 ----
    lx, ly, lw = 48, 234, W - 96
    kick_f = font(SANS_B, 22)
    d.text((lx, ly), "CLIMATE  \u2014  COP31 IN TURKEY", font=kick_f, fill=RED)
    head_f = font(SERIF_B, 56)
    lines = wrap(d, "CLIMATE TALKS COLLAPSE", head_f, lw)
    y = draw_text_block(d, lx, ly + 32, lines, head_f, INK, 62)
    deck_f = font(SANS, 25)
    deck = ("The UN summit ends with no deal after the longest climate "
            "conference in history, split over fossil fuels and money.")
    lines = wrap(d, deck, deck_f, lw)
    draw_text_block(d, lx, y + 6, lines, deck_f, INK, 32)
    d.line([48, 412, W - 48, 412], fill=RULE, width=2)

    # ---- grid: 2 columns x 4 rows ----
    gx, gy = 48, 428
    col_w = 464
    gutter = 16
    row_h = 125
    k_f = font(SANS_B, 15)
    h_f = font(SERIF_B, 25)
    de_f = font(SANS, 18)
    for i, (icon, kicker, head, deck) in enumerate(STORIES):
        col = i % 2
        row = i // 2
        x = gx + col * (col_w + gutter)
        y = gy + row * row_h
        ICONS[icon](d, x, y + 4, 78)
        tx = x + 92
        tw = col_w - 92
        d.text((tx, y), kicker, font=k_f, fill=RED)
        lines = wrap(d, head, h_f, tw)[:2]
        yy = draw_text_block(d, tx, y + 18, lines, h_f, INK, 28)
        lines = wrap(d, deck, de_f, tw)[:2]
        draw_text_block(d, tx, yy + 1, lines, de_f, INK, 21)
        if row < 3:
            d.line([x, y + row_h - 4, x + col_w, y + row_h - 4],
                   fill=(200, 192, 172), width=1)

    # ---- bottom strip: three more stories as one-liners ----
    by = 428 + 4 * row_h + 6
    d.line([48, by, W - 48, by], fill=RULE, width=2)
    strip_f = font(SANS_B, 18)
    d.text((48, by + 12),
           "SEOUL SHUFFLES CABINET  \u00b7  HUANG BACK AT NVIDIA  \u00b7  FBI PROBES DATABASE HACK",
           font=strip_f, fill=INK)
    strip2_f = font(SANS, 18)
    d.text((48, by + 38),
           "ALSO: Belgium flights grounded  \u00b7  UN chief urges AI rules  \u00b7  Skubal signs $450M Mets deal.",
           font=strip2_f, fill=GREY)

    img.save(out_path, format="PNG", compress_level=6)
    return out_path


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    build(out)
    data = open(out, "rb").read()
    print("wrote", out, len(data), "bytes")
    print("sha256", hashlib.sha256(data).hexdigest())
    im = Image.open(out)
    print("size", im.size, im.format)
