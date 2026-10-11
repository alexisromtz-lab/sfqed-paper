#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""N3 · FORMA TEMPORAL DE rho_HE EN EL FOCO -- camino EXACTO de fasores.

CLAUSULA QUE SE EVALUA (PREREGISTRO_VACIO_NO_LINEAL_20261011.md §7, sello
be456faa7a73dbf9, introducido por el commit 2a3a9ac):

  N3  forma temporal: al foco, rho_HE es constante mas UNA linea en 4 omega,
      con razon linea/constante = 3/4, y SIN linea en 1 omega ni en 2 omega.
      banda declarada en el pre-registro: razon 0.75 +- banda ;
      lineas <= 1e-3 de la constante.

CAMINO (el §7 lo exige: "camino separado, requisito no comodidad"):
  la suma EXACTA de fasores de sim/field_solver.py sobre la malla 61^3,
  evaluada en el NODO del foco (centro = 61//2, que es exactamente el origen
  porque la malla es impar y simetrica).
  NO es el FDTD. NO importa sim/maxwell2d.py. Costo sobre la huella del
  solver de Maxwell: 0. Este script LEE sim/ y no escribe nada dentro de el.

LEY CONSTITUTIVA (declarada: la del monitor del motor, sim/maxwell2d.py:266-276,
y la del propio field_solver.py:medir):
  F = (1/2)(|E|^2 - |B|^2) ; G = E . B ; con |B_E| = c|B| (las dos magnitudes
  en V/m). Y rho_HE = c_* (F^2 + 7 G^2) / E_cr^4   [relativo, adimensional].
  rho_HE es HOMOGENEA de grado 4 en los campos y c_* > 0, E_cr^4 > 0 son
  constantes POSITIVAS: no mueven ni la forma ni la razon. La clausula N3 es
  invariante de la convencion de c_* (pre-registro §2 y §7).

ALGEBRA SELLADA QUE N3 CITA (main.tex l.478-484: forma cerrada del foco del
cono de N haces co-rotantes de semiangulo alpha, fase comun en el foco; el
mismo par F, G sale del par contra-propagante circular, asi que la forma NO es
una eleccion de este script):

  E = E_f cos(w t) z_hat ;  B = - E_f sin(w t) z_hat ;  E_f = N sin(alpha) E_0
  F = (E_f^2/2) cos(2 w t) ;  G = -(E_f^2/2) sin(2 w t)
  rho_HE = (E_f^4/4)(cos^2 + 7 sin^2)(2 w t) = (E_f^4/4)(4 - 3 cos 4 w t)
  => constante = E_f^4 ; linea 4w = 0.75 E_f^4 ; razon = 3/4 EXACTA.

CONTROLES DECLARADOS (el metro es un instrumento: se prueba antes de creerle)
  P1 control POSITIVO del sensor: serie sintetica 1 + 0.75 cos(4 th) -> el
     espectro debe recuperar 0.75 exacto. Es del SENSOR, no evidencia de fisica.
  P2 control NEGATIVO de la clausula: la geometria coaxial contra-propagante
     (misma helicidad) da B = 0 y F constante en el foco -> NO debe aparecer
     linea en 4w. Si apareciera, el metro veria una linea que el algebra niega.
  P3 control POSITIVO del nulo 2w: el cono con polarizacion LINEAL si tiene
     componente 2w -> la cota de 1e-3 SI puede enrojecer. Un cero que no puede
     diferir no es evidencia.
  P4 el pre-registro NO fija la banda de la razon; se toma su propia cota de
     lineas (1e-3) como banda operativa, y se declara esa eleccion.
"""
from __future__ import annotations

import hashlib
import math
import sys
import time
from pathlib import Path

RAIZ = Path("/Users/marlene/sfqed-paper")
sys.path.insert(0, str(RAIZ / "sim"))

import numpy as np          # noqa: E402
import field_solver as FS   # noqa: E402

TOL_LINEA = 1e-3            # [DEL PRE-REGISTRO] cota de las lineas 1w y 2w
TOL_RAZON = 1e-3            # [ELEGIDA] banda operativa de la razon (pre-registro la deja abierta)

CASOS = [
    dict(rol="JUICIO", caso="estrella", pol="circular", alpha=al, n=n, env=True, m=32, nodos=61)
    for n in (2, 4, 16) for al in (15.0, 30.0, 45.0, 60.0, 90.0)
] + [
    dict(rol="CONTROL-P2", caso="coaxial_contra", pol="circular", alpha=0.0, n=4, env=True, m=32, nodos=61),
    dict(rol="CONTROL-P3", caso="estrella", pol="lineal", alpha=30.0, n=4, env=True, m=32, nodos=61),
    dict(rol="CONTROL-env", caso="estrella", pol="circular", alpha=30.0, n=4, env=False, m=32, nodos=61),
    dict(rol="CONTROL-malla", caso="estrella", pol="circular", alpha=30.0, n=4, env=True, m=32, nodos=121),
    dict(rol="CONTROL-fases", caso="estrella", pol="circular", alpha=30.0, n=4, env=True, m=64, nodos=61),
]


def sha16(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def serie_foco(caso, pol, alpha, n, env, m, nodos):
    """Serie temporal en el nodo del foco, con la convencion EXACTA de
    field_solver.medir: E(t) = Re[Efasor e^{-i w t}] = Re*cos + Im*sin."""
    lista = FS.haces(caso, pol, alpha, n)
    Er, Br, centro = FS.campos(lista, 1.0, con_envolvente=env, nodos=nodos)
    i = centro
    E = [Er[k][i, i, i] for k in range(3)]
    B = [Br[k][i, i, i] for k in range(3)]
    th = np.arange(m) * (2.0 * math.pi / m)
    c, s = np.cos(th), np.sin(th)
    Ej = [c * x.real + s * x.imag for x in E]
    Bj = [c * x.real + s * x.imag for x in B]
    E2 = sum(e * e for e in Ej)
    B2 = sum(b * b for b in Bj)
    F = 0.5 * (E2 - B2)
    G = sum(Ej[k] * Bj[k] for k in range(3))
    rho = F * F + 7.0 * G * G
    return th, F, G, rho


def espectro(y):
    """DC y amplitud de cada armonico (k omega) de la serie muestreada."""
    m = y.size
    X = np.fft.rfft(y) / m
    dc = float(X[0].real)
    amps = {k: 2.0 * float(abs(X[k])) for k in range(1, m // 2)}
    amps[m // 2] = float(abs(X[m // 2]))
    return dc, amps


def main() -> int:
    t0 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    salida = (Path(sys.argv[1]) if len(sys.argv) > 1
              else Path(__file__).with_name("N3_FASORES_CRUDO_20261011.txt"))

    piezas = {k: sha16(RAIZ / v) for k, v in (
        ("field_solver.py", "sim/field_solver.py"),
        ("maxwell2d.py", "sim/maxwell2d.py"),
        ("main.tex", "main.tex"),
        ("pre-registro", "sim/data/vacio_no_lineal/PREREGISTRO_VACIO_NO_LINEAL_20261011.md"),
    )}

    cab = [
        "# N3_FASORES_CRUDO_20261011 -- rho_HE = c_* (F^2 + 7 G^2)/E_cr^4 en el foco",
        "# CLAUSULA: N3 del PREREGISTRO_VACIO_NO_LINEAL_20261011.md §7 (constante + UNA linea en 4w,",
        "#   razon 3/4, sin linea en 1w ni 2w; cotas de linea 1e-3 de la constante).",
        "# CAMINO: suma EXACTA de fasores de sim/field_solver.py en malla 61^3, nodo del foco.",
        "#   NO es FDTD; sim/maxwell2d.py no se importa. Costo sobre la huella del solver: 0.",
        "# LEY: F = (1/2)(|E|^2 - |B|^2), G = E.B, |B_E| = c|B|; rho homogenea de grado 4 en los campos.",
        "# MOTOR: python3 -B, numpy %s, malla de nodos impar y simetrica (el foco ES un nodo)." % np.__version__,
        "# UNIDAD: campos en unidades de la amplitud por haz E_0 = 1; rho en unidades de E_0^4.",
        "# VENTANA UTC: %s" % t0,
        "# SHA16 DE LAS ENTRADAS (medidas fuera, no citadas): "
        + " ".join("%s=%s" % (k, v) for k, v in piezas.items()),
        "# CONTROL P1 (sensor): 1 + 0.75 cos(4 th) -> razon recuperada, se imprime abajo.",
        "# CONTROL P2 (geometria): coaxial_contra -> B = 0 en el foco, F constante -> sin linea 4w.",
        "# CONTROL P3 (nulo 2w): estrella polarizacion lineal -> SI tiene 2w (la cota puede enrojecer).",
        "# CONTROL P4: el pre-registro no fija la banda de la razon; se usa su propia cota de",
        "#   lineas (1e-3) como banda operativa. ELEGIDA, declarada.",
        "# COLUMNAS: fila,rol,caso,pol,alpha_deg,N,env,m_fase,nodos,dc,amp1_rel,amp2_rel,",
        "#   amp3_rel,amp4_rel,amp5_rel,amp6_rel,maxrel_otras,razon4,delta_teo_rel",
        "#   rol=JUICIO juzga la clausula N3 (cono circular); los CONTROL se miden y se declaran,",
        "#   NO se juzgan: P2 debe dar 4w sin linea, P3 debe dar 2w con linea.",
    ]

    filas = []
    print("UNIVERSO DECLARADO: sim/field_solver.py (%s) + sim/params.py + la forma cerrada sellada"
          % piezas["field_solver.py"])
    print("  de main.tex (%s) l.478-484; ley constitutiva de sim/maxwell2d.py (%s) l.266-276."
          % (piezas["main.tex"], piezas["maxwell2d.py"]))
    print("MOTOR = python3 -B, numpy %s ; UNIDAD = E_0 por haz (amplitud) y E_0^4 (rho) ; "
          "VENTANA UTC = %s" % (np.__version__, t0))
    print("LECTURA SOLO sobre sim/ y main.tex: este script no escribe dentro del repositorio.")

    # ---- P1: control positivo del sensor ----
    thc = np.arange(32) * (2.0 * math.pi / 32)
    dcs, ampsc = espectro(1.0 + 0.75 * np.cos(4.0 * thc))
    raz_c = ampsc[4] / dcs
    print("P1 sensor (1 + 0.75 cos 4th): dc = %.16f razon4 = %.16f delta = %.3e"
          % (dcs, raz_c, abs(raz_c - 0.75)))
    p1_ok = abs(raz_c - 0.75) < 1e-12
    filas.append("# P1 sensor  1+0.75 cos4th  dc=%.16f  razon4=%.16f  delta=%.3e  ok=%s"
                 % (dcs, raz_c, abs(raz_c - 0.75), p1_ok))

    print("%-24s %-8s %5s %3s %5s %4s %5s %12s %9s %9s %9s %9s %9s %8s"
          % ("rol:caso", "pol", "alpha", "N", "env", "m", "nodos", "dc", "a1/dc", "a2/dc",
             "a3/dc", "a4/dc", "maxotr", "delta_teo"))
    fallos = []
    fila_i = 0
    for cs in CASOS:
        th, F, G, rho = serie_foco(cs["caso"], cs["pol"], cs["alpha"], cs["n"],
                                   cs["env"], cs["m"], cs["nodos"])
        dc, amps = espectro(rho)
        rel = {k: (amps[k] / dc if dc else float("nan")) for k in amps}
        otros = max([abs(rel[k]) for k in rel if k != 4] or [0.0])
        razon = rel.get(4, float("nan"))
        dteo = float("nan")
        if cs["caso"] == "estrella" and cs["pol"] == "circular":
            ef = cs["n"] * math.sin(math.radians(cs["alpha"]))
            teo = ef ** 4 * (1.0 - 0.75 * np.cos(4.0 * th))
            dteo = float(np.abs(rho - teo).max() / np.abs(teo).max())
        fila_i += 1
        filas.append("%d,%s,%s,%s,%.1f,%d,%d,%d,%d,%.12e,%.6e,%.6e,%.6e,%.6e,%.6e,%.6e,%.6e,%.16f,%.6e"
                     % (fila_i, cs["rol"], cs["caso"], cs["pol"], cs["alpha"], cs["n"],
                        int(cs["env"]), cs["m"], cs["nodos"], dc, abs(rel.get(1, 0.0)),
                        abs(rel.get(2, 0.0)), abs(rel.get(3, 0.0)), abs(rel.get(4, 0.0)),
                        abs(rel.get(5, 0.0)), abs(rel.get(6, 0.0)), otros, razon, dteo))
        print("%-24s %-8s %5.1f %3d %5d %4d %5d %12.6e %9.2e %9.2e %9.2e %9.6f %9.2e %8s"
              % ("%s:%s" % (cs["rol"], cs["caso"]), cs["pol"], cs["alpha"], cs["n"],
                 int(cs["env"]), cs["m"], cs["nodos"], dc, abs(rel.get(1, 0.0)),
                 abs(rel.get(2, 0.0)), abs(rel.get(3, 0.0)), razon, otros,
                 ("%.2e" % dteo) if dteo == dteo else "-"))
        # La clausula N3 se juzga SOLO en los casos de JUICIO (cono circular).
        # Los CONTROLES deben diferir a proposito: se miden, no se juzgan aqui.
        if cs["rol"] == "JUICIO":
            if abs(rel.get(1, 0.0)) > TOL_LINEA:
                fallos.append("N3: linea 1w = %.3e (N=%d alpha=%.0f)"
                              % (abs(rel.get(1, 0.0)), cs["n"], cs["alpha"]))
            if abs(rel.get(2, 0.0)) > TOL_LINEA:
                fallos.append("N3: linea 2w = %.3e (N=%d alpha=%.0f)"
                              % (abs(rel.get(2, 0.0)), cs["n"], cs["alpha"]))
            if abs(rel.get(3, 0.0)) > TOL_LINEA:
                fallos.append("N3: linea 3w = %.3e (N=%d alpha=%.0f)"
                              % (abs(rel.get(3, 0.0)), cs["n"], cs["alpha"]))
            if otros > TOL_LINEA:
                fallos.append("N3: linea espuria = %.3e (N=%d alpha=%.0f)"
                              % (otros, cs["n"], cs["alpha"]))
            if abs(razon - 0.75) > TOL_RAZON:
                fallos.append("N3: razon 4w/dc = %.16f != 0.75 (N=%d alpha=%.0f)"
                              % (razon, cs["n"], cs["alpha"]))
            if dteo == dteo and dteo > 1e-12:
                fallos.append("N3: la serie no reproduce la forma cerrada (delta=%.3e)"
                              % dteo)
        elif cs["rol"] in ("CONTROL-env", "CONTROL-malla", "CONTROL-fases"):
            # no son la clausula: son nulos del metro que SI pueden diferir.
            if abs(razon - 0.75) > TOL_RAZON:
                fallos.append("%s: razon 4w/dc = %.16f != 0.75" % (cs["rol"], razon))
            if max(abs(rel.get(1, 0.0)), abs(rel.get(2, 0.0)), otros) > TOL_LINEA:
                fallos.append("%s: linea espuria por encima de 1e-3" % cs["rol"])

    if not p1_ok:
        fallos.append("P1: el sensor no recupera 0.75")

    # ---- P3: el nulo 2w TIENE que poder enrojecer ----
    th, F, G, rho = serie_foco("estrella", "lineal", 30.0, 4, True, 32, 61)
    dc_l, amps_l = espectro(rho)
    rel2_l = amps_l[2] / dc_l
    print("P3 nulo 2w (estrella lineal N=4 alpha=30): 2w/dc = %.6f  (si el metro fuera ciego, seria 0)"
          % rel2_l)
    filas.append("# P3 estrella lineal: 2w/dc = %.6e  (control positivo del nulo: 2w SI existe)" % rel2_l)
    if rel2_l <= TOL_LINEA:
        fallos.append("P3: el metro NO ve la linea 2w del cono lineal (%.3e): el nulo no puede diferir"
                      % rel2_l)

    # ---- P2: la geometria coaxial no debe dar 4w ----
    th, F, G, rho = serie_foco("coaxial_contra", "circular", 0.0, 4, True, 32, 61)
    dc_c, amps_c = espectro(rho)
    print("P2 negativo (coaxial_contra N=4): dc = %.12e  4w/dc = %.3e  (B = 0 en el foco)"
          % (dc_c, amps_c[4] / dc_c))
    filas.append("# P2 coaxial_contra: dc = %.12e  4w/dc = %.3e" % (dc_c, amps_c[4] / dc_c))

    rc = 0 if not fallos else 1
    ver = "CONFORME" if rc == 0 else "FRACTURA"
    cab.append("# RESULTADO: %s · los tres puntos de N3 (forma, razon, nulos) medidos." % ver)

    salida.write_text("\n".join(cab + filas) + "\n", encoding="utf-8")
    print("---")
    if fallos:
        for f in fallos:
            print("ROJO: " + f)
    print("N3 · %s · RC %d · MOTOR python3-B/numpy %s · SHA16 field_solver.py=%s "
          "maxwell2d.py=%s main.tex=%s · CRUDO: %s"
          % (ver, rc, np.__version__, piezas["field_solver.py"], piezas["maxwell2d.py"],
             piezas["main.tex"], salida))
    return rc


if __name__ == "__main__":
    sys.exit(main())
