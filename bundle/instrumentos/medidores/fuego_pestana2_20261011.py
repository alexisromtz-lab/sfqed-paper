#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fuego_pestana2_20261011.py — disparo de la PESTANA 2 (circular corregida, sigma_phi por haz).

UNIVERSO DECLARADO: instrumento = sim/runner_2d3v.py sha16=f280fb6744917e9a (528 l, 24072 B)
  = congelado 368627d18d83d253 + parche sim/parche_salida_fases.py sha16=87756c47d76267dd;
  geometria = sim/params.py 9983b3d25a68f032 + sim/configs.json c7508e0430319162;
  pol = circular ; dl = 0.0 ; PASOS = 300 ; N_LISTA = [1, 2, 4, 8, 16] ;
  Omega_foco = |r| <= 80 celdas = 2 lambda_L ; malla 480x480 ; dx = lambda_L/40 ; CFL = 0.6 ;
  unidad = a0 = eE/(m_e omega c) ; motor = numpy float64 (FDTD Yee 2D3V) ; ventana = reloj UTC.
MOTOR: python3 -B + subprocess (un proceso por sigma) + ProcessPoolExecutor (4 por defecto).
UNIDAD del conteo: fila del CSV canonico (12 grupos x 5 = 60). VENTANA: hora UTC impresa.
LECTURA = PICO (max|E| en el disco |r| <= w0 y la ventana causal) = el a_medido del instrumento.
PRE-REGISTRO (sellado ANTES de correr): sim/PREREGISTRO_PESTANA2_CIRCULAR_CORREGIDA_20261011.md
NO se corre sim/falsador.py sobre el archivo nuevo (su MEDIDAS esta cableado a medidas_aN.csv).

Uso:
  python3 -B sim/fuego_pestana2_20261011.py --sigma 0.000            # control K0, en serie
  python3 -B sim/fuego_pestana2_20261011.py --todo                   # los 12 grupos (4 obreros)
  python3 -B sim/fuego_pestana2_20261011.py --todo --trabajadores 4
  python3 -B sim/fuego_pestana2_20261011.py --unir                   # union + betas (lee el disco)
"""

from __future__ import annotations

import argparse
import hashlib
import math
import re
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

AQUI = Path("/Users/marlene/sfqed-paper/sim")
RAIZ = AQUI.parent
INSTRUMENTO = AQUI / "runner_2d3v.py"
PARCHE = AQUI / "parche_salida_fases.py"
DIFF = AQUI / "salida_fases.diff"
PRE_REG = AQUI / "PREREGISTRO_PESTANA2_CIRCULAR_CORREGIDA_20261011.md"
TESTIGO = AQUI / "medidas_aN_circular.csv"
PARAMS = AQUI / "params.py"
CONFIGS = AQUI / "configs.json"

SHA16_INSTR = "f280fb6744917e9a"
BYTES_INSTR = 24072
LINEAS_INSTR = 528
SHA16_PARCHE = "87756c47d76267dd"
SHA16_DIFF = "f7f826abc259f792"
SHA16_TESTIGO = "ee5539f3f9efa96d"
BYTES_TESTIGO = 672
SHA16_PARAMS = "9983b3d25a68f032"
SHA16_CONFIGS = "c7508e0430319162"

DIR_GRUPOS = AQUI / "data" / "pestana2_circular_corregida_20261011"
CSV_CANONICO = AQUI / "data" / "medidas_aN_circular_corregida_20261011.csv"
CSV_RESUMEN = DIR_GRUPOS / "resumen_pestana2.csv"

POL = "circular"
DL = 0.0
PASOS = 300
N_LISTA = [1, 2, 4, 8, 16]
SIGMAS = [0.000, 0.125, 0.250, 0.375, 0.500, 0.625,
          0.750, 1.000, 1.250, 1.500, 2.000, 3.000]
BETA_OBJETIVO = 0.45
CRUCE_PICO = 0.527493      # rad — beta_pico (col 6 del resumen de fasores): lo que SE ADJUDICA
CRUCE_FOCO = 0.554987      # rad — biseccion FOCO: el OTRO objeto, se reporta, no se adjudica
RAD_A_FS = 0.4247
TOL_REJILLA = 0.125        # rad — un paso de la rejilla pre-registrada

# --- LOS 12 VECTORES DE FASE PRE-REGISTRADOS (sellados en el pre-registro ANTES del disparo) ---
VECTORES: dict[str, list[float]] = {
    "0.000": [0.0] * 16,
    "0.125": [0.0687094893, -0.0511464500, 0.1457727101, -0.1936910200,
              0.0270471764, 0.0599394537, 0.0202919117, 0.3875863407,
              0.0405015762, 0.1124333587, 0.0800698401, 0.1032299037,
              0.0463516644, -0.0724911502, 0.0649244155, -0.0570627276],
    "0.250": [-0.0431841272, -0.0409505238, 0.2020075129, 0.0560316124,
              -0.1858981660, 0.1264433242, -0.2174277351, -0.1777060927,
              0.0490389421, -0.1111397639, -0.2002293579, -0.2348987494,
              0.2407786446, 0.2473828760, 0.0594420265, -0.5724696814],
    "0.375": [-0.2448402789, -0.1010270999, 0.3935280420, -0.2544353890,
              -0.0962903718, 0.0871594835, 0.1487684174, 0.6068850642,
              0.4481967974, 0.3178929566, 0.1593717958, -0.3066721525,
              0.4035229184, 0.2044700624, -0.5750722043, 0.2800557096],
    "0.500": [-1.0457097788, -0.7179268958, 0.0854004516, 0.5917371508,
              0.1897057480, 0.1512492204, -0.0725764976, -0.3692159092,
              0.6339738552, 0.0584446990, -0.2868277528, 0.2708580807,
              0.0289701708, -0.1562016589, 0.0901860093, 0.0237523229],
    "0.625": [0.9282634506, 0.2869560109, 0.5767539131, 0.2462173280,
              -0.4479256941, 0.7162137004, 0.0142115579, 0.9579540132,
              -1.0206606664, 0.8148137699, -0.0111347949, -0.0333202131,
              0.2630244318, 0.1315405883, 0.1566418052, 0.0945886376],
    "0.750": [-1.0643893646, 1.2289425736, -0.6097832253, 0.9272718506,
              -0.4356807574, 0.3217569600, -1.3150424186, -1.2558588681,
              0.8814997520, -0.1212054426, 0.0004251633, 0.1060158071,
              -0.0581915393, 0.4480939209, 0.0058251556, 0.2115525407],
    "1.000": [0.2627682938, -0.0679180644, -0.7119141605, -1.0486495126,
              0.2624714856, -0.0388888241, 1.1625632919, -1.0297946618,
              1.1381032717, 0.0767233646, 0.9964648575, 0.0187422780,
              0.8319190073, -0.1589536061, -0.0193530891, -0.6838990471],
    "1.250": [-1.1523701678, 0.4063829577, 0.0319514395, 0.4069726438,
              -1.5368899445, 0.2647447956, 2.6553934473, 0.0497335732,
              -0.5130900698, -0.1388801368, -0.6529383042, -2.9426626889,
              1.9715826465, -1.1631912718, 0.3796768825, -0.4612170713],
    "1.500": [-0.4256202638, 1.6485738898, -0.8654894001, 0.6764657283,
              -1.9309570106, -0.0240598653, -0.0169402350, 0.2389215330,
              -1.4513056881, 1.6477137420, -2.6149222633, -0.3101579469,
              -0.2261687906, 1.2633529736, 0.4181257127, -0.0349364120],
    "2.000": [1.0046694060, 2.3072713633, -2.9525801791, 1.6867654898,
              2.4156468327, 0.2006460804, -0.4740029788, -0.4104127941,
              -1.0948410817, 0.3369087688, 2.0890267885, 0.4836179447,
              2.0019927099, 1.7828828432, -0.8504775877, 0.7655877911],
    "3.000": [1.3156151504, 3.1715338970, 0.2065893287, 0.3959933023,
              -1.5973125467, 3.3118334216, 4.2110540191, -0.4801298387,
              1.3462246852, 4.1533929732, 1.5807466442, -4.5130102845,
              -1.3525799930, -3.3915155448, 2.6007503456, 0.0317296495],
}

RE_FDTD = re.compile(r"a_fdtd=\s*([0-9eE.+-]+)")
RE_CENTRO = re.compile(r"centro=\s*([0-9eE.+-]+)")
RE_N = re.compile(r"^N=\s*(\d+)")  # el log imprime «N= 1 …» (espacio tras el signo):
# la adyacencia «N=<int>» era una suposicion del metro, no una propiedad del objeto.


def ahora() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha16(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]


def guarda() -> None:
    b = INSTRUMENTO.read_bytes()
    h = hashlib.sha256(b).hexdigest()[:16]
    lin = b.count(b"\n")
    print(f"G1 instrumento : {INSTRUMENTO.name}  sha16={h}  {len(b)} B  {lin} l")
    print(f"G1 esperado    : {SHA16_INSTR}  {BYTES_INSTR} B  {LINEAS_INSTR} l")
    if (h, len(b), lin) != (SHA16_INSTR, BYTES_INSTR, LINEAS_INSTR):
        raise SystemExit("G1 ROJO: el instrumento no es el parcheado congelado")
    for p, esperado in ((PARCHE, SHA16_PARCHE), (DIFF, SHA16_DIFF),
                        (PARAMS, SHA16_PARAMS), (CONFIGS, SHA16_CONFIGS),
                        (TESTIGO, SHA16_TESTIGO)):
        h2 = sha16(p)
        if h2 != esperado:
            raise SystemExit(f"G1 ROJO: {p.name} sha16={h2} esperado={esperado}")
        print(f"G1 OK          : {p.name:30s} sha16={h2}")
    if TESTIGO.stat().st_size != BYTES_TESTIGO:
        raise SystemExit(f"G1 ROJO: el testigo cambio de tamano ({TESTIGO.stat().st_size} B)")
    print(f"G1 pre-registro: {PRE_REG.name} sha16={sha16(PRE_REG)}  {PRE_REG.stat().st_size} B")
    print(f"G1 hora        : T_UTC={ahora()}")
    if len(VECTORES) != 12 or any(len(v) != 16 for v in VECTORES.values()):
        raise SystemExit("G1 ROJO: los vectores sellados no son 12 x 16")
    print("G1 OK          : 12 vectores x 16 componentes (solo del pre-registro, nada recalculado)")


def abre_grupo(sigma: float) -> dict:
    clave = f"{sigma:.3f}"
    vec = VECTORES[clave]
    csv = DIR_GRUPOS / f"sigma_{clave}.csv"
    log = DIR_GRUPOS / f"log_sigma_{clave}.txt"
    fases = ",".join(repr(x) for x in vec)
    cmd = [sys.executable, "-B", str(INSTRUMENTO), "--todo", "--pol", POL,
           "--fases", fases, "--sigma-phi", clave, "--salida", str(csv)]
    t0 = time.time()
    r = subprocess.run(cmd, cwd=str(RAIZ), capture_output=True, text=True)
    pared = time.time() - t0
    log.write_text("# " + " ".join(cmd) + "\n"
                   f"# T_UTC_fin={ahora()}  rc={r.returncode}  pared={pared:.1f} s\n"
                   + r.stdout + "\n# --- stderr ---\n" + r.stderr, encoding="utf-8")
    d: dict = dict(sigma=clave, rc=r.returncode, pared=pared,
                   csv=str(csv), log=str(log))
    if r.returncode != 0:
        print(f"  sigma={clave}: rc={r.returncode} ROJO (ver {log.name})")
        return d
    lineas = csv.read_text(encoding="utf-8").splitlines()
    cab = [l for l in lineas if l.startswith("#")]
    cuerpo = [l for l in lineas if l.strip() and not l.startswith("#")]
    eco = None
    for l in cab:
        if "fases_por_haz =" in l:
            bruto = l.split("fases_por_haz =", 1)[1].strip()
            eco = [float(x) for x in bruto.strip("[]").split(",") if x.strip()]
    filas = [l.split(",") for l in cuerpo]
    ok_eco = (eco == vec)
    ok_filas = (len(filas) == len(N_LISTA)) and all(
        len(f) == 3 and f[2].strip() == clave for f in filas)
    d.update(sha16=sha16(csv), bytes=csv.stat().st_size, filas=len(filas),
             ok_eco=ok_eco, ok_filas=ok_filas,
             a={int(f[0]): float(f[1]) for f in filas} if ok_filas else {})
    print(f"  sigma={clave}: rc=0  {d['filas']} filas  "
          f"eco_vector={'OK' if ok_eco else 'ROJO'}  sha16={d['sha16']}  "
          f"{d['bytes']} B  pared={pared:.1f} s")
    if not (ok_eco and ok_filas):
        raise SystemExit(f"G2/G3 ROJO en sigma={clave}: eco={ok_eco} filas={ok_filas}")
    return d


def beta(pares: list[tuple[int, float]]) -> float:
    """OLS de log a contra log N — la MISMA formula del falsador."""
    xs = [math.log(n) for n, _ in pares]
    ys = [math.log(a) for _, a in pares]
    k = len(xs)
    mx = sum(xs) / k
    my = sum(ys) / k
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)


def cruce(sig: list[float], betas: list[float], objetivo: float = BETA_OBJETIVO):
    for k in range(len(sig) - 1):
        if betas[k] == betas[k + 1]:
            continue
        if (betas[k] - objetivo) * (betas[k + 1] - objetivo) <= 0:
            x = sig[k] + (sig[k + 1] - sig[k]) * (objetivo - betas[k]) / (betas[k + 1] - betas[k])
            return x, sig[k], sig[k + 1]
    return None, None, None


def une() -> dict:
    grupos = []
    for s in SIGMAS:
        clave = f"{s:.3f}"
        csv = DIR_GRUPOS / f"sigma_{clave}.csv"
        if not csv.exists():
            raise SystemExit(f"FALTA el grupo sigma={clave}: {csv}")
        filas = [l.split(",") for l in csv.read_text(encoding="utf-8").splitlines()
                 if l.strip() and not l.startswith("#")]
        if len(filas) != len(N_LISTA) or not all(
                len(f) == 3 and f[2].strip() == clave for f in filas):
            raise SystemExit(f"G3 ROJO: el grupo sigma={clave} no tiene 5 filas con clave propia")
        if [int(f[0]) for f in filas] != N_LISTA:
            raise SystemExit(f"G3 ROJO: el grupo sigma={clave} no trae los 5 N en orden")
        grupos.append((clave, filas, sha16(csv)))
    nfilas = sum(len(f) for _, f, _ in grupos)
    if nfilas != 12 * len(N_LISTA):
        raise SystemExit(f"K4 ROJO: filas={nfilas}, esperado {12 * len(N_LISTA)}")
    cab = [
        "# medidas_aN_circular_corregida_20261011.csv — PESTANA 2 (circular corregida, sigma_phi por haz)",
        "# LECTURA = PICO: a_medido = (e/(m_e c omega)) * max_(r en |r| <= w0, t <= 260) |E(r,t)|",
        f"# MOTOR = sim/runner_2d3v.py sha16={SHA16_INSTR} ({LINEAS_INSTR} l, {BYTES_INSTR} B) = "
        f"congelado 368627d18d83d253 + parche sim/parche_salida_fases.py sha16={SHA16_PARCHE} ; "
        f"diff = sim/salida_fases.diff sha16={SHA16_DIFF}",
        f"# GEOMETRIA = sim/params.py sha16={SHA16_PARAMS} + sim/configs.json sha16={SHA16_CONFIGS}",
        f"# PARAMETROS: pol = {POL} ; dl = {DL} ; PASOS = {PASOS} ; N_LISTA = {N_LISTA} ; "
        "Omega_foco = |r| <= 80 celdas = 2 lambda_L ; malla 480x480 ; dx = lambda_L/40 ; CFL = 0.6",
        f"# PRE-REGISTRO (sellado antes): sim/{PRE_REG.name} sha16={sha16(PRE_REG)}",
        f"# TESTIGO del control sigma=0: sim/medidas_aN_circular.csv sha16={SHA16_TESTIGO}",
        "# UNIDAD: fila del CSV ; UNIVERSO: este archivo ; VENTANA: reloj UTC",
        "# CLAVE por fila = sigma_phi (rad) ; 12 grupos x 5 N = 60 filas",
        "# columnas: sigma_phi,N,a_medido",
    ]
    out = "\n".join(cab) + "\n"
    for clave, filas, h in grupos:
        out += f"# --- grupo sigma_phi = {clave} rad ; sha16_grupo = {h} ; filas = {len(filas)}\n"
        for f in filas:
            out += f"{clave},{f[0]},{f[1]}\n"
    CSV_CANONICO.write_text(out, encoding="utf-8")
    print(f"CANONICO escrito: {CSV_CANONICO.name}  sha16={sha16(CSV_CANONICO)}  "
          f"{CSV_CANONICO.stat().st_size} B  filas_datos={nfilas}  (K4 {'OK' if nfilas == 60 else 'ROJO'})")
    return dict(grupos=grupos, nfilas=nfilas)


def informe() -> None:
    print("\n" + "=" * 92)
    print("INFORME PESTANA 2 — sigma_phi por haz, lectura PICO")
    print("=" * 92)
    # --- lee el canonico ---
    datos: dict[str, list[tuple[int, float]]] = {f"{s:.3f}": [] for s in SIGMAS}
    for l in CSV_CANONICO.read_text(encoding="utf-8").splitlines():
        if not l.strip() or l.startswith("#"):
            continue
        s, n, a = l.split(",")
        datos[s].append((int(n), float(a)))

    # --- K0: el testigo, comparado archivo contra archivo ---
    wit = {}
    for l in TESTIGO.read_text(encoding="utf-8").splitlines():
        if not l.strip() or l.startswith("#"):
            continue
        n, a = l.split(",")[0], l.split(",")[1]
        wit[int(n)] = a.strip()
    g0 = datos["0.000"]
    k0 = [(n, f"{a:.10f}" == wit[n]) for n, a in g0]
    print(f"K0 sigma=0.000 vs testigo {TESTIGO.name} (sha16={sha16(TESTIGO)}):")
    for n, ok in k0:
        a = dict(g0)[n]
        print(f"   N={n:2d}  medido={a:.10f}  testigo={wit[n]:>16s}  {'IGUAL' if ok else 'DISTINTO'}")
    print(f"   K0 = {'VERDE (bit-for-bit)' if all(o for _, o in k0) else 'ROJO'}")

    # --- K2 desde los logs (identidad |P|+|M| >= |P+M|) ---
    k2_total = k2_ok = 0
    peor = None
    for s in SIGMAS:
        lg = DIR_GRUPOS / f"log_sigma_{s:.3f}.txt"
        if not lg.exists():
            continue
        for ln in lg.read_text(encoding="utf-8").splitlines():
            if not ln.startswith("N="):
                continue
            m1, m2 = RE_FDTD.search(ln), RE_CENTRO.search(ln)
            if not (m1 and m2):
                continue
            mn = RE_N.match(ln)
            if not mn:
                continue
            pico, cent = float(m1.group(1)), float(m2.group(1))
            k2_total += 1
            if pico >= cent:
                k2_ok += 1
            if peor is None or (pico - cent) < peor[2]:
                peor = (s, int(mn.group(1)), pico - cent)
    print(f"K2 (a_PICO >= a_FOCO) = {k2_ok}/{k2_total} corridas ; margen minimo = "
          f"{peor[2]:+.6f} (sigma={peor[0]:.3f}, N={peor[1]})"
          f"  [IDENTIDAD declarada, NO evidencia]")

    # --- betas por sigma ---
    print(f"\n{'sigma':>6} {'beta_5p':>9} {'beta_4p':>9} | "
          + " ".join(f"{'a_' + str(n):>13s}" for n in N_LISTA))
    b5, b4, sig = [], [], []
    for s in SIGMAS:
        pares = sorted(datos[f"{s:.3f}"])
        v5 = beta(pares)
        v4 = beta([p for p in pares if p[0] >= 2])
        b5.append(v5)
        b4.append(v4)
        sig.append(s)
        print(f"{s:6.3f} {v5:9.6f} {v4:9.6f} | "
              + " ".join(f"{a:13.10f}" for _, a in pares))
    w5, w4 = beta(sorted(datos["0.000"])), beta([p for p in sorted(datos["0.000"]) if p[0] >= 2])
    print(f"\n  (referencia del testigo: beta_5p = {w5:.6f} ; beta_4p = {w4:.6f})")

    # --- K3: el cruce ---
    x5, s5a, s5b = cruce(sig, b5)
    x4, s4a, s4b = cruce(sig, b4)
    print(f"\nK3 — cruce de beta = {BETA_OBJETIVO}:")
    for nom, x, sa, sb in (("beta_5p", x5, s5a, s5b), ("beta_4p", x4, s4a, s4b)):
        if x is None:
            print(f"   {nom}: NO HAY CRUCE en la rejilla")
            continue
        d = abs(x - CRUCE_PICO)
        print(f"   {nom}: x = {x:.6f} rad = {x * RAD_A_FS:.4f} fs  "
              f"(entre sigma={sa:.3f} y {sb:.3f})  |x - {CRUCE_PICO} (PICO) = {d:.6f} rad"
              f"  -> {'DENTRO' if d <= TOL_REJILLA else 'FUERA'} de la rejilla ({TOL_REJILLA} rad)")
    print(f"   FOCO (el OTRO objeto, biseccion) = {CRUCE_FOCO:.6f} rad = "
          f"{CRUCE_FOCO * RAD_A_FS:.4f} fs — se REPORTA, no se adjudica")

    # --- resumen a disco ---
    cab = ["# resumen_pestana2.csv — PESTANA 2 (circular corregida)",
           f"# instrumento sha16={SHA16_INSTR} ; pre-registro sha16={sha16(PRE_REG)}",
           f"# LECTURA = PICO ; M = 1 por (N, sigma) (NO es RMS) ; pol = {POL} ; dl = {DL}",
           "sigma,beta_5p,beta_4p,a_1,a_2,a_4,a_8,a_16"]
    cuerpo = []
    for k, s in enumerate(SIGMAS):
        d = dict(sorted(datos[f"{s:.3f}"]))
        cuerpo.append(f"{s:.3f},{b5[k]:.6f},{b4[k]:.6f}," +
                      ",".join(f"{d[n]:.10f}" for n in N_LISTA))
    cola = [f"# cruce beta=0.45 beta_5p = {x5:.6f} rad ({x5 * RAD_A_FS:.4f} fs)"
            if x5 is not None else "# cruce beta=0.45 beta_5p = SIN CRUCE",
            f"# cruce beta=0.45 beta_4p = {x4:.6f} rad ({x4 * RAD_A_FS:.4f} fs)"
            if x4 is not None else "# cruce beta=0.45 beta_4p = SIN CRUCE",
            f"# referencia PICO adjudicada = {CRUCE_PICO:.6f} rad ({CRUCE_PICO * RAD_A_FS:.4f} fs)",
            f"# referencia FOCO (otro objeto) = {CRUCE_FOCO:.6f} rad ({CRUCE_FOCO * RAD_A_FS:.4f} fs)",
            f"# K2 = {k2_ok}/{k2_total} ; K0 = {'VERDE' if all(o for _, o in k0) else 'ROJO'}",
            f"# hora = {ahora()}"]
    CSV_RESUMEN.write_text("\n".join(cab + cuerpo + cola) + "\n", encoding="utf-8")
    print(f"\nRESUMEN escrito: {CSV_RESUMEN.name}  sha16={sha16(CSV_RESUMEN)}  "
          f"{CSV_RESUMEN.stat().st_size} B")
    print(f"CIERRE T_UTC={ahora()}")


def main() -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--todo", action="store_true")
    ap.add_argument("--sigma", type=float, default=None)
    ap.add_argument("--unir", action="store_true")
    ap.add_argument("--trabajadores", type=int, default=4)
    a = ap.parse_args()
    guarda()
    DIR_GRUPOS.mkdir(parents=True, exist_ok=True)
    if a.sigma is not None:
        s = round(a.sigma, 3)
        if f"{s:.3f}" not in VECTORES:
            raise SystemExit(f"sigma={s} no esta en la rejilla pre-registrada")
        print(f"\nARRANQUE T_UTC={ahora()}  modo=UN_SIGMA  sigma={s:.3f}  trabajadores=1")
        abre_grupo(s)
        print(f"CIERRE T_UTC={ahora()}")
    elif a.todo:
        print(f"\nARRANQUE T_UTC={ahora()}  modo=TODO  sigmas={len(SIGMAS)}  "
              f"trabajadores={a.trabajadores}")
        t0 = time.time()
        if a.trabajadores <= 1:
            for s in SIGMAS:
                abre_grupo(s)
        else:
            with ProcessPoolExecutor(max_workers=a.trabajadores) as ex:
                list(ex.map(abre_grupo, SIGMAS))
        print(f"CIERRE T_UTC={ahora()}  pared_total={time.time() - t0:.1f} s")
    if a.unir:
        print(f"\nUNION T_UTC={ahora()}")
        une()
        informe()
    if not (a.todo or a.sigma is not None or a.unir):
        ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
