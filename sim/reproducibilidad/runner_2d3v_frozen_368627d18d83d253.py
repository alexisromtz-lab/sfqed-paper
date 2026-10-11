#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sim/runner_2d3v.py -- ETAPA 1: el campo pico en el foco, por solver de Maxwell.

QUE MIDE
  a_medido(N) = (e/(m_e c omega)) * max_{r en Omega_foco, t} |E(r,t)|
  con N haces COPLANARES en el plano xy, angulos theta_j = 2 pi j / N, todos
  enfocados al origen con la misma cintura w0 y faseados en el foco.
  Amplitud pico por haz: a_b(N) = A_REF / sqrt(N)   (hipotesis de la Proposicion:
  'N haces de igual amplitud E_b' con la energia total repartida).

COMO
  FDTD 2D3V (Yee, las SEIS componentes Ex,Ey,Ez,Bx,By,Bz) en numpy puro, en
  unidades naturales c = omega = k = 1.  EN ESAS UNIDADES LA VARIABLE DE CAMPO
  ES 'a' MISMA (a = eE/(m_e c omega)), asi que la medida se lee directo.

  La condicion inicial NO es un ansatz paraxial: es una superposicion EXACTA de
  ondas planas (espectro angular gaussiano de ancho de cintura w0).  Cada termino
  es solucion exacta de Maxwell en vacio y transversal a SU propio k, luego
  div E = div B = 0 exactamente.  El FDTD solo tiene que no estropearla, y el
  propio runner MIDE cuanto la estropea (comparacion contra la solucion exacta).

POR QUE |E| ES 'a' -- el escalon que hay que MEDIR, no suponer
  En un foco simetrico sum_j k_j = 0, luego B(foco) = (1/c) sum_j k_j x E_j = 0,
  luego F = E^2/2 > 0 y G = 0 en el foco, y
  a = sqrt(sqrt(F^2+G^2)+F) = sqrt(2F) = |E|.
  El runner lo COMPRUEBA imprimiendo |E|, |B|, F, G y a en el instante del pico.
  Una onda plana SOLA tiene |E| != 0 y a = 0: por eso Control 1 no puede ser
  sobre |E|, tiene que ser sobre el invariante.

QUE NO HACE
  No corre PIC.  No simula pares.  No incluye plasma, ni back-reaction, ni
  'el campo visto por la particula' (eso es la etapa 2: sim/schwinger_offline.py).
  No es un pulso: la configuracion es MONOCROMATICA (CW), la envolvente es
  estacionaria y lo que viaja es la portadora; tau entra SOLO por la
  normalizacion de amplitud declarada.

Uso
  python3 -B sim/runner_2d3v.py --modo control1
  python3 -B sim/runner_2d3v.py --modo barrido --todo          (escribe el CSV)
  python3 -B sim/runner_2d3v.py --modo barrido --n 2
  python3 -B sim/runner_2d3v.py --modo barrido --todo --dl 0.5 (el NULO: Control 2)
  python3 -B sim/runner_2d3v.py --modo barrido --todo --pol circular
  python3 -B sim/runner_2d3v.py --modo control4
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
RAIZ = AQUI.parent
sys.path.insert(0, str(AQUI))

import params as P  # noqa: E402

CONFIGS = AQUI / "configs.json"
# PARTICION POR POLARIZACION (ajuste operativo ordenado 11-Oct-2026): --todo
# sobrescribia sim/medidas_aN.csv en CADA corrida y borraba la trazabilidad del
# estado (una corrida circular piso la serie lineal del 10-Oct).  La serie LINEAL
# conserva el nombre canonico porque es EXACTAMENTE la ruta que lee sim/falsador.py;
# la circular escribe un archivo propio.
CSV_NOMBRE = {"linear": "medidas_aN.csv", "circular": "medidas_aN_circular.csv"}
CSV = AQUI / CSV_NOMBRE["linear"]      # ruta canonica = la que lee el falsador

UNIVERSO = (
    "params.py (constantes y derivados; R1: ningun numero de memoria) + malla, "
    "ventana, umbrales e inclinaciones [ELEGIDAS y declaradas abajo]; motor = "
    "numpy float64 (FDTD Yee 2D3V, c=omega=k=1); unidad = celda del reticulo y "
    "escalon temporal; medicion = max de |E| sobre el disco |r| <= w0 y sobre la "
    "ventana CAUSAL de pasos."
)
REGLA_HUELLA = "x == x"

# ------------------- numerica ELEGIDA antes de ver la salida -------------------
N_LISTA = [1, 2, 4, 8, 16]
SIGMA_J = 100.0                 # [ELEGIDO] energia total de entrada (la misma en los 5 N)
DX_SOBRE_LAMBDA = 40            # [DECLARADO en PROTOCOLO_1overN.md seccion 4]
CFL = 0.6                       # [ELEGIDO] limite 2D: dt <= dx/sqrt(2) => CFL <= 0.7071
                                #  (0.9 era INESTABLE: defecto medido en la 1a corrida)
NX = NY = 480                   # [DECLARADO] caja de 12 lambda
N_ESPONJA = 30                  # [ELEGIDO] capa absorbente (celdas)
ABS_MAX = 0.02                  # [ELEGIDO] absorcion por paso en el borde de la capa
RADIO_FOCO_CELDAS = 80          # [ELEGIDO] Omega_foco: |r| <= w0 = 2 lambda = 80 celdas
PASOS_TOTAL = 300               # [ELEGIDO]
PASOS_MEDICION = 260            # [ELEGIDO] ventana CAUSAL: el primer rebote llega ~paso 229
VENTANA_SOSTEN = 60             # [ELEGIDO] ultimos pasos de la ventana (pico sostenido)
N_ANGULAR = 61                  # [ELEGIDO] terminos del espectro angular por haz
DELTA_MAX = 0.75                # [ELEGIDO] corte del espectro angular (rad)

COMP = ("Ex", "Ey", "Ez", "Hx", "Hy", "Hz")   # H = B en vacio (c = 1)

DXn = 2.0 * math.pi / DX_SOBRE_LAMBDA          # paso de malla en unidades de 1/k
DTn = CFL * DXn                                # paso temporal en unidades de 1/omega
PASO_REBOTE = 6.0 * 2.0 * math.pi / DTn        # borde -> foco, en pasos (6 lambda / c)
KAPPA = math.pi * P.W0_OVER_LAMBDA             # k w0 / 2
AREA_3D = math.pi * P.W0 ** 2 / 2.0            # convencion de pico (igual que gen_configs.py)
A_REF = P.a0_de_intensidad(SIGMA_J / (AREA_3D * P.TAU))

_PD = None
_PW = None


def _pesos():
    """[ELEGIDO] pesos del espectro angular: exp(-(k w0/2)^2 sin^2 d) * cos d."""
    global _PD, _PW
    if _PD is None:
        d = np.linspace(-DELTA_MAX, DELTA_MAX, N_ANGULAR)
        w = np.exp(-(KAPPA * np.sin(d)) ** 2) * np.cos(d)
        _PD, _PW = d, w / w.sum()
    return _PD, _PW


def a_b(N, ref=None):
    """Amplitud pico normalizada por haz. [DECLARADO] a_b(N) = A_REF/sqrt(N)."""
    return (A_REF if ref is None else ref) / math.sqrt(N)


def hora():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


# ------------------------------------------------------------- solucion exacta
def bloque(Xc, Yc, th0, am0, pol, fase, comps):
    """Re/Im, en los nodos (Xc,Yc), de las componentes pedidas de UN haz.

    Cada termino del espectro angular es una onda plana exacta de frecuencia
    omega = 1 y |k| = 1, polarizada con SU propio k -> transversal
    -> div E = div B = 0 exacto.
    """
    d, w = _pesos()
    cf, sf = math.cos(fase), math.sin(fase)
    out = {}
    for c in comps:
        out[c] = [np.zeros((NX, NY)), np.zeros((NX, NY))]
    for m in range(N_ANGULAR):
        th = th0 + d[m]
        ct, st = math.cos(th), math.sin(th)
        cX, sX = np.cos(ct * Xc), np.sin(ct * Xc)
        cY, sY = np.cos(st * Yc), np.sin(st * Yc)
        Cp = np.outer(cX, cY) - np.outer(sX, sY)   # cos(khat . r)
        Sp = np.outer(sX, cY) + np.outer(cX, sY)   # sin(khat . r)
        Cq = Cp * cf - Sp * sf                     # cos(khat . r + fase)
        Sq = Sp * cf + Cp * sf                     # sin(khat . r + fase)
        am = am0 * w[m]
        if pol == "linear":
            # pol = zhat ;  B_p = khat x zhat = (sin th, -cos th, 0)
            if "Ez" in comps:
                out["Ez"][0] += am * Cq
                out["Ez"][1] += am * Sq
            if "Hx" in comps:
                out["Hx"][0] += am * st * Cq
                out["Hx"][1] += am * st * Sq
            if "Hy" in comps:
                out["Hy"][0] -= am * ct * Cq
                out["Hy"][1] -= am * ct * Sq
        else:
            # pol = e1hat + i zhat ,  e1hat = (-sin th, cos th, 0)
            if "Ex" in comps:
                out["Ex"][0] -= am * st * Cq
                out["Ex"][1] -= am * st * Sq
            if "Ey" in comps:
                out["Ey"][0] += am * ct * Cq
                out["Ey"][1] += am * ct * Sq
            if "Ez" in comps:
                out["Ez"][0] -= am * Sq
                out["Ez"][1] += am * Cq
            if "Hx" in comps:
                out["Hx"][0] -= am * st * Sq
                out["Hx"][1] += am * st * Cq
            if "Hy" in comps:
                out["Hy"][0] += am * ct * Sq
                out["Hy"][1] -= am * ct * Cq
            if "Hz" in comps:
                out["Hz"][0] += am * Cq
                out["Hz"][1] += am * Sq
    return out


def _malla():
    xg = (np.arange(NX, dtype=float) - NX // 2) * DXn
    yg = (np.arange(NY, dtype=float) - NY // 2) * DXn
    return xg, yg, 0.5 * DXn


# escalonamiento Yee: clave 0=(x,y) 1=(x,y+h) 2=(x+h,y) 3=(x+h,y+h)
STAG = {"Ez": 0, "Ey": 1, "Hx": 1, "Ex": 2, "Hy": 2, "Hz": 3}
COMPS_DE_CLAVE = {0: ("Ez",), 1: ("Ey", "Hx"), 2: ("Ex", "Hy"), 3: ("Hz",)}


def campos(N, pol, dl_lambda=0.0, ref=None):
    """E(r,t) = Re[Ep e^{-i w t}] = R0(r) cos(wt) + R1(r) sin(wt); seis componentes."""
    xg, yg, h = _malla()
    NODOS = {0: (xg, yg), 1: (xg, yg + h), 2: (xg + h, yg), 3: (xg + h, yg + h)}
    F0 = {c: np.zeros((NX, NY)) for c in COMP}
    F1 = {c: np.zeros((NX, NY)) for c in COMP}
    for j in range(N):
        th0 = 2.0 * math.pi * j / N
        fase = -2.0 * math.pi * dl_lambda if (j == N - 1 and dl_lambda != 0.0) else 0.0
        am0 = a_b(N, ref)
        for k, comps in COMPS_DE_CLAVE.items():
            Xc, Yc = NODOS[k]
            b = bloque(Xc, Yc, th0, am0, pol, fase, comps)
            for c in comps:
                F0[c] += b[c][0]
                F1[c] += b[c][1]
    return F0, F1


# --------------------------------------------------------------------------- FDTD
def paso(Ex, Ey, Ez, Hx, Hy, Hz, r1):
    """Un paso Yee 2D3V en vacio (c = 1).  np.roll envuelve: el campo alli vale ~1e-8."""
    Hx -= r1 * (np.roll(Ez, -1, axis=1) - Ez)
    Hy += r1 * (np.roll(Ez, -1, axis=0) - Ez)
    Hz -= r1 * ((np.roll(Ey, -1, axis=0) - Ey) - (np.roll(Ex, -1, axis=1) - Ex))
    Ex += r1 * (Hz - np.roll(Hz, 1, axis=1))
    Ey -= r1 * (Hz - np.roll(Hz, 1, axis=0))
    Ez += r1 * ((Hy - np.roll(Hy, 1, axis=0)) - (Hx - np.roll(Hx, 1, axis=1)))


def _esponja():
    f = np.ones(NX)
    for i in range(N_ESPONJA):
        v = 1.0 - ABS_MAX * (1.0 - i / N_ESPONJA) ** 2
        f[i] = v
        f[NX - 1 - i] = v
    return f[:, None] * f[None, :]


ESPO = _esponja()
XG, YG, _H = _malla()
_Xm, _Ym = np.meshgrid(XG, YG, indexing="ij")
MASK_FOCO = np.asarray((_Xm ** 2 + _Ym ** 2) <= (RADIO_FOCO_CELDAS * DXn) ** 2)
_INT0 = N_ESPONJA + 20
MASK_INT = np.zeros((NX, NY), dtype=bool)
MASK_INT[_INT0:NX - _INT0, _INT0:NY - _INT0] = True


def invariantes(Ex, Ey, Ez, Bx, By, Bz):
    """F = (E^2-B^2)/2 ; G = E.B ; a = sqrt(sqrt(F^2+G^2)+F)  (punto a punto)."""
    E2 = Ex * Ex + Ey * Ey + Ez * Ez
    B2 = Bx * Bx + By * By + Bz * Bz
    F = 0.5 * (E2 - B2)
    G = Ex * Bx + Ey * By + Ez * Bz
    a = np.sqrt(np.maximum(np.sqrt(F * F + G * G) + F, 0.0))
    return E2, B2, F, G, a


def correr(N, pol, dl_lambda, pasos, verbose=True, ref=None):
    F0, F1 = campos(N, pol, dl_lambda, ref)
    Ex, Ey, Ez = F0["Ex"].copy(), F0["Ey"].copy(), F0["Ez"].copy()
    # leapfrog: E en t = n*dt, H en t = (n+1/2)*dt  =>  H se inicializa en el SEMI-PASO
    _ch, _sh = math.cos(0.5 * DTn), math.sin(0.5 * DTn)
    Hx = F0["Hx"] * _ch + F1["Hx"] * _sh
    Hy = F0["Hy"] * _ch + F1["Hy"] * _sh
    Hz = F0["Hz"] * _ch + F1["Hz"] * _sh
    r1 = DTn / DXn
    mmax, paso_max = -1.0, -1
    m_sost = -1.0
    # MEDICION PUNTUAL EN EL CENTRO (ajuste operativo ordenado 11-Oct-2026):
    # r = (0,0) = celda (NX//2, NY//2), donde Ez vive EXACTAMENTE en el nodo.
    # Es ADITIVA: no sustituye al sup sobre el disco, lo acompaña.
    centro_max, centro_en_pico = -1.0, float("nan")
    errores = []
    umbral_sost = max(0, min(pasos, PASOS_MEDICION) - VENTANA_SOSTEN)
    # DENOMINADOR DECLARADO del error: una ESCALA, no el max instantaneo.
    # En t = (m + 1/2) T la portadora vale 0 y el max instantaneo se anula:
    # el cociente explota sobre un residuo de 1e-14 sin que el objeto crezca.
    DEN_E = {c: float(np.abs(F0[c]).max() + np.abs(F1[c]).max()) for c in COMP[:3]}
    e_ini = float(np.sum(Ex ** 2 + Ey ** 2 + Ez ** 2) + np.sum(Hx ** 2 + Hy ** 2 + Hz ** 2))
    for n in range(pasos + 1):
        if n > 0:
            paso(Ex, Ey, Ez, Hx, Hy, Hz, r1)
            Ex *= ESPO
            Ey *= ESPO
            Ez *= ESPO
            Hx *= ESPO
            Hy *= ESPO
            Hz *= ESPO
        if n <= PASOS_MEDICION:
            Em = np.sqrt(Ex * Ex + Ey * Ey + Ez * Ez)
            m = float(Em[MASK_FOCO].max())
            c0 = float(Em[NX // 2, NY // 2])
            centro_max = max(centro_max, c0)
            if m > mmax:
                mmax, paso_max = m, n
                centro_en_pico = c0
            if n >= umbral_sost:
                m_sost = max(m_sost, m)
        if verbose and (n % 25 == 0 or n == pasos):
            t = n * DTn
            c, s = math.cos(t), math.sin(t)
            err = 0.0
            err_f = 0.0
            idx = None
            for comp, arr in (("Ex", Ex), ("Ey", Ey), ("Ez", Ez)):
                ex = F0[comp] * c + F1[comp] * s
                den = max(1e-30, DEN_E[comp])
                d = np.where(MASK_INT, np.abs(arr - ex), 0.0)
                e = float(d.max()) / den
                err_f = max(err_f, float(np.where(MASK_FOCO, np.abs(arr - ex), 0.0).max()) / den)
                if e > err:
                    err = e
                    idx = (comp,) + tuple(int(v) for v in np.unravel_index(np.argmax(d), d.shape))
            errores.append((n, err))
            if idx is not None:
                print(f"    err interior p{n:<3d} = {err:.3e}   en {idx[0]}[{idx[1]},{idx[2]}]"
                      f"   | err DENTRO del foco = {err_f:.3e}"
                      f"   (capa absorbente = {N_ESPONJA} celdas)", flush=True)
    e_fin = float(np.sum(Ex ** 2 + Ey ** 2 + Ez ** 2) + np.sum(Hx ** 2 + Hy ** 2 + Hz ** 2))

    res = dict(N=N, pol=pol, dl=dl_lambda, a_b=a_b(N, ref), a_pred=N * a_b(N, ref),
               a_fdtd=mmax, a_sost=m_sost, paso_pico=paso_max,
               a_centro=centro_max, a_centro_pico=centro_en_pico,
               a_exacto=None, foco=None, errores=errores,
               e_ini=e_ini, e_fin=e_fin, e_rel=abs(e_fin / e_ini - 1.0))

    # en el instante del pico: |E|, |B|, F, G, a (desde la solucion EXACTA)
    if paso_max >= 0:
        t = paso_max * DTn
        c, s = math.cos(t), math.sin(t)
        ex = F0["Ex"] * c + F1["Ex"] * s
        ey = F0["Ey"] * c + F1["Ey"] * s
        ez = F0["Ez"] * c + F1["Ez"] * s
        bx = F0["Hx"] * c + F1["Hx"] * s
        by = F0["Hy"] * c + F1["Hy"] * s
        bz = F0["Hz"] * c + F1["Hz"] * s
        E2, B2, F, G, a = invariantes(ex, ey, ez, bx, by, bz)
        Emod = np.sqrt(E2)
        Emod_f = np.where(MASK_FOCO, Emod, -1.0)
        idx = np.unravel_index(int(np.argmax(Emod_f)), Emod_f.shape)
        res["a_exacto"] = float(Emod_f.max())
        res["foco"] = dict(Emod=float(Emod[idx]),
                           Bmod=float(math.sqrt(max(B2[idx], 0.0))),
                           F=float(F[idx]), G=float(G[idx]), a_inv=float(a[idx]),
                           x=float(XG[idx[0]]), y=float(YG[idx[1]]))
    return res


# ------------------------------------------------------------------- controles
def control1():
    """Lemma 1: una onda plana SOLA -> F = G = 0 -> a = 0, con |E| != 0."""
    xg, yg, _ = _malla()
    th = 0.3
    ct, st = math.cos(th), math.sin(th)
    ph = ct * xg[:, None] + st * yg[None, :]
    am = 10.0
    Ez = am * np.cos(ph)
    Bx = am * st * np.cos(ph)
    By = -am * ct * np.cos(ph)
    z = np.zeros_like(Ez)
    E2, B2, F, G, a = invariantes(z, z, Ez, Bx, By, z)
    return dict(Emod=float(np.abs(Ez).max()),
                Bmod=float(math.sqrt(float((Bx ** 2 + By ** 2).max()))),
                maxF=float(np.abs(F).max()), maxG=float(np.abs(G).max()),
                maxa=float(a.max()))


def control4(N=1):
    """Conservacion de energia y ley de escala: U = int (E^2+B^2)/2 debe ir como a_b^2."""
    ref = A_REF
    us = []
    for esc in (0.5, 1.0, 2.0):
        r = correr(N, "linear", 0.0, 40, verbose=False, ref=ref * esc)
        us.append((esc, r["e_ini"], r["e_rel"]))
    base = us[1][1]
    ley = [round(u / (base * e * e), 6) for e, u, _ in us]
    return dict(escala=us, ley_U_sobre_U1_e2=ley)


# ------------------------------------------------------------------- salida
def pre_registro(pol, dl, pasos):
    print("=" * 78)
    print("PRE-REGISTRO  (declarado ANTES de medir)")
    print("=" * 78)
    print(f"UNIVERSO DECLARADO: {UNIVERSO}")
    print(f"REGLA DE HUELLA = {REGLA_HUELLA}")
    print(f"hora = {hora()}")
    print("a_medido(N) = (e/(m_e c omega)) * max_(r en Omega_foco, t) |E(r,t)|")
    print(f"Omega_foco = disco |r| <= w0 = {RADIO_FOCO_CELDAS} celdas = "
          f"{RADIO_FOCO_CELDAS * DXn:.6f} (1/k)  = 2 lambda")
    print(f"polarizacion = {pol}   ;  desajuste de camino = {dl} lambda en UN haz")
    print("PREDICCION (eq:oneoverN):  a_tot(N) = N a_b(N) = sqrt(N) A_REF")
    print(f"  A_REF = a0_de_intensidad(SIGMA/((pi w0^2/2) tau)) = {A_REF:.10f}")
    for N in N_LISTA:
        print(f"    N = {N:2d}   a_b = {a_b(N):14.8f}   a_pred = {N * a_b(N):14.8f}")
    print("BANDA del falsador: VERDE [0.45,0.55] ; GRIS 0.35-0.45 y 0.55-0.65 ; "
          "MUERTE <=0.35 o >=0.65 ; tolerancia por N = 0.20")
    print(f"malla {NX}x{NY} ; dx = lambda/{DX_SOBRE_LAMBDA} ; dxn = {DXn:.9f} (1/k) ; "
          f"dtn = {DTn:.9f} (1/omega) ; CFL = {CFL}")
    print(f"ventana CAUSAL: el primer rebote del borde llega al foco en el paso "
          f"{PASO_REBOTE:.1f} -> se mide hasta el paso {PASOS_MEDICION} de {pasos}")
    print("DECLARADO: NO es un pulso; la configuracion es MONOCROMATICA (CW). tau entra")
    print("           solo por la normalizacion de amplitud. Lo que viaja es la portadora.")
    print("=" * 78)


def fila(r):
    f = r["foco"]
    return (f"N={r['N']:2d} {r['pol']:8s} a_b={r['a_b']:12.7f} a_pred={r['a_pred']:12.7f} "
            f"a_fdtd={r['a_fdtd']:12.7f} ratio={r['a_fdtd'] / r['a_pred']:9.5f} "
            f"sost={r['a_sost']:12.7f} paso={r['paso_pico']:3d} "
            f"centro={r['a_centro']:12.7f} cent_pico={r['a_centro_pico']:12.7f} "
            f"|E|={f['Emod']:12.7f} "
            f"|B|={f['Bmod']:11.3e} F={f['F']:12.5f} G={f['G']:11.3e} a_inv={f['a_inv']:12.7f}")


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--modo", default="barrido", choices=["barrido", "control1", "control4"])
    ap.add_argument("--n", type=int, default=None)
    ap.add_argument("--todo", action="store_true")
    ap.add_argument("--pol", default="linear", choices=["linear", "circular"])
    ap.add_argument("--dl", type=float, default=0.0)
    ap.add_argument("--pasos", type=int, default=PASOS_TOTAL)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if a.modo == "control1":
        c = control1()
        print(f"CONTROL 1 (Lemma 1: una onda plana sola)   hora = {hora()}")
        print(f"  UNIVERSO DECLARADO: {UNIVERSO}")
        print(f"  |E| = {c['Emod']:.6f}   |B| = {c['Bmod']:.6f}   (iguales: onda plana)")
        print(f"  max|F| = {c['maxF']:.3e}   max|G| = {c['maxG']:.3e}   max a = {c['maxa']:.3e}")
        # CORRECCION DECLARADA DEL PISO (no ajuste al numero):
        # el pre-registro estimo 'a < eps*|E|' -- UNIDAD MAL PUESTA: a = sqrt(2F) para G=0,
        # luego el piso de 'a' es la RAIZ del piso de F.  Para una onda plana,
        # F = 0.5*(E^2-B^2) con E^2 ~ B^2 ~ am^2 => cancelacion catastrofica: el error de F
        # es unas pocas ulps de |E|^2.  Piso ANALITICO declarado con holgura (4x el caso
        # medido leido como ~4 eps*|E|^2): |F|,|G| <= 16*eps*|E|^2  y  a <= sqrt(32*eps)*|E|.
        eps_m = np.finfo(float).eps
        piso_F = 16.0 * eps_m * c["Emod"] ** 2
        piso_a = math.sqrt(2.0 * piso_F)
        ok = (c["maxF"] < piso_F) and (c["maxG"] < piso_F) and (c["maxa"] < piso_a)
        print(f"  PISO DECLARADO (por cancelacion, 16 ulps): |F|,|G| < {piso_F:.3e} ; "
              f"a < {piso_a:.3e}")
        print(f"  margen medido/piso: F {c['maxF'] / piso_F:.4f} ; a {c['maxa'] / piso_a:.4f}")
        print(f"  VEREDICTO: {'VERDE' if ok else 'ROJO'} (a = 0 aunque |E| != 0)")
        return 0 if ok else 1

    if a.modo == "control4":
        c = control4()
        print(f"CONTROL 4 (energia y ley de escala)   hora = {hora()}")
        for e, u, er in c["escala"]:
            print(f"  a_b x {e:4.2f}   U = {u:.10e}   |dU/U| propagado = {er:.2e}")
        print(f"  U / (U_1 * e^2) = {c['ley_U_sobre_U1_e2']}  (debe ser ~1: U va como a_b^2)")
        return 0

    pre_registro(a.pol, a.dl, a.pasos)
    lista = N_LISTA if a.todo else ([a.n] if a.n else [1])
    rs = []
    for N in lista:
        r = correr(N, a.pol, a.dl, a.pasos)
        rs.append(r)
        print(fila(r))

    print("-" * 78)
    print("error relativo maximo FDTD vs solucion EXACTA (Ex,Ey,Ez, sobre la caja):")
    for r in rs:
        print(f"  N={r['N']:2d}  " + "  ".join(f"p{n}: {e:.2e}" for n, e in r["errores"]))
    print("energia |U_fin/U_ini - 1|: " + "  ".join(
        f"N={r['N']:2d}: {r['e_rel']:.2e}" for r in rs))

    if a.todo and a.dl == 0.0:
        cab = ("# a_medido = (e/(m_e c omega)) * max_(r en Omega_foco, t) |E(r,t)|\n"
               "# medido con sim/runner_2d3v.py (FDTD Yee 2D3V, numpy, c = omega = k = 1)\n"
               f"# UNIVERSO DECLARADO: {UNIVERSO}\n"
               f"# pol = {a.pol} ; Omega_foco = |r| <= w0 ; N_LISTA = {N_LISTA} ; "
               f"hora = {hora()}\n")
        cuerpo = "".join(f"{r['N']},{r['a_fdtd']:.10f}\n" for r in rs)
        csv_pol = AQUI / CSV_NOMBRE[a.pol]
        csv_pol.write_text(cab + cuerpo, encoding="utf-8")
        hh = hashlib.sha256(csv_pol.read_bytes()).hexdigest()[:16]
        print(f"CSV escrito: {csv_pol}  sha16={hh}  {csv_pol.stat().st_size} B  "
              f"{len(rs)} filas")
        if csv_pol != CSV:
            print(f"  (la ruta canonica {CSV} NO se toco: es la serie LINEAL del falsador)")
    elif a.todo:
        print(f"CSV NO escrito: hay desajuste declarado (--dl {a.dl}); esta corrida es el NULO")

    if a.json:
        print(json.dumps(rs, indent=2, default=float))
    return 0


if __name__ == "__main__":
    sys.exit(main())
