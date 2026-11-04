"""Export individual part/subassembly GLB files for the GitHub Pages 3D Web Portal."""
from __future__ import annotations

import sys
from pathlib import Path

from cadgen import glb

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from dual_barrel_body import dual_barrel_body  # noqa: E402
from elastomer_stopper import elastomer_stopper  # noqa: E402
from helical_mixer_cap import helical_mixer_cap  # noqa: E402
from initial_plug_cap import initial_plug_cap  # noqa: E402
from luer_transfer_cap import luer_transfer_cap  # noqa: E402
from mixer_4part_exploded import mixer_4part_exploded  # noqa: E402
from mixer_part1_outer_cap import mixer_part1_outer_cap  # noqa: E402
from mixer_part2_seal_seat import mixer_part2_seal_seat  # noqa: E402
from mixer_part3_bell_cannula import mixer_part3_bell_cannula  # noqa: E402
from mixer_part4_helical_core import mixer_part4_helical_core  # noqa: E402
from plunger_clip import plunger_clip  # noqa: E402
from plunger_rod import plunger_rod  # noqa: E402
from powder_syringe import powder_syringe  # noqa: E402


@glb(out="../GLB/dual_barrel_body.glb")
def _glb_barrel():
    return dual_barrel_body()


@glb(out="../GLB/plunger_rod.glb")
def _glb_rod():
    return plunger_rod()


@glb(out="../GLB/elastomer_stopper.glb")
def _glb_stopper():
    return elastomer_stopper()


@glb(out="../GLB/plunger_clip.glb")
def _glb_clip():
    return plunger_clip()


@glb(out="../GLB/helical_mixer_cap.glb")
def _glb_mixer():
    return helical_mixer_cap()


@glb(out="../GLB/mixer_part1_outer_cap.glb")
def _glb_mixer_p1():
    return mixer_part1_outer_cap()


@glb(out="../GLB/mixer_part2_seal_seat.glb")
def _glb_mixer_p2():
    return mixer_part2_seal_seat()


@glb(out="../GLB/mixer_part3_bell_cannula.glb")
def _glb_mixer_p3():
    return mixer_part3_bell_cannula()


@glb(out="../GLB/mixer_part4_helical_core.glb")
def _glb_mixer_p4():
    return mixer_part4_helical_core()


@glb(out="../GLB/mixer_4part_exploded.glb")
def _glb_mixer_exploded():
    return mixer_4part_exploded()


@glb(out="../GLB/luer_transfer_cap.glb")
def _glb_luer():
    return luer_transfer_cap()


@glb(out="../GLB/initial_plug_cap.glb")
def _glb_plug():
    return initial_plug_cap()


@glb(out="../GLB/powder_syringe.glb")
def _glb_powder():
    return powder_syringe()


if __name__ == "__main__":
    _glb_barrel()
    _glb_rod()
    _glb_stopper()
    _glb_clip()
    _glb_mixer()
    _glb_mixer_p1()
    _glb_mixer_p2()
    _glb_mixer_p3()
    _glb_mixer_p4()
    _glb_mixer_exploded()
    _glb_luer()
    _glb_plug()
    _glb_powder()
    print("Exported all 13 modular GLB assets to GLB/")
