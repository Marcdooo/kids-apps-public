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


def ship():
    return [
        BG,
        GROUND,
        rect(48, 16, 4, 50),                                 # mast
        poly((46, 18), (46, 56), (16, 56)),                  # sails
        poly((54, 18), (54, 56), (84, 56)),
        poly((52, 16), (52, 4), (68, 10)),                   # flag
        poly((8, 60), (92, 60), (78, 88), (24, 88)),         # hull
        circle(34, 72, 4),                                   # portholes
        circle(50, 72, 4),
        circle(66, 72, 4),
        half_ellipse(20, 94, 14, 6),                         # waves
        half_ellipse(80, 94, 14, 6),
        ellipse(20, 14, 13, 5.6),                            # cloud
        circle(88, 20, 6),
    ]


def chest():
    return [
        BG,
        GROUND,
        rect(16, 50, 68, 36),                                # base
        half_ellipse(50, 50, 34, 24),                        # lid
        rect(16, 46, 68, 8),                                 # band
        rect(26, 30, 7, 56),                                 # straps
        rect(67, 30, 7, 56),
        rect(43, 46, 14, 16),                                # lock
        circle(24, 92, 5),                                   # coins
        circle(36, 94, 5),
        circle(76, 92, 5),
        star(50, 14, 9, 4),                                  # sparkles
        star(16, 22, 7, 3.2),
        star(84, 24, 7, 3.2),
    ]


def parrot():
    return [
        BG,
        GROUND,
        rect(14, 82, 72, 6),                                 # perch
        poly((36, 78), (38, 98), (48, 98), (50, 78)),        # tail
        poly((48, 78), (54, 98), (64, 98), (60, 76)),
        ellipse(48, 56, 21, 30),                             # body
        ellipse(48, 62, 11, 18),                             # chest
        rotated_ellipse(38, 60, 8, 20, -10),                 # wing
        circle(50, 26, 15),                                  # head
        poly((44, 14), (46, 2), (53, 12)),                   # crest
        poly((60, 20), (78, 28), (62, 36)),                  # beak
        circle(54, 22, 3.4),                                 # eye
        circle(12, 20, 4.4),
        circle(88, 60, 4.4),
    ]


def pirate():
    return [
        BG,
        GROUND,
        ellipse(50, 92, 34, 8),                              # shoulders
        circle(28, 54, 5.4),                                 # ears
        circle(72, 54, 5.4),
        half_ellipse(50, 56, 22, 28, top=False),             # beard
        ellipse(50, 52, 21, 20),                             # face
        circle(40, 48, 6.6),                                 # eye patch
        circle(60, 46, 3.6),                                 # eye
        circle(50, 57, 3.8),                                 # nose
        ellipse(50, 64, 12, 4),                              # moustache
        half_ellipse(50, 34, 34, 24),                        # hat dome
        rect(12, 32, 76, 8),                                 # hat brim
        circle(50, 20, 6.4),                                 # skull
        circle(12, 70, 4.4),
        circle(90, 66, 4.4),
    ]


def island():
    return [
        BG,
        GROUND,
        poly((46, 78), (54, 78), (58, 38), (52, 34)),        # trunk
        half_ellipse(50, 84, 44, 18),                        # island
        rotated_ellipse(43, 30, 14, 5, -25),                 # palm leaves
        rotated_ellipse(41, 43, 14, 5, -38),
        rotated_ellipse(67, 30, 14, 5, 25),
        rotated_ellipse(69, 43, 14, 5, 38),
        rotated_ellipse(55, 22, 5.4, 12, 0),
        circle(50, 41, 3.8),                                 # coconuts
        circle(59, 42, 3.8),
        circle(20, 16, 5),                                   # clouds
        ellipse(80, 14, 12, 5),
        circle(10, 90, 4.4),
        circle(92, 92, 4.4),
    ]


def map_():
    return [
        BG,
        GROUND,
        rect(8, 12, 84, 76),                                 # parchment
        ellipse(28, 62, 15, 10),                             # island
        poly((46, 38), (58, 56), (34, 56)),                  # mountain
        circle(22, 28, 9),                                   # compass
        star(22, 28, 8, 3.2),
        circle(40, 74, 3.8),                                 # path dots
        circle(50, 72, 3.8),
        circle(60, 68, 3.8),
        circle(66, 62, 3.8),
        poly((68, 40), (72, 36), (84, 48), (80, 52)),        # X marks the spot
        poly((80, 36), (84, 40), (72, 52), (68, 48)),
        poly((78, 58), (78, 74), (88, 74)),                  # little boat sail
        poly((68, 74), (90, 74), (84, 82), (72, 82)),        # hull
    ]


PICTURES = {
    "ship": ship,
    "chest": chest,
    "parrot": parrot,
    "pirate": pirate,
    "island": island,
    "map": map_,
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
