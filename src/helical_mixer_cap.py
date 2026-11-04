"""Part #1 Assembly (CSL-CAP-201): 4-Part Helical Static Mixer Cap (螺旋混合雙管蓋四件式總成).

True 4-part injection-molded subassembly matching vendor CAD (`混合頭.png`) & medical DFM:
1. `CSL-CAP-201-1` (`mixer_part1_outer_cap`)  : Olive-green ribbed Poka-Yoke bayonet retaining cap (Ø22.00 x 14.87 mm)
2. `CSL-CAP-201-2` (`mixer_part2_seal_seat`)  : Brown dual-sleeve manifold elastomer seal seat (Ø19.60 x 7.40 mm @ Z=1.60)
3. `CSL-CAP-201-3` (`mixer_part3_bell_cannula`): Clear 1-piece bell-mouth mixing cannula (Ø10.20 -> Ø4.00/Ø3.00 x 32.56 mm @ Z=9.04)
4. `CSL-CAP-201-4` (`mixer_part4_helical_core`): Maroon 9-element Kenics helical mixer core with Ø4.40 anti-ejection collar (28.00 mm @ Z=9.60)
"""
from __future__ import annotations

from cadgen import build123d as bd
from cadgen import glb, step, stl
from lib import specs as S
from mixer_part1_outer_cap import mixer_part1_outer_cap
from mixer_part2_seal_seat import mixer_part2_seal_seat
from mixer_part3_bell_cannula import mixer_part3_bell_cannula
from mixer_part4_helical_core import mixer_part4_helical_core


def _build_helical_mixer_cap() -> bd.Shape:
    p1 = mixer_part1_outer_cap()
    p1.label = "part1_outer_cap"

    p2 = bd.Pos(0, 0, S.MIXER_P2_Z0) * mixer_part2_seal_seat()
    p2.label = "part2_seal_seat"

    p3 = bd.Pos(0, 0, S.MIXER_P3_Z0) * mixer_part3_bell_cannula()
    p3.label = "part3_bell_cannula"

    p4 = bd.Pos(0, 0, S.MIXER_P4_Z0) * mixer_part4_helical_core()
    p4.label = "part4_helical_core"

    return bd.Compound(
        children=[p1, p2, p3, p4],
        label="helical_mixer_cap",
    )


@step(out="../STEP/helical_mixer_cap.step")
@stl(out="../STL/helical_mixer_cap.stl")
@glb(out="../GLB/helical_mixer_cap.glb")
def helical_mixer_cap():
    return _build_helical_mixer_cap()


if __name__ == "__main__":
    helical_mixer_cap()
