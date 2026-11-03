"""Part #3: Initial Plug Valve Cap (初始塞閥蓋, Ø22.00 x 17.00 mm) for sterile storage & transport."""
from __future__ import annotations

import math
from cadgen import build123d as bd
from cadgen import srgb, step, stl
from lib import cap_features as CF
from lib import specs as S


def _build_initial_plug_cap() -> bd.Shape:
    # 1. Outer Sage-Green Twist-Grip Bayonet Cap (Z = 0.00 .. 17.00 mm)
    cyl = bd.Cylinder(
        radius=S.CAP_BODY_OD / 2.0,
        height=S.PLUG_CAP_BODY_LEN,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    outer = CF.add_poka_yoke_bayonet_lugs(cyl, z0=0.0)

    # Ergonomic flat twist tab (Z = 9.00 .. 17.00 mm -> length = 8.00 mm, thickness = 4.00 mm exact)
    # Profile in YZ (extruded along X = 20.00 mm) with ergonomic concave waist & 4.00 mm flared tip
    tab_pts = [
        (-2.00, S.PLUG_CAP_BODY_LEN - 0.3),
        (-2.00, S.PLUG_CAP_BODY_LEN + 1.2),
        (-1.45, S.PLUG_CAP_BODY_LEN + 4.5),
        (-2.00, S.PLUG_CAP_TOTAL_LEN),
        (2.00, S.PLUG_CAP_TOTAL_LEN),
        (1.45, S.PLUG_CAP_BODY_LEN + 4.5),
        (2.00, S.PLUG_CAP_BODY_LEN + 1.2),
        (2.00, S.PLUG_CAP_BODY_LEN - 0.3),
    ]
    tab_face = bd.Plane.YZ * bd.Polygon(*tab_pts, align=None)
    tab = bd.extrude(tab_face, amount=S.PLUG_TAB_SPAN / 2.0, both=True)
    # Trim tab X ends cleanly inside Ø21.0 cylinder so it sits nicely on the Ø22 cap face
    tab_trim = bd.Pos(0, 0, S.PLUG_CAP_BODY_LEN - 0.5) * bd.Cylinder(
        radius=S.PLUG_TAB_SPAN / 2.0,
        height=S.PLUG_TAB_LEN + 1.0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    outer = outer + (tab & tab_trim)

    # Internal stepped cavity receiving the dual blind elastomer plug pad
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
    outer = outer - cav_low - cav_high
    outer.label = "plug_outer_cap"
    outer.color = srgb(S.HEX_PLUG_SAGE)

    # 2. Internal Dual Blind Elastomer Plug Pad
    plug_pad = CF.make_dual_seal_base(open_a=False, open_b=False)
    plug_pad.label = "dual_blind_plug"
    plug_pad.color = srgb(S.HEX_PLUG_RUBBER)

    return bd.Compound(children=[outer, plug_pad], label="initial_plug_cap")


@step(out="../STEP/initial_plug_cap.step")
@stl(out="../STL/initial_plug_cap.stl")
def initial_plug_cap():
    return _build_initial_plug_cap()


if __name__ == "__main__":
    initial_plug_cap()
