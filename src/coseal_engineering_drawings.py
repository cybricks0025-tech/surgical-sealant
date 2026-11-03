"""8-Sheet ISO A3 Engineering Drawings derived directly from the 3D STEP models."""
from __future__ import annotations

from pathlib import Path

import cadgen
from cadgen.eng_drawing import Sheet, eng_drawing
from lib import specs as S

_HERE = Path(__file__).resolve().parent
_STEP = _HERE / ".." / "STEP"
_REVS = [
    ("A", "2026-10-28", "VENDOR CONCEPT LAYOUT"),
    ("B", "2026-11-03", "COMPLETE 3D CAD, POKA-YOKE & ISO TOLERANCES"),
]


@eng_drawing(out="../PDF/coseal_iso_engineering_drawings.pdf")
def coseal_engineering_drawings():
    # ==========================================================================
    # SHEET 1: STAGE 3 FULL DISPENSING ASSEMBLY
    # ==========================================================================
    assy = cadgen.read_step(_STEP / "coseal_device_dispense.step")
    s1 = Sheet(
        "A3",
        scale=0.5,
        title="DUAL/SINGLE-BARREL SEALANT MIXING DEVICE - DISPENSE ASSY",
        part_number="CSL-ASSY-001",
        material="MEDICAL COC / PP / SILICONE",
        revision="B",
        author="ANTIGRAVITY CAD",
        general_tolerance="ISO 2768-m",
        revisions=_REVS,
        notes=[
            "STERILIZATION: ETO OR GAMMA COMPATIBLE.",
            "BARREL CAPACITY: 2 X 4.0 ML WORKING (5.0 ML MAX).",
            "POKA-YOKE BAYONET PREVENTS 180-DEG MIS-ASSEMBLY.",
        ],
    )
    top1 = s1.view(assy, "top", at=(165, 236))
    front1 = s1.view(assy, "front", at=(165, 132))
    right1 = s1.view(assy, "right", at=(245, 132))
    _iso1 = s1.view(assy, "iso", at=(345, 180), scale=0.65, label="ISOMETRIC (0.65:1)")
    top1.dim((-23.05, 16.705, 2.0), (23.05, 16.705, 2.0), orientation="h", offset=8)
    top1.dim((-23.05, -16.705, 0.0), (-23.05, 16.705, 0.0), orientation="v", offset=-8)
    front1.dim((-23.05, 0, S.CLIP_INITIAL_Z), (-23.05, 0, 105.60), orientation="v")
    front1.dim((-23.05, 0, 0.0), (-12.80, 0, S.BARREL_TOTAL_LENGTH), orientation="v")
    front1.dim((12.80, 0, S.BARREL_TOTAL_LENGTH), (2.00, 0, 105.60), orientation="v")

    # ==========================================================================
    # SHEET 2: DUAL-BARREL SYRINGE BODY
    # ==========================================================================
    barrel = cadgen.read_step(_STEP / "dual_barrel_body.step")
    s2 = Sheet(
        "A3",
        scale=1.2,
        title="DUAL-BARREL SYRINGE BODY (POKA-YOKE BAYONET)",
        part_number="CSL-PRT-101",
        material="MEDICAL GRADE PP / COC (CLEAR)",
        revision="B",
        author="ANTIGRAVITY CAD",
        general_tolerance="ISO 2768-m",
        revisions=_REVS,
        notes=[
            "ASYMMETRIC BAYONET GAPS: +Y 60 DEG / -Y 20 DEG.",
            "INTERNAL BORE SURFACE FINISH Ra <= 0.4 um.",
            "NOZZLE BORE PITCH 8.00 +-0.03 MM; OD 3.20 / ID 1.80.",
        ],
    )
    top2 = s2.view(barrel, "top", at=(170, 238))
    front2 = s2.view(barrel, "front", at=(170, 134))
    right2 = s2.view(barrel, "right", at=(265, 134))
    _iso2 = s2.view(barrel, "iso", at=(352, 182), scale=1.1, label="ISOMETRIC (1.1:1)")
    top2.dim((-23.05, 16.705, 2.0), (23.05, 16.705, 2.0), orientation="h", offset=16)
    top2.dim((-23.05, -16.705, 0.0), (-23.05, 16.705, 0.0), orientation="v", offset=-10)
    front2.dim((-23.05, 0, 0.0), (-12.80, 0, S.BARREL_TOTAL_LENGTH), orientation="v", offset=-10)
    top2.dim((S.BARREL_X_B, 16.705, 0), (S.BARREL_X_A, 16.705, 0), orientation="h", offset=7, tol=0.05)
    top2.hole((S.BARREL_X_A, 0, 0), S.BARREL_ID, depth=S.BARREL_BORE_CYL_Z, count=2, angle=30, tol=0.05)
    front2.dim((-14.90, 0, 30.0), (14.90, 0, 30.0), orientation="h")
    front2.dim((23.05, 0, 0.0), (23.05, 0, S.FLANGE_THICKNESS), orientation="v")

    # ==========================================================================
    # SHEET 3: PART #1 HELICAL STATIC MIXER CAP
    # ==========================================================================
    mixer = cadgen.read_step(_STEP / "helical_mixer_cap.step")
    s3 = Sheet(
        "A3",
        scale=2.0,
        title="PART 1 - HELICAL STATIC MIXER DUAL-BARREL CAP",
        part_number="CSL-CAP-201",
        material="ABS / SILICONE / CLEAR PC",
        revision="B",
        author="ANTIGRAVITY CAD",
        general_tolerance="ISO 2768-m",
        revisions=_REVS,
        notes=[
            "8-ELEMENT ALTERNATING L/R 180-DEG KENICS MIXER.",
            "SEPARATED CHANNELS CONVERGE AT CANNULA INLET.",
            "SEAL SOCKET MOLDED ID 3.10 +-0.05 MM (INTERFERENCE).",
        ],
    )
    top3, front3, right3, _iso3 = s3.three_views(mixer, gap=40, iso=True)
    front3.overall()
    right3.dim((0.0, -11.00, 0.0), (0.0, 11.00, 0.0), orientation="h")
    front3.dim((-11.00, 0, 0.0), (-3.80, 0, S.MIXER_BODY_LEN), orientation="v")
    front3.dim((3.80, 0, S.MIXER_BODY_LEN), (2.00, 0, S.MIXER_CAP_TOTAL_LEN), orientation="v")
    top3.diameter((0.0, 0.0, S.MIXER_CAP_TOTAL_LEN), 2.00, angle=45)

    # ==========================================================================
    # SHEET 4: PART #2 LUER RECONSTITUTION TRANSFER CAP
    # ==========================================================================
    luer = cadgen.read_step(_STEP / "luer_transfer_cap.step")
    s4 = Sheet(
        "A3",
        scale=2.0,
        title="PART 2 - LUER RECONSTITUTION SINGLE-BARREL CAP",
        part_number="CSL-CAP-202",
        material="MEDICAL PP + TPE / PC",
        revision="B",
        author="ANTIGRAVITY CAD",
        general_tolerance="ISO 2768-m",
        revisions=_REVS,
        notes=[
            "FEMALE LUER-LOCK PER ISO 80369-7 (6% TAPER).",
            "PORT A (+4.00 MM) OPEN; PORT B (-4.00 MM) BLIND.",
            "OUTER RING ROTATES 65 DEG AROUND STATIONARY INSERT.",
        ],
    )
    top4, front4, right4, _iso4 = s4.three_views(luer, gap=42, iso=True)
    top4.overall()
    front4.overall()
    front4.dim((-S.CAP_LUG_SPAN / 2.0, 0, 0.0), (S.CAP_LUG_SPAN / 2.0, 0, 0.0), orientation="h", tol=0.05)
    front4.dim((-15.00, 0, S.LUER_SKIRT_LEN), (-15.00, 0, 9.00), orientation="v")
    front4.dim((S.NOZZLE_X_A + 3.90, 0, 9.00), (S.NOZZLE_X_A + 3.90, 0, S.LUER_CAP_TOTAL_LEN), orientation="v")
    top4.dim((0.0, 0.0, 9.00), (S.NOZZLE_X_A, 0.0, S.LUER_CAP_TOTAL_LEN), orientation="h", tol=0.03)
    top4.diameter((S.NOZZLE_X_A, 0.0, S.LUER_CAP_TOTAL_LEN), S.LUER_THREAD_OD / 2.0, angle=35)

    # ==========================================================================
    # SHEET 5: PART #3 INITIAL PLUG VALVE CAP
    # ==========================================================================
    plug = cadgen.read_step(_STEP / "initial_plug_cap.step")
    s5 = Sheet(
        "A3",
        scale=2.0,
        title="PART 3 - INITIAL PLUG VALVE SEALING CAP",
        part_number="CSL-CAP-203",
        material="MEDICAL PP + BUTYL / SILICONE",
        revision="B",
        author="ANTIGRAVITY CAD",
        general_tolerance="ISO 2768-m",
        revisions=_REVS,
        notes=[
            "DUAL BLIND ELASTOMER PLUGS SEAL BOTH BARRELS.",
            "OUTER CAP SPINS FREELY AROUND STATIONARY PLUG PAD.",
            "MOLDED SOCKET ID 3.10 +-0.05 MM; BORE PIN OD 1.86 MM.",
        ],
    )
    top5, front5, right5, _iso5 = s5.three_views(plug, gap=36, iso=True)
    front5.overall()
    right5.overall()
    right5.dim((0, 2.00, S.PLUG_CAP_BODY_LEN), (0, 2.00, S.PLUG_CAP_TOTAL_LEN), orientation="v")
    right5.dim((0, -2.00, S.PLUG_CAP_TOTAL_LEN), (0, 2.00, S.PLUG_CAP_TOTAL_LEN), orientation="h")
    front5.dim((-11.00, 0, 0.0), (-11.00, 0, S.PLUG_CAP_BODY_LEN), orientation="v")

    # ==========================================================================
    # SHEET 6: PART #4 SINGLE/DUAL PLUNGER SELECTOR CLIP
    # ==========================================================================
    clip = cadgen.read_step(_STEP / "plunger_clip.step")
    s6 = Sheet(
        "A3",
        scale=3.0,
        title="PART 4 - SINGLE/DUAL PLUNGER SELECTOR CLIP",
        part_number="CSL-PRT-104",
        material="MEDICAL POM (DELRIN) / TOUGHENED PP",
        revision="B",
        author="ANTIGRAVITY CAD",
        general_tolerance="ISO 2768-m",
        revisions=_REVS,
        notes=[
            "CAPTIVE PIVOT ON BARREL B (-7.20 MM) ROTATES 90 DEG.",
            "SIDE SNAP C-JAW ON BARREL A (+7.20 MM): 0.90 MM DETENT.",
            "INTERNAL SLOT WIDTH 1.80 +0.10/-0.00 MM FOR 1.60 MM DISC.",
        ],
    )
    top6, front6, right6, _iso6 = s6.three_views(clip, gap=34, iso=True)
    top6.overall()
    front6.overall()
    top6.dim((S.BARREL_X_B, 0, S.CLIP_THICKNESS), (S.BARREL_X_A, 0, S.CLIP_THICKNESS), orientation="h", tol=0.05)
    top6.hole((S.BARREL_X_B, 0, S.CLIP_THICKNESS), S.CLIP_PIVOT_HOLE_DIA, depth=2.60, angle=135)
    top6.dim(
        (S.BARREL_X_A - S.CLIP_SNAP_THROAT / 2.0, -8.20, 2.0),
        (S.BARREL_X_A + S.CLIP_SNAP_THROAT / 2.0, -8.20, 2.0),
        orientation="h",
        tol=0.05,
    )

    # ==========================================================================
    # SHEET 7: CRUCIFORM PLUNGER ROD
    # ==========================================================================
    rod = cadgen.read_step(_STEP / "plunger_rod.step")
    s7 = Sheet(
        "A3",
        scale=1.2,
        title="CRUCIFORM PLUNGER ROD (DUAL-BARREL DRIVE)",
        part_number="CSL-PRT-102",
        material="MEDICAL GRADE PP / ABS",
        revision="B",
        author="ANTIGRAVITY CAD",
        general_tolerance="ISO 2768-m",
        revisions=_REVS,
        notes=[
            "QTY PER SYSTEM: 2 PCS (IDENTICAL FOR BARREL A & B).",
            "THUMB DISC 12.80 X 1.60 MM MATES WITH SELECTOR CLIP #4.",
            "NECK JOURNAL DIA 6.20 MM X 3.20 MM LENGTH.",
        ],
    )
    top7 = s7.view(rod, "top", at=(175, 240))
    front7 = s7.view(rod, "front", at=(175, 145))
    right7 = s7.view(rod, "right", at=(255, 145))
    _iso7 = s7.view(rod, "iso", at=(348, 182), scale=1.2, label="ISOMETRIC (1.2:1)")
    front7.overall()
    top7.diameter((0, 0, 0), S.PLUNGER_DISC_OD / 2.0, angle=45)
    front7.dim((-6.40, 0, 0.0), (-5.30, 0, S.PLUNGER_TOTAL_LEN), orientation="v", tol=0.10)
    front7.dim((6.40, 0, 0.0), (3.10, 0, S.PLUNGER_DISC_THICK + S.PLUNGER_NECK_LEN), orientation="v")

    # ==========================================================================
    # SHEET 8: TRIPLE-RIB MEDICAL ELASTOMER STOPPER
    # ==========================================================================
    stopper = cadgen.read_step(_STEP / "elastomer_stopper.step")
    s8 = Sheet(
        "A3",
        scale=5.0,
        title="TRIPLE-RIB ELASTOMER PISTON STOPPER",
        part_number="CSL-PRT-103",
        material="MEDICAL BROMOBUTYL / SILICONE (SHORE A 55)",
        revision="B",
        author="ANTIGRAVITY CAD",
        general_tolerance="ISO 2768-m",
        revisions=_REVS,
        notes=[
            "QTY PER SYSTEM: 2 PCS (MEDICAL SILICONE OIL COATED).",
            "MOLDED SEALING RIB OD 12.50 +-0.10 MM FOR 12.20 BORE.",
            "CONICAL TIP MINIMIZES RESIDUAL HOLD-UP VOLUME.",
        ],
    )
    top8, front8, right8, _iso8 = s8.three_views(stopper, gap=36, iso=True)
    front8.overall()
    top8.diameter((0, 0, 0), S.STOPPER_OD / 2.0, angle=45)
    front8.dim((-6.08, 0, 0.0), (-6.08, 0, 5.20), orientation="v")

    return [s1, s2, s3, s4, s5, s6, s7, s8]


if __name__ == "__main__":
    coseal_engineering_drawings()
