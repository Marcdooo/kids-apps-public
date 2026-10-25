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


GROUND = rect(0, 86, 100, 14)
SUN = circle(88, 14, 6)


def butterfly():
    return [
        BG,
        GROUND,
        rotated_ellipse(32, 60, 17, 11, 30),                 # lower wings
        rotated_ellipse(68, 60, 17, 11, -30),
        rotated_ellipse(30, 36, 20, 13, -35),                # upper wings
        rotated_ellipse(70, 36, 20, 13, 35),
        circle(26, 34, 4.8),                                 # wing spots
        circle(74, 34, 4.8),
        circle(30, 62, 3.8),
        circle(70, 62, 3.8),
        ellipse(50, 52, 4.8, 22),                            # body
        circle(50, 26, 5.6),                                 # head
        rotated_ellipse(43, 15, 1.8, 9, -25),                # antennae
        rotated_ellipse(57, 15, 1.8, 9, 25),
        SUN,
    ]


def ladybug():
    return [
        BG,
        GROUND,
        ellipse(50, 92, 40, 7),                              # leaf
        rotated_ellipse(40, 14, 1.8, 8, -25),                # antennae
        rotated_ellipse(60, 14, 1.8, 8, 25),
        circle(50, 28, 13),                                  # head
        circle(50, 58, 30),                                  # shell
        rect(48, 32, 4, 56),                                 # center line
        circle(34, 50, 6.6),                                 # spots
        circle(66, 50, 6.6),
        circle(32, 72, 6.2),
        circle(68, 72, 6.2),
        circle(44, 26, 3.6),                                 # eyes
        circle(56, 26, 3.6),
        SUN,
    ]


def bee():
    return [
        BG,
        GROUND,
        rotated_ellipse(42, 32, 9, 17, -25),                 # wings
        rotated_ellipse(60, 30, 9, 17, 25),
        rotated_ellipse(40, 22, 1.8, 8, -20),                # antennae
        ellipse(54, 58, 28, 21),                             # body
        ellipse(46, 58, 4.4, 17),                            # stripes
        ellipse(58, 58, 4.4, 18),
        ellipse(70, 58, 4, 13),
        poly((80, 54), (95, 58), (80, 63)),                  # stinger
        circle(24, 58, 12),                                  # head
        circle(21, 54, 3.8),                                 # eye
        ellipse(19, 64, 4.6, 2.8),                           # smile
        circle(14, 20, 6),                                   # flower
        circle(20, 16, 6),
        circle(18, 24, 6),
        SUN,
    ]


def snail():
    return [
        BG,
        GROUND,
        ellipse(48, 80, 36, 8),                              # body
        ellipse(17, 66, 7.6, 14),                            # neck and head
        rect(12, 44, 3.6, 14),                               # eye stalks
        rect(21, 44, 3.6, 14),
        circle(13.8, 42, 4),                                 # eyes
        circle(22.8, 42, 4),
        circle(58, 54, 26),                                  # shell
        circle(58, 54, 17),
        circle(58, 54, 8),
        ellipse(15, 70, 3.8, 2.4),                           # smile
        circle(14, 16, 6),                                   # cloud
        circle(24, 14, 7),
        SUN,
    ]


def caterpillar():
    return [
        BG,
        GROUND,
        ellipse(48, 90, 44, 8),                              # leaf
        circle(18, 70, 11),                                  # segments
        circle(32, 62, 11.4),
        circle(46, 56, 11.8),
        circle(60, 56, 11.4),
        circle(72, 62, 11),
        circle(82, 50, 14),                                  # head
        rotated_ellipse(76, 30, 1.8, 8, -20),                # antennae
        rotated_ellipse(90, 30, 1.8, 8, 20),
        circle(78, 47, 3.6),                                 # eyes
        circle(88, 47, 3.6),
        ellipse(83, 57, 5, 2.8),                             # smile
        circle(14, 20, 6),
        SUN,
    ]


def dragonfly():
    return [
        BG,
        rect(0, 88, 100, 12),                                # pond
        rotated_ellipse(30, 38, 19, 6.4, -12),               # wings
        rotated_ellipse(70, 38, 19, 6.4, 12),
        rotated_ellipse(32, 52, 17, 5.6, 10),
        rotated_ellipse(68, 52, 17, 5.6, -10),
        rect(46, 50, 8, 36),                                 # tail
        poly((46, 86), (54, 86), (50, 96)),                  # tail tip
        ellipse(50, 44, 9, 11),                              # thorax
        circle(50, 24, 9.6),                                 # head
        circle(45, 22, 3.4),                                 # eyes
        circle(55, 22, 3.4),
        circle(14, 16, 6),                                   # cloud
        circle(24, 14, 7),
        SUN,
    ]


PICTURES = {
    "butterfly": butterfly,
    "ladybug": ladybug,
    "bee": bee,
    "snail": snail,
    "caterpillar": caterpillar,
    "dragonfly": dragonfly,
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
