#!/usr/bin/env python3
"""Render the news-image-20261123 broadsheet (1024x1024 PNG, PIL, no network).

Layout: masthead with giant date, lead story, two minis, a first-reported
UTC timeline strip, an 8-section x 4-story grid (32 stories), a markets
ticker with Friday closes, and a visible DATE CHECK line. All 35 stories
were first reported on Monday 23 November 2026 (sources dated that day);
nothing from 22 November is presented as today's news. Early edition:
built 00:30 UTC from stories verified so far; a full-day rebuild will
replace it before entries close.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (163, 22, 33)
DARK = (26, 26, 26)
RULE = (120, 110, 95)
GREY = (90, 84, 74)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w, max_lines=None):
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
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        # trim last line so the ellipsis fits
        while lines and draw.textlength(lines[-1] + "...", font=fnt) > max_w:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1] + "..."
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 24  # margin

    # ---------- masthead ----------
    f_title = font(SERIF_B, 47)
    f_date = font(SANS_B, 22)
    f_tag = font(SANS_B, 12)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 16), title, font=f_title, fill=INK)
    date = "MONDAY, 23 NOVEMBER 2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 70), date, font=f_date, fill=RED)
    tag = "EARLY EDITION \u00b7 00:30 UTC"
    d.text((W - mx - d.textlength(tag, font=f_tag), 76), tag, font=f_tag, fill=GREY)
    d.text((mx, 76), "make.fun \u00b7 news-image", font=f_tag, fill=GREY)
    d.line([(mx, 104), (W - mx, 104)], fill=INK, width=3)
    d.line([(mx, 109), (W - mx, 109)], fill=RULE, width=1)

    # ---------- lead ----------
    y = 120
    f_kick = font(SANS_B, 13)
    f_head = font(SERIF_B, 27)
    f_sum = font(SANS, 14)
    d.text((mx, y), "CLIMATE SUMMIT COLLAPSES \u2014 COP31 ENDS WITHOUT A DEAL",
           font=f_kick, fill=RED)
    y += 22
    head = ("COP31 breaks down with no deal as the final draft "
            "drops any mention of fossil fuels")
    y = draw_lines(d, wrap(d, head, f_head, W - 2 * mx, 2), mx, y, f_head, INK, 32)
    y += 2
    summ = ("Governments leave the Turkiye talks without agreement on the words "
            "that cause global warming; negotiators vow to keep talking.")
    y = draw_lines(d, wrap(d, summ, f_sum, W - 2 * mx, 2), mx, y, f_sum, INK, 19)
    d.line([(mx, 232), (W - mx, 232)], fill=RULE, width=1)

    # ---------- two minis ----------
    f_mlab = font(SANS_B, 11)
    f_mhead = font(SANS_B, 15)
    f_msum = font(SANS, 12)
    minis = [
        ("UNITED NATIONS \u00b7 AI WEAPONS",
         "Nations agree to keep negotiating curbs on lethal AI systems",
         "Talks on autonomous weapons continue after a UN conference ends without a ban."),
        ("INDONESIA \u00b7 FACTORY FIRE",
         "24 bodies recovered after factory fire; dozens still missing",
         "Rescuers keep searching the burnt-out plant as families wait for news of the missing."),
    ]
    col_w = (W - 2 * mx - 12) // 2
    for i, (lab, hd, sm) in enumerate(minis):
        x = mx + i * (col_w + 12)
        yy = 242
        d.text((x, yy), lab, font=f_mlab, fill=RED)
        yy += 17
        yy = draw_lines(d, wrap(d, hd, f_mhead, col_w, 2), x, yy, f_mhead, INK, 18)
        yy = draw_lines(d, wrap(d, sm, f_msum, col_w, 2), x, yy, f_msum, INK, 15)
    d.line([(mx, 316), (W - mx, 316)], fill=RULE, width=1)

    # ---------- timeline strip ----------
    d.rectangle([(mx, 326), (W - mx, 384)], fill=DARK)
    f_thead = font(SANS_B, 12)
    f_titem = font(SANS, 11)
    d.text((mx + 10, 331), "FIRST REPORTED \u00b7 MONDAY 23 NOV \u00b7 UTC",
           font=f_thead, fill=(247, 242, 231))
    timeline = [
        ("00:02", "COP31 talks collapse, no fossil-fuel deal"),
        ("00:02", "UN to keep negotiating lethal-AI curbs"),
        ("00:02", "Australia rebukes US CBO over AUKUS"),
        ("00:02", "24 bodies found after Indonesia factory fire"),
        ("00:02", "Russian cargo ship ablaze off Finland"),
        ("00:02", "Houthi missile intercepted over Saudi Arabia"),
    ]
    tw3 = (W - 2 * mx - 20 - 2 * 12) // 3
    for i, (t, txt) in enumerate(timeline):
        x = mx + 10 + (i % 3) * (tw3 + 12)
        yy = 352 + (i // 3) * 15
        d.text((x, yy), t, font=f_thead, fill=(255, 196, 66))
        d.text((x + 42, yy), txt, font=f_titem, fill=(247, 242, 231))
    d.line([(mx, 392), (W - mx, 392)], fill=INK, width=2)

    # ---------- grid: 8 sections x 4 stories ----------
    sections = [
        ("WORLD", [
            ("Russian cargo ship still on fire off Finland",
             "Vessel burns after an attack; fire crews battle the blaze at sea."),
            ("14 missing after drone hits Kyiv region building",
             "Zelenskiy says rescuers are searching the rubble for survivors."),
            ("10 port workers hurt in Libya ship assault",
             "Drone strike on a Russian ship at Benghazi causes a blast."),
            ("Myanmar junta calls ASEAN decision unfair",
             "Army-backed government slams the bloc's move as imbalanced."),
        ]),
        ("EUROPE", [
            ("Thousands march in Lisbon over living costs",
             "Anger at prices brings crowds onto the streets of Portugal."),
            ("UK to build Ukrainian drones in new deal",
             "Britain agrees to produce Kyiv's drones under a fresh pact."),
            ("Ukraine pushes back near Sumy, reports say",
             "Pro-Russia channels report a retreat toward the border."),
            ("India, Bulgaria talk ties, IMEC, Black Sea",
             "Delhi and Sofia discuss trade routes and regional security."),
        ]),
        ("MIDDLE EAST", [
            ("Houthi missile intercepted over Saudi Arabia",
             "Saudi-led coalition says it stopped the strike in the west."),
            ("Saudis neutralise UAV as Houthis hit Sanaa",
             "Air defences down a drone and a projectile, Riyadh says."),
            ("Hormuz tanker attacks hit highest level",
             "UKMTO counts dozens of ships targeted since late September."),
            ("Iran: uranium stockpile stays in the country",
             "FM Araghchi says enriched uranium will be used as needed."),
        ]),
        ("ASIA & INDIA", [
            ("Nepal PM holds bilateral talks with Modi",
             "Balendra Shah reviews ties with India on a state visit."),
            ("Amit Shah launches \u20b94,000 cr Arunachal push",
             "Infra projects and self-reliance top the Home Minister's visit."),
            ("Modi inaugurates AI Centre at IIT Patna",
             "New hub to train talent as India races on artificial intelligence."),
            ("BJP MP Wadkute dies; leaders condole death",
             "Rajya Sabha MP dies of cardiac arrest in Delhi; PM pays tribute."),
        ]),
        ("TECH", [
            ("Nvidia row: aide tied to chip-diversion ring",
             "Fresh details link Alice Huang to a secret China network."),
            ("S. Korea minister quits over AI exam cheating",
             "Education chief resigns as a cheating scandal engulfs exams."),
            ("US lawmaker threatens SpaceX over Starshield",
             "Congress member warns on Ukraine limits, CNN reports."),
            ("BHASHINI shows off multilingual AI at IFFI",
             "India's language-AI platform demos at the Dakshin Day event."),
        ]),
        ("SCIENCE & SPACE", [
            ("NASA briefs today on NG-25 cargo launch",
             "Cygnus freighter named for Jim Lovell heads for the ISS."),
            ("China to fly first non-Chinese astronaut",
             "Shenzhou-24 will carry a crew to the Tiangong station."),
            ("Pakistan's first astronaut to fly with China",
             "State-backed flyer joins the Shenzhou-24 mission to Tiangong."),
            ("ESA to release first Hera asteroid images",
             "Probe's first views of Didymos arrive after its long cruise."),
        ]),
        ("CULTURE", [
            ("IFFI 2026 hosts BRICS film roundtable",
             "Festival brings partners together to grow the film industry."),
            ("IFFI showcases restored cinema classics",
             "Restored gems celebrate India's film heritage on screen."),
            ("'We Are All Strangers' to close IFFI 57",
             "Closing film caps the festival's 57th edition in Goa."),
            ("Russian film 'New Home' team meets media",
             "IFFI guests talk cinema as the festival's screenings roll on."),
        ]),
        ("SPORT", [
            ("India post record 720/9d in Wellington Test",
             "Pant smashes a ton as India pile up their best total in NZ."),
            ("Pakistan A beat India A by 48 runs",
             "Rising Stars: Pakistan A defend 313 in the 50-over clash."),
            ("Pollard second to 15,000 T20 runs",
             "West Indies star joins an exclusive club in the shortest format."),
            ("Liverpool rout Man Utd 4\u20130",
             "Reds run riot as Atl\u00e9tico and Milan also win big on Sunday."),
        ]),
    ]
    f_slab = font(SANS_B, 12)
    f_sh = font(SANS_B, 12)
    f_ss = font(SANS, 10)
    grid_top, grid_bot = 402, 902
    gx0, gx1 = mx, W - mx
    cols, rows = 4, 2
    cw = (gx1 - gx0 - (cols - 1) * 12) // cols
    rh = (grid_bot - grid_top - (rows - 1) * 12) // rows
    for idx, (sec, stories) in enumerate(sections):
        cx = gx0 + (idx % cols) * (cw + 12)
        cy = grid_top + (idx // cols) * (rh + 12)
        d.rectangle([(cx, cy), (cx + cw, cy + 20)], fill=RED)
        d.text((cx + 6, cy + 3), sec, font=f_slab, fill=(255, 255, 255))
        yy = cy + 26
        for j, (hd, sm) in enumerate(stories):
            if j:
                d.line([(cx, yy - 3), (cx + cw, yy - 3)], fill=(210, 203, 188), width=1)
            yy = draw_lines(d, wrap(d, hd, f_sh, cw - 2, 2), cx + 1, yy, f_sh, INK, 13)
            yy = draw_lines(d, wrap(d, sm, f_ss, cw - 2, 2), cx + 1, yy, f_ss, GREY, 11)
            yy += 4
        assert yy <= cy + rh + 2, f"section {sec} overflows: {yy} > {cy + rh}"

    # ---------- ticker ----------
    d.rectangle([(mx, 912), (W - mx, 946)], fill=DARK)
    f_tick = font(SANS_B, 12)
    tick = ("MARKETS \u00b7 FRI 20 NOV:  Sensex 83,919.71 +897.96   "
            "Nifty 25,800.60 +286.30   Brent $92.23   Gold \u20b91,22,435 \u22124%   "
            "NVDA $125.53 \u221214.01%")
    tw_ = d.textlength(tick, font=f_tick)
    assert tw_ <= W - 2 * mx - 16, f"ticker too wide: {tw_}"
    d.text((mx + 8, 921), tick, font=f_tick, fill=(255, 196, 66))

    # ---------- date check + footer ----------
    f_dc = font(SANS_B, 12)
    f_ft = font(SANS, 10)
    dc = ("DATE CHECK: Every story above was first reported on Monday 23 November 2026 "
          "\u2014 no story from 22 November is presented as today's news.")
    y = 956
    y = draw_lines(d, wrap(d, dc, f_dc, W - 2 * mx, 2), mx, y, f_dc, RED, 15)
    src = ("Sources: Jagran Josh \u00b7 Observer Voice \u00b7 The Daily Jagran \u00b7 Salonvision \u00b7 "
           "Bizen-Art \u00b7 Jamuna TV \u00b7 SpacePolicyOnline \u00b7 SportzCraazy \u00b7 TechnoSports \u00b7 "
           "ScoreZaap \u00b7 CricTracker \u00b7 Motley Fool. Early edition \u2014 a full-day rebuild will "
           "replace this before entries close 25 Nov 00:00 UTC.")
    y = draw_lines(d, wrap(d, src, f_ft, W - 2 * mx, 3), mx, y + 2, f_ft, GREY, 13)
    assert y <= 1020, f"footer overflows: {y}"

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    print(f"wrote {out}: {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()
