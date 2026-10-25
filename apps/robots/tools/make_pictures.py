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


def robot():
    return [
        BG,
        GROUND,
        rect(46, 4, 8, 12),                                  # antenna
        circle(50, 6, 4.4),
        rect(34, 82, 11, 14),                                # legs
        rect(55, 82, 11, 14),
        rect(30, 92, 19, 6),                                 # feet
        rect(51, 92, 19, 6),
        rect(11, 50, 13, 30),                                # arms
        rect(76, 50, 13, 30),
        circle(17.5, 82, 7),                                 # hands
        circle(82.5, 82, 7),
        rect(26, 48, 48, 36),                                # body
        rect(44, 40, 12, 9),                                 # neck
        rect(24, 22, 6, 14),                                 # ears
        rect(70, 22, 6, 14),
        rect(30, 14, 40, 28),                                # head
        circle(40, 26, 5),                                   # eyes
        circle(60, 26, 5),
        rect(40, 34, 20, 5),                                 # mouth
        rect(36, 54, 28, 14),                                # chest panel
        circle(44, 76, 3.8),                                 # buttons
        circle(56, 76, 3.8),
    ]


def cutebot():
    return [
        BG,
        GROUND,
        circle(50, 7, 5.4),                                  # antenna ball
        ellipse(40, 92, 9, 6),                               # feet
        ellipse(60, 92, 9, 6),
        rotated_ellipse(24, 70, 5.4, 13, 20),                # arms
        rotated_ellipse(76, 70, 5.4, 13, -20),
        ellipse(50, 74, 23, 20),                             # body
        circle(50, 74, 9.6),                                 # belly dial
        ellipse(50, 34, 29, 23),                             # head
        ellipse(50, 34, 22, 15),                             # visor
        circle(41, 34, 4.4),                                 # eyes
        circle(59, 34, 4.4),
        circle(10, 20, 4.4),
        circle(90, 24, 4.4),
        SUN,
    ]


def gears():
    return [
        BG,
        GROUND,
        star(34, 34, 27, 21, points=8),                      # big gear
        circle(34, 34, 9),
        star(72, 58, 22, 17, points=8, rot=-67),             # medium gear
        circle(72, 58, 7.4),
        star(34, 78, 16, 12.4, points=8, rot=-80),           # small gear
        circle(34, 78, 5.4),
        circle(88, 18, 5),
    ]


def rover():
    return [
        BG,
        GROUND,
        poly((0, 82), (22, 56), (46, 82)),                   # mountains
        poly((58, 82), (80, 58), (100, 82)),
        poly((10, 44), (36, 30), (46, 38), (20, 52)),        # solar panel
        rect(24, 50, 48, 18),                                # body
        rect(60, 30, 5, 22),                                 # mast
        rect(54, 20, 18, 11),                                # camera head
        circle(63, 25, 3.4),                                 # lens
        rotated_ellipse(80, 54, 11, 3, -35),                 # arm
        circle(89, 46, 4.4),
        circle(32, 76, 10),                                  # wheels
        circle(52, 78, 8),
        circle(72, 76, 10),
        circle(32, 76, 4),
        circle(72, 76, 4),
        circle(86, 14, 6),
    ]


def drone():
    return [
        BG,
        GROUND,
        poly((38, 58), (34, 74), (40, 74), (44, 60)),        # legs
        poly((62, 58), (66, 74), (60, 74), (56, 60)),
        rect(20, 48, 60, 5),                                 # arms
        circle(20, 50, 6.4),                                 # motors
        circle(80, 50, 6.4),
        ellipse(20, 42, 14, 3.4),                            # propellers
        ellipse(80, 42, 14, 3.4),
        ellipse(50, 52, 17, 10),                             # body
        circle(50, 62, 6.4),                                 # camera
        circle(50, 49, 3.4),                                 # light
        ellipse(18, 16, 14, 6),                              # clouds
        ellipse(80, 22, 12, 5.4),
        ellipse(50, 90, 18, 4.4),                            # landing pad
    ]


def arm():
    return [
        BG,
        GROUND,
        rect(0, 90, 100, 6),                                 # conveyor
        rect(6, 74, 16, 16),                                 # box
        rect(16, 86, 46, 10),                                # base
        poly((40, 84), (50, 82), (62, 42), (52, 38)),        # lower arm
        circle(44, 84, 9),                                   # joint
        poly((54, 34), (62, 44), (82, 28), (76, 20)),        # upper arm
        circle(57, 39, 8),                                   # joint
        rect(80, 14, 7, 26),                                 # gripper palm
        rect(87, 14, 10, 6),                                 # fingers
        rect(87, 34, 10, 6),
        circle(88, 60, 4.4),
        circle(88, 78, 4.4),
        SUN,
    ]


PICTURES = {
    "robot": robot,
    "cutebot": cutebot,
    "gears": gears,
    "rover": rover,
    "drone": drone,
    "arm": arm,
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
