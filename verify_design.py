"""Re-verification of the dual-syringe micro-mixer design numbers.
All inputs that are ASSUMPTIONS are marked; change them when measured data exist.
"""
import math

kB, T = 1.380649e-23, 298.0
rho = 1000.0

# ---------------- ASSUMPTIONS ----------------
mu_A = 0.050      # Pa.s  PEG in S-buffer (UNMEASURED; plausible range 0.005-0.05)
mu_B = 0.001      # Pa.s  T-buffer (water-like)
mu_mix = 0.010    # Pa.s  mixed, polymer diluted 2x (assumption)
V_total = 2.0e-6  # m3   2 mL total dispensed
t_disp = 10.0     # s    dispensing time
Q = V_total / t_disp          # total flow
Q_each = Q / 2
D_ion = 1.0e-9    # m2/s  small buffer ions / OH- (OH- ~5e-9, carbonate ~1e-9)
D_peg = 6.0e-11   # m2/s  4-arm PEG 10-20 kDa
pKa_SH = 8.8      # thiol pKa used previously (PEG-thiols often 8.5-10)

print("=== Flow conditions ===")
print(f"Q_total = {Q*1e6:.2f} mL/s, Q_each = {Q_each*1e6:.2f} mL/s")

# ---------------- 1. Inlet resistance balancing ----------------
def R_circ(mu, L, D):
    return 128 * mu * L / (math.pi * D**4)

L_in = 3e-3
RA = R_circ(mu_A, L_in, 0.80e-3)
RB = R_circ(mu_B, L_in, 0.35e-3)
print("\n=== 1. Inlet orifices (old design) ===")
print(f"(0.80/0.35)^4 = {(0.80/0.35)**4:.1f}  vs viscosity ratio {mu_A/mu_B:.0f}  -> NOT equal")
print(f"Length ratio needed L_B/L_A = {(mu_A/mu_B)*(0.35/0.80)**4:.2f}")
print(f"dP inlet A = {RA*Q_each/1e3:.2f} kPa, dP inlet B = {RB*Q_each/1e3:.2f} kPa")

# ---------------- 2. Mixing channel ----------------
def R_rect(mu, L, w, h):
    # h < w, standard approximation
    return 12 * mu * L / (w * h**3 * (1 - 0.630 * h / w))

print("\n=== 2. Mixing channel ===")
for name, w, h, L in [("OLD (2.4 x 1.0 mm, 8 mm SHM)", 2.4e-3, 1.0e-3, 8e-3),
                      ("NEW (1.5 x 0.5 mm, 28.8 mm SHM)", 1.5e-3, 0.5e-3, 28.8e-3)]:
    A = w * h
    U = Q / A
    Dh = 2 * w * h / (w + h)
    Re_mix = rho * U * Dh / mu_mix
    Re_B = rho * U * Dh / mu_B
    Pe = U * h / D_ion
    gamma_w = 6 * Q / (w * h**2)
    t_res = L / U
    # Stroock 2002 calibration: Δy90 ≈ 1 cm at Pe≈2e5 for w=200 µm -> a ≈ 4.1
    a = 1.0e-2 / (200e-6 * math.log(2e5))
    s_end = w * math.exp(-L / (a * w))   # striation thickness model
    t_ion = s_end**2 / D_ion
    t_peg = s_end**2 / D_peg
    L90 = a * w * math.log(Pe)
    dP = R_rect(mu_mix, L, w, h) * Q
    print(f"-- {name}")
    print(f"   U={U:.3f} m/s  Dh={Dh*1e3:.2f} mm  Re(mix)={Re_mix:.1f}  Re(water)={Re_B:.0f}")
    print(f"   Pe(ion)={Pe:.2e}  wall shear≈{gamma_w:.0f} 1/s  residence={t_res*1e3:.0f} ms")
    print(f"   Stroock-scaled L90 = {L90*1e3:.0f} mm; striation at exit ≈ {s_end*1e6:.0f} µm")
    print(f"   ion equilibration s²/D ≈ {t_ion:.2f} s ; PEG interdiffusion ≈ {t_peg:.1f} s")
    print(f"   dP (μ_mix={mu_mix*1e3:.0f} cP) = {dP/1e3:.1f} kPa ; with 50 cP = {dP*0.05/mu_mix/1e3:.1f} kPa")

# groove/height ratio
print(f"\nGroove depth ratio OLD: 80 µm / 1000 µm = {0.08:.2f} (Stroock used ~0.2-0.3)")
print(f"Groove depth ratio NEW: 150 µm / 500 µm = {0.15/0.5:.2f}")

# ---------------- 3. Polymer chain stretching claim ----------------
print("\n=== 3. Coil-stretch claim ===")
Rg = 3e-9
for eta in (1e-3, 0.05):
    tau = eta * Rg**3 / (kB * T)
    print(f"   Zimm τ (η={eta*1e3:.0f} cP) ≈ {tau:.1e} s ; Wi at 3000 1/s = {3000*tau:.1e}")
print("   Even a semidilute 1e-5 s relaxation gives Wi ≈ 0.03 << 1  -> no coil-stretch")

# ---------------- 4. Thiolate fraction ----------------
print("\n=== 4. Thiolate fraction ===")
f = lambda pH: 1 / (1 + 10**(pKa_SH - pH))
for pH in (4.0, 6.0, 8.0, 9.0, 9.6, 9.8):
    print(f"   pH {pH}: S- fraction = {f(pH)*100:.3f} %")
print(f"   ratio 9.8/6.0 = {f(9.8)/f(6.0):.0f}x  (previously claimed >1000x)")

# ---------------- 5. Dead volume (new geometry) ----------------
print("\n=== 5. Hold-up volume, NEW geometry ===")
inlet = 2 * 9e-3 * math.pi * (0.4e-3)**2
chan = 1.5e-3 * 0.5e-3 * 28.8e-3
groove = 48 * (1.5e-3 * math.sqrt(2) * 0.25e-3) * 0.15e-3
nozzle = 6e-3 * 0.40e-6
tot = inlet + chan + groove + nozzle
for k, v in [("inlets", inlet), ("channel", chan), ("grooves", groove), ("nozzle", nozzle), ("TOTAL", tot)]:
    print(f"   {k:8s} {v*1e9:5.1f} µL")

# ---------------- 6. Hand force ----------------
print("\n=== 6. Plunger force (two 3 mL barrels, ID 8.66 mm) ===")
A_bar = math.pi * (8.66e-3 / 2)**2
dP_new = R_rect(mu_mix, 28.8e-3, 1.5e-3, 0.5e-3) * Q
print(f"   dP={dP_new/1e3:.1f} kPa -> F ≈ {dP_new*2*A_bar:.1f} N (+ stopper friction ~5-10 N)")
