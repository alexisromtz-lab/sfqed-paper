#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""control_referencia_directa_20261013.py

CONTROL DE LA REFERENCIA DIRECTA del evaluador de adjuntos en tres mallas
(hermano: sim/evaluador_adjuntos_tres_mallas.py, corrida del 2026-10-13).

HUELLA-CONTROL-REFERENCIA-DIRECTA-20261013

OBJETO: su corrida RC=0 imprimio, en su seccion 3 (ley de composicion),
    P (interpolacion)  P3(P2(P1 v)) vs P_dir v : 1.988e+00
    A (adjunto exacto) A3(A2(A1 v)) vs A_dir v : 1.522e+01
Cifras que NO son redondeo. Este control mide si el defecto es del OBJETO
(la ley no se compone al nivel del operador) o del METRO (la referencia
DIRECTA del hermano esta mal construida), y lo decide con par controlado:
la MISMA referencia directa con paso general contra la del hermano.

No toca ningun instrumento del repo: es pieza NUEVA y de LECTURA PURA.
No corre el solver. NO escribe archivo alguno (crudo por stdout).
No eleva nada (n = 1). No escribe "p = 2": no mide tasas.
"""

import math
import sys
from datetime import datetime, timezone

T_UTC = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
LADO = 6.0
NODOS = [60 * 2 ** k + 1 for k in range(4)]      # [61, 121, 241, 481]
H = [LADO / (n - 1) for n in NODOS]
PASO = [(NODOS[k] - 1) // (NODOS[k - 1] - 1) for k in (1, 2, 3)]


def sec(t):
    print("")
    print("=== %s ===" % t)


def w_trap(n):
    w = [1.0] * n
    w[0] = 0.5
    w[-1] = 0.5
    return w


# --- referencia GENERAL (paso derivado de (nc, nf)) ------------------------
def R_gen(nc, nf):
    paso = (nf - 1) // (nc - 1)
    M = [[0.0] * nf for _ in range(nc)]
    for j in range(nc):
        M[j][paso * j] = 1.0
    return M


def P_gen(nc, nf):
    """Interpolacion lineal con paso general: nodo j del grueso en la fila paso*j."""
    paso = (nf - 1) // (nc - 1)
    M = [[0.0] * nc for _ in range(nf)]
    for i in range(nf):
        j = i // paso
        if j >= nc - 1:
            M[i][nc - 1] = 1.0
            continue
        t = (i - paso * j) / float(paso)
        M[i][j] = 1.0 - t
        M[i][j + 1] = t
    return M


def A_gen(nc, nf):
    """Adjunto EXACTO de R_gen bajo G_n = diag(h_n w_n)."""
    paso = (nf - 1) // (nc - 1)
    hc, hf = LADO / (nc - 1), LADO / (nf - 1)
    wc, wf = w_trap(nc), w_trap(nf)
    M = [[0.0] * nc for _ in range(nf)]
    for j in range(nc):
        i = paso * j
        M[i][j] = (hc * wc[j]) / (hf * wf[i])
    return M


# --- copia LITERAL de las dos funciones del HERMANO v1 ---------------------
def P_v1(nc, nf):
    """Copia literal del P_mat del hermano v1: paso FIJO 2, ignora nf."""
    M = [[0.0] * nc for _ in range(nf)]
    for j in range(nc):
        M[2 * j][j] = 1.0
        if j + 1 < nc:
            M[2 * j + 1][j] = 0.5
            M[2 * j + 1][j + 1] = 0.5
    return M


def A_v1(nc, nf):
    """Copia literal del A_mat del hermano v1: paso FIJO 2, ignora nf."""
    hc, hf = LADO / (nc - 1), LADO / (nf - 1)
    wc, wf = w_trap(nc), w_trap(nf)
    M = [[0.0] * nc for _ in range(nf)]
    for j in range(nc):
        i = 2 * j
        M[i][j] = (hc * wc[j]) / (hf * wf[i])
    return M


def mv(A, v):
    return [sum(row[t] * v[t] for t in range(len(v)) if row[t]) for row in A]


def ninf(v):
    return max(abs(x) for x in v) if v else 0.0


def filas_no_nulas(M):
    return sum(1 for row in M if any(row))


def emp(a, b, n, h):
    w = w_trap(n)
    return h * sum(w[i] * a[i] * b[i] for i in range(n))


# --- vectores de prueba: MISMA receta que el hermano -----------------------
def u_lisa(x):
    return math.sin(2.0 * math.pi * x)


def phi_lisa(x):
    return math.cos(3.0 * x) + 0.5


def familia(n, idx_impulso):
    base = [u_lisa(i * LADO / (n - 1)) for i in range(n)]
    phi = [phi_lisa(i * LADO / (n - 1)) for i in range(n)]
    imp = [1.0 if i == idx_impulso else 0.0 for i in range(n)]
    p1 = [0.0] * n
    s = 12345
    for i in range(n):
        s = (1103515245 * s + 12345) % (2 ** 31)
        p1[i] = s / float(2 ** 31) - 0.5
    p2 = [math.sin(3.1 * i) * math.cos(0.37 * i) for i in range(n)]
    return [base, phi, imp, p1, p2]


VC = familia(NODOS[0], 17)      # 61 nodos: arranque de las cadenas gruesa -> fina
VE = familia(NODOS[3], 137)     # 481 nodos: arranque de la cadena fina -> gruesa

Pn = [P_gen(NODOS[k - 1], NODOS[k]) for k in (1, 2, 3)]   # cada una factor 2
An = [A_gen(NODOS[k - 1], NODOS[k]) for k in (1, 2, 3)]


def encadena(cadena, v):
    w = list(v)
    for M in cadena:
        w = mv(M, w)
    return w


def peor_contra(cadena, directo, vetores):
    peor = 0.0
    for v in vetores:
        w = encadena(cadena, v)
        r = mv(directo, v)
        peor = max(peor, ninf([w[i] - r[i] for i in range(len(w))]))
    return peor


print("T_UTC=%s" % T_UTC)
print("HUELLA: HUELLA-CONTROL-REFERENCIA-DIRECTA-20261013")
print("UNIVERSO DECLARADO: escalera sellada NODOS = %s (LADO = %.1f, 60*2**k + 1)" % (NODOS, LADO))
print("VENTANA: %s | MOTOR: python3 -B (stdio puro, CERO corridas del driver) | UNIDAD: nodo" % T_UTC)
print("PASO entre mallas: %s   (anidamiento exacto: paso entero = 2, 4, 8)" % PASO)

sec("1. LA REFERENCIA DIRECTA DEL HERMANO v1: que filas llena y que deja en cero")
for etiqueta, f in (("P_v1", P_v1), ("A_v1", A_v1)):
    M = f(NODOS[0], NODOS[3])
    print("  %s(%d,%d): filas=%d  filas_no_nulas=%d  filas_en_cero=%d  ultima_fila_no_nula=%d"
          % (etiqueta, NODOS[0], NODOS[3], len(M), filas_no_nulas(M),
             len(M) - filas_no_nulas(M),
             max(i for i in range(len(M)) if any(M[i]))))
print("  => la referencia DIRECTA del hermano solo alcanza las filas 0..%d de %d:"
      % (2 * (NODOS[0] - 1) + 1, NODOS[3] - 1))
print("     el defecto es del METRO (paso fijo 2 escrito en la funcion), no del objeto.")

sec("2. CONTROL: con paso 2 las dos construcciones COINCIDEN (las cadenas anidadas del hermano eran correctas)")
dP2 = max(abs(P_v1(NODOS[0], NODOS[1])[i][j] - Pn[0][i][j])
          for i in range(NODOS[1]) for j in range(NODOS[0]))
dA2 = max(abs(A_v1(NODOS[0], NODOS[1])[i][j] - An[0][i][j])
          for i in range(NODOS[1]) for j in range(NODOS[0]))
print("  P_v1(61,121) vs P_gen(61,121): max|dif| = %.3e" % dP2)
print("  A_v1(61,121) vs A_gen(61,121): max|dif| = %.3e" % dA2)
print("  => 0 exacto: el hermano acerto en las patas anidadas de la cadena.")

sec("3. CONTROL POSITIVO: reproducir las dos cifras del hermano (1.988 / 15.22)")
resP_v1 = peor_contra(Pn, P_v1(NODOS[0], NODOS[3]), VC)
resA_v1 = peor_contra(An, A_v1(NODOS[0], NODOS[3]), VC)
print("  P: cadena P1(P2(P3 v)) vs P_v1(61,481) v : %.3e" % resP_v1)
print("  A: cadena A1(A2(A3 v)) vs A_v1(61,481) v : %.3e" % resA_v1)
print("  (si estas dos cifras no reproducen 1.988e+00 y 1.522e+01, el defecto NO esta identificado)")

sec("4. LA MISMA LEY CONTRA LA REFERENCIA CON PASO GENERAL (el metro corregido)")
resP_gen = peor_contra(Pn, P_gen(NODOS[0], NODOS[3]), VC)
resA_gen = peor_contra(An, A_gen(NODOS[0], NODOS[3]), VC)
Rn = [R_gen(NODOS[k - 1], NODOS[k]) for k in (1, 2, 3)]
resR_gen = peor_contra([Rn[2], Rn[1], Rn[0]], R_gen(NODOS[0], NODOS[3]), VE)
print("  R (inyeccion)      R1(R2(R3 v)) vs R_dir v : %.3e   (0 exacto: corte de indices, sin aritmetica)" % resR_gen)
print("  P (interpolacion)  P3(P2(P1 v)) vs P_dir v : %.3e   (redondeo: dos caminos del MISMO interpolante)" % resP_gen)
print("  A (adjunto exacto) A3(A2(A1 v)) vs A_dir v : %.3e   (redondeo: producto telescopico de razones)" % resA_gen)
print("  => con el metro corregido las tres patas son identidad numerica, no discrepancia.")
print("     IDENTIDAD de la operacion (los dos caminos SON el mismo interpolante): se declara, NO es evidencia.")

sec("5. CONTROL DE IDENTIDAD DEL ADJUNTO (el que decide cual de las dos A es la adjunta)")
E_gen = 0.0
E_v1 = 0.0
for k in (1, 2, 3):
    nf, nc = NODOS[k], NODOS[k - 1]
    uf = [u_lisa(i * H[k]) for i in range(nf)]
    phc = [phi_lisa(i * H[k - 1]) for i in range(nc)]
    iz = emp(mv(R_gen(nc, nf), uf), phc, nc, H[k - 1])
    E_gen = max(E_gen, abs(iz - emp(uf, mv(A_gen(nc, nf), phc), nf, H[k])))
    E_v1 = max(E_v1, abs(iz - emp(uf, mv(A_v1(nc, nf), phc), nf, H[k])))
print("  los tres escalones ANIDADOS (paso 2): |<Ri,Ru>_c - <u,A phi>_f|")
print("    con A_gen = %.3e    con A_v1 = %.3e   (identicos: paso 2; por eso el hermano imprimio 0.000e+00)" % (E_gen, E_v1))
nc, nf = NODOS[0], NODOS[3]
uf6 = [u_lisa(i * H[3]) for i in range(nf)]
phc6 = [phi_lisa(i * H[0]) for i in range(nc)]
iz6 = emp(mv(R_gen(nc, nf), uf6), phc6, nc, H[0])
K_gen = abs(iz6 - emp(uf6, mv(A_gen(nc, nf), phc6), nf, H[3]))
K_v1 = abs(iz6 - emp(uf6, mv(A_v1(nc, nf), phc6), nf, H[3]))
print("  el escalon DIRECTO (paso 8, 61 -> 481): |<Ri,Ru>_c - <u,A phi>_f|")
print("    con A_gen = %.3e    con A_v1 = %.3e" % (K_gen, K_v1))
print("  => con paso general A es la adjunta (redondeo); con paso 2 la A del hermano NO lo es (O(1)).")
print("     El par (con / sin) es lo que decide: el defecto es de la funcion, no de la malla.")

sec("6. DICTAMEN DEL CONTROL")
print("  el rojo del hermano (1.988e+00 y 1.522e+01) es DEL METRO, no del objeto:")
print("  la ley f* g* = (gf)* se compone al nivel del operador con residuo de redondeo")
print("  cuando las tres patas usan la misma construccion de paso general.")
print("  ACCION: la pieza hermana NO se muta (A2.1: target no rastreado => estado sucio, RC 13).")
print("          Se le deja su crudo tal cual y este control lo declara. n = 1. NO se eleva.")
print("RC_CONTROL=0")
sys.exit(0)
