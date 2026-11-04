"""Part #1-3 (CSL-CAP-201-3): One-Piece Bell-Mouth Mixing Cannula / Shroud (一體式喇叭口透明混合外管).

Standalone part coordinates: Z = 0.00 .. 32.56 mm (placed at Z_cap = 9.04 mm in `helical_mixer_cap`).
True single-piece molded housing matching vendor CAD (`混合頭.png`) & Sulzer Mixpac DFM:
- Total length: 32.56 mm (nominal 32.60 mm; reaches Z_cap = 41.60 mm exact when seated at Z_cap = 9.04 mm)
- Bottom flared bell base (Z = 0.00 .. 2.46 mm):
  Flat sealing rim Ø10.20 x 0.46 mm + Conical outer clamping wall Ø10.20 -> Ø4.00 mm (Z = 0.46 .. 2.46 mm)
  Clamped directly between Part #1-1 outer cap and Part #1-2 seal seat without glue/solvent!
- Inner conical convergence funnel (Z = 0.00 .. 1.86 mm):
  Tapers smoothly from Ø7.64 mm inlet to Ø3.00 mm bore (acts as positive anti-ejection stop for Part #1-4!)
- Straight mixing tube (Z = 2.46 .. 32.56 mm):
  Ø4.00 mm OD x Ø3.00 mm ID; protrudes 26.73 mm past the 14.87 mm outer cap.
"""
from __future__ import annotations

from cadgen import build123d as bd
from cadgen import glb, srgb, step, stl
from lib import specs as S


def build_mixer_part3_bell_cannula() -> bd.Shape:
    z_rim_top = 0.46
    z_cone_top = 2.46
    z_tip = S.MIXER_P3_LEN  # 32.56 mm exact (9.04 + 32.56 = 41.60 mm)

    # Outer solid: bottom rim + conical bell + straight Ø4.00 mm tube
    outer_rim = bd.Cylinder(
        radius=S.MIXER_P3_BELL_OD / 2.0,
        height=z_rim_top,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    outer_bell = bd.Pos(0, 0, z_rim_top) * bd.Cone(
        bottom_radius=S.MIXER_P3_BELL_OD / 2.0,
        top_radius=S.MIXER_TUBE_OD / 2.0,
        height=z_cone_top - z_rim_top,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    outer_tube = bd.Pos(0, 0, z_cone_top) * bd.Cylinder(
        radius=S.MIXER_TUBE_OD / 2.0,
        height=z_tip - z_cone_top,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    outer = outer_rim + outer_bell + outer_tube

    # Inner core pin (monotonically decreasing radius along +Z for 1-piece core extraction):
    z_throat = 1.86
    inner_funnel = bd.Pos(0, 0, -0.05) * bd.Cone(
        bottom_radius=S.MIXER_P3_BELL_ID / 2.0,
        top_radius=S.MIXER_TUBE_ID / 2.0,
        height=z_throat + 0.05,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    inner_bore = bd.Pos(0, 0, z_throat - 0.05) * bd.Cylinder(
        radius=S.MIXER_TUBE_ID / 2.0,
        height=z_tip - z_throat + 0.25,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )

    shroud = outer - inner_funnel - inner_bore
    shroud.label = "mixer_part3_bell_cannula"
    shroud.color = srgb("#D8E8F8", 0.36)
    return shroud


@step(out="../STEP/mixer_part3_bell_cannula.step")
@stl(out="../STL/mixer_part3_bell_cannula.stl")
@glb(out="../GLB/mixer_part3_bell_cannula.glb")
def mixer_part3_bell_cannula():
    return build_mixer_part3_bell_cannula()


if __name__ == "__main__":
    mixer_part3_bell_cannula()
