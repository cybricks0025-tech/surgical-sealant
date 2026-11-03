"""Master parametric dimensions for the Dual/Single-Barrel Surgical Sealant Mixing Device.

All vendor-specified dimensions from `20261028雙單管混合裝置-尺寸.pdf` are preserved 1:1.
Previously unspecified mating, sealing, Luer (ISO 80369-7), Poka-Yoke bayonet, and
internal flow-channel dimensions are explicitly defined here so all 3D models and
2D engineering drawings stay 100% synchronized.

Coordinate convention (millimeters):
- X: Dual-barrel pairing axis (+X = Barrel A [S-buffer / PEG dissolution], -X = Barrel B [T-buffer])
- Y: Transverse axis (bayonet drop-in axis & finger-ear axis)
- Z: Longitudinal dispensing axis (Barrel flange back face = Z 0.00 in barrel coordinates)
"""

# ==============================================================================
# 1. SYSTEM & ASSEMBLY OVERALL DIMENSIONS (Vendor PDF exact match)
# ==============================================================================
SYSTEM_TOTAL_LENGTH = 166.60      # Overall length in Stage 3 (Clip rear to Mixer tip)
BARREL_TOTAL_LENGTH = 69.40       # Flange back face (Z=0) to collar front rim (Z=69.40)
MIXER_EXPOSED_LENGTH = 36.20      # Exposed length of Cap #1 past collar rim (69.40 -> 105.60)
CLIP_INITIAL_Z = -61.00           # Rear face of plunger clip in initial filled state (-61.00 + 166.60 = 105.60)

# ==============================================================================
# 2. DUAL-BARREL SYRINGE BODY (雙腔針筒本體)
# ==============================================================================
BARREL_PITCH = 14.40              # Center-to-center spacing between Barrel A (+7.20) & Barrel B (-7.20)
BARREL_X_A = BARREL_PITCH / 2.0   # +7.20 mm (Active reconstitution barrel: S-buffer + PEG)
BARREL_X_B = -BARREL_PITCH / 2.0  # -7.20 mm (Buffer barrel: T-buffer)
BARREL_ID = 12.20                 # Inner bore diameter (5.0 mL max / 4.0 mL working volume per barrel)
BARREL_OD = 15.40                 # Outer barrel diameter (wall = 1.60 mm; total dual span = 29.80 mm)
BARREL_BORE_CYL_Z = 58.50         # End of cylindrical bore before conical roof
BARREL_BORE_TOP_Z = 61.00         # Apex of internal barrel roof

# 4-Lobed Ergonomic Finger Flange (指翼)
FLANGE_SPAN_X = 46.10             # Vendor spec: 46.10 mm across main wings
FLANGE_SPAN_Y = 33.41             # Vendor spec: 33.41 mm across transverse finger ears
FLANGE_WING_WIDTH_Y = 17.60       # Width of main X-wings
FLANGE_THICKNESS = 2.00           # Axial thickness (Z = 0.00 .. 2.00)

# Front Recessed Deck, Dual Male Nozzles & Poka-Yoke Bayonet Collar
DECK_FLOOR_Z = 63.80              # Recessed front deck floor (0.20 mm clearance below cap skirt @ Z=64.00)
CAP_SEAT_Z = 64.00                # Datum Z where caps sit when bayonet-locked (69.40 - 5.40 = 64.00)
COLLAR_INSERT_DEPTH = 5.40        # 69.40 - 64.00 = 5.40 mm cap insertion depth

NOZZLE_PITCH = 8.00               # Eccentric inward-converged nozzle pitch (+4.00 / -4.00 mm)
NOZZLE_X_A = NOZZLE_PITCH / 2.0   # +4.00 mm (Matches eccentric Luer port offset!)
NOZZLE_X_B = -NOZZLE_PITCH / 2.0  # -4.00 mm
NOZZLE_OD = 3.20                  # Male nozzle outer diameter
NOZZLE_ID = 1.80                  # Male nozzle bore diameter
NOZZLE_HEIGHT = 3.50              # Protrusion above DECK_FLOOR_Z (Z = 63.80 .. 67.30)

COLLAR_OD = 25.60                 # Outer diameter of split bayonet collar crescents
COLLAR_ID = 22.20                 # Inner bore of collar (0.20 mm clearance for Ø22.00 caps)
BAYONET_GROOVE_DIA = 24.30        # Undercut groove diameter for Ø23.96 bayonet lugs
BAYONET_GROOVE_HEIGHT = 2.10      # Undercut slot Z span (Z = 63.80 .. 65.90)
CAP_BODY_OD = 22.00               # Vendor spec: Ø22.00 mm cap body diameter
CAP_LUG_SPAN = 23.96              # Vendor spec: 23.96 mm across bayonet locking lugs
CAP_LUG_HEIGHT = 1.80             # Axial thickness of bayonet lugs

# Poka-Yoke Asymmetric Lug Angles (prevents 180-deg mis-assembly of Cap #2!)
LUG_WIDE_DEG = 26.0               # Wide lug (+X locked / +Y entry)
LUG_NARROW_DEG = 15.0             # Narrow lug (-X locked / -Y entry)

# ==============================================================================
# 3. PLUNGER ROD & ELASTOMER STOPPER (十字推桿與醫療級活塞)
# ==============================================================================
STOPPER_OD = 12.16                # CAD nominal fit in Ø12.20 bore (drawing specifies Ø12.50±0.10 Interference)
STOPPER_LENGTH = 7.00             # Axial length of purple elastomer stopper
STOPPER_INITIAL_Z = 12.90         # Rear face of stopper at initial 4.0 mL fill state (front @ 19.90)

PLUNGER_RIB_SPAN = 11.20          # Cruciform (+) shaft outer diameter
PLUNGER_RIB_THICK = 1.80          # Cruciform web thickness
PLUNGER_SHAFT_LENGTH = 70.70      # From front face of thumb disc to front pusher plate
PLUNGER_DISC_OD = 12.80           # Rear thumb disc diameter
PLUNGER_DISC_THICK = 1.60         # Rear thumb disc thickness (fits 1.80 mm slot in Clip #4)
PLUNGER_NECK_OD = 6.20            # Neck journal diameter behind thumb disc
PLUNGER_NECK_LEN = 3.20           # Neck journal axial length
PLUNGER_TOTAL_LEN = PLUNGER_SHAFT_LENGTH + PLUNGER_DISC_THICK  # 72.30 mm (+ 3.50 mm stopper pin = 75.80 mm)

# ==============================================================================
# 4. PART #4: SINGLE/DUAL PLUNGER SELECTOR CLIP (單雙管推拉切換片)
# ==============================================================================
CLIP_SPAN_X = 30.00               # Vendor spec: 30.00 mm length across dual plungers
CLIP_WIDTH_Y = 16.40              # Width perpendicular to plungers
CLIP_THICKNESS = 4.00             # Vendor spec: 4.00 mm total axial thickness
CLIP_BACK_WALL = 1.40             # Solid rear push-plate thickness
CLIP_SLOT_DEPTH = 1.80            # Internal capture slot for 1.60 mm thumb discs
CLIP_FRONT_LIP = 0.80             # Front retaining flange thickness (1.40 + 1.80 + 0.80 = 4.00)
CLIP_POCKET_DIA = 13.10           # Internal pocket diameter for Ø12.80 thumb disc
CLIP_PIVOT_HOLE_DIA = 6.80        # Captive pivot bore around Ø6.20 plunger neck (Barrel B)
CLIP_SNAP_THROAT = 11.90          # Side C-hook snap opening (0.90 mm elastic snap interference on Ø12.80)

# ==============================================================================
# 5. PART #1: HELICAL STATIC MIXER CAP (螺旋混合雙管蓋)
# ==============================================================================
MIXER_CAP_TOTAL_LEN = 41.60       # Vendor spec: 41.60 mm
MIXER_BODY_LEN = 14.87            # Vendor spec: 14.87 mm
MIXER_TUBE_EXPOSED = 26.73        # Vendor spec: 26.73 mm (14.87 + 26.73 = 41.60)
MIXER_TUBE_OD = 4.00              # Vendor spec: Ø4.00 mm cannula OD
MIXER_TUBE_ID = 3.00              # Cannula ID (wall = 0.50 mm)
MIXER_ELEMENT_COUNT = 8           # 8 alternating L/R 180-deg Kenics helical elements
MIXER_ELEMENT_LEN = 3.00          # Length per helical element (24.0 mm active mixing zone)

# ==============================================================================
# 6. PART #2: LUER RECONSTITUTION TRANSFER CAP (魯爾混合單管蓋)
# ==============================================================================
LUER_CAP_TOTAL_LEN = 15.00        # Vendor spec: 15.00 mm
LUER_FLANGE_OD = 30.00            # Vendor spec: Ø30.00 mm knurled outer ring
LUER_FLANGE_THICK = 3.40          # Vendor spec: 3.40 mm flange thickness
LUER_SKIRT_LEN = 5.60             # Rear bayonet skirt length (5.60 + 3.40 = 9.00 mm)
LUER_BOSS_LEN = 6.00              # Vendor spec: 6.00 mm protruding Luer boss (9.00 + 6.00 = 15.00)
LUER_THREAD_OD = 7.80             # Vendor spec: Ø7.80 mm ISO 80369-7 Female Luer external thread OD
LUER_TAPER_OPEN_ID = 4.27         # ISO 80369-7 6% Female Luer entry diameter
LUER_TAPER_BASE_ID = 3.91         # 4.27 - 0.06 * 6.00 = 3.91 mm (exact 6% Luer taper!)
LUER_THROAT_ID = 2.00             # Internal transfer channel ID

# ==============================================================================
# 7. PART #3: INITIAL PLUG VALVE CAP (初始塞閥蓋)
# ==============================================================================
PLUG_CAP_TOTAL_LEN = 17.00        # Vendor spec: 17.00 mm
PLUG_CAP_BODY_LEN = 9.00          # Cylindrical bayonet body (17.00 - 8.00 = 9.00 mm)
PLUG_TAB_LEN = 8.00               # Vendor spec: 8.00 mm twist-grip tab length
PLUG_TAB_THICK = 4.00             # Vendor spec: 4.00 mm twist-grip tab thickness
PLUG_TAB_SPAN = 20.00             # Ergonomic tab width across cap face

# Shared Elastomer Seal Seat Geometry (used inside Caps #1, #2, #3)
SEAL_FLANGE_OD = 18.60            # Captive disc seated inside cap counterbore (Ø18.80)
SEAL_FLANGE_Z0 = 5.30             # Bottom of elastomer flange in cap local coords
SEAL_FLANGE_Z1 = 7.10             # Top of elastomer flange in cap local coords
SEAL_SLEEVE_Z0 = 1.60             # Bottom of nozzle sealing sleeve (clears Z=0.00 cap base by 1.60 mm)
SEAL_SLEEVE_OD = 5.20             # Outer diameter of dual sealing sleeves
SEAL_SOCKET_ID = 3.24             # CAD nominal fit on Ø3.20 male nozzle (drawing: Ø3.10 interference)
SEAL_PIN_OD = 1.74                # CAD nominal fit in Ø1.80 nozzle bore (drawing: Ø1.86 interference)

# ==============================================================================
# 8. COLOR PALETTE (Matches Vendor Presentation Colors for Instant Recognition)
# ==============================================================================
HEX_BARREL_CLEAR = "#DCE8F2"      # Translucent medical cyclic olefin / polypropylene
HEX_PLUNGER_SLATE = "#686B8A"     # Slate-blue-grey plunger rods
HEX_STOPPER_PURPLE = "#9B26B6"    # Medical magenta-purple butyl/silicone stoppers
HEX_CLIP_GREEN = "#3F7A44"        # Forest green selector clip (#4)
HEX_MIXER_OLIVE = "#8C8D48"       # Olive-khaki mixer outer cap (#1)
HEX_SEAL_BROWN = "#8B5A3C"        # Brown elastomer manifold seat
HEX_FUNNEL_MAROON = "#963A36"     # Maroon Y-convergence funnel
HEX_MIXER_RED = "#B53737"         # Red Kenics static mixer elements
HEX_LUER_PURPLE = "#885E88"       # Purple knurled Luer adapter ring (#2)
HEX_LUER_TEAL = "#138A8A"         # Teal eccentric Female Luer insert (#2)
HEX_PLUG_SAGE = "#5D8263"         # Sage green initial plug cap (#3)
HEX_PLUG_RUBBER = "#845553"       # Brownish-red dual blind plug pad (#3)
