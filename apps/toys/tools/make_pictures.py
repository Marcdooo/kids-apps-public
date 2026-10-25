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


def sector(cx, cy, r, a0, a1, steps=10):
    pts = [(cx, cy)]
    for i in range(steps + 1):
        a = math.radians(a0 + (a1 - a0) * i / steps)
        pts.append((round(cx + r * math.cos(a), 2), round(cy + r * math.sin(a), 2)))
    return poly(*pts)


def teddy():
    return [
        BG,
        GROUND,
        circle(28, 18, 10),                                  # ears
        circle(72, 18, 10),
        circle(28, 18, 5),                                   # inner ears
        circle(72, 18, 5),
        ellipse(34, 90, 12, 9),                              # feet
        ellipse(66, 90, 12, 9),
        rotated_ellipse(22, 66, 8, 16, 25),                  # arms
        rotated_ellipse(78, 66, 8, 16, -25),
        ellipse(50, 70, 23, 26),                             # body
        ellipse(50, 74, 14, 16),                             # belly
        circle(50, 36, 21),                                  # head
        ellipse(50, 45, 10, 8),                              # muzzle
        ellipse(50, 41, 4.4, 3.2),                           # nose
        circle(41, 31, 3.4),                                 # eyes
        circle(59, 31, 3.4),
        poly((50, 57), (36, 50), (36, 64)),                  # bow
        poly((50, 57), (64, 50), (64, 64)),
        circle(50, 57, 4),
        SUN,
    ]


def ball():
    return [
        BG,
        GROUND,
        ellipse(50, 89, 28, 6),                              # shadow
        sector(50, 46, 34, -90, -30),
        sector(50, 46, 34, -30, 30),
        sector(50, 46, 34, 30, 90),
        sector(50, 46, 34, 90, 150),
        sector(50, 46, 34, 150, 210),
        sector(50, 46, 34, 210, 270),
        circle(50, 46, 6),                                   # center
        circle(14, 24, 5),                                   # sparkles
        star(88, 62, 8, 3.6),
        star(12, 66, 8, 3.6),
    ]


def blocks():
    return [
        BG,
        GROUND,
        rect(12, 64, 36, 24),                                # bottom blocks
        rect(52, 64, 36, 24),
        rect(32, 40, 36, 24),                                # middle block
        poly((36, 40), (50, 14), (64, 40)),                  # roof block
        circle(30, 76, 7),                                   # shapes on blocks
        star(70, 76, 9, 4),
        diamond(50, 52, 8),
        circle(50, 31, 4.4),
        circle(90, 60, 4.4),
        circle(10, 40, 4.4),
        SUN,
    ]


def horse():
    return [
        BG,
        GROUND,
        half_ellipse(50, 84, 42, 11, top=False),             # rocker
        poly((30, 62), (40, 62), (32, 86), (22, 86)),        # legs
        poly((58, 62), (68, 62), (80, 86), (70, 86)),
        rotated_ellipse(82, 50, 4.4, 13, 28),                # tail
        ellipse(52, 56, 26, 14),                             # body
        poly((26, 58), (46, 52), (40, 26), (24, 32)),        # neck
        rotated_ellipse(44, 34, 3.4, 13, 25),                # mane
        rotated_ellipse(24, 26, 17, 8.4, -55),               # head
        poly((34, 12), (38, 2), (44, 14)),                   # ear
        circle(21, 24, 3.2),                                 # eye
        ellipse(54, 48, 11, 5.4),                            # saddle
        circle(88, 20, 6),
    ]


def kite():
    return [
        BG,
        GROUND,
        poly((50, 6), (78, 38), (50, 38)),                   # kite quarters
        poly((78, 38), (50, 74), (50, 38)),
        poly((50, 74), (22, 38), (50, 38)),
        poly((22, 38), (50, 6), (50, 38)),
        diamond(50, 82, 5.4),                                # tail bows
        diamond(44, 89, 5.4),
        diamond(53, 94, 5.4),
        ellipse(18, 14, 13, 6),                              # clouds
        ellipse(84, 56, 12, 5.6),
        circle(88, 14, 6),
    ]


def train():
    return [
        BG,
        GROUND,
        rect(0, 86, 100, 5),                                 # track
        circle(78, 14, 6),                                   # smoke
        circle(88, 8, 5),
        rect(70, 30, 10, 16),                                # chimney
        rect(66, 26, 18, 6),
        rect(10, 34, 34, 6),                                 # cab roof
        rect(14, 40, 30, 36),                                # cab
        rect(44, 48, 44, 28),                                # boiler
        half_ellipse(60, 48, 8, 8),                          # dome
        rect(20, 46, 16, 14),                                # window
        poly((88, 62), (98, 78), (88, 78)),                  # front
        circle(28, 76, 11),                                  # wheels
        circle(58, 80, 8),
        circle(76, 80, 8),
        circle(28, 76, 4.4),
    ]


PICTURES = {
    "teddy": teddy,
    "ball": ball,
    "blocks": blocks,
    "horse": horse,
    "kite": kite,
    "train": train,
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
