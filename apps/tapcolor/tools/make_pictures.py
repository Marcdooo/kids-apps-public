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


def diamond(cx, cy, r):
    return poly((cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy))


BG = rect(0, 0, 100, 100)


def house():
    return [
        BG,
        rect(0, 78, 100, 22),                      # ground
        circle(82, 18, 9),                         # sun
        poly((44, 80), (56, 80), (68, 100), (32, 100)),  # path
        rect(62, 30, 8, 16),                       # chimney
        rect(24, 52, 52, 28),                      # wall
        poly((18, 52), (50, 24), (82, 52)),        # roof
        rect(44, 62, 12, 18),                      # door
        rect(30, 58, 10, 10),                      # window left
        rect(60, 58, 10, 10),                      # window right
    ]


def fish():
    return [
        BG,
        rect(0, 86, 100, 14),                      # sand
        poly((8, 90), (12, 62), (16, 90)),         # seaweed left
        poly((86, 90), (91, 66), (96, 90)),        # seaweed right
        circle(78, 22, 4.5),                       # bubbles
        circle(88, 18, 3.8),
        poly((64, 50), (88, 32), (88, 68)),        # tail
        poly((30, 38), (44, 18), (56, 38)),        # top fin
        poly((38, 62), (52, 62), (46, 80)),        # belly fin
        ellipse(42, 50, 26, 17),                   # body
        circle(28, 46, 3.8),                       # eye
    ]


def rocket():
    return [
        BG,
        diamond(15, 15, 4.5),                      # stars
        diamond(85, 20, 4.5),
        diamond(20, 58, 4.5),
        diamond(84, 60, 4.5),
        diamond(72, 90, 4.5),
        circle(16, 84, 11),                        # planet
        poly((42, 74), (58, 74), (50, 96)),        # flame
        poly((38, 56), (22, 78), (38, 76)),        # left fin
        poly((62, 56), (78, 78), (62, 76)),        # right fin
        rect(38, 22, 24, 54),                      # body
        poly((50, 6), (62, 22), (38, 22)),         # nose cone
        rect(38, 60, 24, 7),                       # band
        circle(50, 40, 7),                         # window
    ]


def flower():
    regions = [
        BG,
        rect(0, 80, 100, 20),                      # ground
        rect(47, 46, 6, 40),                       # stem
        rotated_ellipse(36, 68, 11, 4.8, -25),     # left leaf
        rotated_ellipse(64, 62, 11, 4.8, 25),      # right leaf
    ]
    cx, cy = 50, 34
    for k in range(8):                             # petals
        ang = math.radians(k * 45)
        regions.append(rotated_ellipse(
            round(cx + 15 * math.cos(ang), 2),
            round(cy + 15 * math.sin(ang), 2),
            10, 6.5, k * 45))
    regions.append(circle(cx, cy, 8.5))            # center
    return regions


def car():
    return [
        BG,
        circle(20, 18, 8),                         # sun
        rect(0, 72, 100, 28),                      # road
        rect(10, 90, 20, 3),                       # road stripes
        rect(45, 90, 20, 3),
        rect(80, 90, 15, 3),
        poly((28, 50), (36, 32), (66, 32), (76, 50)),          # cabin
        poly((8, 56), (16, 50), (84, 50), (92, 58), (92, 70), (8, 70)),  # body
        poly((33, 48), (39, 36), (48, 36), (48, 48)),          # window left
        poly((52, 48), (52, 36), (63, 36), (70, 48)),          # window right
        circle(87, 60, 3.5),                       # headlight
        circle(28, 72, 9),                         # wheels
        circle(72, 72, 9),
        circle(28, 72, 4),                         # hubs
        circle(72, 72, 4),
    ]


def cat():
    return [
        BG,
        poly((22, 44), (26, 12), (46, 28)),        # left ear
        poly((78, 44), (74, 12), (54, 28)),        # right ear
        circle(50, 56, 32),                        # head
        circle(38, 50, 6),                         # eyes
        circle(62, 50, 6),
        ellipse(50, 70, 14, 9),                    # muzzle
        poly((44, 61), (56, 61), (50, 69)),        # nose
    ]


PICTURES = {
    "house": house,
    "fish": fish,
    "rocket": rocket,
    "flower": flower,
    "car": car,
    "cat": cat,
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
