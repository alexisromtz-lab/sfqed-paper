#!/usr/bin/env python3
"""sim/gen_configs.py -- genera la TABLA de configuraciones de la serie 1/N.

QUE HACE
  Fija energia total Sigma y duracion tau, reparte en N pulsos co-propagantes
  circular co-rotantes en coincidencia perfecta, y calcula el a0 por pulso y el
  a0 TOTAL esperado si los N campos se suman coherentes.
  El modelo predice a_tot(N) = sqrt(N) * a_ref  (pendiente beta = 0.5 en log-log).
  Esta tabla trae el PREDICHO; la medicion la trae el PIC y la juzga falsador.py.

QUE NO HACE
  NO emite un namelist listo para correr en Smilei/WarpX. Emite una tabla
  agnostica de motor + un MAPEO DECLARADO de nombres de clave (ver MAPPING).
  Escribir un namelist "listo" que nadie corrio seria una cifra sin comando.

Uso:
  python3 -B sim/gen_configs.py                 tabla + escribe sim/configs.json
  python3 -B sim/gen_configs.py --sin-escribir  solo imprime
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import params as P  # noqa: E402

AQUI = Path(__file__).resolve().parent

UNIVERSO = ("sim/params.py (SI, lambda_L=0.8um) + una Sigma y una malla de N "
            "ELEGIDAS; modelo de reparto coherente declarado abajo")

# ---- elecciones declaradas ----
SIGMA_J = 100.0            # J   [ELEGIDO] energia total de la serie (fija)
N_LISTA = [1, 2, 4, 8, 16]  # -   [ELEGIDO] malla de N (potencias de 2)
CFL = 0.9                  # -   [ELEGIDO]
DX_OVER_LAMBDA = 1.0 / 40  # -   [ELEGIDO] dx = lambda/40
CAJA_LAMBDA = 12.0         # -   [ELEGIDO] caja 12 lambda por lado
DIAG_CADA_PASOS = 20       # -   [ELEGIDO] cadencia de diagnostico

# MAPEO DECLARADO a nombres de clave de los motores citados en refs.bib.
# Es un MAPEO (que clave lleva que magnitud), no una config lista.
MAPPING = {
    "Smilei2018": {"a0": "laser.amplitude", "lambda0": "laser.wavelength",
                   "polarizacion": "laser.polarization_phi",
                   "dx": "grid.length", "pasos": "main.n_step",
                   "salida_campos": "diag_fields.dump_step"},
    "WarpX2022": {"a0": "warpx.a0", "lambda0": "warpx.lambda0",
                  "polarizacion": "warpx.polarization",
                  "dx": "amr.n_cell / amr.max_level",
                  "pasos": "max_step", "salida_campos": "warpx.plot_int"},
    "EPOCH2015": {"a0": "laser.intensity (via a0)", "lambda0": "laser.wavelength",
                  "polarizacion": "laser.polarisation",
                  "dx": "nx / length_x", "pasos": "nsteps",
                  "salida_campos": "output.dump_first"},
}


def area_cintura() -> float:
    """Area efectiva del pulso Gaussiano circular (m2)."""
    return math.pi * P.W0**2 / 2.0


def a_ref_de_energia(sigma_j: float) -> float:
    """a0 de un pulso de energia sigma_j, duracion tau, cintura w0 (convencion R2)."""
    i_si = sigma_j / (area_cintura() * P.TAU)
    return P.a0_de_intensidad(i_si)


def serie() -> dict:
    a_ref = a_ref_de_energia(SIGMA_J)
    dx = DX_OVER_LAMBDA * P.LAMBDA_L
    dt = CFL * dx / P.C
    caja = CAJA_LAMBDA * P.LAMBDA_L
    n_pasos = int(round((P.TAU + caja / P.C) / dt))
    filas = []
    for n in N_LISTA:
        e_beam = SIGMA_J / n
        a_beam = a_ref / math.sqrt(n)      # energia por pulso Sigma/n
        a_tot = math.sqrt(n) * a_ref       # suma coherente de N campos
        filas.append({
            "N": n,
            "E_por_pulso_J": e_beam,
            "a_beam": a_beam,
            "a_tot_pred": a_tot,
            "beta_pred": 0.5,
            "E0_tot_V_m": P.campo_de_a0(a_tot),
            "I_tot_W_cm2": P.intensidad_de_a0(a_tot) * 1e-4,
        })
    return {
        "T_UTC": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "UNIVERSO DECLARADO": UNIVERSO,
        "modelo": ("energia total fija, tau fija, w0 fija, coincidencia perfecta, "
                   "circular co-rotante -> a_tot(N) = sqrt(N) a_ref"),
        "SIGMA_J": SIGMA_J, "N_LISTA": N_LISTA,
        "a_ref_N_1": a_ref,
        "numerica": {
            "dx_m": dx, "dx_sobre_lambda": DX_OVER_LAMBDA, "CFL": CFL,
            "dt_s": dt, "caja_m": caja, "caja_sobre_lambda": CAJA_LAMBDA,
            "n_pasos": n_pasos, "diag_cada_pasos": DIAG_CADA_PASOS,
            "w0_m": P.W0, "tau_s": P.TAU, "lambda_m": P.LAMBDA_L,
            "unidades": "naturales hbar=c=1, m_e=1 para el motor; SI en esta tabla",
        },
        "controles_obligatorios": [
            "una sola onda plana -> a0 debe dar 0 (Lemma 1: F=G=0)",
            "desajuste DeltaL = lambda/2 -> el escalado debe romperse",
            "lineal -> F cambia de signo y G = 0; circular -> F,G quietos",
            "energia total conservada dentro de la tolerancia declarada",
        ],
        "MAPPING": MAPPING,
        "filas": filas,
    }


def imprimir(s: dict) -> None:
    print(f"UNIVERSO DECLARADO: {s['UNIVERSO DECLARADO']}")
    print(f"hora = {s['T_UTC']}")
    print(f"modelo: {s['modelo']}")
    print(f"Sigma = {s['SIGMA_J']:.6g} J (fija) ; tau = {s['numerica']['tau_s']:.4g} s ; "
          f"w0 = {s['numerica']['w0_m']:.4g} m")
    print(f"a_ref(N=1) = {s['a_ref_N_1']:.6g}")
    print("--- numerica declarada ---")
    nu = s["numerica"]
    print(f"  dx = lambda/{1/nu['dx_sobre_lambda']:.0f} = {nu['dx_m']:.6g} m ; "
          f"CFL = {nu['CFL']} ; dt = {nu['dt_s']:.6g} s")
    print(f"  caja = {nu['caja_sobre_lambda']:.4g} lambda ; n_pasos = {nu['n_pasos']} ; "
          f"diag cada {nu['diag_cada_pasos']} pasos")
    print(f"  unidades = {nu['unidades']}")
    print("--- tabla (PREDICHO por el modelo, no medido) ---")
    hdr = f"{'N':>3} {'Sigma/N[J]':>11} {'a_beam':>10} {'a_tot_pred':>11} {'beta':>5} {'I_tot[W/cm2]':>13}"
    print("  " + hdr)
    for f in s["filas"]:
        print(f"  {f['N']:>3} {f['E_por_pulso_J']:>11.4g} {f['a_beam']:>10.4f} "
              f"{f['a_tot_pred']:>11.4f} {f['beta_pred']:>5.2f} {f['I_tot_W_cm2']:>13.4g}")
    print("--- controles obligatorios ---")
    for c in s["controles_obligatorios"]:
        print("  - " + c)
    print("--- MAPEO a motores (nombres de clave; NO es namelist listo) ---")
    for motor, kv in s["MAPPING"].items():
        print(f"  {motor}: " + ", ".join(f"{k}->{v}" for k, v in kv.items()))


def main() -> int:
    s = serie()
    imprimir(s)
    if "--sin-escribir" not in sys.argv[1:]:
        destino = AQUI / "configs.json"
        destino.write_text(json.dumps(s, indent=2, sort_keys=True) + "\n",
                           encoding="utf-8")
        print(f"escrito: {destino} ({destino.stat().st_size} B)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
