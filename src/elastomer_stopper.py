"""Medical Elastomer Syringe Stopper (醫療級三環彈性活塞, 7.00 mm length)."""
from __future__ import annotations

from cadgen import build123d as bd
from cadgen import srgb, step, stl
from lib import specs as S


def _build_elastomer_stopper() -> bd.Shape:
    r_seal = S.STOPPER_OD / 2.0      # 6.08 mm CAD fit (Ø12.50±0.10 molded interference)
    r_valley = r_seal - 0.45         # Relief groove between triple sealing ribs

    # Main cylindrical core + conical dome tip (Z = 0.00 .. 7.00 mm)
    cyl_h = 5.20
    cone_h = S.STOPPER_LENGTH - cyl_h  # 1.80 mm
    body = bd.Cylinder(
        radius=r_seal,
        height=cyl_h,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    ) + bd.Pos(0, 0, cyl_h) * bd.Cone(
        bottom_radius=r_seal,
        top_radius=1.80,
        height=cone_h,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )

    # Cut two circumferential friction-relief grooves leaving 3 sealing ribs
    for gz in (1.35, 3.15):
        groove = bd.Pos(0, 0, gz) * (
            bd.Cylinder(
                radius=r_seal + 0.5,
                height=0.85,
                align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
            )
            - bd.Cylinder(
                radius=r_valley,
                height=0.95,
                align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
            ).moved(bd.Location((0, 0, -0.05)))
        )
        body = body - groove

    # Cut internal retention cavity matching plunger_rod's stud (with 0.08 mm clearance)
    cav_stem = bd.Pos(0, 0, -0.1) * bd.Cylinder(
        radius=2.40,
        height=1.80,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    cav_head = bd.Pos(0, 0, 1.55) * bd.Cone(
        bottom_radius=3.12,
        top_radius=1.92,
        height=1.85,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    body = body - cav_stem - cav_head

    body.label = "elastomer_stopper"
    body.color = srgb(S.HEX_STOPPER_PURPLE)
    return body


@step(out="../STEP/elastomer_stopper.step")
@stl(out="../STL/elastomer_stopper.stl")
def elastomer_stopper():
    return _build_elastomer_stopper()


if __name__ == "__main__":
    elastomer_stopper()
