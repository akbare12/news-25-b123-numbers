#!/usr/bin/env python3
"""Render entry.png for news-image-20261125 (b123-numbers).

Front page, 1024x1024, 50 stories: 3 heroes + 10 cards + 37 ALSO.
All stories are events of Wednesday, November 25, 2026.
Build-time only; the grader never runs this file (main.py is stdlib-only).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 14  # margin
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

INK = (17, 17, 17)
PAPER = (255, 255, 255)
RED = (200, 16, 46)
BLUE = (20, 71, 123)
TEAL = (14, 124, 123)
PURPLE = (91, 45, 142)
GOLD = (150, 100, 0)
GREY_BG = (242, 242, 242)
GREY_LINE = (210, 210, 210)
GREY_TXT = (90, 90, 90)
YELLOW = (255, 243, 205)
DARK = (26, 26, 46)
MAP_BG = (226, 236, 244)
LAND = (196, 214, 190)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(size, bold=False, serif=False):
    name = "DejaVuSerif-Bold.ttf" if serif else (
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, max_w, leading, fill=INK, max_lines=None):
    """Draw wrapped text; returns y after the last line."""
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=2)

    # ---------- masthead ----------
    d.text((M, 8), "THE WORLD IN ONE PAGE", font=font(30, bold=True, serif=True), fill=INK)
    date_txt = "WEDNESDAY, NOVEMBER 25, 2026"
    d.text((W - M - d.textlength(date_txt, font=font(15, bold=True)), 16),
           date_txt, font=font(15, bold=True), fill=RED)
    d.text((M, 46), "50 STORIES  •  3 HEROES  •  10 CARDS  •  37 ALSO  •  ALL FROM ONE DAY",
           font=font(11, bold=True), fill=GREY_TXT)
    d.rectangle([M, 60, W - M, 63], fill=RED)

    # ---------- heroes ----------
    heroes = [
        dict(color=RED, badge="20%", sub="CHINA 20%  •  EU 15%  •  VIETNAM 20%",
             head="Trump hits 14 trade partners with new tariffs",
             body="China faces 20%, the EU 15% and Vietnam 20% as Washington "
                  "targets industrial overcapacity.",
             why="Costs rise; supply chains shift."),
        dict(color=BLUE, badge="-6.16%", sub="SAMSUNG -9.9%  •  SK HYNIX -11.1%",
             head="Kospi crashes 6.16% as chip stocks tumble",
             body="A circuit breaker trips as foreigners sell KRW 1.95tn "
                  "in a rout led by chipmakers.",
             why="Billions wiped off Asia tech."),
        dict(color=PURPLE, badge="1st", sub="FIRST FOREIGN ASTRONAUT",
             head="Pakistan's Ali becomes first foreign astronaut on Tiangong",
             body="Muhammad Zeeshan Ali, 40, rides Shenzhou-24 to the station, "
                  "stays 5-10 days, then returns with Shenzhou-23.",
             why="China opens its station to the world."),
    ]
    hx, hy, hw, hh = M, 68, 326, 200
    for i, h in enumerate(heroes):
        x = hx + i * (hw + 8)
        d.rectangle([x, hy, x + hw, hy + hh], outline=GREY_LINE, width=1)
        # scene, 92 px tall (>= 85 px winner pattern)
        d.rectangle([x, hy, x + hw, hy + 92], fill=h["color"])
        d.text((x + 12, hy + 8), h["badge"], font=font(44, bold=True), fill=PAPER)
        d.text((x + 12, hy + 62), h["sub"], font=font(11, bold=True), fill=PAPER)
        if i == 2:  # tiny rocket, top-right corner, clear of the sub line
            rx, ry = x + hw - 44, hy + 8
            d.polygon([(rx + 10, ry), (rx + 20, ry + 14), (rx, ry + 14)], fill=PAPER)
            d.rectangle([rx, ry + 14, rx + 20, ry + 42], fill=PAPER)
            d.polygon([(rx + 10, ry + 54), (rx + 3, ry + 42), (rx + 17, ry + 42)],
                      fill=(255, 200, 60))
        y = hy + 98
        y = text_block(d, x + 10, y, h["head"], font(16, bold=True), hw - 20, 19, max_lines=2)
        y = text_block(d, x + 10, y + 2, h["body"], font(11), hw - 20, 14, max_lines=3)
        d.text((x + 10, hy + hh - 16), "WHY IT MATTERS: " + h["why"],
               font=font(9, bold=True), fill=h["color"])

    # ---------- DATE CHECK (2 lines) ----------
    dy = 276
    d.rectangle([M, dy, W - M, dy + 42], fill=YELLOW, outline=(220, 190, 90), width=1)
    d.text((M + 10, dy + 3), "DATE CHECK", font=font(12, bold=True), fill=RED)
    d.text((M + 118, dy + 3),
           "IN: 50 stories, all from 25 Nov - tariffs, Kospi, Shenzhou-24 lead.",
           font=font(12), fill=INK)
    d.text((M + 10, dy + 22),
           "LEFT OUT - Huawei verdict 24 Nov, PIF Tower attack 24 Nov, Sudan strikes 24 Nov, "
           "Nvidia CEO reinstated 23 Nov",
           font=font(12, bold=True), fill=INK)

    # ---------- 10 cards, 5 x 2 ----------
    cards = [
        ("GAZA", (120, 30, 30), "GAZA", "Hamas security chief killed",
         "Abuelouf dies in a Shati strike; his wife and two children are also killed."),
        ("BOGOR", (90, 60, 10), "9", "Gold mine collapse kills 9",
         "17 miners are trapped 100 m underground as rescuers dig through rubble."),
        ("IOWA", (40, 80, 40), "9,500", "9,500 lbs of lead azide seized",
         "The Army detonates the degraded explosives stockpile in a controlled blast."),
        ("CARTAGENA", (0, 110, 130), "76", "76 hostages walk free",
         "A rescue operation frees 76 hostages held in Cartagena."),
        ("CAIRO", (180, 60, 0), "31", "Tanker fire kills 31",
         "A fuel tanker overturns on a Cairo highway and bursts into flames."),
        ("SOLOMONS", (0, 90, 110), "$740M", "Australia signs $740M pact",
         "Canberra seals a $740M security and aid pact with the Solomon Islands."),
        ("NEW YORK", (60, 60, 120), "100th", "Macy's 100th parade delayed",
         "The 100th parade is postponed as a storm threatens the route."),
        ("MADRID", (140, 40, 90), "90", "Abrego Garcia: 90 days",
         "Abrego Garcia reaches Spain; a Madrid court sets 90 days in his case."),
        ("NVIDIA", (20, 90, 40), "-3.9%", "Nvidia slides 3.9%",
         "S&P puts the chipmaker on downgrade watch as AI shares sell off."),
        ("SPACEX", (30, 50, 90), "1M", "1 million satellites cleared",
         "The US authorizes SpaceX to deploy 1M satellites for AI data centers."),
    ]
    cw = (W - 2 * M - 4 * 8) // 5
    cy, chh = 326, 134
    for row in range(2):
        for col in range(5):
            k = row * 5 + col
            place, color, big, head, body = cards[k]
            x = M + col * (cw + 8)
            y = cy + row * (chh + 8)
            d.rectangle([x, y, x + cw, y + chh], outline=GREY_LINE, width=1)
            # mini-scene, 48 px tall (>= 45 px winner pattern)
            d.rectangle([x, y, x + cw, y + 48], fill=color)
            bf = font(28, bold=True)
            while d.textlength(big, font=bf) > cw - 16 and bf.size > 16:
                bf = font(bf.size - 2, bold=True)
            d.text((x + 8, y + 10), big, font=bf, fill=PAPER)
            d.text((x + cw - 8 - d.textlength(place, font=font(10, bold=True)), y + 30),
                   place, font=font(10, bold=True), fill=PAPER)
            yy = y + 52
            yy = text_block(d, x + 8, yy, head, font(12, bold=True), cw - 16, 14, max_lines=2)
            text_block(d, x + 8, yy + 1, body, font(10), cw - 16, 12, max_lines=3)
            d.text((x + 8, y + chh - 13), "C  •  R  •  CL", font=font(8), fill=GREY_TXT)

    # ---------- map: 13 pins + key ----------
    my = 606
    d.rectangle([M, my, M + 620, my + 144], fill=MAP_BG, outline=GREY_LINE, width=1)
    d.text((M + 8, my + 4), "WHERE IT HAPPENED", font=font(11, bold=True), fill=INK)
    # rough continents (stylised blobs)
    mx, mw, mh = M, 620, 144
    continents = [
        [(60, 30), (150, 22), (215, 38), (195, 68), (125, 82), (70, 62)],
        [(195, 86), (245, 82), (260, 116), (225, 140), (198, 116)],
        [(305, 32), (345, 22), (365, 40), (335, 56), (308, 50)],
        [(305, 62), (355, 56), (375, 86), (345, 122), (312, 100)],
        [(370, 22), (475, 16), (545, 30), (565, 60), (485, 80), (425, 76), (385, 50)],
        [(485, 106), (545, 100), (555, 124), (505, 130)],
    ]
    for poly in continents:
        d.polygon([(mx + px, my + py) for px, py in poly], fill=LAND)
    pins = [  # (lon, lat, name)
        (-77, 39, "Washington - tariffs"), (4, 51, "Brussels - EU tariff list"),
        (116, 40, "Beijing - China 20%"), (106, 21, "Hanoi - Vietnam 20%"),
        (127, 37, "Seoul - Kospi -6.16%"), (99, 40, "Jiuquan - Shenzhou-24"),
        (34, 31, "Gaza - Abuelouf killed"), (107, -6, "Bogor - mine collapse"),
        (-93, 42, "Iowa - 9,500 lbs"), (-75, 10, "Cartagena - 76 freed"),
        (31, 30, "Cairo - tanker fire"), (160, -9, "Honiara - $740M pact"),
        (-4, 40, "Madrid - 90 days"),
    ]
    # display offsets (dx, dy) to separate pins that would collide on the map
    offsets = {2: (12, -10), 3: (0, 0), 4: (0, 0), 5: (14, -8), 6: (-12, -8),
               7: (-14, -12), 11: (12, 12), 13: (-16, 10)}
    for i, (lon, lat, _name) in enumerate(pins, 1):
        px = mx + int((lon + 180) / 360 * mw)
        py = my + int((90 - lat) / 180 * mh)
        dx, dy = offsets.get(i, (0, 0))
        px += dx
        py += dy
        px = max(mx + 12, min(mx + mw - 12, px))
        py = max(my + 16, min(my + mh - 12, py))
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=PAPER, width=1)
        num = str(i)
        nf = font(9, bold=True)
        d.text((px - d.textlength(num, font=nf) / 2, py - 6), num, font=nf, fill=PAPER)
    # key list (right of map)
    kx = M + 620 + 12
    d.text((kx, my), "MAP KEY", font=font(11, bold=True), fill=RED)
    for i, (_lon, _lat, name) in enumerate(pins, 1):
        d.text((kx, my + 14 + (i - 1) * 10), "%d  %s" % (i, name),
               font=font(10), fill=INK)

    # ---------- ALSO: 37 items, 3 columns, 1 line each ----------
    ay = 758
    d.text((M, ay), "ALSO  •  C  R  CL", font=font(13, bold=True), fill=INK)
    d.rectangle([M, ay + 18, W - M, ay + 20], fill=RED)
    also = [
        "US growth revised to 4.3%; inflation stays high",
        "Bangladesh lifts garment wage 36% to $139",
        "UK net migration falls to lowest since 1997",
        "Sinner out long after knee surgery",
        "Taiwan comedian gets security over jokes",
        "London Museum reopens in Victorian market",
        "CIA, ODNI hit by breach of unclassified data",
        "Hungary, Ukraine make fresh start on trade",
        "Coast Guard finds all six in Mississippi crash",
        "India, Malaysia drill hostage rescue",
        "US charges 800+ in global anti-scam sweep",
        "Trump says war funding secured",
        "Gaza medics warn meningitis spreading",
        "WFP: wars put food aid for millions at risk",
        "Suits say ICE brutalized citizens in jail",
        "Trump floats pardon for Jensen Huang",
        "Rights group: Modi weakened institutions",
        "Stars defend director Panahi after sentence",
        "Far right leads polls before Spain snap vote",
        "Court bars US from punishing ICC liaisons",
        "Stars push Van Hollen for Democratic leader",
        "Kim inspects nuclear sites, urges nukes",
        "China urges US to fix tariff practices",
        "Duran Duran guitarist Andy Taylor dies at 65",
        "Musk pledges $18B SpaceX stock for US kids",
        "Trump warns Russia over widening Ukraine war",
        "Hunger Games prequel eyes $80M-$90M opening",
        "Intruders break into royal home Anmer Hall",
        "Lakers top Jazz; Doncic posts 28 and 8",
        "Hong Kong fire survivors demand answers",
        "Myanmar rebel with artificial leg fights on",
        "Airports court private cash for upgrades",
        "UK watchdog warns on AI as Meta ships Muse",
        "Japan data-center boom faces local revolt",
        "Canada student curbs test Carney talent push",
        "Army map: lead dust could drift to Missouri",
        "Democrat Broderick flips red Tennessee seat",
    ]
    assert len(also) == 37, "ALSO must be 37, got %d" % len(also)
    col_w = (W - 2 * M - 2 * 12) // 3
    af = font(10)
    for col in range(3):
        chunk = also[col * 13:(col + 1) * 13] if col < 2 else also[26:]
        x = M + col * (col_w + 12)
        for j, item in enumerate(chunk):
            d.text((x, ay + 26 + j * 13), "•  " + item, font=af, fill=INK)

    # ---------- number strip ----------
    sy = 950
    d.rectangle([M, sy, W - M, sy + 28], fill=DARK)
    strip = "20%   •   -6.16%   •   9,500 lbs   •   76   •   31   •   9   •   $740M   •   -3.9%   •   90 days   •   100th   •   1M   •   5-10 days"
    sf = font(13, bold=True)
    d.text(((W - d.textlength(strip, font=sf)) / 2, sy + 6), strip, font=sf, fill=PAPER)

    # ---------- footer ----------
    fy = 986
    d.text((M, fy), "Sources: Reuters, AP, BBC, CNN, Xinhua, Korea Exchange, pm.gov.au",
           font=font(11), fill=GREY_TXT)
    right = "ALL STORIES: 25 NOVEMBER 2026"
    d.text((W - M - d.textlength(right, font=font(11, bold=True)), fy),
           right, font=font(11, bold=True), fill=INK)

    img.save(OUT, optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
