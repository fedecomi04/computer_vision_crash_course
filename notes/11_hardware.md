# 11 — Hardware

Every algorithm on the Visual-Odometry/SLAM spine ultimately consumes pixels and timestamps from **physical sensors**. This module steps below the math to the hardware layer: how shutters, synchronization, sensor modalities, mounting, and **calibration** determine whether "where is the camera and what is it looking at" can even be answered accurately. The blunt rule: **calibration quality bounds the whole pipeline** — no estimator recovers what bad geometry/timing destroys.

## Electrical & Sensing

### Global vs Rolling Shutter

- **Global shutter:** all pixels exposed simultaneously → one image = one instant. Preserves the pinhole assumption: every pixel shares a single camera pose.
- **Rolling shutter:** rows exposed **sequentially** (top to bottom). During fast motion, each row is captured at a slightly different pose/time.
  - Distorts moving scenes (skew, wobble, "jello") and **breaks the instantaneous-projection assumption** that VO/SLAM triangulation and PnP rely on.
  - Mitigations: faster readout, rolling-shutter-aware models (per-row pose), or just prefer global shutter for high-dynamics robotics.

### Synchronization & Timestamping

- Multi-sensor estimation (e.g. VIO) assumes you know **when** each measurement happened, on a common clock.
- **Hardware triggering:** a shared signal fires cameras (and pulses the IMU) so exposures are co-timed, not merely software-stamped after USB/OS jitter.
- **Timestamping** at capture (mid-exposure) avoids latency bias; sub-millisecond errors map directly into pose error during motion.

### Sensor-Modality Trade-offs

| Modality | Range | Lighting robustness | Resolution | Cost | Best for |
|---|---|---|---|---|---|
| RGB camera | passive (depth via geometry) | needs ambient light | high | low | texture, semantics, indoor+outdoor |
| Depth — structured light | short (~0.3–5 m) | fails in sunlight | medium | low–med | indoor scanning |
| Depth — ToF | short–mid | better outdoors than SL | medium | med | indoor/robotics |
| Thermal | mid | works in darkness/smoke | low | high | night, search & rescue |
| LiDAR | long (10s–100s m) | excellent (active) | sparse/angular | high | outdoor/driving mapping |

- No single modality wins everywhere → **sensor fusion** (Module 08) trades cost vs robustness vs range.

## Mechanical

- **Rigid mounting:** sensors must be fixed relative to each other on a stiff frame.
  - **Extrinsics** (the SE(3) transform between sensors) are calibrated *once* and assumed constant. Flex, vibration, or thermal drift silently invalidates them.
  - A rig that bends under load injects errors no software filter can undo — rigidity is a prerequisite for trusting calibration.

## Calibration

```mermaid
flowchart LR
    CB[Checkerboard / target] --> INT[Intrinsic: K, distortion]
    INT --> EXT[Extrinsic: sensor-to-sensor SE3]
    EXT --> PIPE[VO / SLAM estimator]
    PIPE --> ACC[Trajectory accuracy bounded by calibration]
```

- **Intrinsic calibration:** recover the camera matrix $K$ and lens **distortion** coefficients.
  - $K = \begin{bmatrix} f_x & 0 & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{bmatrix}$; distortion (radial $k_1,k_2,\dots$, tangential) un-warps lines that bend at the edges.
  - Method: photograph a **checkerboard** at many poses; corners give known 3D↔2D correspondences to solve for $K$ and distortion.
- **Extrinsic calibration:** the rigid transforms between sensors.
  - **Camera-to-camera:** stereo baseline + relative rotation.
  - **Camera-to-IMU:** spatial transform *and* time offset — critical for VIO; tools like Kalibr estimate both.
  - **Camera-to-LiDAR:** align image features with the point cloud so semantics and geometry register.
- **Why it bounds everything:** errors in $K$, distortion, baseline, or sensor timing propagate straight into triangulation, depth, and pose. A SLAM system is at best as accurate as its calibration.

> **Key takeaway:** Shutter type, synchronization, modality choice, rigid mounting, and especially calibration form the physical foundation whose quality caps the accuracy of every estimator built on top.

[← 10 CNNs & Semantics](10_cnns_and_semantics.md) · [Index](../README.md) · [Next → 12 Evaluation](12_evaluation.md)
