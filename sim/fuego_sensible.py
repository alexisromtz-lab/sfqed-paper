#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sim/fuego_sensible.py -- CONDUCTOR B': el filtro analitico corre ANTES del solver.

ORDEN DEL DUENO (verbatim, 11-Oct-2026): "Se cablea B'; el sello de
`sim/maxwell2d.py` permanece cerrado e inmutable en `1db75ea7b0b8cba4`."

CONTRATO DE SALIDA (fijado por el dueno ANTES de escribirse esta pieza):
  RC 0 Conforme   el filtro intercepta      -> VEREDICTO: DEDUCIDO_ANALITICO
                  el FDTD corre y converge  -> VEREDICTO: FDTD_COMPLETO
  RC 1 Fractura   el observable numerico contradice las cotas, o falla una afirmacion
                  fisica de este conductor.
  RC 2 Fallo de metro  el filtro levanta ValueError (fail-closed), o falta
                  interprete/dato declarado.
La distincion FDTD vs DEDUCIDO **no** viaja en el codigo de retorno (los dos son
RC 0): viaja en el VEREDICTO. Reusar RC 2 para una corrida degenerada seria mentir
sobre la clase: en este arbol RC 2 ya significa "el metro no puede leer"
(`sim/filtro_analitico.py:control`), y una corrida degenerada es una MEDICION
(deduccion por Cauchy-Schwarz), no una averia.

POR QUE B' Y NO A (medido, no opinado):
  1. `maxwell2d.correr()` NO tiene `alpha` en su firma (l.283, unica firma del motor):
     cablear el filtro DENTRO del solver pidiendo alpha por ahi seria imposibilidad
     SINTACTICA, no solo rotura de hash.
  2. Un archivo NUEVO en `sim/` esta FUERA del universo del manifiesto del bundle (las
     rutas de `bundle/HASHES.sha256` son relativas a `bundle/`) => no fabrica huerfano
     alli, y `sim/maxwell2d.py` queda byte a byte intacto.
  3. La ruta de intercepto NO importa ni ejecuta el solver: se verifica sobre
     `sys.modules` y, en `--control`, en SUBPROCESO (interprete limpio).

EL OBSERVABLE R (uno solo, y el mismo en las dos rutas): R = a_inv / |E|, adimensional.
  Con F = eps0/2 (E^2 - c^2 B^2) y G = eps0 c E.B, la identidad de Lagrange da
  4(F^2 + G^2)/eps0^2 = (E^2 + c^2 B^2)^2 - 4 |E x cB|^2 <= (E^2 + c^2 B^2)^2, de donde
  sqrt(F^2 + G^2) <= (eps0/2)(E^2 + c^2 B^2) y por lo tanto
      a_inv = sqrt( sqrt(F^2 + G^2) + F ) / sqrt(eps0) <= |E|   PUNTO A PUNTO.
  De ahi la cota, que es algebra y no umbral:    0 <= R <= 1
  y sus DOS extremos son EXACTAMENTE las dos razones del filtro:
      B = 0        (antinodo)  => F = eps0/2 |E|^2, G = 0 => R = 1.000000  (Cauchy-Schwarz
                     saturada; es `filtro_analitico.cota_deducida_antinodo()`)
      F = G = 0    (onda plana transversal) => R = 0.000000  (el docstring de la regla 2
                     del filtro lo declara: "forzando a_inv = 0 continuo")
  La ruta FDTD no deduce: LEE lo que el motor mide, `corrida["a_inv_rel_al_pico"]`
  (sim/maxwell2d.py:376) = max_t ( max_ventana a_inv / max_ventana |E| ) con las dos
  ventanas en el MISMO paso => R <= 1 por la misma algebra. Los dos sellos ya lo
  cumplen: etapa1_contra 0.99208992 · etapa1_colineal 0.99951328.

DIVERGENCIA DECLARADA (se declara, no se adjudica): el contrato imprime
`R: 1.000000` en el intercepto. Aqui se imprime 1.000000 si la razon es
`saturacion_antinodo` y 0.000000 si es `semiangulo_nulo`, porque ese segundo caso es el
OTRO extremo de la MISMA cota y el filtro ya declara a_inv = 0 para el. No se decide en
nombre del dueno: si quiere el literal 1.000000 en las dos, se cambia en una linea
(`cota_deducida`).

DOS PAPELES, UN SOLO alpha: el FDTD no lleva alpha (hecho 1) y el cono de semiangulo
alpha vive en la familia `estrella` de `sim/field_solver.py`. La rama nominal lee el
CAMPO del cono con `field_solver.haces/medir` y lee R del FDTD. No se mezclan: se
imprimen los dos, cada uno con su fuente declarada, y el R del VEREDICTO es el del FDTD
(asi lo fija el contrato: la ruta nominal es la del FDTD).

UNIVERSO DECLARADO: la terna (modo, alpha_deg, N) por corrida; los CUATRO nombres de modo
del motor (`colineal` | `colineal-nulo` | `contra` | `contra-nulo`) mas el catalogo de
familias de `field_solver` (`copropagante` | `coaxial_contra` | `estrella`); y el
observable unico R = a_inv/|E| en [0, 1]. No hay malla propia: la malla (480x480,
dx = lambda_L/40) y la ventana de medida (celdas [100, 380]) son las DECLARADAS por el
motor y no se re-declaran aqui.
MOTOR: python3 -B. stdlib en la ruta de intercepto; numpy solo dentro de la rama nominal.
UNIDAD: corrida (una terna). R adimensional. VENTANA: la hora UTC impresa antes de toda
cifra.

Uso:
  python3 -B sim/fuego_sensible.py                                   # contra, alpha 30, N 4 -> intercepta
  python3 -B sim/fuego_sensible.py --modo colineal --alpha 26.5651 --N 4
  python3 -B sim/fuego_sensible.py --modo colineal --alpha 0 --N 4    # semiangulo nulo
  python3 -B sim/fuego_sensible.py --control
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import sys
import time
from pathlib import Path

AQUI = Path(__file__).resolve().parent
if str(AQUI) not in sys.path:
    sys.path.insert(0, str(AQUI))

from filtro_analitico import (  # noqa: E402  (la funcion pura tiene UNA casa)
    MODOS_DEL_MOTOR,
    RAZON_ANTINODO,
    RAZON_SEMIANGULO,
    cota_deducida_antinodo,
    evaluar_sensibilidad_previa,
)

SELLO_DEL_SOLVER = "1db75ea7b0b8cba4"   # sim/maxwell2d.py, no se toca
CONDUCTOR = "sim/fuego_sensible.py"
DEDUCCIONES = AQUI / "data" / "deducciones"   # carpeta NUEVA; no pisa ningun archivo
TOL_COTA = 1e-9                          # solo error de redondeo en el borde de la cota

# Slugs del contrato. Las razones verbatim viven en el filtro; aqui solo se nombran
# cortas para la linea de veredicto. La trazabilidad va en los dos sentidos.
SLUG_ANTINODO = "saturacion_antinodo"
SLUG_SEMIANGULO = "semiangulo_nulo"
SLUG = {RAZON_ANTINODO: SLUG_ANTINODO, RAZON_SEMIANGULO: SLUG_SEMIANGULO}

# La familia del cono es `estrella` y NO se mapea desde el modo: es la unica familia de
# `field_solver` donde `alpha_deg` es parametro del objeto (`copropagante` y
# `coaxial_contra` lo reciben y lo descartan; ver `haces()` l.124). Se declara, no se mapea.

VERSION_DE_SALIDA = 1


# ------------------------------------------------------------------ utilidades
def sha16_conductor() -> str:
    """sha16 del PROPIO archivo leido en el momento de correr (no un literal).

    Un sha escrito a mano dentro de la pieza describe su version anterior; uno leido
    en tiempo de corrida mide el objeto que efectivamente corre.
    """
    try:
        return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()[:16]
    except OSError as exc:                                  # pragma: no cover
        return "sin-medida:%s" % exc.strerror


def modulos_del_solver_cargados() -> list:
    """Los modulos que la ruta de intercepto NO debe haber cargado."""
    return [m for m in ("maxwell2d", "field_solver", "numpy", "params") if m in sys.modules]


def descomponer_modo(modo: str) -> tuple:
    """`contra-nulo` -> (`contra`, True). El sufijo es del motor, no de aqui."""
    nulo = modo.endswith("-nulo")
    return (modo[: -len("-nulo")] if nulo else modo), nulo


def cota_deducida(razon: str) -> float:
    """R deducida por cada regla. Ver la algebra de la cota en el docstring del modulo."""
    if razon == RAZON_ANTINODO:
        return cota_deducida_antinodo()
    if razon == RAZON_SEMIANGULO:
        return 0.0
    raise ValueError("razon de saturacion desconocida: %r" % (razon,))


def revisar_cotas(R: float, a_medido: float, pasos: int) -> list:
    """Afirmaciones fisicas de la ruta FDTD. Devuelve la lista de fracturas (vacia = OK).

    Se aisla en una funcion pura para que `--control` pueda probar que sabe ENROJECER
    sin pagar una corrida del solver: un gate sin `assert` detras informa, no protege.
    """
    fracturas = []
    if not (math.isfinite(R) and -TOL_COTA <= R <= 1.0 + TOL_COTA):
        fracturas.append(
            "cota de Cauchy-Schwarz violada: R = %r fuera de [0, 1] "
            "(a_inv <= |E| punto a punto)" % (R,)
        )
    if not (math.isfinite(a_medido) and a_medido > 0.0):
        fracturas.append("a_medido no finito o no positivo: %r" % (a_medido,))
    if int(pasos) < 1:
        fracturas.append("ventana vacia: pasos = %r" % (pasos,))
    return fracturas


def _bloque_entrada(modo, alpha_deg, N, tol_rango) -> dict:
    return {
        "modo": modo,
        "alpha_deg": alpha_deg,
        "N": int(N),
        "tol_rango": tol_rango,
    }


def _cabecera(universo: str) -> dict:
    return {
        "T_UTC": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "UNIVERSO DECLARADO": universo,
        "MOTOR": "python3 -B",
        "UNIDAD": "corrida (una terna modo/alpha/N); R = a_inv/|E| adimensional en [0, 1]",
        "VENTANA": "la hora UTC de este mismo bloque",
        "conductor": CONDUCTOR,
        "sha16_conductor": sha16_conductor(),
        "sello_del_solver": SELLO_DEL_SOLVER,
        "version_de_salida": VERSION_DE_SALIDA,
    }


def imprimir_bloque(b: dict) -> None:
    for k in ("T_UTC", "UNIVERSO DECLARADO", "MOTOR", "UNIDAD", "VENTANA"):
        print("%s: %s" % (k, b[k]))
    for k in ("conductor", "sha16_conductor", "sello_del_solver"):
        print("%s: %s" % (k, b[k]))


# ------------------------------------------------------------------ ruta 1: deduccion
def emitir_deduccion(modo, alpha_deg, N, tol_rango, razon, escribir=True) -> dict:
    """Registro de deduccion analitica. Aqui el solver NO esta importado ni se corre."""
    slug = SLUG[razon]
    R = cota_deducida(razon)
    rec = _cabecera(
        "el algebra del invariante eq:ab en las unidades del motor, SIN malla, SIN campo "
        "y SIN tiempo: la cota se resuelve por deduccion y el FDTD no se invoca."
    )
    rec.update({
        "entrada": _bloque_entrada(modo, alpha_deg, N, tol_rango),
        "veredicto": "DEDUCIDO_ANALITICO",
        "RC": 0,
        "razon": razon,
        "razon_slug": slug,
        "R": round(R, 6),
        "R_unidad": "a_inv / |E| (adimensional, 0 <= R <= 1)",
        "FDTD": "NO INVOCADO",
        "modulos_del_solver_cargados": modulos_del_solver_cargados(),
    })
    imprimir_bloque(rec)
    print("entrada: modo=%s alpha_deg=%s N=%d tol_rango=%r" % (modo, alpha_deg, int(N), tol_rango))
    print("razon: %s" % razon)
    print("FDTD: NO INVOCADO (el filtro intercepto antes de importar el solver)")
    print("modulos del solver en sys.modules: %s"
          % (rec["modulos_del_solver_cargados"] or "ninguno"))
    ruta = None
    if escribir:
        DEDUCCIONES.mkdir(parents=True, exist_ok=True)
        sello = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
        nombre = "deduccion_%s_%s_a%g_N%d_%s.json" % (slug, modo, alpha_deg, int(N), sello)
        ruta = DEDUCCIONES / nombre
        ruta.write_text(json.dumps(rec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("registro en disco: %s" % ruta)
        rec["registro_en_disco"] = str(ruta)
    print("VEREDICTO: DEDUCIDO_ANALITICO · RC: 0 · R: %.6f · RAZON: %s" % (R, slug))
    return rec


# ------------------------------------------------------------------ ruta 2: solver
def _amplitud_por_haz(M, N: int) -> tuple:
    """a_beam(N) con la convencion del motor, y su control contra configs.json.

    La convencion es `a_beam = a_ref / sqrt(N)` (el modelo reparte coherente: a_tot =
    sqrt(N) a_ref). No se inventa: se verifica contra las cinco filas DECLARADAS de
    `sim/configs.json` y, si N no esta en la tabla, se declara DERIVADA.
    """
    a_ref = float(M.A_REF)
    a_beam = a_ref / math.sqrt(N)
    tabla = {int(f["N"]): float(f["a_beam"]) for f in M.CFG["filas"]}
    if N in tabla:
        desvio = abs(a_beam - tabla[N])
        nota = "verificada contra configs.json (desvio %.3e)" % desvio
        return a_beam, nota, desvio <= 1e-9
    return a_beam, "DERIVADA: N=%d no esta en N_LISTA de configs.json" % N, True


def correr_nominal(modo, alpha_deg, N, tol_rango, verbose=False, json_out=False) -> tuple:
    """Rama `(True, "")`: aqui SI se importa y corre el solver. Devuelve (RC, rec)."""
    import field_solver as F          # noqa: PLC0415  (import tardio = pureza de la ruta 1)
    import maxwell2d as M             # noqa: PLC0415
    import params as P                # noqa: PLC0415

    base, nulo = descomponer_modo(modo)
    rec = _cabecera(
        "FDTD Yee 2D3V de sim/maxwell2d.py sha16=%s (malla 480x480, dx = lambda_L/40, "
        "ventana de medida en celdas [100, 380]) LEIDO en su observable "
        "`a_inv_rel_al_pico`; y el campo del cono de semiangulo alpha de "
        "sim/field_solver.py familia `estrella` (malla 61^3, nodos propios), como LECTURA "
        "SEPARADA. El FDTD no lleva alpha; el alpha solo vive en `field_solver`. "
        "UNIDAD: R = a_inv/|E| adimensional; a_medido en unidades de a0." % SELLO_DEL_SOLVER
    )
    rec["entrada"] = _bloque_entrada(modo, alpha_deg, N, tol_rango)
    imprimir_bloque(rec)
    print("entrada: modo=%s (base=%s nulo=%s) alpha_deg=%s N=%d tol_rango=%r"
          % (modo, base, nulo, alpha_deg, int(N), tol_rango))
    print("el filtro devolvio (True, ''): paso al solver, flujo nominal")

    a_beam, nota_amp, amp_ok = _amplitud_por_haz(M, int(N))
    print("amplitud por haz: a_beam = %.6f  [%s]" % (a_beam, nota_amp))
    r = M.correr(modo=base, n=int(N), nulo=nulo, verbose=verbose)

    e0 = P.campo_de_a0(a_beam)
    lista = F.haces("estrella", "circular", alpha_deg, int(N))
    med = F.medir(lista, e0)
    R_cono = (med["a_inv"] / med["a_amp"]) if med["a_amp"] > 0.0 else float("nan")

    R = float(r["a_inv_rel_al_pico"])
    a_medido = float(r["a_medido"])
    fracturas = revisar_cotas(R, a_medido, int(r["pasos"]))
    if not amp_ok:
        fracturas.append("convencion de amplitud: a_beam no coincide con configs.json")

    rec.update({
        "veredicto": "FDTD_COMPLETO" if not fracturas else "FRACTURA",
        "RC": 0 if not fracturas else 1,
        "R": round(R, 6),
        "R_fuente": "sim/maxwell2d.py corrida['a_inv_rel_al_pico']",
        "R_unidad": "a_inv / |E| (adimensional, 0 <= R <= 1)",
        "fracturas": fracturas,
        "FDTD": "INVOCADO",
        "a_medido": a_medido,
        "a_beam": a_beam,
        "a_beam_nota": nota_amp,
        "pasos": int(r["pasos"]),
        "cfl": r["cfl"],
        "nulo": nulo,
        "familia_del_cono": "estrella",
        "alpha_deg_del_cono": alpha_deg,
        "R_cono_alpha": None if math.isnan(R_cono) else round(R_cono, 6),
        "R_cono_nota": ("lectura a nivel de CAMPO del cono de semiangulo alpha; NO es el R "
                        "del veredicto (que es el del FDTD) y no se promedia con el"),
        "E_max_V_m": r["E_max_V_m"],
        "cB_sobre_E_en_el_pico": r["cB_sobre_E_en_el_pico"],
        "F_rel_pico": r["F_rel_pico"],
        "t_max_fs": r["t_max_fs"] * 1e15,
        "modulos_del_solver_cargados": modulos_del_solver_cargados(),
    })

    print("filtro: paso (no intercepto)")
    print("solver: modo=%s N=%d nulo=%s pasos=%d cfl=%s" % (base, int(N), nulo, int(r["pasos"]), r["cfl"]))
    print("FDTD: a_medido = %.6g (unidades de a0) · E_max = %.6g V/m · cB/|E| en el pico = %.6f"
          % (a_medido, float(r["E_max_V_m"]), float(r["cB_sobre_E_en_el_pico"])))
    print("FDTD: R = a_inv_rel_al_pico = %.6f   [fuente: corrida del solver, no deducida]" % R)
    print("campo del cono alpha=%s: R_cono = %s  [lectura separada, no entra al veredicto]"
          % (alpha_deg, "SIN MEDIDA" if math.isnan(R_cono) else "%.6f" % R_cono))
    if fracturas:
        for f in fracturas:
            print("FRACTURA: %s" % f)
        print("VEREDICTO: FRACTURA · RC: 1 · R: %.6f · CAUSA: %s" % (R, fracturas[0]))
    else:
        print("VEREDICTO: FDTD_COMPLETO · RC: 0 · R: %.6f" % R)
    return rec["RC"], rec


# ------------------------------------------------------------------ main
def _parse(argv) -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        prog="fuego_sensible.py",
        description="Conductor B': filtro analitico PREVIO al solver, con contrato de RC.",
    )
    # Sin `choices=`: el modo invalido lo tiene que rechazar el FILTRO (ValueError -> RC 2).
    # Si lo rechazara argparse, la ruta de ValueError del filtro nunca se ejerceria por CLI.
    ap.add_argument("--modo", default="contra",
                    help="uno de: %s" % ", ".join(MODOS_DEL_MOTOR))
    ap.add_argument("--alpha", type=float, default=30.0, help="semiangulo en grados")
    ap.add_argument("--N", type=int, default=4, help="numero de haces")
    ap.add_argument("--tol", type=float, default=1e-4, dest="tol_rango",
                    help="tolerancia del filtro (default 1e-4, el del filtro)")
    ap.add_argument("--no-escribir", action="store_true",
                    help="no deja el registro de deduccion en disco")
    ap.add_argument("--json", action="store_true", help="imprime el registro JSON al final")
    ap.add_argument("--verbose", action="store_true", help="pasa --verbose a correr()")
    ap.add_argument("--control", action="store_true", help="par de controles del conductor")
    return ap.parse_args(argv)


def main(argv) -> int:
    args = _parse(argv)
    if args.control:
        return control()

    try:
        ok, razon = evaluar_sensibilidad_previa(args.modo, args.alpha, args.N, args.tol_rango)
    except ValueError as exc:
        print("T_UTC: %s" % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
        print("FALLO DE METRO: el filtro rechazo la corrida (fail-closed): %s" % exc)
        print("VEREDICTO: FALLO_DE_METRO · RC: 2 · CAUSA: %s" % exc)
        return 2

    if not ok:
        rec = emitir_deduccion(args.modo, args.alpha, args.N, args.tol_rango, razon,
                               escribir=not args.no_escribir)
        if args.json:
            print(json.dumps(rec, ensure_ascii=False))
        return 0

    rc, rec = correr_nominal(args.modo, args.alpha, args.N, args.tol_rango,
                             verbose=args.verbose, json_out=args.json)
    if args.json:
        print(json.dumps(rec, ensure_ascii=False))
    return rc


# ------------------------------------------------------------------ control
def _en_subproceso(extra: list) -> tuple:
    """Corre el conductor en un interprete LIMPIO. Devuelve (RC, salida)."""
    cmd = [sys.executable, "-B", str(Path(__file__).resolve())] + extra
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def control() -> int:
    """Par de controles del conductor. RC: 0 discriminan, 1 no, 2 SIN MEDIDA."""
    print("T_UTC: %s" % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    print("UNIVERSO DECLARADO: %d controles del conductor. Los 3 primeros en SUBPROCESO "
          "(interprete limpio, es la unica forma de medir que la ruta de intercepto no "
          "carga el solver); el 4o en proceso, porque despues de el `numpy` ya esta cargado."
          % 6)
    print("MOTOR: python3 -B + subprocess. UNIDAD: caso de control (RC + linea de veredicto).")
    print("VENTANA: la hora UTC de arriba.")
    fallos = 0

    print("--- 1. INTERCEPTO (debe dar RC 0 · DEDUCIDO_ANALITICO y NO cargar el solver) ---")
    casos = (
        (["--modo", "contra", "--alpha", "30", "--N", "2", "--no-escribir"], 0,
         "VEREDICTO: DEDUCIDO_ANALITICO · RC: 0 · R: 1.000000 · RAZON: saturacion_antinodo",
         "antinodo: B -> 0, cota 1 exacta"),
        (["--modo", "colineal", "--alpha", "0", "--N", "4", "--no-escribir"], 0,
         "VEREDICTO: DEDUCIDO_ANALITICO · RC: 0 · R: 0.000000 · RAZON: semiangulo_nulo",
         "semiangulo nulo: F = G = 0, cota 0 exacta"),
        (["--modo", "contra", "--alpha", "0", "--N", "2", "--no-escribir"], 0,
         "VEREDICTO: DEDUCIDO_ANALITICO · RC: 0 · R: 1.000000 · RAZON: saturacion_antinodo",
         "las dos reglas aplican: precedencia declarada por el filtro"),
    )
    for extra, rc_esp, linea_esp, nota in casos:
        rc, out = _en_subproceso(extra)
        carga = "NO INVOCADO" in out
        bien = (rc == rc_esp) and (linea_esp in out) and carga
        fallos += 0 if bien else 1
        print("  %-4s %-42s -> RC=%s  [%s]" % ("OK" if bien else "ROJO", " ".join(extra), rc, nota))
        if not bien:
            print("        esperado RC=%s y la linea %r; y 'FDTD: NO INVOCADO' presente (%s)"
                  % (rc_esp, linea_esp, carga))
            print("        salida: %s" % out.strip().replace("\n", " | "))

    print("--- 2. FALLO DE METRO (debe dar RC 2, no verde ni razon de saturacion) ---")
    for extra, nota in (
        (["--modo", "xyz", "--no-escribir"], "modo no declarado: lo caza el filtro, no argparse"),
        (["--modo", "contra", "--N", "3", "--no-escribir"], "N impar en contra: el motor lo prohibe"),
        (["--modo", "colineal", "--N", "0", "--no-escribir"], "N < 1"),
        (["--modo", "colineal", "--tol", "0", "--no-escribir"], "tol_rango no positiva"),
    ):
        rc, out = _en_subproceso(extra)
        bien = (rc == 2) and ("FALLO_DE_METRO" in out)
        fallos += 0 if bien else 1
        print("  %-4s %-42s -> RC=%s  [%s]" % ("OK" if bien else "ROJO", " ".join(extra), rc, nota))

    print("--- 3. EL GATE DE FRACTURA SABE ENROJECER (funcion pura, sin solver) ---")
    for R, a_med, pasos, n_esp, nota in (
        (2.0, 1.0e3, 1113, 1, "R fuera de la cota"),
        (1.0, 1.0e3, 1113, 0, "R = 1 exacto: el BORDE es legal, no fractura"),
        (0.0, 1.0e3, 1113, 0, "R = 0 exacto: el otro borde tambien es legal"),
        (0.99, 1.0e3, 1113, 0, "R interior: el valor de los sellos"),
        (0.99, 0.0, 1113, 1, "a_medido nulo: no hay senal"),
        (0.99, 1.0e3, 0, 1, "ventana vacia"),
    ):
        fr = revisar_cotas(R, a_med, pasos)
        bien = len(fr) == n_esp
        fallos += 0 if bien else 1
        print("  %-4s R=%-5s a_medido=%-7s pasos=%-5s -> %d fractura(s)  [%s]"
              % ("OK" if bien else "ROJO", R, a_med, pasos, len(fr), nota))

    print("--- 4. PUREZA EN PROCESO (antes de la corrida nominal) ---")
    sucio = modulos_del_solver_cargados()
    print("  %-4s modulos del solver cargados por el --control hasta aqui: %s"
          % ("OK" if not sucio else "ROJO", sucio or "ninguno"))
    fallos += 1 if sucio else 0

    print("--- 5. FLUJO NOMINAL (paso al solver: debe dar RC 0 · FDTD_COMPLETO) ---")
    rc, out = _en_subproceso(["--modo", "colineal", "--alpha", "26.5651", "--N", "4",
                              "--no-escribir"])
    linea = [l for l in out.splitlines() if l.startswith("VEREDICTO:")]
    bien = (rc == 0) and linea and linea[-1].startswith("VEREDICTO: FDTD_COMPLETO · RC: 0 · R: ")
    fallos += 0 if bien else 1
    print("  %-4s colineal alpha=26.5651 N=4 -> RC=%s" % ("OK" if bien else "ROJO", rc))
    print("        %s" % (linea[-1] if linea else "sin linea de veredicto"))
    for l in out.splitlines():
        if l.startswith("FDTD: R = ") or l.startswith("campo del cono") or l.startswith("filtro: "):
            print("        %s" % l)

    print("--- 6. ESCRITURA DEL REGISTRO DE DEDUCCION ---")
    antes = sorted(p.name for p in DEDUCCIONES.glob("*.json")) if DEDUCCIONES.is_dir() else []
    rc, out = _en_subproceso(["--modo", "contra", "--alpha", "30", "--N", "2"])
    despues = sorted(p.name for p in DEDUCCIONES.glob("*.json")) if DEDUCCIONES.is_dir() else []
    nuevas = [n for n in despues if n not in antes]
    bien = (rc == 0) and len(nuevas) == 1
    fallos += 0 if bien else 1
    print("  %-4s RC=%s · registros nuevos: %d  [%s]"
          % ("OK" if bien else "ROJO", rc, len(nuevas), DEDUCCIONES))
    for n in nuevas:
        print("        %s" % n)

    if fallos:
        print("VEREDICTO: EL CONDUCTOR NO DISCRIMINA · RC: 1 · %d control(es) en rojo" % fallos)
        return 1
    print("VEREDICTO: CONDUCTOR DISCRIMINA · RC: 0 · intercepto sin solver, nominal con "
          "solver, RC 2 solo del metro, gate de fractura probado en las dos direcciones")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
