#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sim/control_pareado_convergente.py -- CONTROL PAREADO ANALITICO (ventana C, 11-Oct-2026)

UNIVERSO DECLARADO: MOTOR = (a) el motor analitico EXACTO sim/field_solver.py + sim/params.py,
  caja de lado 6 lambda_L con `nodos` nodos por lado (3D cubica y 2D cuadrada), M_FASE = 32
  fases de omega t sobre un periodo, cintura W0 = 2 lambda_L, helice h = +1 ; (b) el SOLVER
  FDTD sim/maxwell2d.py (SOLO LECTURA, no se edita) con su lazo de la casa: CFL_2D, ventana
  [VENTANA_I0, VENTANA_I1] y cadencia DIAG_CADA = 20. MOTOR = python3 -B con numpy.
  UNIDAD = adimensional (a y |E| divididos por E_a0(1) = P.campo_de_a0(1.0)).
  VENTANA = reloj UTC impreso abajo. ESCRITURA: SOLO sim/data/invariantes/.
  sim/medidas_aN.csv es INTOCABLE (se verifica su sha16 antes y despues).

ETIQUETA: verificacion del INSTRUMENTO, NO evidencia del articulo (misma clausula que S).

PRE-REGISTRO (dictado del dueno, verbatim; se transcribe ANTES de calcular el primer numero):
  rama 1  "~0.08: El residuo de 0.744 es un artefacto geometrico derivado de muestrear un frente
          esferico/parabolico en una malla cartesiana ortogonal."
  rama 2  "~0.74: El valor refleja la estructura intrinseca del campo convergente, validando que
          el lector no introduce distorsion relevante."
  rama 3  "0.2 - 0.4: El exceso procede de la dinamica temporal del solver FDTD (transitorios del
          pulso o aproximacion de derivadas)."
  Las tres salidas quedan ETIQUETADAS antes del primer numero: impide el ajuste narrativo post-hoc.

TENSION DE LECTURA LLANA, DECLARADA (no adjudicada): la rama 1 llama "artefacto geometrico" al
  residuo de 0.744 y la rama 3 llama "exceso ... dinamica temporal" a un valor MENOR (0.2-0.4).
  Leidas llanamente, rama 1 y rama 3 se cruzan. Se transcriben verbatim y el veredicto se emite
  POR NUMERO de rama, citando la etiqueta del dueno tal cual (regla de dictado: al interpretar se
  corrige el oido Y SE DECLARA que se corrigio; no se cita el error como si fuera el objeto).

LO QUE ESTE ARCHIVO AGREGA, Y POR QUE (declarado):
  (A) El control que decide rama 1 vs rama 2 no es "proyectar sobre Yee": es medir la razon
      R = max_{malla,t} a / max_{malla,t} |E| con el campo EXACTO del motor analitico, donde NO HAY
      MALLA YEE, NI FDTD, NI PULSO.  Si R ya vale ~0.74 SIN malla, la malla no puede ser su causa.
      Se mide ADEMAS la dependencia con la malla (lambda/10 y lambda/20) para separar "artefacto de
      muestreo" (debe DESAPARECER al refinar) de "estructura intrinseca" (debe CONVERGER a un
      valor no nulo).
  (B) La proyeccion Yee que el dueno pidio se ejecuta DESPUES, y no sobre un objeto distinto: se
      muestrea ESE MISMO campo analitico 2D en las POSICIONES YEE reales del solver.  El stencil
      real (deducido de sim/maxwell2d.py, funcion paso()) es el Yee 2D completo:
          Ez en (i,j)   Ex en (i+1/2,j)   Ey en (i,j+1/2)
          Hx en (i,j+1/2)   Hy en (i+1/2,j)   Hz en (i+1/2,j+1/2)
      y se lee con TRES lecturas: L1 naive (la de la casa), L2 interpolado (la del lector sellado)
      y L4 desestarcado COMPLETO (declarado aqui).
  (C) L4 SE MIDE PORQUE L2 NO ES UN DESESTARCADO COMPLETO.  Verificado por lectura del codigo
      sellado: lector_invariantes.py define B_a_nodos = (MU0*interp_y(Hx), MU0*interp_x(Hy),
      MU0*interp_x(Hz)) y NO toca E.  Contra la geometria Yee de arriba:  Bx (en y+1/2) SI se
      corrige, By (en x+1/2) SI se corrige, Bz (en x+1/2 y+1/2) se corrige SOLO en x, y los dos
      componentes de E que viven fuera del nodo (Ex en x+1/2, Ey en y+1/2) NO se corrigen.
      => L2 deja medio nodo en Bz, en Ex y en Ey.  NO se afirma que sea un defecto: se mide, y se
      declara el criterio (el invariante a(x) es funcion del campo de continuo, asi que una lectura
      co-ubicada exige desplazar LOS SEIS componentes a un punto comun).
  (D) El control sintetico del lector sellado (onda plana con k a lo largo de x) es CIEGO por
      construccion a ese medio nodo: con k en x, Hz no se desplaza en y y Ex no se desplaza en x.
      El control pareado 2D de este archivo si lo ve, porque los frentes son CURVOS/oblicuos.
      Se declara; NO se edita el lector sellado ni su sello.

NO SE RE-ETIQUETA NADA DEL INFORME SELLADO.  Este archivo es un INSTRUMENTO NUEVO y hermano.
"""

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

import field_solver as FS          # noqa: E402
import maxwell2d as M              # noqa: E402
import lector_invariantes as L     # noqa: E402  (SOLO LECTURA: el lector sellado)
import params as P                 # noqa: E402

DATOS = AQUI / "data" / "invariantes"
CRUDO = DATOS / "control_pareado_convergente.json"
MEDIDAS_A_N = AQUI / "medidas_aN.csv"          # INTOCABLE
CRUDO_SELLADO = DATOS / "crudo_lector_invariantes.json"   # SOLO LECTURA (el crudo sellado)

E_A0_1 = P.campo_de_a0(1.0)
LAMBDA = P.LAMBDA_L
LADO = 6.0                                     # lado de la caja, en lambda_L
W0 = P.W0
HELIC = +1.0
M_FASE = 32
FASES = tuple(2.0 * math.pi * m / M_FASE for m in range(M_FASE))
K_ANA = P.OMEGA / P.C

# ramas pre-registradas (el veredicto se emite POR NUMERO; la etiqueta se cita verbatim)
RAMAS = (
    (1, 0.02, 0.15, "rama 1 (~0.08): artefacto geometrico de muestrear el frente en malla "
                    "cartesiana ortogonal"),
    (2, 0.60, 0.90, "rama 2 (~0.74): estructura intrinseca del campo convergente; el lector no "
                    "introduce distorsion relevante"),
    (3, 0.15, 0.55, "rama 3 (0.2 - 0.4): exceso por la dinamica temporal del solver FDTD"),
)


def sha16(ruta) -> str:
    return hashlib.sha256(Path(ruta).read_bytes()).hexdigest()[:16]


def rama_de(R: float):
    """Mapea R a la rama por NUMERO.  Ojo: los intervalos 1 y 3 se SOLAPAN en [0.15,0.15]
    (declarado).  Se devuelve TODA rama cuyo intervalo contenga R, sin elegir."""
    return [r[0] for r in RAMAS if r[1] <= R <= r[2]]


def etiqueta_de(R: float):
    """Etiqueta del dueno (la del pre-registro) para toda rama que contenga R.  Verbatim."""
    return [r[3] for r in RAMAS if r[1] <= R <= r[2]]


# ==================================================================
# BLOQUE A -- razon INTRINSECA con el campo exacto del motor analitico (3D)
# ==================================================================
def razon_3d(familia, alpha_deg, n, nodos):
    """R = max_{malla,t} a / max_{malla,t} |E| del campo EXACTO.  Sin malla Yee, sin FDTD."""
    lista = FS.haces(familia, "circular", float(alpha_deg), int(n))
    Er, Br, centro = FS.campos(lista, E_A0_1, True, nodos)
    amax = 0.0
    emax = 0.0
    pun = {"F_rel": 0.0, "G_rel": 0.0, "cociente": 0.0}
    for th in FASES:
        c, s = math.cos(th), math.sin(th)
        E = [Er[k].real * c + Er[k].imag * s for k in range(3)]
        B = [Br[k].real * c + Br[k].imag * s for k in range(3)]
        a, Fq, Gq = L.invariante_adimensional(E[0], E[1], E[2], B[0], B[1], B[2])
        e2 = E[0] * E[0] + E[1] * E[1] + E[2] * E[2]
        em = float(np.sqrt(e2.max()))
        if em > emax:
            emax = em
        av = float(a.max())
        if av > amax:
            amax = av
            i = int(np.argmax(a))
            ep = float(math.sqrt(e2.flat[i]))
            pun = {"cociente": av / ep if ep else 0.0,
                   "F_rel": float(Fq.flat[i]) / (0.5 * ep * ep) if ep else 0.0,
                   "G_rel": float(Gq.flat[i]) / (ep * ep) if ep else 0.0}
    return {"R": amax / emax if emax else 0.0,
            "a_inv": amax / E_A0_1, "a_amp": emax / E_A0_1,
            "puntual_en_el_max_de_a": pun["cociente"],
            "F_rel_en_el_max_de_a": pun["F_rel"],
            "G_rel_en_el_max_de_a": pun["G_rel"]}


# ==================================================================
# BLOQUE B -- proyeccion Yee del mismo campo analitico (2D, geometria del solver)
# ==================================================================
def psis_2d(familia, alpha_deg, n):
    """Direcciones khat = (sin psi, cos psi) en el plano.  psi = 0 es +y."""
    a = math.radians(float(alpha_deg))
    out = []
    for k in range(int(n)):
        if familia == "copropagante":
            psi = 0.0
        elif familia == "cruce":                  # dos haces que se cruzan en 2*alpha
            psi = a if k % 2 == 0 else -a
        elif familia == "contra":                 # pares enfrentados
            psi = 0.0 if k % 2 == 0 else math.pi
        else:
            raise ValueError("familia 2D desconocida: " + familia)
        out.append(psi)
    return out


def abanico_2d(alpha_deg, m):
    """BLOQUE D.  Abanico CONVERGENTE DE UNA CARA: m direcciones repartidas en psi in [-a, +a]
    alrededor de +y, todas con el eje pasando por el foco comun.  Es el analogo 2D de un haz
    enfocado desde una cara (el frente parabolico del solver sellado).
    m = 2 -> psi = (+a, -a): reproduce la familia 'cruce' de BLOQUE B.  CONTROL CRUZADO."""
    a = math.radians(float(alpha_deg))
    m = int(m)
    if m < 2:
        raise ValueError("abanico_2d necesita m >= 2")
    return [-a + 2.0 * a * i / float(m - 1) for i in range(m)]


def par_enfrentado_2d(alpha_deg, m):
    """CONTROL SATURADO: m direcciones alrededor de +x y m alrededor de -x (contra-propagantes).
    Con m = 1 es el par enfrentado puro: R debe dar 1.000000 (se alcanza la cota |E|)."""
    a = math.radians(float(alpha_deg))
    m = int(m)
    ds = [0.0] if m == 1 else [-a + 2.0 * a * i / float(m - 1) for i in range(m)]
    return [0.5 * math.pi + d for d in ds] + [-0.5 * math.pi + d for d in ds]


def campo2d(psis, X, Y, e0):
    """Campo analitico EXACTO 2D en las coordenadas que se le pasen.

    eps = e_perp + i h zhat  (circular, helice h) ; B = khat x eps en unidades de E.
    Envolvente exp(-rho^2/W0^2) con rho = distancia PERPENDICULAR EN EL PLANO a la recta del
    haz que pasa por el foco.  Declarado: en 2D el solver tambien es invariante en z (su perfil
    g(j) es transversal y no hay coordenada ignorable en el campo), asi que la envolvente es la
    distancia en el plano, no la distancia 3D.
    """
    Er = [np.zeros_like(X, complex) for _ in range(3)]
    Br = [np.zeros_like(X, complex) for _ in range(3)]
    for psi in psis:
        kv = np.array([math.sin(psi), math.cos(psi), 0.0])
        ev = np.array([math.cos(psi), -math.sin(psi), 0.0]) + 1j * HELIC * np.array([0.0, 0.0, 1.0])
        bv = np.cross(kv, ev)
        kdot = kv[0] * X + kv[1] * Y
        rho = math.cos(psi) * X - math.sin(psi) * Y
        amp = e0 * np.exp(1j * K_ANA * kdot) * np.exp(-(rho / W0) ** 2)
        for c in range(3):
            Er[c] += amp * ev[c]
            Br[c] += amp * bv[c]
    return Er, Br


def malla_2d(nodos):
    h = LADO * LAMBDA / (nodos - 1)
    x = np.linspace(-LADO * LAMBDA / 2.0, LADO * LAMBDA / 2.0, nodos)
    X, Y = np.meshgrid(x, x, indexing="ij")
    return X, Y, h


def muestreo_yee(psis, nodos, e0):
    """Los SEIS componentes en sus posiciones Yee reales (ver docstring, punto B)."""
    X, Y, h = malla_2d(nodos)
    E0, B0 = campo2d(psis, X, Y, e0)              # (i, j)      -> Ez
    Ex_, Bx_ = campo2d(psis, X + h / 2.0, Y, e0)  # (i+1/2, j)  -> Ex, By
    Ey_, By_ = campo2d(psis, X, Y + h / 2.0, e0)  # (i, j+1/2)  -> Ey, Hx
    Ez_, Bz_ = campo2d(psis, X + h / 2.0, Y + h / 2.0, e0)   # (i+1/2, j+1/2) -> Hz
    return {"Ez": E0[2], "Ex": Ex_[0], "Ey": Ey_[1],
            "Bx": By_[0], "By": Bx_[1], "Bz": Bz_[2]}, h


def _lecturas2d(S, con_yee):
    """L1 naive (la casa) / L2 interpolado (el lector sellado) / L4 completo (declarado aqui)."""
    if not con_yee:
        uno = tuple(S[c] for c in ("Ex", "Ey", "Ez", "Bx", "By", "Bz"))
        return {"L0_exacto": uno}
    return {
        "L1_naive": (S["Ex"], S["Ey"], S["Ez"], S["Bx"], S["By"], S["Bz"]),
        "L2_lector": (S["Ex"], S["Ey"], S["Ez"],
                      L.interp_y(S["Bx"]), L.interp_x(S["By"]), L.interp_x(S["Bz"])),
        "L4_completo": (L.interp_x(S["Ex"]), L.interp_y(S["Ey"]), S["Ez"],
                        L.interp_y(S["Bx"]), L.interp_x(S["By"]),
                        L.interp_y(L.interp_x(S["Bz"]))),
    }


def razon_2d(psis, nodos, e0, con_yee=True):
    """Lee el campo en el interior declarado (se excluye la fila y la columna 0) y devuelve R
    por lectura, mas el detalle del maximo de a."""
    if con_yee:
        S, h = muestreo_yee(psis, nodos, e0)
    else:
        X, Y, h = malla_2d(nodos)
        E, B = campo2d(psis, X, Y, e0)
        S = {"Ex": E[0], "Ey": E[1], "Ez": E[2], "Bx": B[0], "By": B[1], "Bz": B[2]}
    lec = _lecturas2d(S, con_yee)
    INT = (slice(1, nodos), slice(1, nodos))
    salida = {}
    for nom, (ex, ey, ez, bx, by, bz) in lec.items():
        amax = 0.0
        emax = 0.0
        det = {}
        nan_extra = 0
        for th in FASES:
            c, s = math.cos(th), math.sin(th)
            f = [z.real * c + z.imag * s for z in (ex, ey, ez, bx, by, bz)]
            a, Fq, Gq = L.invariante_adimensional(*f)
            e2 = f[0] * f[0] + f[1] * f[1] + f[2] * f[2]
            nn = int(np.isnan(a).sum())
            # borde declarado de la interpolacion: fila 0 + columna 0 = 2*nodos - 1 celdas
            nan_extra = max(nan_extra, max(0, nn - (2 * nodos - 1)))
            em = float(np.sqrt(np.nanmax(e2[INT])))
            if em > emax:
                emax = em
            av = float(np.nanmax(a[INT]))
            if av > amax:
                amax = av
                i = int(np.nanargmax(np.where(np.isnan(a), -np.inf, a)))
                ep = float(math.sqrt(e2.flat[i]))
                det = {"cociente": av / ep if ep else 0.0,
                       "F_rel": float(Fq.flat[i]) / (0.5 * ep * ep) if ep else 0.0,
                       "G_rel": float(Gq.flat[i]) / (ep * ep) if ep else 0.0,
                       "ij": (int(i // nodos), int(i % nodos))}
        salida[nom] = {"R": amax / emax if emax else 0.0,
                       "a_inv": amax / E_A0_1, "a_amp": emax / E_A0_1,
                       "nan_extra_declarada": nan_extra, **det}
    salida["_malla"] = {"nodos": nodos, "dx_sobre_lambda": LADO / (nodos - 1),
                        "delta_kdx2_rad": math.pi * (LADO / (nodos - 1)) / 2.0}
    return salida


# ==================================================================
# BLOQUE C -- la CUARTA lectura sobre el campo FDTD sellado (lazo de la casa, sin editar nada)
# ==================================================================
def fdtd_lecturas(modo, n):
    cfl = M.CFL_2D
    pasos = int(round(M.TRANSITO_LAMBDA / (cfl * M.DX_OVER_LAMBDA)))
    dt = cfl * M.DX / P.C
    Fv = M.campos_vacios()
    masc = M.mascara_esponja()
    g, fases = M.perfiles()
    terminos, _ = M.terminos_de(modo, n, nulo=False)
    V0, V1 = M.VENTANA_I0, M.VENTANA_I1
    sl = (slice(V0, V1 + 1), slice(None))

    rel = {}
    inv = {}
    emax = 0.0
    for k in range(pasos):
        t = (k + 0.5) * dt
        M.inyectar(Fv, t, terminos, g, fases)
        M.paso(Fv, dt, masc)
        e = M.modulo_E(Fv)
        em = float(e[sl].max())
        if em > emax:
            emax = em
        if k % M.DIAG_CADA:
            continue
        Bx = M.MU0 * L.interp_y(Fv["Hx"])
        By = M.MU0 * L.interp_x(Fv["Hy"])
        Bz = M.MU0 * L.interp_x(Fv["Hz"])
        j = {
            "L1_naive": (Fv["Ex"], Fv["Ey"], Fv["Ez"],
                         M.MU0 * Fv["Hx"], M.MU0 * Fv["Hy"], M.MU0 * Fv["Hz"]),
            "L2_lector": (Fv["Ex"], Fv["Ey"], Fv["Ez"], Bx, By, Bz),
            "L4_completo": (L.interp_x(Fv["Ex"]), L.interp_y(Fv["Ey"]), Fv["Ez"],
                            Bx, By, M.MU0 * L.interp_y(L.interp_x(Fv["Hz"]))),
        }
        for nom, (ex, ey, ez, bx, by, bz) in j.items():
            a, _, _ = L.invariante(ex[sl], ey[sl], ez[sl], bx[sl], by[sl], bz[sl],
                                   P.EPS0, M.MU0)
            v = float(np.nanmax(a))
            prev = inv.get(nom, 0.0)
            if v > prev:
                inv[nom] = v
            if em > 0.0:
                rel[nom] = max(rel.get(nom, 0.0), v / em)
    return {"modo": modo, "N": n, "pasos": pasos, "E_max_V_m": emax,
            "a_medido_a0": P.a0_de_campo(emax),
            "rel_cadencia20": rel,
            "inv_cadencia20_sobre_Ea0": {k: v / E_A0_1 for k, v in inv.items()}}


# ==================================================================
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sin-escribir", action="store_true")
    ap.add_argument("--sin-fdtd", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()

    t0 = time.time()
    sha_antes = sha16(MEDIDAS_A_N)
    print("T_UTC = " + time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    print("UNIVERSO DECLARADO: motor analitico exacto (sim/field_solver.py + sim/params.py, "
          "caja %.1f lambda, %d fases) + SOLVER FDTD sim/maxwell2d.py SOLO LECTURA "
          "(ventana %d-%d, cadencia %d, CFL %s)" %
          (LADO, M_FASE, M.VENTANA_I0, M.VENTANA_I1, M.DIAG_CADA, M.CFL_2D))
    print("sha16 lector sellado = %s   field_solver = %s   maxwell2d = %s"
          % (sha16(AQUI / "lector_invariantes.py"), sha16(AQUI / "field_solver.py"),
             sha16(AQUI / "maxwell2d.py")))
    print("ETIQUETA: verificacion del INSTRUMENTO, NO evidencia del articulo.")
    for r in RAMAS:
        print("   PREREG rama %d  [%.2f, %.2f]  %s" % r)

    crudo = {"T_UTC": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
             "sha16": {"field_solver": sha16(AQUI / "field_solver.py"),
                       "maxwell2d": sha16(AQUI / "maxwell2d.py"),
                       "lector": sha16(AQUI / "lector_invariantes.py"),
                       "self": sha16(Path(__file__))},
             "preregistro": {"ramas": [{"n": r[0], "lo": r[1], "hi": r[2], "etiqueta": r[3]}
                                       for r in RAMAS],
                             "tension_llana": "rama 1 y rama 3 se cruzan (declarado)"},
             "bloque_A_3d": {}, "bloque_B_2d": {}, "bloque_C_fdtd": {},
             "bloque_D_2d_abanico": {}}

    # ---------------- BLOQUE A ----------------
    print("\n=== BLOQUE A: razon INTRINSECA con el campo EXACTO (sin malla Yee, sin FDTD) ===")
    print("  R = max a / max |E| ; se declara tambien el par (lambda_equiv de la rama 2)")
    casos3d = [("copropagante", 0.0, 4), ("coaxial_contra", 0.0, 4)]
    for al in (15.0, 20.0, 26.5651, 30.0, 35.0, 45.0):
        casos3d.append(("estrella", al, 4))
    print("  %-16s %8s %3s | %12s %10s %10s %10s %10s" %
          ("familia", "alpha", "N", "R", "a_inv", "a_amp", "F_rel*", "G_rel*"))
    for nodos in (61, 121):
        print("  -- nodos = %d  (dx = lambda/%.2f) --" % (nodos, LADO / (nodos - 1)))
        for fam, al, n in casos3d:
            r = razon_3d(fam, al, n, nodos)
            crudo["bloque_A_3d"].setdefault(fam, {}).setdefault(str(al),
                                                               {})[str(nodos)] = r
            print("  %-16s %8.4f %3d | %12.6f %10.4f %10.4f %10.5f %10.5f" %
                  (fam, al, n, r["R"], r["a_inv"], r["a_amp"],
                   r["F_rel_en_el_max_de_a"], r["G_rel_en_el_max_de_a"]))
            if a.verbose:
                print("        branche(s) por intervalo: %s" % rama_de(r["R"]))

    # ---------------- BLOQUE B ----------------
    print("\n=== BLOQUE B: proyeccion YEE del mismo campo analitico 2D + desestarcado ===")
    print("  L1 naive = la casa ; L2 = interpolacion del lector sellado ; L4 = completo (6 comp.)")
    print("  %-13s %8s %6s | %8s | %12s %12s %12s %12s | %8s" %
          ("familia", "alpha", "nodos", "dx/l", "R_intr(ref)", "R_L1", "R_L2", "R_L4",
           "R_L4/R_int"))
    casos2d = [("copropagante", 0.0, 2), ("cruce", 26.5651, 2), ("cruce", 30.0, 2),
               ("contra", 0.0, 2)]
    NODOS_FINO = 1201          # malla de referencia SIN Yee: dx = lambda/200
    for fam, al, n in casos2d:
        psis = psis_2d(fam, al, n)
        ri = razon_2d(psis, NODOS_FINO, E_A0_1, con_yee=False)["L0_exacto"]
        print("  %-13s %8.4f %6s | %8s | %12.6f %12s %12s %12s | %8s" %
              (fam, al, "ref", "1/200", ri["R"], "-", "-", "-", "-"))
        for nodos in (61, 121, 241):
            ry = razon_2d(psis, nodos, E_A0_1, con_yee=True)
            clave = "%s|%s|%d" % (fam, al, nodos)
            crudo["bloque_B_2d"][clave] = {
                "intrinseco_nodos_%d" % NODOS_FINO: ri,
                "yee": {k: v for k, v in ry.items()},
                "R4_sobre_R_intrinseco": (ry["L4_completo"]["R"] / ri["R"]
                                          if ri["R"] else None)}
            print("  %-13s %8.4f %6d | %8.4f | %12.6f %12.6f %12.6f %12.6f | %8.4f" %
                  (fam, al, nodos, LADO / (nodos - 1), ri["R"],
                   ry["L1_naive"]["R"], ry["L2_lector"]["R"], ry["L4_completo"]["R"],
                   ry["L4_completo"]["R"] / ri["R"] if ri["R"] else float("nan")))
        print("")
        if a.verbose:
            for nodos in (61, 121, 241):
                ry = crudo["bloque_B_2d"]["%s|%s|%d" % (fam, al, nodos)]["yee"]
                print("      nodos %d  na_extra L2 %d L4 %d  cociente L4 %s" %
                      (nodos, ry["L2_lector"]["nan_extra_declarada"],
                       ry["L4_completo"]["nan_extra_declarada"],
                       ry["L4_completo"].get("cociente")))

    # ---------------- BLOQUE C ----------------
    if not a.sin_fdtd:
        print("\n=== BLOQUE C: la 4a lectura sobre el campo FDTD sellado (2 patas) ===")
        print("  %-10s %3s | %14s | %12s %12s %12s" %
              ("modo", "N", "a_medido (a0)", "rel L1", "rel L2", "rel L4"))
        for modo, n in (("colineal", 1), ("contra", 2)):
            r = fdtd_lecturas(modo, n)
            crudo["bloque_C_fdtd"]["%s|%d" % (modo, n)] = r
            print("  %-10s %3d | %14.8f | %12.9f %12.9f %12.9f" %
                  (modo, n, r["a_medido_a0"], r["rel_cadencia20"].get("L1_naive", 0.0),
                   r["rel_cadencia20"].get("L2_lector", 0.0),
                   r["rel_cadencia20"].get("L4_completo", 0.0)))
            if a.verbose:
                print("      inv/E_a0: %s" % {k: round(v, 6) for k, v in
                                              r["inv_cadencia20_sobre_Ea0"].items()})

    # ---------------- BLOQUE D (POST-HOC, DECLARADO, ADITIVO) ----------------
    print("\n=== BLOQUE D (POST-HOC, DECLARADO, ADITIVO): analogo 2D de la geometria sellada ===")
    print("  El solver sellado es 2D (x-y) y su fuente es un FRENTE PARABOLICO: un haz que")
    print("  converge al foco desde UNA cara.  El analogo 2D es el ABANICO DE UNA CARA:")
    print("  psi in [-alpha, +alpha] alrededor de +y, m direcciones por el foco comun.")
    print("  m = 2 reproduce la familia 'cruce' de BLOQUE B -> CONTROL CRUZADO (R = sin alpha).")
    print("  El par contra-propagante se mide aparte como CONTROL SATURADO (cota |E|, R = 1).")
    print("  Se mide DESPUES de A/B/C y NO re-etiqueta nada.")
    print("  %-8s %4s %7s %8s | %12s"
          % ("alpha", "m", "nodos", "dx/l", "R_intr(malla 181)"))
    for al in (26.5651, 30.0):
        for m in (2, 3, 5, 9, 17):
            ri = razon_2d(abanico_2d(al, m), 181, E_A0_1, con_yee=False)["L0_exacto"]
            crudo["bloque_D_2d_abanico"]["abanico|%s|%d|181" % (al, m)] = ri
            print("  %-8.4f %4d %7d %8.4f | %12.6f"
                  % (al, m, 181, LADO / 180.0, ri["R"]))
    psis_s = abanico_2d(30.0, 17)
    ri_s = razon_2d(psis_s, 361, E_A0_1, con_yee=False)["L0_exacto"]
    crudo["bloque_D_2d_abanico"]["abanico|30.0|17|ref361"] = ri_s
    print("  ref  alpha=30.0000 m=17 nodos=361 (dx = lambda/60)  R_intr = %.6f" % ri_s["R"])
    print("  %-8s %4s %8s %8s | %12s %12s %12s | %10s"
          % ("alpha", "m", "nodos", "dx/l", "R_L1", "R_L2", "R_L4", "R_L4/R_0"))
    for nodos in (61, 121, 241):
        ry = razon_2d(psis_s, nodos, E_A0_1, con_yee=True)
        crudo["bloque_D_2d_abanico"]["abanico|30.0|17|yee%d" % nodos] = ry
        print("  %-8.4f %4d %8d %8.4f | %12.6f %12.6f %12.6f | %10.4f"
              % (30.0, 17, nodos, LADO / (nodos - 1), ry["L1_naive"]["R"],
                 ry["L2_lector"]["R"], ry["L4_completo"]["R"],
                 ry["L4_completo"]["R"] / ri_s["R"]))
    print("  -- CONTROL CRUZADO (m=2 vs 'cruce' de BLOQUE B) y CONTROL SATURADO (par) --")
    for al in (26.5651, 30.0):
        r2 = crudo["bloque_D_2d_abanico"]["abanico|%s|2|181" % al]["R"]
        print("     alpha=%-8.4f m=2 R_intr=%.6f   sin(alpha)=%.6f"
              % (al, r2, math.sin(math.radians(al))))
    for al in (26.5651, 30.0):
        rp = razon_2d(par_enfrentado_2d(al, 1), 181, E_A0_1, con_yee=False)["L0_exacto"]
        crudo["bloque_D_2d_abanico"]["par_enfrentado|%s|1|181" % al] = rp
        print("     alpha=%-8.4f par enfrentado puro R_intr=%.6f  (cota |E|)"
              % (al, rp["R"]))

    # ---------------- GATE VIVO contra el crudo sellado (solo lectura) ----------------
    print("\n=== GATE VIVO: BLOQUE C contra el crudo SELLADO (solo lectura) ===")
    sell = json.loads(CRUDO_SELLADO.read_text())
    porclave = {(c["modo"], int(c["N"])): c for c in sell["corridas"]}
    gate = {"sha16_crudo_sellado": sha16(CRUDO_SELLADO), "pares": {}}
    for modo, n in (("colineal", 1), ("contra", 2)):
        c = porclave.get((modo, n))
        m = crudo["bloque_C_fdtd"].get("%s|%d" % (modo, n))
        if c is None or m is None:
            print("  %-9s N=%d  NO COMPARABLE (falta una de las dos patas)" % (modo, n))
            continue
        fila = {}
        for etq, mio, sellado in (("L1_naive", m["rel_cadencia20"]["L1_naive"],
                                   c["a_inv_rel_al_pico_cadencia20"]),
                                  ("L2_lector", m["rel_cadencia20"]["L2_lector"],
                                   c["a_inv_rel_al_pico_cadencia20_interp"])):
            desvio = abs(mio - sellado)
            ok = desvio < 1e-12
            fila[etq] = {"mio": mio, "sellado": sellado, "desvio": desvio, "ok": ok}
            print("  %-9s N=%d %-9s mio %.16f  sellado %.16f  desvio %.2e  %s"
                  % (modo, n, etq, mio, sellado, desvio, "OK" if ok else "ROJO"))
        gate["pares"]["%s|%d" % (modo, n)] = fila
    crudo["gate_vivo"] = gate

    # ---------------- veredicto ----------------
    print("\n=== VEREDICTO (por NUMERO de rama; etiqueta del dueno citada verbatim) ===")
    for fam, al, n in (("estrella", 26.5651, 4), ("estrella", 30.0, 4)):
        R = crudo["bloque_A_3d"][fam][str(al)]["61"]["R"]
        R2 = crudo["bloque_A_3d"][fam][str(al)]["121"]["R"]
        print("  intrinseco %s alpha=%.4f : R(lam/10)=%.6f R(lam/20)=%.6f  -> rama(s) %s"
              % (fam, al, R, R2, rama_de(R2)))
    print("  derivada con la malla (lam/10 -> lam/20): %s" %
          {k: (crudo["bloque_A_3d"]["estrella"][k]["61"]["R"],
               crudo["bloque_A_3d"]["estrella"][k]["121"]["R"])
           for k in ("26.5651", "30.0")})
    print("  -- valor SELLADO del articulo (razon_cadencia20 del FDTD), por lectura --")
    for modo, n in (("colineal", 1), ("contra", 2)):
        m = crudo["bloque_C_fdtd"].get("%s|%d" % (modo, n))
        if not m:
            continue
        for etq in ("L1_naive", "L2_lector", "L4_completo"):
            v = m["rel_cadencia20"][etq]
            print("     %-9s N=%d %-12s = %.9f  -> rama(s) %s :: %s"
                  % (modo, n, etq, v, rama_de(v), etiqueta_de(v)))
    ri26 = crudo["bloque_A_3d"]["estrella"]["26.5651"]["121"]["R"]
    ri30 = crudo["bloque_A_3d"]["estrella"]["30.0"]["121"]["R"]
    for etq in ("L2_lector", "L4_completo"):
        v = crudo["bloque_C_fdtd"]["colineal|1"]["rel_cadencia20"][etq]
        al_eff = 26.5651 + (v - ri26) / (ri30 - ri26) * (30.0 - 26.5651)
        print("  alpha EFECTIVO del valor sellado con la lectura %-12s = %.4f grados"
              "  (interpolando el cono 3D entre 26.5651 y 30)" % (etq, al_eff))
    print("  -- BLOQUE D (post-hoc): abanico de una cara vs controles --")
    for al in (26.5651, 30.0):
        r2 = crudo["bloque_D_2d_abanico"].get("abanico|%s|2|181" % al, {}).get("R")
        r17 = crudo["bloque_D_2d_abanico"].get("abanico|%s|17|181" % al, {}).get("R")
        rp = crudo["bloque_D_2d_abanico"].get("par_enfrentado|%s|1|181" % al, {}).get("R")
        print("     alpha=%-8.4f m=2 R=%.6f  m=17 R=%.6f  par enfrentado R=%.6f"
              % (al, r2 if r2 is not None else float("nan"),
                 r17 if r17 is not None else float("nan"),
                 rp if rp is not None else float("nan")))

    sha_desp = sha16(MEDIDAS_A_N)
    print("\nsim/medidas_aN.csv sha16 antes %s  despues %s  (intacto: %s)"
          % (sha_antes, sha_desp, sha_antes == sha_desp))
    crudo["medidas_aN_intacto"] = (sha_antes == sha_desp)
    crudo["segundos"] = round(time.time() - t0, 1)

    if not a.sin_escribir:
        DATOS.mkdir(parents=True, exist_ok=True)
        CRUDO.write_text(json.dumps(crudo, indent=1, sort_keys=True, default=str))
        print("escrito %s (%d B)" % (CRUDO, CRUDO.stat().st_size))
    print("tiempo total %.1f s" % (time.time() - t0))
    return 3 if sha_antes != sha_desp else 0


if __name__ == "__main__":
    sys.exit(main())
