#!/usr/bin/env python3
"""Draw one newspaper page summing up world news of Friday 27 November 2026.

Deterministic: no network, no clock, no randomness. Every run writes the
same bytes to ${MAKEFUN_OUTPUT_DIR:-/output}/entry.png (1024x1024 PNG).
Only the Python standard library and Pillow are used.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (22, 22, 22)
RED = (163, 22, 33)
BLUE = (31, 78, 121)
TEAL = (18, 110, 105)
GREY = (96, 92, 84)
LIGHT = (233, 227, 210)
SKY = (176, 203, 224)
SKY_DARK = (120, 155, 190)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
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


def para(draw, x, y, text, fnt, max_w, leading, color=INK):
    """Draw wrapped paragraph, return y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def headline(draw, x, y, text, fnt, max_w, leading):
    return para(draw, x, y, text, fnt, max_w, leading)


def kicker(draw, x, y, text, color=RED):
    draw.text((x, y), text, font=SANS_B(13), fill=color)
    return y + 20


def rule(draw, x0, x1, y, color=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def draw_parade_scene(draw, x0, y0, x1, y1):
    """Storm sky over a Manhattan street, one big balloon held low."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY, outline=INK, width=2)
    # cloud bands
    for i, cy in enumerate(range(y0 + 8, y0 + 78, 22)):
        shade = (150 + i * 8, 178 + i * 4, 200)
        draw.ellipse([x0 + 12 + (i % 3) * 96, cy, x0 + 132 + (i % 3) * 96, cy + 30],
                     fill=shade)
    # skyline
    base = y1 - 46
    bx = x0 + 10
    heights = [66, 92, 58, 104, 74, 88, 62]
    for h in heights:
        bw = 40
        draw.rectangle([bx, base - h + 46, bx + bw, y1 - 2], fill=(88, 96, 108))
        for wy in range(base - h + 56, y1 - 8, 14):
            for wx in range(bx + 6, bx + bw - 6, 10):
                draw.rectangle([wx, wy, wx + 4, wy + 6], fill=(214, 196, 130))
        bx += bw + 6
    # street
    draw.rectangle([x0, y1 - 46, x1, y1], fill=(70, 70, 74))
    draw.line([(x0, y1 - 24), (x1, y1 - 24)], fill=(240, 210, 90), width=3)
    # big balloon, tethered low in the wind
    cx, cy = (x0 + x1) // 2 + 30, y0 + 108
    draw.ellipse([cx - 88, cy - 52, cx + 88, cy + 52], fill=(196, 44, 52),
                 outline=INK, width=2)
    draw.ellipse([cx - 88, cy - 52, cx - 30, cy + 52], fill=(214, 84, 90))
    draw.arc([cx - 88, cy - 52, cx + 88, cy + 52], 20, 160, fill=INK, width=2)
    draw.line([(cx - 40, cy + 50), (cx - 26, y1 - 48)], fill=INK, width=2)
    draw.line([(cx + 40, cy + 50), (cx + 26, y1 - 48)], fill=INK, width=2)
    draw.rectangle([cx - 22, y1 - 62, cx + 22, y1 - 46], fill=(122, 74, 30),
                   outline=INK, width=2)
    # rain, slanted by the wind
    for i in range(26):
        rx = x0 + 14 + (i * 37) % (x1 - x0 - 28)
        ry = y0 + 12 + (i * 53) % 150
        draw.line([(rx, ry), (rx - 9, ry + 18)], fill=(240, 244, 248), width=2)
    draw.text((x0 + 10, y1 - 22), "A balloon held low: gusts hit 66 mph",
              font=SANS_B(12), fill=(255, 255, 255))


def draw_seat_chart(draw, x0, y0, width):
    """Horizontal bars: seats won by each party in New Zealand's House."""
    parties = [
        ("National", 40, BLUE),
        ("Labour", 36, RED),
        ("Greens", 17, (46, 139, 60)),
        ("ACT", 13, (240, 196, 40)),
        ("NZ First", 12, (60, 60, 60)),
        ("Opportunity", 7, TEAL),
        ("Te Pati Maori", 5, (120, 70, 130)),
    ]
    draw.text((x0, y0), "SEATS IN THE 130-SEAT HOUSE",
              font=SANS_B(12), fill=GREY)
    y = y0 + 16
    bar_max = width - 132
    for name, seats, color in parties:
        draw.text((x0, y), name, font=SANS(11), fill=INK)
        bx = x0 + 108
        bw = max(6, int(bar_max * seats / 40.0))
        draw.rectangle([bx, y + 1, bx + bw, y + 10], fill=color)
        draw.text((bx + bw + 5, y), str(seats), font=SANS_B(11), fill=INK)
        y += 13
    return y


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28
    rx = W - mx

    # ---- masthead ----
    d.text((W // 2, 14), "THE WORLD IN ONE DAY", font=SERIF_B(52),
           fill=INK, anchor="mt")
    rule(d, mx, rx, 78, RED, 4)
    d.text((mx, 88), "FRIDAY, 27 NOVEMBER 2026", font=SANS_B(17), fill=RED)
    d.text((rx, 88), "THE DAY'S NEWS  •  ONE PAGE", font=SANS_B(15),
           fill=GREY, anchor="rt")
    rule(d, mx, rx, 114, INK, 2)

    # ---- lead story: Macy's parade ----
    y = 126
    y = kicker(d, mx, y, "NEW YORK  •  FIRST POSTPONEMENT IN 100 YEARS")
    y = headline(d, mx, y, "STORM GROUNDS A CENTURY", SERIF_B(34), 600, 38)
    y = headline(d, mx, y + 2, "OF THANKSGIVING", SERIF_B(34), 600, 38)
    y = headline(d, mx, y + 4, "Macy's 100th parade moves to Saturday",
                 SERIF(24), 600, 30)
    lead_text = (
        "A powerful nor'easter swept the US East Coast on Thanksgiving Day, "
        "with gusts of 66 mph at LaGuardia and a record 2.18 inches of rain "
        "in Central Park. Macy's moved its milestone 100th parade to "
        "Saturday 28 November, 8:30 a.m. -- the first postponement in "
        "its 100-year history."
    )
    ty = y + 6
    ty = para(d, mx, ty, lead_text, SERIF(15), 596, 19)
    draw_parade_scene(d, 648, 126, rx, 344)
    d.text((648, 350), "The parade route: 2.5 miles to Herald Square.",
           font=SANS(12), fill=GREY)
    rule(d, mx, rx, 384, INK, 2)

    # ---- row A: New Zealand (left) + Ebola (right) ----
    y = 396
    y = kicker(d, mx, y, "WELLINGTON  •  FINAL COUNT")
    y = headline(d, mx, y, "New Zealand deadlocked", SERIF_B(24), 460, 28)
    y = headline(d, mx, y, "at 65 seats each", SERIF_B(24), 460, 28)
    y = para(d, mx, y + 4,
             "Final count of the 7 November election, released Friday: the "
             "ruling coalition falls to 65 of 130 seats, one short of a "
             "majority. Opportunity (7 seats) now decides who governs.",
             SERIF(13), 460, 18)
    cy = draw_seat_chart(d, mx, y + 6, 460)
    _ = cy

    x2 = 524
    y = 396
    y = kicker(d, x2, y, "EASTERN CONGO  •  HEALTH EMERGENCY", color=TEAL)
    y = headline(d, x2, y, "Ebola passes 12,000 cases", SERIF_B(24), 472, 28)
    y = headline(d, x2, y, "as fighting hampers the response",
                 SERIF_B(24), 472, 28)
    y = para(d, x2, y + 4,
             "Confirmed cases in eastern Congo topped 12,021, health "
             "ministry data showed Thursday, with 5,904 deaths -- the "
             "fastest-growing Ebola outbreak on record and the second "
             "largest ever. The Bundibugyo strain has no approved vaccine, "
             "and clashes are forcing some responders to evacuate.",
             SERIF(14), 472, 19)
    d.rectangle([x2, y + 6, rx, y + 54], fill=(250, 226, 222), outline=RED,
                width=2)
    d.text((x2 + 12, y + 11), "12,021 cases  •  5,904 deaths",
           font=SANS_B(19), fill=RED)
    d.text((x2 + 12, y + 34), "Second-largest Ebola outbreak on record",
           font=SANS(13), fill=INK)
    rule(d, mx, rx, 652, INK, 2)

    # ---- row B: three stories ----
    cols = [(mx, 306), (362, 306), (696, 300)]
    stories = [
        ("GULF OF OMAN  •  CONFLICT", RED,
         "US disables ship in Iran blockade",
         "A US aircraft fired precision munitions into the stern of the "
         "Palau-flagged bulk carrier Pacific Archer on Thursday, disabling "
         "its propulsion as it tried to run the blockade of Iranian ports. "
         "The crew was unharmed -- the 15th ship disabled since April; "
         "158 more were turned back."),
        ("MADRID  •  ELECTION SUNDAY", BLUE,
         "Spain votes as right leads polls",
         "Spain holds a snap general election on Sunday 29 November. Final "
         "polls put the conservative People's Party first, near 31%, with "
         "the Socialists close behind and far-right Vox third. Together the "
         "PP and Vox are projected above the 176 seats needed for a "
         "majority in the 350-seat Congress."),
        ("CHARLEROI, BELGIUM  •  SPACE", TEAL,
         "Europe opens its biggest satellite factory",
         "King Philippe inaugurated Europe's largest satellite factory in "
         "Charleroi this week. The Aerospacelab megafactory is designed to "
         "build up to 500 satellites a year for the EU's IRIS-2 secure "
         "communications network, a rival to Starlink. Production is "
         "targeted for the end of 2028."),
    ]
    y = 666
    for (cx, cw), (kick, color, head, body) in zip(cols, stories):
        yy = kicker(d, cx, y, kick, color=color)
        yy = headline(d, cx, yy, head, SERIF_B(19), cw, 23)
        yy = para(d, cx, yy + 3, body, SERIF(13), cw, 17)
    rule(d, mx, rx, 858, INK, 2)

    # ---- In Brief ----
    y = 870
    d.text((mx, y), "IN BRIEF", font=SANS_B(16), fill=RED)
    d.text((rx, y), "FRIDAY 27 NOVEMBER 2026", font=SANS_B(13), fill=GREY,
           anchor="rt")
    briefs = [
        ("KENYA: ", "A court convicted cult leader Paul Mackenzie over "
         "123 further deaths in the Shakahola starvation case."),
        ("WASHINGTON: ", "The US goods trade deficit widened to $149.5 "
         "billion in October, a record import bill, the Census Bureau said."),
        ("OTTAWA: ", "Canada's Supreme Court largely upheld Quebec's ban "
         "on religious symbols for some public-sector workers."),
    ]
    y += 26
    for bold, rest in briefs:
        line = bold + rest
        lines = wrap(d, line, SERIF(14), rx - mx)
        for ln in lines:
            d.text((mx, y), ln, font=SERIF(14), fill=INK)
            y += 18
        y += 4
    rule(d, mx, rx, 962, INK, 2)

    # ---- footer: sources ----
    d.text((mx, 972),
           "Sources: AP  •  Reuters  •  US Central Command  •  NZ Electoral "
           "Commission  •  DR Congo Ministry of Health  •  El Pais polling",
           font=SANS(12), fill=GREY)
    d.text((mx, 992),
           "Every story above happened or was first reported on 27 November "
           "2026.  •  Drawn with Pillow; no network used.",
           font=SANS(12), fill=GREY)

    img.save(os.path.join(out_dir, "entry.png"), format="PNG",
             optimize=True)


if __name__ == "__main__":
    main()
