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


def cow():
    return [
        BG,
        GROUND,
        rect(84, 42, 3.4, 22),                               # tail
        circle(85.7, 66, 4.2),                               # tail tuft
        rect(31, 66, 7, 20),                                 # legs
        rect(43, 66, 7, 20),
        rect(62, 66, 7, 20),
        rect(74, 66, 7, 20),
        ellipse(56, 56, 30, 18),                             # body
        ellipse(48, 51, 8, 6),                               # spots
        ellipse(70, 62, 7, 5),
        rotated_ellipse(32, 38, 7, 3.4, -30),                # ears
        rotated_ellipse(12, 36, 7, 3.4, 30),
        poly((17, 38), (13, 24), (24, 33)),                  # horns
        poly((27, 36), (32, 23), (35, 35)),
        ellipse(22, 47, 13, 12),                             # head
        ellipse(15, 53, 8, 5.4),                             # muzzle
        circle(20, 43, 3.2),                                 # eye
        SUN,
    ]


def pig():
    return [
        BG,
        GROUND,
        ellipse(72, 92, 18, 5),                              # mud
        rect(32, 66, 8, 18),                                 # legs
        rect(44, 66, 8, 18),
        rect(62, 66, 8, 18),
        rect(74, 66, 8, 18),
        circle(88, 52, 4.4),                                 # tail curl
        ellipse(56, 56, 32, 21),                             # body
        poly((24, 44), (26, 26), (38, 40)),                  # ear
        ellipse(24, 54, 16, 15),                             # head
        ellipse(13, 58, 8, 6.4),                             # snout
        circle(11, 58, 3.2),                                 # nostril
        circle(17, 58, 3.2),
        circle(24, 48, 3.4),                                 # eye
        ellipse(36, 56, 4.4, 3.6),                           # cheek
        SUN,
    ]


def chicken():
    return [
        BG,
        GROUND,
        rect(40, 70, 6, 18),                                 # legs
        rect(56, 70, 6, 18),
        poly((70, 52), (92, 28), (90, 58)),                  # tail
        ellipse(52, 58, 26, 22),                             # body
        rotated_ellipse(56, 60, 13, 8, 18),                  # wing
        circle(29, 23, 4.8),                                 # comb
        circle(36, 21, 4.8),
        circle(43, 24, 4.8),
        circle(32, 38, 13),                                  # head
        poly((20, 36), (6, 41), (20, 46)),                   # beak
        ellipse(23, 51, 3.6, 5),                             # wattle
        circle(31, 34, 3.4),                                 # eye
        ellipse(82, 88, 6, 7.6),                             # egg
        SUN,
    ]


def sheep():
    return [
        BG,
        GROUND,
        rect(36, 70, 6, 18),                                 # legs
        rect(46, 70, 6, 18),
        rect(64, 70, 6, 18),
        rect(74, 70, 6, 18),
        ellipse(56, 58, 26, 14),                             # wool
        circle(42, 50, 13),
        circle(56, 44, 14),
        circle(70, 50, 13),
        rotated_ellipse(30, 40, 7, 3.2, 35),                 # ear
        ellipse(22, 54, 11, 13),                             # face
        circle(19, 49, 3.4),                                 # eye
        ellipse(18, 61, 4.6, 3.2),                           # nose
        circle(14, 18, 5.4),                                 # cloud puffs
        circle(24, 16, 6.4),
        circle(34, 19, 5),
        SUN,
    ]


def barn():
    return [
        BG,
        GROUND,
        rect(82, 42, 12, 42),                                # silo
        half_ellipse(88, 42, 6, 7),                          # silo dome
        rect(16, 46, 66, 38),                                # barn
        poly((10, 48), (49, 20), (88, 48)),                  # roof
        rect(42, 30, 14, 12),                                # hayloft window
        rect(40, 58, 10, 26),                                # doors
        rect(50, 58, 10, 26),
        rect(22, 56, 12, 12),                                # windows
        rect(66, 56, 12, 12),
        circle(14, 14, 6),                                   # sun
        ellipse(70, 16, 12, 5),                              # cloud
    ]


def tractor():
    return [
        BG,
        GROUND,
        rect(80, 36, 5, 18),                                 # exhaust
        rect(52, 50, 36, 18),                                # hood
        rect(22, 30, 30, 38),                                # cab
        rect(26, 34, 22, 18),                                # window
        rect(18, 24, 38, 6),                                 # roof
        circle(32, 70, 17),                                  # big wheel
        circle(32, 70, 7),                                   # hub
        circle(78, 76, 11),                                  # small wheel
        circle(78, 76, 4.4),                                 # hub
        circle(88, 14, 6),                                   # sun
    ]


PICTURES = {
    "cow": cow,
    "pig": pig,
    "chicken": chicken,
    "sheep": sheep,
    "barn": barn,
    "tractor": tractor,
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
