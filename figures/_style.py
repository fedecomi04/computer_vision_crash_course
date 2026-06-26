"""Shared style + paths for all figure scripts.

Import this from each figure script so every diagram looks consistent and
writes into assets/generated/. Uses the non-interactive Agg backend so the
scripts run headless (no display required).
"""
import os
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

# assets/generated/ relative to the repo root (parent of figures/)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(os.path.join(HERE, "..", "assets", "generated"))
os.makedirs(OUT_DIR, exist_ok=True)

# A muted, consistent palette.
CAM = "#1f77b4"      # cameras / centers
POINT = "#d62728"    # 3D world points
RAY = "#2ca02c"      # rays / projections
PLANE = "#7f7f7f"    # image planes / axes
ACCENT = "#ff7f0e"   # highlighted quantities

plt.rcParams.update({
    "font.size": 11,
    "font.family": "DejaVu Sans",
    "axes.linewidth": 1.0,
    "figure.dpi": 130,
})


def save(fig, name):
    """Save a figure into assets/generated/ and report the path."""
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, bbox_inches="tight", dpi=130)
    plt.close(fig)
    print("wrote", path)
