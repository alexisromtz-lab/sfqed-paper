#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LECTOR DE INVARIANTES  (orden de Pestaña 3 · tres salvaguardas)

LEE  a_inv = sqrt( sqrt(F^2 + G^2) + F )  con
     F = 1/2 (eps0|E|^2 - |B|^2/mu0)      G = (E.B)/(c mu0)
en los DOS motores del repo, y NO toca sim/medidas_aN.csv.

=====================================================================
PRE-REGISTRO (escrito ANTES de imprimir cualquier cifra de este archivo)
=====================================================================
Ventana ... motor analitico : malla 61^3, lado 6 lambda_L, M_FASE = 32
Ventana ... motor 2D FDTD   : caja 480^2 (12 lambda_L), dx = lambda_L/40,
                              VENTANA DE MEDIDA = celdas [100,380] (halo de 20
                              alrededor de cada plano fuente), diagnostico
                              propio cada paso; el del motor sellado es cada 20.
Unidad   ... a0 = campo_de_a0(1.0) (V/m) para el valor, y cociente adimensional
             a_inv/|E| para la comparacion con el pico.
Metricas ... DOS, por orden del dueno:
             (1) a_inv_origen  = max sobre el tiempo de a_inv en el nodo focal
                 exacto: analitico [30,30,30] (donde eje_malla(61)[30] == 0.0),
                 FDTD [IC,JC] = [240,240].
             (2) a_inv_supremo = max sobre tiempo Y sobre la ventana espacial,
                 CON la localizacion del supremo (i,j y (i-IC)*dx en lambda_L).
Metricas ... tres lecturas del MISMO campo, para separar el artefacto de malla
             de la fisica:
             (L1) naive            = emparejamiento de INDICE IGUAL (E y H en la
                                     misma celda). Es lo que hace hoy
                                     maxwell2d.invariante_a en malla escalonada.
             (L2) interpolado      = B promediado a los nodos enteros de E antes
                                     del producto escalar. Es la salvaguarda #1.
             (L3) interpolado_puntual = L2 evaluado en la celda y el instante del
                                     pico de |E| de la ventana (no en su propio
                                     maximo): mide cuanto del cociente sellado
                                     "a_inv_rel_al_pico" es cociente de DOS
                                     maximos en celdas distintas.

COTAS CERRADAS del control sintetico (onda plana transversa circular, lambda = 40
celdas, verdad a_inv = F = G = 0 EXACTO porque E.B = 0 y |B| = |E|/c):
    delta = k dx/2 = 0.078540 rad = 4.5000 deg ; sin(delta) = 0.078459
    L1  a_inv/|E| = sqrt(sin(delta)) = 0.280106     |G|/(eps0 E^2) = sin(delta)
    L2  a_inv/|E| = sin(delta)       = 0.078459     G = 0 exacto,
                                                    |F|/(eps0 E^2/2) = sin^2(delta)
    Las dos cotas se escriben ANTES de correr; el control enrojece si no se
    reproducen a 1e-6.  Nota estructural: a_inv es raiz de una forma cuadratica,
    asi que un error RELATIVO O(delta^2) en el campo sale O(delta) en a_inv.

ANCLA declarada de antemano: en el motor analitico a_inv(N=1) = 0 por Lemma 1
(control C1), luego el cociente anclado a la medida a(1) es 0/0 para la lectura
de invariante. La ancla NO CERO minima es N = 2; la ley esperada es
a_inv(N) = a_inv(2) * sqrt(N/2).

QUE DECIDE ESTE ARCHIVO (pregunta abierta, no adjudicada):
el sello FDTD etapa1_colineal.json trae a_inv_rel_al_pico = 0.999513 y
F_rel_pico = 0.10551, IDENTICOS en N = 1,2,4,8,16; el motor analitico da a_inv = 0
para la misma familia. La cota de malla sola (L1 = 0.280106, y con el desfase
temporal anadido ~0.36) NO alcanza 0.9995. Si al interpolar (L2) el FDTD baja a
~0.08-0.28 => el sello era artefacto del lector. Si NO baja => hay
no-transversalidad real del haz convergente que el modelo analitico no puede
representar (su B = khat x eps hace E.B = 0 POR CONSTRUCCION), y entonces
"Lemma 1 => a_inv = 0" es identidad del modelo, no medida del campo.

SALVAGUARDAS: (1) interpolacion de Yee antes del producto escalar -- aqui, con
control sintetico de verdad cerrada. (2) cero colisiones: este archivo vive solo
y escribe SOLO en sim/data/invariantes/; al terminar verifica que
sim/medidas_aN.csv conserva su sha16 y aborta si no. (3) las dos metricas de
arriba, mas la tercera lectura.  NO ES EVIDENCIA del articulo: es verificacion de
instrumento (misma clausula que S).
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

import field_solver as FS  # noqa: E402
import maxwell2d as M  # noqa: E402
import params as P  # noqa: E402

DATOS = AQUI / "data" / "invariantes"
CSV = DATOS / "medidas_invariantes_aN.csv"
CRUDO = DATOS / "crudo_lector_invariantes.json"
MEDIDAS_A_N = AQUI / "medidas_aN.csv"          # INTOCABLE

LECTURAS = ("naive", "interpolado", "interpolado_puntual")
SELLOS = {"colineal": AQUI / "etapa1_colineal.json",
          "contra": AQUI / "etapa1_contra.json"}
TOL_SINT = 1e-6
TOL_ANALITICO = 1e-9
E_A0_1 = P.campo_de_a0(1.0)
DELTA = math.sin(math.pi / 40.0)               # sin(k dx/2) con lambda = 40 dx


def sha16(ruta: Path) -> str:
    return hashlib.sha256(Path(ruta).read_bytes()).hexdigest()[:16]


def sello_de(modo: str, n: int):
    """Fila del motor sellado (etapa1_<modo>.json) para comparar, si existe.

    SOLO LECTURA: este archivo nunca escribe en los JSON sellados.
    """
    ruta = SELLOS.get(modo)
    if ruta is None or not ruta.exists():
        return None
    datos = json.loads(ruta.read_text())
    for fila in datos.get("filas", []):
        c = fila.get("corrida", {})
        if int(c.get("N", -1)) == int(n) and not c.get("nulo"):
            return c
    return None


# ==================================================================
# implementacion INDEPENDIENTE del invariante (dos normalizaciones)
# ==================================================================
def invariante(Ex, Ey, Ez, Bx, By, Bz, eps, mu):
    """Devuelve (a, F, G) en SI: F, G en J/m^3 ; a en V/m."""
    e2 = Ex * Ex + Ey * Ey + Ez * Ez
    b2 = Bx * Bx + By * By + Bz * Bz
    F = 0.5 * (eps * e2 - b2 / mu)
    G = (Ex * Bx + Ey * By + Ez * Bz) / (P.C * mu)
    raiz = np.sqrt(F * F + G * G)
    return np.sqrt(np.maximum(raiz + F, 0.0)) / math.sqrt(eps), F, G


def invariante_adimensional(Ex, Ey, Ez, Bx, By, Bz):
    """Misma funcion con B ya en unidades de E (convencion del motor analitico:
    Br = cross(khat, eps), o sea c|B| = |E|).  Devuelve (a, F, G) sin normalizar.
    """
    e2 = Ex * Ex + Ey * Ey + Ez * Ez
    b2 = Bx * Bx + By * By + Bz * Bz
    F = 0.5 * (e2 - b2)
    G = Ex * Bx + Ey * By + Ez * Bz
    raiz = np.sqrt(F * F + G * G)
    return np.sqrt(np.maximum(raiz + F, 0.0)), F, G


# ==================================================================
# interpolacion a los nodos enteros de E (salvaguarda #1)
# ==================================================================
def interp_x(a):
    """Medionodos (i-1/2 , i+1/2) -> nodo i, a lo largo de x (eje 0).
    Error de la interpolacion: el valor sale atenuado por cos(k dx/2) si no se
    corrige; el DESFASE es exactamente 0.  La fila 0 no tiene vecino izquierdo:
    se marca NaN y NUNCA se lee (la ventana de medida arranca en la celda 100)."""
    b = 0.5 * (a + np.roll(a, 1, axis=0))
    b[0, :] = np.nan
    return b


def interp_y(a):
    b = 0.5 * (a + np.roll(a, 1, axis=1))
    b[:, 0] = np.nan
    return b


def B_a_nodos(F):
    """B interpolado a los nodos enteros de E, con la geometria REAL del esquema:
    Hy, Hz viven en x_(i+1/2) (su derivada es ddx_f) ; Hx vive en y_(j+1/2)."""
    return (M.MU0 * interp_y(F["Hx"]),
            M.MU0 * interp_x(F["Hy"]),
            M.MU0 * interp_x(F["Hz"]))


# ==================================================================
# control 1: sintetico de verdad cerrada (malla de Yee)
# ==================================================================
def control_sintetico():
    DX, NX, NY = M.DX, M.NX, M.NY
    k = 2.0 * math.pi / (40.0 * DX)
    x = np.arange(NX) * DX
    A = 1.0
    hb = A / P.C                                # B en tesla: |B| = |E|/c
    z = np.zeros((NX, NY))
    phi = np.tile(k * x[:, None], (1, NY))
    phh = np.tile(k * (x + DX / 2.0)[:, None], (1, NY))
    E_y = A * np.cos(phi)
    E_z = A * np.sin(phi)
    Bh_y = -hb * np.sin(phh)
    Bh_z = +hb * np.cos(phh)
    INT = (slice(2, NX - 2), slice(0, NY))      # interior declarado, 2 de guarda

    salida = {}
    for nom, By, Bz in (("naive", Bh_y, Bh_z),
                        ("interpolado", interp_x(Bh_y), interp_x(Bh_z))):
        a, Fs, Gs = invariante(z, E_y, E_z, z, By, Bz, P.EPS0, M.MU0)
        a = np.abs(a)[INT]
        salida[nom] = {
            "a_inv_sobre_E": float(a.max() / A),
            "G_sobre_eps0E2": float(np.abs(Gs)[INT].max() / (P.EPS0 * A * A)),
            "F_sobre_eps0E2_medio": float(np.abs(Fs)[INT].max() / (0.5 * P.EPS0 * A * A)),
        }
    cotas = {
        "naive": {"a_inv_sobre_E": math.sqrt(DELTA), "G_sobre_eps0E2": DELTA,
                  "F_sobre_eps0E2_medio": 0.0},
        "interpolado": {"a_inv_sobre_E": DELTA, "G_sobre_eps0E2": 0.0,
                        "F_sobre_eps0E2_medio": DELTA * DELTA},
    }
    desvios = {}
    ok = True
    for nom in salida:
        for campo in cotas[nom]:
            d = abs(salida[nom][campo] - cotas[nom][campo])
            desvios[f"{nom}.{campo}"] = d
            if d > TOL_SINT:
                ok = False
    return {"ok": ok, "medido": salida, "cota_cerrada": cotas,
            "desvio_max": max(desvios.values()), "delta_sin_kdx2": DELTA,
            "k_dx_2_deg": math.degrees(k * DX / 2.0)}


# ==================================================================
# control 2: mi lector contra el lector del motor analitico
# ==================================================================
def _a_inv_analitico(lista, e0, nodos=None):
    """Reimplementacion independiente de field_solver.medir() para a_inv."""
    Er, Br, centro = FS.campos(lista, e0, True, nodos)
    amp_max = 0.0
    inv_max = 0.0
    inv_foco = 0.0
    quies = math.inf
    fo_min = math.inf
    for m in range(FS.M_FASE):
        th = 2.0 * math.pi * m / FS.M_FASE
        c, s = math.cos(th), math.sin(th)
        E = [Er[i].real * c + Er[i].imag * s for i in range(3)]
        B = [Br[i].real * c + Br[i].imag * s for i in range(3)]
        a, _, _ = invariante_adimensional(E[0], E[1], E[2], B[0], B[1], B[2])
        amp_max = max(amp_max, float(np.sqrt(sum(e * e for e in E).max())))
        inv_max = max(inv_max, float(a.max()))
        af = float(a[centro, centro, centro])
        inv_foco = max(inv_foco, af)
        fo_min = min(fo_min, af)
    quies = (fo_min / inv_foco) if inv_foco > 0 else 0.0
    return {"a_amp": amp_max / E_A0_1, "a_inv": inv_max / E_A0_1,
            "a_fo_max": inv_foco / E_A0_1, "quiescencia": quies}, Er, Br, centro


def control_analitico():
    casos = {}
    for fam, n in (("copropagante", 4), ("coaxial_contra", 4)):
        lista = FS.haces(fam, "circular", FS.ALPHA_REF_DEG, n)
        e0 = P.campo_de_a0(1.0)
        mio, Er, Br, centro = _a_inv_analitico(lista, e0)
        suyo = FS.medir(lista, e0)
        desvio = abs(mio["a_inv"] - suyo["a_inv"]) / max(abs(suyo["a_inv"]), 1e-300)
        # co-localizacion: E y B salen del MISMO amp sobre el MISMO X,Y,Z.
        # Si estuvieran escalonados media celda, E.B no podria anularse exacto.
        maxEB = 0.0
        maxE = 0.0
        for m in range(FS.M_FASE):
            th = 2.0 * math.pi * m / FS.M_FASE
            c, s = math.cos(th), math.sin(th)
            E = [Er[i].real * c + Er[i].imag * s for i in range(3)]
            B = [Br[i].real * c + Br[i].imag * s for i in range(3)]
            EB = np.abs(E[0] * B[0] + E[1] * B[1] + E[2] * B[2]).max()
            EE = sum(e * e for e in E).max()
            maxEB = max(maxEB, float(EB))
            maxE = max(maxE, float(EE))
        casos[fam] = {
            "N": n,
            "a_inv_mio": mio["a_inv"], "a_inv_motor": suyo["a_inv"],
            "a_amp_motor": suyo["a_amp"], "desvio_rel": desvio,
            "a_fo_max_motor": suyo["a_fo_max"],
            "F_fo_max_motor": suyo["F_fo_max"],
            "G_fo_absmax_motor": suyo["G_fo_absmax"],
            "max_abs_EB_sobre_maxE2": (maxEB / maxE) if maxE else 0.0,
            "centro": centro,
        }
    ok = all(c["desvio_rel"] <= TOL_ANALITICO for c in casos.values())
    return {"ok": ok, "casos": casos}


# ==================================================================
# motor 2D FDTD: copia fiel del bucle de maxwell2d.correr()
# ==================================================================
def corrida_motor2d(modo, n, verbose=False):
    cfl = M.CFL_2D
    pasos = int(round(M.TRANSITO_LAMBDA / (cfl * M.DX_OVER_LAMBDA)))
    dt = cfl * M.DX / P.C
    F = M.campos_vacios()
    masc = M.mascara_esponja()
    g, fases = M.perfiles()
    terminos, _ = M.terminos_de(modo, n, nulo=False)

    V0, V1 = M.VENTANA_I0, M.VENTANA_I1
    sl = (slice(V0, V1 + 1), slice(None))
    IC, JC = M.IC, M.JC

    emax = 0.0
    efoco = 0.0
    reg = {L: {"origen": 0.0, "supremo": 0.0, "ij": None, "F": 0.0, "G": 0.0,
               "t_fs": 0.0, "nan_extra": 0, "E_en_supremo": 0.0}
           for L in LECTURAS}
    pico = {"a_naive": 0.0, "a_interp": 0.0, "F": 0.0, "G": 0.0, "ij": None}
    rel_cad_naive = 0.0
    inv_cad_naive = 0.0
    # el sello mide razon de MAXIMOS DE VENTANA al mismo instante (dos celdas
    # distintas): se reproduce la cifra en LAS DOS lecturas para poder separar
    # el defecto de la razon (ii) de la fisica del punto nodal.
    rel_cad_interp = 0.0
    inv_cad_interp = 0.0
    desv_naive_mio = 0.0
    registro = []

    for k in range(pasos):
        t = (k + 0.5) * dt
        M.inyectar(F, t, terminos, g, fases)
        M.paso(F, dt, masc)
        e = M.modulo_E(F)
        e_ven = e[sl]
        em = float(e_ven.max())
        idx = int(np.argmax(e_ven))
        ip, jp = divmod(idx, M.NY)
        ip += V0
        if em > emax:
            emax = em
        ef = float(e[IC, JC])
        if ef > efoco:
            efoco = ef

        Bxi, Byi, Bzi = B_a_nodos(F)

        # --- L1 naive: el lector de la casa, sobre la ventana ---
        sub = {c: F[c][sl] for c in M.COMPONENTES}
        a_naive_full = M.invariante_a(sub)                 # funcion de la casa
        a1, F1, G1 = invariante(sub["Ex"], sub["Ey"], sub["Ez"],
                                M.MU0 * sub["Hx"], M.MU0 * sub["Hy"],
                                M.MU0 * sub["Hz"], P.EPS0, M.MU0)
        desv_naive_mio = max(desv_naive_mio,
                             float(np.abs(a1 - a_naive_full).max() / max(a_naive_full.max(), 1e-300)))
        v1 = float(a_naive_full.max())
        if v1 > reg["naive"]["supremo"]:
            reg["naive"]["supremo"] = v1
            ij = np.unravel_index(int(np.argmax(a_naive_full)), a_naive_full.shape)
            reg["naive"]["ij"] = (int(ij[0]) + V0, int(ij[1]))
            reg["naive"]["t_fs"] = (k + 1) * dt * 1e15
            reg["naive"]["F"] = float(F1[ij])
            reg["naive"]["G"] = float(G1[ij])
            # |E| CO-UBICADO en la celda e instante del supremo: es el
            # companero puntual de la razon de maximos del sello.
            reg["naive"]["E_en_supremo"] = float(e_ven[ij])
        reg["naive"]["origen"] = max(reg["naive"]["origen"], float(a_naive_full[IC - V0, JC]))
        if k % M.DIAG_CADA == 0:                           # cadencia del sello
            inv_cad_naive = max(inv_cad_naive, v1)
            if em > 0.0:
                rel_cad_naive = max(rel_cad_naive, v1 / em)

        # --- L2 interpolado: B en los nodos enteros de E ---
        a_i, F_i, G_i = invariante(F["Ex"], F["Ey"], F["Ez"],
                                   Bxi, Byi, Bzi, P.EPS0, M.MU0)
        ai = a_i[sl]
        # NaN DECLARADO: la interpolacion en j de Hx no tiene vecino j-1 en la
        # columna 0 => una NaN por fila. Cualquier OTRA NaN es un defecto y se
        # cuenta aparte; el maximo se toma con nanmax (la columna 0 queda fuera).
        n_nan = int(np.isnan(ai).sum())
        reg["interpolado"]["nan_extra"] = max(reg["interpolado"]["nan_extra"],
                                             n_nan - int(ai.shape[0]))
        v2 = float(np.nanmax(ai))
        if v2 > reg["interpolado"]["supremo"]:
            reg["interpolado"]["supremo"] = v2
            ij = np.unravel_index(int(np.nanargmax(ai)), ai.shape)
            reg["interpolado"]["ij"] = (int(ij[0]) + V0, int(ij[1]))
            reg["interpolado"]["t_fs"] = (k + 1) * dt * 1e15
            reg["interpolado"]["F"] = float(F_i[sl][ij])
            reg["interpolado"]["G"] = float(G_i[sl][ij])
            reg["interpolado"]["E_en_supremo"] = float(e_ven[ij])
        reg["interpolado"]["origen"] = max(reg["interpolado"]["origen"],
                                           float(a_i[IC, JC]))
        if k % M.DIAG_CADA == 0:                           # cadencia del sello
            inv_cad_interp = max(inv_cad_interp, v2)
            if em > 0.0:
                rel_cad_interp = max(rel_cad_interp, v2 / em)

        # --- L3 puntual: L2 en la celda e instante del pico de |E| ---
        if em >= emax:
            ic, jc = ip, jp
            pico["a_naive"] = float(a_naive_full[ic - V0, jc])
            pico["a_interp"] = float(a_i[ic, jc])
            pico["F"] = float(F_i[ic, jc])
            pico["G"] = float(G_i[ic, jc])
            pico["ij"] = (ic, jc)
            pico["E_max_punto"] = em

        if verbose and k % (M.DIAG_CADA * 10) == 0:
            print(f"    paso {k:5d}  max|E| = {em:.6g}  a_inv naive {v1:.6g} "
                  f"interp {v2:.6g}", flush=True)

    pico["a_naive"] = float(pico.get("a_naive", 0.0))
    salida = {
        "modo": modo, "N": n, "pasos": pasos, "cfl": cfl,
        "a_medido_a0": P.a0_de_campo(emax),
        "E_max_V_m": emax,
        "a_foco_a0": P.a0_de_campo(efoco),
        "a_inv_naive_max_cadencia20_V_m": inv_cad_naive,
        "a_inv_rel_al_pico_cadencia20": rel_cad_naive,
        "a_inv_interp_max_cadencia20_V_m": inv_cad_interp,
        "a_inv_rel_al_pico_cadencia20_interp": rel_cad_interp,
        "desvio_mi_naive_vs_casa": desv_naive_mio,
        "lecturas": {},
        "pico": pico,
    }
    for L in LECTURAS:
        if L == "interpolado_puntual":
            continue
        d = reg[L]
        salida["lecturas"][L] = {
            "origen_a0": d["origen"] / E_A0_1,
            "origen_sobre_amp": d["origen"] / E_A0_1 / salida["a_foco_a0"] if salida["a_foco_a0"] else 0.0,
            "supremo_a0": d["supremo"] / E_A0_1,
            "supremo_sobre_amp": d["supremo"] / E_A0_1 / P.a0_de_campo(emax) if emax else 0.0,
            "supremo_ij": d["ij"],
            "supremo_lambda_del_foco": (d["ij"][0] - IC) * M.DX_OVER_LAMBDA if d["ij"] else None,
            "supremo_t_fs": d["t_fs"],
            "F_supremo": d["F"], "G_supremo": d["G"],
            "nan_extra_declarada": d["nan_extra"],
            # cociente PUNTUAL en el propio supremo (misma celda, mismo
            # instante): el sello no lo mide; aqui si.
            "E_en_supremo_a0": d["E_en_supremo"] / E_A0_1,
            "supremo_sobre_E_en_supremo": (d["supremo"] / d["E_en_supremo"]
                                           if d["E_en_supremo"] else 0.0),
            "razon_cadencia20": rel_cad_naive if L == "naive" else rel_cad_interp,
            "a_inv_max_cadencia20_V_m": (inv_cad_naive if L == "naive"
                                        else inv_cad_interp),
        }
    salida["lecturas"]["interpolado_puntual"] = {
        "a_a0_en_el_pico": pico["a_interp"] / E_A0_1,
        "a_naive_a0_en_el_pico": pico["a_naive"] / E_A0_1,
        "celda": pico["ij"],
        "E_max_punto_V_m": pico.get("E_max_punto", 0.0),
        "F_rel": pico["F"] / max(0.5 * P.EPS0 * pico.get("E_max_punto", 1.0) ** 2, 1e-300),
        "G_rel": pico["G"] / max(P.EPS0 * pico.get("E_max_punto", 1.0) ** 2, 1e-300),
    }
    return salida


# ==================================================================
def main() -> int:
    ap = argparse.ArgumentParser(description="Lector de invariantes (a_inv)")
    ap.add_argument("--control", action="store_true", help="solo los dos controles")
    ap.add_argument("--modos", nargs="+", default=["colineal", "contra"])
    ap.add_argument("--ns", nargs="+", type=int, default=[1, 2, 4, 8, 16])
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--sin-escribir", action="store_true")
    args = ap.parse_args()

    sha_antes = sha16(MEDIDAS_A_N) if MEDIDAS_A_N.exists() else "AUSENTE"
    t0 = time.time()

    print("== LECTOR DE INVARIANTES ==")
    print(f"sha16 maxwell2d.py     = {sha16(AQUI / 'maxwell2d.py')}")
    print(f"sha16 field_solver.py  = {sha16(AQUI / 'field_solver.py')}")
    print(f"sha16 lector (este)    = {sha16(Path(__file__))}")
    print(f"sim/medidas_aN.csv intocable, sha16 antes = {sha_antes}")
    print(f"UNIVERSO DECLARADO: analitico malla 61^3 (6 lambda_L, M_FASE=32) ; "
          f"FDTD malla xy {M.NX}x{M.NY} (12 lambda_L, dx=lambda_L/40), ventana de "
          f"medida celdas [{M.VENTANA_I0},{M.VENTANA_I1}], unidad = a0 ; "
          f"la ventana temporal es TODO el transito ({M.TRANSITO_LAMBDA:.3f} lambda_L)")

    c1 = control_sintetico()
    print("\n-- control 1: sintetico de malla de Yee (verdad cerrada a_inv = 0) --")
    print(f"{'lectura':16s} {'a_inv/|E| medido':>17s} {'cota cerrada':>13s} "
          f"{'|G|/(eps0E^2)':>14s} {'cota':>10s} {'|F|/(eps0E^2/2)':>16s} {'cota':>10s}")
    for L in ("naive", "interpolado"):
        m = c1["medido"][L]; c = c1["cota_cerrada"][L]
        print(f"{L:16s} {m['a_inv_sobre_E']:17.6f} {c['a_inv_sobre_E']:13.6f} "
              f"{m['G_sobre_eps0E2']:14.6f} {c['G_sobre_eps0E2']:10.6f} "
              f"{m['F_sobre_eps0E2_medio']:16.6f} {c['F_sobre_eps0E2_medio']:10.6f}")
    print(f"   k dx/2 = {c1['k_dx_2_deg']:.4f} deg ; desvio max contra la cota = {c1['desvio_max']:.3e}")
    print(f"   control 1: {'VERDE' if c1['ok'] else 'ROJO'}")

    c2 = control_analitico()
    print("\n-- control 2: mi lector contra field_solver.medir() (motor analitico) --")
    for fam, c in c2["casos"].items():
        print(f"   {fam:18s} a_inv mio {c['a_inv_mio']:.6f}  motor {c['a_inv_motor']:.6f}"
              f"  desvio {c['desvio_rel']:.2e}  a_fo {c['a_fo_max_motor']:.6f}"
              f"  |E.B|/E^2 max {c['max_abs_EB_sobre_maxE2']:.2e}")
    print(f"   el motor analitico NO tiene malla escalonada: Er y Br salen del MISMO")
    print(f"   amp sobre el MISMO X,Y,Z => E.B = 0 exacto en cada nodo y la")
    print(f"   interpolacion de la salvaguarda #1 es la IDENTIDAD ahi.")
    print(f"   control 2: {'VERDE' if c2['ok'] else 'ROJO'}")

    if not (c1["ok"] and c2["ok"]):
        print("\nCONTROL ROJO -> no se escribe ningun artefacto", file=sys.stderr)
        return 3

    crudo = {"T_UTC": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
             "sha16": {"maxwell2d": sha16(AQUI / "maxwell2d.py"),
                       "field_solver": sha16(AQUI / "field_solver.py"),
                       "lector": sha16(Path(__file__))},
             "control_sintetico": c1, "control_analitico": c2, "corridas": []}
    filas = []
    no_aplicables = []

    if not args.control:
        # PRE-VUELO (0 s): la aplicabilidad de cada par se pregunta AL MOTOR.
        # terminos_de es PURA (arma listas, no toca campos) => el par no aplicable se
        # sabe en 0 s. Antes se descubria a mitad de serie: la escritura es POST-BUCLE,
        # asi que un fallo en la ultima pierna se llevaba por delante las anteriores
        # (medido 2026-10-11: colineal 1,2,4,8,16 = 5 piernas y ~470 s de computo
        # perdidas por el N=1 de contra). Un par no aplicable se DECLARA y se salta.
        pares = []
        for modo in args.modos:
            for n in args.ns:
                try:
                    M.terminos_de(modo, n, nulo=False)
                except ValueError as e:
                    no_aplicables.append({"modo": modo, "N": n, "motivo": str(e)})
                    print(f"\n-- {modo} N={n}: NO APLICABLE ({e}) -> se salta, declarado --")
                    continue
                pares.append((modo, n))
        crudo["no_aplicables"] = no_aplicables
        if not pares:
            print("\nningun par aplicable", file=sys.stderr)
            return 3
        for modo, n in pares:
                ts = time.time()
                r = corrida_motor2d(modo, n, verbose=args.verbose)
                r["segundos"] = round(time.time() - ts, 1)
                crudo["corridas"].append(r)
                print(f"\n-- FDTD {modo} N={n}  ({r['segundos']} s) --")
                s = sello_de(modo, n)
                print(f"   a_medido {r['a_medido_a0']:.6f}  a_foco {r['a_foco_a0']:.6f}"
                      f"  sellado a_medido {s['a_medido'] if s else 'AUSENTE'!r}"
                      f"  identico: {bool(s) and r['a_medido_a0'] == s['a_medido']}")
                for L in ("naive", "interpolado"):
                    d = r["lecturas"][L]
                    lam = (f"{d['supremo_lambda_del_foco']:.2f}"
                           if d["supremo_lambda_del_foco"] is not None else "n/a")
                    print(f"   {L:12s} origen {d['origen_a0']:.6f} (/{d['origen_sobre_amp']:.6f} del foco)"
                          f"  supremo {d['supremo_a0']:.6f} (/{d['supremo_sobre_amp']:.6f})"
                          f"  en {lam} lambda del foco"
                          f"  nan_extra {d['nan_extra_declarada']}")
                    print(f"   {L:12s} razon de maximos de ventana (cadencia 20) "
                          f"{d['supremo_sobre_amp']:.6f} vs E co-ubicado en el supremo "
                          f"{d['E_en_supremo_a0']:.6f} => puntual "
                          f"{d['supremo_sobre_E_en_supremo']:.6f}"
                          f"  a_inv_max {d['supremo_a0'] * E_A0_1:.10g} V/m")
                p = r["lecturas"]["interpolado_puntual"]
                print(f"   puntual en el pico de |E|: interp {p['a_a0_en_el_pico']:.6f}"
                      f"  naive {p['a_naive_a0_en_el_pico']:.6f}"
                      f"  F_rel {p['F_rel']:.6f}  G_rel {p['G_rel']:.6f}")
                if s:
                    print(f"   sello: a_inv_max_V_m {s['a_inv_max_V_m']!r} ; a_inv_rel_al_pico "
                          f"{s['a_inv_rel_al_pico']!r} ; F_rel_pico {s['F_rel_pico']!r}")
                    print(f"   GATE naive-cadencia20: a_inv_max mio "
                          f"{r['a_inv_naive_max_cadencia20_V_m']!r} == sello: "
                          f"{r['a_inv_naive_max_cadencia20_V_m'] == s['a_inv_max_V_m']} ; "
                          f"cociente mio {r['a_inv_rel_al_pico_cadencia20']!r} == sello: "
                          f"{r['a_inv_rel_al_pico_cadencia20'] == s['a_inv_rel_al_pico']}")
                    print(f"   MISMA razon (de maximos de ventana, cadencia 20) con la lectura "
                          f"INTERPOLADA: {r['a_inv_rel_al_pico_cadencia20_interp']:.6f}"
                          f"  [cota de malla de la onda plana: {DELTA:.6f}; naive "
                          f"{math.sqrt(DELTA):.6f}]")
                    print(f"   cociente PUNTUAL co-ubicado en el supremo (el sello no lo mide): "
                          f"naive {r['lecturas']['naive']['supremo_sobre_E_en_supremo']:.6f} ; "
                          f"interp {r['lecturas']['interpolado']['supremo_sobre_E_en_supremo']:.6f}")
                print(f"   desvio mi-lector-naive vs la casa (maxwell2d.invariante_a): "
                      f"{r['desvio_mi_naive_vs_casa']:.2e}")
                for L in ("naive", "interpolado"):
                    d = r["lecturas"][L]
                    filas.append([n, modo, L, f"{r['a_medido_a0']:.10g}",
                                  f"{d['origen_a0']:.10g}", f"{d['origen_sobre_amp']:.10g}",
                                  f"{d['supremo_a0']:.10g}", f"{d['supremo_sobre_amp']:.10g}",
                                  d["supremo_ij"][0] if d["supremo_ij"] else -1,
                                  d["supremo_ij"][1] if d["supremo_ij"] else -1,
                                  f"{d['supremo_lambda_del_foco']:.6g}" if d["supremo_lambda_del_foco"] is not None else "",
                                  f"{d['F_supremo']:.10g}", f"{d['G_supremo']:.10g}",
                                  f"{d['supremo_t_fs']:.6g}",
                                  f"{d['razon_cadencia20']:.10g}",
                                  f"{d['E_en_supremo_a0']:.10g}",
                                  f"{d['supremo_sobre_E_en_supremo']:.10g}",
                                  f"{d['nan_extra_declarada']}"])

    sha_despues = sha16(MEDIDAS_A_N) if MEDIDAS_A_N.exists() else "AUSENTE"
    if sha_despues != sha_antes:
        print(f"\nCOLISION: sim/medidas_aN.csv cambio ({sha_antes} -> {sha_despues})",
              file=sys.stderr)
        return 3

    if not args.sin_escribir and filas:
        DATOS.mkdir(parents=True, exist_ok=True)
        cab = ("# LECTOR DE INVARIANTES -- a_inv = sqrt(sqrt(F^2+G^2)+F)\n"
               "# NO ES EVIDENCIA DEL ARTICULO: verificacion de instrumento (misma clausula que S).\n"
               f"# UNIVERSO DECLARADO: FDTD malla xy {M.NX}x{M.NY} (12 lambda_L, dx = lambda_L/40), "
               f"CFL_2D = {M.CFL_2D}, transito {M.TRANSITO_LAMBDA:.4f} lambda_L, "
               f"VENTANA DE MEDIDA = celdas [{M.VENTANA_I0},{M.VENTANA_I1}], unidad = a0; "
               "ventana temporal = todo el transito; motor numpy; unidad de conteo = celda.\n"
               "# TEMPORAL: a_inv_origen es el MAXIMO EN EL TIEMPO en el nodo focal [IC,JC]; "
               "a_inv_supremo es el maximo sobre tiempo Y ventana, con su celda.\n"
               f"# LECTURAS: naive = emparejamiento de indice igual (el de maxwell2d.invariante_a, "
               "que empareja E y H en la misma celda de una malla ESCALONADA) ; interpolado = B "
               "promediado a los nodos enteros de E (salvaguarda #1) ; "
               "interpolado_puntual = el interpolado evaluado en la celda e instante del pico de |E|.\n"
               f"# COTA DE MALLA MEDIDA (onda plana transversa, verdad a_inv = 0): naive "
               f"a_inv/|E| = sqrt(sin(k dx/2)) = {math.sqrt(DELTA):.6f} ; interpolado = "
               f"sin(k dx/2) = {DELTA:.6f}. Ninguna de las dos es 0: a_inv es raiz de una forma "
               "cuadratica y amplifica un error relativo O(delta^2) del campo a O(delta).\n"
               "# ANCLA: en el motor analitico a_inv(1) = 0 (Lemma 1) -> el cociente anclado a la "
               "medida a(1) es 0/0 para esta lectura; ancla no nula minima N = 2.\n"
               "# sim/medidas_aN.csv NO se toca (sha16 verificado antes y despues).\n"
               f"# PARES NO APLICABLES (declarados; ni medidos ni contados): "
               f"{no_aplicables if no_aplicables else 'ninguno'}.\n"
               "N,geometria,lectura,a_medido_a0,a_inv_origen_a0,a_inv_origen_sobre_amp_foco,"
               "a_inv_supremo_a0,a_inv_supremo_sobre_amp_pico,supremo_i,supremo_j,"
               "supremo_lambda_del_foco,F_supremo_J_m3,G_supremo_J_m3,supremo_t_fs,"
               "razon_maximos_cadencia20,E_en_supremo_a0,cociente_puntual_en_el_supremo,"
               "nan_extra\n")
        texto = cab + "\n".join(",".join(str(c) for c in f) for f in filas) + "\n"
        CSV.write_text(texto)
        CRUDO.write_text(json.dumps(crudo, indent=1, ensure_ascii=False) + "\n")
        print(f"\nescrito {CSV}  ({len(filas)} filas, {CSV.stat().st_size} B)")
        print(f"escrito {CRUDO}  ({CRUDO.stat().st_size} B)")
    elif args.sin_escribir:
        print("\n--sin-escribir: no se escribe ningun artefacto")

    print(f"\nsim/medidas_aN.csv sha16 despues = {sha_despues}  (intacto: {sha_despues == sha_antes})")
    print(f"tiempo total {time.time() - t0:.1f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
