"""Pinhole camera model: perspective projection by similar triangles.

Side view. The optical axis is the horizontal (depth Z) axis; the vertical
axis is height Y. A 3D point P projects through the optical center O onto the
(virtual, in-front) image plane at distance f. The two shaded triangles are
similar, giving y = f * Y / Z.
"""
import numpy as np
from _style import plt, CAM, POINT, RAY, PLANE, ACCENT, save

f = 2.0          # focal length (O -> image plane)
Z, Y = 6.0, 3.0  # 3D point depth and height
yp = f * Y / Z   # projected image height

fig, ax = plt.subplots(figsize=(7.2, 4.2))

# Optical axis
ax.axhline(0, color=PLANE, lw=1.0, ls=(0, (6, 4)), zorder=1)
ax.annotate("optical axis (Z)", (6.3, 0.05), color=PLANE, fontsize=9)

# Image plane (virtual, in front of the camera)
ax.plot([f, f], [-2.2, 2.2], color=PLANE, lw=2.0)
ax.annotate("image plane", (f, 2.35), color=PLANE, ha="center", fontsize=9)

# Optical center
ax.plot(0, 0, "o", color=CAM, ms=9, zorder=5)
ax.annotate("O\n(optical center)", (-0.15, -0.15), color=CAM, ha="right",
            va="top", fontsize=10)

# 3D world point and ray O -> P
ax.plot(Z, Y, "o", color=POINT, ms=9, zorder=5)
ax.annotate("P = (X, Y, Z)", (Z, Y + 0.18), color=POINT, ha="center")
ax.plot([0, Z], [0, Y], color=RAY, lw=1.6, zorder=3)

# Projected point on the image plane
ax.plot(f, yp, "o", color=ACCENT, ms=8, zorder=6)
ax.annotate("p", (f + 0.12, yp + 0.05), color=ACCENT, fontsize=11)

# Similar-triangle annotations
ax.plot([f, f], [0, yp], color=ACCENT, lw=1.2)
ax.plot([Z, Z], [0, Y], color=POINT, lw=1.0, ls=":")
ax.annotate("f", (f / 2, -0.18), color=ACCENT, ha="center", va="top")
ax.annotate("Z", (Z / 2, -0.18), color=POINT, ha="center", va="top")
ax.annotate("y", (f + 0.1, yp / 2), color=ACCENT, va="center")
ax.annotate("Y", (Z + 0.12, Y / 2), color=POINT, va="center")

ax.text(2.6, -1.7, r"$y = f\,\dfrac{Y}{Z}$", fontsize=15,
        bbox=dict(boxstyle="round", fc="white", ec=ACCENT))

ax.set_xlim(-1.2, 7.6)
ax.set_ylim(-2.6, 2.9)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("Pinhole camera model — perspective projection", fontsize=12)
save(fig, "pinhole_model.png")
