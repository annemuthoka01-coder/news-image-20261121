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

    im_resized = im.resize((1024, 1024), Image.LANCZOS)
    im_resized.save("entry.png", "PNG")

if __name__ == "__main__":
    main()
