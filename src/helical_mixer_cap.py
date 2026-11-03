"""Part #1: Helical Static Mixer Cap (螺旋混合雙管蓋, Ø22.00 x 41.60 mm; cannula Ø4.00 x 26.73 mm).

4-part subassembly:
1. Olive-green ribbed bayonet outer cap (Ø22.00 x 14.87 mm, 23.96 mm Poka-Yoke lugs)
2. Brown dual-sleeve elastomer seal seat (keeps Channels A & B separated through base)
3. Maroon conical Y-convergence funnel (merges streams right at mixer entrance to prevent manifold gelation)
4. Clear Ø4.00 mm cannula + 8-element alternating L/R 180-deg Kenics helical static mixer core
"""
from __future__ import annotations

import math
from cadgen import build123d as bd
from cadgen import srgb, step, stl
from lib import cap_features as CF
from lib import specs as S


def _make_kenics_helical_core(z_start: float, n_elements: int, elem_len: float) -> bd.Shape:
    """Build an alternating left/right 180-deg twisted Kenics static mixer core."""
    blade_w = 2.82
    blade_t = 0.42
    parts = []
    stations = 5  # 0, 45, 90, 135, 180 deg per element

    for idx in range(n_elements):
        ez0 = z_start + idx * elem_len
        direction = 1.0 if (idx % 2 == 0) else -1.0
        base_ang = 90.0 * idx  # Orthogonal 90-deg flow-splitting junction between adjacent elements!
        profiles = []
        for s in range(stations):
            frac = s / (stations - 1)
            ang = base_ang + direction * 180.0 * frac
            z = ez0 + frac * elem_len
            prof = (
                bd.Pos(0, 0, z)
                * bd.Rot(0, 0, ang)
                * bd.Rectangle(blade_w, blade_t)
            )
            profiles.append(prof)
        elem = bd.loft(profiles, ruled=True)
        parts.append(elem)

        if idx > 0:
            # Small central structural tie cylinder across orthogonal blade transition
            hub = bd.Pos(0, 0, ez0 - 0.25) * bd.Cylinder(
                radius=0.58,
                height=0.50,
                align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
            )
            parts.append(hub)

    core = parts[0]
    for p in parts[1:]:
        core = core + p
    return core


def _build_helical_mixer_cap() -> bd.Shape:
    # 1. Olive-Green Ribbed Outer Bayonet Cap (Z = 0.00 .. 14.87 mm exact)
    shoulder_z0 = 12.40
    cyl = bd.Cylinder(
        radius=S.CAP_BODY_OD / 2.0,
        height=shoulder_z0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    cone_top = bd.Pos(0, 0, shoulder_z0) * bd.Cone(
        bottom_radius=S.CAP_BODY_OD / 2.0,
        top_radius=3.80,
        height=S.MIXER_BODY_LEN - shoulder_z0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    outer = CF.add_poka_yoke_bayonet_lugs(cyl + cone_top, z0=0.0)

    # 16 vertical grip flutes at half-angles so cardinal extremes stay exact Ø22.00 mm
    flutes = []
    for i in range(16):
        ang = math.radians((i + 0.5) * 22.5)
        fx = (S.CAP_BODY_OD / 2.0 + 0.15) * math.cos(ang)
        fy = (S.CAP_BODY_OD / 2.0 + 0.15) * math.sin(ang)
        flutes.append(
            bd.Pos(fx, fy, 2.30)
            * bd.Cylinder(
                radius=0.45,
                height=9.60,
                align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
            )
        )
    outer = outer - bd.Compound(children=flutes)

    # Internal stepped cavities for seal seat, Y-funnel, and cannula
    cav_low = bd.Pos(0, 0, -0.2) * bd.Cylinder(
        radius=18.72 / 2.0,
        height=6.34 + 0.2,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    cav_mid = bd.Pos(0, 0, 6.25) * bd.Cylinder(
        radius=17.12 / 2.0,
        height=(7.15 - 6.25),
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    cav_funnel = bd.Pos(0, 0, 7.10) * bd.Cylinder(
        radius=10.50 / 2.0,
        height=3.15,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    cav_tube = bd.Pos(0, 0, 10.20) * bd.Cylinder(
        radius=S.MIXER_TUBE_OD / 2.0 + 0.03,
        height=S.MIXER_BODY_LEN - 10.20 + 0.5,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    outer = outer - cav_low - cav_mid - cav_funnel - cav_tube
    outer.label = "mixer_outer_cap"
    outer.color = srgb(S.HEX_MIXER_OLIVE)

    # 2. Brown Dual-Sleeve Elastomer Seal Seat (Z = 1.60 .. 7.10 mm)
    seal_seat = CF.make_dual_seal_base(open_a=True, open_b=True)
    # Add upper tapered exit funnels at (±4.00, 0, 5.80..7.10) matching zoom_混合頭.png!
    for nx in (S.NOZZLE_X_A, S.NOZZLE_X_B):
        f_cut = bd.Pos(nx, 0, 5.75) * bd.Cone(
            bottom_radius=S.NOZZLE_ID / 2.0,
            top_radius=1.55,
            height=1.40,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )
        seal_seat = seal_seat - f_cut
    seal_seat.label = "mixer_seal_seat"
    seal_seat.color = srgb(S.HEX_SEAL_BROWN)

    # 3. Maroon Conical Y-Convergence Funnel (Z = 7.14 .. 10.18 mm)
    y_base = bd.Pos(0, 0, 7.14) * bd.Cylinder(
        radius=10.36 / 2.0,
        height=0.80,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    ) + bd.Pos(0, 0, 7.94) * bd.Cone(
        bottom_radius=10.36 / 2.0,
        top_radius=S.MIXER_TUBE_OD / 2.0,
        height=10.18 - 7.94,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    # Cut converging Y-channels from (±4.00, 0, 7.10) to (0, 0, 10.20)
    for nx in (S.NOZZLE_X_A, S.NOZZLE_X_B):
        s_in = bd.Pos(nx, 0, 7.08) * bd.Circle(1.45)
        s_out = bd.Pos(0.45 * (1 if nx > 0 else -1), 0, 10.22) * bd.Circle(0.95)
        y_base = y_base - bd.loft([s_in, s_out], ruled=True)
    y_throat = bd.Pos(0, 0, 9.70) * bd.Cylinder(
        radius=S.MIXER_TUBE_ID / 2.0,
        height=0.60,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    y_funnel = y_base - y_throat
    y_funnel.label = "y_convergence_funnel"
    y_funnel.color = srgb(S.HEX_FUNNEL_MAROON)

    # 4. Clear Mixing Cannula (Z = 10.24 .. 41.60 mm -> exposed past 14.87 = 26.73 mm exact!)
    cannula_z0 = 10.24
    cannula_len = S.MIXER_CAP_TOTAL_LEN - cannula_z0
    cannula = bd.Pos(0, 0, cannula_z0) * (
        bd.Cylinder(
            radius=S.MIXER_TUBE_OD / 2.0,
            height=cannula_len,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )
        - bd.Cylinder(
            radius=S.MIXER_TUBE_ID / 2.0,
            height=cannula_len + 0.4,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        ).moved(bd.Location((0, 0, -0.2)))
    )
    cannula.label = "mixing_cannula"
    cannula.color = srgb("#DCEAF7", 0.34)

    # 5. Red 8-Element Kenics Helical Static Mixer Core (Z = 15.00 .. 39.00 mm)
    mixer_core = _make_kenics_helical_core(
        z_start=15.00, n_elements=S.MIXER_ELEMENT_COUNT, elem_len=S.MIXER_ELEMENT_LEN
    )
    mixer_core.label = "helical_mixer_core"
    mixer_core.color = srgb(S.HEX_MIXER_RED)

    return bd.Compound(
        children=[outer, seal_seat, y_funnel, cannula, mixer_core],
        label="helical_mixer_cap",
    )


@step(out="../STEP/helical_mixer_cap.step")
@stl(out="../STL/helical_mixer_cap.stl")
def helical_mixer_cap():
    return _build_helical_mixer_cap()


if __name__ == "__main__":
    helical_mixer_cap()
