"""Reference Single-Barrel Male Luer-Lock Powder Syringe (標準單管粉劑魯爾鎖定注射器) for Stage 2 Reconstitution."""
from __future__ import annotations

from cadgen import build123d as bd
from cadgen import srgb, step
from lib import specs as S


def _build_powder_syringe() -> bd.Shape:
    # Oriented with Male Luer-Lock tip pointing in -Z (from Z = 0.00 tip into +Z barrel)
    # so placing it at (NOZZLE_X_A, 0, CAP_SEAT_Z + LUER_CAP_TOTAL_LEN - 4.0) threads right onto Cap #2!
    # 1. Male Luer-Lock 6% cone (Z = 0.00 .. 6.50 mm) + internal Ø8.20 Lock Collar (Z = 1.50 .. 7.50 mm)
    luer_cone = bd.Cone(
        bottom_radius=1.96,
        top_radius=2.16,
        height=6.50,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    lock_skirt = bd.Pos(0, 0, 1.50) * (
        bd.Cylinder(
            radius=5.20,
            height=6.00,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )
        - bd.Cylinder(
            radius=4.05,
            height=5.20,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        ).moved(bd.Location((0, 0, -0.1)))
    )
    # Barrel body (Z = 6.50 .. 64.50 mm, Ø13.20 OD / Ø10.80 ID) + Finger Flange
    shoulder = bd.Pos(0, 0, 6.50) * bd.Cone(
        bottom_radius=5.20,
        top_radius=6.60,
        height=2.50,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    barrel = bd.Pos(0, 0, 9.00) * bd.Cylinder(
        radius=6.60,
        height=55.00,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    flange_2d = bd.fillet(bd.Rectangle(24.0, 14.5).vertices(), radius=3.5)
    flange = bd.Pos(0, 0, 62.50) * bd.extrude(flange_2d, amount=1.50)

    bore_main = bd.Pos(0, 0, 8.80) * bd.Cylinder(
        radius=5.40,
        height=56.00,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    bore_luer = bd.Pos(0, 0, -0.20) * bd.Cylinder(
        radius=1.00,
        height=9.50,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    syr_body = (luer_cone + lock_skirt + shoulder + barrel + flange) - bore_main - bore_luer
    syr_body.label = "powder_syringe_barrel"
    syr_body.color = srgb("#E6EEF5", 0.35)

    # Stopper & Plunger inside powder syringe (partially drawn back during mixing)
    stopper = bd.Pos(0, 0, 28.00) * bd.Cylinder(
        radius=5.35,
        height=6.00,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    stopper.label = "powder_stopper"
    stopper.color = srgb("#3A3D45")

    rod_ribs = bd.Pos(0, 0, 34.00) * (
        bd.Box(9.40, 1.40, 52.00, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        + bd.Box(1.40, 9.40, 52.00, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    )
    rod_disc = bd.Pos(0, 0, 86.00) * bd.Cylinder(
        radius=6.50,
        height=1.60,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    rod = rod_ribs + rod_disc
    rod.label = "powder_plunger"
    rod.color = srgb("#CFD6DE", 0.65)

    return bd.Compound(children=[syr_body, stopper, rod], label="powder_syringe")


@step(out="../STEP/powder_syringe.step")
def powder_syringe():
    return _build_powder_syringe()


if __name__ == "__main__":
    powder_syringe()
