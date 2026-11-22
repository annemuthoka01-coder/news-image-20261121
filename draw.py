import os
from PIL import Image, ImageDraw, ImageFont

S = 2

def X(v):
    return int(v * S)

PALETTE = {
    "PAPER": "#F7F2E4",
    "CARD": "#FFFDF6",
    "INK": "#16130E",
    "RED": "#B02A1E",
    "DBLUE": "#1E3A52",
    "SEA": "#7FA8BC",
    "SAND": "#D9C9A3",
    "GREEN": "#1E7A46",
    "AMBER": "#B97A14",
    "GREY": "#6B6659",
    "LINE": "#C9C2AE",
    "WHITE": "#FFFFFF",
}

FONT_PATHS = {
    "serifb": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "sansb": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
}

def F(kind, size):
    path = FONT_PATHS.get(kind)
    scaled_size = int(size * S)
    if path and os.path.exists(path):
        try:
            return ImageFont.truetype(path, scaled_size)
        except Exception:
            pass
    return ImageFont.load_default()

def wrap(d, text, font, width):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        w = d.textlength(test_line, font=font)
        if w <= width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    return lines if lines else [""]

def fit(d, text, kind, start_size, max_width):
    size = start_size
    while size > 6:
        font = F(kind, size)
        w = d.textlength(text, font=font)
        if w <= max_width:
            return font, size
        size -= 0.5
    return F(kind, size), size

def badge(d, x, y, level):
    text = "CONFIRMED" if level == "C" else "REPORTED"
    fill = PALETTE["GREEN"] if level == "C" else PALETTE["AMBER"]
    font = F("sansb", 8.5)
    bbox = d.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad_x = X(5)
    pad_y = X(3)
    bw = tw + pad_x * 2
    bh = th + pad_y * 2
    bx = X(x)
    by = X(y)
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=X(3), fill=fill)
    d.text((bx + pad_x, by + pad_y - X(1)), text, fill=PALETTE["WHITE"], font=font)
    return bw

def draw_band(d):
    d.rectangle([0, 0, X(1024), X(27)], fill=PALETTE["INK"])
    font_l = F("sansb", 13)
    d.text((X(24), X(6)), "THE WORLD IN ONE DAY", fill=PALETTE["WHITE"], font=font_l)
    font_r = F("sansb", 10)
    text_r = "40 STORIES · 9 REGIONS · EVERY ONE DATED SATURDAY 21 NOVEMBER 2026"
    tw = d.textlength(text_r, font=font_r)
    d.text((X(1000) - tw, X(8)), text_r, fill=PALETTE["WHITE"], font=font_r)

def draw_masthead(d):
    font_m, _ = fit(d, "Saturday 21 November 2026", "serifb", 66, X(952))
    bbox = d.textbbox((0, 0), "Saturday 21 November 2026", font=font_m)
    tw = bbox[2] - bbox[0]
    x_center = X(512) - tw / 2
    d.text((x_center, X(34)), "Saturday 21 November 2026", fill=PALETTE["INK"], font=font_m)

    strap = "Iran hits Bahrain bases · a deep quake shakes Peru · COP31 runs into overtime"
    font_s = F("serif", 16.5)
    sbox = d.textbbox((0, 0), strap, font=font_s)
    stw = sbox[2] - sbox[0]
    sx_center = X(512) - stw / 2
    d.text((sx_center, X(108)), strap, fill=PALETTE["INK"], font=font_s)

    d.rectangle([X(24), X(134), X(1000), X(137)], fill=PALETTE["INK"])
    d.line([X(24), X(140), X(1000), X(140)], fill=PALETTE["INK"], width=X(1))

def draw_timeline(d):
    font_lbl = F("sansb", 11)
    d.text((X(24), X(148)), "THE DAY IN UTC", fill=PALETTE["RED"], font=font_lbl)

    d.line([X(150), X(172), X(990), X(172)], fill=PALETTE["INK"], width=X(2))

    events = [
        (170, "00:09", "Peru quake, Junín"),
        (330, "05:00", "Tanker hit off Khasab"),
        (420, "05:50", "Second tanker hit"),
        (700, "14:10", "England v New Zealand"),
        (880, "17:30", "Arsenal at Newcastle"),
    ]

    font_time = F("serifb", 12.5)
    font_sub = F("sans", 9)

    for x_pos, t_str, l_str in events:
        cx = X(x_pos)
        cy = X(172)
        r = X(5)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PALETTE["INK"])

        tb = d.textbbox((0, 0), t_str, font=font_time)
        tw = tb[2] - tb[0]
        d.text((cx - tw / 2, X(150)), t_str, fill=PALETTE["INK"], font=font_time)

        lines = wrap(d, l_str, font_sub, X(118))
        ly = X(180)
        for line in lines:
            lb = d.textbbox((0, 0), line, font=font_sub)
            lw = lb[2] - lb[0]
            d.text((cx - lw / 2, ly), line, fill=PALETTE["INK"], font=font_sub)
            ly += X(11)

def draw_stats(d):
    stats = [
        ("6.7", "quake magnitude, central Peru (USGS)"),
        ("2", "tankers hit off Khasab, Oman (UKMTO)"),
        ("98.5%", "of EU-goods tariffs lifted by Indonesia deal (Euronews)"),
        ("82,500", "marched across France on Saturday (Interior Ministry)"),
        ("37-12", "England's record win over All Blacks (Reuters)"),
        ("24M", "barrels of Saudi crude to be stored in Japan (Japan Today)"),
    ]

    total_w = X(1000) - X(24)
    gap = X(6)
    n = len(stats)
    box_w = (total_w - gap * (n - 1)) / n
    box_h = X(58)
    y0 = X(198)

    font_val = F("serifb", 24)
    font_lbl = F("sans", 8.5)

    for i, (val, lbl) in enumerate(stats):
        bx = X(24) + i * (box_w + gap)
        d.rectangle([bx, y0, bx + box_w, y0 + box_h], fill=PALETTE["CARD"], outline=PALETTE["LINE"], width=X(1))
        d.rectangle([bx, y0, bx + X(4), y0 + box_h], fill=PALETTE["RED"])

        d.text((bx + X(10), y0 + X(3)), val, fill=PALETTE["RED"], font=font_val)

        lines = wrap(d, lbl, font_lbl, box_w - X(16))
        ly = y0 + X(30)
        for line in lines[:2]:
            d.text((bx + X(10), ly), line, fill=PALETTE["INK"], font=font_lbl)
            ly += X(11)

def main():
    W = 1024 * S
    H = 1024 * S
    im = Image.new("RGB", (W, H), color=PALETTE["PAPER"])
    d = ImageDraw.Draw(im)

    draw_band(d)
    draw_masthead(d)
    draw_timeline(d)
    draw_stats(d)
    draw_leads(d)
    draw_minis(d)

    im_resized = im.resize((1024, 1024), Image.LANCZOS)
    im_resized.save("entry.png", "PNG")


def draw_leads(d):
    leads = [
        {
            "tag": "GULF · IRAN STRIKES",
            "badge": "CONFIRMED",
            "headline": "Iran strikes Bahrain bases; tankers hit off Oman",
            "deck": "Bahrain says an Iranian strike set a civilian plant ablaze, and the IRGC says it hit US radar at two bases. Two tankers were struck off Khasab - tanker hits are now at a wartime high.",
            "source": "AP · Reuters · UKMTO · FT",
            "type": "gulf",
        },
        {
            "tag": "PERU · EARTHQUAKE",
            "badge": "CONFIRMED",
            "headline": "Deep 6.7 quake shakes central Peru",
            "deck": "Centred near Junín and felt in Lima. Landslides and minor damage were reported, but no deaths and no tsunami threat.",
            "source": "USGS · IGP · AFP",
            "type": "peru",
        },
        {
            "tag": "CLIMATE · COP31",
            "badge": "CONFIRMED",
            "headline": "COP31 talks run into overtime in Antalya",
            "deck": "The summit blew past Friday's deadline over fossil fuels. A last-minute text went to a late-night plenary, with the approval session set for Sunday 06:00 GMT.",
            "source": "Reuters · Al Jazeera",
            "type": "cop31",
        },
    ]

    card_w = X(316)
    card_h = X(252)
    y0 = X(264)
    xs = [X(24), X(350), X(676)]

    font_tag = F("sansb", 10.5)
    font_head = F("serifb", 19.5)
    font_deck = F("sans", 10.5)
    font_source = F("sans", 8.5)

    for i, lead in enumerate(leads):
        x0 = xs[i]
        # Card background
        d.rectangle([x0, y0, x0 + card_w, y0 + card_h], fill=PALETTE["CARD"], outline=PALETTE["LINE"], width=X(1))

        # Padding inside card: X(8) left/right
        cx = x0 + X(8)
        cy = y0 + X(8)
        content_w = card_w - X(16)

        # Tag row
        d.text((cx, cy), lead["tag"], fill=PALETTE["RED"], font=font_tag)
        badge(d, (x0 + card_w - X(8) - X(65)) // S, cy // S, "C" if lead["badge"] == "CONFIRMED" else "R")
        cy += X(18)

        # Illustration area (height ~104)
        ill_h = X(104)
        ill_y = cy
        d.rectangle([cx, ill_y, cx + content_w, ill_y + ill_h], fill=PALETTE["SAND"] if lead["type"] != "cop31" else "#DDEBD2", outline=PALETTE["LINE"], width=X(1))

        if lead["type"] == "gulf":
            # Sea fill background for gulf map
            d.rectangle([cx, ill_y, cx + content_w, ill_y + ill_h], fill="#C5D5E4")
            # Iran polygon at top right
            d.polygon([
                (cx + content_w * 0.4, ill_y),
                (cx + content_w, ill_y),
                (cx + content_w, ill_y + ill_h * 0.5),
                (cx + content_w * 0.7, ill_y + ill_h * 0.4),
            ], fill=PALETTE["SAND"], outline=PALETTE["LINE"])
            d.text((cx + content_w * 0.65, ill_y + X(8)), "IRAN", fill=PALETTE["INK"], font=F("sansb", 9))

            # Oman along bottom
            d.polygon([
                (cx, ill_y + ill_h),
                (cx + content_w, ill_y + ill_h),
                (cx + content_w, ill_y + ill_h * 0.75),
                (cx, ill_y + ill_h * 0.8),
            ], fill=PALETTE["SAND"], outline=PALETTE["LINE"])
            d.text((cx + content_w * 0.65, ill_y + ill_h * 0.78), "OMAN", fill=PALETTE["INK"], font=F("sansb", 9))

            # Bahrain island left-centre with red burst
            bx = cx + content_w * 0.3
            by = ill_y + ill_h * 0.5
            d.ellipse([bx - X(10), by - X(6), bx + X(10), by + X(6)], fill=PALETTE["SAND"], outline=PALETTE["LINE"])
            d.text((bx - X(14), by - X(16)), "BAHRAIN", fill=PALETTE["INK"], font=F("sansb", 8))
            # Red star burst
            d.polygon([(bx, by - X(8)), (bx + X(3), by - X(2)), (bx + X(9), by), (bx + X(3), by + X(2)), (bx, by + X(8)), (bx - X(3), by + X(2)), (bx - X(9), by), (bx - X(3), by - X(2))], fill=PALETTE["RED"])

            # Tankers with orange-red bursts
            tx1 = cx + content_w * 0.48
            ty1 = ill_y + ill_h * 0.55
            d.rectangle([tx1, ty1, tx1 + X(16), ty1 + X(6)], fill=PALETTE["INK"])
            d.ellipse([tx1 + X(4), ty1 - X(4), tx1 + X(12), ty1 + X(2)], fill="#FF5500")

            tx2 = cx + content_w * 0.62
            ty2 = ill_y + ill_h * 0.62
            d.rectangle([tx2, ty2, tx2 + X(16), ty2 + X(6)], fill=PALETTE["INK"])
            d.ellipse([tx2 + X(4), ty2 - X(4), tx2 + X(12), ty2 + X(2)], fill="#FF5500")

            # Strait of Hormuz label
            d.text((cx + X(10), ill_y + ill_h * 0.35), "STRAIT OF HORMUZ", fill="#FFFFFF", font=F("sansb", 9))

        elif lead["type"] == "peru":
            # Sky strip top
            d.rectangle([cx, ill_y, cx + content_w, ill_y + ill_h * 0.25], fill="#EAE4D9")
            d.text((cx + X(6), ill_y + X(4)), "JUNÍN · 00:09 UTC", fill=PALETTE["INK"], font=F("sansb", 8.5))
            # Andes triangles
            d.polygon([(cx + X(80), ill_y + ill_h * 0.25), (cx + X(120), ill_y + ill_h * 0.05), (cx + X(160), ill_y + ill_h * 0.25)], fill="#B98A4A")
            d.polygon([(cx + X(140), ill_y + ill_h * 0.25), (cx + X(180), ill_y + ill_h * 0.08), (cx + X(220), ill_y + ill_h * 0.25)], fill="#8C6239")

            # Earth layers
            band_h = (ill_h * 0.75) / 3
            colors = ["#D4B08C", "#B98A4A", "#7A4A21"]
            for b_idx, col in enumerate(colors):
                by0 = ill_y + ill_h * 0.25 + b_idx * band_h
                d.rectangle([cx, by0, cx + content_w - X(40), by0 + band_h], fill=col)

            # Epicentre red star with concentric ellipses
            ep_x = cx + content_w * 0.4
            ep_y = ill_y + ill_h * 0.75
            for r_val in [X(24), X(16), X(8)]:
                d.ellipse([ep_x - r_val, ep_y - r_val * 0.6, ep_x + r_val, ep_y + r_val * 0.6], outline=PALETTE["RED"], width=X(1))
            d.polygon([(ep_x, ep_y - X(5)), (ep_x + X(2), ep_y - X(1)), (ep_x + X(5), ep_y), (ep_x + X(2), ep_y + X(1)), (ep_x, ep_y + X(5)), (ep_x - X(2), ep_y + X(1)), (ep_x - X(5), ep_y), (ep_x - X(2), ep_y - X(1))], fill=PALETTE["RED"])

            # Depth scale right side
            sx = cx + content_w - X(35)
            sy0 = ill_y + ill_h * 0.25
            sy1 = ill_y + ill_h
            d.line([sx, sy0, sx, sy1], fill=PALETTE["INK"], width=X(1))
            d.text((sx + X(4), sy0), "0 km", fill=PALETTE["INK"], font=F("sans", 8))
            d.text((sx + X(4), (sy0 + sy1) / 2), "50 km", fill=PALETTE["INK"], font=F("sans", 8))
            d.text((sx + X(4), sy1 - X(12)), "108-129 km", fill=PALETTE["INK"], font=F("sansb", 8))

        elif lead["type"] == "cop31":
            # Thermometer left
            tx = cx + X(30)
            ty_top = ill_y + X(15)
            ty_bot = ill_y + ill_h - X(15)
            d.rectangle([tx - X(4), ty_top, tx + X(4), ty_bot], fill="#FFFFFF", outline=PALETTE["INK"], width=X(1))
            # Red fill up to 1.5C line (70% up)
            fill_top = ty_bot - (ty_bot - ty_top) * 0.7
            d.rectangle([tx - X(3), fill_top, tx + X(3), ty_bot], fill=PALETTE["RED"])
            d.ellipse([tx - X(8), ty_bot - X(8), tx + X(8), ty_bot + X(8)], fill=PALETTE["RED"], outline=PALETTE["INK"], width=X(1))
            d.line([tx + X(6), fill_top, tx + X(20), fill_top], fill=PALETTE["RED"], width=X(1))
            d.text((tx + X(22), fill_top - X(6)), "1.5°C", fill=PALETTE["RED"], font=F("sansb", 9))

            # 13 day bars right
            bar_start_x = cx + X(110)
            bar_w = X(10)
            bar_gap = X(3)
            max_bh = ill_h - X(30)
            for d_i in range(13):
                bx = bar_start_x + d_i * (bar_w + bar_gap)
                bh = max_bh * (0.5 + 0.03 * d_i)
                if d_i == 12:
                    bh = max_bh * 0.95
                    bcol = PALETTE["RED"]
                else:
                    bcol = "#78A651"
                d.rectangle([bx, ill_y + ill_h - X(10) - bh, bx + bar_w, ill_y + ill_h - X(10)], fill=bcol)
            d.text((bar_start_x, ill_y + X(8)), "+1 DAY · DAY 13", fill=PALETTE["INK"], font=F("sansb", 8.5))

        cy += ill_h + X(8)

        # Headline (up to 2 lines)
        head_lines = wrap(d, lead["headline"], font_head, content_w)
        for line in head_lines[:2]:
            d.text((cx, cy), line, fill=PALETTE["INK"], font=font_head)
            cy += X(21)

        cy += X(2)

        # Deck (up to 4 lines)
        deck_lines = wrap(d, lead["deck"], font_deck, content_w)
        for line in deck_lines[:4]:
            d.text((cx, cy), line, fill=PALETTE["INK"], font=font_deck)
            cy += X(13)

        # Source line at bottom
        d.text((cx, y0 + card_h - X(16)), lead["source"], fill=PALETTE["GREY"], font=font_source)


def draw_minis(d):
    minis = [
        ("GULF OF FINLAND · SECURITY", "C", "Drones hit Russian ship off Finland", "A Kaliningrad-bound vessel caught fire; Helsinki restricts the gulf's airspace and waters.", "AFP", lambda d, x, y: (
            d.rectangle([x+10, y+18, x+32, y+26], fill=PALETTE["GREY"]),
            d.line([x+18, y+14, x+24, y+18], fill=PALETTE["RED"], width=2),
            d.ellipse([x+22, y+10, x+26, y+14], fill=PALETTE["RED"]),
            d.point([(x+13, y+20), (x+15, y+22), (x+19, y+20)], fill=PALETTE["INK"])
        )),
        ("GAZA", "C", "Four killed by Israeli fire", "Three died in a drone strike on a food vehicle in Gaza City; one was shot in Jabalia.", "AFP · Reuters", lambda d, x, y: (
            d.rectangle([x+10, y+16, x+26, y+28], fill=PALETTE["LINE"]),
            d.rectangle([x+26, y+20, x+34, y+28], fill=PALETTE["CARD"], outline=PALETTE["LINE"]),
            d.ellipse([x+13, y+28, x+17, y+32], fill=PALETTE["INK"]),
            d.ellipse([x+27, y+28, x+31, y+32], fill=PALETTE["INK"]),
            d.line([x+16, y+20, x+20, y+20], fill=PALETTE["RED"], width=2),
            d.line([x+18, y+18, x+18, y+22], fill=PALETTE["RED"], width=2)
        )),
        ("YEMEN · SAUDI", "R", "Riyadh intercepts 3 Houthi missiles", "Emergency alerts sounded in the Saudi capital for a third night.", "Al Jazeera", lambda d, x, y: (
            d.arc([x+12, y+12, x+32, y+32], 180, 270, fill=PALETTE["RED"], width=2),
            d.line([x+10, y+28, x+18, y+20], fill=PALETTE["INK"], width=2),
            d.line([x+14, y+30, x+22, y+22], fill=PALETTE["INK"], width=2),
            d.line([x+18, y+32, x+26, y+24], fill=PALETTE["INK"], width=2)
        )),
        ("SINALOA · MEXICO", "C", "Mexico captures cartel boss Chapo Isidro", "The FBI Top Ten fugitive, with a $5M reward, was seized in Guasave.", "AP · Al Jazeera", lambda d, x, y: (
            d.ellipse([x+12, y+12, x+32, y+32], outline=PALETTE["RED"], width=2),
            d.text((x+15, y+16), "$", fill=PALETTE["INK"], font=F("sansb", 9)),
            d.polygon([(x+26, y+12), (x+28, y+16), (x+32, y+17), (x+29, y+20), (x+30, y+24), (x+26, y+22), (x+22, y+24), (x+23, y+20), (x+20, y+17), (x+24, y+16)], fill=PALETTE["AMBER"])
        )),
        ("INDONESIA · TRADE", "C", "Indonesia and EU sign trade pact", "The deal lifts 98.5% of tariffs on EU goods, after a decade of talks.", "Euronews", lambda d, x, y: (
            d.rectangle([x+10, y+14, x+22, y+26], fill=PALETTE["DBLUE"]),
            d.ellipse([x+14, y+18, x+18, y+22], outline=PALETTE["SAND"], width=1),
            d.rectangle([x+22, y+14, x+34, y+26], fill=PALETTE["WHITE"], outline=PALETTE["LINE"]),
            d.rectangle([x+22, y+20, x+34, y+26], fill=PALETTE["RED"])
        )),
        ("IRAQ · DISASTER", "C", "Basra power-station fire kills 4", "Thirty-five people were injured as the fire shut the plant.", "Reuters", lambda d, x, y: (
            d.polygon([(x+14, y+28), (x+26, y+12), (x+38, y+28)], outline=PALETTE["LINE"], width=2),
            d.line([x+26, y+16, x+26, y+28], fill=PALETTE["LINE"], width=2),
            d.ellipse([x+22, y+14, x+28, y+22], fill=PALETTE["RED"])
        )),
        ("INDONESIA · DISASTER", "C", "Candy-factory fire near Jakarta", "Three dead, four hurt and 36 missing in Banten province.", "The Guardian", lambda d, x, y: (
            d.rectangle([x+12, y+18, x+34, y+30], fill=PALETTE["GREY"]),
            d.polygon([(x+12, y+18), (x+19, y+12), (x+27, y+18), (x+34, y+12), (x+34, y+18)], fill=PALETTE["LINE"]),
            d.ellipse([x+20, y+10, x+26, y+18], fill=PALETTE["RED"])
        )),
        ("BANGLADESH · LABOUR", "C", "80 garment factories close", "Wage sit-ins idled plants in Savar and Ashulia; 96 people were arrested.", "Daily Star · TBS", lambda d, x, y: (
            d.rectangle([x+10, y+16, x+34, y+30], fill=PALETTE["GREY"]),
            d.ellipse([x+16, y+12, x+20, y+16], fill=PALETTE["INK"]),
            d.ellipse([x+22, y+12, x+26, y+16], fill=PALETTE["INK"]),
            d.ellipse([x+28, y+12, x+32, y+16], fill=PALETTE["INK"]),
            d.rectangle([x+12, y+20, x+18, y+30], fill=PALETTE["WHITE"]),
            d.rectangle([x+26, y+20, x+32, y+30], fill=PALETTE["WHITE"])
        )),
        ("LONDON · RUGBY", "C", "England beat All Blacks 37-12", "A record 25-point margin at Twickenham; back-to-back wins, first since 2003.", "Reuters · AP", lambda d, x, y: (
            d.ellipse([x+14, y+16, x+32, y+28], fill=PALETTE["SAND"], outline=PALETTE["INK"]),
            d.line([x+23, y+16, x+23, y+28], fill=PALETTE["INK"]),
            d.line([x+19, y+20, x+27, y+24], fill=PALETTE["WHITE"]),
            d.line([x+19, y+24, x+27, y+20], fill=PALETTE["WHITE"])
        )),
        ("SPACE", "C", "BepiColombo enters Mercury orbit", "ESA's twin craft end an eight-year cruise - only the second mission to orbit Mercury.", "ESA via AP", lambda d, x, y: (
            d.ellipse([x+14, y+16, x+26, y+28], fill=PALETTE["GREY"]),
            d.arc([x+10, y+12, x+32, y+32], 0, 360, fill=PALETTE["LINE"]),
            d.rectangle([x+28, y+14, x+32, y+18], fill=PALETTE["RED"])
        ))
    ]

    for i, (tag, b_lvl, headline, deck, src, draw_icon) in enumerate(minis):
        col = i % 5
        row = i // 5
        x = 24 + col * 197
        y = 524 if row == 0 else 646
        w = 189
        h = 114

        # Card background & border
        d.rectangle([x, y, x+w, y+h], fill=PALETTE["CARD"], outline=PALETTE["LINE"])

        # Icon strip
        d.rectangle([x, y, x+w, y+34], fill="#EFE9D6")
        d.line([x, y+34, x+w, y+34], fill=PALETTE["LINE"])
        draw_icon(d, x, y)

        # Tag line & badge chip
        d.text((x+8, y+38), tag, fill=PALETTE["RED"], font=F("sansb", 8))
        badge(d, x + w - 32, y+37, b_lvl)

        # Headline (up to 2 lines)
        hl_lines = wrap(d, headline, F("sansb", 11.5), w - 16)
        hy = y + 50
        for line in hl_lines[:2]:
            d.text((x+8, hy), line, fill=PALETTE["INK"], font=F("sansb", 11.5))
            hy += 13

        # Deck (up to 2 lines)
        deck_lines = wrap(d, deck, F("sans", 9), w - 16)
        for line in deck_lines[:2]:
            d.text((x+8, hy), line, fill=PALETTE["INK"], font=F("sans", 9))
            hy += 11

        # Source at bottom
        d.text((x+8, y + h - 13), src, fill=PALETTE["GREY"], font=F("sans", 8))

if __name__ == "__main__":
    main()
