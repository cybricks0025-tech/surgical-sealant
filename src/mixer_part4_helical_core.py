"""Part #1-4 (CSL-CAP-201-4): 9-Element Kenics Helical Mixer Core with Anti-Ejection Base
(防脫出底座靜態螺旋混合芯).

Standalone part coordinates: Z = 0.00 .. 28.00 mm (placed at Z_cap = 9.60 mm in `helical_mixer_cap`).
Inserted from the wide rear bell mouth of Part #1-3 (`CSL-CAP-201-3`) along +Z:
- Total length: 28.00 mm (Z = 0.00 .. 28.00 mm), single watertight B-Rep solid
- Rear Anti-Ejection Conical Collar & Splitter Bar (Z = 0.00 .. 1.00 mm):
  Outer diameter Ø4.40 -> Ø3.40 mm (> Ø3.00 mm cannula bore ID!), physically preventing
  the mixer core from ever blowing out the distal tip under high hydrogel dispensing pressure!
- 9 Alternating Left/Right 180-deg Twisted Kenics Blades (Z = 1.00 .. 28.00 mm):
  Pitch = 3.00 mm per element (27.00 mm active mixing zone, 2^9 = 512 striations),
  Blade span = 2.86 mm (light fit in Ø3.00 mm ID bore), Blade thickness = 0.42 mm.
"""
from __future__ import annotations

from cadgen import build123d as bd
from cadgen import glb, srgb, step, stl
from lib import specs as S


def build_mixer_part4_helical_core() -> bd.Shape:
    z_helix0 = 1.00
    n_elements = S.MIXER_ELEMENT_COUNT  # 9
    elem_len = S.MIXER_ELEMENT_LEN      # 3.00
    blade_w = S.MIXER_BLADE_SPAN        # 2.86
    blade_t = S.MIXER_BLADE_THICK       # 0.42
    stations = 5

    # 1. Rear Anti-Ejection Conical Collar (Z = 0.00 .. 1.00 mm, Ø4.40 -> Ø3.40 mm, wall 0.50 mm)
    collar_outer = bd.Cone(
        bottom_radius=S.MIXER_P4_COLLAR_OD / 2.0,
        top_radius=3.40 / 2.0,
        height=z_helix0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    collar_inner = bd.Pos(0, 0, -0.05) * bd.Cone(
        bottom_radius=3.40 / 2.0,
        top_radius=2.40 / 2.0,
        height=z_helix0 + 0.10,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    collar_ring = collar_outer - collar_inner

    # Diametral splitter bar spanning full Ø4.40->Ø3.40 collar & overlapping 0.30 mm up into Element 0!
    splitter_raw = bd.Box(
        S.MIXER_P4_COLLAR_OD + 0.4,
        blade_t,
        z_helix0 + 0.30,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    splitter_env = bd.Cone(
        bottom_radius=S.MIXER_P4_COLLAR_OD / 2.0,
        top_radius=3.40 / 2.0,
        height=z_helix0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    ) + (
        bd.Pos(0, 0, z_helix0 - 0.05)
        * bd.Cylinder(
            radius=blade_w / 2.0,
            height=0.40,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )
    )
    splitter_fin = splitter_raw & splitter_env
    # Central structural bridge hub from Z = 0.70 .. 1.35 mm tying collar, splitter & Element 0
    base_hub = bd.Pos(0, 0, 0.70) * bd.Cylinder(
        radius=0.62,
        height=0.65,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    # Cross-tie spokes inside collar (along Y axis) so collar_ring & base_hub fuse with 0 ambiguity
    y_spoke = bd.Pos(0, 0, 0.55) * bd.Box(
        0.52,
        3.10,
        0.45,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )

    core = collar_ring + splitter_fin + base_hub + y_spoke

    # 2. 9 Alternating L/R 180-deg Kenics Helical Elements (Z = 1.00 .. 28.00 mm)
    for idx in range(n_elements):
        ez0 = z_helix0 + idx * elem_len
        direction = 1.0 if (idx % 2 == 0) else -1.0
        base_ang = 90.0 * idx
        profiles = []
        for s in range(stations):
            frac = s / (stations - 1)
            ang = base_ang + direction * 180.0 * frac
            z = ez0 + frac * elem_len
            prof = bd.Pos(0, 0, z) * bd.Rot(0, 0, ang) * bd.Rectangle(blade_w, blade_t)
            profiles.append(prof)
        elem = bd.loft(profiles, ruled=True)
        core = core + elem

        if idx > 0:
            hub = bd.Pos(0, 0, ez0 - 0.25) * bd.Cylinder(
                radius=0.56,
                height=0.50,
                align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
            )
            core = core + hub

    core.label = "mixer_part4_helical_core"
    core.color = srgb(S.HEX_MIXER_RED)
    return core


@step(out="../STEP/mixer_part4_helical_core.step")
@stl(out="../STL/mixer_part4_helical_core.stl")
@glb(out="../GLB/mixer_part4_helical_core.glb")
def mixer_part4_helical_core():
    return build_mixer_part4_helical_core()


if __name__ == "__main__":
    mixer_part4_helical_core()
