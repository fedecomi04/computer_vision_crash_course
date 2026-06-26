"""Epipolar geometry: the epipolar plane, lines, and epipoles for two views.

A 3D point X is seen by two cameras with centers C and C'. The plane through
C, C', X is the epipolar plane; it meets each image plane in an epipolar line.
The baseline C-C' meets each image plane at the epipole (e, e'). The match of x
in the second view is constrained to lie on the epipolar line l' (this is the
x'^T F x = 0 constraint).
"""
import numpy as np
from _style import plt, CAM, POINT, RAY, PLANE, ACCENT, save

C = np.array([0.0, 0.0])
Cp = np.array([6.0, 0.0])
X = np.array([3.0, 4.2])

fig, ax = plt.subplots(figsize=(7.6, 4.6))

# Baseline
ax.plot([C[0], Cp[0]], [C[1], Cp[1]], color=PLANE, lw=1.4, ls=(0, (6, 4)))
ax.annotate("baseline", ((C[0] + Cp[0]) / 2, -0.28), color=PLANE,
            ha="center", fontsize=9)

# Camera centers
for c, name, ha in [(C, "C", "right"), (Cp, "C'", "left")]:
    ax.plot(*c, "o", color=CAM, ms=10, zorder=5)
    ax.annotate(name, (c[0] + (-0.18 if ha == "right" else 0.18), c[1] - 0.05),
                color=CAM, ha=ha, va="top", fontsize=12)

# Image planes (short segments in front of each camera, facing X)
def image_plane(c, ax):
    d = X - c
    d = d / np.linalg.norm(d)
    n = np.array([-d[1], d[0]])          # in-plane direction
    mid = c + d * 1.5                     # plane sits 1.5 in front
    p0, p1 = mid - n * 1.1, mid + n * 1.1
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=PLANE, lw=2.2)
    return mid, d

mid, _ = image_plane(C, ax)
midp, _ = image_plane(Cp, ax)

# 3D point and the two viewing rays
ax.plot(*X, "o", color=POINT, ms=10, zorder=6)
ax.annotate("X", (X[0], X[1] + 0.2), color=POINT, ha="center", fontsize=12)
for c in (C, Cp):
    ax.plot([c[0], X[0]], [c[1], X[1]], color=RAY, lw=1.6, zorder=3)

# Projected points x, x' where each ray crosses its image plane
def project(c):
    d = X - c
    return c + d / np.linalg.norm(d) * 1.5

x, xp = project(C), project(Cp)
ax.plot(*x, "o", color=ACCENT, ms=7, zorder=7)
ax.plot(*xp, "o", color=ACCENT, ms=7, zorder=7)
ax.annotate("x", (x[0] - 0.12, x[1]), color=ACCENT, ha="right", fontsize=11)
ax.annotate("x'", (xp[0] + 0.12, xp[1]), color=ACCENT, ha="left", fontsize=11)

# Epipoles: baseline direction meeting each image plane (schematic markers)
ax.annotate("e", (1.55, 0.02), color=CAM, fontsize=10)
ax.annotate("e'", (4.3, 0.02), color=CAM, fontsize=10)

# Shade the epipolar plane (triangle C, C', X)
tri = plt.Polygon([C, Cp, X], closed=True, fc=RAY, ec="none", alpha=0.08)
ax.add_patch(tri)
ax.annotate("epipolar plane", (3.0, 1.6), color=RAY, ha="center", fontsize=9)

ax.text(0.1, 4.3, r"$x'^{\top} F\, x = 0$", fontsize=15,
        bbox=dict(boxstyle="round", fc="white", ec=ACCENT))

ax.set_xlim(-1.2, 7.6)
ax.set_ylim(-1.0, 5.1)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("Epipolar geometry — two views of a 3D point", fontsize=12)
save(fig, "epipolar_geometry.png")
