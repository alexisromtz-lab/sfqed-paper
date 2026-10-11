#!/usr/bin/env python3
"""sim/params.py -- constantes y numeros DERIVADOS del vertical 1/N.

Reglas de esta pieza:
  R1  Ningun numero fisico se cita de memoria: se calcula aqui y se imprime.
  R2  Cada cifra viaja con su unidad y con la CONVENCION con que se define
      (dos convenciones de intensidad dan dos numeros: se declara cual es).
  R3  Lo ELEGIDO (no derivado) se marca [ELEGIDO]; lo derivado, no.
  R4  Al pasar a unidades naturales se declara la entrada, no se supone.

Uso:
  python3 -B sim/params.py           bloque legible
  python3 -B sim/params.py --json    el mismo bloque en json
"""
from __future__ import annotations

import json
import math
import sys
import time

UNIVERSO = ("SI 2019 (CODATA 2018); una lambda_L y una tau ELEGIDAS; "
            "intensidad definida para onda CIRCULAR de amplitud E0 "
            "(I = eps0*c*E0**2), NO para onda lineal (esa vale la mitad)")

# ---- constantes SI (CODATA 2018 / SI 2019) ----
C = 299792458.0            # m/s      (exacta)
H_BAR = 1.054571817e-34    # J s
M_E = 9.1093837015e-31     # kg
Q_E = 1.602176634e-19      # C        (exacta)
EPS0 = 8.8541878128e-12    # F/m

# ---- elecciones declaradas ----
LAMBDA_L = 0.8e-6          # m   [ELEGIDO] longitud de onda del laser
TAU = 20e-15               # s   [ELEGIDO] duracion del pulso (envolvente FWHM)
W0_OVER_LAMBDA = 2.0       # -   [ELEGIDO] cintura w0 = 2 lambda_L
I_TECHNO = 1.0e23          # W/cm2 [ELEGIDO] techo tecnico de referencia
# (LUXE/ELI clase); ver R2: es una intensidad, no un campo.

# ---- derivados ----
OMEGA = 2.0 * math.pi * C / LAMBDA_L
PERIODO = 2.0 * math.pi / OMEGA
LAMBDA_C_RED = H_BAR / (M_E * C)          # Compton reducida, m
E_CR = M_E**2 * C**3 / (Q_E * H_BAR)      # V/m   (Schwinger)
A0_CR = Q_E * E_CR / (M_E * OMEGA * C)    # -     campo critico en unidades a0
I_CR = EPS0 * C * E_CR**2                 # W/m2  (R2: convencion circular)
CYCLES = TAU / PERIODO
W0 = W0_OVER_LAMBDA * LAMBDA_L


def campo_de_a0(a0: float) -> float:
    """Amplitud de campo E0 (V/m) para un a0 dado."""
    return M_E * OMEGA * C * a0 / Q_E


def intensidad_de_a0(a0: float) -> float:
    """Intensidad (W/m2) para un a0 dado, convencion R2 (circular)."""
    return EPS0 * C * campo_de_a0(a0) ** 2


def a0_de_intensidad(i_si: float) -> float:
    """a0 a partir de una intensidad en W/m2, misma convencion R2."""
    return math.sqrt(i_si / (EPS0 * C)) * Q_E / (M_E * OMEGA * C)


def bloque() -> dict:
    return {
        "T_UTC": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "UNIVERSO DECLARADO": UNIVERSO,
        "C": C, "H_BAR": H_BAR, "M_E": M_E, "Q_E": Q_E, "EPS0": EPS0,
        "LAMBDA_L_m": LAMBDA_L, "TAU_s": TAU,
        "W0_OVER_LAMBDA": W0_OVER_LAMBDA, "W0_m": W0,
        "I_TECHNO_W_cm2": I_TECHNO,
        "OMEGA_rad_s": OMEGA, "PERIODO_s": PERIODO, "CICLOS": CYCLES,
        "LAMBDA_C_RED_m": LAMBDA_C_RED,
        "E_CR_V_m": E_CR,
        "A0_CR": A0_CR,
        "I_CR_W_m2": I_CR, "I_CR_W_cm2": I_CR * 1e-4,
        "E0_de_a0_1_V_m": campo_de_a0(1.0),
        "I_de_a0_1_W_cm2": intensidad_de_a0(1.0) * 1e-4,
        "ORDENES_hasta_I_TECHNO": math.log10((I_CR * 1e-4) / I_TECHNO),
    }


def imprimir(b: dict) -> None:
    print(f"UNIVERSO DECLARADO: {b['UNIVERSO DECLARADO']}")
    print(f"hora = {b['T_UTC']}")
    print("--- constantes (SI) ---")
    for k in ("C", "H_BAR", "M_E", "Q_E", "EPS0"):
        print(f"  {k:9s} = {b[k]:.10g}")
    print("--- elecciones ---")
    print(f"  lambda_L  = {b['LAMBDA_L_m']:.6g} m   [ELEGIDO]")
    print(f"  tau       = {b['TAU_s']:.6g} s   [ELEGIDO]")
    print(f"  w0        = {b['W0_m']:.6g} m  ({b['W0_OVER_LAMBDA']} lambda_L) [ELEGIDO]")
    print(f"  I_techo   = {b['I_TECHNO_W_cm2']:.3g} W/cm2  [ELEGIDO]")
    print("--- derivados (calculados, no citados) ---")
    print(f"  omega     = {b['OMEGA_rad_s']:.10g} rad/s")
    print(f"  T         = {b['PERIODO_s']:.6g} s   ({b['CICLOS']:.3f} ciclos en tau)")
    print(f"  lambda_C  = {b['LAMBDA_C_RED_m']:.10g} m  (Compton reducida)")
    print(f"  E_cr      = {b['E_CR_V_m']:.6g} V/m")
    print(f"  a0_cr     = {b['A0_CR']:.6g}   (= lambda_L/(2 pi lambda_C))")
    print(f"  I_cr      = {b['I_CR_W_cm2']:.6g} W/cm2  (convencion R2: circular)")
    print(f"  a0 = 1  ->  E0 = {b['E0_de_a0_1_V_m']:.6g} V/m ; "
          f"I = {b['I_de_a0_1_W_cm2']:.6g} W/cm2")
    print(f"  ordenes de I_cr sobre I_techo = {b['ORDENES_hasta_I_TECHNO']:.3f}")
    print("--- nota de honestidad ---")
    print("  Schwinger (a0 ~ a0_cr) NO es alcanzable: el escalado 1/N se prueba")
    print("  con a0 >> 1 pero a0 << a0_cr, i.e. en regimen CLASICO de campos.")


def main() -> int:
    b = bloque()
    if "--json" in sys.argv[1:]:
        print(json.dumps(b, indent=2, sort_keys=True))
    else:
        imprimir(b)
    return 0


if __name__ == "__main__":
    sys.exit(main())
