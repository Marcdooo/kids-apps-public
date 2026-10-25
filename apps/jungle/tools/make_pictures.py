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


def lion():
    return [
        BG,
        GROUND,
        star(50, 50, 46, 36, points=12),                     # mane
        circle(30, 24, 8),                                   # ears
        circle(70, 24, 8),
        circle(50, 52, 24),                                  # face
        ellipse(50, 64, 13, 10),                             # muzzle
        poly((43, 56), (57, 56), (50, 66)),                  # nose
        circle(41, 46, 3.4),                                 # eyes
        circle(59, 46, 3.4),
        ellipse(50, 74, 6, 3.6),                             # mouth
        circle(12, 12, 5),
        circle(90, 88, 5),
    ]


def elephant():
    return [
        BG,
        GROUND,
        ellipse(20, 46, 17, 24),                             # ears
        ellipse(80, 46, 17, 24),
        ellipse(20, 46, 9, 15),                              # inner ears
        ellipse(80, 46, 9, 15),
        ellipse(50, 46, 23, 28),                             # head
        rect(43, 58, 14, 30),                                # trunk
        ellipse(50, 88, 10, 7),                              # trunk tip
        rotated_ellipse(36, 74, 3.6, 9, 15),                 # tusks
        rotated_ellipse(64, 74, 3.6, 9, -15),
        circle(41, 40, 3.4),                                 # eyes
        circle(59, 40, 3.4),
        circle(88, 14, 6),
        circle(10, 86, 5),
    ]


def giraffe():
    return [
        BG,
        GROUND,
        rect(26, 88, 8, 12),                                 # legs
        rect(66, 88, 8, 12),
        poly((36, 82), (64, 82), (58, 30), (42, 30)),        # neck
        ellipse(50, 84, 36, 12),                             # body
        circle(50, 54, 4.4),                                 # spots
        circle(48, 68, 4.8),
        circle(42, 84, 4.4),
        circle(62, 82, 4.8),
        circle(76, 86, 4.4),
        rect(40, 2, 6, 14),                                  # horns
        rect(54, 2, 6, 14),
        rotated_ellipse(34, 20, 7, 3.4, -30),                # ears
        rotated_ellipse(66, 20, 7, 3.4, 30),
        ellipse(50, 24, 14, 11),                             # head
        ellipse(50, 30, 8, 5),                               # muzzle
        circle(43, 22, 3.2),                                 # eyes
        circle(57, 22, 3.2),
        circle(86, 14, 6),
    ]


def monkey():
    return [
        BG,
        GROUND,
        rotated_ellipse(80, 86, 3.6, 14, 40),                # tail
        ellipse(50, 84, 22, 14),                             # body
        rotated_ellipse(26, 80, 6, 13, 25),                  # arms
        rotated_ellipse(74, 80, 6, 13, -25),
        circle(24, 46, 10),                                  # ears
        circle(76, 46, 10),
        circle(24, 46, 5),
        circle(76, 46, 5),
        circle(50, 40, 25),                                  # head
        circle(41, 38, 10),                                  # face lobes
        circle(59, 38, 10),
        ellipse(50, 52, 14, 11),
        circle(41, 38, 3.2),                                 # eyes
        circle(59, 38, 3.2),
        circle(50, 48, 3.4),                                 # nose
        ellipse(50, 57, 7, 3.6),                             # mouth
        rotated_ellipse(12, 24, 4, 12, -30),                 # banana
    ]


def zebra():
    return [
        BG,
        GROUND,
        rect(26, 66, 7, 20),                                 # legs
        rect(36, 66, 7, 20),
        rect(60, 66, 7, 20),
        rect(70, 66, 7, 20),
        rotated_ellipse(82, 56, 3.6, 12, 25),                # tail
        ellipse(52, 56, 28, 15),                             # body
        poly((26, 52), (42, 50), (34, 26), (22, 30)),        # neck
        rotated_ellipse(22, 28, 14, 8, -50),                 # head
        poly((28, 14), (32, 6), (38, 16)),                   # ear
        rotated_ellipse(36, 34, 3, 11, 20),                  # mane
        circle(20, 24, 3.2),                                 # eye
        rotated_ellipse(42, 56, 3, 12, 10),                  # stripes
        rotated_ellipse(52, 56, 3, 13, 5),
        rotated_ellipse(62, 56, 3, 12, 0),
        rotated_ellipse(72, 56, 3, 10, -5),
        SUN,
    ]


def hippo():
    return [
        BG,
        GROUND,
        circle(22, 20, 7),                                   # ears
        circle(78, 20, 7),
        circle(32, 25, 9),                                   # eye bumps
        circle(68, 25, 9),
        ellipse(50, 50, 38, 28),                             # head
        ellipse(50, 66, 30, 17),                             # snout
        circle(40, 60, 3.6),                                 # nostrils
        circle(60, 60, 3.6),
        circle(32, 32, 3.6),                                 # eyes
        circle(68, 32, 3.6),
        rect(40, 74, 7, 7),                                  # teeth
        rect(53, 74, 7, 7),
        circle(88, 90, 5),
        circle(10, 90, 5),
    ]


PICTURES = {
    "lion": lion,
    "elephant": elephant,
    "giraffe": giraffe,
    "monkey": monkey,
    "zebra": zebra,
    "hippo": hippo,
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
