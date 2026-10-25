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


def dome_piece(cx, cy, rx, ry, x0, x1, steps=40):
    """A vertical slice of the top half of an ellipse."""
    pts = [(x0, cy)]
    for i in range(steps + 1):
        x = x0 + (x1 - x0) * i / steps
        t = (x - cx) / rx
        y = cy - ry * math.sqrt(max(0.0, 1 - t * t))
        pts.append((round(x, 2), round(y, 2)))
    pts.append((x1, cy))
    return poly(*pts)


def arc_band(cx, cy, ro, ri, steps=30):
    pts = []
    for i in range(steps + 1):
        a = math.pi * i / steps
        pts.append((round(cx - ro * math.cos(a), 2), round(cy - ro * math.sin(a), 2)))
    for i in range(steps, -1, -1):
        a = math.pi * i / steps
        pts.append((round(cx - ri * math.cos(a), 2), round(cy - ri * math.sin(a), 2)))
    return poly(*pts)


def sun():
    rays = []
    for k in range(12):
        a = math.radians(k * 30)
        b0, b1 = a - math.radians(10), a + math.radians(10)
        rays.append(poly((round(50 + 24 * math.cos(b0), 2), round(50 + 24 * math.sin(b0), 2)),
                         (round(50 + 45 * math.cos(a), 2), round(50 + 45 * math.sin(a), 2)),
                         (round(50 + 24 * math.cos(b1), 2), round(50 + 24 * math.sin(b1), 2))))
    return [BG] + rays + [
        circle(50, 50, 22),                                  # sun face
        circle(42, 45, 3.4),                                 # eyes
        circle(58, 45, 3.4),
        ellipse(50, 58, 8, 4),                               # smile
    ]


def raincloud():
    return [
        BG,
        GROUND,
        ellipse(50, 36, 36, 15),                             # cloud
        circle(32, 28, 15),
        circle(52, 22, 19),
        circle(72, 30, 14),
        poly((54, 46), (42, 66), (51, 66), (44, 80), (64, 56), (54, 56), (62, 46)),   # lightning
        ellipse(22, 60, 4.4, 7.4),                           # raindrops
        ellipse(78, 60, 4.4, 7.4),
        ellipse(32, 72, 4.4, 7.4),
        ellipse(68, 72, 4.4, 7.4),
        ellipse(10, 72, 4.4, 7.4),
        ellipse(90, 72, 4.4, 7.4),
    ]


def snowflake():
    return [
        BG,
        GROUND,
        rotated_ellipse(50, 46, 36, 3.6, 0),                 # arms
        rotated_ellipse(50, 46, 36, 3.6, 60),
        rotated_ellipse(50, 46, 36, 3.6, 120),
        circle(86, 46, 5.4),                                 # tips
        circle(14, 46, 5.4),
        circle(68, 15, 5.4),
        circle(32, 77, 5.4),
        circle(32, 15, 5.4),
        circle(68, 77, 5.4),
        poly((50, 36), (59, 41), (59, 51), (50, 56), (41, 51), (41, 41)),   # center
        star(14, 16, 8, 3.6, points=6),                      # small flakes
        star(88, 80, 8, 3.6, points=6),
        star(10, 84, 7, 3.2, points=6),
        star(90, 16, 7, 3.2, points=6),
    ]


def autumntree():
    return [
        BG,
        GROUND,
        poly((43, 90), (57, 90), (54, 48), (46, 48)),        # trunk
        circle(30, 46, 15),                                  # leaves
        circle(70, 46, 15),
        circle(50, 30, 22),
        circle(36, 28, 11),
        circle(64, 28, 11),
        rotated_ellipse(12, 62, 6.4, 3.6, 30),               # falling leaves
        rotated_ellipse(88, 66, 6.4, 3.6, -30),
        rotated_ellipse(20, 82, 6.4, 3.6, 10),
        rotated_ellipse(66, 90, 6.4, 3.6, -10),
        ellipse(86, 88, 9, 6.4),                             # pumpkin
        SUN,
    ]


def rainbow():
    return [
        BG,
        GROUND,
        arc_band(50, 84, 48, 41),
        arc_band(50, 84, 41, 34),
        arc_band(50, 84, 34, 27),
        arc_band(50, 84, 27, 20),
        arc_band(50, 84, 20, 13),
        ellipse(14, 86, 13, 7),                              # clouds
        circle(22, 80, 7),
        ellipse(86, 86, 13, 7),
        circle(78, 80, 7),
        circle(14, 16, 6),                                   # sun
        circle(60, 14, 4.4),
        circle(86, 34, 4.4),
    ]


def umbrella():
    cx, cy, rx, ry = 50, 52, 42, 34
    return [
        BG,
        GROUND,
        rect(48, 52, 4, 38),                                 # handle
        half_ellipse(43, 90, 6, 6, top=False),               # hook
        dome_piece(cx, cy, rx, ry, 8, 29),                   # panels
        dome_piece(cx, cy, rx, ry, 29, 50),
        dome_piece(cx, cy, rx, ry, 50, 71),
        dome_piece(cx, cy, rx, ry, 71, 92),
        ellipse(14, 72, 3.8, 6.4),                           # raindrops
        ellipse(86, 70, 3.8, 6.4),
        ellipse(26, 88, 3.8, 6.4),
        ellipse(76, 88, 3.8, 6.4),
        ellipse(12, 22, 12, 5.4),                            # cloud
        ellipse(86, 16, 12, 5.4),
    ]


PICTURES = {
    "sun": sun,
    "raincloud": raincloud,
    "snowflake": snowflake,
    "autumntree": autumntree,
    "rainbow": rainbow,
    "umbrella": umbrella,
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
