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


def cat():
    return [
        BG,
        poly((20, 44), (24, 8), (46, 28)),         # ears
        poly((80, 44), (76, 8), (54, 28)),
        poly((26, 36), (28, 18), (40, 28)),        # inner ears
        poly((74, 36), (72, 18), (60, 28)),
        rect(0, 90, 100, 10),                      # grass
        ellipse(50, 58, 32, 28),                   # head
        circle(38, 52, 6),                         # eyes
        circle(62, 52, 6),
        poly((43, 60), (57, 60), (50, 69)),        # nose
        ellipse(29, 66, 5, 4),                     # cheeks
        ellipse(71, 66, 5, 4),
        ellipse(50, 79, 10, 4),                    # chin
    ]


def dog():
    return [
        BG,
        rect(0, 90, 100, 10),                      # grass
        ellipse(18, 50, 11, 24),                   # floppy ears
        ellipse(82, 50, 11, 24),
        ellipse(50, 50, 26, 32),                   # head
        ellipse(36, 28, 8, 6),                     # patch
        circle(40, 42, 5),                         # eyes
        circle(60, 42, 5),
        ellipse(50, 66, 16, 13),                   # snout
        ellipse(50, 60, 7, 5),                     # nose
        ellipse(50, 80, 5.5, 8),                   # tongue
    ]


def fish():
    return [
        BG,
        rect(0, 90, 100, 10),                      # sand
        circle(82, 20, 6),                         # bubbles
        circle(72, 34, 4.5),
        circle(60, 10, 4),
        ellipse(12, 76, 6, 15),                    # seaweed
        ellipse(90, 80, 5, 11),
        poly((68, 50), (94, 30), (94, 70)),        # tail
        poly((32, 36), (46, 16), (60, 34)),        # top fin
        poly((38, 64), (48, 78), (58, 64)),        # bottom fin
        ellipse(44, 50, 30, 20),                   # body
        rect(52, 34, 6, 32),                       # stripe
        circle(26, 45, 4.6),                       # eye
    ]


def bird():
    return [
        BG,
        circle(16, 16, 9),                         # sun
        rect(0, 78, 100, 6),                       # branch
        ellipse(18, 92, 10, 4.5),                  # leaves
        ellipse(82, 92, 10, 4.5),
        poly((26, 52), (6, 46), (8, 66), (28, 66)),    # tail
        ellipse(50, 58, 26, 20),                   # body
        ellipse(54, 66, 14, 9),                    # belly
        ellipse(42, 56, 12, 8),                    # wing
        circle(68, 36, 13),                        # head
        poly((79, 33), (95, 40), (79, 45)),        # beak
        circle(70, 33, 4),                         # eye
    ]


def turtle():
    return [
        BG,
        circle(82, 16, 8),                         # sun
        rect(0, 80, 100, 20),                      # ground
        poly((6, 66), (26, 56), (26, 72)),         # tail
        ellipse(34, 76, 8, 6),                     # legs
        ellipse(68, 76, 8, 6),
        circle(85, 58, 10),                        # head
        ellipse(50, 58, 30, 22),                   # shell
        poly((40, 48), (50, 42), (60, 48), (60, 60), (50, 66), (40, 60)),  # shell pattern
        circle(30, 58, 4.6),                       # shell dots
        circle(70, 58, 4.6),
        circle(88, 55, 4),                         # eye
    ]


def rabbit():
    return [
        BG,
        rect(0, 90, 100, 10),                      # grass
        ellipse(36, 24, 8, 22),                    # ears
        ellipse(64, 24, 8, 22),
        ellipse(36, 26, 4, 14),                    # inner ears
        ellipse(64, 26, 4, 14),
        ellipse(50, 62, 28, 24),                   # head
        circle(40, 58, 4.8),                       # eyes
        circle(60, 58, 4.8),
        ellipse(33, 70, 5, 4),                     # cheeks
        ellipse(67, 70, 5, 4),
        poly((44, 65), (56, 65), (50, 73)),        # nose
        rect(45, 75, 10, 9),                       # teeth
    ]


PICTURES = {
    "cat": cat,
    "dog": dog,
    "fish": fish,
    "bird": bird,
    "turtle": turtle,
    "rabbit": rabbit,
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
