"""Part #1-1 (CSL-CAP-201-1): Mixer Bayonet Retaining Outer Cap (螺旋混合頭 — 外旋卡口壓蓋).

Dimensions:
- Outer envelope: Ø22.00 mm body (23.96 mm Poka-Yoke lug span) x 14.87 mm total height
- Conical upper clamping shoulder: Z = 11.87 .. 14.87 mm (Ø22.00 -> Ø6.20 mm flat collar)
- Top exit guide bore: Ø4.08 mm (clears Ø4.00 mm bell-mouth cannula)
- Stepped internal bore (monotonically open toward -Z for 2-plate injection molding):
  Z = 0.00 .. 6.82 mm : Ø19.70 mm (retains manifold lower lip Ø19.60 mm)
  Z = 6.82 .. 8.04 mm : Ø18.70 mm (mates with manifold flange Ø18.60 mm)
  Z = 8.04 .. 9.55 mm : Ø12.40 mm (houses manifold upper boss Ø12.20 mm & bell rim Ø11.40 mm)
  Z = 9.55 .. 11.55 mm: Conical clamping seat Ø11.50 -> Ø4.08 mm (clamps bell cannula without glue)
"""
from __future__ import annotations

import math
from cadgen import build123d as bd
from cadgen import glb, srgb, step, stl
from lib import cap_features as CF
from lib import specs as S


def build_mixer_part1_outer_cap() -> bd.Shape:
    shoulder_z0 = 11.87
    cyl = bd.Cylinder(
        radius=S.CAP_BODY_OD / 2.0,
        height=shoulder_z0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    cone_top = bd.Pos(0, 0, shoulder_z0) * bd.Cone(
        bottom_radius=S.CAP_BODY_OD / 2.0,
        top_radius=3.10,
        height=S.MIXER_BODY_LEN - shoulder_z0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    outer = CF.add_poka_yoke_bayonet_lugs(cyl + cone_top, z0=0.0)

    # 16 vertical grip flutes placed at half-angles so X/Y cardinal span stays exact Ø22.00 mm
    flutes = []
    for i in range(16):
        ang = math.radians((i + 0.5) * 22.5)
        fx = (S.CAP_BODY_OD / 2.0 + 0.15) * math.cos(ang)
        fy = (S.CAP_BODY_OD / 2.0 + 0.15) * math.sin(ang)
        flutes.append(
            bd.Pos(fx, fy, 2.30)
            * bd.Cylinder(
                radius=0.45,
                height=9.00,
                align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
            )
        )
    outer = outer - bd.Compound(children=flutes)

    # Monotonic stepped internal cavities
    cav_1 = bd.Pos(0, 0, -0.20) * bd.Cylinder(
        radius=19.70 / 2.0,
        height=6.82 + 0.20,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    cav_2 = bd.Pos(0, 0, 6.80) * bd.Cylinder(
        radius=18.70 / 2.0,
        height=8.04 - 6.80,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    cav_3 = bd.Pos(0, 0, 8.02) * bd.Cylinder(
        radius=12.40 / 2.0,
        height=9.55 - 8.02,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    cav_cone = bd.Pos(0, 0, 9.55) * bd.Cone(
        bottom_radius=11.50 / 2.0,
        top_radius=4.08 / 2.0,
        height=11.55 - 9.55,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    cav_bore = bd.Pos(0, 0, 11.50) * bd.Cylinder(
        radius=4.08 / 2.0,
        height=S.MIXER_BODY_LEN - 11.50 + 0.40,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )

    outer = outer - cav_1 - cav_2 - cav_3 - cav_cone - cav_bore
    outer.label = "mixer_part1_outer_cap"
    outer.color = srgb(S.HEX_MIXER_OLIVE)
    return outer


@step(out="../STEP/mixer_part1_outer_cap.step")
@stl(out="../STL/mixer_part1_outer_cap.stl")
@glb(out="../GLB/mixer_part1_outer_cap.glb")
def mixer_part1_outer_cap():
    return build_mixer_part1_outer_cap()


if __name__ == "__main__":
    mixer_part1_outer_cap()
