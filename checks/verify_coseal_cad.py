"""Deterministic geometry, dimension, topology, and collision verification for the CoSeal-inspired device."""
from __future__ import annotations

import sys
from itertools import combinations
from pathlib import Path

from cadgen import read_scene, read_step
from cadgen.geometry import overlap_volume, topology_errors

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from lib import specs as S  # noqa: E402


def assert_close(name: str, actual: float, expected: float, tol: float = 0.05) -> None:
    err = abs(actual - expected)
    status = "PASS" if err <= tol else "FAIL"
    print(f"  [{status}] {name:42s}: actual={actual:8.3f} mm, expected={expected:8.3f} mm (err={err:.4f})")
    if err > tol:
        raise AssertionError(f"{name}: {actual:.3f} != {expected:.3f} (tol {tol})")


def check_part_envelope_and_topology(step_rel: str, expected_xyz: tuple[float, float, float]) -> None:
    path = ROOT / step_rel
    print(f"\n=== Checking {step_rel} ===")
    shape = read_step(path)
    solids = list(shape.solids())
    print(f"  Solids count: {len(solids)}")
    assert len(solids) >= 1, f"No solids in {step_rel}"

    for i, s in enumerate(solids):
        assert s.is_valid, f"Solid {i} in {step_rel} failed BRepCheck"
        assert s.volume > 0.0, f"Solid {i} in {step_rel} has non-positive volume {s.volume}"
        errs = topology_errors(s)
        assert len(errs) == 0, f"Topology errors in {step_rel} solid {i}: {errs}"

    bb = shape.bounding_box()
    sx, sy, sz = bb.size.X, bb.size.Y, bb.size.Z
    assert_close(f"{path.stem} X-span", sx, expected_xyz[0])
    assert_close(f"{path.stem} Y-span", sy, expected_xyz[1])
    assert_close(f"{path.stem} Z-span", sz, expected_xyz[2])


def check_assembly_overlaps(step_rel: str, max_overlap_mm3: float = 0.01) -> None:
    path = ROOT / step_rel
    scene = read_scene(path)
    bodies = []
    for leaf in scene.leaves():
        for solid in leaf.shape().solids():
            bodies.append((leaf.label or leaf.ref, solid))
    print(f"\n=== Pairwise Interference Check: {step_rel} ({len(bodies)} solids) ===")
    failures = []
    tested = 0
    for (la, sa), (lb, sb) in combinations(bodies, 2):
        # Fast conservative AABB filter first
        ba = sa.bounding_box(optimal=False)
        bb = sb.bounding_box(optimal=False)
        if (
            ba.max.X < bb.min.X or bb.max.X < ba.min.X
            or ba.max.Y < bb.min.Y or bb.max.Y < ba.min.Y
            or ba.max.Z < bb.min.Z or bb.max.Z < ba.min.Z
        ):
            tested += 1
            continue
        vol = overlap_volume(sa, sb)
        tested += 1
        if vol > max_overlap_mm3:
            failures.append((la, lb, round(vol, 4)))
    print(f"  Tested pairs: {tested}, max_limit={max_overlap_mm3} mm^3, overlaps={failures}")
    if failures:
        raise AssertionError(f"Interference detected in {step_rel}: {failures}")


def main() -> None:
    # 1. Verify individual parts against exact vendor specs
    check_part_envelope_and_topology(
        "STEP/dual_barrel_body.step",
        (S.FLANGE_SPAN_X, S.FLANGE_SPAN_Y, S.BARREL_TOTAL_LENGTH),  # 46.10 x 33.41 x 69.40
    )
    check_part_envelope_and_topology(
        "STEP/plunger_clip.step",
        (S.CLIP_SPAN_X, S.CLIP_WIDTH_Y, S.CLIP_THICKNESS),          # 30.00 x 16.40 x 4.00
    )

    # 1b. Verify all 4 standalone sub-parts of #1 Helical Static Mixer Cap
    check_part_envelope_and_topology(
        "STEP/mixer_part1_outer_cap.step",
        (S.CAP_LUG_SPAN, S.CAP_BODY_OD, S.MIXER_BODY_LEN),          # 23.96 x 22.00 x 14.87
    )
    check_part_envelope_and_topology(
        "STEP/mixer_part2_seal_seat.step",
        (S.MIXER_P2_RIM_OD, S.MIXER_P2_RIM_OD, S.MIXER_P2_HEIGHT),  # 19.60 x 19.60 x 7.40
    )
    check_part_envelope_and_topology(
        "STEP/mixer_part3_bell_cannula.step",
        (S.MIXER_P3_BELL_OD, S.MIXER_P3_BELL_OD, S.MIXER_P3_LEN),   # 10.20 x 10.20 x 32.56
    )
    check_part_envelope_and_topology(
        "STEP/mixer_part4_helical_core.step",
        (S.MIXER_P4_COLLAR_OD, S.MIXER_P4_COLLAR_OD, S.MIXER_P4_LEN),  # 4.40 x 4.40 x 28.00
    )
    check_part_envelope_and_topology(
        "STEP/helical_mixer_cap.step",
        (S.CAP_LUG_SPAN, S.CAP_BODY_OD, S.MIXER_CAP_TOTAL_LEN),     # 23.96 x 22.00 x 41.60
    )
    mixer_solids = list(read_step(ROOT / "STEP/helical_mixer_cap.step").solids())
    assert len(mixer_solids) == 4, f"Expected exact 4 solids in helical_mixer_cap.step, got {len(mixer_solids)}"
    print(f"  [PASS] helical_mixer_cap exact sub-part solid count = {len(mixer_solids)}")
    check_part_envelope_and_topology(
        "STEP/luer_transfer_cap.step",
        (S.LUER_FLANGE_OD, S.LUER_FLANGE_OD, S.LUER_CAP_TOTAL_LEN), # 30.00 x 30.00 x 15.00
    )
    check_part_envelope_and_topology(
        "STEP/initial_plug_cap.step",
        (S.CAP_LUG_SPAN, S.CAP_BODY_OD, S.PLUG_CAP_TOTAL_LEN),      # 23.96 x 22.00 x 17.00
    )

    # 2. Verify full Stage 3 Dispensing Assembly (166.60 mm exact overall length & 36.20 mm exposed mixer)
    check_part_envelope_and_topology(
        "STEP/coseal_device_dispense.step",
        (S.FLANGE_SPAN_X, S.FLANGE_SPAN_Y, S.SYSTEM_TOTAL_LENGTH),  # 46.10 x 33.41 x 166.60
    )
    disp_scene = read_scene(ROOT / "STEP/coseal_device_dispense.step")
    barrel_bb = disp_scene.resolve("#barrel").shape().bounding_box()
    mixer_bb = disp_scene.resolve("#mixer_cap").shape().bounding_box()
    exposed_mixer = mixer_bb.max.Z - barrel_bb.max.Z
    assert_close("Mixer exposed past barrel collar", exposed_mixer, S.MIXER_EXPOSED_LENGTH)

    # 3. Verify 0.00 mm^3 solid interference across subassemblies & full dispensing assembly
    check_assembly_overlaps("STEP/helical_mixer_cap.step")
    check_assembly_overlaps("STEP/luer_transfer_cap.step")
    check_assembly_overlaps("STEP/initial_plug_cap.step")
    check_assembly_overlaps("STEP/coseal_device_dispense.step")

    print("\nALL GEOMETRY, DIMENSION, TOPOLOGY, AND CLEARANCE CHECKS PASSED!")


if __name__ == "__main__":
    main()
