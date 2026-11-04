"""Exploded 4-Part Showcase Assembly of Part #1 (`CSL-CAP-201-EXP`, 螺旋混合頭四件式組裝爆炸模型).

Displays the exact axial assembly order (bottom-up rear-loading sequence without glue/solvents):
- Top (`Z = +52.0 mm`)   : `CSL-CAP-201-1` 外旋卡口壓蓋 (drops over Part 1-3 cannula from above)
- Upper-Mid (`Z = +12.0`): `CSL-CAP-201-3` 一體式喇叭口透明混合外管 (passes upward through Part 1-1's Ø4.08 bore)
- Lower-Mid (`Z = -22.0`): `CSL-CAP-201-4` 防脫出底座靜態螺旋混合芯 (inserts upward into Part 1-3's Ø7.64 bell mouth)
- Bottom (`Z = -36.0 mm`): `CSL-CAP-201-2` 雙流道分流密封內座 (presses into Part 1-1's Ø19.70/Ø18.70 retaining lip)
"""
from __future__ import annotations

from cadgen import build123d as bd
from cadgen import glb, step, stl
from mixer_part1_outer_cap import mixer_part1_outer_cap
from mixer_part2_seal_seat import mixer_part2_seal_seat
from mixer_part3_bell_cannula import mixer_part3_bell_cannula
from mixer_part4_helical_core import mixer_part4_helical_core


@step(out="../STEP/mixer_4part_exploded.step")
@stl(out="../STL/mixer_4part_exploded.stl")
@glb(out="../GLB/mixer_4part_exploded.glb")
def mixer_4part_exploded():
    p1 = bd.Pos(0, 0, 52.0) * mixer_part1_outer_cap()
    p1.label = "part1_outer_cap"

    p3 = bd.Pos(0, 0, 12.0) * mixer_part3_bell_cannula()
    p3.label = "part3_bell_cannula"

    p4 = bd.Pos(0, 0, -22.0) * mixer_part4_helical_core()
    p4.label = "part4_helical_core"

    p2 = bd.Pos(0, 0, -36.0) * mixer_part2_seal_seat()
    p2.label = "part2_seal_seat"

    return bd.Compound(
        children=[p1, p3, p4, p2],
        label="mixer_4part_exploded",
    )


if __name__ == "__main__":
    mixer_4part_exploded()
