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

def draw_bottom(d):
    # Headings at y766
    d.text((X(24), X(766)), "WHERE IT HAPPENED", fill=PALETTE["RED"], font=F("sansb", 12))
    d.text((X(400), X(766)), "ALSO ON SATURDAY - 27 MORE", fill=PALETTE["RED"], font=F("sansb", 12))
    
    # MAP panel rectangle x24-388, y784-924
    d.rectangle([X(24), X(784), X(388), X(924)], fill="#DCE9EC", outline=PALETTE["LINE"])
    
    # Continents as SAND-filled polygons with LINE outline
    continents_raw = [
        # North America
        [(2,8),(20,4),(30,6),(28,12),(24,14),(26,18),(20,22),(16,20),(12,16),(6,14),(2,12)],
        # South America
        [(22,24),(30,23),(32,28),(28,35),(24,33),(21,28)],
        # Africa
        [(46,16),(58,15),(62,20),(58,30),(52,33),(47,28),(45,21)],
        # Europe
        [(44,6),(56,4),(60,8),(55,12),(47,12),(43,9)],
        # Asia
        [(58,4),(88,3),(97,8),(92,14),(84,13),(80,19),(74,16),(70,12),(62,13),(58,8)],
        # SE Asia isles
        [(80,22),(86,21),(88,24),(82,25)],
        # Australia
        [(84,27),(95,26),(97,31),(88,33),(83,30)]
    ]
    for poly in continents_raw:
        pts = [(X(24 + rx * 3.64), X(784 + ry * 3.89)) for rx, ry in poly]
        d.polygon(pts, fill=PALETTE["SAND"], outline=PALETTE["LINE"])
        
    # DOTS
    dots = [
        (1, 66, 15), (2, 24, 27), (3, 57, 11), (4, 55, 5),
        (5, 60, 14), (6, 66, 17), (7, 10, 16), (8, 85, 23),
        (9, 64, 13), (10, 83, 25), (11, 76, 15), (12, 46, 6)
    ]
    for num, rx, ry in dots:
        cx = X(24 + rx * 3.64)
        cy = X(784 + ry * 3.89)
        r = X(7.5)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PALETTE["RED"])
        # White F("sansb",7.5) number centred on it
        f_dot = F("sansb", 7.5)
        bbox = d.textbbox((0, 0), str(num), font=f_dot)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        d.text((cx - tw / 2, cy - th / 2 - 1), str(num), fill="#FFFFFF", font=f_dot)
        
    # KEY under map, F("sans",8) INK at x24, three lines starting y932, step 13
    key_lines = [
        "1 Bahrain · 2 Peru · 3 Antalya · 4 Gulf of Finland",
        "5 Gaza · 6 Riyadh · 7 Sinaloa · 8 Jakarta · 9 Basra",
        "10 Banten · 11 Dhaka · 12 London · 13 Mercury (in orbit)"
    ]
    ky = X(932)
    for kl in key_lines:
        d.text((X(24), ky), kl, fill=PALETTE["INK"], font=F("sans", 8))
        ky += X(13)
        
    # LIST ITEMS
    items_col1 = [
        (14, "Tokyo", "Saudi crude stored in Japan to triple to 24M barrels (Japan Today)"),
        (15, "Paris", "82,500 march in a sixth Saturday of cost-of-living protests (Reuters)"),
        (16, "Taipei", "Short-selling curbed after TAIEX's worst week since 1991 · 1 outlet"),
        (17, "Geneva", "128 nations back killer-robot arms talks · 1 outlet"),
        (18, "Balochistan", "Pakistan says 15 militants killed in raid · 1 outlet"),
        (19, "Rabat", "All 54 CAF members back Infantino for FIFA vote · 1 outlet"),
        (20, "Las Vegas", "Verstappen takes Grand Prix pole · 1 outlet"),
        (21, "Dublin", "Ireland edge South Africa 20-17 · 1 outlet"),
        (22, "Newcastle", "Arsenal held 2-2 at Newcastle · 1 outlet"),
        (23, "Leeds", "Leeds beat Chelsea 4-1 · 1 outlet"),
        (24, "Cleveland", "Harden passes Bryant on NBA 50-point list (ESPN)"),
        (25, "Washington", "Second judge blocks Trump's 250-ft arch (UPI)"),
        (26, "California", "Palisades Fire arsonist convicted at retrial · 1 outlet"),
        (27, "Kyiv", "Zelensky: Crimean Bridge attacks a justified reply · 1 outlet")
    ]
    
    items_col2 = [
        (28, "Beijing", "Nvidia halts H200 chip exports to China · 1 outlet"),
        (29, "Washington", "Vance declines to back Trump's Iran claim · 1 outlet"),
        (30, "Delhi", "Modi to SCO forum: cultural ties serve peace · 1 outlet"),
        (31, "Zagreb", "Thousands protest after hospital death · 1 outlet"),
        (32, "Pas-de-Calais", "Floods swamp 850 homes, shut 85 roads · 1 outlet"),
        (33, "Ethiopia", "About 700,000 displaced by conflict · 1 outlet"),
        (34, "Blue Nile", "Sudan army says security being restored (Anadolu) · 1 outlet"),
        (35, "Fukushima", "Snow warning; 700 homes lose power (Kyodo) · 1 outlet"),
        (36, "Bali", "Russian Interpol fugitive refused entry (Antara) · 1 outlet"),
        (37, "Melbourne", "Cricket Australia backs captain Cummins (AFP)"),
        (38, "Muscat", "India U19s beat Pakistan by 1 wicket, record 9th Asia Cup · 1 outlet"),
        (39, "Dhaka", "Border guards deploy 90 platoons, 7 districts (Dhaka Tribune) · 1 outlet"),
        (40, "Pabna", "BNP-Awami League clashes injure several (UNB) · 1 outlet")
    ]
    
    def draw_list_column(x_start, items):
        y = X(786)
        col_w = X(294)
        f_num = F("sansb", 7.5)
        f_body = F("sans", 7.5)
        
        for num, place, text in items:
            num_str = str(num)
            num_w = d.textbbox((0, 0), num_str, font=f_num)[2]
            space_w = d.textbbox((0, 0), " ", font=f_num)[2]
            
            full_text = f"{place} - {text}"
            lines = wrap(d, full_text, f_body, col_w - num_w - space_w)
            if not lines:
                lines = [full_text]
                
            d.text((x_start, y), num_str, fill=PALETTE["RED"], font=f_num)
            d.text((x_start + num_w + space_w, y), lines[0], fill=PALETTE["INK"], font=f_body)
            y += X(10.0)
            
            for l in lines[1:]:
                d.text((x_start + X(14), y), l, fill=PALETTE["INK"], font=f_body)
                y += X(10.0)
                
            y += X(1.5)
        return y

    y1_end = draw_list_column(X(400), items_col1)
    y2_end = draw_list_column(X(706), items_col2)
    
    print(f"Col 1 final y: {y1_end} (max allowed {X(968)})")
    print(f"Col 2 final y: {y2_end} (max allowed {X(968)})")
    if y1_end > X(968) or y2_end > X(968):
        print("OVERFLOW")

def draw_footer(d):
    boxes = [
        (X(24), X(560), "DATE CHECK", "Held back: anything we could not date to Saturday - one APEC leaders' claim among them. Not yet: COP31's approval session (Sun 06:00 GMT) and the Las Vegas race are set, not done, and are marked as such."),
        (X(568), X(1000), "HOW WE CHECKED", "CONFIRMED = two or more major outlets; REPORTED / 1 outlet = a single source, badged as such. Every story happened or was first reported on Saturday 21 November 2026 (Wikipedia Current Events and the named outlets). Original drawings, no photos. Map is schematic.")
    ]
    for x1, x2, heading, body in boxes:
        d.rectangle([x1, X(978), x2, X(1018)], fill=PALETTE["CARD"], outline=PALETTE["LINE"])
        d.text((x1 + X(8), X(982)), heading, fill=PALETTE["RED"], font=F("sansb", 9.5))
        
        body_lines = wrap(d, body, F("sans", 8.5), (x2 - x1) - X(16))
        if len(body_lines) > 2:
            body_lines = body_lines[:2]
            
        by = X(995)
        for bl in body_lines:
            d.text((x1 + X(8), by), bl, fill=PALETTE["INK"], font=F("sans", 8.5))
            by += X(10.5)

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
    draw_bottom(d)
    draw_footer(d)

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
    MINIS = [
        ("GULF OF FINLAND · SECURITY", "C", "Drones hit Russian ship off Finland", "A Kaliningrad-bound vessel caught fire; Helsinki restricts the gulf's airspace and waters.", "AFP", "ship"),
        ("GAZA", "C", "Four killed by Israeli fire", "Three died in a drone strike on a food vehicle in Gaza City; one was shot in Jabalia.", "AFP · Reuters", "truck"),
        ("YEMEN · SAUDI", "R", "Riyadh intercepts 3 Houthi missiles", "Emergency alerts sounded in the Saudi capital for a third night.", "Al Jazeera", "missiles"),
        ("SINALOA · MEXICO", "C", "Mexico captures cartel boss Chapo Isidro", "The FBI Top Ten fugitive, with a $5M reward, was seized in Guasave.", "AP · Al Jazeera", "badge5m"),
        ("INDONESIA · TRADE", "C", "Indonesia and EU sign trade pact", "The deal lifts 98.5% of tariffs on EU goods, after a decade of talks.", "Euronews", "flags"),
        ("IRAQ · DISASTER", "C", "Basra power-station fire kills 4", "Thirty-five people were injured as the fire shut the plant.", "Reuters", "pylon"),
        ("INDONESIA · DISASTER", "C", "Candy-factory fire near Jakarta", "Three dead, four hurt and 36 missing in Banten province.", "The Guardian", "factory"),
        ("BANGLADESH · LABOUR", "C", "80 garment factories close", "Wage sit-ins idled plants in Savar and Ashulia; 96 people were arrested.", "Daily Star · TBS", "crowd"),
        ("LONDON · RUGBY", "C", "England beat All Blacks 37-12", "A record 25-point margin at Twickenham; back-to-back wins, first since 2003.", "Reuters · AP", "rugby"),
        ("SPACE", "C", "BepiColombo enters Mercury orbit", "ESA's twin craft end an eight-year cruise - only the second mission to orbit Mercury.", "ESA via AP", "planet")
    ]
    for i, (tag, lvl, headline, deck, source, icon) in enumerate(MINIS):
        col = i % 5
        row = i // 5
        x = X(24 + col * 197)
        y = X(520 if row == 0 else 644)
        w = X(189)
        h = X(118)
        
        d.rectangle([x, y, x + w, y + h], fill=PALETTE["CARD"], outline=PALETTE["LINE"], width=X(1))
        d.rectangle([x, y, x + w, y + X(30)], fill="#EFE9D6")
        d.line([x, y + X(30), x + w, y + X(30)], fill=PALETTE["LINE"], width=X(1))
        
        # Icon area left X(6), width X(44)
        ix = x + X(6)
        iy = y + X(3)
        iw = X(44)
        ih = X(24)
        
        if icon == "ship":
            d.rectangle([ix + X(4), iy + X(10), ix + X(36), iy + X(20)], fill="#7F8C8D")
            d.ellipse([ix + X(18), iy + X(2), ix + X(24), iy + X(8)], fill=PALETTE["RED"])
        elif icon == "truck":
            d.rectangle([ix + X(4), iy + X(8), ix + X(28), iy + X(20)], fill="#7F8C8D")
            d.rectangle([ix + X(28), iy + X(12), ix + X(38), iy + X(20)], fill="#BDC3C7")
            d.ellipse([ix + X(8), iy + X(19), ix + X(14), iy + X(25)], fill="#2C3E50")
            d.ellipse([ix + X(30), iy + X(19), ix + X(36), iy + X(25)], fill="#2C3E50")
            d.rectangle([ix + X(14), iy + X(11), ix + X(18), iy + X(17)], fill=PALETTE["RED"])
            d.rectangle([ix + X(12), iy + X(13), ix + X(20), iy + X(15)], fill=PALETTE["RED"])
        elif icon == "missiles":
            d.line([ix + X(4), iy + X(22), ix + X(36), iy + X(6)], fill=PALETTE["INK"], width=X(2))
            d.line([ix + X(8), iy + X(24), ix + X(40), iy + X(8)], fill=PALETTE["INK"], width=X(2))
            d.line([ix + X(2), iy + X(20), ix + X(34), iy + X(4)], fill=PALETTE["INK"], width=X(2))
            d.arc([ix + X(20), iy + X(2), ix + X(42), iy + X(22)], start=180, end=270, fill=PALETTE["RED"], width=X(2))
        elif icon == "badge5m":
            d.ellipse([ix + X(4), iy + X(2), ix + X(24), iy + X(22)], outline=PALETTE["RED"], width=X(2))
            d.polygon([ix+X(14),iy+X(4), ix+X(16),iy+X(9), ix+X(21),iy+X(9), ix+X(17),iy+X(12), ix+X(19),iy+X(17), ix+X(14),iy+X(14), ix+X(9),iy+X(17), ix+X(11),iy+X(12), ix+X(7),iy+X(9), ix+X(12),iy+X(9)], fill=PALETTE["AMBER"])
            d.text((ix + X(26), iy + X(6)), "$5M", fill=PALETTE["RED"], font=F("sansb", 8))
        elif icon == "flags":
            d.rectangle([ix + X(4), iy + X(4), ix + X(20), iy + X(20)], fill="#2980B9")
            d.ellipse([ix + X(8), iy + X(8), ix + X(16), iy + X(16)], fill="#F1C40F")
            d.rectangle([ix + X(22), iy + X(4), ix + X(38), iy + X(20)], fill="#BDC3C7")
            d.rectangle([ix + X(22), iy + X(4), ix + X(38), iy + X(12)], fill=PALETTE["RED"])
        elif icon == "pylon":
            d.polygon([ix+X(22),iy+X(2), ix+X(8),iy+X(24), ix+X(36),iy+X(24)], outline=PALETTE["INK"], width=X(1))
            d.ellipse([ix+X(18),iy+X(12), ix+X(26),iy+X(22)], fill=PALETTE["RED"])
        elif icon == "factory":
            d.rectangle([ix+X(4), iy+X(10), ix+X(36), iy+X(22)], fill="#7F8C8D")
            d.polygon([ix+X(4),iy+X(10), ix+X(12),iy+X(2), ix+X(20),iy+X(10), ix+X(28),iy+X(2), ix+X(36),iy+X(10)], fill="#95A5A6")
            d.ellipse([ix+X(28),iy+X(2), ix+X(34),iy+X(10)], fill=PALETTE["RED"])
        elif icon == "crowd":
            d.rectangle([ix+X(4), iy+X(12), ix+X(20), iy+X(22)], fill="#7F8C8D")
            for dx_dot in [X(24), X(29), X(34)]:
                d.ellipse([ix+dx_dot, iy+X(16), ix+dx_dot+X(4), iy+X(20)], fill=PALETTE["INK"])
        elif icon == "rugby":
            d.ellipse([ix+X(4), iy+X(4), ix+X(30), iy+X(22)], fill="#E67E22", outline=PALETTE["INK"], width=X(1))
            d.line([ix+X(17), iy+X(4), ix+X(17), iy+X(22)], fill="#FFFFFF", width=X(1))
            d.line([ix+X(34), iy+X(2), ix+X(34), iy+X(24)], fill=PALETTE["INK"], width=X(1))
            d.line([ix+X(38), iy+X(2), ix+X(38), iy+X(24)], fill=PALETTE["INK"], width=X(1))
        elif icon == "planet":
            d.ellipse([ix+X(10), iy+X(4), ix+X(26), iy+X(20)], fill="#7F8C8D")
            d.arc([ix+X(4), iy+X(2), ix+X(32), iy+X(22)], start=30, end=210, fill=PALETTE["INK"], width=X(1))
            d.rectangle([ix+X(30), iy+X(10), ix+X(34), iy+X(14)], fill=PALETTE["RED"])

        # Tag below the strip
        d.text((x + X(8), y + X(35)), tag, fill=PALETTE["RED"], font=F("sansb", 8))
        
        # Badge chip
        badge(d, 24 + col * 197 + 189 - 70, (520 if row == 0 else 644) + 33, lvl)
        
        # Headline
        hl_font = F("sansb", 11.5)
        hl_size = 11.5
        hl_lines = wrap(d, headline, hl_font, X(173))
        if len(hl_lines) > 2:
            hl_font = F("sansb", hl_size - 0.5)
            hl_lines = wrap(d, headline, hl_font, X(173))
            if len(hl_lines) > 2:
                hl_lines = hl_lines[:2]
        
        hx = x + X(8)
        hy = y + X(49)
        for hline in hl_lines:
            d.text((hx, hy), hline, fill=PALETTE["INK"], font=hl_font)
            hy += X(13)
        
        # Deck
        deck_font = F("sans", 8.5)
        deck_size = 8.5
        deck_lines = wrap(d, deck, deck_font, X(173))
        if len(deck_lines) > 3:
            deck_lines = deck_lines[:3]
        
        dy = hy + X(2)
        for dline in deck_lines:
            d.text((hx, dy), dline, fill=PALETTE["INK"], font=deck_font)
            dy += X(10.5)
        
        # Source
        d.text((x + X(8), y + h - X(12)), source, fill=PALETTE["GREY"], font=F("sans", 8))

if __name__ == "__main__":
    main()

