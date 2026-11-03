"""Part #4: Single/Dual Plunger Selector Clip (單雙管推拉切換片, 30.00 x 16.40 x 4.00 mm).

- Captive pivot journal at Barrel B (X = -7.20 mm): rotates 90 deg without detaching.
- Side-entry elastic snap-in C-hook at Barrel A (X = +7.20 mm): locks both plungers for 1:1 drive
  when horizontal (0 deg), or releases Plunger A when swung 90 deg down (-Y).
"""
from __future__ import annotations

from cadgen import build123d as bd
from cadgen import srgb, step, stl
from lib import specs as S


def _build_plunger_clip() -> bd.Shape:
    # 1. Outer rounded rectangular block (30.00 x 16.40 x 4.00 mm, Z = 0 .. 4.00 mm)
    base_2d = bd.fillet(
        bd.Rectangle(S.CLIP_SPAN_X, S.CLIP_WIDTH_Y).vertices(), radius=2.20
    )
    body = bd.extrude(base_2d, amount=S.CLIP_THICKNESS)

    slot_z0 = S.CLIP_BACK_WALL                      # 1.40 mm
    slot_z1 = S.CLIP_BACK_WALL + S.CLIP_SLOT_DEPTH  # 3.20 mm

    # 2. Captive Pivot Pocket at X = -7.20 mm (Barrel B)
    pivot_disc_pocket = bd.Pos(S.BARREL_X_B, 0, slot_z0) * bd.Cylinder(
        radius=S.CLIP_POCKET_DIA / 2.0,
        height=S.CLIP_SLOT_DEPTH,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    pivot_neck_hole = bd.Pos(S.BARREL_X_B, 0, slot_z0) * bd.Cylinder(
        radius=S.CLIP_PIVOT_HOLE_DIA / 2.0,
        height=S.CLIP_THICKNESS - slot_z0 + 0.5,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    # End molding relief window at -X end (matches vendor CAD detail in zoom_clip.png!)
    end_window = bd.Pos(-S.CLIP_SPAN_X / 2.0 + 1.80, 0, slot_z0) * bd.Box(
        1.80,
        7.60,
        S.CLIP_SLOT_DEPTH,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )

    # 3. Side-Entry Snap-In C-Pocket at X = +7.20 mm (Barrel A)
    snap_disc_pocket = bd.Pos(S.BARREL_X_A, 0, slot_z0) * bd.Cylinder(
        radius=S.CLIP_POCKET_DIA / 2.0,
        height=S.CLIP_SLOT_DEPTH,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    snap_neck_hole = bd.Pos(S.BARREL_X_A, 0, slot_z0) * bd.Cylinder(
        radius=S.CLIP_PIVOT_HOLE_DIA / 2.0,
        height=S.CLIP_THICKNESS - slot_z0 + 0.5,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    # Open -Y side entry throat:
    # - Internal disc slot entry width = 11.90 mm (0.90 mm snap detent over Ø12.80 thumb disc!)
    # - Front lip neck entry width = 6.50 mm (clears Ø6.20 plunger neck during swing!)
    disc_side_entry = bd.Pos(S.BARREL_X_A, -S.CLIP_WIDTH_Y / 2.0, slot_z0) * bd.Box(
        S.CLIP_SNAP_THROAT,
        S.CLIP_WIDTH_Y,
        S.CLIP_SLOT_DEPTH,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    neck_side_entry = bd.Pos(S.BARREL_X_A, -S.CLIP_WIDTH_Y / 2.0, slot_z1 - 0.1) * bd.Box(
        6.50,
        S.CLIP_WIDTH_Y,
        S.CLIP_FRONT_LIP + 0.4,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    # Center slot connecting between the two pockets inside Z = 1.40..3.20 for clean molding
    mid_slot = bd.Pos(0, 0, slot_z0) * bd.Box(
        S.BARREL_PITCH,
        9.00,
        S.CLIP_SLOT_DEPTH,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    # Elastic relief slit on +X side of C-jaw so snap arm flexes smoothly without stress cracking
    flex_slit = bd.Pos(S.BARREL_X_A + 5.60, 1.20, slot_z0) * bd.Box(
        3.20,
        1.10,
        S.CLIP_THICKNESS - slot_z0 + 0.4,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )

    body = (
        body
        - pivot_disc_pocket
        - pivot_neck_hole
        - end_window
        - snap_disc_pocket
        - snap_neck_hole
        - disc_side_entry
        - neck_side_entry
        - mid_slot
        - flex_slit
    )

    body.label = "plunger_clip"
    body.color = srgb(S.HEX_CLIP_GREEN)
    return body


@step(out="../STEP/plunger_clip.step")
@stl(out="../STL/plunger_clip.stl")
def plunger_clip():
    return _build_plunger_clip()


if __name__ == "__main__":
    plunger_clip()
