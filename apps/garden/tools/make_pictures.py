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


def sunflower():
    petals = []
    for k in range(12):
        a = math.radians(k * 30)
        petals.append(rotated_ellipse(50 + 21 * math.cos(a), 32 + 21 * math.sin(a), 9.4, 4.6, k * 30))
    return [
        BG,
        GROUND,
        rect(47, 50, 6, 44),                                 # stem
        rotated_ellipse(36, 74, 11, 4.6, -30),               # leaves
        rotated_ellipse(64, 66, 11, 4.6, 30),
    ] + petals + [
        circle(50, 32, 13),                                  # center
        circle(14, 90, 4.4),
        circle(88, 88, 4.4),
        circle(10, 26, 4.4),
        circle(90, 56, 4.4),
    ]


def tulip():
    return [
        BG,
        GROUND,
        rect(47, 56, 6, 38),                                 # stem
        rotated_ellipse(32, 76, 17, 5.4, -50),               # leaves
        rotated_ellipse(68, 72, 17, 5.4, 50),
        rotated_ellipse(38, 36, 11, 21, 14),                 # petals
        rotated_ellipse(62, 36, 11, 21, -14),
        ellipse(50, 34, 11, 22),
        circle(14, 24, 4.4),
        circle(88, 30, 4.4),
        circle(14, 90, 4.4),
        circle(88, 92, 4.4),
        SUN,
    ]


def tree():
    return [
        BG,
        GROUND,
        rect(43, 52, 14, 40),                                # trunk
        circle(32, 42, 17),                                  # leaves
        circle(68, 42, 17),
        circle(50, 28, 23),
        circle(40, 32, 4),                                   # apples
        circle(60, 26, 4),
        circle(50, 46, 4),
        circle(26, 48, 4),
        circle(74, 46, 4),
        circle(14, 88, 4.4),
        circle(88, 90, 4.4),
        SUN,
    ]


def mushroom():
    return [
        BG,
        GROUND,
        poly((38, 60), (62, 60), (64, 90), (36, 90)),        # stem
        half_ellipse(50, 62, 38, 38),                        # cap
        ellipse(50, 62, 30, 5),                              # gills
        circle(34, 46, 6),                                   # spots
        circle(54, 34, 7),
        circle(68, 50, 5.4),
        circle(46, 52, 4.4),
        rect(80, 78, 6, 12),                                 # small mushroom
        half_ellipse(83, 78, 10, 9),
        circle(14, 88, 4.4),
        circle(16, 22, 5),
        SUN,
    ]


def wateringcan():
    return [
        BG,
        GROUND,
        poly((30, 42), (34, 22), (56, 22), (60, 42), (53, 42), (51, 29), (39, 29), (37, 42)),   # handle
        poly((60, 62), (84, 36), (89, 41), (60, 78)),        # spout
        poly((82, 28), (98, 36), (91, 46), (78, 38)),        # sprinkler head
        rect(24, 42, 40, 42),                                # body
        rect(24, 54, 40, 6),                                 # band
        ellipse(90, 60, 3.6, 5.4),                           # water drops
        ellipse(82, 72, 3.6, 5.4),
        ellipse(94, 76, 3.6, 5.4),
        circle(14, 90, 4.4),
        circle(60, 92, 4.4),
        SUN,
    ]


def nest():
    return [
        BG,
        GROUND,
        rect(0, 72, 100, 8),                                 # branch
        rotated_ellipse(14, 62, 8, 4, -30),                  # leaves
        rotated_ellipse(88, 62, 8, 4, 30),
        half_ellipse(50, 62, 36, 22, top=False),             # nest bowl
        ellipse(36, 58, 8, 10.4),                            # eggs
        ellipse(50, 55, 8, 10.4),
        ellipse(64, 58, 8, 10.4),
        ellipse(50, 64, 38, 6),                              # nest rim
        rotated_ellipse(26, 78, 14, 2.8, 8),                 # twigs
        rotated_ellipse(72, 80, 14, 2.8, -8),
        ellipse(22, 20, 13, 5.4),                            # cloud
        circle(84, 18, 6),
    ]


PICTURES = {
    "sunflower": sunflower,
    "tulip": tulip,
    "tree": tree,
    "mushroom": mushroom,
    "wateringcan": wateringcan,
    "nest": nest,
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
