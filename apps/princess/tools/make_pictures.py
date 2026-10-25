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


def princess():
    return [
        BG,
        GROUND,
        ellipse(50, 28, 23, 25),                             # hair
        poly((34, 48), (66, 48), (90, 98), (10, 98)),        # gown
        rect(40, 44, 20, 16),                                # bodice
        circle(35, 52, 6.4),                                 # sleeves
        circle(65, 52, 6.4),
        rect(36, 58, 28, 5),                                 # belt
        star(50, 80, 9, 4),                                  # gown star
        circle(50, 30, 15),                                  # head
        poly((36, 16), (38, 5), (44, 11), (50, 2), (56, 11), (62, 5), (64, 16)),   # crown
        circle(43.5, 30, 3.2),                               # eyes
        circle(56.5, 30, 3.2),
        ellipse(50, 38, 5, 3),                               # mouth
        circle(14, 24, 4.4),
        circle(88, 30, 4.4),
        star(86, 62, 7, 3.2),
    ]


def castle():
    return [
        BG,
        GROUND,
        rect(30, 40, 40, 46),                                # keep
        rect(30, 33, 8, 8),                                  # battlements
        rect(46, 33, 8, 8),
        rect(62, 33, 8, 8),
        rect(10, 36, 18, 50),                                # towers
        rect(72, 36, 18, 50),
        poly((7, 36), (19, 14), (31, 36)),                   # tower roofs
        poly((69, 36), (81, 14), (93, 36)),
        poly((19, 14), (19, 3), (31, 8)),                    # flags
        poly((81, 14), (81, 3), (93, 8)),
        rect(14, 50, 10, 14),                                # tower windows
        rect(76, 50, 10, 14),
        circle(50, 50, 6),                                   # round window
        rect(43, 64, 14, 22),                                # gate
        half_ellipse(50, 64, 7, 7),
        circle(88, 90, 4.4),
        circle(8, 94, 4.4),
        SUN,
    ]


def dragon():
    return [
        BG,
        GROUND,
        poly((26, 68), (4, 86), (16, 90), (34, 80)),         # tail
        poly((4, 86), (2, 74), (16, 78)),                    # tail tip
        poly((34, 48), (28, 14), (56, 36)),                  # wings
        poly((50, 46), (54, 12), (72, 40)),
        ellipse(46, 64, 26, 22),                             # body
        ellipse(52, 70, 14, 14),                             # belly
        ellipse(34, 90, 11, 6),                              # feet
        ellipse(58, 90, 11, 6),
        poly((60, 54), (76, 54), (78, 36), (64, 34)),        # neck
        poly((30, 46), (34, 36), (39, 45)),                  # back spikes
        poly((40, 42), (45, 32), (50, 42)),
        ellipse(74, 28, 15, 12),                             # head
        ellipse(87, 32, 9, 6.4),                             # snout
        poly((64, 20), (66, 6), (73, 17)),                   # horns
        poly((77, 16), (84, 6), (86, 20)),
        circle(73, 25, 3.2),                                 # eye
        circle(88, 30, 3),                                   # nostril
        circle(10, 30, 4.4),
        star(86, 62, 7, 3.2),
    ]


def crown():
    return [
        BG,
        GROUND,
        poly((18, 58), (18, 28), (34, 46), (50, 20), (66, 46), (82, 28), (82, 58)),   # points
        circle(18, 24, 5.4),                                 # ball tips
        circle(50, 16, 5.4),
        circle(82, 24, 5.4),
        rect(16, 56, 68, 28),                                # band
        rect(16, 56, 68, 6),                                 # rim
        circle(32, 72, 6),                                   # jewels
        diamond(50, 72, 9),
        circle(68, 72, 6),
        star(12, 54, 8, 3.6),                                # sparkles
        star(90, 50, 8, 3.6),
        circle(88, 90, 4.4),
        circle(10, 92, 4.4),
    ]


def knight():
    return [
        BG,
        GROUND,
        ellipse(50, 84, 33, 16),                             # shoulders
        rect(12, 28, 5, 36),                                 # sword blade
        poly((11, 28), (14.5, 14), (18, 28)),                # sword tip
        rect(8, 62, 13, 5),                                  # hilt
        rect(12, 67, 5, 12),                                 # grip
        circle(14.5, 82, 4),                                 # pommel
        poly((68, 60), (92, 60), (92, 78), (80, 96), (68, 78)),   # shield
        rect(78, 64, 4, 28),                                 # shield cross
        rect(70, 70, 20, 4),
        rotated_ellipse(60, 10, 14, 4.4, -25),               # plume
        half_ellipse(50, 26, 18, 16),                        # helmet top
        rect(32, 26, 36, 36),                                # helmet
        rect(34, 36, 32, 10),                                # visor
        circle(43, 41, 3.2),                                 # eyes
        circle(57, 41, 3.2),
        rect(44, 50, 12, 8),                                 # chin guard
        circle(90, 20, 5),
    ]


def carriage():
    return [
        BG,
        GROUND,
        rect(44, 22, 12, 8),                                 # stem
        ellipse(50, 54, 33, 26),                             # pumpkin
        ellipse(36, 54, 11, 24),                             # segments
        ellipse(64, 54, 11, 24),
        rect(40, 42, 20, 16),                                # window
        rect(10, 76, 80, 5),                                 # axle
        circle(28, 80, 13),                                  # wheels
        circle(72, 80, 13),
        circle(28, 80, 5),
        circle(72, 80, 5),
        star(12, 20, 8, 3.6),                                # sparkles
        star(88, 20, 8, 3.6),
        circle(88, 52, 4.4),
    ]


PICTURES = {
    "princess": princess,
    "castle": castle,
    "dragon": dragon,
    "crown": crown,
    "knight": knight,
    "carriage": carriage,
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
