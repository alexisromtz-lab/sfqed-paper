#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sim/falsador_mallas_no_anidadas.py -- el verdugo de la ROTACION DE NODOS.

QUE FALSIFICA
  El observable de la ley 1/N, a_medido(N) = (e/(m_e c omega)) * max_{|r|<=w0, t} |E|,
  se mide hoy con los N haces COPLANARES en los angulos ANIDADOS

      theta_j = 2 pi j / N                (j = 0 .. N-1)        [la casa]

  Este verdugo mide el MISMO objeto con los angulos NO ANIDADOS

      theta_j = (j + 1/2) * 2 pi / N      (j = 0 .. N-1)        [el falsador]

  Las dos familias describen el MISMO campo fisico: la segunda es la primera rotada
  rigida por pi/N.  Como Omega_foco = disco |r| <= w0 es rotacionalmente simetrico y
  los invariantes (F, G, a) son escalares, la medida DEBE coincidir hasta la anisotropia
  del reticulo cartesiano.  Si NO coincide, la ley 1/N publicada es propiedad de la
  CONVENCION de nodos anidados, no del campo enfocado.

UNIVERSO DECLARADO (se imprime antes de la primera cifra)
  MOTOR  = sim/runner_2d3v.py (sha16 declarado en la cabecera de la corrida), importado
           en SOLO LECTURA; el paso Yee, la esponja, MASK_FOCO, los invariantes y la
           VENTANA DE MEDIDA son los suyos, sin re-implementar.  numpy float64.
  UNIDAD = a_adimensional (a = eE/(m_e c omega)) y pendiente log-log beta (adimensional).
  VENTANA = reloj UTC impreso con la corrida.
  ESCRITURA = NINGUNA.  Este archivo no escribe nada: el crudo se obtiene por redireccion.

PRE-REGISTRO (sellado aqui, ANTES de calcular el primer numero)

  H0 (el nulo que la casa afirma) : a_no_anidado(N) / a_anidado(N) = 1 + O(anisotropia).
  Prediccion declarada: |razon - 1| <= 1e-2 en todo N, y |beta_no_anidado - beta_anidado|
  <= 0.05 (= la mitad del ancho de la banda VERDE ya pre-registrada [0.45, 0.55] de la ley
  1/N: por debajo de eso, ninguna convencion puede mover un veredicto de sim/falsador.py).

  Bandas del veredicto, POR N y sobre beta:
    VERDE  <=> |razon(N) - 1| <= 0.20 para todo N  Y  |dbeta| <= 0.05
    ROJO   <=> algun N con |razon(N) - 1| >  0.20  O  |dbeta| > 0.05
  El 0.20 es la MISMA tolerancia por N ya pre-registrada en sim/PROTOCOLO_1overN.md seccion 2
  (TOL_RATIO de sim/falsador.py): no se inventa un umbral nuevo, se hereda el de la casa.

CONTROLES OBLIGATORIOS (corren ANTES del veredicto; sin ellos no hay veredicto)
  C0  certificado del arnes : la copia local de campos() con delta = 0 debe dar los SEIS
      componentes BIT A BIT iguales a runner_2d3v.campos, en todo N.  Y una corrida
      end-to-end con el parche en delta = 0 debe dar el MISMO a_fdtd que sin parche.
  C1  simetria del reticulo : delta = 0 vs delta = 1 con fases identicamente NULAS.
      Los dos conjuntos de angulos son el MISMO conjunto y la fase tambien => la medida
      debe coincidir dentro de 1e-12 (banda declarada, no de fisica: el reticulo cuadrado
      admite esa permutacion, solo se rompe por no-asociatividad del punto flotante).
  C1b nulo de un solo haz : N = 1, delta = 0 vs delta = 0.5.  La rotacion es de pi, que es
      simetria EXACTA del reticulo cuadrado => banda 1e-12.
  C2  control que DEBE DIFERIR (discriminante) : delta = 0 vs delta = 1 con el vector de
      FASES_TESTIGO (no nulo).  Ahi la fase cambia de haz y el campo cambia de verdad:
      algun N debe salir con |razon - 1| > 0.20.  Si NO difiere, el arnes no esta
      leyendo las fases (o el parche no se aplico) => CONTRATO ROTO.

  Los controles (C0 end-to-end, C1, C1b, C2) corren con PASOS_CONTROL = 40 pasos: prueban
  el CONSTRUCTOR del campo y la asignacion de fase, no la propagacion.  El objeto (C3)
  corre con --pasos, por defecto PASOS_TOTAL.

SIMETRIA DEL RETICULO (declarado ANTES de medir; gobierna QUE N discrimina)
  El reticulo de Yee es cuadrado, asi que rotarlo por pi/2 lo deja invariante.
  Consecuencia, por N y con delta = 1/2 (el objeto la rotacion es pi/N):
    N = 1 -> pi      SIMETRIA EXACTA del reticulo  => INVARIANTE POR CONSTRUCCION
    N = 2 -> pi/2    SIMETRIA EXACTA del reticulo  => INVARIANTE POR CONSTRUCCION
    N >= 4 -> pi/N   NO es simetria del cuadrado    => N INFORMATIVA (el objeto real)
  Por eso N = 1 y N = 2 no pueden fallar aunque la ley 1/N fuera pura convencion, y su
  VERDE no es evidencia: la evidencia esta en N >= 4.  El veredicto se emite igual sobre
  todas las N pedidas, y este reparto se imprime para que el VERDE de N = 1, 2 no se lea
  como confirmacion.
  Y por la MISMA razon el control C2 usa un conjunto propio, N = {3, 8} (rotaciones de
  2 pi/3 y pi/4: ninguna es simetria del cuadrado).  Elegir N = {2, 4} habria dejado el
  control CIEGO: medido, con {2, 4} el control daba razon - 1 = 0.000e+00 y declaraba
  CONTRATO ROTO sobre un arnes sano -- un control que no puede diferir no es un control.
  La pata N = 1 se agrega al control solo si el operador pidio N = 1.

RC  0 = verde (invariante)  1 = rojo (la medida depende de la convencion de nodos)
    2 = SIN MEDIDA / CONTRATO ROTO (ni verde ni rojo: no hay objeto, o el metro falla)

USO
  python3 -B sim/falsador_mallas_no_anidadas.py --todo
  python3 -B sim/falsador_mallas_no_anidadas.py --n 4
  python3 -B sim/falsador_mallas_no_anidadas.py --todo --pol circular --json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
if str(AQUI) not in sys.path:
    sys.path.insert(0, str(AQUI))

import runner_2d3v as R  # noqa: E402  (SOLO LECTURA: el instrumento de la casa)

# --------------------------------------------------------------- sellado
DELTA_ANIDADA = 0.0            # [la casa]      theta_j = 2 pi j / N
DELTA_NO_ANIDADA = 0.5         # [el falsador]  theta_j = (j + 1/2) * 2 pi / N
DELTA_PERMUTADA = 1.0          # [control C1/C2] el mismo conjunto, la fase corrida un haz
BANDA_RETICULO = 1.0e-12       # [DECLARADA] banda de los controles de simetria, no de fisica
TOL_VALOR = 0.20               # [HEREDADA] = TOL_RATIO de sim/falsador.py (PROTOCOLO seccion 2)
                               #   Tolerancia FISICA del OBJETO (C3). NO se reusa como umbral
                               #   de control: "cableado bien" y "significativo fisicamente"
                               #   son DOS objetos distintos, y un umbral prestado compara dos
                               #   objetos distintos (leccion de la Pestaña 2).
TOL_BETA = 0.05                # [DECLARADA] = media anchura de la banda VERDE [0.45, 0.55]
PISO_LECTURA = 1.0e-6          # [DECLARADO] piso de CABLEADO, solo para C2. Tres ordenes por
                               #   encima del ruido de float (~1e-16 medido) y tres por debajo
                               #   de la senal medida en C2 (~7e-4..1e-3). Prueba que el arnes
                               #   LEE la fase y que el parche alcanza al constructor; no dice
                               #   nada de la fisica.
BANDA_OK = (0.45, 0.55)
BANDA_MUERTE = (0.35, 0.65)
PASOS_CONTROL = 40             # [DECLARADO] los controles prueban el constructor, no el vuelo
PREDICCION = 1.0e-2            # [DECLARADA] magnitud esperada del residuo de anisotropia

SEMILLA_TXT = "sfqed/mallas_no_anidadas/20261012"
_sem = int.from_bytes(hashlib.sha256(SEMILLA_TXT.encode()).digest()[:8], "big")
FASES_TESTIGO = tuple(float(x) for x in np.random.default_rng(_sem).normal(0.0, 1.0, 16))
FASES_NULAS = tuple(0.0 for _ in range(16))

UNIVERSO = (
    "sim/runner_2d3v.py importado en SOLO LECTURA (paso Yee, esponja, MASK_FOCO, "
    "invariantes y ventana de medida son suyos); motor numpy float64; unidad = a "
    "adimensional y pendiente log-log beta; malla 480x480, dx = lambda/40, CFL 0.6; "
    "medicion = max de |E| sobre el disco |r| <= w0 en la ventana causal; "
    "ESCRITURA = NINGUNA."
)

# ------------------------------------------------------------------ arnes
_ORIG = R.campos          # el original, guardado una sola vez


def campos_delta(N, pol, dl_lambda=0.0, ref=None, fases=None, delta=0.0):
    """COPIA FIEL de runner_2d3v.campos con UNA SOLA LINEA cambiada: la ley de angulos.

    Original (l.191 del instrumento):  th0 = 2.0 * math.pi * j / N
    Aqui:                              th0 = 2.0 * math.pi * (j + delta) / N

    El resto del cuerpo es identico, incluida la rama de `fases` y la de `dl_lambda`.
    El certificado C0 la ata bit a bit al original en delta = 0: si esa identidad falla,
    el defecto es de ESTA copia y el veredicto no se emite.
    """
    xg, yg, h = R._malla()
    NODOS = {0: (xg, yg), 1: (xg, yg + h), 2: (xg + h, yg), 3: (xg + h, yg + h)}
    F0 = {c: np.zeros((R.NX, R.NY)) for c in R.COMP}
    F1 = {c: np.zeros((R.NX, R.NY)) for c in R.COMP}
    for j in range(N):
        th0 = 2.0 * math.pi * (j + delta) / N        # <<< LA UNICA LINEA CAMBIADA
        if fases is not None:
            fase = float(fases[j % len(fases)])
        else:
            fase = -2.0 * math.pi * dl_lambda if (j == N - 1 and dl_lambda != 0.0) else 0.0
        am0 = R.a_b(N, ref)
        for k, comps in R.COMPS_DE_CLAVE.items():
            Xc, Yc = NODOS[k]
            b = R.bloque(Xc, Yc, th0, am0, pol, fase, comps)
            for c in comps:
                F0[c] += b[c][0]
                F1[c] += b[c][1]
    return F0, F1


def _con_delta(delta):
    def f(N, pol, dl_lambda=0.0, ref=None, fases=None):
        return campos_delta(N, pol, dl_lambda, ref, fases, delta)
    return f


def correr_con_delta(N, pol, delta, pasos, fases=None):
    """Corre el INSTRUMENTO DE LA CASA bajo la ley de angulos `delta`.

    Parchea el atributo `campos` del modulo en MEMORIA, corre, y lo restaura en el
    `finally`.  El archivo en disco NO se toca.  Si la restauracion no vuelve a dejar el
    original, se levanta: un parche que sobrevive contamina la corrida siguiente.
    """
    R.campos = _con_delta(delta)
    try:
        res = R.correr(N, pol, 0.0, pasos, verbose=False, fases=fases)
    finally:
        R.campos = _ORIG
    if R.campos is not _ORIG:
        raise RuntimeError("el parche de personas_campos no se restauro")
    return res


def a_de(res, causa_si_falta):
    """Extrae a_fdtd; si el campo no esta o no es finito, NO se inventa un cero."""
    if not isinstance(res, dict) or "a_fdtd" not in res:
        raise RuntimeError(f"{causa_si_falta}: la corrida no trae a_fdtd (llaves: "
                           f"{sorted(res.keys()) if isinstance(res, dict) else type(res)})")
    a = float(res["a_fdtd"])
    if not math.isfinite(a):
        raise RuntimeError(f"{causa_si_falta}: a_fdtd no finito ({a!r})")
    return a


def beta_loglog(pares):
    """Pendiente por minimos cuadrados de log a contra log N (mismo estimador que
    sim/falsador.py, para que las dos cifras sean comparables)."""
    xs = [math.log(n) for n, _ in pares]
    ys = [math.log(a) for _, a in pares]
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    if den == 0.0:
        raise RuntimeError("beta: denominador cero (todas las N iguales)")
    return num / den


# ------------------------------------------------------ controles del arnes
def control_C0(ns, pol):
    """Certificado: campos_delta(delta=0) == runner.campos, BIT A BIT, seis componentes."""
    print("--- C0  certificado del arnes: copia(delta=0) contra el instrumento, bit a bit ---")
    for N in ns:
        orig = _ORIG(N, pol, 0.0, None, None)
        copi = campos_delta(N, pol, 0.0, None, None, 0.0)
        malos = []
        peor = 0.0
        for c in R.COMP:
            for k in (0, 1):
                if not np.array_equal(orig[k][c], copi[k][c]):
                    d = float(np.max(np.abs(orig[k][c] - copi[k][c]))) if orig[k][c].size else 0.0
                    malos.append(f"{c}[{k}]")
                    peor = max(peor, d)
        if malos:
            print(f"  ROJO N={N}: {len(malos)} arreglo(s) difieren ({','.join(malos[:6])}"
                  f"{'...' if len(malos) > 6 else ''}) max|dif| = {peor:.3e}")
            return False, f"C0: la copia NO reproduce el instrumento en N={N} ({malos[0]})"
        print(f"  OK   N={N:2d}: 12 arreglos (6 componentes x Re/Im) identicos bit a bit")
    return True, ""


def control_C0b(N, pol, pasos):
    """End-to-end: con el parche en delta = 0, a_fdtd debe ser EL MISMO que sin parche."""
    print(f"--- C0b certificado end-to-end (N={N}, {pasos} pasos) ---")
    sin = a_de(R.correr(N, pol, 0.0, pasos, verbose=False), "C0b sin parche")
    con = a_de(correr_con_delta(N, pol, DELTA_ANIDADA, pasos), "C0b con parche delta=0")
    if sin != con:
        print(f"  ROJO: sin parche a = {sin!r} ; con parche(delta=0) a = {con!r}"
              f" ; dif rel = {abs(con / sin - 1.0):.3e}")
        return False, f"C0b: el parche en delta=0 mueve la corrida (N={N})"
    print(f"  OK   a_fdtd = {sin!r} en las dos (identico, no solo parecido)")
    return True, ""


def control_simetria(ns, pol, delta, etiqueta, fases, banda):
    """C1 / C1b: dos corridas que DEBEN coincidir dentro de `banda`."""
    print(f"--- {etiqueta} (delta 0 vs {delta}) ---")
    peor = 0.0
    causa = ""
    for N in ns:
        a0 = a_de(correr_con_delta(N, pol, DELTA_ANIDADA, PASOS_CONTROL, fases),
                  f"{etiqueta} delta=0")
        a1 = a_de(correr_con_delta(N, pol, delta, PASOS_CONTROL, fases),
                  f"{etiqueta} delta={delta}")
        r = a1 / a0 - 1.0
        peor = max(peor, abs(r))
        print(f"  N={N:2d} a0={a0:.12g} a1={a1:.12g} razon-1={r:+.3e}"
              f" {'OK' if abs(r) <= banda else 'ROJO'}")
        if abs(r) > banda and not causa:
            causa = f"{etiqueta}: N={N} se mueve {r:+.3e} > {banda:g}"
    return (not causa), (causa or ""), peor


def control_discriminante(ns, pol):
    """C2: con FASES_TESTIGO no nulas, delta=1 DEBE mover la medida (N>=2).

    El discriminante NO depende de las N que eligio el operador: si `--n 1`, este
    control se quedaria sin objeto y declararia CONTRATO ROTO por su propia poda.
    Por eso corre sobre un conjunto PROPIO declarado, {2, 4}, y solo agrega N=1
    (la pata invariante) si el operador lo pidio.
    """
    ns_c2 = sorted({3, 8} | ({1} if 1 in ns else set()))
    print("--- C2  control que DEBE DIFERIR: delta 0 vs 1 con FASES_TESTIGO ---")
    print(f"  conjunto propio del control: N = {ns_c2} (declarado, no el del operador {ns}).")
    print("  Ninguno de estos N hace simetria del cuadrado: 2 pi/3 y pi/4 no son pi/2.")
    print("  FASES_TESTIGO = [" + ", ".join(f"{x:.6f}" for x in FASES_TESTIGO) + "]")
    movido = False
    causa = ""
    for N in ns_c2:
        a0 = a_de(correr_con_delta(N, pol, DELTA_ANIDADA, PASOS_CONTROL, FASES_TESTIGO), "C2 d0")
        a1 = a_de(correr_con_delta(N, pol, DELTA_PERMUTADA, PASOS_CONTROL, FASES_TESTIGO), "C2 d1")
        r = a1 / a0 - 1.0
        print(f"  N={N:2d} a0={a0:.12g} a1={a1:.12g} razon-1={r:+.3e}", end="")
        if N == 1:
            print()
            if abs(r) > BANDA_RETICULO:
                causa = (f"C2: N=1 con un solo haz NO puede moverse, y se movio {r:+.3e}")
            continue
        if abs(r) > PISO_LECTURA:
            print(f"   OK  lee (> piso de cableado {PISO_LECTURA:g})")
            movido = True
        else:
            print(f"   <<< NO LEE: por debajo del piso de cableado {PISO_LECTURA:g}")
    if causa:
        return False, causa
    if not movido:
        return False, ("C2: con fases TESTIGO no nulas y N no trivial (3, 8) la medida NO se "
                       "movio por encima del piso de cableado => el arnes no esta leyendo "
                       "las fases, o el parche no alcanza al constructor del campo")
    print(f"  (el umbral de C2 es el piso de CABLEADO {PISO_LECTURA:g}, no la tolerancia fisica "
          f"{TOL_VALOR:g} del objeto: son dos objetos distintos)")
    return True, ""


# --------------------------------------------------------------- el objeto
def pre_registro(ns, pol, pasos):
    print("=" * 78)
    print("PRE-REGISTRO  (declarado ANTES de medir; no se toca despues)")
    print("=" * 78)
    print(f"UNIVERSO DECLARADO: {UNIVERSO}")
    print(f"hora = {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")
    print("la casa : theta_j = 2 pi j / N")
    print("falsador: theta_j = (j + 1/2) * 2 pi / N      (la casa, rotada pi/N)")
    print(f"N_LISTA = {ns} ; pol = {pol} ; pasos del objeto = {pasos} ; "
          f"pasos de los controles = {PASOS_CONTROL}")
    print(f"Omega_foco = disco |r| <= w0 = {R.RADIO_FOCO_CELDAS} celdas ; "
          f"malla {R.NX}x{R.NY} ; dx = 2 pi/{R.DX_SOBRE_LAMBDA} ; CFL = {R.CFL}")
    triviales = [N for N in ns if N in (1, 2)]
    informativas = [N for N in ns if N not in (1, 2)]
    print(f"SIMETRIA DEL RETICULO: N {triviales} son INVARIANTES POR CONSTRUCCION (rotacion "
          f"pi/N con N<=2 es pi/2 o pi, simetria exacta del cuadrado) -> su VERDE no es "
          f"evidencia.  N INFORMATIVAS = {informativas}.")
    print(f"PREDICCION (H0): |razon - 1| <= {PREDICCION:g} en todo N  y  |dbeta| <= {TOL_BETA:g}")
    print(f"BANDAS: VERDE si |razon(N)-1| <= {TOL_VALOR:g} en todo N y |dbeta| <= {TOL_BETA:g}"
          f" ; ROJO en caso contrario")
    print(f"       (el {TOL_VALOR:g} es TOL_RATIO heredado de sim/falsador.py; el {TOL_BETA:g} "
          f"es media anchura de la banda VERDE {BANDA_OK} de la ley 1/N)")
    print(f"       piso de CABLEADO del control C2 = {PISO_LECTURA:g} (declarado; no es la "
          f"tolerancia del objeto)")
    print("=" * 78)


def main() -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--n", type=int, default=None, help="un solo N (default: N_LISTA)")
    ap.add_argument("--todo", action="store_true", help="recorre N_LISTA")
    ap.add_argument("--pol", default="linear", choices=["linear", "circular"])
    ap.add_argument("--pasos", type=int, default=R.PASOS_TOTAL)
    ap.add_argument("--json", action="store_true", help="solo las cifras, sin prosa")
    args = ap.parse_args()

    if args.n is not None:
        ns = [int(args.n)]
    elif args.todo:
        ns = list(R.N_LISTA)
    else:
        ns = list(R.N_LISTA)
    ns = sorted(set(ns))

    if not args.json:
        pre_registro(ns, args.pol, args.pasos)

    fallos_metro = []

    # ---------------- controles (si el metro falla, NO hay veredicto) ----------
    if not args.json:
        ok, causa = control_C0(ns, args.pol)
        if not ok:
            fallos_metro.append(causa)
        ok, causa = control_C0b(max(ns), args.pol, PASOS_CONTROL)
        if not ok:
            fallos_metro.append(causa)
        ok, causa, _ = control_simetria(ns, args.pol, DELTA_PERMUTADA,
                                        "C1  simetria del reticulo (fases NULAS)",
                                        FASES_NULAS, BANDA_RETICULO)
        if not ok:
            fallos_metro.append(causa)
        ok, causa, _ = control_simetria([1], args.pol, DELTA_NO_ANIDADA,
                                        "C1b nulo de un solo haz (rotacion de pi)",
                                        FASES_NULAS, BANDA_RETICULO)
        if not ok:
            fallos_metro.append(causa)
        ok, causa = control_discriminante(ns, args.pol)
        if not ok:
            fallos_metro.append(causa)

    if fallos_metro:
        print("CONTRATO ROTO: " + " ; ".join(fallos_metro))
        print("VEREDICTO: SIN MEDIDA -- el metro no pasa sus propios controles.")
        return 2

    if len(ns) < 3:
        print(f"CONTRATO ROTO: {len(ns)} N(s) -> con menos de 3 puntos beta es un ajuste, "
              f"no una pendiente.")
        print("VEREDICTO: SIN MEDIDA.")
        return 2

    # ---------------------------- el objeto --------------------------------
    print("--- C3  EL OBJETO: anidada vs no anidada, fases NULAS, "
          f"{args.pasos} pasos ---")
    a0_map, a1_map = {}, {}
    for N in ns:
        a0_map[N] = a_de(correr_con_delta(N, args.pol, DELTA_ANIDADA, args.pasos),
                         f"C3 anidada N={N}")
        a1_map[N] = a_de(correr_con_delta(N, args.pol, DELTA_NO_ANIDADA, args.pasos),
                         f"C3 no anidada N={N}")
        print(f"  N={N:2d} anidada={a0_map[N]:.12g}  no_anidada={a1_map[N]:.12g}")

    if any(a <= 0.0 for a in a0_map.values()) or any(a <= 0.0 for a in a1_map.values()):
        print("CONTRATO ROTO: alguna a <= 0 -> no es una amplitud.")
        print("VEREDICTO: SIN MEDIDA.")
        return 2

    beta0 = beta_loglog([(N, a0_map[N]) for N in ns])
    beta1 = beta_loglog([(N, a1_map[N]) for N in ns])
    dbeta = beta1 - beta0

    print("--- razon por N  (no_anidada / anidada) ---")
    fallos_valor = []
    for N in ns:
        r = a1_map[N] / a0_map[N] - 1.0
        marca = "OK  " if abs(r) <= TOL_VALOR else "ROJO"
        print(f"  {marca} N={N:2d} razon-1 = {r:+.6e}   (|.| <= {TOL_VALOR:g})")
        if abs(r) > TOL_VALOR:
            fallos_valor.append((N, r))

    print("--- la ley 1/N en las dos convenciones ---")
    print(f"  beta(anidada)    = {beta0:.6f}   banda VERDE {BANDA_OK} ; "
          f"muerte <= {BANDA_MUERTE[0]} o >= {BANDA_MUERTE[1]}")
    print(f"  beta(no_anidada) = {beta1:.6f}")
    print(f"  dbeta = {dbeta:+.6f}   (|dbeta| <= {TOL_BETA:g})")

    if args.json:
        print(json.dumps(dict(
            N=ns, pol=args.pol, pasos=args.pasos,
            a_anidada={str(N): a0_map[N] for N in ns},
            a_no_anidada={str(N): a1_map[N] for N in ns},
            razon_menos_1={str(N): a1_map[N] / a0_map[N] - 1.0 for N in ns},
            beta_anidada=beta0, beta_no_anidada=beta1, dbeta=dbeta,
            tolerancias=dict(valor=TOL_VALOR, beta=TOL_BETA, reticulo=BANDA_RETICULO,
                             piso_lectura=PISO_LECTURA),
            prediccion=PREDICCION)))

    fallos = []
    for N, r in fallos_valor:
        fallos.append(f"N={N}: la convencion mueve la medida {r:+.4f} (>{TOL_VALOR:g})")
    if abs(dbeta) > TOL_BETA:
        fallos.append(f"dbeta = {dbeta:+.4f} (>{TOL_BETA:g}): la ley 1/N depende de la "
                      f"convencion de nodos")

    if fallos:
        print(f"VEREDICTO: ROJO -- la medida NO es invariante bajo la rotacion de nodos. "
              f"{len(fallos)} causa(s):")
        for f in fallos:
            print("  - " + f)
        print("  LECTURA: la ley 1/N publicada es propiedad de la CONVENCION ANIDADA "
              "theta_j = 2 pi j / N, no del campo enfocado.")
        return 1

    print("VEREDICTO: VERDE -- la medida es invariante bajo theta_j -> theta_j + pi/N "
          "dentro de las bandas pre-registradas: no es la convencion de nodos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
