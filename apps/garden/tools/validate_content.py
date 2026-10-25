#!/usr/bin/env python3
"""Checks the content packs of a kids app without needing Flutter.

    python3 tools/validate_content.py [--preview-dir DIR]

Checks:
  * every picture parses and uses known region types, inside the 0..100 space
  * every region has enough *visible* area to be tapped (not hidden behind
    regions drawn later), so a child can always reach it
  * every language file has exactly the same keys as English, keeps the
    {placeholders}, and has a name for every picture
  * index.json lists exactly the picture files that exist
Optionally writes a contact-sheet PNG of the pictures filled with palette colors.
"""
import argparse
import json
import os
import random
import re
import sys

from PIL import Image, ImageDraw

ROOT = os.path.join(os.path.dirname(__file__), "..")
PICS = os.path.join(ROOT, "assets", "pictures")
I18N = os.path.join(ROOT, "assets", "i18n")
CONFIG = os.path.join(ROOT, "lib", "core", "app_config.dart")

RASTER = 400            # pixels per side for visibility sampling
MIN_VISIBLE_AREA = 30   # square units out of 10 000 (0.3 % of the picture)
KNOWN = {"poly", "circle", "ellipse", "rect"}

errors = []


def err(msg):
    errors.append(msg)
    print("ERROR:", msg)


def region_points(r, steps=48):
    """Region outline as a list of (x, y) in the 0..100 space."""
    import math
    t = r["type"]
    if t == "poly":
        return [tuple(p) for p in r["points"]]
    if t == "rect":
        x, y, w, h = r["x"], r["y"], r["w"], r["h"]
        return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    if t == "circle":
        cx, cy = r["c"]
        rad = r["r"]
        return [(cx + rad * math.cos(2 * math.pi * i / steps),
                 cy + rad * math.sin(2 * math.pi * i / steps)) for i in range(steps)]
    if t == "ellipse":
        cx, cy = r["c"]
        return [(cx + r["rx"] * math.cos(2 * math.pi * i / steps),
                 cy + r["ry"] * math.sin(2 * math.pi * i / steps)) for i in range(steps)]
    raise ValueError(t)


def check_region_shape(pid, i, r):
    if not isinstance(r, dict) or r.get("type") not in KNOWN:
        err(f"{pid} region {i}: unknown type {r.get('type') if isinstance(r, dict) else r!r}")
        return False
    try:
        pts = region_points(r)
    except (KeyError, TypeError, ValueError) as e:
        err(f"{pid} region {i}: malformed ({e!r})")
        return False
    if len(pts) < 3:
        err(f"{pid} region {i}: fewer than 3 points")
        return False
    for x, y in pts:
        if not (-0.01 <= x <= 100.01 and -0.01 <= y <= 100.01):
            err(f"{pid} region {i}: point ({x:.1f},{y:.1f}) outside 0..100")
            return False
    return True


def load_palette():
    text = open(CONFIG, encoding="utf-8").read()
    block = text.split("palette = [", 1)[1].split("];", 1)[0]
    return ["#" + m for m in re.findall(r"Color\(0xFF([0-9A-Fa-f]{6})\)", block)]


def draw_picture(regions, size, fills, palette):
    img = Image.new("RGB", (size, size), "white")
    d = ImageDraw.Draw(img)
    s = size / 100.0
    for i, r in enumerate(regions):
        pts = [(x * s, y * s) for x, y in region_points(r)]
        color = palette[fills[i] % len(palette)] if i in fills else "white"
        d.polygon(pts, fill=color, outline="#263238")
    return img


def visible_areas(regions):
    """Visible area of each region, in square units, using topmost-wins."""
    if len(regions) > 254:
        raise ValueError("more than 254 regions in one picture")
    img = Image.new("L", (RASTER, RASTER), 0)   # pixel value = region index + 1
    d = ImageDraw.Draw(img)
    s = RASTER / 100.0
    for i, r in enumerate(regions):
        d.polygon([(x * s, y * s) for x, y in region_points(r)], fill=i + 1)
    counts = img.histogram()
    unit = 10000.0 / (RASTER * RASTER)
    return [counts[i + 1] * unit for i in range(len(regions))]


def check_pictures():
    index_path = os.path.join(PICS, "index.json")
    ids = json.load(open(index_path, encoding="utf-8"))
    on_disk = sorted(f[:-5] for f in os.listdir(PICS)
                     if f.endswith(".json") and f != "index.json")
    if sorted(ids) != on_disk:
        err(f"index.json {sorted(ids)} does not match files {on_disk}")
    pictures = {}
    for pid in ids:
        path = os.path.join(PICS, pid + ".json")
        if not os.path.exists(path):
            continue
        data = json.load(open(path, encoding="utf-8"))
        if data.get("id") != pid:
            err(f"{pid}: id field is {data.get('id')!r}")
        if not data.get("name_key"):
            err(f"{pid}: missing name_key")
        regions = data.get("regions", [])
        if not all(check_region_shape(pid, i, r) for i, r in enumerate(regions)):
            continue
        areas = visible_areas(regions)
        worst = min(range(1, len(areas)), key=lambda k: areas[k])
        for i, a in enumerate(areas):
            if i > 0 and a < MIN_VISIBLE_AREA:
                err(f"{pid} region {i} ({regions[i]['type']}): visible area {a:.1f} "
                    f"< {MIN_VISIBLE_AREA} (too small or hidden)")
        print(f"{pid:8s} {len(regions):2d} regions, smallest visible area "
              f"{min(areas[1:]):.0f} (region {worst})")
        pictures[pid] = data
    return pictures


def check_i18n(pictures):
    files = sorted(f for f in os.listdir(I18N) if f.endswith(".json"))
    tables = {f[:-5]: json.load(open(os.path.join(I18N, f), encoding="utf-8"))
              for f in files}
    base = tables.get("en")
    if base is None:
        err("assets/i18n/en.json is missing")
        return
    for pid, data in pictures.items():
        if data["name_key"] not in base:
            err(f"en.json has no key {data['name_key']!r} for picture {pid}")
    for lang, table in tables.items():
        missing = sorted(set(base) - set(table))
        extra = sorted(set(table) - set(base))
        if missing:
            err(f"{lang}.json missing keys: {missing}")
        if extra:
            err(f"{lang}.json has keys not in en.json: {extra}")
        for k, v in table.items():
            if not isinstance(v, str) or not v.strip():
                err(f"{lang}.json key {k!r} is empty or not a string")
            elif k in base and sorted(re.findall(r"\{\w+\}", v)) != sorted(re.findall(r"\{\w+\}", base[k])):
                err(f"{lang}.json key {k!r} placeholders differ from English")
    # languages declared in app_config.dart must have a file
    cfg = open(CONFIG, encoding="utf-8").read()
    declared = re.findall(r"'([a-z]{2})':\s*'[^']+'", cfg.split("languages = {", 1)[1].split("};", 1)[0])
    for code in declared:
        if code not in tables:
            err(f"app_config.dart lists language {code!r} but assets/i18n/{code}.json is missing")
    for code in tables:
        if code not in declared:
            err(f"assets/i18n/{code}.json exists but app_config.dart does not list {code!r}")
    print("languages:", ", ".join(sorted(tables)), "| keys per language:", len(base))


def write_preview(pictures, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    palette = load_palette()
    rnd = random.Random(7)
    cell = 260
    cols = 3
    rows = (len(pictures) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell, rows * cell * 2), "#eceff1")
    for n, (pid, data) in enumerate(pictures.items()):
        regions = data["regions"]
        blank = draw_picture(regions, cell - 20, {}, palette)
        colored = draw_picture(regions, cell - 20,
                               {i: rnd.randrange(len(palette) - 1) for i in range(len(regions))},
                               palette)
        x, y = (n % cols) * cell + 10, (n // cols) * cell * 2 + 10
        sheet.paste(blank, (x, y))
        sheet.paste(colored, (x, y + cell))
    path = os.path.join(out_dir, "preview.png")
    sheet.save(path)
    print("preview written to", path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview-dir")
    args = ap.parse_args()
    pictures = check_pictures()
    check_i18n(pictures)
    if args.preview_dir:
        write_preview(pictures, args.preview_dir)
    if errors:
        print(f"\n{len(errors)} problem(s) found")
        sys.exit(1)
    print("\nAll content checks passed")


if __name__ == "__main__":
    main()
