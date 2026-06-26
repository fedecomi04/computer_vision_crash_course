"""Triangulation: back-projected rays from two views meet at the 3D point.

With known camera poses, each 2D observation defines a back-projected ray.
Ideally the two rays intersect at the world point X. With measurement noise
they do NOT exactly meet (dashed) — linear DLT finds the least-squares point
and nonlinear refinement minimizes reprojection error. Small baseline / low
parallax makes the intersection ill-conditioned (poor depth).
"""
import numpy as np
from _style import plt, CAM, POINT, RAY, ACCENT, PLANE, save

C0 = np.array([0.0, 0.0])
C1 = np.array([5.0, 0.0])
X = np.array([2.5, 4.0])          # true 3D point

fig, ax = plt.subplots(figsize=(7.2, 4.6))

# Baseline
ax.plot([C0[0], C1[0]], [C0[1], C1[1]], color=PLANE, lw=1.2, ls=(0, (6, 4)))
ax.annotate("baseline  B", (2.5, -0.3), color=PLANE, ha="center", fontsize=9)

# Camera centers
for c, name in [(C0, "C0"), (C1, "C1")]:
    ax.plot(*c, "o", color=CAM, ms=10, zorder=5)
ax.annotate("C0", (C0[0] - 0.15, -0.1), color=CAM, ha="right", va="top")
ax.annotate("C1", (C1[0] + 0.15, -0.1), color=CAM, ha="left", va="top")

# Ideal rays through the true point
for c in (C0, C1):
    d = X - c
    end = c + d / np.linalg.norm(d) * (np.linalg.norm(d) + 0.7)
    ax.plot([c[0], end[0]], [c[1], end[1]], color=RAY, lw=1.6, zorder=3)

# Noisy rays (slightly perturbed angle) -> do not meet at X
def noisy_ray(c, ang_deg):
    d = X - c
    ang = np.deg2rad(ang_deg)
    R = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
    d = R @ (d / np.linalg.norm(d))
    return c, c + d * (np.linalg.norm(X - c) + 0.7)

for (c, e) in [noisy_ray(C0, 2.4), noisy_ray(C1, -2.6)]:
    ax.plot([c[0], e[0]], [c[1], e[1]], color=POINT, lw=1.1,
            ls=":", zorder=2)

# True point and an estimated point (midpoint of closest approach, schematic)
ax.plot(*X, "o", color=POINT, ms=10, zorder=6)
ax.annotate("X  (true)", (X[0] + 0.15, X[1] + 0.1), color=POINT)
Xhat = X + np.array([0.28, -0.32])
ax.plot(*Xhat, "x", color=ACCENT, ms=11, mew=2.5, zorder=7)
ax.annotate(r"$\hat{X}$  (estimate)", (Xhat[0] + 0.15, Xhat[1] - 0.15),
            color=ACCENT)

ax.text(0.1, 3.9, r"$x \times (P X) = 0 \;\Rightarrow\; A X = 0$",
        fontsize=13, bbox=dict(boxstyle="round", fc="white", ec=ACCENT))

ax.set_xlim(-1.0, 6.6)
ax.set_ylim(-0.9, 5.0)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("Triangulation — intersecting back-projected rays", fontsize=12)
save(fig, "triangulation.png")
