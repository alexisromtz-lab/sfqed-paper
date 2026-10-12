#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DRIVER DEL EXPONENTE DE CONVERGENCIA `p` CON UNA TERCERA MALLA (nodos = 481).

RUTA B (pre-registro seccion 7): driver NUEVO que IMPORTA el instrumento viejo
en modo lectura y NO lo edita. La Ruta A (parchear main() del instrumento) fue
RECHAZADA POR DEFECTO.

CONTRATO DEL QUE NACE (pre-registro sellado, NO se edita):
    sim/PREREGISTRO_CONVERGENCIA_P_20261012.md
    l=326  b=17111  sha16=7476477b58cda501
Padres declarados: sim/PREREGISTRO_INVOCACION_LECTOR_INVARIANTES_20261012.md:243
  sim/PREREGISTRO_PARIDAD_CONMUTADOR_V2_20261012.md:118
  sim/ACTA_DEL_FALSO_ROJO_DE_V1_Y_EL_VETO_SUSTANTIVO_DE_V5_20261011.md seccion 7
  sim/ACTA_DEL_CICLO_V2_EL_VERDE_5_5_Y_EL_DESFASE_DECLARADO_20261012.md seccion 9

OBJETO: la terna (R, h, geometria) del instrumento pareado y su residuo
        eps(h) = R_L4(h) / R_0 - 1
con R_0 = referencia INTRINSECA de la MISMA geometria (lectura L0_exacto a 361
nodos, dx = lambda/60). La referencia NO se afina con la malla: es fija.

ESTIMADOR (verbatim del pre-registro, seccion 2):
        p(h1 -> h2) = log( eps(h1) / eps(h2) ) / log( h1 / h2 )

UNIVERSO DECLARADO:
  DENOMINADOR = referencia intrinseca L0_exacto a 361 nodos de la MISMA
                geometria (misma convencion que el bloque D del instrumento).
  MOTOR       = python3 -B + sim/control_pareado_convergente.py importado SOLO
                LECTURA (sha16 del import se imprime y se re-mide al cerrar).
  UNIDAD      = nodos por lado y h = dx/lambda = 6.0/(nodos-1).
  VENTANA     = hora UTC impresa en la cabecera y en el crudo.
  UMBRAL      = bandas pre-registradas del pre-registro seccion 4.

Mallas y ley de afinamiento: nodos = 60*2**k + 1  ->  h = 0.1*2**(-k)
  61 -> 0.1  ·  121 -> 0.05  ·  241 -> 0.025  ·  481 -> 0.0125 (= lambda/80)
Cada escalon divide h por 2 EXACTO: el driver lo MIDE y lo imprime, no lo supone.

CONTROLES (todos imprimen su CAUSA, no solo su codigo):
  C0  certificado del arnes: la receta heredada en 61/121/241 debe reproducir
      las SEIS cifras de `p` publicadas y los NUEVE porcentajes de exceso.
      Certificado por medicion propia (hora 2026-10-12T07:14:20Z, RC=0) antes
      de sellar este archivo: la receta se reprodujo digito a digito.
      Si una cifra difiere en el ULTIMO DIGITO IMPRESO -> CONTRATO ROTO, rc=2,
      y E3 NO se mide.
  C1  positivo sintetico: eps = C*h**p para p en {1.00, 1.50, 1.93, 2.00}
      sobre h = 0.1, 0.05, 0.025, 0.0125 (incluye el escalon E3). error <= 1e-12.
  C2  negativo sintetico: eps = C*h*log(1/h) -> p != 2 y p difiere ENTRE
      escalones. Un control que no puede diferir no es un control.
  C3  guarda de cero entradas (probada con 4 casos y su causa impresa).
  C4  control de la referencia: eps debe DECRECER al refinar, por geometria.

PROHIBICIONES:
  - No se toca sim/maxwell2d.py, sim/medidas_aN.csv, sim/control_pareado_convergente.py.
  - No se escribe en bundle/.
  - No se declara `p = 2` exacto como resultado.
  - Unica escritura permitida: el crudo declarado, dentro de sim/data/invariantes/.

USO:
    python3 -B sim/driver_convergencia_p.py --nodos 61,121,241,481 --geometrias 3 --json
    python3 -B sim/driver_convergencia_p.py --sin-escribir     (no escribe crudo)

RC: 0 = banda VERDE en las tres geometrias y monotono
    1 = cualquier otra banda (GRIS / ROJO / MIXTO declarado)
    2 = CONTRATO ROTO o SIN MEDIDA (nunca un verde parcial)
"""

import argparse
import hashlib
import json
import math
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
if str(AQUI) not in sys.path:
    sys.path.insert(0, str(AQUI))

# SOLO LECTURA: el instrumento heredado. Importarlo no escribe (su main() esta
# detras de `if __name__ == "__main__"`).
import control_pareado_convergente as C

# ---------------------------------------------------------------- declarados
DATOS = AQUI / "data" / "invariantes"
CRUDO = DATOS / "convergencia_p_tercera_malla_20261012.json"
INSTRUMENTO = AQUI / "control_pareado_convergente.py"
MEDIDAS_A_N = AQUI / "medidas_aN.csv"

REF_NODOS = 361                      # referencia intrinseca heredada (dx = lambda/60)
LEY_NODOS = (61, 121, 241, 481)      # nodos = 60*2**k + 1, k = 0..3
NODOS_TERCERA_MALLA = 481            # la malla que este ciclo estrena (dx = lambda/80)

TOL_ULTIMO_DIGITO = 5.0e-5           # medio escalon del ultimo decimal impreso (4 dec)
TOL_SINTETICO = 1.0e-12              # error maximo admitido en C1
PISO_LOG = 1.0e-12                   # piso de cableado para log(h1/h2) != 0
BANDA_VERDE = (1.96, 2.00)           # [1.96, 2.00)  p3 >= p2 en las tres
BANDA_GRIS = (1.90, 1.96)            # [1.90, 1.96)  exigiria una 4a malla (961)
PISO_NO_SATURA = 1.90                # p3 < 1.90  -> ROJO NO-SATURA
TECHO_SOBREPASO = 2.00               # p3 >= 2.00 -> ROJO SOBREPASO

# Geometrias declaradas (pre-registro seccion 0.3): alpha_deg, m, etiqueta
GEOMETRIAS = (
    (30.0, 17, "abanico 30.0 m=17"),
    (26.5651, 17, "abanico 26.5651 m=17"),
    (30.0, 9, "abanico 30.0 m=9"),
)

# Cifras HEREDADAS del pre-registro seccion 0.3 (fuente: abstract marco fibrado
# seccion 5.b, tabla de secuencia de malla). Certificadas por medicion propia.
HEREDADO = (
    ((30.0, 17), (33.9658, 9.6907, 2.5226), 1.8094, 1.9417),
    ((26.5651, 17), (43.0890, 12.6034, 3.3138), 1.7735, 1.9273),
    ((30.0, 9), (30.4986, 8.6149, 2.2341), 1.8238, 1.9471),
)


# ------------------------------------------------------------------ utileria
def sha16(ruta):
    """sha256(bytes)[:16] del archivo; la UNIDAD del metro se declara aqui."""
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()[:16]


def h_de(nodos):
    """h = dx/lambda del instrumento, en unidades de lambda.

    Declarado: NO lleva la constante fisica LAMBDA. El instrumento heredado
    imprime su columna `dx/l` como LADO/(nodos-1) (bloque D), y la unidad del
    objeto es adimensional. Meter LAMBDA aqui daria 1e-7 y el cociente h1/h2
    seguiria dando 2: el defecto seria invisible en p y visible solo en la
    columna impresa. La columna impresa tambien es medicion.
    """
    return C.LADO / float(nodos - 1)


def eps_de(R, R0):
    """Residuo relativo del objeto: eps = R(h)/R_0 - 1."""
    return R / R0 - 1.0


def p_de(e1, e2, h1, h2):
    """Estimador del pre-registro. Levanta ValueError con la CAUSA si no aplica."""
    if not (e1 > 0.0):
        raise ValueError("eps(h1) = %.6e no es > 0" % e1)
    if not (e2 > 0.0):
        raise ValueError("eps(h2) = %.6e no es > 0" % e2)
    lr = math.log(h1 / h2)
    if abs(lr) < PISO_LOG:
        raise ValueError("log(h1/h2) = %.6e esta por debajo del piso %.1e" % (lr, PISO_LOG))
    return math.log(e1 / e2) / lr


def ley_de(nodos):
    """Devuelve k si nodos cumple nodos = 60*2**k + 1, si no None."""
    for k, n in enumerate(LEY_NODOS):
        if nodos == n:
            return k
    return None


def banda_de_p3(p3):
    if p3 >= TECHO_SOBREPASO:
        return "ROJO SOBREPASO"
    if p3 >= BANDA_VERDE[0]:
        return "VERDE"
    if p3 >= BANDA_GRIS[0]:
        return "GRIS"
    return "ROJO NO-SATURA"


def fmt4(x):
    return "%+.4f" % x


# ------------------------------------------------------------------ controles
def control_C1():
    """Positivo sintetico: eps = C*h**p, con el escalon E3 incluido."""
    print("C1 POSITIVO SINTETICO: eps = C*h**p sobre h = 0.1, 0.05, 0.025, 0.0125")
    hs = [0.1, 0.05, 0.025, 0.0125]
    C0 = 3.0
    ok = True
    datos = []
    for p in (1.00, 1.50, 1.93, 2.00):
        es = [C0 * h ** p for h in hs]
        ps = [p_de(es[i], es[i + 1], hs[i], hs[i + 1]) for i in range(3)]
        err = max(abs(v - p) for v in ps)
        bien = err <= TOL_SINTETICO
        ok = ok and bien
        datos.append({"p": p, "medido": ps, "error": err})
        print("   p=%.2f  medido= %.10f %.10f %.10f  error=%.2e  %s"
              % (p, ps[0], ps[1], ps[2], err, "OK" if bien else "FALLA"))
    if not ok:
        print("   CAUSA: el estimador no recupera un exponente constante plantado")
    return ok, datos


def control_C2():
    """Negativo sintetico: eps = C*h*log(1/h) -> no es 2 y difiere por escalon."""
    print("C2 NEGATIVO SINTETICO: eps = C*h*log(1/h)  (exponente NO constante)")
    hs = [0.1, 0.05, 0.025, 0.0125]
    C0 = 3.0
    es = [C0 * h * math.log(1.0 / h) for h in hs]
    ps = [p_de(es[i], es[i + 1], hs[i], hs[i + 1]) for i in range(3)]
    no_es_dos = all(abs(v - 2.0) > 1.0e-3 for v in ps)
    difiere = abs(ps[0] - ps[1]) > 1.0e-3
    ok = bool(no_es_dos and difiere)
    print("   p estimado = %.4f %.4f %.4f   no-es-2=%s  difiere-e1-e2=%s  %s"
          % (ps[0], ps[1], ps[2], no_es_dos, difiere, "OK" if ok else "FALLA"))
    if not ok:
        print("   CAUSA: el control no discrimina (no puede diferir de 2 o no varia)")
    return ok, {"p": ps, "no_es_dos": bool(no_es_dos), "difiere": bool(difiere)}


def guardia_escalones(nodos, epss):
    """Guarda de cero entradas. Devuelve (ok, causa). No imprime."""
    if len(nodos) < 3:
        return False, "%d malla(s): con menos de 3 puntos beta es un ajuste, no una pendiente" % len(nodos)
    if len(nodos) != len(epss):
        return False, "%d mallas contra %d eps: la terna no esta alineada" % (len(nodos), len(epss))
    for i, e in enumerate(epss):
        if not (e > 0.0):
            return False, "eps(h[%d]) = %.6e no es > 0" % (i, e)
    for i in range(len(nodos) - 1):
        lr = math.log(h_de(nodos[i]) / h_de(nodos[i + 1]))
        if abs(lr) < PISO_LOG:
            return False, "log(h[%d]/h[%d]) = %.6e esta por debajo del piso %.1e" % (i, i + 1, lr, PISO_LOG)
    return True, "3 o mas mallas, eps > 0 y log(h1/h2) != 0"


def control_C3():
    """Prueba la guarda de cero entradas con 4 casos y su causa impresa."""
    print("C3 GUARDA DE CERO ENTRADAS (se prueba a si misma y declara la causa)")
    casos = (
        ("positivo  4 mallas eps>0", [61, 121, 241, 481], [0.3, 0.06, 0.015, 0.0037], True),
        ("negativo  2 mallas", [61, 121], [0.3, 0.06], False),
        ("negativo  eps <= 0", [61, 121, 241], [0.3, -0.06, 0.015], False),
        ("negativo  h1 == h2", [241, 241, 481], [0.3, 0.06, 0.015], False),
    )
    ok = True
    datos = []
    for nombre, ns, es, esperado in casos:
        bien, causa = guardia_escalones(ns, es)
        acierta = (bien == esperado)
        ok = ok and acierta
        datos.append({"caso": nombre, "ok": bool(bien), "causa": causa, "esperado": bool(esperado)})
        print("   %-26s -> %-5s esperado=%-5s %s  CAUSA: %s"
              % (nombre, str(bien), str(esperado), "OK" if acierta else "FALLA", causa))
    if not ok:
        print("   CAUSA: la guarda no separa el caso sano de los tres defectuosos")
    return ok, datos


# --------------------------------------------------------------- pre-registro
def pre_registro(nodos, geos, hora):
    print("=" * 78)
    print("DRIVER DEL EXPONENTE p CON UNA TERCERA MALLA  (Ruta B: instrumento importado, SOLO LECTURA)")
    print("UNIVERSO DECLARADO: 3 geometrias abanico con secuencia de malla; DENOMINADOR =")
    print("  referencia intrinseca L0_exacto a %d nodos de la MISMA geometria (dx = lambda/%.0f);" % (REF_NODOS, (REF_NODOS - 1) / C.LADO))
    print("  MOTOR = python3 -B + %s (importado, no editado);" % INSTRUMENTO.name)
    print("  UNIDAD = nodos por lado y h = dx/lambda = %.1f/(nodos-1);" % C.LADO)
    print("  VENTANA = %s (UTC);  UMBRAL = bandas del pre-registro seccion 4." % hora)
    print("  MALLAS = %s ; TERCERA MALLA PRE-REGISTRADA = %d" % (",".join(str(n) for n in nodos), NODOS_TERCERA_MALLA))
    print("  GEOMETRIAS = %d declaradas" % geos)
    for k, n in enumerate(nodos):
        h = h_de(n)
        print("    nodos=%-5d h=%.6f  ley 60*2**k+1 = %s" % (n, h, ("k=%d OK" % k) if ley_de(n) is not None else "FUERA DE LA LEY (declarado)"))
    for i in range(len(nodos) - 1):
        print("    escalon E%d: %d -> %d   log(h1/h2) = %.12f" % (i + 1, nodos[i], nodos[i + 1], math.log(h_de(nodos[i]) / h_de(nodos[i + 1]))))
    print("=" * 78)


def cadena(nodos):
    """Recorre el objeto: R_0 por geometria y las tres lecturas en cada malla."""
    filas = []
    for al, m, etiqueta in GEOMETRIAS:
        psis = C.abanico_2d(al, m)
        r0 = C.razon_2d(psis, REF_NODOS, C.E_A0_1, con_yee=False)["L0_exacto"]
        print("[%s]  R_0(%d nodos, dx = lambda/%d) = %.16f   F_rel=%.6e  G_rel=%.2e"
              % (etiqueta, REF_NODOS, int((REF_NODOS - 1) / C.LADO), r0["R"], r0["F_rel"], r0["G_rel"]))
        eps = []
        lecturas = {}
        for n in nodos:
            ry = C.razon_2d(psis, n, C.E_A0_1, con_yee=True)
            l4 = ry["L4_completo"]
            e = eps_de(l4["R"], r0["R"])
            eps.append(e)
            lecturas[str(n)] = {
                "L1_naive": ry["L1_naive"]["R"],
                "L2_lector": ry["L2_lector"]["R"],
                "L4_completo": l4["R"],
                "nan_extra_declarada": l4.get("nan_extra_declarada", None),
                "ij": l4.get("ij", None),
                "eps": e,
                "eps_pct": 100.0 * e,
            }
            print("    nodos=%-5d dx/l=%.6f  R_L4=%.16f  eps= %s pct   nan_extra=%s"
                  % (n, h_de(n), l4["R"], fmt4(100.0 * e), l4.get("nan_extra_declarada", None)))
        filas.append({"al": al, "m": m, "etiqueta": etiqueta, "R0": r0["R"],
                      "R0_F_rel": r0["F_rel"], "R0_G_rel": r0["G_rel"],
                      "eps": eps, "lecturas": lecturas})
    return filas


def control_C0(filas, nodos):
    """Certificado del arnes: la receta heredada debe reproducir las seis p y los nueve eps%."""
    print("-" * 78)
    print("C0 CERTIFICADO DEL ARNES -- receta heredada en %s" % ",".join(str(n) for n in nodos[:3]))
    print("   tolerancia = %.1e (medio escalon del ultimo decimal impreso, 4 decimales)" % TOL_ULTIMO_DIGITO)
    idx = {n: i for i, n in enumerate(nodos)}
    if not all(n in idx for n in nodos[:3]):
        print("   CAUSA: el certificado exige las mallas heredadas %s" % (nodos[:3],))
        return False, {}
    ok = True
    datos = {}
    for (al, m), heredado_pct, hp1, hp2 in HEREDADO:
        fila = [f for f in filas if f["al"] == al and f["m"] == m]
        if not fila:
            print("   CAUSA: geometria %s m=%d declarada como heredada y ausente de la corrida" % (al, m))
            ok = False
            continue
        f = fila[0]
        i1, i2, i3 = idx[nodos[0]], idx[nodos[1]], idx[nodos[2]]
        e1, e2, e3 = f["eps"][i1], f["eps"][i2], f["eps"][i3]
        p1 = p_de(e1, e2, h_de(nodos[i1]), h_de(nodos[i2]))
        p2 = p_de(e2, e3, h_de(nodos[i2]), h_de(nodos[i3]))
        pct = (100.0 * e1, 100.0 * e2, 100.0 * e3)
        est_pct = tuple(fmt4(v) for v in pct)
        esp_pct = tuple(fmt4(v) for v in heredado_pct)
        est_p = (fmt4(p1), fmt4(p2))
        esp_p = (fmt4(hp1), fmt4(hp2))
        bien = (est_pct == esp_pct) and (est_p == esp_p)
        ok = ok and bien
        msg_pct = "IDENTICO" if est_pct == esp_pct else "DIVERGE"
        msg_p = "IDENTICO" if est_p == esp_p else "DIVERGE"
        print("   [%s]" % f["etiqueta"])
        print("      eps%%  heredado %s %s %s  | medido %s %s %s  %s"
              % (esp_pct[0], esp_pct[1], esp_pct[2], est_pct[0], est_pct[1], est_pct[2], msg_pct))
        print("      p     heredado %s %s        | medido %s %s        %s"
              % (esp_p[0], esp_p[1], est_p[0], est_p[1], msg_p))
        print("      (crudo p=%.6f %.6f  eps%%=%.6f %.6f %.6f)"
              % (p1, p2, pct[0], pct[1], pct[2]))
        datos[f["etiqueta"]] = {"heredado_pct": esp_pct, "medido_pct": est_pct,
                               "heredado_p": esp_p, "medido_p": est_p,
                               "medido_raw": {"p1": p1, "p2": p2, "eps_pct": pct}}
    if not ok:
        print("   CAUSA: la receta heredada NO se reproduce digito a digito sobre el instrumento de hoy")
    else:
        print("   C0 OK: las seis cifras de p y los nueve porcentajes se reproducen digito a digito")
    return ok, datos


def control_C4(filas, nodos):
    """La referencia debe hacer que eps decrezca al refinar, por geometria."""
    print("-" * 78)
    print("C4 CONTROL DE LA REFERENCIA -- eps debe DECRECER al refinar h")
    ok = True
    datos = []
    for f in filas:
        mono = all(f["eps"][i + 1] < f["eps"][i] for i in range(len(f["eps"]) - 1))
        ok = ok and mono
        datos.append({"etiqueta": f["etiqueta"], "monotono": bool(mono), "eps": list(f["eps"])})
        if not mono:
            malos = [(nodos[i], nodos[i + 1], f["eps"][i], f["eps"][i + 1])
                     for i in range(len(f["eps"]) - 1) if not f["eps"][i + 1] < f["eps"][i]]
            print("   CAUSA: [%s] eps NO decrece en %s" % (f["etiqueta"], malos))
        else:
            print("   [%s] eps decrece en los %d escalones  OK" % (f["etiqueta"], len(f["eps"]) - 1))
    return ok, datos


def objeto(filas, nodos):
    """Extrae p en cada escalon, imprime C5 y decide el veredicto por bandas."""
    print("-" * 78)
    print("OBJETO -- p por escalon (C5: banda de p3 junto a las bandas de E1 y E2)")
    res = []
    bandas = []
    monotono = True
    # Guarda de contrato ANTES de extraer: sin 3 escalones no hay E3 que medir, y
    # sin correspondencia 1 a 1 entre filas y receta heredada no hay C0 que citar.
    # Se declara la causa en vez de reventar en la aritmetica de abajo.
    if len(nodos) < 3:
        print("   CAUSA: %d malla(s): con menos de 3 nodos no existe el escalon E3"
              % len(nodos))
        return 2, "ROJO SIN E3", res
    if len(filas) != len(HEREDADO):
        print("   CAUSA: %d geometrias medidas contra %d declaradas en HEREDADO"
              % (len(filas), len(HEREDADO)))
        return 2, "ROJO GEOMETRIAS", res
    for f in filas:
        ps = [p_de(f["eps"][i], f["eps"][i + 1], h_de(nodos[i]), h_de(nodos[i + 1]))
              for i in range(len(nodos) - 1)]
        idx3 = len(nodos) - 1
        p3 = ps[idx3 - 1] if len(ps) >= 3 else None
        p2 = ps[idx3 - 2] if len(ps) >= 2 else None
        b3 = banda_de_p3(p3)
        b2 = banda_de_p3(p2) if p2 is not None else "N/A"
        b1 = banda_de_p3(ps[0])
        mon = (p3 is None) or (p3 >= p2)
        monotono = monotono and mon
        bandas.append(b3)
        h3 = h_de(nodos[-1])
        c_p3 = f["eps"][-1] / h3 ** p3
        c_p2 = f["eps"][-1] / h3 ** 2.0
        res.append({"etiqueta": f["etiqueta"], "p": ps, "p3": p3, "p2": p2,
                    "banda_p3": b3, "banda_p2": b2, "banda_p1": b1,
                    "monotono": bool(mon), "C_p3": c_p3, "C_p2": c_p2,
                    "h3": h3, "eps3": f["eps"][-1]})
        print("   [%s]" % f["etiqueta"])
        print("      E1 p=%s [%s]   E2 p=%s [%s]   E3 p=%s [%s]   p2-p1=%+.4f  p3-p2=%+.4f"
              % (fmt4(ps[0]), b1, fmt4(ps[1]), b2, fmt4(p3), b3, ps[1] - ps[0], p3 - ps[1]))
        print("      par (p, C) publicado: (%.6f, %.6f) con p=p3   |   (%.6f, %.6f) con p=2 fijo"
              % (p3, c_p3, p3, c_p2))
        if not mon:
            print("      CAUSA: p3 < p2 -> NO-MONOTONO en esta geometria")

    distintas = sorted(set(bandas))
    if not monotono:
        veredicto = "ROJO NO-MONOTONO"
        rc = 1
    elif len(distintas) > 1:
        veredicto = "MIXTO (declarado, NO adjudicado): bandas %s" % ",".join(distintas)
        rc = 1
    elif distintas[0] == "VERDE":
        veredicto = "VERDE -- p desacelera hacia 2 desde abajo sin alcanzarlo, en las tres geometrias"
        rc = 0
    else:
        veredicto = distintas[0]
        rc = 1
    print("-" * 78)
    print("BANDAS DECLARADAS: VERDE [%.2f, %.2f) y p3 >= p2  ·  GRIS [%.2f, %.2f) (exigiria %d nodos)  ·  ROJO NO-SATURA p3 < %.2f  ·  ROJO SOBREPASO p3 >= %.2f  ·  ROJO NO-MONOTONO p3 < p2"
          % (BANDA_VERDE[0], BANDA_VERDE[1], BANDA_GRIS[0], BANDA_GRIS[1], 961, PISO_NO_SATURA, TECHO_SOBREPASO))
    print("p = 2 EXACTO NO SE ESCRIBE COMO RESULTADO. Se publica el par (p, C).")
    print("VEREDICTO: %s" % veredicto)
    return rc, veredicto, res


def main(argv=None):
    ap = argparse.ArgumentParser(description="Exponente de convergencia p con una tercera malla (nodos=481).")
    ap.add_argument("--nodos", default="61,121,241,481", help="lista de mallas, creciente")
    ap.add_argument("--geometrias", type=int, default=3, help="numero de geometrias declaradas (debe ser 3)")
    ap.add_argument("--sin-escribir", action="store_true", help="no escribe el crudo")
    ap.add_argument("--json", action="store_true", help="imprime el crudo por stdout")
    a = ap.parse_args(argv)

    t0 = time.time()
    hora = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    nodos = [int(x) for x in a.nodos.split(",") if x.strip()]
    pre_registro(nodos, a.geometrias, hora)

    sha_inst_antes = sha16(INSTRUMENTO)
    sha_med_antes = sha16(MEDIDAS_A_N)
    print("IDENTIDAD AL ABRIR: instrumento %s = %s ; medidas_aN.csv = %s ; pre-registro = 7476477b58cda501"
          % (INSTRUMENTO.name, sha_inst_antes, sha_med_antes))

    # ---- contrato de destino y de universo (antes de cualquier medicion)
    if a.geometrias != 3:
        print("CONTRATO ROTO: se pidieron %d geometrias y el universo declarado son 3 "
              "(las tres con secuencia de malla en el crudo del falsador)." % a.geometrias)
        print("VEREDICTO: SIN MEDIDA.")
        return 2
    if len(nodos) < 3:
        print("CONTRATO ROTO: %d malla(s) -> con menos de 3 puntos beta es un ajuste, no una pendiente." % len(nodos))
        print("VEREDICTO: SIN MEDIDA.")
        return 2
    if sorted(nodos) != nodos or len(set(nodos)) != len(nodos):
        print("CONTRATO ROTO: las mallas deben ir estrictamente crecientes y sin repetir: %s" % nodos)
        print("VEREDICTO: SIN MEDIDA.")
        return 2
    if NODOS_TERCERA_MALLA not in nodos:
        print("CONTRATO ROTO: la tercera malla pre-registrada es %d y la corrida no la incluye (%s)."
              % (NODOS_TERCERA_MALLA, nodos))
        print("VEREDICTO: SIN MEDIDA.")
        return 2

    # ---- controles sinteticos primero (el orden del instrumento hermano)
    ok1, d1 = control_C1()
    ok2, d2 = control_C2()
    ok3, d3 = control_C3()
    if not (ok1 and ok2 and ok3):
        print("CONTRATO ROTO: fallo un control sintetico (C1=%s C2=%s C3=%s)." % (ok1, ok2, ok3))
        print("VEREDICTO: SIN MEDIDA.")
        return 2
    print("C1 C2 C3 OK: el estimador recupera lo plantado, discrimina y la guarda separa los casos.")

    # ---- el objeto
    filas = cadena(nodos)

    # ---- guardas de objeto (pre-registro seccion 2)
    for f in filas:
        bien, causa = guardia_escalones(nodos, f["eps"])
        if not bien:
            print("CONTRATO ROTO: [%s] %s" % (f["etiqueta"], causa))
            print("VEREDICTO: SIN MEDIDA.")
            return 2

    # ---- C0 antes de extraer E3
    ok0, d0 = control_C0(filas, nodos)
    if not ok0:
        print("CONTRATO ROTO: el certificado del arnes no pasa. E3 NO se mide.")
        print("VEREDICTO: SIN MEDIDA.")
        return 2

    ok4, d4 = control_C4(filas, nodos)
    if not ok4:
        print("CONTRATO ROTO: la referencia no hace decrecer eps. E3 NO se mide.")
        print("VEREDICTO: SIN MEDIDA.")
        return 2

    rc, veredicto, res = objeto(filas, nodos)
    if rc == 2:
        print("CONTRATO ROTO: el objeto no se pudo extraer. CRUDO NO ESCRITO.")
        print("VEREDICTO: SIN MEDIDA.")
        return 2

    sha_inst_desp = sha16(INSTRUMENTO)
    sha_med_desp = sha16(MEDIDAS_A_N)
    intacto = (sha_inst_antes == sha_inst_desp) and (sha_med_antes == sha_med_desp)
    if not intacto:
        print("CONTRATO ROTO: un archivo sellado se movio durante la corrida "
              "(instrumento %s->%s ; medidas %s->%s)." % (sha_inst_antes, sha_inst_desp, sha_med_antes, sha_med_desp))
        rc = 2
        veredicto = "SIN MEDIDA (archivo sellado movido)"

    crudo = {
        "T_UTC": hora,
        "universo_declarado": ("3 geometrias abanico; DENOMINADOR = L0_exacto a %d nodos de la MISMA geometria; "
                              "MOTOR = python3 -B + control_pareado_convergente.py importado SOLO LECTURA; "
                              "UNIDAD = nodos y h = dx/lambda; VENTANA = T_UTC; UMBRAL = bandas seccion 4." % REF_NODOS),
        "mallas": nodos,
        "ley_de_afinamiento": "nodos = 60*2**k + 1 -> h = 0.1*2**(-k)",
        "referencia_nodos": REF_NODOS,
        "referencia_dx_sobre_lambda": C.LADO / (REF_NODOS - 1),
        "geometrias": {f["etiqueta"]: {"alpha_deg": f["al"], "m": f["m"], "R0": f["R0"],
                                       "R0_F_rel": f["R0_F_rel"], "R0_G_rel": f["R0_G_rel"],
                                       "lecturas": f["lecturas"]} for f in filas},
        "escalones": {f["etiqueta"]: {"eps": f["eps"], "eps_pct": [100.0 * e for e in f["eps"]]} for f in filas},
        "control_C0": d0,
        "control_C1": d1,
        "control_C2": d2,
        "control_C3": d3,
        "control_C4": d4,
        "objeto": res,
        "veredicto": veredicto,
        "rc": rc,
        "segundos": time.time() - t0,
        "sha16": {"field_solver": sha16(AQUI / "field_solver.py"),
                  "lector": sha16(AQUI / "lector_invariantes.py"),
                  "maxwell2d": sha16(AQUI / "maxwell2d.py"),
                  "instrumento": sha_inst_desp,
                  "medidas_aN_csv": sha_med_desp,
                  "driver": sha16(Path(__file__).resolve())},
        "medidas_aN_intacto": bool(intacto),
    }

    sha_crudo = "NO ESCRITO"
    ruta_crudo = str(CRUDO)
    if not a.sin_escribir:
        DATOS.mkdir(parents=True, exist_ok=True)
        with open(CRUDO, "w", encoding="utf-8") as f:
            json.dump(crudo, f, indent=1, sort_keys=True, ensure_ascii=False)
            f.write("\n")
        sha_crudo = sha16(CRUDO)
    if a.json:
        print(json.dumps(crudo, indent=1, sort_keys=True, ensure_ascii=False))

    print("CIERRE: escalones=%d mallas=%d geometrias=%d segundos=%.1f cronologia=%s"
          % (len(nodos) - 1, len(nodos), len(filas), crudo["segundos"],
             "PREREGISTRO < DRIVER < CRUDO" if not a.sin_escribir else "truncada (sin crudo)"))
    print("VEREDICTO: %s" % veredicto)
    print("VEREDICTO · RC=%d · MOTOR=python3 -B · SHA16=%s · CRUDO: %s" % (rc, sha_crudo, ruta_crudo))
    return rc


if __name__ == "__main__":
    sys.exit(main())
