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


def star(cx, cy, R, r=None, points=5):
    """A star polygon (R = outer radius, r = inner radius)."""
    r = r or R * 0.45
    pts = []
    for i in range(points * 2):
        ang = -math.pi / 2 + i * math.pi / points
        rad = R if i % 2 == 0 else r
        pts.append((round(cx + rad * math.cos(ang), 2), round(cy + rad * math.sin(ang), 2)))
    return poly(*pts)


def crescent(c1, r1, c2, r2, steps=240):
    """Circle 1 with circle 2 cut out of it (sampled, so it is always a clean shape)."""
    def ring(c, r):
        return [(c[0] + r * math.cos(2 * math.pi * i / steps),
                 c[1] + r * math.sin(2 * math.pi * i / steps)) for i in range(steps)]

    def d(p, c):
        return math.hypot(p[0] - c[0], p[1] - c[1])
    outer = ring(c1, r1)
    keep = [d(p, c2) >= r2 for p in outer]
    start = next(i for i in range(steps) if keep[i] and not keep[i - 1])
    outer = [outer[(start + i) % steps] for i in range(steps) if keep[(start + i) % steps]]
    inner = ring(c2, r2)
    ikeep = [d(p, c1) <= r1 for p in inner]
    istart = next(i for i in range(steps) if ikeep[i] and not ikeep[i - 1])
    inner = [inner[(istart + i) % steps] for i in range(steps) if ikeep[(istart + i) % steps]]
    # the inner arc must continue from the end of the outer arc
    end = outer[-1]
    if d(inner[0], end) > d(inner[-1], end):
        inner.reverse()
    pts = outer + inner
    return poly(*[(round(x, 2), round(y, 2)) for x, y in pts])


def arc_band(cx, cy, rxo, ryo, rxi, ryi, a0, a1, rot, steps=24):
    """A slice of an elliptical ring (angles in degrees, then rotated by rot)."""
    r = math.radians(rot)

    def pt(rx, ry, t):
        x, y = rx * math.cos(t), ry * math.sin(t)
        return (round(cx + x * math.cos(r) - y * math.sin(r), 2),
                round(cy + x * math.sin(r) + y * math.cos(r), 2))
    ts = [math.radians(a0 + (a1 - a0) * i / steps) for i in range(steps + 1)]
    return poly(*([pt(rxo, ryo, t) for t in ts] + [pt(rxi, ryi, t) for t in ts[::-1]]))


def hill(cx, half_w, h):
    """A rounded hill sitting on the bottom edge, clipped to the picture."""
    pts = []
    for i in range(41):
        x = cx - half_w + 2 * half_w * i / 40
        if 0 <= x <= 100:
            y = 100 - h * math.sqrt(max(0.0, 1 - ((x - cx) / half_w) ** 2))
            pts.append((round(x, 2), round(y, 2)))
    if pts[0][0] > 0:
        pts.insert(0, (0, 100))
    pts.append((pts[-1][0], 100))
    pts.insert(0, (pts[0][0], 100))
    return poly(*pts)


def diamond(cx, cy, r):
    return poly((cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy))


BG = rect(0, 0, 100, 100)


def rocket():
    return [
        BG,
        diamond(14, 16, 4.5),                      # stars
        diamond(86, 22, 4.5),
        diamond(10, 60, 4.5),
        diamond(90, 56, 4.5),
        poly((38, 84), (62, 84), (50, 100)),       # flame
        poly((33, 62), (16, 84), (34, 82)),        # fins
        poly((67, 62), (84, 84), (66, 82)),
        ellipse(50, 52, 17, 38),                   # body
        poly((36, 66), (64, 66), (64, 72), (36, 72)),   # band
        circle(50, 40, 10.5),                      # window ring
        circle(50, 40, 7),                         # window
        poly((44, 89), (56, 89), (50, 99)),        # inner flame
    ]


def planet():
    return [
        BG,
        circle(16, 16, 7),                         # moon
        diamond(84, 12, 4.5),                      # stars
        diamond(90, 84, 4.5),
        diamond(12, 90, 4.5),
        rotated_ellipse(50, 50, 44, 12, -20),      # ring (behind)
        circle(50, 50, 24),                        # planet
        circle(43, 38, 5),                         # craters
        circle(58, 40, 4.2),
        arc_band(50, 50, 44, 12, 34, 8, 20, 160, -20),   # ring (front)
    ]


def moon():
    return [
        BG,
        star(18, 20, 10),                          # stars
        star(84, 18, 12),
        star(88, 52, 8),
        star(12, 56, 8),
        star(70, 84, 9),
        crescent((46, 48), 32, (64, 40), 27),      # moon
        circle(33, 54, 5),                         # craters
        circle(38, 36, 3.8),
        hill(25, 45, 14),                          # hills
        hill(82, 40, 12),
    ]


def ufo():
    return [
        BG,
        diamond(14, 14, 4.5),                      # stars
        diamond(86, 12, 4.5),
        diamond(88, 46, 4.5),
        poly((38, 60), (62, 60), (84, 100), (16, 100)),   # beam
        rect(0, 92, 100, 8),                       # ground
        circle(50, 38, 15),                        # dome
        ellipse(50, 36, 7, 8),                     # alien head
        ellipse(50, 53, 38, 11),                   # saucer
        circle(26, 53, 4),                         # lights
        circle(40, 59, 4),
        circle(60, 59, 4),
        circle(74, 53, 4),
    ]


def astronaut():
    return [
        BG,
        diamond(12, 14, 4.5),                      # stars
        diamond(88, 12, 4.5),
        diamond(8, 56, 4.5),
        diamond(92, 56, 4.5),
        rect(22, 62, 56, 28),                      # backpack
        hill(50, 28, 18),                          # body
        circle(22, 42, 5),                         # ear pieces
        circle(78, 42, 5),
        circle(50, 42, 28),                        # helmet
        ellipse(50, 44, 20, 15),                   # visor
        ellipse(43, 38, 6, 4),                     # shine
        ellipse(50, 70, 20, 5),                    # collar
        rect(42, 80, 16, 10),                      # panel
    ]


def alien():
    return [
        BG,
        diamond(12, 14, 4.5),                      # stars
        diamond(88, 16, 4.5),
        diamond(8, 60, 4.5),
        diamond(92, 62, 4.5),
        rect(33, 10, 4, 16),                       # antennas
        rect(63, 10, 4, 16),
        circle(35, 9, 5),
        circle(65, 9, 5),
        ellipse(50, 54, 32, 34),                   # head
        ellipse(37, 50, 9, 12),                    # eyes
        ellipse(63, 50, 9, 12),
        circle(37, 52, 4),                         # pupils
        circle(63, 52, 4),
        ellipse(50, 74, 10, 5),                    # mouth
    ]


PICTURES = {
    "rocket": rocket,
    "planet": planet,
    "moon": moon,
    "ufo": ufo,
    "astronaut": astronaut,
    "alien": alien,
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
