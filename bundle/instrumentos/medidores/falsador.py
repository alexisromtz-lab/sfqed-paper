#!/usr/bin/env python3
"""sim/falsador.py -- el gate del escalado 1/N.

LEE   sim/configs.json (lo que PREDICE el modelo) y, si existe, una MEDICION
      sim/medidas_aN.csv con dos columnas: N,a_medido  (una linea por caso).
JUZGA contra la banda PRE-REGISTRADA en sim/PROTOCOLO_1overN.md:
      beta = d log(a) / d log(N)  debe caer en [0.45, 0.55]
      muere si beta <= 0.35 o beta >= 0.65
      muere si |a(N)/(a(1) sqrt(N)) - 1| > 0.20 en algun N
SALE  0 = verde ; 1 = rojo ; 2 = SIN MEDIDA (ni verde ni rojo: no hay objeto)

CONTROLES (no requieren PIC: generan la medicion sinteticamente)
  python3 -B sim/falsador.py --sintetico 0.5   espera VERDE (exit 0)
  python3 -B sim/falsador.py --sintetico 1.0   espera ROJO  (exit 1)

Un gate que imprime ROJO y sale 0 informa, no protege (D21); por eso el
veredicto y el exit code son el mismo hecho.
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

AQUI = Path(__file__).resolve().parent
CONFIGS = AQUI / "configs.json"
MEDIDAS = AQUI / "medidas_aN.csv"
TOL_RATIO = 0.20
BANDA_OK = (0.45, 0.55)
BANDA_MUERTE = (0.35, 0.65)


def leer_configs() -> dict:
    if not CONFIGS.exists():
        print(f"SIN PREDICHO: falta {CONFIGS} -> corre gen_configs.py")
        sys.exit(2)
    return json.loads(CONFIGS.read_text(encoding="utf-8"))


def leer_medidas() -> list[tuple[float, float]] | None:
    if not MEDIDAS.exists():
        return None
    filas = []
    for ln, linea in enumerate(MEDIDAS.read_text(encoding="utf-8").splitlines(), 1):
        t = linea.strip()
        if not t or t.startswith("#"):
            continue
        partes = [p.strip() for p in t.replace(";", ",").split(",")]
        if len(partes) < 2:
            raise ValueError(f"{MEDIDAS}:{ln}: se esperan N,a_medido -> {linea!r}")
        filas.append((float(partes[0]), float(partes[1])))
    return filas or None


def beta_loglog(pares: list[tuple[float, float]]) -> float:
    """Pendiente por minimos cuadrados de log a contra log N."""
    xs = [math.log(n) for n, _ in pares]
    ys = [math.log(a) for _, a in pares]
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    return num / den


def main() -> int:
    args = sys.argv[1:]
    s = leer_configs()
    fails: list[str] = []

    sint = None
    if "--sintetico" in args:
        i = args.index("--sintetico")
        if i + 1 >= len(args):
            print("falta el valor de --sintetico")
            return 2
        sint = float(args[i + 1])

    if sint is not None:
        a1 = s["a_ref_N_1"]
        pares = [(float(n), a1 * float(n) ** sint) for n in s["N_LISTA"]]
        origen = f"SINTETICO a(N) = a_ref * N**{sint}  (control del metro)"
    else:
        pares = leer_medidas()
        origen = f"medido en {MEDIDAS}"

    print(f"hora = {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")
    print(f"UNIVERSO DECLARADO: {s['UNIVERSO DECLARADO']}")
    print(f"predicho por el modelo: {s['modelo']}")
    print(f"medicion usada: {origen}")
    if pares is None:
        print("VEREDICTO: SIN MEDIDA -- no hay a(N) que juzgar (ni verde ni rojo).")
        print(f"  escribe {MEDIDAS} con lineas 'N,a_medido' y vuelve a correr.")
        return 2

    print("--- (N, a) ---")
    for n, a in pares:
        print(f"  N={n:<6g} a={a:.6g}")
    if len(pares) < 2:
        print("VEREDICTO: SIN MEDIDA -- con un solo N no hay pendiente.")
        return 2

    beta = beta_loglog(pares)
    print(f"--- pendiente medida ---\n  beta = {beta:.6f}")
    print(f"  banda PRE-REGISTRADA = [{BANDA_OK[0]}, {BANDA_OK[1]}] ; "
          f"muerte si <= {BANDA_MUERTE[0]} o >= {BANDA_MUERTE[1]}")

    if beta <= BANDA_MUERTE[0] or beta >= BANDA_MUERTE[1]:
        fails.append(f"beta = {beta:.4f} fuera de la zona de muerte "
                     f"[{BANDA_MUERTE[0]}, {BANDA_MUERTE[1]}]")
    elif not (BANDA_OK[0] <= beta <= BANDA_OK[1]):
        fails.append(f"beta = {beta:.4f} cae en la banda gris "
                     f"(fuera de [{BANDA_OK[0]}, {BANDA_OK[1]}] y dentro de la de muerte)")

    print("--- desviacion por N  |a(N)/(a(1) sqrt(N)) - 1| ---")
    ref = None
    for n, a in pares:
        if n == 1.0:
            ref = a
            break
    if ref is None:
        print("  (no hay N=1 en la medicion: no se puede anclar el cociente)")
        fails.append("sin N=1 no se puede medir el cociente contra sqrt(N)")
    else:
        for n, a in pares:
            desv = abs(a / (ref * math.sqrt(n)) - 1.0)
            marca = "OK  " if desv <= TOL_RATIO else "ROJO"
            print(f"  {marca} N={n:<6g} desv = {desv:.4f} (tol {TOL_RATIO})")
            if desv > TOL_RATIO:
                fails.append(f"N={n:g}: desviacion {desv:.4f} > {TOL_RATIO}")

    if fails:
        print(f"VEREDICTO: ROJO -- {len(fails)} fallo(s):")
        for f in fails:
            print("  - " + f)
        return 1
    print("VEREDICTO: VERDE -- beta dentro de la banda pre-registrada y sin "
          "desviacion por N.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
