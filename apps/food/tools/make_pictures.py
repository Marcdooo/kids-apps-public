#!/usr/bin/env python3
"""Generates the coloring pictures in assets/pictures/ (original artwork).

Each picture is a list of regions in a 100 x 100 space, drawn in order (later
regions sit on top). Run from the project root:

    python3 tools/make_pictures.py

Then run tools/validate_content.py to check every region can actually be hit.
"""
import json
import math
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "pictures")


def rect(x, y, w, h):
    return {"type": "rect", "x": x, "y": y, "w": w, "h": h}


def circle(cx, cy, r):
    return {"type": "circle", "c": [cx, cy], "r": r}


def ellipse(cx, cy, rx, ry):
    return {"type": "ellipse", "c": [cx, cy], "rx": rx, "ry": ry}


def poly(*points):
    return {"type": "poly", "points": [list(p) for p in points]}


def rotated_ellipse(cx, cy, rx, ry, angle_deg, steps=28):
    """A tilted ellipse as a polygon (the app only needs axis-aligned ones)."""
    a = math.radians(angle_deg)
    pts = []
    for i in range(steps):
        t = 2 * math.pi * i / steps
        x = rx * math.cos(t)
        y = ry * math.sin(t)
        pts.append((round(cx + x * math.cos(a) - y * math.sin(a), 2),
                    round(cy + x * math.sin(a) + y * math.cos(a), 2)))
    return poly(*pts)


def bezier(p0, p1, p2, n=24):
    """Points along a quadratic curve."""
    out = []
    for i in range(n + 1):
        t = i / n
        out.append((round((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], 2),
                    round((1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1], 2)))
    return out


def banana_part(t0, t1):
    """A slice of a crescent-shaped banana between curve positions t0..t1."""
    outer = bezier((8, 30), (48, 122), (94, 20), 40)
    inner = bezier((8, 30), (50, 78), (94, 20), 40)
    a, b = int(t0 * 40), int(t1 * 40)
    return poly(*(outer[a:b + 1] + inner[a:b + 1][::-1]))


def diamond(cx, cy, r):
    return poly((cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy))


BG = rect(0, 0, 100, 100)


def apple():
    return [
        BG,
        rect(0, 90, 100, 10),                      # table
        ellipse(50, 58, 34, 31),                   # apple
        ellipse(36, 46, 6, 9),                     # shine
        rect(48, 14, 4, 16),                       # stem
        rotated_ellipse(62, 18, 11, 5, -25),       # leaf
        circle(50, 72, 4.6),                       # little spot
    ]


def banana():
    return [
        BG,
        circle(14, 14, 8),                         # sun
        rect(0, 90, 100, 10),                      # table
        banana_part(0.0, 0.14),                    # tip
        banana_part(0.14, 0.5),                    # peel left
        banana_part(0.5, 0.86),                    # peel right
        banana_part(0.86, 1.0),                    # stem end
    ]


def ice_cream():
    return [
        BG,
        circle(84, 14, 9),                         # sun
        poly((34, 52), (66, 52), (50, 96)),        # cone
        poly((34, 52), (66, 52), (61.8, 64), (38.2, 64)),   # cone band
        ellipse(50, 46, 22, 12),                   # lower scoop
        circle(50, 30, 16),                        # top scoop
        circle(50, 11, 5),                         # cherry
        circle(43, 28, 4),                         # sprinkles
        circle(57, 33, 4),
        circle(40, 47, 4),
    ]


def pizza():
    return [
        BG,
        rect(0, 92, 100, 8),                       # table
        poly((12, 22), (88, 22), (50, 94)),        # slice
        poly((21, 29), (79, 29), (50, 84)),        # cheese
        ellipse(50, 22, 38, 7),                    # crust
        circle(40, 42, 7),                         # pepperoni
        circle(60, 42, 7),
        circle(50, 62, 7),
        circle(50, 40, 3.8),                       # olives
        circle(45, 54, 3.8),
        circle(56, 52, 3.8),
    ]


def cupcake():
    return [
        BG,
        rect(0, 90, 100, 10),                      # table
        poly((28, 56), (72, 56), (66, 90), (34, 90)),       # wrapper
        poly((40.3, 56), (46.5, 56), (47.4, 90), (43, 90)),  # stripes
        poly((53.5, 56), (59.7, 56), (57, 90), (52.6, 90)),
        ellipse(50, 52, 30, 10),                   # frosting layers
        ellipse(50, 40, 23, 10),
        ellipse(50, 29, 15, 9),
        circle(50, 15, 6),                         # cherry
        circle(40, 43, 4),                         # sprinkles
        circle(60, 42, 4),
        circle(50, 52, 4),
    ]


def carrot():
    return [
        BG,
        rect(0, 90, 100, 10),                      # soil
        rotated_ellipse(36, 18, 5, 13, -25),       # leaves
        rotated_ellipse(64, 18, 5, 13, 25),
        rotated_ellipse(50, 17, 5, 13, 0),
        poly((34, 32), (66, 32), (50, 94)),        # carrot
        ellipse(50, 34, 17, 9),                    # top
        ellipse(44, 50, 5.5, 3),                   # grooves
        ellipse(53, 62, 5, 3),
    ]


PICTURES = {
    "apple": apple,
    "banana": banana,
    "ice_cream": ice_cream,
    "pizza": pizza,
    "cupcake": cupcake,
    "carrot": carrot,
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for pid, build in PICTURES.items():
        data = {"id": pid, "name_key": "pic_" + pid, "regions": build()}
        with open(os.path.join(OUT, pid + ".json"), "w", encoding="utf-8") as f:
            json.dump(data, f, separators=(",", ":"))
            f.write("\n")
    with open(os.path.join(OUT, "index.json"), "w", encoding="utf-8") as f:
        json.dump(list(PICTURES), f)
        f.write("\n")
    print("wrote", len(PICTURES), "pictures to", os.path.normpath(OUT))


if __name__ == "__main__":
    main()
