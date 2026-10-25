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


def ground():
    return rect(0, 86, 100, 14)


def sun(x=88, y=14, r=8):
    return circle(x, y, r)


def trex():
    return [
        BG,
        sun(),
        ground(),
        poly((66, 50), (98, 74), (62, 72)),                  # tail
        ellipse(56, 60, 24, 17),                             # body
        ellipse(52, 68, 14, 6.4),                            # belly
        poly((36, 46), (46, 30), (62, 46), (46, 64)),        # neck
        poly((5, 36), (26, 20), (48, 22), (50, 44), (30, 46), (7, 47)),   # head
        poly((7, 47), (30, 46), (30, 56), (12, 52)),         # jaw
        circle(35, 30, 3.6),                                 # eye
        ellipse(36, 64, 3.6, 6.4),                           # arm
        ellipse(60, 74, 10, 12),                             # leg
        poly((46, 87), (54, 80), (68, 80), (72, 89), (46, 89)),   # foot
        circle(64, 56, 4),                                   # spots
        circle(76, 64, 3.6),
    ]


def triceratops():
    return [
        BG,
        sun(),
        ground(),
        poly((80, 54), (98, 64), (80, 70)),                  # tail
        ellipse(40, 80, 7, 11),                              # legs
        ellipse(70, 80, 7, 11),
        ellipse(58, 60, 26, 16),                             # body
        rotated_ellipse(32, 46, 13, 16, -15),                # frill
        ellipse(26, 60, 13, 10),                             # head
        poly((14, 58), (2, 60), (14, 66)),                   # nose horn
        poly((26, 52), (22, 36), (32, 50)),                  # brow horns
        poly((34, 50), (36, 34), (40, 48)),
        circle(22, 58, 3.2),                                 # eye
        circle(30, 40, 3.4),                                 # frill dots
        circle(40, 46, 3.4),
        circle(52, 62, 4),                                   # body spots
        circle(66, 56, 4),
    ]


def stegosaurus():
    return [
        BG,
        sun(),
        ground(),
        diamond(36, 40, 8),                                  # plates
        diamond(48, 35, 9),
        diamond(60, 35, 9),
        diamond(71, 41, 8),
        poly((78, 62), (98, 72), (80, 74)),                  # tail
        poly((86, 66), (94, 52), (94, 68)),                  # tail spike
        ellipse(50, 62, 32, 16),                             # body
        ellipse(15, 66, 9, 7),                               # head
        circle(12, 64, 3.2),                                 # eye
        ellipse(34, 82, 7, 10),                              # legs
        ellipse(66, 82, 7, 10),
        circle(46, 62, 4),                                   # spots
        circle(58, 66, 4),
    ]


def brachiosaurus():
    return [
        BG,
        sun(),
        ground(),
        rect(10, 50, 5, 36),                                 # tree trunk
        circle(13, 42, 10),                                   # tree top
        poly((84, 62), (98, 74), (84, 74)),                  # tail
        ellipse(62, 64, 26, 15),                             # body
        poly((38, 60), (28, 16), (40, 14), (50, 54)),        # neck
        ellipse(32, 13, 10, 6.4),                            # head
        circle(28, 12, 3.2),                                 # eye
        ellipse(46, 82, 6, 10),                              # legs
        ellipse(58, 82, 6, 10),
        ellipse(70, 82, 6, 10),
        ellipse(80, 82, 6, 10),
        circle(60, 60, 4),                                   # spots
        circle(72, 66, 4),
    ]


def pterodactyl():
    return [
        BG,
        sun(),
        ellipse(22, 78, 14, 6),                              # clouds
        ellipse(80, 80, 16, 6),
        poly((46, 48), (6, 18), (24, 54)),                   # wings
        poly((54, 48), (94, 20), (78, 56)),
        poly((58, 52), (88, 66), (60, 58)),                  # tail
        ellipse(50, 52, 11, 7),                              # body
        circle(38, 46, 6.4),                                 # head
        poly((34, 42), (8, 50), (34, 52)),                   # beak
        poly((42, 41), (52, 30), (46, 44)),                  # crest
        circle(36, 44, 3.2),                                 # eye
    ]


def egg():
    return [
        BG,
        sun(),
        ground(),
        circle(50, 44, 18),                                  # baby dino head
        poly((50, 20), (43, 29), (57, 29)),                  # head spike
        circle(43, 40, 3.4),                                 # eyes
        circle(57, 40, 3.4),
        ellipse(50, 49, 6.4, 2.8),                             # mouth
        poly((26, 60), (34, 52), (42, 62), (50, 54), (58, 62), (66, 52), (74, 60),
             (76, 70), (72, 80), (64, 86), (36, 86), (28, 80), (24, 70)),   # eggshell
        circle(38, 70, 4),                                   # shell spots
        circle(58, 74, 4.4),
        circle(66, 64, 3.6),
        ellipse(14, 78, 8, 4),                               # small stones
        ellipse(88, 80, 8, 4),
    ]


PICTURES = {
    "trex": trex,
    "triceratops": triceratops,
    "stegosaurus": stegosaurus,
    "brachiosaurus": brachiosaurus,
    "pterodactyl": pterodactyl,
    "egg": egg,
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
