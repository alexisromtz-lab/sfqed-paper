#!/usr/bin/env python3
"""sim/maxwell2d.py -- ETAPA 1: propagador clasico de Maxwell en malla 2D (Yee, 2D3V).

UNIVERSO DECLARADO (se imprime antes de toda cifra):
  malla xy de 480x480 celdas = 12 lambda_L por lado; dx = lambda_L/40;
  transito 19.485 lambda_L (el pre-registrado 866 pasos a CFL 0.90) =
  1113 pasos a CFL_2D = 0.70; diagnostico cada 20 pasos (PROTOCOLO_1overN.md §4);
  CFL_2D = 0.70 [CORREGIDO] -- el 0.90 pre-registrado viola la condicion de
  von Neumann en 2D (limite 1/sqrt(2) = 0.7071); la divergencia a 0.90 se MIDE
  en --control-cfl, no se supone;
  VENTANA DE MEDIDA: celdas i en [100, 380] (0.5 lambda de halo respecto de los
  planos fuente 80/400 y del absorbedor 0-60/420-480). El maximo de caja se
  imprime ADEMAS como artefacto declarado: sobre la linea de inyeccion
  cB/|E| = 0.514 (no es onda: es el campo de la propia fuente) y |E| vale 6.9x
  (blanda) o 21x (dura) la amplitud inyectada (medido 00:28:47Z);
  vacio clasico, sin plasma y sin tasa de Schwinger dentro del solver (la
  Schwinger se integra DESPUES, §6 del protocolo);
  SI 2019 (CODATA 2018) via sim/params.py; motor numpy; unidad de conteo = celda.

QUE MIDE
  a_medido(N) = e * max_{(x,y),t} |E| / (m_e omega c)      [adimensional]
  la MISMA unidad que a_ref_N_1 = 170.534. La suma de los N haces la hace la
  ecuacion de actualizacion (lineal); el instrumento no suma a mano.
  Ademas el invariante de eq:ab: a_inv = sqrt(sqrt(F^2+G^2)+F) con
  F = eps0/2 (E^2 - c^2 B^2) y G = eps0 c E.B, devuelto en unidades de campo.

MODOS
  colineal        N haces co-propagantes desde el plano fuente, en coincidencia
                  de fase == el objeto PRE-REGISTRADO en el protocolo §1.
  colineal-nulo   idem con fase pi entre haces sucesivos (DeltaL = lambda/2):
                  control §5.2 (el escalado DEBE romperse).
  contra          N/2 pares contra-propagantes (configuracion eq:cp_inv del
                  paper: campo NO nulo, B = 0 en el foco); brazos = 4 lambda.
  contra-nulo     el brazo derecho desplazado lambda/2.

Uso:
  python3 -B sim/maxwell2d.py --modo colineal --n 4
  python3 -B sim/maxwell2d.py --serie           # escribe sim/medidas_aN.csv
  python3 -B sim/maxwell2d.py --serie-contra
  python3 -B sim/maxwell2d.py --control-energia
  python3 -B sim/maxwell2d.py --control-cfl
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
if str(AQUI) not in sys.path:
    sys.path.insert(0, str(AQUI))
import params as P  # noqa: E402  (las constantes tienen UNA casa)

CFG = json.loads((AQUI / "configs.json").read_text(encoding="utf-8"))
A_REF = float(CFG["a_ref_N_1"])          # 170.534, del modelo, no de aqui
N_LISTA = [int(n) for n in CFG["N_LISTA"]]

# --- numerica declarada (PROTOCOLO_1overN.md §4) ---
DX_OVER_LAMBDA = 1.0 / 40.0
CFL_PRE = 0.9                 # el del protocolo (inestable en 2D: se mide)
CFL_2D = 0.70                 # [CORREGIDO] por debajo de 1/sqrt(2) = 0.7071
CAJA_LAMBDA = 12.0
NPASOS = 866                  # a CFL_PRE: el protocolo fija el TIEMPO, no el paso
DIAG_CADA = 20
# El contenido fisico de "866 pasos" es el TRANSITO: 866 * 0.90 * dx = 19.485
# lambda_L, o sea el tiempo justo para que el pulso (fuente en -4 lambda,
# frontera absorbiendo en +6 lambda, duracion 7.5 lambda) despeje la caja.
# A CFL_2D = 0.70 los MISMOS 866 pasos dan solo 15.2 lambda y el absorbedor
# todavia guarda 2.4e-01 del pico (residuo medido 00:32:29Z). Se conserva el
# transito y se derivan los pasos: 1113 a 0.70.
TRANSITO_LAMBDA = NPASOS * CFL_PRE * DX_OVER_LAMBDA
NX = int(round(CAJA_LAMBDA / DX_OVER_LAMBDA))
NY = NX
DX = P.LAMBDA_L * DX_OVER_LAMBDA
MU0 = 1.0 / (P.EPS0 * P.C * P.C)
IC = NX // 2
JC = NY // 2

# --- geometria e instrumento ELEGIDOS (el protocolo no los fija) ---
BRAZO_LAMBDA = 4.0            # [ELEGIDO] plano fuente -> foco (= 8 x lambda/2)
D_CELDAS = int(round(BRAZO_LAMBDA / DX_OVER_LAMBDA))
I_SL = IC - D_CELDAS          # 80  (plano fuente izquierdo)
I_SR = IC + D_CELDAS          # 400 (plano fuente derecho)
BRAZO_M = BRAZO_LAMBDA * P.LAMBDA_L
ESPONJA_CELDAS = 60           # [ELEGIDO] grosor de la capa absorbente
ALFA_ESPONJA = 0.10           # [ELEGIDO] amortiguamiento pico por paso
CONVERGE = True               # [ELEGIDO] frente de onda convergente al foco

# --- VENTANA DE MEDIDA (declarada; ver UNIVERSO) ---
# La linea de inyeccion NO es un objeto de Maxwell: en la celda fuente el campo
# se SUMA/FIJA a mano cada paso y queda una discontinuidad no-Maxwelliana. Medido
# en la sonda del eje (00:28:47Z): cB/|E| = 0.514 en la linea vs 1.001 en el haz,
# y |E| en la linea = 6.9x (blanda) / 21x (dura) la amplitud prescrita. Por eso
# el objeto medido es el campo RADIADO, y la fuente se excluye con un halo.
MARGEN_FUENTE_CELDAS = 20     # [ELEGIDO] halo excluido alrededor de cada plano fuente
VENTANA_I0 = I_SL + MARGEN_FUENTE_CELDAS     # 100
VENTANA_I1 = I_SR - MARGEN_FUENTE_CELDAS     # 380

UNIVERSO = (
    f"malla xy {NX}x{NY} = {CAJA_LAMBDA:g} lambda_L por lado, dx = lambda_L/40; "
    f"transito fisico = {TRANSITO_LAMBDA:.3f} lambda_L (los {NPASOS} pasos "
    f"pre-registrados a CFL {CFL_PRE}) = "
    f"{int(round(TRANSITO_LAMBDA / (CFL_2D * DX_OVER_LAMBDA)))} pasos a CFL "
    f"{CFL_2D}; diagnostico cada {DIAG_CADA} pasos (PROTOCOLO_1overN.md §4); "
    f"CFL de 2D = {CFL_2D} [CORREGIDO del {CFL_PRE} pre-registrado: limite de von "
    f"Neumann en 2D = 1/sqrt(2) = {1/math.sqrt(2):.4f}]; vacio clasico, SI 2019 "
    "(CODATA 2018) via sim/params.py; motor numpy; unidad de conteo = celda; "
    f"VENTANA DE MEDIDA = celdas [{VENTANA_I0},{VENTANA_I1}] (excluye la linea de "
    "inyeccion, que no es objeto de Maxwell: ahi cB/|E| = 0.514 y |E| = 6.9x lo "
    "prescrito, medido)"
)

COMPONENTES = ("Ex", "Ey", "Ez", "Hx", "Hy", "Hz")


# ---------------------------------------------------------------- derivadas
def ddx(F):
    g = np.zeros_like(F)
    g[1:, :] = (F[1:, :] - F[:-1, :]) / DX
    return g


def ddy(F):
    g = np.zeros_like(F)
    g[:, 1:] = (F[:, 1:] - F[:, :-1]) / DX
    return g


def ddx_f(F):
    g = np.zeros_like(F)
    g[:-1, :] = (F[1:, :] - F[:-1, :]) / DX
    return g


def ddy_f(F):
    g = np.zeros_like(F)
    g[:, :-1] = (F[:, 1:] - F[:, :-1]) / DX
    return g


def campos_vacios():
    z = lambda: np.zeros((NX, NY), dtype=np.float64)
    return {"Ex": z(), "Ey": z(), "Ez": z(), "Hx": z(), "Hy": z(), "Hz": z()}


def mascara_esponja():
    m = np.ones((NX, NY))
    for eje, n in ((0, NX), (1, NY)):
        idx = np.arange(n)
        borde = np.maximum(
            np.clip(ESPONJA_CELDAS - idx, 0, ESPONJA_CELDAS),
            np.clip(idx - (n - 1 - ESPONJA_CELDAS), 0, ESPONJA_CELDAS),
        ) / ESPONJA_CELDAS
        s = 1.0 - ALFA_ESPONJA * borde ** 2
        m *= s.reshape((-1, 1) if eje == 0 else (1, -1))
    return m


def paso(F, dt, mascara):
    """Un paso de Yee: H en t+dt/2 y E en t+dt."""
    ce = dt / P.EPS0
    ch = dt / MU0
    Ex, Ey, Ez, Hx, Hy, Hz = (F[k] for k in COMPONENTES)
    F["Hx"] = Hx - ch * ddy_f(Ez)
    F["Hy"] = Hy + ch * ddx_f(Ez)
    F["Hz"] = Hz - ch * (ddx_f(Ey) - ddy_f(Ex))
    F["Ex"] = Ex + ce * ddy(F["Hz"])
    F["Ey"] = Ey - ce * ddx(F["Hz"])
    F["Ez"] = Ez + ce * (ddx(F["Hy"]) - ddy(F["Hx"]))
    if mascara is not None:
        for k in COMPONENTES:
            F[k] *= mascara


def energia(F):
    """Densidad integrada U = suma (eps0 E^2/2 + B^2/2mu0) dx^2  [J/m por z]."""
    e2 = F["Ex"] ** 2 + F["Ey"] ** 2 + F["Ez"] ** 2
    b2 = MU0 ** 2 * (F["Hx"] ** 2 + F["Hy"] ** 2 + F["Hz"] ** 2)
    return float(np.sum(0.5 * (P.EPS0 * e2 + b2 / MU0)) * DX * DX)


# ---------------------------------------------------------------- fuentes
def envolvente(t):
    """Pulso compacto sin^2 (declarado): 0 fuera de [0, tau]."""
    if t < 0.0 or t > P.TAU:
        return 0.0
    return math.sin(math.pi * t / P.TAU) ** 2


def perfiles():
    """Perfil transversal g(rho) y las DOS curvaturas de frente (una por sentido).

    Una fuente en el plano x0 que radia hacia +x necesita fase +k rho^2/(2R)
    para que todas las contribuciones lleguen EN FASE al foco a distancia R
    (el radio rho recorre un camino mayor en rho^2/(2R) y hay que adelantarlo).
    La fuente que radia hacia -x lleva el signo opuesto. Con el signo cambiado
    el frente DIVERGE: medido en el humo 00:31:30Z, |E| caia de 44.4 (a 0.5
    lambda de la fuente) a 33.8 en el foco.
    """
    j = np.arange(NY)
    g = np.exp(-(((j - JC) * DX) / P.W0) ** 2)
    rho2 = ((j - JC) * DX) ** 2
    if not CONVERGE:
        z = np.zeros(NY)
        return g, {I_SL: z, I_SR: z}
    fase_izq = +P.OMEGA * rho2 / (2.0 * BRAZO_M)   # radia hacia +x (foco a la derecha)
    fase_der = -P.OMEGA * rho2 / (2.0 * BRAZO_M)   # radia hacia -x
    return g, {I_SL: fase_izq, I_SR: fase_der}


def inyectar(F, t, terminos, g, fases, duro=False):
    """Suma los terminos fuente (haces) sobre E. La suma es lineal: es la ec. de Maxwell.

    duro=False (fuente blanda): se SUMA a lo que ya hay -> el campo en la linea
      acumula el campo casi-estatico de la propia fuente (artefacto del
      instrumento, medido: factor 6.9 sobre la amplitud inyectada).
    duro=True  (fuente dura): se FIJA el campo en la linea -> sin acumulacion.
    fases: dict columna -> perfil de fase (curvatura del frente, con su sentido).
    """
    env = envolvente(t)
    if env == 0.0:
        return
    acum = {}
    for col, amp, desfase in terminos:
        th = P.OMEGA * t + fases[col] + desfase
        sy = amp * env * g * np.cos(th)
        sz = -amp * env * g * np.sin(th)
        if col in acum:
            a, b = acum[col]
            acum[col] = (a + sy, b + sz)
        else:
            acum[col] = (sy, sz)
    for col, (sy, sz) in acum.items():
        if duro:
            F["Ey"][col, :] = sy
            F["Ez"][col, :] = sz
        else:
            F["Ey"][col, :] += sy
            F["Ez"][col, :] += sz


def terminos_de(modo, n, nulo=False):
    """Reparte la energia total en N haces: a_beam = a_ref / sqrt(N) (modelo).

    colineal  -> N terminos en el plano fuente izquierdo.
    contra    -> N/2 en el izquierdo y N/2 en el derecho (pares enfrentados).
    """
    a_beam = A_REF / math.sqrt(n)
    e_beam = P.campo_de_a0(a_beam)          # V/m por haz
    if modo.startswith("colineal"):
        dphi = math.pi if nulo else 0.0
        return [(I_SL, e_beam, dphi * k) for k in range(n)], {}
    if n % 2:
        raise ValueError("el modo contra necesita N par (pares enfrentados)")
    dphi = math.pi if nulo else 0.0
    medio = n // 2
    izq = [(I_SL, e_beam, dphi * k) for k in range(medio)]
    der = [(I_SR, e_beam, dphi * k) for k in range(medio)]
    return izq + der, {}


def invariante_a(F):
    """a de eq:ab en unidades de campo (V/m)."""
    Ex, Ey, Ez, Hx, Hy, Hz = (F[k] for k in COMPONENTES)
    Bx, By, Bz = MU0 * Hx, MU0 * Hy, MU0 * Hz
    e2 = Ex ** 2 + Ey ** 2 + Ez ** 2
    b2 = Bx ** 2 + By ** 2 + Bz ** 2
    Fs = 0.5 * (P.EPS0 * e2 - b2 / MU0)
    Gs = (Ex * Bx + Ey * By + Ez * Bz) / (P.C * MU0)
    raiz = np.sqrt(Fs * Fs + Gs * Gs)
    return np.sqrt(np.maximum(raiz + Fs, 0.0)) / math.sqrt(P.EPS0)


def modulo_E(F):
    return np.sqrt(F["Ex"] ** 2 + F["Ey"] ** 2 + F["Ez"] ** 2)


# ---------------------------------------------------------------- corrida
def correr(modo="colineal", n=1, cfl=None, absorbe=True, nulo=False,
           pasos=None, desplaza_dcha=0, verbose=False, duro=False, sonda=False):
    cfl = CFL_2D if cfl is None else cfl
    pasos = int(round(TRANSITO_LAMBDA / (cfl * DX_OVER_LAMBDA))) if pasos is None else pasos
    dt = cfl * DX / P.C
    F = campos_vacios()
    masc = mascara_esponja() if absorbe else None
    g, fases = perfiles()
    terminos, _ = terminos_de(modo, n, nulo=nulo)
    if desplaza_dcha:
        terminos = [(c + (desplaza_dcha if c > IC else 0), a, d)
                    for c, a, d in terminos]
        fases = {c + (desplaza_dcha if c > IC else 0): v
                 for c, v in fases.items()}

    emax = 0.0
    emax_caja = 0.0
    tmax = 0.0
    imax = jmax = -1
    rel = {}
    a_inv_max = 0.0
    a_inv_rel_max = 0.0
    efoco_max = 0.0
    efoco_t = 0.0
    cola = []
    sonda_ax = None
    for k in range(pasos):
        t = (k + 0.5) * dt
        inyectar(F, t, terminos, g, fases, duro=duro)
        paso(F, dt, masc)
        e = modulo_E(F)
        em_caja = float(e.max())
        if em_caja > emax_caja:
            emax_caja = em_caja
        e_ven = e[VENTANA_I0:VENTANA_I1 + 1, :]
        em = float(e_ven.max())
        idx = int(np.argmax(e_ven))
        if em > emax:
            emax = em
            tmax = (k + 1) * dt
            imax, jmax = divmod(idx, NY)
            imax += VENTANA_I0
            e2p = float((F["Ex"] ** 2 + F["Ey"] ** 2 + F["Ez"] ** 2)[imax, jmax])
            b2p = MU0 ** 2 * float((F["Hx"] ** 2 + F["Hy"] ** 2 + F["Hz"] ** 2)[imax, jmax])
            rel = {"F": 0.5 * (P.EPS0 * e2p - b2p / MU0),
                   "Emax_punto": em,
                   "cB_sobre_E": (P.C * math.sqrt(b2p) / math.sqrt(e2p)) if e2p > 0 else 0.0}
        ef = float(e[IC, JC])
        if ef > efoco_max:
            efoco_max = ef
            efoco_t = (k + 1) * dt
            if sonda:
                bmag = MU0 * np.sqrt(F["Hx"] ** 2 + F["Hy"] ** 2 + F["Hz"] ** 2)
                sonda_ax = {"eje": e[:, JC].copy(), "eje_cB": (P.C * bmag)[:, JC].copy()}
        cola.append(em)
        if len(cola) > 100:
            cola.pop(0)
        if k % DIAG_CADA == 0:
            ai = invariante_a(F)
            aim = float(ai[VENTANA_I0:VENTANA_I1 + 1, :].max())
            a_inv_max = max(a_inv_max, aim)
            if em > 0.0:
                a_inv_rel_max = max(a_inv_rel_max, aim / em)
        if verbose and k % (DIAG_CADA * 4) == 0:
            print(f"    paso {k:4d}  t = {t*1e15:6.2f} fs  max|E| = {em:.6g} V/m")
    a_max = P.a0_de_campo(emax)
    a_foco = P.a0_de_campo(efoco_max)
    muestras = []
    if sonda_ax is not None:
        for i in (I_SL, I_SL + 20, I_SL + 40, IC - 80, IC - 40, IC, IC + 40,
                  IC + 80, I_SR):
            ee = float(sonda_ax["eje"][i])
            cb = float(sonda_ax["eje_cB"][i])
            muestras.append({
                "i": i, "x_lambda_del_foco": (i - IC) * DX_OVER_LAMBDA,
                "E_V_m": ee, "a0_equivalente": P.a0_de_campo(ee),
                "cB_sobre_E": (cb / ee) if ee > 0 else 0.0,
            })
    return {
        "modo": modo, "N": n, "nulo": bool(nulo), "cfl": cfl, "dt_s": dt,
        "pasos": pasos, "absorbe": bool(absorbe),
        "desplaza_dcha_celdas": int(desplaza_dcha),
        "E_max_V_m": emax, "a_medido": a_max,
        "E_max_caja_V_m": emax_caja, "a_medido_caja": P.a0_de_campo(emax_caja),
        "ventana_celdas": [VENTANA_I0, VENTANA_I1],
        "cB_sobre_E_en_el_pico": rel.get("cB_sobre_E", 0.0),
        "t_max_fs": tmax * 1e15,
        "pico_i": imax, "pico_j": jmax,
        "pico_lambda_de_borde": imax * DX_OVER_LAMBDA,
        "pico_lambda_del_foco": (imax - IC) * DX_OVER_LAMBDA,
        "E_foco_V_m": efoco_max, "a_foco": a_foco, "t_foco_fs": efoco_t * 1e15,
        "b_foco_rel": efoco_max / emax,
        "a_inv_max_V_m": a_inv_max,
        "a_inv_rel_al_pico": a_inv_rel_max,
        "F_rel_pico": rel.get("F", 0.0) / max(0.5 * P.EPS0 * rel.get("Emax_punto", 1.0) ** 2, 1e-300),
        "cola_max_V_m": max(cola) if cola else 0.0,
        "cola_rel": (max(cola) / emax) if cola and emax else 0.0,
        "duro": bool(duro),
        "sonda_eje": muestras,
    }


def bloque(r, extra=None):
    b = {
        "T_UTC": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "UNIVERSO DECLARADO": UNIVERSO,
        "a_ref_N_1": A_REF,
        "geometria": {
            "BRAZO_LAMBDA": BRAZO_LAMBDA, "D_CELDAS": D_CELDAS,
            "I_SL": I_SL, "I_SR": I_SR, "foco_ij": [IC, JC],
            "w0_over_lambda": P.W0_OVER_LAMBDA, "convergente": CONVERGE,
            "esponja_celdas": ESPONJA_CELDAS, "alfa_esponja": ALFA_ESPONJA,
            "tau_s": P.TAU,
        },
        "corrida": r,
    }
    if extra:
        b.update(extra)
    return b


def imprimir(b):
    r = b["corrida"]
    print(f"UNIVERSO DECLARADO: {b['UNIVERSO DECLARADO']}")
    print(f"hora = {b['T_UTC']}")
    print(f"modo = {r['modo']}  N = {r['N']}  nulo = {r['nulo']}  cfl = {r['cfl']}")
    print(f"  a_medido (max de |E| EN LA VENTANA, sin la linea de inyeccion) = "
          f"{r['a_medido']:.6g}"
          f"   [E_max = {r['E_max_V_m']:.6g} V/m, t = {r['t_max_fs']:.2f} fs,"
          f" celda ({r['pico_i']},{r['pico_j']}) = {r['pico_lambda_del_foco']:+.3f} lambda del foco]")
    print(f"  a_medido_caja (incluye la linea de inyeccion = ARTEFACTO) = "
          f"{r['a_medido_caja']:.6g}"
          f"   [E_max = {r['E_max_caja_V_m']:.6g} V/m; caja/ventana = "
          f"{r['a_medido_caja'] / r['a_medido']:.4g}]")
    print(f"  cB/|E| en el pico de la ventana = {r['cB_sobre_E_en_el_pico']:.4f}"
          f"   (1.0 = onda transversa propagandose; 0.514 medido en la linea de inyeccion)")
    print(f"  a_foco   (celda del foco)    = {r['a_foco']:.6g}"
          f"   [t = {r['t_foco_fs']:.2f} fs; a_foco/a_medido = {r['b_foco_rel']:.4f}]")
    print(f"  invariante a (eq:ab) max = {r['a_inv_max_V_m']:.6g} V/m"
          f"  ->  a_inv/|E|_pico = {r['a_inv_rel_al_pico']:.4f}"
          f"   (1.0 = campo puramente electrico; 0 = campo nulo)")
    print(f"  F/(eps0 E^2/2) en el pico = {r['F_rel_pico']:+.4f}"
          f"   (1.0 = puramente electrico; 0 = nulo)")
    print(f"  residuo del absorbedor (ultimos 100 pasos) = {r['cola_rel']:.3e} del pico")
    if r.get("sonda_eje"):
        print("  sonda del eje en el instante del pico del foco")
        print("    i    x-lambda   |E| (V/m)      a0 equiv   cB/|E|")
        for m in r["sonda_eje"]:
            print(f"    {m['i']:4d}  {m['x_lambda_del_foco']:+7.3f}   "
                  f"{m['E_V_m']:.6g}   {m['a0_equivalente']:10.4f}   "
                  f"{m['cB_sobre_E']:.3f}")


def serie(modo="colineal", nulo=False, etiqueta="colineal"):
    filas = []
    for n in N_LISTA:
        if modo == "contra" and n == 1:
            continue
        r = correr(modo=modo, n=n, nulo=nulo)
        b = bloque(r)
        filas.append(b)
        imprimir(b)
        print("")
    salida = {
        "T_UTC": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "UNIVERSO DECLARADO": UNIVERSO,
        "etiqueta": etiqueta, "modo": modo, "nulo": bool(nulo),
        "filas": filas,
    }
    (AQUI / f"etapa1_{etiqueta}.json").write_text(
        json.dumps(salida, indent=2, sort_keys=True), encoding="utf-8")
    pares = [(f["corrida"]["N"], f["corrida"]["a_medido"]) for f in filas]
    beta = pendiente(pares)
    print(f"--- serie {etiqueta} ---")
    for n, a in pares:
        print(f"  N={n:<3d} a_medido = {a:.6f}")
    print(f"  beta = {beta:.6f}   (control interno del instrumento)")
    print(f"  escrito: sim/etapa1_{etiqueta}.json")
    return pares, beta


def pendiente(pares):
    xs = [math.log(n) for n, _ in pares]
    ys = [math.log(a) for _, a in pares]
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    return num / den


def escribir_csv(pares, eta, nota):
    lineas = [
        "# sim/medidas_aN.csv -- MEDICION de la Etapa 1 (propagador clasico de",
        "# Maxwell 2D, sim/maxwell2d.py). Columna 1 = N ; columna 2 = a_medido",
        "# (adimensional, e max|E| / (m_e omega c)).",
        f"# generado: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}",
        f"# UNIVERSO DECLARADO: {UNIVERSO}",
        f"# geometria: haces co-propagantes desde el plano fuente x = {I_SL} celdas,",
        f"#   frente convergente al foco ({IC},{JC}), brazo {BRAZO_LAMBDA:g} lambda,",
        f"#   energia total fija repartida en N (a_beam = a_ref/sqrt(N), modelo).",
        f"# eta = a_medido(1)/a_tot_pred(1) = {eta:.6f}: el acoplamiento del",
        "#   instrumento. El falsador ancla en a(1) MEDIDO, asi que eta se cancela",
        "#   en beta y en el cociente; se declara para que la escala absoluta no",
        "#   se lea como parte del veredicto.",
        "# " + nota,
    ]
    for n, a in pares:
        lineas.append(f"{n},{a:.10g}")
    (AQUI / "medidas_aN.csv").write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print(f"escrito: sim/medidas_aN.csv ({len(pares)} filas)")


def pec_muros(F):
    """PEC: la E tangencial se anula en las cuatro paredes.

    Es la CONDICION que hace exactamente adjunto al par (ddx, ddx_f): el
    termino de borde de la identidad ddx = -ddx_f^T + (1/dx)(E_{N-1}H_{N-1} -
    E_0 H_0) se anula. NO se usa en correr(): aqui solo se PRUEBA la hipotesis
    del muro, midiendo el MISMO control con y sin ella.
    """
    F["Ey"][0, :] = 0.0
    F["Ey"][NX - 1, :] = 0.0
    F["Ez"][0, :] = 0.0
    F["Ez"][NX - 1, :] = 0.0
    F["Ex"][:, 0] = 0.0
    F["Ex"][:, NY - 1] = 0.0
    F["Ez"][:, 0] = 0.0
    F["Ez"][:, NY - 1] = 0.0


def control_energia(pasos_libres=None, pec=False):
    """Caja CERRADA y sin esponja: la energia del esquema debe conservarse.

    DEFECTO #1 CORREGIDO (declarado 11-Oct-2026): la version anterior anclaba
    U0 en t = TAU/2, o sea EN MEDIO del pulso y con la fuente TODAVIA
    inyectando, y lo rotulaba "U(t)/U0 medido tras apagar". Medido: dt =
    4.6699e-17 s, TAU = 20 fs = 429 pasos; el ancla caia en el paso 214 de 500
    => 214 de las 286 muestras median la INYECCION y no la conservacion
    (familia: un rotulo fijo que afirma lo que la linea siguiente desmiente no
    protege, informa). Ahora U0 se ancla en el primer paso con la fuente
    APAGADA y se cuentan SOLO los pasos de evolucion libre.

    DEFECTO #2 (medido en la misma corrida): el "invariante exacto de Yee" que
    yo habia escrito (E adelantada + producto de las dos H) dio deriva
    1.090e-03: NO era el invariante exacto -- el emparejamiento temporal se
    habia elegido a mano. Se corrige MIDIENDO CINCO emparejamientos en la
    MISMA corrida y comparando; la eleccion del candidato sale de esa
    comparacion (declarado). Lo que SI se pre-registra es el umbral (1e-9):
    un invariante exacto no puede diferir mas que roundoff.

    Se corre >= 2 travesias de la caja para que la onda TOQUE las paredes: es
    ahi donde el par (ddx, ddx_f) puede dejar de ser adjunto. Por eso el
    control acepta pec=True (E tangencial = 0 en las cuatro paredes), que es
    el UNICO cambio entre las dos corridas.
    """
    dt = CFL_2D * DX / P.C
    pasos_pulso = int(math.ceil(P.TAU / dt))
    if pasos_libres is None:
        pasos_libres = int(round(2.0 * NX / CFL_2D))     # 2 travesias de caja
    pasos = pasos_pulso + pasos_libres
    ripple = (P.OMEGA * dt) ** 2 / 4.0
    umbral = 1e-9
    paso_muro = int(round(I_SL / CFL_2D))
    print(f"UNIVERSO DECLARADO: {UNIVERSO}")
    print(f"control de energia: caja CERRADA (sin esponja), 1 haz, cfl = "
          f"{CFL_2D}, PEC en los muros = {pec}")
    print(f"  dt = {dt:.6g} s; omega dt = {P.OMEGA * dt:.4f} rad; "
          f"TAU = {P.TAU * 1e15:.4g} fs = {pasos_pulso} pasos de inyeccion")
    print(f"  el frente sale de la linea de inyeccion (i = {I_SL}) y toca la "
          f"pared en el paso ~{paso_muro} => la evolucion libre que se mide ya "
          f"incluye rebote (declarado)")
    print(f"  pre-registro (ANTES de medir): un invariante EXACTO no puede "
          f"diferir mas que roundoff (< {umbral:.0e}).")
    print("    Se miden cinco emparejamientos temporales de la MISMA energia "
          "(1/2 eps0 E.E + 1/2 mu0 H.H):")
    print("      1) E(n+1)^2 + H(n+1/2).H(n-1/2)   2) E(n).E(n+1) + H(n+1/2)^2")
    print("      3) E(n).E(n+1) + producto H        4) E(n)^2 + H(n-1/2)^2")
    print("      5) E(n+1)^2 + H(n+1/2)^2  (= energia(), sin centrar)")
    print(f"    el que quede en roundoff es el invariante exacto; los otros "
          f"deben oscilar a O((omega dt)^2) = {ripple:.3e}")
    print(f"    Se corren {pasos} pasos: {pasos_pulso} de inyeccion + "
          f"{pasos_libres} de evolucion libre = "
          f"{pasos_libres * CFL_2D / NX:.2f} travesias de la caja.")
    F = campos_vacios()
    g, fc = perfiles()
    terminos, _ = terminos_de("colineal", 1)
    u0 = None
    k0 = 0
    cand = {j: [] for j in range(1, 6)}
    for k in range(pasos):
        t = (k + 0.5) * dt
        inyectar(F, t, terminos, g, fc)     # sale solo si t > TAU (envolvente = 0)
        Ep = (F["Ex"], F["Ey"], F["Ez"])    # E^n (post-inyeccion)
        Hm = (F["Hx"], F["Hy"], F["Hz"])    # H^{n-1/2}
        paso(F, dt, None)                   # paso() REBINDE: Ep y Hm quedan intactos
        if pec:
            pec_muros(F)
        if (k + 1) * dt <= P.TAU:           # la fuente todavia inyecta: no se mide
            continue
        e2a = F["Ex"] ** 2 + F["Ey"] ** 2 + F["Ez"] ** 2
        e2b = Ep[0] ** 2 + Ep[1] ** 2 + Ep[2] ** 2
        ebe = Ep[0] * F["Ex"] + Ep[1] * F["Ey"] + Ep[2] * F["Ez"]
        h2a = F["Hx"] ** 2 + F["Hy"] ** 2 + F["Hz"] ** 2
        h2b = Hm[0] ** 2 + Hm[1] ** 2 + Hm[2] ** 2
        hba = Hm[0] * F["Hx"] + Hm[1] * F["Hy"] + Hm[2] * F["Hz"]
        gm = MU0 / P.EPS0
        med = {1: e2a + gm * hba, 2: ebe + gm * h2a, 3: ebe + gm * hba,
               4: e2b + gm * h2b, 5: e2a + gm * h2a}
        v = {j: 0.5 * P.EPS0 * float(np.sum(x)) * DX * DX
             for j, x in med.items()}
        if u0 is None:
            u0 = dict(v)
            k0 = k + 1
            print(f"  ancla de U0: paso {k0} de {pasos}, "
                  f"t = {k0 * dt * 1e15:.3f} fs > TAU = {P.TAU * 1e15:.3f} fs "
                  f"(fuente YA apagada)")
        for j in v:
            cand[j].append(v[j] / u0[j])
    nm = len(cand[1])
    deriva = {j: max(abs(u - 1.0) for u in cand[j]) for j in cand}
    mit = {j: (max(abs(u - 1.0) for u in cand[j][:nm // 2]),
               max(abs(u - 1.0) for u in cand[j][nm // 2:])) for j in cand}
    nombres = {1: "E(n+1)^2 + H(n+1/2).H(n-1/2)  [un solo H]",
               2: "E(n).E(n+1) + H(n+1/2)^2        [un solo E]",
               3: "E(n).E(n+1) + H(n+1/2).H(n-1/2) [bilineal]",
               4: "E(n)^2 + H(n-1/2)^2             [atrasado]",
               5: "E(n+1)^2 + H(n+1/2)^2           [sin centrar]"}
    print(f"  MEDIDO (evolucion libre, {nm} muestras, "
          f"{pasos - nm} pasos de inyeccion excluidos):")
    print("     candidato                                     deriva max   "
          "1a mitad   2a mitad")
    for j in sorted(deriva):
        print(f"    {j}) {nombres[j]:44s} {deriva[j]:.3e}   {mit[j][0]:.3e}  "
              f"{mit[j][1]:.3e}")
    exacto = min(deriva, key=deriva.get)
    v = "OK" if deriva[exacto] < umbral else "ROJO"
    print(f"  veredicto: el candidato {exacto} -- {nombres[exacto]} -- es el "
          f"de deriva minima = {deriva[exacto]:.3e} contra el umbral "
          f"pre-registrado {umbral:.0e} => {v}")
    if pec:
        print("  (corrida con PEC: el unico cambio respecto de la anterior es "
              "que la E tangencial se anula en las cuatro paredes)")
    destino = AQUI / ("etapa1_control_energia%s.json"
                      % ("_pec" if pec else ""))
    destino.write_text(
        json.dumps({"T_UTC": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "UNIVERSO DECLARADO": UNIVERSO, "pec": pec,
                    "pasos_pulso": pasos_pulso, "pasos_libres": pasos_libres,
                    "pasos": pasos, "ancla_paso": k0, "cfl": CFL_2D,
                    "dt_s": dt, "paso_muro": paso_muro,
                    "ripple_previsto": ripple, "umbral": umbral,
                    "deriva": {str(j): deriva[j] for j in deriva},
                    "deriva_mitades": {str(j): list(mit[j]) for j in mit},
                    "candidato_exacto": exacto, "veredicto": v},
                   indent=2, sort_keys=True), encoding="utf-8")
    return deriva


def control_cfl():
    """El CFL pre-registrado (0.90) contra el limite de von Neumann en 2D."""
    print(f"UNIVERSO DECLARADO: {UNIVERSO}")
    print("control de estabilidad: el MISMO instrumento con dos CFL.")
    print(f"  limite de von Neumann en 2D: dt <= dx/(c sqrt(2))  ->  CFL <= "
          f"{1/math.sqrt(2):.6f}")
    out = {}
    for cfl in (CFL_PRE, CFL_2D):
        picos = []
        dt = cfl * DX / P.C
        F = campos_vacios()
        g, fc = perfiles()
        terminos, _ = terminos_de("colineal", 1)
        for k in range(400):
            t = (k + 0.5) * dt
            if t <= P.TAU:
                inyectar(F, t, terminos, g, fc)
            paso(F, dt, mascara_esponja())
            picos.append(float(modulo_E(F).max()))
        crec = picos[-1] / max(picos[0], 1e-300)
        out[str(cfl)] = {"E_pico_final_V_m": picos[-1], "crecimiento": crec}
        print(f"  cfl = {cfl}: |E| al paso 400 = {picos[-1]:.6g} V/m "
              f"(crecimiento {crec:.3e} respecto del paso 0)")
    (AQUI / "etapa1_control_cfl.json").write_text(
        json.dumps({"T_UTC": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "UNIVERSO DECLARADO": UNIVERSO, "medido": out},
                   indent=2, sort_keys=True), encoding="utf-8")
    return out


def main() -> int:
    args = sys.argv[1:]
    if "--control-energia" in args:
        control_energia()
        return 0
    if "--control-energia-pec" in args:
        control_energia(pec=True)
        return 0
    if "--control-cfl" in args:
        control_cfl()
        return 0
    if "--serie" in args:
        pares, beta = serie("colineal", nulo=False, etiqueta="colineal")
        eta = pares[0][1] / float(CFG["filas"][0]["a_tot_pred"])
        escribir_csv(pares, eta, "modo colineal (PRE-REGISTRADO, §1).")
        return 0
    if "--serie-nulo" in args:
        serie("colineal", nulo=True, etiqueta="colineal_nulo")
        return 0
    if "--serie-contra" in args:
        serie("contra", nulo=False, etiqueta="contra")
        return 0
    if "--serie-contra-nulo" in args:
        r = correr(modo="contra", n=4, desplaza_dcha=int(round(0.5 / DX_OVER_LAMBDA)))
        imprimir(bloque(r))
        return 0
    modo = "colineal"
    if "--modo" in args:
        modo = args[args.index("--modo") + 1]
    n = 1
    if "--n" in args:
        n = int(args[args.index("--n") + 1])
    nulo = "--nulo" in args
    r = correr(modo=modo, n=n, nulo=nulo, verbose="--verbose" in args,
               duro="--duro" in args, sonda="--sonda" in args)
    b = bloque(r)
    imprimir(b)
    if "--json" in args:
        print(json.dumps(b, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
