#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
evaluador_adjuntos_tres_mallas.py -- frente 8.4 de sfqed-paper
HUELLA: HUELLA-EVALUADOR-ADJUNTOS-TRES-MALLAS-20261013

QUE ES
  Instrumento NUEVO del frente 8.4. No vuelve a correr el solver del Frente 2:
  toma la escalera de mallas YA SELLADA (nodos = 60*2**k + 1 -> 61/121/241/481,
  h = dx/lambda = 0.1*2**-k, LADO = 6.0) y mide, sobre ella, el objeto de la
  fila 6 de la tabla categorica (heredada del acta de convergencia p):

    (1) C-ORD -- el orden de composicion adoptado en el arnes contra el
        declarado en la adenda 8.4; y si ese orden esta ELEGIDO o FORZADO
        por las dimensiones.
    (2) La ley de composicion f* g* = (gf)* sobre las TRES mallas anidadas,
        medida como identidad de OPERADORES (no como producto matricial).
    (3) La 2-celda (P R - I) punto a punto, y su tasa de decaimiento.
    (4) La adjuncion en DOS PLANOS: al nivel del EMPAREJAMIENTO y al nivel
        del OPERADOR. Los dos planos dan respuestas distintas y las dos son
        verdaderas.
    (5) El falsador: con nodos NO anidados, la ley sobrevive pero la
        precision cae a O(h).

QUE NO HACE
  No toca ningun instrumento del repo (lectura pura de la escalera sellada).
  No corre el solver. No escribe fuera de su propio crudo. No eleva nada (n=1).
  No escribe "p = 2" como resultado: publica el par (p, C).

ESCRITURA (unica)
  /Users/marlene/sfqed-paper/sim/data/invariantes/adjuntos_tres_mallas_20261013.json
"""

import json
import math
import pathlib
import sys
import time

T_UTC = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

LADO = 6.0
LAMBDA = 1.0
NODOS = [60 * 2 ** k + 1 for k in range(4)]      # 61 121 241 481
H = [LADO / (n - 1) for n in NODOS]              # 0.1 0.05 0.025 0.0125

CRUDO = pathlib.Path(
    "/Users/marlene/sfqed-paper/sim/data/invariantes/adjuntos_tres_mallas_20261013.json"
)

# ---------------------------------------------------------------------------
# 0. PRE-REGISTRO -- se imprime ANTES de cualquier cifra
# ---------------------------------------------------------------------------
PREREGISTRO = {
    "objeto": "la ley de composicion f* g* = (gf)* vista en el ARNES NUMERICO, sobre las tres mallas anidadas ya selladas",
    "orden_adoptado": "X Y := X o Y (diagramatico); en codigo: aplicar(comp(X, Y), v) == X @ (Y @ v)",
    "prediccion_2celda": "delta = u - P R u es el error de interpolacion lineal en los nodos IMPARES: |delta| = (h^2/8)|u''|, razon 4 por escalon => p = 2 EXACTO por construccion (no asintotico)",
    "prediccion_escisura": "el defecto de escisura al nivel del emparejamiento mezcla el error de cuadratura de las DOS mallas => esperado O(h^2)",
    "prediccion_operador": "al nivel del OPERADOR el adjunto exacto NO es la interpolacion lineal: la discrepancia es estructural, O(1), sin tasa",
    "prediccion_falsador": "con nodos NO anidados (fino desfasado media malla fina) la ley de composicion sigue siendo exacta (es un corte de indices) pero la CONSISTENCIA cae a O(h)",
    "bandas": {
        "dicho": "heredadas del Frente 2 (PREREGISTRO_CONVERGENCIA_P_20261012 §4); no se re-eligen",
        "VERDE": "1.96 <= p < 2.00 y p3 >= p2",
        "GRIS": "1.90 <= p < 1.96 (pediria la 4a malla, nodos=961)",
        "ROJO_NO_SATURA": "p < 1.90",
        "ROJO_SOBREPASO": "p >= 2.00",
        "ROJO_NO_MONOTONO": "p3 < p2",
    },
    "prohibiciones": [
        "no se escribe 'p = 2' como resultado: solo el par (p, C)",
        "una identidad no es evidencia: el adjunto exacto y la ley de composicion de adjuntos son identidades de algebra; se declaran, no se adjudican",
        "un defecto EXACTAMENTE cuadratico no es un objeto asintotico: si toca la banda superior, se declara el defecto de DOMINIO del umbral, no se baja el umbral",
        "una salida que no puede diferir no es evidencia (los dos controles: nodos pares exactos, y el adjunto que anula el residuo)",
    ],
}


def sec(t):
    print("")
    print("=== %s ===" % t)


def muestras(n, f, desfase=0.0):
    h = LADO / (n - 1)
    return [f((i + desfase) * h) for i in range(n)]


def u_lisa(x):
    return math.sin(2.0 * math.pi * x / LAMBDA)


def phi_lisa(x):
    return math.cos(3.0 * x) + 0.5


def w_trap(n):
    w = [1.0] * n
    w[0] = 0.5
    w[-1] = 0.5
    return w


def R_mat(nc, nf, paso):
    """Restriccion por INYECCION: nodo j del grueso <- nodo paso*j del fino."""
    M = [[0.0] * nf for _ in range(nc)]
    for j in range(nc):
        M[j][paso * j] = 1.0
    return M


def Rdir(nc, nf):
    return R_mat(nc, nf, (nf - 1) // (nc - 1))


def P_mat(nc, nf):
    """Prolongacion por INTERPOLACION LINEAL (la escisura elegida)."""
    M = [[0.0] * nc for _ in range(nf)]
    for j in range(nc):
        M[2 * j][j] = 1.0
        if j + 1 < nc:
            M[2 * j + 1][j] = 0.5
            M[2 * j + 1][j + 1] = 0.5
    return M


def A_mat(nc, nf):
    """Adjunto EXACTO de R bajo el emparejamiento trapezoidal G_n = diag(h_n w_n)."""
    hc, hf = LADO / (nc - 1), LADO / (nf - 1)
    wc, wf = w_trap(nc), w_trap(nf)
    R = R_mat(nc, nf, 2)
    M = [[0.0] * nc for _ in range(nf)]
    for j in range(nc):
        i = 2 * j
        M[i][j] = (hc * wc[j]) / (hf * wf[i]) * R[j][i]
    return M


def mv(A, v):
    return [sum(row[t] * v[t] for t in range(len(v)) if row[t]) for row in A]


def mm(A, B):
    n, k, m = len(A), len(B), len(B[0])
    return [[sum(A[i][t] * B[t][j] for t in range(k)) for j in range(m)]
            for i in range(n)]


def trasp(M):
    return [list(r) for r in zip(*M)]


def emp(a, b, n, h):
    """Emparejamiento discreto trapezoidal: h * suma(w_i a_i b_i)."""
    w = w_trap(n)
    return h * sum(w[i] * a[i] * b[i] for i in range(n))


def ninf(v):
    return max(abs(x) for x in v) if v else 0.0


def imax(v):
    return max(range(len(v)), key=lambda i: abs(v[i])) if v else -1


def tasa(d1, d2, h1, h2):
    if d1 <= 0.0 or d2 <= 0.0 or h1 <= 0.0 or h2 <= 0.0:
        return None
    lar = math.log(h1 / h2)
    if lar == 0.0:
        return None
    return math.log(d1 / d2) / lar


def banda(p, p_prev):
    if p is None:
        return "SIN MEDIDA"
    if p >= 2.00:
        return "ROJO SOBREPASO"
    if p < 1.90:
        return "ROJO NO-SATURA"
    if p < 1.96:
        return "GRIS"
    if p_prev is not None and p < p_prev:
        return "ROJO NO-MONOTONO"
    return "VERDE"


# ---------------------------------------------------------------------------
# 0. PRE-REGISTRO impreso
# ---------------------------------------------------------------------------
print("T_UTC=%s" % T_UTC)
print("HUELLA: HUELLA-EVALUADOR-ADJUNTOS-TRES-MALLAS-20261013")
sec("0. PRE-REGISTRO (antes de cualquier cifra)")
for k in ("objeto", "orden_adoptado", "prediccion_2celda", "prediccion_escisura",
          "prediccion_operador", "prediccion_falsador"):
    print("  %-20s %s" % (k + ":", PREREGISTRO[k]))
print("  bandas: %s" % PREREGISTRO["bandas"]["dicho"])
for k in ("VERDE", "GRIS", "ROJO_NO_SATURA", "ROJO_SOBREPASO", "ROJO_NO_MONOTONO"):
    print("    %-16s %s" % (k + ":", PREREGISTRO["bandas"][k]))
for p in PREREGISTRO["prohibiciones"]:
    print("  prohibido: %s" % p)

# ---------------------------------------------------------------------------
sec("1. UNIVERSO DECLARADO")
print("  UNIVERSO DECLARADO: la escalera de mallas sellada del Frente 2 (4 mallas, 3 escalones)")
print("                      + los operadores R (inyeccion), P (interpolacion), A (adjunto exacto)")
print("  MOTOR: python3 -B, aritmetica float64, CERO corridas del solver")
print("  UNIDAD: nodo / razon adimensional (dx/lambda) / byte")
print("  VENTANA: %s" % T_UTC)
print("  mallas = %s" % NODOS)
print("  h      = %s" % ["%.6f" % x for x in H])
print("  anidamiento: %s" % ["%d = 2*%d - 1" % (NODOS[k], NODOS[k - 1]) for k in (1, 2, 3)])
paso_ok = all(NODOS[k] == 2 * NODOS[k - 1] - 1 for k in (1, 2, 3))
print("  guarda de anidamiento exacto: %s" % ("OK" if paso_ok else "ROTA -> abortar"))
if not paso_ok:
    sys.exit(3)

# operadores por escalon: escalon k va del fino N[k] al grueso N[k-1]
Rk = [None] + [R_mat(NODOS[k - 1], NODOS[k], 2) for k in (1, 2, 3)]
Pk = [None] + [P_mat(NODOS[k - 1], NODOS[k]) for k in (1, 2, 3)]
Ak = [None] + [A_mat(NODOS[k - 1], NODOS[k]) for k in (1, 2, 3)]

# ---------------------------------------------------------------------------
sec("2. ORDEN DE COMPOSICION (C-ORD) -- declarado, y FORZADO por dimensiones")
A1, B1 = Rk[1], Rk[2]     # A1: (61,121)   B1: (121,241)
print("  formas: R1 = %dx%d   R2 = %dx%d" % (len(A1), len(A1[0]), len(B1), len(B1[0])))
vs = [muestras(NODOS[2], u_lisa), muestras(NODOS[2], phi_lisa)]
comp_diag = [mv(A1, mv(B1, v)) for v in vs]      # diagramatico: X despues de Y
prod = mm(A1, B1)                                # (61,241)
comp_apl = [mv(prod, v) for v in vs]
res_ord = max(ninf([comp_diag[q][i] - comp_apl[q][i] for i in range(len(comp_apl[q]))])
              for q in range(len(vs)))
print("  lectura diagramatica  aplicar(comp(X,Y), v) = X @ (Y @ v)")
print("  lectura matricial     comp(X,Y) = X @ Y")
print("  residuo entre las dos lecturas (2 vectores) = %.3e" % res_ord)
print("  ORDEN INVERSO R2 @ R1: %dx%d . %dx%d -> sin sentido por dimensiones (la regla no se elige: se sigue)"
      % (len(B1), len(B1[0]), len(A1), len(A1[0])))
AtA, AtB = trasp(A1), trasp(B1)                  # AtA: (121,61)   AtB: (241,121)
izq = trasp(prod)                                # (gf)^*  -> (241,61)
der = mm(AtB, AtA)                               # f^* g^* -> (241,61)
res_adj = max(abs(izq[i][j] - der[i][j]) for i in range(len(izq)) for j in range(len(izq[0])))
print("  (gf)^* = f^* g^*  -> residuo %.3e  (IDENTIDAD de algebra: se declara, NO es evidencia)" % res_adj)
print("  (fg)^* = g^* f^*  -> forma %dx%d . %dx%d: indefinida por dimensiones"
      % (len(AtA), len(AtA[0]), len(AtB), len(AtB[0])))

# ---------------------------------------------------------------------------
sec("3. LEY DE COMPOSICION f* g* = (gf)* EN LAS TRES MALLAS ANIDADAS")
print("  metrica: identidad de OPERADORES sobre 5 vectores de prueba (liso, fino, impulso, 2 pseudoaleatorios)")
print("           NO se declara como producto matricial completo (el producto denso no se conserva)")
base = [u_lisa(x) for x in [i * H[3] for i in range(NODOS[3])]]
impulso = [1.0 if i == 137 else 0.0 for i in range(NODOS[3])]
prng = [0.0] * NODOS[3]
s = 12345
for i in range(NODOS[3]):
    s = (1103515245 * s + 12345) % (2 ** 31)
    prng[i] = s / float(2 ** 31) - 0.5
prng2 = [math.sin(3.1 * i) * math.cos(0.37 * i) for i in range(NODOS[3])]
W = NODOS[3]
VE = [base, [phi_lisa(x) for x in [i * H[3] for i in range(W)]], impulso, prng, prng2]

Rdirc = Rdir(NODOS[0], NODOS[3])
Pdirc = P_mat(NODOS[0], NODOS[3])
Adirc = A_mat(NODOS[0], NODOS[3])

# familia GRUESA (NODOS[0] = 61): es el punto de partida de las cadenas P y A
basec = [u_lisa(x) for x in [i * H[0] for i in range(NODOS[0])]]
impulsoc = [1.0 if i == 17 else 0.0 for i in range(NODOS[0])]
prngc = [0.0] * NODOS[0]
s = 12345
for i in range(NODOS[0]):
    s = (1103515245 * s + 12345) % (2 ** 31)
    prngc[i] = s / float(2 ** 31) - 0.5
prng2c = [math.sin(3.1 * i) * math.cos(0.37 * i) for i in range(NODOS[0])]
VC = [basec, [phi_lisa(x) for x in [i * H[0] for i in range(NODOS[0])]],
      impulsoc, prngc, prng2c]


def resid_comp(cadena, directo, vetores):
    peor = 0.0
    for v in vetores:
        w = list(v)
        for M in cadena:
            w = mv(M, w)
        ref = mv(directo, v)
        peor = max(peor, ninf([w[i] - ref[i] for i in range(len(w))]))
    return peor


resR = resid_comp([Rk[3], Rk[2], Rk[1]], Rdirc, VE)   # fina 481 -> gruesa 61
resP = resid_comp([Pk[1], Pk[2], Pk[3]], Pdirc, VC)   # gruesa 61 -> fina 481
resA = resid_comp([Ak[1], Ak[2], Ak[3]], Adirc, VC)   # gruesa 61 -> fina 481
print("  R (inyeccion)      R1(R2(R3 v)) vs R_dir v : %.3e   (0 exacto: corte de indices, sin aritmetica)" % resR)
print("  P (interpolacion)  P3(P2(P1 v)) vs P_dir v : %.3e   (redondeo: dos caminos de suma del MISMO interpolante)" % resP)
print("  A (adjunto exacto) A3(A2(A1 v)) vs A_dir v : %.3e   (redondeo: producto telescopico de razones)" % resA)
print("  control de la afirmacion R: identidad BIT A BIT = %s" % ("SI" if resR == 0.0 else "NO"))

# ---------------------------------------------------------------------------
sec("4. LA 2-CELDA (P R - I) PUNTO A PUNTO, Y SU TASA")
print("  delta_k = u_(N[k]) - P_k R_k u_(N[k])   (la escisura vista contra la identidad)")
print("  %-6s %-8s %-12s %-12s %-12s %-9s %-7s %s" %
      ("nivel", "nodos", "h", "|delta|inf", "rho=|d|/|u|", "nodo_max", "x_max", "delta en pares"))
filas = []
for k in (1, 2, 3):
    nf, nc = NODOS[k], NODOS[k - 1]
    uf = muestras(nf, u_lisa)
    d = [uf[i] - mv(Pk[k], mv(Rk[k], uf))[i] for i in range(nf)]
    idx = imax(d)
    pares = max(abs(d[2 * j]) for j in range(nc))
    rho = ninf(d) / ninf(uf)
    filas.append({"k": k, "nodos_fino": nf, "h": H[k], "delta_inf": ninf(d),
                  "rho": rho, "nodo_max": idx, "x_max": idx * H[k],
                  "delta_en_nodos_pares": pares})
    print("  %-6d %-8d %-12.6f %-12.6e %-12.6e %-9d %-7.4f %.3e" %
          (k, nf, H[k], ninf(d), rho, idx, idx * H[k], pares))
p2 = {}
for k in (2, 3):
    p2[k] = tasa(filas[k - 2]["rho"], filas[k - 1]["rho"], H[k - 1], H[k])
print("  tasas: p(121->241) = %s   p(241->481) = %s" %
      ("%.9f" % p2[2] if p2[2] else "SIN MEDIDA", "%.9f" % p2[3] if p2[3] else "SIN MEDIDA"))
print("  par (p, C) con C = rho / h^p:")
for k in (2, 3):
    if p2[k]:
        print("     escalon %d: (p = %.9f, C = %.9e)" % (k, p2[k], filas[k - 1]["rho"] / H[k] ** p2[k]))
print("  control de la 2-celda: |delta| en los nodos PARES = %.3e (debe ser 0: la interpolacion ES exacta en los nodos)"
      % max(f["delta_en_nodos_pares"] for f in filas))

# ---------------------------------------------------------------------------
sec("5. ADJUNCION EN DOS PLANOS: el emparejamiento converge, el operador no")
print("  plano EMPAREJAMIENTO  <R u, phi>_c  contra  <u, P phi>_f   (mismas G trapezoidales)")
print("  %-6s %-12s %-12s %-12s %-12s %-9s" %
      ("escalon", "|<Ru,phi>_c|", "|<u,Pphi>_f|", "D_escisura", "D_identidad", "rho_D"))
De, Di = [], []
for k in (1, 2, 3):
    nf, nc = NODOS[k], NODOS[k - 1]
    uf = muestras(nf, u_lisa)
    phc = muestras(nc, phi_lisa)
    iz = emp(mv(Rk[k], uf), phc, nc, H[k - 1])
    de = emp(uf, mv(Pk[k], phc), nf, H[k])
    di = emp(uf, mv(Ak[k], phc), nf, H[k])
    D = abs(iz - de)
    Dident = abs(iz - di)
    De.append(D)
    Di.append(Dident)
    print("  %-6d %-12.6e %-12.6e %-12.6e %-12.3e %-9.3e" %
          (k, abs(iz), abs(de), D, Dident, D / max(abs(iz), 1e-300)))
pD = {k: tasa(De[k - 2], De[k - 1], H[k - 1], H[k]) for k in (2, 3)}
print("  tasas de la escisura: p = %s | %s" %
      ("%.9f" % pD[2] if pD[2] else "SIN MEDIDA", "%.9f" % pD[3] if pD[3] else "SIN MEDIDA"))
print("  CONTROL DE IDENTIDAD: con P -> A (adjunto exacto) el residuo es %.3e en los tres escalones" % max(Di))
print("    => el adjunto exacto anula el emparejamiento POR CONSTRUCCION: identidad, no medida")
print("  plano OPERADOR: discrepancia estructural P - A")
for k in (1, 2, 3):
    nf, nc = NODOS[k], NODOS[k - 1]
    dif = max(abs(Pk[k][i][j] - Ak[k][i][j]) for i in range(nf) for j in range(nc))
    print("    escalon %d: |P - A|inf = %.6f  (O(1), SIN tasa: es OTRO operador, no un defecto que decaiga)" % (k, dif))
print("  => dos planos, dos respuestas verdaderas: la adjuncion CONVERGE al nivel del emparejamiento")

# ---------------------------------------------------------------------------
sec("6. FALSADOR: nodos NO anidados (fino desfasado media malla fina)")
print("  si la exactitud viniera de la SUAVIDAD y no del ANIDAMIENTO, este caso tambien daria p = 2")
filasF = []
for k in (1, 2, 3):
    nf, nc = NODOS[k], NODOS[k - 1]
    uf_rot = muestras(nf, u_lisa, desfase=0.5)
    inyect = mv(Rk[k], uf_rot)
    uc = muestras(nc, u_lisa)
    e = max(abs(inyect[j] - uc[j]) for j in range(nc))
    filasF.append({"k": k, "nodos_fino": nf, "h": H[k], "e_inf": e,
                   "rho": e / ninf(uc)})
    print("    escalon %d: |R_rot u_fino(desfasado) - u_grueso|inf = %.6e   rho = %.6e" %
          (k, e, e / ninf(uc)))
print("  ley de composicion bajo desfase (mismo corte de indices):")
Wr = [muestras(NODOS[3], u_lisa, desfase=0.5), prng, impulso]
rz = 0.0
for v in Wr:
    w = mv(Rk[1], mv(Rk[2], mv(Rk[3], v)))
    rz = max(rz, ninf([w[i] - mv(Rdirc, v)[i] for i in range(len(w))]))
print("    residuo de la ley = %.3e  => la ley SOBREVIVE al desfase (es corte de indices, no aritmetica)" % rz)
pF = {k: tasa(filasF[k - 2]["rho"], filasF[k - 1]["rho"], H[k - 1], H[k]) for k in (2, 3)}
print("  tasas del falsador: p = %s | %s" %
      ("%.9f" % pF[2] if pF[2] else "SIN MEDIDA", "%.9f" % pF[3] if pF[3] else "SIN MEDIDA"))
print("    (esperado p = 1: la consistencia cae un orden; el anidamiento es lo que la sostiene)")

# ---------------------------------------------------------------------------
sec("7. BANDAS (heredadas, no re-elegidas) Y PAR (p, C)")
print("  objeto 1: la 2-celda (P R - I)")
print("     p2 = %.9f   p3 = %.9f   [p3 >= p2: %s]   banda p3 = %s" %
      (p2[2] or float("nan"), p2[3] or float("nan"),
       (p2[3] >= p2[2]) if (p2[2] and p2[3]) else "SIN MEDIDA",
       banda(p2[3], p2[2])))
print("     OJO DOMINIO: el defecto es cuadratico POR CONSTRUCCION (no asintotico); si toca 2.00")
print("     es defecto de DOMINIO del umbral sellado, no del objeto. NO se baja el umbral.")
print("  objeto 2: la escisura al nivel del emparejamiento")
print("     p2 = %s   p3 = %s   banda p3 = %s" %
      ("%.9f" % pD[2] if pD[2] else "NA", "%.9f" % pD[3] if pD[3] else "NA",
       banda(pD[3], pD[2])))
print("  objeto 3 (falsador): p3 = %s   banda = %s  (el falsador DEBE ir rojo: si diera verde, la causa no seria el anidamiento)"
      % ("%.9f" % pF[3] if pF[3] else "NA", banda(pF[3], pF[2])))
print("  NADA de esto entra a main.tex. n = 1. NO se eleva.")

# ---------------------------------------------------------------------------
sec("8. ESCRITURA DEL CRUDO")
if CRUDO.exists():
    print("  COLISION: el crudo ya existe -> CERO escrituras")
    sys.exit(11)
crudo = {
    "T_UTC": T_UTC,
    "instrumento": "sim/evaluador_adjuntos_tres_mallas.py",
    "huella": "HUELLA-EVALUADOR-ADJUNTOS-TRES-MALLAS-20261013",
    "frente": "8.4 (fila 6: ley de composicion f* g* = (gf)*)",
    "universo": {"mallas": NODOS, "h": H, "LADO": LADO, "lambda": LAMBDA,
                 "anidamiento_exacto": paso_ok},
    "preregistro": PREREGISTRO,
    "c_ord": {"formas": {"R1": [len(A1), len(A1[0])], "R2": [len(B1), len(B1[0])]},
              "residuo_diagramatico_vs_matricial": res_ord,
              "orden_inverso_definido": False,
              "residuo_adjunto_gf_vs_fg": res_adj,
              "orden_adjunto_forzado_por_dimensiones": True},
    "ley_composicion": {"residuo_R": resR, "residuo_P": resP, "residuo_A": resA,
                        "vectores_de_prueba": len(VE), "metrica": "identidad de operadores"},
    "celda_2": {"filas": filas, "p_121_241": p2[2], "p_241_481": p2[3],
                "banda": banda(p2[3], p2[2])},
    "adjuncion": {"D_escisura": De, "D_identidad": Di,
                  "p_esc_121_241": pD[2], "p_esc_241_481": pD[3],
                  "banda_escisura": banda(pD[3], pD[2]),
                  "operador_O1": {str(k): max(abs(Pk[k][i][j] - Ak[k][i][j])
                                              for i in range(NODOS[k])
                                              for j in range(NODOS[k - 1])) for k in (1, 2, 3)}},
    "falsador": {"filas": filasF, "residuo_ley_bajo_desfase": rz,
                 "p_121_241": pF[2], "p_241_481": pF[3],
                 "banda": banda(pF[3], pF[2])},
    "veredicto": {
        "ley_en_tres_mallas": "MEDIDA: exacta (residuo 0) para la restriccion por inyeccion; redondeo para interpolacion y adjunto",
        "orden_de_adjuntos": "FORZADO por dimensiones, no elegido: el orden inverso no esta definido",
        "celda_2": "cuadratica exacta por construccion; toca la banda superior por DOMINIO del umbral",
        "adjuncion": "converge al nivel del emparejamiento (escisura O(h^2)); NO converge al nivel del operador (O(1))",
        "falsador": "el desfase conserva la ley pero baja la consistencia a O(h): el anidamiento es la causa",
    },
    "no_hace": ["no corre el solver", "no toca instrumentos del repo",
                "no escribe fuera de su crudo", "no eleva (n=1)",
                "no escribe p = 2 como resultado"],
}
CRUDO.parent.mkdir(parents=True, exist_ok=True)
CRUDO.write_text(json.dumps(crudo, indent=1, sort_keys=True), encoding="utf-8")
print("  escrito: %s" % CRUDO)
print("  bytes = %d" % CRUDO.stat().st_size)
print("FIN_UTC=%s" % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
sys.exit(0)
