"""Complete 3-Stage System Overview Assembly (三階段完整雙單管混合系統總成與爆炸展示).

Displays all three clinical configurations side-by-side along Y = 0, -68, -136 mm
(matching the vendor's system presentation layout) plus standalone exploded caps:
- Stage 3 (Top, Y = +68 mm): Synchronized Dual-Barrel Dispensing with #1 Helical Mixer Cap
- Stage 2 (Middle, Y = 0 mm): Single-Barrel Reconstitution with #2 Luer Transfer Cap,
  90-deg swung #4 Selector Clip, unlocked Plunger A, and attached Powder Syringe
- Stage 1 (Bottom, Y = -68 mm): Sterile Storage & Shipping with #3 Initial Plug Valve Cap
"""
from __future__ import annotations

from cadgen import build123d as bd
from cadgen import glb, step
from dual_barrel_body import dual_barrel_body
from elastomer_stopper import elastomer_stopper
from helical_mixer_cap import helical_mixer_cap
from initial_plug_cap import initial_plug_cap
from lib import specs as S
from luer_transfer_cap import luer_transfer_cap
from plunger_clip import plunger_clip
from plunger_rod import plunger_rod
from powder_syringe import powder_syringe

PLUNGER_Z0 = S.CLIP_INITIAL_Z + S.CLIP_BACK_WALL + 0.10
STOPPER_Z0 = PLUNGER_Z0 + S.PLUNGER_TOTAL_LEN + 0.04


def _make_base_syringe_unit(
    prefix: str,
    stroke_a: float = 0.0,
    stroke_b: float = 0.0,
    clip_swung_90: bool = False,
) -> list[bd.Shape]:
    barrel = dual_barrel_body().moved(bd.Location((0, 0, 0)))
    barrel.label = f"{prefix}_barrel"

    rod_proto = plunger_rod()
    stop_proto = elastomer_stopper()

    pa = bd.Pos(S.BARREL_X_A, 0, PLUNGER_Z0 + stroke_a) * rod_proto
    pa.label = f"{prefix}_plunger_a"
    sa = bd.Pos(S.BARREL_X_A, 0, STOPPER_Z0 + stroke_a) * stop_proto
    sa.label = f"{prefix}_stopper_a"

    pb = bd.Pos(S.BARREL_X_B, 0, PLUNGER_Z0 + stroke_b) * rod_proto
    pb.label = f"{prefix}_plunger_b"
    sb = bd.Pos(S.BARREL_X_B, 0, STOPPER_Z0 + stroke_b) * stop_proto
    sb.label = f"{prefix}_stopper_b"

    clip_raw = plunger_clip()
    if clip_swung_90:
        # Rotate -90 deg about Plunger B axis (X = -7.20, Y = 0) so clip hangs clear of Plunger A!
        clip = (
            bd.Pos(S.BARREL_X_B, 0, S.CLIP_INITIAL_Z + stroke_b)
            * bd.Rot(0, 0, -90)
            * bd.Pos(-S.BARREL_X_B, 0, 0)
            * clip_raw
        )
    else:
        clip = bd.Pos(0, 0, S.CLIP_INITIAL_Z + stroke_b) * clip_raw
    clip.label = f"{prefix}_clip"

    return [barrel, pa, sa, pb, sb, clip]


@step(out="../STEP/coseal_system_overview.step")
@glb(out="../GLB/coseal_system_overview.glb")
def coseal_system_overview():
    # 1. Stage 3 (Y = +65 mm): Dual-Barrel Helical Mixing & Dispensing
    s3_parts = _make_base_syringe_unit("stage3", stroke_a=0.0, stroke_b=0.0, clip_swung_90=False)
    s3_cap = bd.Pos(0, 0, S.CAP_SEAT_Z) * helical_mixer_cap()
    s3_cap.label = "stage3_mixer_cap"
    stage3 = bd.Pos(0, 65.0, 0) * bd.Compound(children=[*s3_parts, s3_cap], label="stage3_dispense")
    stage3.label = "stage3_dispense"

    # 2. Stage 2 (Y = 0 mm): Single-Barrel Reconstitution with Powder Syringe & Swung Clip
    # Show Plunger A pushed 12 mm forward during active back-and-forth dissolution!
    s2_parts = _make_base_syringe_unit("stage2", stroke_a=12.0, stroke_b=0.0, clip_swung_90=True)
    s2_cap = bd.Pos(0, 0, S.CAP_SEAT_Z) * luer_transfer_cap()
    s2_cap.label = "stage2_luer_cap"
    # Powder syringe threaded onto eccentric Female Luer port at X = +4.00 mm
    pwd_syr = bd.Pos(S.NOZZLE_X_A, 0, S.CAP_SEAT_Z + S.LUER_CAP_TOTAL_LEN - 3.80) * powder_syringe()
    pwd_syr.label = "stage2_powder_syringe"
    stage2 = bd.Compound(children=[*s2_parts, s2_cap, pwd_syr], label="stage2_reconstitution")

    # 3. Stage 1 (Y = -65 mm): Initial Storage & Sterile Seal with Cap #3
    s1_parts = _make_base_syringe_unit("stage1", stroke_a=0.0, stroke_b=0.0, clip_swung_90=False)
    s1_cap = bd.Pos(0, 0, S.CAP_SEAT_Z) * initial_plug_cap()
    s1_cap.label = "stage1_plug_cap"
    stage1 = bd.Pos(0, -65.0, 0) * bd.Compound(children=[*s1_parts, s1_cap], label="stage1_storage")
    stage1.label = "stage1_storage"

    # 4. Exploded Reference Caps on Display Column (Z = 185 mm) for instant inspection
    disp_c1 = bd.Pos(0, 65.0, 185.0) * helical_mixer_cap()
    disp_c1.label = "display_helical_mixer_cap"
    disp_c2 = bd.Pos(0, 0.0, 185.0) * luer_transfer_cap()
    disp_c2.label = "display_luer_transfer_cap"
    disp_c3 = bd.Pos(0, -65.0, 185.0) * initial_plug_cap()
    disp_c3.label = "display_initial_plug_cap"

    return bd.Compound(
        children=[stage1, stage2, stage3, disp_c1, disp_c2, disp_c3],
        label="coseal_system_overview",
    )


if __name__ == "__main__":
    coseal_system_overview()
