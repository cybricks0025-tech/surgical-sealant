"""Part #1-2 (CSL-CAP-201-2): Dual-Channel Manifold Seal Seat (螺旋混合頭 — 雙流道分流密封內座).

Standalone part coordinates: Z = 0.00 .. 7.40 mm (placed at Z_cap = 1.60 mm in `helical_mixer_cap`).
Matches vendor CAD cross-section (`混合頭.png`) 1:1 while resolving syringe nozzle mating:
- Total height: 7.40 mm (Z = 0.00 .. 7.40 mm), single watertight B-Rep solid, straight-pull moldable
- Dual lower sealing sleeves at X = ±4.00 mm (8.00 mm pitch):
  OD Ø5.60 mm (Z = 0.00 .. 4.40 mm), female nozzle socket Ø3.26 mm CAD (Ø3.10±0.05 mm molded
  interference) x 1.95 mm deep, straight vertical Ø1.80 mm risers emptying directly into Ø10.00 mm cup!
- Stepped anti-pullout peripheral flange:
  Lower retaining rim Ø19.60 mm (Z = 4.40 .. 5.18 mm) + Upper flange Ø18.60 mm (Z = 5.18 .. 6.40 mm)
- Upper central boss: Ø12.20 mm (Z = 6.40 .. 7.40 mm) with Ø10.00 mm collection cup, central
  inverted-frustum diverter island (Ø4.40 -> Ø5.80 mm), & 0.80 mm partition rib keeping A & B
  separated until entering Part #1-3's bell mouth.
"""
from __future__ import annotations

from cadgen import build123d as bd
from cadgen import glb, srgb, step, stl
from lib import specs as S


def build_mixer_part2_seal_seat() -> bd.Shape:
    # Stepped main flange (Z = 4.40 .. 6.40 mm) + upper boss (Z = 6.40 .. 7.40 mm)
    rim_low = bd.Pos(0, 0, 4.40) * bd.Cylinder(
        radius=S.MIXER_P2_RIM_OD / 2.0,
        height=0.82,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    flange_up = bd.Pos(0, 0, 5.18) * bd.Cylinder(
        radius=S.MIXER_P2_FLANGE_OD / 2.0,
        height=1.26,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    boss_top = bd.Pos(0, 0, 6.40) * bd.Cylinder(
        radius=S.MIXER_P2_BOSS_OD / 2.0,
        height=1.00,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    body = rim_low + flange_up + boss_top

    # Dual lower sleeves (Z = 0.00 .. 4.50 mm) at X = ±4.00 mm
    for nx in (S.NOZZLE_X_A, S.NOZZLE_X_B):
        sleeve = bd.Pos(nx, 0, 0.00) * bd.Cylinder(
            radius=S.MIXER_P2_SLEEVE_OD / 2.0,
            height=4.50,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )
        body = body + sleeve

    # Cut upper collection cup (Z = 6.40 .. 7.50 mm, Ø10.00 mm) + inner annular channel (Z = 4.80 .. 6.45 mm, Ø6.20 mm)
    cup_upper = bd.Pos(0, 0, 6.40) * bd.Cylinder(
        radius=S.MIXER_P2_CUP_ID / 2.0,
        height=1.10,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    cup_mid = bd.Pos(0, 0, 4.80) * bd.Cylinder(
        radius=6.20 / 2.0,
        height=1.70,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    body = body - cup_upper - cup_mid

    # Re-add central inverted-frustum diverter island (Z = 4.65 .. 6.40 mm, Ø4.20 -> Ø5.40 mm)
    # matching the exact slanted central feature visible in vendor's `混合頭.png`!
    diverter_island = bd.Pos(0, 0, 4.65) * bd.Cone(
        bottom_radius=4.20 / 2.0,
        top_radius=5.40 / 2.0,
        height=1.75,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    # Central partition rib across Y separating +X (A) and -X (B) inside the Ø10.00 cup up to Z = 7.35 mm
    divider_rib = bd.Pos(0, 0, 4.65) * bd.Box(
        0.80,
        S.MIXER_P2_CUP_ID + 0.30,
        2.70,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    island = bd.Cylinder(
        radius=(S.MIXER_P2_CUP_ID + 0.20) / 2.0,
        height=2.70,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    ).moved(bd.Location((0, 0, 4.65))) & (diverter_island + divider_rib)
    body = body + island

    # Cut straight vertical female nozzle sockets (Z = -0.10 .. 1.95 mm) & straight Ø1.80 mm risers!
    for nx in (S.NOZZLE_X_A, S.NOZZLE_X_B):
        sock = bd.Pos(nx, 0, -0.10) * bd.Cylinder(
            radius=3.26 / 2.0,
            height=2.05,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )
        riser = bd.Pos(nx, 0, 1.90) * bd.Cylinder(
            radius=S.NOZZLE_ID / 2.0,
            height=5.00,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )
        body = body - sock - riser

    body.label = "mixer_part2_seal_seat"
    body.color = srgb(S.HEX_SEAL_BROWN)
    return body


@step(out="../STEP/mixer_part2_seal_seat.step")
@stl(out="../STL/mixer_part2_seal_seat.stl")
@glb(out="../GLB/mixer_part2_seal_seat.glb")
def mixer_part2_seal_seat():
    return build_mixer_part2_seal_seat()


if __name__ == "__main__":
    mixer_part2_seal_seat()
