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


def whale():
    return [
        BG,
        rect(0, 90, 100, 10),                                # sand
        poly((78, 58), (90, 40), (98, 38), (94, 52), (98, 66), (90, 66)),   # tail
        ellipse(46, 60, 36, 22),                             # body
        ellipse(42, 72, 24, 8),                              # belly
        rotated_ellipse(52, 76, 8, 3.5, 25),                 # fin
        circle(24, 54, 3.4),                                 # eye
        poly((28, 40), (20, 20), (28, 27), (36, 20)),        # spout
        circle(14, 78, 3.6),                                 # bubbles
        circle(9, 66, 3.2),
        circle(86, 20, 5),
    ]


def octopus():
    return [
        BG,
        rect(0, 92, 100, 8),                                 # sand
        rotated_ellipse(24, 68, 5, 20, 30),                  # tentacles
        rotated_ellipse(36, 74, 5, 18, 12),
        rotated_ellipse(64, 74, 5, 18, -12),
        rotated_ellipse(76, 68, 5, 20, -30),
        rotated_ellipse(46, 78, 5, 14, 4),
        rotated_ellipse(54, 78, 5, 14, -4),
        circle(50, 36, 24),                                  # head
        circle(41, 34, 5),                                   # eyes
        circle(59, 34, 5),
        ellipse(50, 48, 7, 3.4),                             # mouth
        circle(36, 22, 3.6),                                 # spots
        circle(62, 20, 3.6),
        circle(12, 14, 5),                                   # bubbles
        circle(88, 30, 4.4),
    ]


def crab():
    return [
        BG,
        rect(0, 86, 100, 14),                                # sand
        rotated_ellipse(22, 66, 11, 3.2, -18),               # legs
        rotated_ellipse(20, 74, 11, 3.2, 8),
        rotated_ellipse(78, 66, 11, 3.2, 18),
        rotated_ellipse(80, 74, 11, 3.2, -8),
        rect(39, 34, 5, 16),                                 # eye stalks
        rect(56, 34, 5, 16),
        rotated_ellipse(24, 52, 3.5, 12, -35),               # arms
        rotated_ellipse(76, 52, 3.5, 12, 35),
        ellipse(50, 62, 26, 16),                             # shell
        circle(18, 36, 11),                                  # claws
        circle(82, 36, 11),
        poly((18, 36), (11, 22), (22, 25)),                  # claw notches
        poly((82, 36), (89, 22), (78, 25)),
        circle(41.5, 31, 5),                                 # eyes
        circle(58.5, 31, 5),
        ellipse(50, 70, 8, 3.4),                             # mouth
        circle(40, 58, 3.6),
        circle(60, 58, 3.6),
    ]


def starfish():
    return [
        BG,
        rect(0, 84, 100, 16),                                # sand
        star(50, 52, 42, 18),                                # starfish
        circle(50, 52, 10),                                  # center
        circle(50, 24, 3.5),                                 # dots on arms
        circle(22, 44, 3.5),
        circle(78, 44, 3.5),
        circle(32, 74, 3.5),
        circle(68, 74, 3.5),
        circle(12, 14, 5),                                   # bubbles
        circle(90, 22, 4.4),
        circle(86, 10, 3.2),
    ]


def jellyfish():
    return [
        BG,
        ellipse(32, 66, 3.4, 20),                            # tentacles
        ellipse(42, 70, 3.4, 20),
        ellipse(52, 72, 3.4, 20),
        ellipse(62, 70, 3.4, 20),
        ellipse(72, 66, 3.4, 20),
        half_ellipse(52, 52, 32, 30),                        # dome
        rect(20, 52, 64, 6),                                 # rim
        circle(40, 36, 4.2),                                 # spots
        circle(56, 30, 4.2),
        circle(68, 42, 4.2),
        circle(14, 20, 5),                                   # bubbles
        circle(88, 18, 4.4),
        circle(90, 80, 4.4),
    ]


def submarine():
    return [
        BG,
        rect(0, 90, 100, 10),                                # sand
        rect(44, 32, 18, 30),                                # tower
        rect(58, 18, 4, 16),                                 # periscope
        rect(58, 18, 12, 4),
        poly((84, 50), (97, 42), (97, 74), (84, 66)),        # propeller
        ellipse(50, 58, 36, 17),                             # hull
        circle(32, 58, 5.4),                                 # windows
        circle(50, 58, 5.4),
        circle(68, 58, 5.4),
        circle(12, 36, 4.4),                                 # bubbles
        circle(8, 24, 3.4),
        circle(90, 20, 5),
    ]


PICTURES = {
    "whale": whale,
    "octopus": octopus,
    "crab": crab,
    "starfish": starfish,
    "jellyfish": jellyfish,
    "submarine": submarine,
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
