#!/usr/bin/env python3
"""Generates the store assets for this app into store/ (and launcher icons).

    python3 tools/make_store_assets.py            # store/ only
    python3 tools/make_store_assets.py --launcher # also overwrite android launcher icons

Output (all original artwork, drawn from the app's own picture files):
    store/icon-512.png, store/icon-114.png
    store/<lang>/feature-graphic-1024x500.png   (Google Play)
    store/<lang>/tablet-1920x1200-N.png     (Amazon Fire tablets, Google tablets)
    store/<lang>/phone-1080x1920-N.png      (Google Play phones)

The screenshots are renders of the app's real layout with the app's real picture
data and text (not photos of a running device). If a store reviewer prefers
device captures, replace them with real screenshots.
"""
import argparse
import json
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
from validate_content import load_palette, region_points  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
PICS = os.path.join(ROOT, "assets", "pictures")
I18N = os.path.join(ROOT, "assets", "i18n")
OUT = os.path.join(ROOT, "store")
RES = os.path.join(ROOT, "android", "app", "src", "main", "res")

SS = 2                      # supersampling factor for smooth edges
OUTLINE = "#263238"
PALETTE = load_palette()

# Per-app look, overridable with tools/store_config.json (see apps/vehicles for an
# example). The defaults below are this app's own settings.
DEFAULT_CFG = {
    "icon": "fish",
    "hero": ["house", "fish"],
    "shots": [["house", 6, 1], ["rocket", "full", 7], ["cat", 5, 8]],
    "grid": {"house": "full", "fish": "full", "rocket": "full",
             "flower": "empty", "car": 8, "cat": "empty"},
    "accent": "#29B6F6", "light": "#E1F5FE",
    "appbar": "#EAF5FB", "bg": "#F7FBFE", "border": "#D5E3EC",
    "taglines": {"en": "Tap a color. Tap to fill.", "fr": "Choisis, touche, colorie !",
                 "pl": "Wybierz kolor. Dotknij."},
    "fills": {},
}
_cfg_path = os.path.join(os.path.dirname(__file__), "store_config.json")
CFG = dict(DEFAULT_CFG)
if os.path.exists(_cfg_path):
    CFG.update(json.load(open(_cfg_path, encoding="utf-8")))

FONT_PATHS = {
    False: ["/usr/share/fonts/opentype/inter/Inter-Medium.otf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"],
    True: ["/usr/share/fonts/opentype/inter/Inter-Bold.otf",
           "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
           "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"],
}
SYMBOL_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


CJK_FONTS = {False: "/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc",
             True: "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"}
LANG = ""   # set per language while rendering; Japanese needs a CJK font


def font(size, bold=False, path=None):
    if LANG == "ja" and path is None and os.path.exists(CJK_FONTS[bold]):
        return ImageFont.truetype(CJK_FONTS[bold], max(1, int(size)), index=0)
    for p in ([path] if path else FONT_PATHS[bold]):
        if p and os.path.exists(p):
            return ImageFont.truetype(p, max(1, int(size)))
    return ImageFont.load_default()


def load_pictures():
    ids = json.load(open(os.path.join(PICS, "index.json"), encoding="utf-8"))
    return {pid: json.load(open(os.path.join(PICS, pid + ".json"), encoding="utf-8"))
            for pid in ids}


PICTURES = load_pictures()

# palette index per region (see AppConfig.palette): 0 red, 1 orange, 2 yellow, 3 lime,
# 4 green, 5 sky, 6 blue, 7 purple, 8 pink, 9 brown, 10 grey, 11 white
FULL = {
    "house": {0: 5, 1: 3, 2: 2, 3: 10, 4: 0, 5: 1, 6: 8, 7: 9, 8: 6, 9: 6},
    "fish": {0: 5, 1: 2, 2: 4, 3: 4, 4: 11, 5: 11, 6: 7, 7: 0, 8: 8, 9: 1, 10: 11},
    "rocket": {0: 6, 1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 8, 7: 1, 8: 0, 9: 0,
               10: 11, 11: 0, 12: 2, 13: 5},
    "cat": {0: 5, 1: 9, 2: 9, 3: 1, 4: 4, 5: 4, 6: 11, 7: 8},
    "flower": {0: 5, 1: 3, 2: 4, 3: 4, 4: 4, 13: 2,
               **{5 + k: (8 if k % 2 == 0 else 0) for k in range(8)}},
    "car": {0: 5, 1: 2, 2: 10, 3: 11, 4: 11, 5: 11, 6: 0, 7: 0, 8: 5, 9: 5,
            10: 2, 11: 9, 12: 9, 13: 11, 14: 11},
}


for _pid, _f in CFG["fills"].items():
    FULL[_pid] = {int(k): v for k, v in _f.items()}


def first_n(fills, n):
    return {k: v for k, v in fills.items() if k < n}


def state(pid, spec):
    """spec: 'full', 'empty' or a number n (the first n regions colored)."""
    if spec == "empty":
        return {}
    full = FULL[pid]
    return full if spec == "full" else first_n(full, int(spec))


def render_picture(pid, size, fills):
    regions = PICTURES[pid]["regions"]
    big = size * SS
    img = Image.new("RGB", (big, big), "white")
    d = ImageDraw.Draw(img)
    s = big / 100.0
    lw = max(2, round(0.9 * s))
    for i, r in enumerate(regions):
        pts = [(x * s, y * s) for x, y in region_points(r)]
        d.polygon(pts, fill=PALETTE[fills[i]] if i in fills else "#FFFFFF")
        d.line(pts + [pts[0]], fill=OUTLINE, width=lw, joint="curve")
    return img.resize((size, size), Image.LANCZOS)


def rounded(img, radius):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, img.size[0] - 1, img.size[1] - 1], radius, fill=255)
    out = img.convert("RGBA")
    out.putalpha(mask)
    return out


def save(img, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.convert("RGB").save(path, "PNG", optimize=True)


# ---------------------------------------------------------------- icons

def make_icons(launcher):
    icon = render_picture(CFG["icon"], 512, FULL[CFG["icon"]])
    save(icon, os.path.join(OUT, "icon-512.png"))
    save(icon.resize((114, 114), Image.LANCZOS), os.path.join(OUT, "icon-114.png"))
    # Amazon wants PNGs with transparency: same art with rounded, transparent corners
    for px in (512, 114):
        small = icon.resize((px, px), Image.LANCZOS)
        rounded(small, int(px * 0.18)).save(
            os.path.join(OUT, f"icon-{px}-transparent.png"), "PNG", optimize=True)
    if launcher:
        for folder, px in [("mdpi", 48), ("hdpi", 72), ("xhdpi", 96),
                           ("xxhdpi", 144), ("xxxhdpi", 192)]:
            target = os.path.join(RES, "mipmap-" + folder, "ic_launcher.png")
            if not os.path.isdir(os.path.dirname(target)):
                sys.exit("android/ launcher folders not found: run Bootstrap Android first")
            icon.resize((px, px), Image.LANCZOS).save(target, "PNG")
        print("launcher icons written")


# ---------------------------------------------------------- feature graphic

def make_feature_graphic(title, tagline, out_path):
    w, h = 1024, 500
    img = Image.new("RGB", (w, h), CFG["accent"])
    d = ImageDraw.Draw(img)
    base = [int(CFG["accent"][i:i + 2], 16) for i in (1, 3, 5)]
    for y in range(h):                       # soft vertical gradient
        t = y / h
        d.line([(0, y), (w, y)], fill=(min(255, int(base[0] + 30 * t)),
                                       min(255, int(base[1] + 25 * t)),
                                       max(0, int(base[2] - 10 * t))))
    max_text_w = 470                         # keep clear of the picture cards
    size = 70
    while size > 28 and d.textlength(title, font=font(size, True)) > max_text_w:
        size -= 2
    d.text((56, 150), title, font=font(size, True), fill="white", anchor="lm")
    tag_size = 34
    while tag_size > 18 and d.textlength(tagline, font=font(tag_size)) > max_text_w:
        tag_size -= 2
    d.text((56, 150 + size // 2 + 44), tagline, font=font(tag_size), fill=CFG["light"], anchor="lm")
    placement = [(540, 40, 6), (705, 150, -7)]
    for pid, (x, y, ang) in zip(CFG["hero"], placement):
        card = rounded(render_picture(pid, 240, FULL[pid]), 26)
        shadow = Image.new("RGBA", (card.width + 40, card.height + 40), (0, 0, 0, 0))
        ImageDraw.Draw(shadow).rounded_rectangle(
            [20, 28, card.width + 20, card.height + 28], 28, fill=(0, 0, 0, 70))
        shadow.paste(card, (20, 20), card)
        rot = shadow.rotate(ang, resample=Image.BICUBIC, expand=True)
        img.paste(rot, (x, y), rot)
    save(img, out_path)


# ------------------------------------------------------------- UI renders

BG = CFG["bg"]
CARD_BORDER = CFG["border"]
TEXT = "#1B2A33"


class Screen:
    """Draws the app's layout in dp units scaled by k onto a W x H canvas."""

    def __init__(self, w, h, k):
        self.w, self.h, self.k = w, h, k
        self.img = Image.new("RGB", (w, h), BG)
        self.d = ImageDraw.Draw(self.img)

    def px(self, v):
        return round(v * self.k)

    def appbar(self, title, back, right):
        k = self.k
        self.d.rectangle([0, 0, self.w, self.px(64)], fill=CFG["appbar"])
        self.d.line([(0, self.px(64)), (self.w, self.px(64))], fill=CARD_BORDER, width=max(1, self.px(1)))
        cy = self.px(32)
        x_title = self.px(72) if back else self.px(16)
        self.d.text((x_title, cy), title, font=font(22 * k), fill=TEXT, anchor="lm")
        if back:
            cx = self.px(28)
            lw = self.px(2.2)
            self.d.line([(cx + self.px(9), cy), (cx - self.px(9), cy)], fill=TEXT, width=lw)
            self.d.line([(cx - self.px(9), cy), (cx - self.px(1), cy - self.px(8))], fill=TEXT, width=lw)
            self.d.line([(cx - self.px(9), cy), (cx - self.px(1), cy + self.px(8))], fill=TEXT, width=lw)
        x = self.w - self.px(28)
        for kind in reversed(right):
            if kind == "lock":
                lw = self.px(2.2)
                self.d.rounded_rectangle([x - self.px(9), cy - self.px(2), x + self.px(9), cy + self.px(11)],
                                         self.px(2), outline=TEXT, width=lw)
                self.d.arc([x - self.px(6), cy - self.px(12), x + self.px(6), cy + self.px(2)],
                           180, 360, fill=TEXT, width=lw)
            elif kind == "undo":
                self.d.text((x, cy), "↶", font=font(30 * k, path=SYMBOL_FONT), fill=TEXT, anchor="mm")
            elif kind == "trash":
                lw = self.px(2.2)
                self.d.line([(x - self.px(9), cy - self.px(7)), (x + self.px(9), cy - self.px(7))], fill=TEXT, width=lw)
                self.d.line([(x - self.px(3), cy - self.px(10)), (x + self.px(3), cy - self.px(10))], fill=TEXT, width=lw)
                self.d.rounded_rectangle([x - self.px(7), cy - self.px(5), x + self.px(7), cy + self.px(11)],
                                         self.px(2), outline=TEXT, width=lw)
            x -= self.px(48)

    def card(self, x, y, w, h, pid, fills, label):
        k = self.k
        self.d.rounded_rectangle([x, y, x + w, y + h], self.px(12), fill="white",
                                 outline=CARD_BORDER, width=max(1, self.px(1)))
        side = w - self.px(16)
        pic = render_picture(pid, side, fills)
        self.img.paste(pic, (x + self.px(8), y + self.px(8)))
        self.d.text((x + w // 2, y + h - self.px(18)), label, font=font(16 * k),
                    fill=TEXT, anchor="mm")

    def grid(self, items, columns, labels):
        k = self.k
        pad, gap = self.px(16), self.px(16)
        cw = (self.w - 2 * pad - (columns - 1) * gap) // columns
        ch = round(cw / 0.9)
        for n, (pid, fills) in enumerate(items):
            r, c = divmod(n, columns)
            self.card(pad + c * (cw + gap), self.px(64) + pad + r * (ch + gap), cw, ch,
                      pid, fills, labels[pid])

    def palette(self, x, y, width, selected):
        """Wrap of 48dp circles, centered, like the app's palette."""
        k = self.k
        size, gap = self.px(48), self.px(10)
        per_row = max(1, (width + gap) // (size + gap))
        n = len(PALETTE)
        rows = math.ceil(n / per_row)
        for i in range(n):
            r, c = divmod(i, per_row)
            in_row = min(per_row, n - r * per_row)
            row_w = in_row * size + (in_row - 1) * gap
            cx = x + (width - row_w) // 2 + c * (size + gap)
            cy = y + r * (size + gap)
            sel = i == selected
            self.d.ellipse([cx, cy, cx + size, cy + size], fill=PALETTE[i],
                           outline=OUTLINE if sel else "#B0BEC5",
                           width=self.px(4 if sel else 1.5))
        return rows * (size + gap)

    def coloring(self, title, pid, fills, selected, landscape):
        k = self.k
        self.appbar(title, True, ["undo", "trash"])
        top = self.px(64)
        if landscape:
            pal_w = self.px(150)
            area_w, area_h = self.w - pal_w, self.h - top
            side = min(area_w - self.px(24), area_h - self.px(24))
            px_, py_ = (area_w - side) // 2, top + (area_h - side) // 2
            self.img.paste(render_picture(pid, side, fills), (px_, py_))
            self.palette(self.w - pal_w + self.px(12), top + self.px(12), pal_w - self.px(24), selected)
        else:
            size, gap = self.px(48), self.px(10)
            width = self.w - self.px(24)
            per_row = max(1, (width + gap) // (size + gap))
            pal_h = math.ceil(len(PALETTE) / per_row) * (size + gap) + self.px(24)
            area_h = self.h - top - pal_h
            side = min(self.w - self.px(24), area_h - self.px(24))
            px_, py_ = (self.w - side) // 2, top + (area_h - side) // 2
            self.img.paste(render_picture(pid, side, fills), (px_, py_))
            self.palette(self.px(12), self.h - pal_h + self.px(12), width, selected)


def make_screenshots(lang):
    t = json.load(open(os.path.join(I18N, lang + ".json"), encoding="utf-8"))
    labels = {pid: t["pic_" + pid] for pid in PICTURES}
    shots = {1: ("grid", None)}
    for n, (pid, spec, sel) in enumerate(CFG["shots"], start=2):
        shots[n] = ("color", (pid, state(pid, spec), sel))
    grid_items = [(pid, state(pid, CFG["grid"].get(pid, "empty"))) for pid in PICTURES]
    for name, (w, h, k, landscape, cols) in {
            "tablet-1920x1200": (1920, 1200, 2, True, 4),
            "phone-1080x1920": (1080, 1920, 3, False, 2)}.items():
        for n, (kind, arg) in shots.items():
            s = Screen(w, h, k)
            if kind == "grid":
                s.appbar(t["app_title"], False, ["lock"])
                s.grid(grid_items, cols, labels)
            else:
                pid, fills, sel = arg
                s.coloring(labels[pid], pid, fills, sel, landscape)
            save(s.img, os.path.join(OUT, lang, f"{name}-{n}.png"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--launcher", action="store_true",
                    help="also overwrite android launcher icons")
    args = ap.parse_args()
    make_icons(args.launcher)
    taglines = CFG["taglines"]
    langs = sorted(f[:-5] for f in os.listdir(I18N) if f.endswith(".json"))
    global LANG
    for lang in langs:
        LANG = lang
        t = json.load(open(os.path.join(I18N, lang + ".json"), encoding="utf-8"))
        make_screenshots(lang)
        make_feature_graphic(t["app_title"], taglines.get(lang, taglines["en"]),
                             os.path.join(OUT, lang, "feature-graphic-1024x500.png"))
    print("store assets written to", os.path.normpath(OUT))


if __name__ == "__main__":
    main()
