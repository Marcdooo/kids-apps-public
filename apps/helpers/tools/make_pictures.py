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


def person(coat, hat, extras=(), under=()):
    """A friendly front-facing worker: shoulders, face, then the job's own parts."""
    return ([
        BG,
        GROUND,
        poly((12, 100), (20, 72), (80, 72), (88, 100)),      # shoulders
    ] + list(under) + list(coat) + [
        rect(43, 60, 14, 14),                                # neck
        circle(30, 46, 5.6),                                 # ears
        circle(70, 46, 5.6),
        ellipse(50, 46, 20, 22),                             # face
        circle(42.5, 46, 3.2),                               # eyes
        circle(57.5, 46, 3.2),
        ellipse(50, 56, 6, 3),                               # smile
    ] + list(hat) + list(extras))


def firefighter():
    return person(
        coat=[rect(18, 88, 64, 6), rect(30, 74, 8, 26), rect(62, 74, 8, 26)],
        hat=[half_ellipse(50, 36, 27, 24), rect(20, 34, 60, 7),
             star(50, 20, 7, 3.2)],
        extras=[circle(10, 14, 4.4), circle(90, 20, 4.4)])


def doctor():
    return person(
        coat=[poly((38, 72), (62, 72), (50, 92)), circle(68, 88, 6.4)],
        hat=[half_ellipse(50, 34, 22, 14), rect(46, 18, 8, 14), rect(41, 22, 18, 6),
             circle(34, 34, 6)],
        extras=[circle(10, 16, 4.4), circle(90, 24, 4.4)])


def police():
    return person(
        coat=[rect(47, 74, 6, 24), star(68, 86, 8, 3.6)],
        hat=[half_ellipse(50, 34, 24, 17), rect(22, 32, 56, 6), star(50, 24, 7, 3.2)],
        extras=[circle(10, 16, 4.4), circle(90, 24, 4.4)])


def chef():
    return person(
        coat=[poly((38, 72), (62, 72), (50, 88)), circle(50, 90, 3.8), circle(50, 78, 3.8)],
        hat=[circle(34, 18, 10), circle(66, 18, 10), circle(50, 12, 12), rect(33, 22, 34, 14)],
        extras=[circle(10, 50, 4.4), circle(90, 50, 4.4)])


def builder():
    return person(
        coat=[rect(26, 78, 48, 5), rect(26, 90, 48, 5)],
        hat=[half_ellipse(50, 33, 25, 20), rect(20, 31, 60, 7), rect(45, 8, 10, 14)],
        extras=[rect(86, 62, 5, 32), rect(78, 56, 20, 9)])


def farmer():
    return person(
        coat=[rect(34, 78, 32, 22), rect(36, 68, 6, 14), rect(58, 68, 6, 14), circle(40, 84, 3.4), circle(60, 84, 3.4)],
        hat=[ellipse(50, 30, 38, 7), half_ellipse(50, 30, 21, 18), rect(30, 24, 40, 6)],
        extras=[rect(8, 52, 5, 44), poly((6, 52), (10.5, 36), (15, 52)), circle(88, 90, 4.4)])


PICTURES = {
    "firefighter": firefighter,
    "doctor": doctor,
    "police": police,
    "chef": chef,
    "builder": builder,
    "farmer": farmer,
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
