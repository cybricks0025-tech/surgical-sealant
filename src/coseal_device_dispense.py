"""Stage 3 Full Dispensing Assembly (雙管同步注射成膠組態, 166.60 mm overall length) with interactive Kinematics & Animation."""
from __future__ import annotations

import cadgen
from cadgen import build123d as bd
from cadgen import glb, step, stl, threemf
from dual_barrel_body import dual_barrel_body
from elastomer_stopper import elastomer_stopper
from helical_mixer_cap import helical_mixer_cap
from lib import specs as S
from plunger_clip import plunger_clip
from plunger_rod import plunger_rod

PLUNGER_Z0 = S.CLIP_INITIAL_Z + S.CLIP_BACK_WALL + 0.10  # -61.00 + 1.50 = -59.50 mm
STOPPER_Z0 = PLUNGER_Z0 + S.PLUNGER_TOTAL_LEN + 0.04     # -59.50 + 72.30 + 0.04 = 12.84 mm

KINEMATICS = {
    "mates": [
        cadgen.slider(
            "stroke_b",
            parent="#barrel",
            child="#plunger_b_group",
            origin=(S.BARREL_X_B, 0.0, 0.0),
            direction=(0.0, 0.0, 1.0),
            limits=(0.0, 38.5),
        ),
        cadgen.slider(
            "stroke_a",
            parent="#barrel",
            child="#plunger_a_group",
            origin=(S.BARREL_X_A, 0.0, 0.0),
            direction=(0.0, 0.0, 1.0),
            limits=(0.0, 38.5),
        ),
        cadgen.revolute(
            "clip_swing",
            parent="#plunger_b_group",
            child="#selector_clip",
            origin=(S.BARREL_X_B, 0.0, 0.0),
            direction=(0.0, 0.0, -1.0),
            limits=(0.0, 90.0),
        ),
    ],
    "couplings": [
        cadgen.couple("dual_inject", {"stroke_a": 1.0, "stroke_b": 1.0}, limits=(0.0, 38.5)),
    ],
    "poses": {
        "ready_to_inject": {"dual_inject": 0.0, "clip_swing": 0.0},
        "half_injected": {"dual_inject": 19.25, "clip_swing": 0.0},
        "fully_injected": {"dual_inject": 38.5, "clip_swing": 0.0},
        "single_barrel_unlocked": {"dual_inject": 0.0, "clip_swing": 90.0},
    },
}

ANIMATION = r"""
export const clips = {
  clinical_workflow: {
    label: "Dual-Syringe Lock & Synchronized Dispensing",
    duration: 8,
    loop: true,
    update(t, m) {
      // 0..2s: Swing selector clip from 90 deg (unlocked) -> 0 deg (locked across both plungers)
      // 2..6s: Synchronized 1:1 dual-plunger dispensing stroke (0 -> 38.5 mm)
      // 6..8s: Smooth reset
      let swing = 0;
      let stroke = 0;
      if (t < 2.0) {
        const u = t / 2.0;
        const s = 0.5 - 0.5 * Math.cos(Math.PI * u);
        swing = 90.0 * (1.0 - s);
      } else if (t < 6.0) {
        const u = (t - 2.0) / 4.0;
        const s = 0.5 - 0.5 * Math.cos(Math.PI * u);
        stroke = 38.5 * s;
      } else {
        const u = (t - 6.0) / 2.0;
        const s = 0.5 - 0.5 * Math.cos(Math.PI * u);
        stroke = 38.5 * (1.0 - s);
        swing = 90.0 * s;
      }
      m.get("plunger_a").translate([0, 0, stroke]);
      m.get("stopper_a").translate([0, 0, stroke]);
      m.get("plunger_b").translate([0, 0, stroke]);
      m.get("stopper_b").translate([0, 0, stroke]);
      m.get("selector_clip")
        .rotate([0, 0, -1], swing, [-7.2, 0, 0])
        .translate([0, 0, stroke]);
    },
  },
};
"""


@step(out="../STEP/coseal_device_dispense.step", kinematics=KINEMATICS, animation=ANIMATION)
@stl(out="../STL/coseal_device_dispense.stl")
@threemf(out="../3MF/coseal_device_dispense.3mf")
@glb(out="../GLB/coseal_device_dispense.glb")
def coseal_device_dispense():
    barrel = dual_barrel_body()
    barrel.label = "barrel"

    rod_proto = plunger_rod()
    stop_proto = elastomer_stopper()

    plunger_a = bd.Pos(S.BARREL_X_A, 0, PLUNGER_Z0) * rod_proto
    plunger_a.label = "plunger_a"
    stopper_a = bd.Pos(S.BARREL_X_A, 0, STOPPER_Z0) * stop_proto
    stopper_a.label = "stopper_a"
    plunger_a_group = bd.Compound(children=[plunger_a, stopper_a], label="plunger_a_group")

    plunger_b = bd.Pos(S.BARREL_X_B, 0, PLUNGER_Z0) * rod_proto
    plunger_b.label = "plunger_b"
    stopper_b = bd.Pos(S.BARREL_X_B, 0, STOPPER_Z0) * stop_proto
    stopper_b.label = "stopper_b"
    plunger_b_group = bd.Compound(children=[plunger_b, stopper_b], label="plunger_b_group")

    clip = bd.Pos(0, 0, S.CLIP_INITIAL_Z) * plunger_clip()
    clip.label = "selector_clip"

    mixer = bd.Pos(0, 0, S.CAP_SEAT_Z) * helical_mixer_cap()
    mixer.label = "mixer_cap"

    return bd.Compound(
        children=[barrel, plunger_a_group, plunger_b_group, clip, mixer],
        label="coseal_device_dispense",
    )


if __name__ == "__main__":
    coseal_device_dispense()
