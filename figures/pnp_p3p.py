"""P3P geometry: recover camera pose from 3 known 3D points.

The camera center C sees three known world points P1, P2, P3 along rays with
known inter-ray angles (from the calibrated image directions). The unknown
depths d1, d2, d3 satisfy a law-of-cosines system on each side of the
tetrahedron C-Pi-Pj:  |Pi Pj|^2 = di^2 + dj^2 - 2 di dj cos(theta_ij),
which reduces to a quartic (up to 4 solutions, disambiguated by a 4th point).
"""
import numpy as np
from _style import plt, CAM, POINT, RAY, ACCENT, save

C = np.array([0.0, 0.0])
P1 = np.array([3.2, 3.0])
P2 = np.array([4.6, 1.1])
P3 = np.array([4.2, -1.4])
pts = [P1, P2, P3]

fig, ax = plt.subplots(figsize=(7.2, 4.8))

# Camera center
ax.plot(*C, "o", color=CAM, ms=11, zorder=6)
ax.annotate("C  (camera center)", (C[0] - 0.15, C[1] - 0.15), color=CAM,
            ha="right", va="top")

# Rays C -> Pi with depth labels
for P, name, dname in [(P1, "P1", "d1"), (P2, "P2", "d2"), (P3, "P3", "d3")]:
    ax.plot([C[0], P[0]], [C[1], P[1]], color=RAY, lw=1.6, zorder=3)
    ax.plot(*P, "o", color=POINT, ms=10, zorder=5)
    ax.annotate(name, (P[0] + 0.15, P[1] + 0.05), color=POINT)
    mid = C + (P - C) * 0.5
    ax.annotate(dname, (mid[0], mid[1] + 0.12), color=RAY, fontsize=10)

# Known distances between the world points (the rigid triangle)
for A, B in [(P1, P2), (P2, P3), (P1, P3)]:
    ax.plot([A[0], B[0]], [A[1], B[1]], color=POINT, lw=1.0, ls=":")
m12 = (P1 + P2) / 2
ax.annotate(r"$\|P_1 P_2\|$", (m12[0] + 0.15, m12[1] + 0.15), color=POINT,
            fontsize=9)

# Angle marker between two rays at C
ang1 = np.degrees(np.arctan2(P1[1], P1[0]))
ang2 = np.degrees(np.arctan2(P2[1], P2[0]))
from matplotlib.patches import Arc
ax.add_patch(Arc(C, 1.6, 1.6, angle=0, theta1=ang2, theta2=ang1,
                 color=ACCENT, lw=1.6))
ax.annotate(r"$\theta_{12}$", (0.95, 1.05), color=ACCENT, fontsize=11)

ax.text(-0.2, -1.7,
        r"$\|P_i P_j\|^2 = d_i^2 + d_j^2 - 2\,d_i d_j \cos\theta_{ij}$",
        fontsize=13, bbox=dict(boxstyle="round", fc="white", ec=ACCENT))

ax.set_xlim(-1.4, 5.6)
ax.set_ylim(-2.4, 3.6)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("P3P — pose from three known 3D-2D correspondences", fontsize=12)
save(fig, "pnp_p3p.png")
