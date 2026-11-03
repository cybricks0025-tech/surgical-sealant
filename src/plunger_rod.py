"""Cruciform Plunger Rod (十字推桿) with rear thumb disc, neck journal, and front stopper stud."""
from __future__ import annotations

from cadgen import build123d as bd
from cadgen import srgb, step, stl
from lib import specs as S


def _build_plunger_rod() -> bd.Shape:
    # 1. Rear Thumb Disc (Z = 0.00 .. 1.60 mm, Ø12.80 mm)
    disc = bd.Cylinder(
        radius=S.PLUNGER_DISC_OD / 2.0,
        height=S.PLUNGER_DISC_THICK,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )

    # 2. Pivot/Clip Neck Journal (Z = 1.60 .. 4.80 mm, Ø6.20 mm)
    neck_z0 = S.PLUNGER_DISC_THICK
    neck = bd.Pos(0, 0, neck_z0) * bd.Cylinder(
        radius=S.PLUNGER_NECK_OD / 2.0,
        height=S.PLUNGER_NECK_LEN,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )

    # 3. Tapered Cruciform (+) Shaft (Z = 4.80 .. 71.10 mm)
    shaft_z0 = neck_z0 + S.PLUNGER_NECK_LEN
    pusher_thick = 1.20
    shaft_z1 = S.PLUNGER_TOTAL_LEN - pusher_thick  # 72.30 - 1.20 = 71.10 mm
    taper_len = 5.50

    # Tapered transition cone + cruciform shaft
    transition = bd.Pos(0, 0, shaft_z0) * bd.Cone(
        bottom_radius=S.PLUNGER_NECK_OD / 2.0,
        top_radius=S.PLUNGER_RIB_SPAN / 2.0,
        height=taper_len,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    rib_mask = bd.Pos(0, 0, shaft_z0) * (
        bd.Box(
            S.PLUNGER_RIB_SPAN + 1.0,
            S.PLUNGER_RIB_THICK,
            shaft_z1 - shaft_z0,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )
        + bd.Box(
            S.PLUNGER_RIB_THICK,
            S.PLUNGER_RIB_SPAN + 1.0,
            shaft_z1 - shaft_z0,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )
    )
    tapered_ribs = transition & rib_mask

    main_ribs = bd.Pos(0, 0, shaft_z0 + taper_len) * (
        bd.Box(
            S.PLUNGER_RIB_SPAN,
            S.PLUNGER_RIB_THICK,
            shaft_z1 - (shaft_z0 + taper_len),
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )
        + bd.Box(
            S.PLUNGER_RIB_THICK,
            S.PLUNGER_RIB_SPAN,
            shaft_z1 - (shaft_z0 + taper_len),
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )
    )
    core_rod = bd.Pos(0, 0, shaft_z0) * bd.Cylinder(
        radius=2.10,
        height=shaft_z1 - shaft_z0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )

    # 4. Front Pusher Seat Disc (Z = 71.10 .. 72.30 mm, Ø10.60 mm)
    pusher = bd.Pos(0, 0, shaft_z1) * bd.Cylinder(
        radius=5.30,
        height=pusher_thick,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )

    # 5. Stopper Retention Stud (Z = 72.30 .. 75.50 mm)
    stud_stem = bd.Pos(0, 0, S.PLUNGER_TOTAL_LEN) * bd.Cylinder(
        radius=2.30,
        height=1.60,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    stud_head = bd.Pos(0, 0, S.PLUNGER_TOTAL_LEN + 1.60) * bd.Cone(
        bottom_radius=3.00,
        top_radius=1.80,
        height=1.60,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )

    rod = disc + neck + tapered_ribs + main_ribs + core_rod + pusher + stud_stem + stud_head
    rod.label = "plunger_rod"
    rod.color = srgb(S.HEX_PLUNGER_SLATE)
    return rod


@step(out="../STEP/plunger_rod.step")
@stl(out="../STL/plunger_rod.stl")
def plunger_rod():
    return _build_plunger_rod()


if __name__ == "__main__":
    plunger_rod()
