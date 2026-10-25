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


def cake():
    return [
        BG,
        GROUND,
        ellipse(50, 90, 46, 6),                              # plate
        rect(14, 60, 72, 28),                                # bottom tier
        rect(24, 40, 52, 22),                                # middle tier
        rect(34, 24, 32, 17),                                # top tier
        rect(14, 60, 72, 7),                                 # icing
        rect(24, 40, 52, 6),
        rect(34, 24, 32, 5),
        circle(26, 77, 4.4),                                 # cherries
        circle(50, 77, 4.4),
        circle(74, 77, 4.4),
        rect(39, 12, 5, 12),                                 # candles
        rect(48, 12, 5, 12),
        rect(57, 12, 5, 12),
        ellipse(41.5, 8, 3.6, 5),                            # flames
        ellipse(50.5, 8, 3.6, 5),
        ellipse(59.5, 8, 3.6, 5),
        star(12, 30, 7, 3.2),
        star(88, 36, 7, 3.2),
    ]


def balloons():
    return [
        BG,
        GROUND,
        ellipse(24, 36, 16, 20),
        ellipse(76, 38, 16, 20),
        ellipse(36, 66, 14, 18),
        ellipse(64, 68, 14, 18),
        ellipse(50, 28, 17, 21),
        circle(10, 12, 4.4),                                 # confetti
        circle(90, 10, 4.4),
        star(12, 66, 7, 3.2),
        star(88, 68, 7, 3.2),
        circle(50, 92, 4.4),
        diamond(50, 62, 4.6),
    ]


def present():
    return [
        BG,
        GROUND,
        rect(12, 58, 76, 30),                                # big box
        rect(46, 58, 8, 30),                                 # ribbon
        rect(26, 32, 48, 26),                                # top box
        rect(22, 28, 56, 8),                                 # lid
        rect(46, 28, 8, 30),
        circle(40, 18, 8),                                   # bow
        circle(60, 18, 8),
        circle(50, 22, 5),
        circle(24, 72, 5),                                   # dots
        circle(76, 72, 5),
        circle(34, 44, 4),
        circle(66, 44, 4),
        star(10, 20, 7, 3.2),
        star(90, 20, 7, 3.2),
    ]


def partyhat():
    def hw(y):
        return (y - 8) / 78 * 26
    rows = []
    ys = [8, 28, 48, 68, 86]
    rows.append(poly((50, 8), (50 - hw(28), 28), (50 + hw(28), 28)))
    for a, b in zip(ys[1:-1], ys[2:]):
        rows.append(poly((50 - hw(a), a), (50 + hw(a), a), (50 + hw(b), b), (50 - hw(b), b)))
    return [
        BG,
        GROUND,
    ] + rows + [
        ellipse(50, 88, 28, 5),                              # rim
        circle(50, 9, 7),                                    # pompom
        circle(40, 56, 3.8),                                 # dots
        circle(60, 76, 3.8),
        star(14, 30, 8, 3.6),
        star(86, 40, 8, 3.6),
        circle(14, 72, 4.4),
        circle(88, 76, 4.4),
    ]


def sundae():
    return [
        BG,
        GROUND,
        poly((64, 22), (70, 18), (86, 4), (92, 10)),         # wafer
        poly((30, 54), (70, 54), (62, 86), (38, 86)),        # glass
        rect(46, 84, 8, 10),                                 # stem
        ellipse(50, 94, 16, 4),                              # foot
        circle(36, 44, 14),                                  # scoops
        circle(64, 44, 14),
        circle(50, 30, 15),
        ellipse(50, 53, 21, 4.4),                            # sauce
        circle(50, 13, 6),                                   # cherry
        circle(14, 30, 4.4),
        circle(88, 60, 4.4),
        star(14, 70, 7, 3.2),
    ]


def pinata():
    return [
        BG,
        GROUND,
        rotated_ellipse(88, 70, 3.4, 18, -35),               # stick
        star(50, 48, 44, 22, points=5),                      # pinata
        star(50, 48, 24, 11, points=5),
        circle(50, 48, 7),
        circle(12, 14, 4.4),
        circle(90, 14, 4.4),
        circle(10, 84, 4.4),
        star(86, 36, 6, 2.8),
    ]


PICTURES = {
    "cake": cake,
    "balloons": balloons,
    "present": present,
    "partyhat": partyhat,
    "sundae": sundae,
    "pinata": pinata,
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
