# Figures

Geometric diagrams for the course are **generated from code**, not committed as
hand-drawn binaries. Each script in this folder is self-contained (matplotlib +
numpy) and writes a PNG into [`../assets/generated/`](../assets/generated). Both
the scripts and their outputs are committed, so the figures render on GitHub and
stay reproducible.

Pipeline / flow diagrams elsewhere in the course use inline
[Mermaid](https://mermaid.js.org/) blocks instead (GitHub renders them natively),
so only the *geometric* figures live here.

## Regenerate everything

One command, from the repository root:

```bash
for f in figures/*.py; do [ "$(basename "$f")" = _style.py ] || python3 "$f"; done
```

(or just `cd figures && for f in *_*.py; do python3 "$f"; done`)

## Requirements

```bash
pip install matplotlib numpy
```

## Scripts

| Script | Output | Used in |
| --- | --- | --- |
| `pinhole_model.py` | `pinhole_model.png` | `notes/00_image_formation.md` |
| `epipolar_geometry.py` | `epipolar_geometry.png` | `notes/03_two_view_geometry.md` |
| `triangulation.py` | `triangulation.png` | `notes/04_triangulation.md` |
| `pnp_p3p.py` | `pnp_p3p.png` | `notes/05_pnp_tracking.md` |

`_style.py` holds the shared palette, output path, and `save()` helper — it is
imported by the others and is not run directly.
