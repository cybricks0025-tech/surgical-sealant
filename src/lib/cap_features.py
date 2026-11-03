"""Shared bayonet lug and internal elastomer seal factories for Caps #1, #2, and #3."""
from __future__ import annotations

import math
from cadgen import build123d as bd
from lib import specs as S


def make_annular_sector(
    r_inner: float,
    r_outer: float,
    deg_start: float,
    deg_end: float,
    height: float,
    z0: float = 0.0,
) -> bd.Solid:
    """Create an exact 3D annular sector solid from deg_start to deg_end [deg] around +Z."""
    a0 = math.radians(deg_start)
    a1 = math.radians(deg_end)
    am = 0.5 * (a0 + a1)

    p_i0 = (r_inner * math.cos(a0), r_inner * math.sin(a0))
    p_im = (r_inner * math.cos(am), r_inner * math.sin(am))
    p_i1 = (r_inner * math.cos(a1), r_inner * math.sin(a1))

    p_o0 = (r_outer * math.cos(a0), r_outer * math.sin(a0))
    p_om = (r_outer * math.cos(am), r_outer * math.sin(am))
    p_o1 = (r_outer * math.cos(a1), r_outer * math.sin(a1))

    wire = bd.Wire(
        [
            bd.ThreePointArc(p_i0, p_im, p_i1),
            bd.Line(p_i1, p_o1),
            bd.ThreePointArc(p_o1, p_om, p_o0),
            bd.Line(p_o0, p_i0),
        ]
    )
    face = bd.make_face(wire)
    solid = bd.extrude(face, amount=height)
    return solid.moved(bd.Location((0, 0, z0)))


def add_poka_yoke_bayonet_lugs(cap_body: bd.Shape, z0: float = 0.0) -> bd.Shape:
    """Fuse asymmetric Poka-Yoke bayonet lugs (23.96 mm outer span) onto a Ø22.00 mm cap skirt.

    - Lug A (+X, 0 deg): 26 deg wide
    - Lug B (-X, 180 deg): 15 deg narrow
    """
    r_in = S.CAP_BODY_OD / 2.0 - 0.4
    r_out = S.CAP_LUG_SPAN / 2.0  # 11.98 mm -> 23.96 mm exact span
    lug_a = make_annular_sector(
        r_in, r_out, -S.LUG_WIDE_DEG / 2.0, S.LUG_WIDE_DEG / 2.0, S.CAP_LUG_HEIGHT, z0
    )
    lug_b = make_annular_sector(
        r_in, r_out, 180.0 - S.LUG_NARROW_DEG / 2.0, 180.0 + S.LUG_NARROW_DEG / 2.0, S.CAP_LUG_HEIGHT, z0
    )
    return cap_body + lug_a + lug_b


def make_dual_seal_base(open_a: bool, open_b: bool) -> bd.Shape:
    """Build the internal dual-nozzle elastomeric seal base seated at Z = 5.30..7.10 mm.

    - Barrel A nozzle socket is at X = +4.00 mm (`open_a=True` -> through bore; `False` -> blind plug + bore pin)
    - Barrel B nozzle socket is at X = -4.00 mm (`open_b=True` -> through bore; `False` -> blind plug + bore pin)
    """
    flange_h = S.SEAL_FLANGE_Z1 - S.SEAL_FLANGE_Z0
    flange = bd.Pos(0, 0, S.SEAL_FLANGE_Z0) * bd.Cylinder(
        radius=S.SEAL_FLANGE_OD / 2.0,
        height=flange_h,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    # Retention step on outer rim (matches vendor section step!)
    step_cut = bd.Pos(0, 0, S.SEAL_FLANGE_Z0 + flange_h * 0.55) * (
        bd.Cylinder(
            radius=S.SEAL_FLANGE_OD / 2.0 + 0.5,
            height=flange_h,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )
        - bd.Cylinder(
            radius=S.SEAL_FLANGE_OD / 2.0 - 0.8,
            height=flange_h + 0.2,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )
    )
    base = flange - step_cut

    sleeve_h = S.SEAL_FLANGE_Z0 - S.SEAL_SLEEVE_Z0 + 0.2
    for x_pos, is_open in ((S.NOZZLE_X_A, open_a), (S.NOZZLE_X_B, open_b)):
        sleeve = bd.Pos(x_pos, 0, S.SEAL_SLEEVE_Z0) * bd.Cylinder(
            radius=S.SEAL_SLEEVE_OD / 2.0,
            height=sleeve_h,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )
        base = base + sleeve

        # Female socket receiving the Ø3.20 mm syringe male nozzle (up to Z = 5.30 mm)
        socket_depth = (S.DECK_FLOOR_Z + S.NOZZLE_HEIGHT - S.CAP_SEAT_Z) - S.SEAL_SLEEVE_Z0 + 0.15
        socket = bd.Pos(x_pos, 0, S.SEAL_SLEEVE_Z0 - 0.1) * bd.Cylinder(
            radius=S.SEAL_SOCKET_ID / 2.0,
            height=socket_depth + 0.1,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )
        base = base - socket

        if is_open:
            # Through flow channel (Ø1.80 mm) through the top of the elastomer flange
            thru = bd.Pos(x_pos, 0, S.SEAL_SLEEVE_Z0 + socket_depth - 0.2) * bd.Cylinder(
                radius=S.NOZZLE_ID / 2.0,
                height=(S.SEAL_FLANGE_Z1 - (S.SEAL_SLEEVE_Z0 + socket_depth)) + 0.6,
                align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
            )
            base = base - thru
        else:
            # Central sealing pin entering the top of the Ø1.80 mm nozzle bore
            pin_top_z = S.SEAL_SLEEVE_Z0 + socket_depth + 0.2
            pin_bot_z = S.SEAL_SLEEVE_Z0 + 0.9
            pin = bd.Pos(x_pos, 0, pin_bot_z) * bd.Cylinder(
                radius=S.SEAL_PIN_OD / 2.0,
                height=pin_top_z - pin_bot_z,
                align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
            )
            base = base + pin

    return base
