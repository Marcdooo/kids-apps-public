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


def bus():
    return [
        BG,
        circle(84, 16, 8),                         # sun
        rect(0, 78, 100, 22),                      # road
        rect(8, 91, 18, 3),                        # road stripes
        rect(41, 91, 18, 3),
        rect(74, 91, 18, 3),
        rect(8, 32, 84, 44),                       # body
        rect(8, 58, 84, 6),                        # stripe
        rect(14, 38, 14, 14),                      # windows
        rect(32, 38, 14, 14),
        rect(50, 38, 14, 14),
        rect(70, 38, 16, 22),                      # door
        circle(91, 68, 3.6),                       # headlight
        circle(26, 76, 9),                         # wheels
        circle(74, 76, 9),
        circle(26, 76, 4),                         # hubs
        circle(74, 76, 4),
    ]


def train():
    return [
        BG,
        circle(82, 14, 8),                         # sun
        circle(22, 12, 5),                         # smoke
        circle(31, 7, 4),
        rect(0, 82, 100, 18),                      # ground
        rect(0, 80, 100, 3),                       # rail
        rect(14, 22, 16, 5),                       # chimney top
        rect(16, 26, 12, 16),                      # chimney
        rect(8, 40, 52, 30),                       # boiler
        rect(56, 24, 36, 6),                       # cab roof
        rect(58, 30, 32, 40),                      # cab
        rect(66, 36, 16, 14),                      # cab window
        poly((8, 62), (0, 78), (14, 78), (14, 62)),  # front guard
        circle(24, 74, 8),                         # wheels
        circle(44, 74, 8),
        circle(72, 74, 8),
        circle(24, 74, 3.5),                       # hubs
        circle(44, 74, 3.5),
        circle(72, 74, 3.5),
    ]


def plane():
    return [
        BG,
        ellipse(22, 18, 14, 6),                    # clouds
        ellipse(76, 84, 16, 6),
        poly((22, 50), (14, 28), (30, 42)),        # tail fin
        poly((40, 46), (30, 24), (46, 24), (58, 46)),    # far wing
        ellipse(50, 52, 38, 10),                   # body
        poly((44, 56), (32, 80), (52, 80), (66, 56)),    # near wing
        circle(46, 49, 3.6),                       # windows
        circle(56, 49, 3.6),
        circle(66, 49, 3.6),
        poly((74, 44), (82, 46), (84, 52), (74, 52)),    # cockpit
    ]


def boat():
    return [
        BG,
        circle(18, 16, 9),                         # sun
        rect(0, 68, 100, 32),                      # sea
        ellipse(20, 92, 12, 3.5),                  # waves
        ellipse(72, 94, 14, 3.5),
        rect(46, 14, 6, 52),                       # mast
        poly((52, 14), (52, 60), (80, 60)),        # big sail
        poly((46, 22), (46, 60), (24, 60)),        # small sail
        poly((18, 62), (82, 62), (70, 84), (30, 84)),    # hull
        circle(40, 72, 3.8),                       # portholes
        circle(52, 72, 3.8),
        circle(64, 72, 3.8),
    ]


def truck():
    return [
        BG,
        circle(16, 16, 8),                         # sun
        rect(0, 80, 100, 20),                      # road
        rect(10, 93, 18, 3),                       # road stripes
        rect(44, 93, 18, 3),
        rect(78, 93, 16, 3),
        rect(8, 32, 56, 46),                       # cargo box
        circle(36, 54, 11),                        # emblem
        poly((64, 46), (78, 46), (92, 60), (92, 78), (64, 78)),  # cab
        poly((68, 50), (76, 50), (85, 60), (68, 60)),    # cab window
        circle(90, 70, 3.6),                       # headlight
        circle(24, 78, 9),                         # wheels
        circle(50, 78, 9),
        circle(78, 78, 9),
        circle(24, 78, 4),                         # hubs
        circle(50, 78, 4),
        circle(78, 78, 4),
    ]


def helicopter():
    return [
        BG,
        ellipse(18, 82, 14, 5),                    # clouds
        ellipse(84, 16, 12, 5),
        poly((64, 46), (92, 40), (92, 50), (70, 58)),    # tail boom
        poly((86, 44), (88, 24), (96, 24), (94, 44)),    # tail fin
        rect(36, 64, 4, 14),                       # skid legs
        rect(58, 64, 4, 14),
        rect(26, 78, 46, 4),                       # skid
        ellipse(46, 52, 26, 16),                   # body
        poly((52, 40), (64, 44), (68, 54), (52, 54)),    # cockpit window
        circle(34, 50, 5),                         # side window
        rect(44, 26, 5, 12),                       # rotor mast
        rect(12, 20, 70, 6),                       # rotor blade
    ]


PICTURES = {
    "bus": bus,
    "train": train,
    "plane": plane,
    "boat": boat,
    "truck": truck,
    "helicopter": helicopter,
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
