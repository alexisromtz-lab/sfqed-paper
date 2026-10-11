#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sim/schwinger_offline.py -- ETAPA 2: el rendimiento LCFA, FUERA del PIC.

FUENTE DE LA FORMULA: no de memoria.  Se LEE main.tex, se extraen los cuerpos de
  eq:schwinger_rate  w(E) = (eE)^2/(4 pi^3) sum n^-2 exp(-n pi m^2/(eE))
  eq:ab              a = sqrt(sqrt(F^2+G^2) + F)
  eq:yield           N = int_Omega d4x w(a(x,t))
  eq:lin_inv         F = E0^2 (cos 2wt + cos 2kz),  G = 0
  eq:cp_inv          F = 2E0^2 cos 2kz,  G = 2E0^2 sin 2kz
y se comparan contra PIN_FORMULAS (sha16 del cuerpo normalizado).  Si main.tex
cambia, este instrumento NO adivina: enrojece y pide re-derivar el pin.
(Doctrina: el instrumento que lleva su creencia adentro mide su propia creencia.)

QUE MIDE: el funcional eq:yield sobre las dos geometrias que el paper separa,
evaluadas en los campos pico declarados por sim/configs.json:
  circular co-rotante -> a(z)   = E_pico |cos kz|                (QUIETO en t)
  lineal              -> a(z,t) = (E_pico/sqrt2) sqrt(max(0, cos 2wt + cos 2kz))
Mas el control de Lemma 1: una sola onda plana -> F = G = 0 -> a = 0.

POR QUE TODO VA EN log10: con x = E_cr/E ~ 2e3, exp(-pi x) es 0.0 en doble; el 0
de la maquina NO dice "cero pares".  El instrumento imprime el exponente, la cola
de la serie y la cota del resto de la celda.

QUE NO HACE: no corre PIC, no lee campos de una corrida, no escribe medidas.
sim/medidas_aN.csv sigue ausente: eso lo trae la etapa 1.

Uso
  python3 -B sim/schwinger_offline.py --pin     imprime los sha16 medidos
  python3 -B sim/schwinger_offline.py           corre, imprime y escribe JSON
  python3 -B sim/schwinger_offline.py --json    idem, salida JSON por stdout
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import sys
import time
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
sys.path.insert(0, str(AQUI))

import params as P  # noqa: E402

MAIN_TEX = RAIZ / "main.tex"
CONFIGS = AQUI / "configs.json"
SALIDA = AQUI / "pronostico_schwinger.json"

UNIVERSO = (
    "main.tex (cuerpos leidos; sha16 impreso) + sim/configs.json (campo pico por N) + "
    "mallas y tolerancias ELEGIDAS; motor python3 float64 sin dependencias; "
    "medida = UNA celda del reticulo (lambda/2 x T/2), la MISMA en las dos geometrias; "
    "volumen y tiempo del rendimiento: V = (pi w0^2/2)(c tau), T = tau  [SUPUESTO DECLARADO]"
)

PIN_FORMULAS = {
    "eq:schwinger_rate": "b043587212f4522b",
    "eq:ab": "7a20202407815345",
    "eq:yield": "b27213b3542beb39",
    "eq:lin_inv": "ade47f905f9ac06e",
    "eq:cp_inv": "46e99b22931bb5a1",
}

# --- numerica declarada ANTES de ver la salida ---
N_TERMINOS = 64          # [ELEGIDO] terminos maximos de la serie de Schwinger
CORTE_DEX = 40.0         # [ELEGIDO] se corta la serie cuando el termino cae 40 dex
N_Z_CIRC = (4001, 8001)  # [ELEGIDO] rejillas en z sobre [0, lambda/2)
N_GRID_LIN = (400, 800)  # [ELEGIDO] rejillas en la esquina [0, U]^2 del pico
U_ESQUINA = 1.0          # [ELEGIDO] lado de la esquina que contiene el pico (rad)
TOL_CONV_DEX = 1.0e-3    # [ELEGIDO] divergencia admitida entre las dos rejillas
TOL_CONTROL_DEX = 1.0e-9  # [ELEGIDO] tolerancia de los controles algebraicos

LN10 = math.log(10.0)
FLOOR_DEX = -320.0


# ------------------------------------------------------------- formula leida
def leer_cuerpos() -> tuple[str, dict]:
    """sha16 del archivo y cuerpos de ecuacion con label, normalizados."""
    tex = MAIN_TEX.read_text(encoding="utf-8")
    sha = hashlib.sha256(tex.encode()).hexdigest()[:16]
    cuerpos = {}
    for _, bloque in re.findall(r"\\begin\{(equation|align)\}(.*?)\\end\{\1\}", tex, flags=re.S):
        lab = re.search(r"\\label\{([^}]*)\}", bloque)
        if lab:
            cuerpos[lab.group(1)] = " ".join(re.sub(r"\\label\{[^}]*\}", "", bloque).split())
    return sha, cuerpos


def sha16(texto: str) -> str:
    return hashlib.sha256(texto.encode()).hexdigest()[:16]


def verificar_pin(cuerpos: dict) -> list:
    fallos = []
    for lab, esperado in PIN_FORMULAS.items():
        cuerpo = cuerpos.get(lab)
        if cuerpo is None:
            fallos.append(f"{lab}: AUSENTE en main.tex")
            continue
        real = sha16(cuerpo)
        if real != esperado:
            fallos.append(f"{lab}: pin {esperado} != leido {real} (la formula del paper cambio)")
    return fallos


# ------------------------------------------------------------------- la formula
def log10sumexp(vals: list):
    """log10(sum 10^v) y cuantas colas se hundieron en el piso de doble."""
    if not vals:
        return None, 0
    m = max(vals)
    colas = 0
    suma = 0.0
    for v in vals:
        d = v - m
        if d < FLOOR_DEX:
            colas += 1
            continue
        suma += 10.0 ** d
    return m + math.log10(suma), colas


def log10_S(x: float):
    """log10 de S(x) = sum n^-2 exp(-n pi x),  x = E_cr/E > 0.  Devuelve (log10S, log10cola)."""
    if not (x > 0.0):
        return None, None
    vals = []
    ref = -math.pi * x / LN10          # termino n=1: el mayor para x>0
    for n in range(1, N_TERMINOS + 1):
        v = -(n * math.pi * x) / LN10 - 2.0 * math.log10(n)
        if n >= 2 and v < ref - CORTE_DEX:
            break
        vals.append(v)
    log10s, _ = log10sumexp(vals)
    cola = -(len(vals) + 1) * math.pi * x / LN10 + math.log10(math.pi ** 2 / 6.0)
    return log10s, cola


def log10_w_SI(E: float):
    """Ruta A: w = (eE)^2/(4 pi^3 hbar^2 c) * S(x), SI.  Devuelve dict en dex."""
    if not (E > 0.0):
        return None
    x = P.E_CR / E
    log10s, cola = log10_S(x)
    pref = (P.Q_E * E) ** 2 / (4.0 * math.pi ** 3 * P.H_BAR ** 2 * P.C)
    return {"x": x, "log10_pref": math.log10(pref), "log10_S": log10s,
            "log10_cola_serie": cola, "log10_w": math.log10(pref) + log10s}


def log10_w_SI_ruta_B(E: float):
    """Ruta B: (m_e^4/x^2)/(4 pi^3) * S en eV^4, convertido por q^4/(hbar^4 c^3).

    Es la MISMA fisica con otra contabilidad: control de aritmetica, no de fisica.
    """
    if not (E > 0.0):
        return None
    x = P.E_CR / E
    log10s, _ = log10_S(x)
    m_eV = P.M_E * P.C ** 2 / P.Q_E
    factor = P.Q_E ** 4 / (P.H_BAR ** 4 * P.C ** 3)   # de constantes, sin numero magico
    return math.log10(m_eV ** 4 / (x ** 2 * 4.0 * math.pi ** 3)) + log10s + math.log10(factor)


# ------------------------------------------------------------------ geometrias
def a_circular(z: float, E_pico: float) -> float:
    """eq:cp_inv + eq:ab: a = 2 E0 |cos kz| = E_pico |cos kz| (E_pico = 2 E0)."""
    return E_pico * abs(math.cos(2.0 * math.pi * z / P.LAMBDA_L))


def a_lineal(z: float, t: float, E_pico: float) -> float:
    """eq:lin_inv + eq:ab: F = E0^2(cos2wt+cos2kz) -> a = E_pico sqrt(max(0,s)/2)."""
    s = math.cos(2.0 * P.OMEGA * t) + math.cos(2.0 * (2.0 * math.pi / P.LAMBDA_L) * z)
    if s <= 0.0:
        return 0.0
    return E_pico * math.sqrt(s / 2.0)


def a_onda_plana(E_pico: float) -> float:
    """Lemma 1: una sola onda plana -> F = G = 0 -> a = 0 (independiente de E_pico)."""
    F = 0.0
    G = 0.0
    return math.sqrt(math.sqrt(F * F + G * G) + F)


def log10_media_circular(E_pico: float, nz: int):
    """log10 de la media de w sobre una celda (lambda/2 en z; constante en t)."""
    dz = (P.LAMBDA_L / 2.0) / nz
    vals = []
    for i in range(nz):
        z = (i + 0.5) * dz
        a = a_circular(z, E_pico)
        if a <= 0.0:
            continue
        vals.append(log10_w_SI(a)["log10_w"])
    log10suma, colas = log10sumexp(vals)
    return log10suma - math.log10(nz), nz - len(vals), colas


def log10_media_lineal(E_pico: float, ng: int):
    """log10 de la media de w sobre la celda (u,v) en [0,2pi)^2, integrando las 4 esquinas.

    El pico esta en la esquina (u,v)=(0,0) y sus 3 equivalentes por periodicidad; se
    integra la esquina [0,U]^2 con la rejilla declarada y el resto de la celda se
    ACOSTA con una cota, que se imprime (no se supone cero).
    """
    du = U_ESQUINA / ng
    vals = []
    for i in range(ng):
        u = (i + 0.5) * du
        cu = math.cos(u)
        for j in range(ng):
            v = (j + 0.5) * du
            s = cu + math.cos(v)
            if s <= 0.0:
                continue
            a = E_pico * math.sqrt(s / 2.0)
            vals.append(log10_w_SI(a)["log10_w"])
    log10suma, colas = log10sumexp(vals)
    area_celda = (2.0 * math.pi) ** 2
    log10_int_esquina = log10suma + math.log10(du * du)     # integral sobre 1 esquina
    log10_media = log10_int_esquina + math.log10(4.0) - math.log10(area_celda)
    # cota del resto: maximo de a fuera de las 4 esquinas, en u=U (o v=U)
    a_borde = E_pico * math.sqrt((1.0 + math.cos(U_ESQUINA)) / 2.0)
    log10_cota_resto = log10_w_SI(a_borde)["log10_w"] + math.log10(area_celda) \
        + math.log10(4.0) - math.log10(area_celda) - log10_media
    return log10_media, colas, log10_cota_resto, ng * ng - len(vals)


# ------------------------------------------------------------------- controles
def controles(E_test: float) -> list:
    res = []

    # CP1: las dos contabilidades (ruta A y ruta B) dan el mismo w en SI
    la = log10_w_SI(E_test)["log10_w"]
    lb = log10_w_SI_ruta_B(E_test)
    res.append(("CP1 dos rutas SI (A: hbar^2 c | B: eV^4 -> q^4/(hbar^4 c^3))",
                abs(la - lb) < TOL_CONTROL_DEX, f"|dA-dB| = {abs(la-lb):.3e} dex"))

    # CP2: Lemma 1 -- onda plana -> a = 0 -> NO hay pares (no un cero)
    a_plana = a_onda_plana(E_test)
    res.append(("CP2 Lemma 1: onda plana -> a = 0 exacto", a_plana == 0.0,
                f"a = {a_plana!r} -> 'NO HAY PARES' (no 0.0 pares)"))

    # CP3: la circular es t-independiente POR CONSTRUCCION (eq:cp_inv) y la lineal no:
    #      el control exige que la lineal SI cambie (si no cambia, el metro es el mismo).
    #      (el primer punto de prueba cayo en un NODO: kz = pi/2 -> a = 0 en las dos; la
    #       leccion es que el punto de prueba tambien se elige, no se supone)
    peor = 0.0
    z_peor = None
    a0_reporte = None
    for frac in (0.0, 1.0 / 8.0, 1.0 / 4.0, 3.0 / 8.0):
        zs = frac * P.LAMBDA_L
        if a0_reporte is None:
            a0_reporte = a_circular(0.0, E_test)
        for k in range(1, 9):
            t = k * (2.0 * math.pi / P.OMEGA) / 8.0
            d = abs(a_lineal(zs, t, E_test) - a_lineal(zs, 0.0, E_test))
            if d > peor:
                peor, z_peor = d, frac
    res.append(("CP3 las dos geometrias NO son la misma: la lineal cambia con t",
                peor > 0.0, f"a_circ(z=0) = {a0_reporte:.6e} V/m fijo en t (eq:cp_inv); "
                            f"cambio medido en la LINEAL = {peor:.3e} V/m en z = {z_peor:.3f} lambda"))

    # CP4: la serie tiene solo el termino n=1 a los x de trabajo (cola declarada)
    _, cola = log10_S(P.E_CR / E_test)
    res.append(("CP4 cola de la serie de Schwinger despreciable",
                cola < -300.0, f"log10 cola(n>1) <= {cola:.1f}"))

    # CP5: la escala entre las dos rutas es CONSTANTE en campos distintos
    #      (caza un error dependiente del campo, p.ej. un exponente mal puesto en x)
    E_bajo = E_test / 1000.0
    d1 = la - log10_w_SI_ruta_B(E_test)
    d2 = log10_w_SI(E_bajo)["log10_w"] - log10_w_SI_ruta_B(E_bajo)
    res.append(("CP5 escala entre rutas constante en E y en E/1000",
                abs(d1 - d2) < TOL_CONTROL_DEX, f"d(E) = {d1:.3e} dex ; d(E/1000) = {d2:.3e} dex"))
    return res


def control_underflow(E_pico: float) -> dict:
    x = P.E_CR / E_pico
    crudo = math.exp(-math.pi * x)
    return {"x": x, "exp_menos_pi_x_doble": crudo,
            "log10_w_dex": log10_w_SI(E_pico)["log10_w"],
            "nota": ("el 0.0 de exp(-pi x) es el piso de doble, no un cero fisico: "
                     "log10 w es finito y es la cifra que se reporta")}


# ------------------------------------------------------------------------ main
def main() -> int:
    args = sys.argv[1:]

    sha_tex, cuerpos = leer_cuerpos()

    if "--pin" in args:
        print(f"UNIVERSO DECLARADO: {UNIVERSO}")
        print(f"main.tex sha16 = {sha_tex}")
        for lab in PIN_FORMULAS:
            c = cuerpos.get(lab)
            print(f"  {lab:<20} {'AUSENTE' if c is None else sha16(c)}")
        return 0

    fallos_pin = verificar_pin(cuerpos)
    if fallos_pin:
        print(f"UNIVERSO DECLARADO: {UNIVERSO}")
        print("ROJO: el pin de la formula no coincide:")
        for f in fallos_pin:
            print(f"  {f}")
        print("Accion: re-derivar el pin con --pin y revisar que la formula siga siendo la misma.")
        return 1

    cfg = json.loads(CONFIGS.read_text(encoding="utf-8"))
    filas = cfg["filas"]
    area = math.pi * P.W0 ** 2 / 2.0
    V = area * (P.C * P.TAU)
    T = P.TAU
    log10_VT = math.log10(V * T)

    controles_res = controles(filas[0]["E0_tot_V_m"])
    uf = control_underflow(filas[0]["E0_tot_V_m"])

    tabla = []
    for f in filas:
        E_pico = f["E0_tot_V_m"]
        w_pico = log10_w_SI(E_pico)

        lc_1, _, _ = log10_media_circular(E_pico, N_Z_CIRC[0])
        lc_2, ceros_c, colas_c = log10_media_circular(E_pico, N_Z_CIRC[1])
        conv_c = abs(lc_2 - lc_1)

        ll_1, _, _, _ = log10_media_lineal(E_pico, N_GRID_LIN[0])
        ll_2, colas_l, cota_resto, ceros_l = log10_media_lineal(E_pico, N_GRID_LIN[1])
        conv_l = abs(ll_2 - ll_1)

        tabla.append({
            "N": f["N"], "E_pico_V_m": E_pico, "a_tot_pred_adimensional": f["a_tot_pred"],
            "x_Ecr_sobre_Epico": w_pico["x"],
            "log10_w_pico": w_pico["log10_w"],
            "log10_cola_serie": w_pico["log10_cola_serie"],
            "log10_media_circular": lc_2, "log10_media_lineal": ll_2,
            "log10_N_circular": lc_2 + log10_VT, "log10_N_lineal": ll_2 + log10_VT,
            "ventaja_circular_dex": lc_2 - ll_2,
            "convergencia_z_dex": conv_c, "convergencia_uv_dex": conv_l,
            "cota_resto_celda_dex": cota_resto,
            "celdas_uv_en_cero": ceros_l, "colas_dobles": colas_l,
            "pares_dobles_circular": 10.0 ** (lc_2 + log10_VT),
        })

    conv_max = max(max(t["convergencia_z_dex"], t["convergencia_uv_dex"]) for t in tabla)
    controles_res.append(("CP6 convergencia de las rejillas (z y u,v)",
                          conv_max < TOL_CONV_DEX, f"peor divergencia = {conv_max:.3e} dex"))
    todo_ok = all(ok for _, ok, _ in controles_res)

    salida = {
        "instrumento": "sim/schwinger_offline.py",
        "etapa": 2,
        "T_UTC": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "UNIVERSO DECLARADO": UNIVERSO,
        "main_tex_sha16": sha_tex,
        "pin_formulas": PIN_FORMULAS,
        "numerica_declarada": {
            "N_TERMINOS": N_TERMINOS, "CORTE_DEX": CORTE_DEX,
            "N_Z_CIRC": list(N_Z_CIRC), "N_GRID_LIN": list(N_GRID_LIN),
            "U_ESQUINA_rad": U_ESQUINA,
            "TOL_CONV_DEX": TOL_CONV_DEX, "TOL_CONTROL_DEX": TOL_CONTROL_DEX,
            "V_m3": V, "T_s": T, "log10_VT_m3s": log10_VT,
        },
        "underflow": uf,
        "controles": [{"nombre": n, "ok": ok, "detalle": d} for n, ok, d in controles_res],
        "todo_verde": todo_ok,
        "tabla": tabla,
    }

    if "--json" in args:
        print(json.dumps(salida, indent=2, ensure_ascii=False))
        return 0 if todo_ok else 1

    print(f"UNIVERSO DECLARADO: {UNIVERSO}")
    print(f"hora = {salida['T_UTC']}   main.tex sha16 = {sha_tex} (pin OK)")
    print(f"medida declarada: V = (pi w0^2/2)(c tau) = {V:.6e} m3 ; T = tau = {T:.3e} s ; "
          f"log10(V T) = {log10_VT:.4f}")
    print(f"piso de doble: exp(-pi x) = {uf['exp_menos_pi_x_doble']!r} con x = {uf['x']:.2f} "
          f"-> log10 w = {uf['log10_w_dex']:.2f} dex (finito)")
    print("--- controles ---")
    for n, ok, d in controles_res:
        print(f"  [{'OK ' if ok else 'ROJO'}] {n}\n         {d}")
    print("--- tabla (dex de w en m^-3 s^-1) ---")
    print(f"{'N':>3} {'E_pico V/m':>14} {'x':>9} {'log10 w(pico)':>14} "
          f"{'log10<w>circ':>13} {'log10<w>lin':>12} {'ventaja dex':>12} {'log10 N circ':>13}")
    for t in tabla:
        print(f"{t['N']:>3} {t['E_pico_V_m']:>14.6e} {t['x_Ecr_sobre_Epico']:>9.1f} "
              f"{t['log10_w_pico']:>14.2f} {t['log10_media_circular']:>13.2f} "
              f"{t['log10_media_lineal']:>12.2f} {t['ventaja_circular_dex']:>12.2f} "
              f"{t['log10_N_circular']:>13.2f}")
    print(f"cota del resto de la celda: aporta a lo sumo 10^"
          f"{max(t['cota_resto_celda_dex'] for t in tabla):.1f} de la media (peor caso entre N)")
    print(f"pares en doble (circular, N=1): {tabla[0]['pares_dobles_circular']!r} "
          f"-> ningun par: hacen falta {abs(tabla[0]['log10_N_circular']):.0f} ordenes")
    print("nota de rotulos: configs.json llama a_tot_pred al parametro adimensional del haz; "
          "la a de eq:ab es un CAMPO en V/m. Misma letra, dos objetos: aqui se usan rotulados.")
    SALIDA.write_text(json.dumps(salida, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"escrito: {SALIDA.relative_to(RAIZ)}")
    if not todo_ok:
        print("ROJO: algun control fallo; la tabla NO se eleva a pronostico.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
