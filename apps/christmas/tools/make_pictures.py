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


def diamond(cx, cy, r):
    return poly((cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy))



def star(cx, cy, r_out, r_in, points=5, rot=-90):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180 / points)
        pts.append((round(cx + r * math.cos(a), 2), round(cy + r * math.sin(a), 2)))
    return poly(*pts)


def half_ellipse(cx, cy, rx, ry, top=True, steps=24):
    pts = []
    for i in range(steps + 1):
        t = math.pi * i / steps
        x = cx - rx * math.cos(t)
        y = cy - ry * math.sin(t) if top else cy + ry * math.sin(t)
        pts.append((round(x, 2), round(y, 2)))
    return poly(*pts)


BG = rect(0, 0, 100, 100)


GROUND = rect(0, 82, 100, 18)
SUN = circle(86, 16, 6)



def tree():
    return [
        BG,
        GROUND,
        rect(43, 70, 14, 16),                                # trunk
        poly((10, 76), (50, 42), (90, 76)),                  # bottom tier
        poly((18, 58), (50, 28), (82, 58)),                  # middle tier
        poly((28, 42), (50, 16), (72, 42)),                  # top tier
        star(50, 12, 8, 3.6),                                # star on top
        circle(32, 70, 4),                                   # baubles
        circle(52, 66, 4),
        circle(70, 72, 4),
        circle(40, 52, 3.8),
        circle(60, 50, 3.8),
        circle(50, 36, 3.6),
        rect(8, 76, 18, 14),                                 # present
        rect(74, 78, 18, 12),                                # present
        SUN,
    ]


def santa():
    return [
        BG,
        GROUND,
        poly((8, 100), (16, 74), (84, 74), (92, 100)),       # coat
        ellipse(50, 58, 26, 24),                             # beard
        ellipse(50, 43, 19, 15),                             # face
        ellipse(50, 54, 14, 5),                              # moustache
        circle(50, 48, 4.4),                                 # nose
        circle(41, 44, 3.4),                                 # eyes
        circle(59, 44, 3.4),
        rect(14, 90, 72, 7),                                 # belt
        rect(43, 88, 14, 11),                                # buckle
        poly((24, 34), (38, 8), (80, 22), (76, 34)),         # hat
        rect(21, 28, 58, 10),                                # hat trim
        circle(38, 7, 6),                                    # pompom
        circle(10, 14, 4.4),                                 # snowflakes
        circle(90, 40, 4.4),
        circle(88, 8, 4.4),
        circle(8, 52, 4.4),
    ]


def snowman():
    return [
        BG,
        GROUND,
        circle(50, 74, 22),                                  # body
        circle(50, 50, 17),                                  # middle
        circle(50, 28, 12.5),                                # head
        rotated_ellipse(21, 46, 14, 2.4, -25),               # arms
        rotated_ellipse(79, 46, 14, 2.4, 25),
        rect(36, 39, 28, 6),                                 # scarf
        rect(56, 43, 6, 16),                                 # scarf tail
        rect(35, 14, 30, 4),                                 # hat brim
        rect(40, 3, 20, 12),                                 # hat
        circle(44.5, 27, 3.2),                               # eyes
        circle(55.5, 27, 3.2),
        poly((50, 29), (68, 33), (50, 36)),                  # carrot nose
        circle(50, 52, 3.6),                                 # buttons
        circle(50, 63, 3.6),
        circle(50, 74, 3.6),
        circle(50, 85, 3.6),
        circle(12, 18, 4.4),                                 # snowflakes
        circle(88, 14, 4.4),
        circle(90, 62, 4.4),
    ]


def gift():
    return [
        BG,
        GROUND,
        rect(6, 66, 20, 22),                                 # small gift
        rect(4, 60, 24, 8),                                  # small lid
        rect(14, 60, 5, 28),                                 # small ribbon
        rect(22, 48, 56, 40),                                # big box
        rect(18, 38, 64, 12),                                # lid
        rect(45, 38, 10, 50),                                # ribbon
        rotated_ellipse(38, 30, 11, 6, -30),                 # bow
        rotated_ellipse(62, 30, 11, 6, 30),
        circle(50, 34, 5.4),                                 # knot
        star(84, 22, 8, 3.6),                                # sparkles
        star(16, 22, 7, 3.2),
        circle(82, 56, 4),
    ]


def reindeer():
    return [
        BG,
        GROUND,
        rotated_ellipse(30, 24, 3.4, 16, -18),               # antlers
        rotated_ellipse(22, 20, 3, 7.5, -62),
        rotated_ellipse(36, 12, 2.8, 6, 20),
        rotated_ellipse(70, 24, 3.4, 16, 18),
        rotated_ellipse(78, 20, 3, 7.5, 62),
        rotated_ellipse(64, 12, 2.8, 6, -20),
        rotated_ellipse(27, 46, 11, 5.4, -30),               # ears
        rotated_ellipse(73, 46, 11, 5.4, 30),
        ellipse(50, 58, 19, 24),                             # head
        circle(42, 52, 3.4),                                 # eyes
        circle(58, 52, 3.4),
        ellipse(50, 72, 12, 9),                              # muzzle
        circle(50, 73, 6),                                   # red nose
        poly((30, 80), (70, 80), (68, 94), (32, 94)),        # scarf
        circle(50, 93, 4.2),                                 # bell
        circle(12, 38, 4.2),                                 # snowflakes
        circle(88, 44, 4.2),
    ]


def stocking():
    return [
        BG,
        GROUND,
        poly((34, 22), (66, 22), (66, 58), (88, 64), (92, 82),   # stocking
             (78, 92), (46, 92), (34, 76)),
        circle(80, 80, 8),                                   # toe patch
        circle(43, 80, 7),                                   # heel patch
        rect(34, 40, 32, 6),                                 # stripes
        rect(34, 52, 32, 6),
        rect(30, 10, 40, 14),                                # cuff
        circle(40, 17, 4),                                   # holly berries
        circle(50, 17, 4),
        circle(60, 17, 4),
        star(16, 34, 9, 4),                                  # stars
        star(84, 30, 9, 4),
        circle(14, 62, 4.4),                                 # snowflakes
        circle(90, 12, 4.4),
    ]


PICTURES = {
    "tree": tree,
    "santa": santa,
    "snowman": snowman,
    "gift": gift,
    "reindeer": reindeer,
    "stocking": stocking,
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
