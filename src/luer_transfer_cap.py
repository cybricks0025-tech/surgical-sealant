"""Part #2: Luer Reconstitution Transfer Cap (魯爾混合單管蓋, Ø30.00 x 15.00 mm).

- Purple knurled outer bayonet cap (Ø30.00 x 3.40 mm flange, Ø22.00 skirt, 23.96 mm Poka-Yoke lugs)
  with 65-deg arcuate kidney slot allowing independent outer-ring rotation.
- Teal stationary insert with Blind Plug on Barrel B (-4.00 mm) and ISO 80369-7 Female Luer-Lock
  port (Ø7.80 mm thread OD, 6% internal taper, 6.00 mm height) on Barrel A (+4.00 mm).
"""
from __future__ import annotations

import math
from cadgen import build123d as bd
from cadgen import srgb, step, stl
from lib import cap_features as CF
from lib import specs as S


def _build_luer_transfer_cap() -> bd.Shape:
    cap_face_z = S.LUER_SKIRT_LEN + S.LUER_FLANGE_THICK  # 5.60 + 3.40 = 9.00 mm

    # 1. Purple Knurled Outer Bayonet Ring (Z = 0.00 .. 9.00 mm)
    skirt = bd.Cylinder(
        radius=S.CAP_BODY_OD / 2.0,
        height=S.LUER_SKIRT_LEN + 0.2,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    skirt = CF.add_poka_yoke_bayonet_lugs(skirt, z0=0.0)

    flange = bd.Pos(0, 0, S.LUER_SKIRT_LEN) * bd.Cylinder(
        radius=S.LUER_FLANGE_OD / 2.0,
        height=S.LUER_FLANGE_THICK,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    # 32 grip knurl flutes at half-step angles so 0/90/180/270 deg preserve exact Ø30.00 mm envelope
    knurl_cuts = []
    n_knurl = 32
    for i in range(n_knurl):
        ang = math.radians((i + 0.5) * (360.0 / n_knurl))
        kx = (S.LUER_FLANGE_OD / 2.0 + 0.15) * math.cos(ang)
        ky = (S.LUER_FLANGE_OD / 2.0 + 0.15) * math.sin(ang)
        knurl_cuts.append(
            bd.Pos(kx, ky, S.LUER_SKIRT_LEN - 0.1)
            * bd.Cylinder(
                radius=0.58,
                height=S.LUER_FLANGE_THICK + 0.2,
                align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
            )
        )
    flange = flange - bd.Compound(children=knurl_cuts)
    outer = skirt + flange

    # Internal stepped counterbore for stationary teal insert
    cav_low = bd.Pos(0, 0, -0.2) * bd.Cylinder(
        radius=18.72 / 2.0,
        height=6.34 + 0.2,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    cav_high = bd.Pos(0, 0, 6.25) * bd.Cylinder(
        radius=17.12 / 2.0,
        height=(7.15 - 6.25),
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )

    # 65-deg Arcuate Kidney Slot on top face (Z = 7.05 .. 9.20 mm) around r = 4.00 mm
    slot_r = 4.05  # 8.10 mm slot width clears Ø7.60 mm teal neck
    kidney_arc = CF.make_annular_sector(
        0.10, S.NOZZLE_X_A + slot_r, -65.0, 0.0, cap_face_z - 7.05 + 0.3, 7.05
    )
    end_a = bd.Pos(S.NOZZLE_X_A, 0, 7.05) * bd.Cylinder(
        radius=slot_r,
        height=cap_face_z - 7.05 + 0.3,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    a_rad = math.radians(-65.0)
    end_b = bd.Pos(S.NOZZLE_X_A * math.cos(a_rad), S.NOZZLE_X_A * math.sin(a_rad), 7.05) * bd.Cylinder(
        radius=slot_r,
        height=cap_face_z - 7.05 + 0.3,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    outer = outer - cav_low - cav_high - kidney_arc - end_a - end_b
    outer.label = "luer_outer_ring"
    outer.color = srgb(S.HEX_LUER_PURPLE)

    # 2. Teal Stationary Eccentric Female Luer-Lock + Blind-Plug Insert (Z = 1.60 .. 15.00 mm)
    teal = CF.make_dual_seal_base(open_a=True, open_b=False)

    # Neck passing through kidney slot (Z = 7.05 .. 9.00 mm, OD = Ø7.50 mm)
    luer_neck = bd.Pos(S.NOZZLE_X_A, 0, 7.05) * bd.Cylinder(
        radius=7.50 / 2.0,
        height=cap_face_z - 7.05 + 0.1,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    # Protruding ISO 80369-7 Female Luer-Lock Boss (Z = 9.00 .. 15.00 mm -> exact 6.00 mm height!)
    luer_core = bd.Pos(S.NOZZLE_X_A, 0, cap_face_z) * bd.Cylinder(
        radius=6.60 / 2.0,
        height=S.LUER_BOSS_LEN,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    # External Ø7.80 mm Luer-Lock thread lug rim & thread bands (exact Ø7.80 mm envelope!)
    lug_top = bd.Pos(S.NOZZLE_X_A, 0, S.LUER_CAP_TOTAL_LEN - 1.10) * bd.Cylinder(
        radius=S.LUER_THREAD_OD / 2.0,
        height=1.10,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    lug_mid1 = bd.Pos(S.NOZZLE_X_A, 0, cap_face_z + 1.40) * bd.Cylinder(
        radius=S.LUER_THREAD_OD / 2.0,
        height=0.90,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    lug_mid2 = bd.Pos(S.NOZZLE_X_A, 0, cap_face_z + 3.00) * bd.Cylinder(
        radius=S.LUER_THREAD_OD / 2.0,
        height=0.90,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    # Standard ISO 80369-7 side flats on external thread lugs (along X, keeping Y span = exact Ø7.80 mm
    # and X span = exact Ø7.80 mm on lug_top while relieving flats at ±45 deg or Y sides? Keep full Ø7.80 at X & Y!)
    teal = teal + luer_neck + luer_core + lug_top + lug_mid1 + lug_mid2

    # Cut internal 6% Female Luer conical bore (Z = 9.00 .. 15.05 mm: Ø3.91 -> Ø4.27 mm) + Ø2.00 mm throat
    luer_taper = bd.Pos(S.NOZZLE_X_A, 0, cap_face_z - 0.05) * bd.Cone(
        bottom_radius=S.LUER_TAPER_BASE_ID / 2.0,
        top_radius=S.LUER_TAPER_OPEN_ID / 2.0,
        height=S.LUER_BOSS_LEN + 0.15,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    luer_throat = bd.Pos(S.NOZZLE_X_A, 0, 5.20) * bd.Cylinder(
        radius=S.LUER_THROAT_ID / 2.0,
        height=(cap_face_z - 5.20) + 0.2,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    teal = teal - luer_taper - luer_throat
    teal.label = "eccentric_luer_insert"
    teal.color = srgb(S.HEX_LUER_TEAL)

    return bd.Compound(children=[outer, teal], label="luer_transfer_cap")


@step(out="../STEP/luer_transfer_cap.step")
@stl(out="../STL/luer_transfer_cap.stl")
def luer_transfer_cap():
    return _build_luer_transfer_cap()


if __name__ == "__main__":
    luer_transfer_cap()
