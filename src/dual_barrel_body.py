"""Dual-Barrel Syringe Body (雙腔針筒本體) with 4-lobed finger flange, eccentric nozzles & Poka-Yoke bayonet collar."""
from __future__ import annotations

from cadgen import build123d as bd
from cadgen import srgb, step, stl
from lib import cap_features as CF
from lib import specs as S


def _build_dual_barrel_body() -> bd.Shape:
    # 1. 4-Lobed Ergonomic Finger Flange (Z = 0.00 .. 2.00 mm; 46.10 x 33.41 mm exact)
    wing_2d = bd.fillet(
        bd.Rectangle(S.FLANGE_SPAN_X, S.FLANGE_WING_WIDTH_Y).vertices(), radius=5.0
    )
    ear_r = 8.40
    ear_cy = S.FLANGE_SPAN_Y / 2.0 - ear_r  # 16.705 - 8.40 = 8.305 -> total Y = 33.41 mm exact
    ear_pos = bd.Pos(0, ear_cy) * bd.Circle(ear_r)
    ear_neg = bd.Pos(0, -ear_cy) * bd.Circle(ear_r)
    flange_sketch = wing_2d + ear_pos + ear_neg
    flange = bd.extrude(flange_sketch, amount=S.FLANGE_THICKNESS)

    # 2. Dual Cylindrical Barrels (X = ±7.20 mm, OD = Ø15.40 mm, Z = 0 .. 63.80 mm)
    barrel_a_outer = bd.Pos(S.BARREL_X_A, 0, 0) * bd.Cylinder(
        radius=S.BARREL_OD / 2.0,
        height=S.DECK_FLOOR_Z,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    barrel_b_outer = bd.Pos(S.BARREL_X_B, 0, 0) * bd.Cylinder(
        radius=S.BARREL_OD / 2.0,
        height=S.DECK_FLOOR_Z,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    center_web = bd.Pos(0, 0, 0) * bd.Box(
        S.BARREL_PITCH,
        9.60,
        S.DECK_FLOOR_Z,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )

    # 3. Front Bayonet Collar Housing (Z = 58.50 .. 69.40 mm, exact total length = 69.40 mm)
    collar_base = bd.Pos(0, 0, 58.50) * bd.Cylinder(
        radius=S.COLLAR_OD / 2.0,
        height=S.BARREL_TOTAL_LENGTH - 58.50,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    # Trim collar outer Y slightly to blend cleanly with barrel aesthetics while preserving Ø25.60 crescent lock
    body = flange + barrel_a_outer + barrel_b_outer + center_web + collar_base

    # Cut recessed front deck cavity (ID = Ø22.20 mm, Z = 63.80 .. 69.40 mm)
    collar_cavity = bd.Pos(0, 0, S.DECK_FLOOR_Z) * bd.Cylinder(
        radius=S.COLLAR_ID / 2.0,
        height=(S.BARREL_TOTAL_LENGTH - S.DECK_FLOOR_Z) + 0.5,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    body = body - collar_cavity

    # Cut Poka-Yoke asymmetric bayonet drop-in gaps through top of collar (Z = 63.80 .. 69.60 mm):
    # - +Y Wide Entry Throat (+48° .. +82° = 34° wide -> accepts 26° wide Lug A)
    # - -Y Narrow Entry Throat (-125.5° .. -104.5° = 21° wide -> accepts ONLY 15° narrow Lug B!)
    gap_h = (S.BARREL_TOTAL_LENGTH - S.DECK_FLOOR_Z) + 0.5
    wide_entry = CF.make_annular_sector(
        S.COLLAR_ID / 2.0 - 0.5, S.COLLAR_OD / 2.0 + 2.0, 48.0, 82.0, gap_h, S.DECK_FLOOR_Z
    )
    narrow_entry = CF.make_annular_sector(
        S.COLLAR_ID / 2.0 - 0.5, S.COLLAR_OD / 2.0 + 2.0, -125.5, -104.5, gap_h, S.DECK_FLOOR_Z
    )
    # Also relieve outer Y shoulders outside the two crescent walls (+82°..+132° and -104.5°..-48°)
    open_plus_y = CF.make_annular_sector(
        S.COLLAR_ID / 2.0 - 0.5, S.COLLAR_OD / 2.0 + 2.0, 48.0, 132.0, gap_h, S.DECK_FLOOR_Z
    )
    open_minus_y = CF.make_annular_sector(
        S.COLLAR_ID / 2.0 - 0.5, S.COLLAR_OD / 2.0 + 2.0, -125.5, -55.0, gap_h, S.DECK_FLOOR_Z
    )
    # Wait: keep Poka-Yoke stop block on -Y side (-104.5° .. -55°) intact as overhanging lip, OR make Poka-Yoke key rib!
    # Let us inspect: if open_plus_y is [48°, 112°] (64° open gap) and open_minus_y is [-125.5°, -104.5°] (21° open gap):
    # Wait: in zoom_混合頭.png bottom, both +Y and -Y have open crescent gaps, with a Poka-Yoke key tab on one side!
    # Making +Y gap = [50°, 110°] (60°) and -Y gap = [-122°, -102°] (20° narrow throat!) keeps two clean crescent walls AND enforces Poka-Yoke!
    gap_plus_y = CF.make_annular_sector(
        S.COLLAR_ID / 2.0 - 0.5, S.COLLAR_OD / 2.0 + 2.0, 50.0, 110.0, gap_h, S.DECK_FLOOR_Z
    )
    gap_minus_y = CF.make_annular_sector(
        S.COLLAR_ID / 2.0 - 0.5, S.COLLAR_OD / 2.0 + 2.0, -122.0, -102.0, gap_h, S.DECK_FLOOR_Z
    )
    body = body - gap_plus_y - gap_minus_y

    # Cut internal bayonet undercut L-grooves (Ø24.30 mm, Z = 63.80 .. 65.90 mm):
    # Lug A enters at +65° and twists CW to 0° (stop at -15°); Lug B enters at -115° and twists CW to 180°/-180° (stop at +168°)
    undercut_a = CF.make_annular_sector(
        S.COLLAR_ID / 2.0 - 0.3,
        S.BAYONET_GROOVE_DIA / 2.0,
        -15.0,
        85.0,
        S.BAYONET_GROOVE_HEIGHT,
        S.DECK_FLOOR_Z,
    )
    undercut_b = CF.make_annular_sector(
        S.COLLAR_ID / 2.0 - 0.3,
        S.BAYONET_GROOVE_DIA / 2.0,
        168.0,
        258.0,
        S.BAYONET_GROOVE_HEIGHT,
        S.DECK_FLOOR_Z,
    )
    body = body - undercut_a - undercut_b

    # 4. Add Dual Eccentric Male Outlet Nozzles (X = ±4.00 mm, OD = Ø3.20 mm, Z = 63.80 .. 67.30 mm)
    for nx in (S.NOZZLE_X_A, S.NOZZLE_X_B):
        noz = bd.Pos(nx, 0, S.DECK_FLOOR_Z - 0.5) * bd.Cylinder(
            radius=S.NOZZLE_OD / 2.0,
            height=S.NOZZLE_HEIGHT + 0.5,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )
        body = body + noz

    # 5. Cut Internal Barrel Bores (Ø12.20 mm -> asymmetric conical roof -> Ø1.80 mm nozzle through-bore)
    for bx, nx in ((S.BARREL_X_A, S.NOZZLE_X_A), (S.BARREL_X_B, S.NOZZLE_X_B)):
        cyl_bore = bd.Pos(bx, 0, -0.2) * bd.Cylinder(
            radius=S.BARREL_ID / 2.0,
            height=S.BARREL_BORE_CYL_Z + 0.2,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )
        # Rear lead-in chamfer for stopper assembly
        lead_in = bd.Pos(bx, 0, -0.05) * bd.Cone(
            bottom_radius=S.BARREL_ID / 2.0 + 0.45,
            top_radius=S.BARREL_ID / 2.0,
            height=0.85,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )
        # Asymmetric lofted conical roof converging from Barrel X (±7.20) to Nozzle X (±4.00)
        sec_low = bd.Pos(bx, 0, S.BARREL_BORE_CYL_Z - 0.05) * bd.Circle(S.BARREL_ID / 2.0)
        sec_high = bd.Pos(nx, 0, S.BARREL_BORE_TOP_Z) * bd.Circle(S.NOZZLE_ID / 2.0)
        roof_cone = bd.loft([sec_low, sec_high], ruled=True)

        # Continuous Ø1.80 mm nozzle outlet bore
        noz_bore = bd.Pos(nx, 0, S.BARREL_BORE_TOP_Z - 0.2) * bd.Cylinder(
            radius=S.NOZZLE_ID / 2.0,
            height=(S.DECK_FLOOR_Z + S.NOZZLE_HEIGHT - S.BARREL_BORE_TOP_Z) + 0.5,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )
        body = body - cyl_bore - lead_in - roof_cone - noz_bore

    body.label = "dual_barrel_body"
    body.color = srgb(S.HEX_BARREL_CLEAR, 0.38)
    return body


@step(out="../STEP/dual_barrel_body.step")
@stl(out="../STL/dual_barrel_body.stl")
def dual_barrel_body():
    return _build_dual_barrel_body()


if __name__ == "__main__":
    dual_barrel_body()
