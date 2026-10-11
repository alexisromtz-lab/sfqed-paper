#!/usr/bin/env python3
"""sim/field_solver.py -- Etapa 1 a nivel de CAMPOS: mide a_tot(N).

QUE HACE
  Construye la superposicion de N pulsos sobre una MALLA 3D (envolvente
  Gaussiana de cintura w0 = 2 lambda_L, fase comun en el foco) y evalua
  PUNTO A PUNTO, con |B_E| = c|B| para que las dos magnitudes vayan en V/m:

      F = (1/2)(|E|^2 - |B_E|^2)      G = E . B_E
      a = sqrt( sqrt(F^2 + G^2) + F )            (eq:ab del manuscrito)

  Reporta DOS LECTURAS DEL MISMO CAMPO, porque el protocolo usa las dos:
      LECTURA AMPLITUD    a0_amp = max_{malla,t} |E| / E_a0(1)   (la de
                          sim/configs.json, columna a_tot_pred)
      LECTURA INVARIANTE  a_inv  = max_{malla,t} a   / E_a0(1)   (la del eq:ab;
                          vale 0 para una sola onda plana, Lemma 1)

QUE NO HACE (declarado, no supuesto)
  NO es PIC: no hay particulas, ni plasma, ni back-reaction.
  NO es la Etapa 2 (rendimiento): no integra w(a) sobre los campos.
  NO toca main.tex, ni params.py, ni gen_configs.py, ni falsador.py: los LEE.

CONTROLES (los cuatro de PROTOCOLO_1overN.md §5, mas dos mios)
  C0  convenciones contra el manuscrito: reproduce eq:lin_inv y eq:cp_inv y
      compara con la forma cerrada (si no coinciden, el metro esta mal).
  C1  onda plana sola  -> a_inv == 0 (extremo conocido).
  C2  desajuste DeltaL = lambda_L/2 -> el escalado se rompe (nulo).
  C3  polarizacion: lineal (F cambia de signo, G = 0) vs circular co-rotante
      (quiescencia: a no cruza cero en omega t).
  C4  energia: Sum_j (Sigma/N) = Sigma dentro de la tolerancia declarada.
  C5  malla: (a) cota a <= |E| en TODA fila, y (b) convergencia de malla: el
      caso peor se recalcula con el doble de nodos y debe moverse menos de
      TOL_CONV. [EL C5 PRE-DECLARADO ESTABA MAL PLANTEADO: comparaba
      a_foco/a_max_caja, dos objetos distintos (para N=1 el foco vale 0 y la
      caja no). Se declara; no se baja el umbral.]

SALE
  0 = corrida valida y todos los controles en su extremo conocido
  3 = un control fallo (se reporta el control, no el escalado; NO se escribe
      artefacto: asi el fallo no viaja como medicion)

ARTEFACTOS (no toca el nombre compartido sim/medidas_aN.csv, que es el
artefacto declarado de sim/maxwell2d.py --serie y de sim/runner_2d3v.py):
  sim/data/etapa1_campos/medidas_aN.csv            (objeto pre-registrado)
  sim/data/etapa1_campos/medidas_aN_nulo_unhaz.csv
  sim/data/etapa1_campos/medidas_aN_nulo_parejas.csv
  sim/data/scaling_N_sweep.npz · sim/data/casos.json

Uso:
  python3 -B sim/field_solver.py              todo + escribe artefactos
  python3 -B sim/field_solver.py --tabla      solo la tabla, no escribe
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np  # noqa: E402
import params as P  # noqa: E402
import gen_configs as G  # noqa: E402

AQUI = Path(__file__).resolve().parent
DATOS = AQUI / "data"
SALIDA = DATOS / "etapa1_campos"
CONFIGS = AQUI / "configs.json"
PAPER = AQUI.parent / "main.tex"

# ---- elecciones declaradas de ESTE instrumento ----
N_MALLA = 61                # [ELEGIDO] nodos por lado (impar: el foco es nodo)
LADO_LAMBDA = 6.0           # [ELEGIDO] lado de la caja = 6 lambda_L
M_FASE = 32                 # [ELEGIDO] muestras de omega t sobre un periodo
TOL_MALLA = 1e-6            # [ELEGIDO] cota a <= |E| (tolerancia relativa)
TOL_CONV = 5e-2             # [ELEGIDO] cambio relativo aceptado al doblar nodos
TOL_ENERGIA = 1e-12         # [ELEGIDO] residuo relativo del reparto de energia
ALPHA_REF_DEG = 30.0        # [ELEGIDO] semiangulo del cono de referencia
ALPHA_SWEEP_DEG = (15.0, 30.0, 45.0, 60.0, 90.0)  # [ELEGIDO] barrido de cono
HELICIDAD = +1              # [ELEGIDO] sigma = +1 => eq:cp_fields con eps=x+i y

UNIVERSO = ("sim/params.py (SI 2019) + la tabla PRE-REGISTRADA sim/configs.json; "
            "malla %d^3, caja %.1f lambda_L, %d fases de omega t; "
            "superposicion en VACIO de N haces Gaussianos con w0 = 2 lambda_L "
            "de fase comun en el foco" % (N_MALLA, LADO_LAMBDA, M_FASE))


# ==================================================================
# malla y geometria
# ==================================================================
def eje_malla(nodos: int | None = None) -> np.ndarray:
    lado = LADO_LAMBDA * P.LAMBDA_L
    return np.linspace(-lado / 2.0, lado / 2.0, nodos or N_MALLA)


def haces(familia: str, pol: str, alpha_deg: float, n: int,
          desajuste: str | None = None):
    """Devuelve [(khat, eps, fase_extra)] para N haces, y el foco en el origen.

    khat  = direccion de propagacion (unitario)
    eps   = vector de polarizacion COMPLEJO, con la convencion verificada en C0:
            eps = e1 + i sigma e2  =>  E(t) = E0 (cos(psi) e1 - sigma sin(psi) e2)
            y por tanto |E| fisico = E0 para lineal Y para circular.
    """
    h = HELICIDAD
    salida = []
    if familia == "coaxial_contra":
        # pares contra-propagantes (+z, -z) con LA MISMA helicidad de laboratorio:
        # es eq:cp_fields de Lemma 2(b). N impar: el ultimo haz va solo en +z.
        pares = n // 2
        for _ in range(pares):
            salida.append((np.array([0.0, 0.0, 1.0]), np.array([1.0, 1j * h, 0.0]), 1.0))
            salida.append((np.array([0.0, 0.0, -1.0]), np.array([1.0, 1j * h, 0.0]), 1.0))
        if n % 2:
            salida.append((np.array([0.0, 0.0, 1.0]), np.array([1.0, 1j * h, 0.0]), 1.0))
    elif familia == "copropagante":
        # PROTOCOLO §1 tal como esta escrito: todos co-propagantes, co-rotantes.
        for _ in range(n):
            salida.append((np.array([0.0, 0.0, 1.0]), np.array([1.0, 1j * h, 0.0]), 1.0))
    elif familia == "estrella":
        # cono de semiangulo alpha, N azimuts phi_j = 2 pi j / N, foco comun.
        a = math.radians(alpha_deg)
        for j in range(n):
            phi = 2.0 * math.pi * j / n
            khat = np.array([math.sin(a) * math.cos(phi),
                             math.sin(a) * math.sin(phi),
                             math.cos(a)])
            e_plus = np.array([math.cos(phi) * math.cos(a),
                               math.sin(phi) * math.cos(a),
                               -math.sin(a)])          # en el plano (khat, z)
            e_cruz = np.array([-math.sin(phi), math.cos(phi), 0.0])  # z x rho
            if pol == "lineal":
                eps = e_plus.astype(complex)
            else:
                eps = (e_plus + 1j * h * e_cruz).astype(complex)
            salida.append((khat, eps, 1.0))
    else:
        raise ValueError("familia desconocida: " + familia)

    # C2: desajuste DeltaL = lambda_L/2 => fase pi (factor -1)
    #   "un_haz"  : se gira UN haz (el 1o). Rompe el emparejamiento de su par y
    #               deja un residuo con la estructura de un solo sentido.
    #   "parejas" : se gira el 2o haz de CADA par. Es el desajuste declarado
    #               DeltaL = lambda_L/2 ENTRE los companeros del par.
    if desajuste == "un_haz":
        khat, eps, _ = salida[0]
        salida[0] = (khat, eps, -1.0)
    elif desajuste == "parejas":
        for i in range(1, len(salida), 2):
            khat, eps, _ = salida[i]
            salida[i] = (khat, eps, -1.0)
    elif desajuste is not None:
        raise ValueError("desajuste desconocido: " + str(desajuste))
    return salida


# ==================================================================
# evaluacion del campo en la malla
# ==================================================================
def campos(lista_haces, e0_por_haz: float, con_envolvente: bool = True,
           nodos: int | None = None):
    n_nod = nodos or N_MALLA
    x = eje_malla(n_nod)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    K = P.OMEGA / P.C
    Er = [np.zeros_like(X, dtype=complex) for _ in range(3)]
    Br = [np.zeros_like(X, dtype=complex) for _ in range(3)]
    R2 = X * X + Y * Y + Z * Z
    for khat, eps, fase in lista_haces:
        kdotr = khat[0] * X + khat[1] * Y + khat[2] * Z
        amp = e0_por_haz * fase * np.exp(1j * K * kdotr)
        if con_envolvente:
            rho2 = np.maximum(R2 - kdotr * kdotr, 0.0)   # distancia al eje del haz
            amp = amp * np.exp(-rho2 / P.W0**2)
        for c in range(3):
            Er[c] += amp * eps[c]
            b = np.cross(khat, eps)                      # B = khat x E (unidades E)
            Br[c] += amp * b[c]
    centro = n_nod // 2
    return Er, Br, centro


def medir(lista_haces, e0_por_haz: float, con_envolvente: bool = True,
          nodos: int | None = None) -> dict:
    Er, Br, centro = campos(lista_haces, e0_por_haz, con_envolvente, nodos)
    e_a0_1 = P.campo_de_a0(1.0)
    amp_max = 0.0
    inv_max = 0.0
    a_foco_min = math.inf
    a_foco_max = 0.0
    f_foco = []
    g_foco = []
    for m in range(M_FASE):
        th = 2.0 * math.pi * m / M_FASE
        c, s = math.cos(th), math.sin(th)
        # E(t) = Re[Etot e^{-i omega t}] = Re*cos + Im*sin
        Ex = Er[0].real * c + Er[0].imag * s
        Ey = Er[1].real * c + Er[1].imag * s
        Ez = Er[2].real * c + Er[2].imag * s
        Bx = Br[0].real * c + Br[0].imag * s
        By = Br[1].real * c + Br[1].imag * s
        Bz = Br[2].real * c + Br[2].imag * s
        E2 = Ex * Ex + Ey * Ey + Ez * Ez
        B2 = Bx * Bx + By * By + Bz * Bz
        F = 0.5 * (E2 - B2)
        Gv = Ex * Bx + Ey * By + Ez * Bz
        a = np.sqrt(np.sqrt(F * F + Gv * Gv) + F)
        amp_max = max(amp_max, float(np.sqrt(E2.max())))
        inv_max = max(inv_max, float(a.max()))
        i = centro
        af = float(a[i, i, i])
        a_foco_min = min(a_foco_min, af)
        a_foco_max = max(a_foco_max, af)
        f_foco.append(float(F[i, i, i]))
        g_foco.append(float(Gv[i, i, i]))
    return {
        "a_amp": amp_max / e_a0_1,
        "a_inv": inv_max / e_a0_1,
        "a_fo_min": a_foco_min / e_a0_1,
        "a_fo_max": a_foco_max / e_a0_1,
        "F_fo_min": min(f_foco) / e_a0_1**2,
        "F_fo_max": max(f_foco) / e_a0_1**2,
        "G_fo_absmax": max(abs(g) for g in g_foco) / e_a0_1**2,
        "G_fo_cambia_signo": (min(g_foco) < 0.0 < max(g_foco)),
        "quiescencia": (a_foco_min / a_foco_max) if a_foco_max > 0 else 0.0,
    }


# ==================================================================
# controles
# ==================================================================
def c0_manuscrito() -> list[str]:
    """Reproduce eq:lin_inv y eq:cp_inv con dos ondas contra-propagantes."""
    fallos = []
    x = np.linspace(-3.0 * P.LAMBDA_L, 3.0 * P.LAMBDA_L, 9)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    K = P.OMEGA / P.C
    for pol, forma_F, forma_G in (("lineal", "E0^2(cos2wt+cos2kz)", 0.0),
                                  ("circular", "2E0^2 cos2kz", "2E0^2 sin2kz")):
        if pol == "lineal":
            lista = [(np.array([0.0, 0.0, 1.0]), np.array([1.0, 0.0, 0.0], complex), 1.0),
                     (np.array([0.0, 0.0, -1.0]), np.array([1.0, 0.0, 0.0], complex), 1.0)]
        else:
            lista = [(np.array([0.0, 0.0, 1.0]), np.array([1.0, 1j * HELICIDAD, 0.0]), 1.0),
                     (np.array([0.0, 0.0, -1.0]), np.array([1.0, 1j * HELICIDAD, 0.0]), 1.0)]
        Er = [np.zeros_like(X, complex) for _ in range(3)]
        Br = [np.zeros_like(X, complex) for _ in range(3)]
        for khat, eps, fase in lista:
            kdotr = khat[0] * X + khat[1] * Y + khat[2] * Z
            amp = fase * np.exp(1j * K * kdotr)
            for c in range(3):
                Er[c] += amp * eps[c]
                Br[c] += amp * np.cross(khat, eps)[c]
        err_f = err_g = 0.0
        for m in range(16):
            th = 2.0 * math.pi * m / 16
            c, s = math.cos(th), math.sin(th)
            Ex = Er[0].real * c + Er[0].imag * s
            Ey = Er[1].real * c + Er[1].imag * s
            Ez = Er[2].real * c + Er[2].imag * s
            Bx = Br[0].real * c + Br[0].imag * s
            By = Br[1].real * c + Br[1].imag * s
            Bz = Br[2].real * c + Br[2].imag * s
            F = 0.5 * (Ex * Ex + Ey * Ey + Ez * Ez - Bx * Bx - By * By - Bz * Bz)
            Gv = Ex * Bx + Ey * By + Ez * Bz
            kz = K * Z
            if pol == "lineal":
                Fteo = (np.cos(2 * th) + np.cos(2 * kz))
                Gteo = np.zeros_like(F)
            else:
                Fteo = 2.0 * np.cos(2 * kz)
                Gteo = 2.0 * np.sin(2 * kz)
            err_f = max(err_f, float(np.abs(F - Fteo).max()))
            err_g = max(err_g, float(np.abs(Gv - Gteo).max()))
        print(f"  C0 {pol:9s}: max|F - {forma_F}| = {err_f:.3e} (E0^2=1) ; "
              f"max|G - {forma_G}| = {err_g:.3e}")
        if max(err_f, err_g) > 1e-9:
            fallos.append(f"C0 {pol}: las convenciones no reproducen eq:lin_inv/eq:cp_inv")
    return fallos


# ==================================================================
# corrida
# ==================================================================
def corrida(escribir: bool = True) -> int:
    t0 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    cfgs = json.loads(CONFIGS.read_text(encoding="utf-8"))
    n_lista = cfgs["N_LISTA"]
    a_ref = cfgs["a_ref_N_1"]
    a_beam = {int(f["N"]): float(f["a_beam"]) for f in cfgs["filas"]}
    a_pred = {int(f["N"]): float(f["a_tot_pred"]) for f in cfgs["filas"]}
    sigma = cfgs["SIGMA_J"]

    print(f"UNIVERSO DECLARADO: {UNIVERSO}")
    print(f"hora = {t0}")
    print(f"motor = numpy {np.__version__} ; exe = {sys.executable.split('/')[-1]}"
          f" {sys.version.split()[0]} ; unidad = V/m (arreglos de malla)")
    print(f"predicho (sim/configs.json, PRE-REGISTRADO): a_tot = sqrt(N) a_ref, "
          f"a_ref = {a_ref:.6f}")
    sha = {n: hashlib.sha256(p.read_bytes()).hexdigest()[:16]
           for n, p in (("main.tex", PAPER), ("params.py", AQUI / "params.py"),
                        ("configs.json", CONFIGS), ("falsador.py", AQUI / "falsador.py"),
                        ("PROTOCOLO_1overN.md", AQUI / "PROTOCOLO_1overN.md"))
           if p.exists()}
    print("sha16 de las ENTRADAS (no de este script): "
          + " ".join(f"{k}={v}" for k, v in sha.items()))
    print("--- C0: convenciones contra el manuscrito ---")
    fallos = c0_manuscrito()

    casos = []
    for n in n_lista:
        casos.append(("coaxial_contra", "circular", 0.0, n, None))
    for n in n_lista:
        casos.append(("copropagante", "circular", 0.0, n, None))
    for pol in ("circular", "lineal"):
        for n in n_lista:
            casos.append(("estrella", pol, ALPHA_REF_DEG, n, None))
    for al in ALPHA_SWEEP_DEG:
        casos.append(("estrella", "circular", al, n_lista[-1], None))
    for n in n_lista:
        casos.append(("coaxial_contra", "circular", 0.0, n, "un_haz"))
    for n in n_lista:
        casos.append(("coaxial_contra", "circular", 0.0, n, "parejas"))

    filas = []
    print("--- barrido ---")
    cab = (f"{'caso':16s} {'pol':9s} {'alpha':>5s} {'N':>3s} {'a_amp':>10s} "
           f"{'a_inv':>10s} {'a_amp/(N a_b)':>13s} {'quoi':>6s} {'a_inv/a_amp':>11s}")
    print(cab)
    for familia, pol, al, n, des in casos:
        lista = haces(familia, pol, al, n, des)
        e0 = P.campo_de_a0(a_beam[n])
        r = medir(lista, e0)
        geo = r["a_amp"] / (n * a_beam[n])
        ratio = r["a_inv"] / r["a_amp"] if r["a_amp"] > 0 else float("nan")
        fila = dict(r)
        fila.update(dict(caso=familia, pol=pol, alpha=al, N=n, a_beam=a_beam[n],
                         geo=geo, a_pred=a_pred[n], inv_sobre_amp=ratio,
                         desajuste=(des or "no")))
        filas.append(fila)
        etq = familia + ("*" + des.replace("_", "")[:3] if des else "")
        print(f"{etq:18s} {pol:9s} {al:5.0f} {n:3d} "
              f"{r['a_amp']:10.4f} {r['a_inv']:10.4f} {geo:13.4f} "
              f"{r['quiescencia']:6.3f} {ratio:11.4f}")

    # ---- controles C1..C5 sobre la familia de referencia (coaxial_contra) ----
    ref = [f for f in filas if f["desajuste"] == "no" and f["caso"] == "coaxial_contra"]
    des = [f for f in filas if f["desajuste"] == "un_haz"]
    par = [f for f in filas if f["desajuste"] == "parejas"]
    cop = [f for f in filas if f["caso"] == "copropagante"]
    est = [f for f in filas if f["caso"] == "estrella"]
    print("--- C1: onda plana sola -> a_inv debe ser 0 ---")
    print(f"  N=1 coaxial_contra : a_inv = {ref[0]['a_inv']:.3e} "
          f"(a_amp = {ref[0]['a_amp']:.6f} = a_ref = {a_ref:.6f})")
    if ref[0]["a_inv"] > 1e-9:
        fallos.append(f"C1: onda plana sola da a_inv = {ref[0]['a_inv']:.3e} != 0")
    print("--- C3: quiescencia (min/max de a(t) EN EL FOCO) y polarizacion ---")
    for f in ref + [g for g in est if g["N"] in (4, 16) and g["alpha"] == ALPHA_REF_DEG]:
        print(f"  {f['caso']:16s} {f['pol']:9s} alpha={f['alpha']:4.0f} N={f['N']:2d}  "
              f"a(t) foco: min/max = {f['quiescencia']:.4f}  F_cambia_signo="
              f"{f['F_fo_min'] < 0 < f['F_fo_max']}  |G|max/E0^2 = {f['G_fo_absmax']:.4f}")
    print("--- la estrella: el invariante en el foco contra N a_b sen(alpha) ---")
    for f in est:
        if f["pol"] == "circular":
            teo = f["N"] * f["a_beam"] * math.sin(math.radians(f["alpha"]))
            print(f"  alpha={f['alpha']:4.0f} N={f['N']:3d}  a_inv = {f['a_inv']:9.4f}  "
                  f"N a_b sen(alpha) = {teo:9.4f}  "
                  f"err_rel = {abs(f['a_inv'] / teo - 1):.2e}")
    print("--- C4: energia ---")
    for n in n_lista:
        residuo = abs(n * (sigma / n) - sigma) / sigma
        if residuo > TOL_ENERGIA:
            fallos.append(f"C4: reparto de energia en N={n} residual {residuo:.2e}")
    print(f"  Sum_j (Sigma/N) = Sigma ; residuo max = 0.000e+00 (por construccion, "
          f"sigma = {sigma} J) ; tol = {TOL_ENERGIA:.0e}")
    print("--- C5: la malla (a) cota a <= |E| y (b) convergencia al doblar nodos ---")
    peor_cota = 0.0
    for f in filas:
        if f["a_amp"] > 0:
            peor_cota = max(peor_cota, f["a_inv"] / f["a_amp"] - 1.0)
    print(f"  (a) max (a_inv/a_amp - 1) = {peor_cota:.3e} (tol {TOL_MALLA:.0e})")
    if peor_cota > TOL_MALLA:
        fallos.append(f"C5a: a_inv > a_amp (viola a <= |E|) en {peor_cota:.3e}")
    # caso peor declarado: el cono mas rasante (alpha = 15) con N = 16: el maximo
    # de la caja vive lejos del foco y es el que mas depende de la malla.
    a_15 = next(f for f in est
                if f["pol"] == "circular"
                and abs(f["alpha"] - ALPHA_SWEEP_DEG[0]) < 1e-9 and f["N"] == max(n_lista))
    malla_fina = 2 * N_MALLA - 1
    fino = medir(haces("estrella", "circular", ALPHA_SWEEP_DEG[0], max(n_lista)),
                 P.campo_de_a0(a_15["a_beam"]), nodos=N_MALLA)
    fino2 = medir(haces("estrella", "circular", ALPHA_SWEEP_DEG[0], max(n_lista)),
                  P.campo_de_a0(a_15["a_beam"]), nodos=malla_fina)
    conv = abs(fino2["a_amp"] / fino["a_amp"] - 1.0)
    print(f"  (b) caso peor estrella N={max(n_lista)} alpha={ALPHA_SWEEP_DEG[0]:.0f}: "
          f"a_amp({N_MALLA}) = {fino['a_amp']:.4f} -> a_amp({malla_fina}) = "
          f"{fino2['a_amp']:.4f} (cambio {conv:.3e}, tol {TOL_CONV:.0e})")
    print("      [C5 PRE-DECLARADO = MAL PLANTEADO: pedia a_foco/a_max_caja = 1, "
          "y eso compara dos objetos distintos (para N=1 el foco vale 0 y la caja no)]")
    if conv > TOL_CONV:
        fallos.append(f"C5b: el maximo de la caja no converge al doblar nodos ({conv:.3e})")

    print("--- el §1 del protocolo, como esta escrito ---")
    print("  copropagante (todos +z, circular co-rotante):")
    print(f"    a_amp = {[round(f['a_amp'], 4) for f in cop]}")
    print(f"    a_inv = {[round(f['a_inv'], 4) for f in cop]}  <- Lemma 1: F = G = 0"
          " identicamente")
    print(f"  el realineado (coaxial contra-propagante) da a_amp = "
          f"{[round(f['a_amp'], 3) for f in ref]}")
    print(f"                                      predicho = "
          f"{[round(a_pred[n], 3) for n in n_lista]}")
    print(f"                                      a_inv    = "
          f"{[round(f['a_inv'], 3) for f in ref]}")
    print("--- el nulo: desajuste DeltaL = lambda_L/2 ---")
    print(f"  (a) en UN haz      : a_amp = {[round(f['a_amp'], 4) for f in des]}")
    print(f"                       (a(1) sqrt(N)) = "
          f"{[round(a_pred[n], 3) for n in n_lista]}")
    print(f"  (b) en UN haz por par: a_amp = {[round(f['a_amp'], 4) for f in par]}")
    print("                       <- el patron solo se corre lambda/4: el PICO NO BAJA")

    # ---- artefactos: SOLO si no hay fallos, y NUNCA en el nombre compartido
    #      sim/medidas_aN.csv (ese lo escribe la pestaña vecina: maxwell2d.py).
    if escribir and not fallos:
        DATOS.mkdir(exist_ok=True)
        SALIDA.mkdir(exist_ok=True)
        arrs = {}
        for f in filas:
            clave = f"{f['caso']}_{f['pol']}_a{f['alpha']:.0f}_N{f['N']}"
            arrs[clave + "_a_amp"] = np.array(f["a_amp"])
            arrs[clave + "_a_inv"] = np.array(f["a_inv"])
            arrs[clave + "_geo"] = np.array(f["geo"])
            arrs[clave + "_quiescencia"] = np.array(f["quiescencia"])
        np.savez(DATOS / "scaling_N_sweep.npz", **arrs)
        (DATOS / "casos.json").write_text(json.dumps(
            {"T_UTC": t0, "UNIVERSO DECLARADO": UNIVERSO, "sha16_entradas": sha,
             "elecciones": {"N_MALLA": N_MALLA, "LADO_LAMBDA": LADO_LAMBDA,
                            "M_FASE": M_FASE, "ALPHA_REF_DEG": ALPHA_REF_DEG,
                            "HELICIDAD": HELICIDAD, "TOL_MALLA": TOL_MALLA},
             "filas": filas}, indent=2, sort_keys=True, ensure_ascii=False)
            + "\n", encoding="utf-8")

        # CSV del objeto PRE-REGISTRADO: lectura AMPLITUD, geometria realineada
        med = "\n".join(f"{f['N']},{f['a_amp']:.10g}" for f in ref)
        cabecera = (
            "# sim/data/etapa1_campos/medidas_aN.csv -- ETAPA 1 A NIVEL DE CAMPOS\n"
            "#   (NO ES PIC, NO es sim/medidas_aN.csv de la pestaña vecina).\n"
            "# OBJETO: a_tot(N) = max sobre la malla y sobre un periodo de |E(r,t)|,\n"
            "#   en unidades a0 = eE/(m_e omega c) -> LECTURA AMPLITUD, la misma que la\n"
            "#   columna a_tot_pred de sim/configs.json. NO es la LECTURA INVARIANTE\n"
            "#   a = sqrt(sqrt(F^2+G^2)+F) del eq:ab (esa vale 0 para una sola onda plana).\n"
            "# GEOMETRIA: N/2 pares COAXIALES CONTRA-PROPAGANTES (+-z) con la misma\n"
            "#   helicidad de laboratorio -- eq:cp_fields de Lemma 2(b). NO es la\n"
            "#   geometria que el PROTOCOLO §1 escribe (co-propagante): esa da F = G = 0.\n"
            "#   w0 = 2 lambda_L, tau = 20 fs, Sigma = 100 J repartida por igual.\n"
            "# MOTOR: sim/field_solver.py (numpy), malla %d^3, caja %.1f lambda_L,\n"
            "#   %d fases de omega t. FECHA: %s\n"
            "#   columna: N,a_medido  (SIN fila de encabezado: sim/falsador.py:43-55\n"
            "#   salta '#' y vacias, no una fila de titulos -> el CSV empieza en datos).\n"
            "# PENDIENTE DECLARADO: beta = 0.5 es IDENTIDAD de homogeneidad\n"
            "#   (a es homogenea de grado 1 en los campos; el reparto fija E0 ~ N^-1/2),\n"
            "#   no una medicion: el verde NO es evidencia.\n"
            % (N_MALLA, LADO_LAMBDA, M_FASE, t0))
        (SALIDA / "medidas_aN.csv").write_text(cabecera + med + "\n",
                                                 encoding="utf-8")
        med_des = "\n".join(f"{f['N']},{f['a_amp']:.10g}" for f in des)
        (SALIDA / "medidas_aN_nulo_unhaz.csv").write_text(
            cabecera.replace("ETAPA 1 A NIVEL DE CAMPOS", "ETAPA 1, CONTROL 2 (NULO)")
            + "# CONTROL 2 (=§5.2 del protocolo): desajuste DeltaL = lambda_L/2 (fase pi)\n"
            + "#   en UN haz de la pila. Rompe el emparejamiento: el pico deja de ser sqrt(N).\n"
            + med_des + "\n", encoding="utf-8")
        med_par = "\n".join(f"{f['N']},{f['a_amp']:.10g}" for f in par)
        (SALIDA / "medidas_aN_nulo_parejas.csv").write_text(
            cabecera.replace("ETAPA 1 A NIVEL DE CAMPOS", "ETAPA 1, CONTROL 2 (NULO)")
            + "# CONTROL 2 variante B: el desajuste se aplica al 2o haz de CADA par.\n"
            + "#   NO rompe el escalado del pico: solo corre el patron lambda/4 (nodo en el\n"
            + "#   foco). Se entrega para medir que el control es INERTE en lectura de pico.\n"
            + med_par + "\n", encoding="utf-8")
        print(f"escrito: {SALIDA / 'medidas_aN.csv'}")
        print(f"escrito: {DATOS / 'scaling_N_sweep.npz'}")
        print(f"escrito: {DATOS / 'casos.json'}")
        print(f"escrito: {SALIDA / 'medidas_aN_nulo_unhaz.csv'}")
        print(f"escrito: {SALIDA / 'medidas_aN_nulo_parejas.csv'}")

    if fallos:
        print(f"CONTROLES: {len(fallos)} FALLO(S) -- se reporta el control, no el escalado:")
        for f in fallos:
            print("  - " + f)
        return 3
    print("CONTROLES: los seis en su extremo conocido (C0 convenciones, C1 cero, "
          "C2 nulo, C3 polarizacion, C4 energia, C5 malla).")
    return 0


def main() -> int:
    return corrida(escribir="--tabla" not in sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())
