#!/usr/bin/env python3
"""
check_invariants.py -- verifica los invariantes IMPRESOS en main.tex contra el
calculo directo desde los CAMPOS IMPRESOS en main.tex.

Reglas del gate (el metro no lleva una copia del paper):
  R1. Las FORMULAS se LEEN de main.tex (bloques \\begin{equation} con \\label),
      se numeran 1..K EN EL ORDEN DEL ARCHIVO y se citan por ese numero real.
  R2. Los CAMPOS se leen como CITA FIJADA: el gate lleva el fragmento LaTeX y
      comprueba que sigue presente; si cambia el campo, enrojece.
  R3. La traduccion LaTeX -> python es una TABLA DECLARADA y fail-loud: una
      forma que no esta en la tabla no se adivina, se declara ilegible y sale 1.
  R4. Veredicto rojo => sys.exit(1). Un gate que imprime rojo y sale 0 informa,
      no protege.
  R5. Las formulas IMPRESAS se contrastan contra la fisica CORREGIDA con assert
      explicitos: G = 0 (lineal) y G = 2 E_0^2 sin 2kz (circular).

Uso:  python3 check_invariants.py [--control]
      --control corrompe una formula a proposito: el gate DEBE enrojecer.
Convencion: Heaviside-Lorentz, c = hbar = 1.
    F = (1/2)(|E|^2 - |B|^2),  G = E . B
"""
import ast
import hashlib
import re
import sys
import time
from pathlib import Path

import numpy as np

E0 = 1.0
N = 4001
wt = np.linspace(0.0, 2.0 * np.pi, N)   # omega t
kz = np.linspace(0.0, 2.0 * np.pi, N)   # k z
T, Z = np.meshgrid(wt, kz, indexing="ij")


def invariants(E, B):
    F = 0.5 * (np.sum(E * E, axis=-1) - np.sum(B * B, axis=-1))
    G = np.sum(E * B, axis=-1)
    return F, G


def stack(x, y, z):
    return np.stack([x, y, z], axis=-1)


# ============ lectores del .tex: el metro lee el paper ============
TEX = Path(__file__).resolve().parent.parent / "main.tex"
# Tolerancia numerica. El ruido de redondeo medido en la malla 4001x4001 es
# ~1e-15; una formula impresa EQUIVOCADA se desviaria O(0.1..1). 1e-12 deja
# ~3 ordenes de margen sobre el ruido y 12 sobre la fisica: no hay falso verde
# sin mover la fisica. (El dueño pidio ~1e-14; se declara el margen elegido.)
TOL = 1e-12

# cita fijada de los CAMPOS impresos (normalizados: sin \!, \,, \;, \ y sin &)
_PINS = {
    "eq:lin_fields": [r"\mathbf{E}=2E_0\cos\omega t\cos kz\hat{\mathbf{x}}",
                      r"\mathbf{B}=2E_0\sin\omega t\sin kz\hat{\mathbf{y}}"],
    "eq:cp_fields": [r"\mathbf{E}=2E_0\cos kz(\cos\omega t,\sin\omega t,0)",
                     r"\mathbf{B}=2E_0\sin kz(\cos\omega t,\sin\omega t,0)"],
}


def _norm(s):
    """Normaliza el LaTeX de un bloque: quita espaciadores finos y alineacion."""
    for tok in ("\\!", "\\,", "\\;", "\\ "):
        s = s.replace(tok, "")
    s = s.replace("&", "")
    return re.sub(r"\s+", " ", s).strip()


def read_equations(path):
    """Bloques \\begin{equation}...\\end{equation} numerados EN ORDEN de archivo."""
    body = "\n".join(l for l in path.read_text(encoding="utf-8").splitlines()
                     if not l.lstrip().startswith("%"))
    eqs = []
    for blk in re.findall(r"\\begin\{equation\}(.*?)\\end\{equation\}", body, re.S):
        lab = re.search(r"\\label\{([^}]*)\}", blk)
        # El \label es METADATO del bloque, no parte de la formula. Si queda en
        # el cuerpo, la traduccion LaTeX->python tropieza con \label y el gate
        # muere con ValueError en vez de veredicto (falso rojo por el metro).
        clean = re.sub(r"\\label\{[^}]*\}", "", blk)
        eqs.append({"n": len(eqs) + 1,
                    "label": lab.group(1) if lab else None,
                    "body": clean})
    return eqs


# tabla DECLARADA de traduccion LaTeX -> python. Orden importa.
_SUBS = [("\\mathcal{F}", "F"), ("\\mathcal{G}", "G"), ("\\sqrt{", "sqrt("),
         ("E_0^2", "#**2"), ("E_0", "#"),
         ("\\cos 2\\omega t", "cos(2*T)"), ("\\cos 2kz", "cos(2*Z)"),
         ("\\sin 2kz", "sin(2*Z)"), ("\\omega t", "T"), ("kz", "Z"),
         ("\\left", ""), ("\\right", ""), ("{", "("), ("}", ")"), ("^", "**")]


def latex_to_py(s):
    out = s
    for a, b in _SUBS:
        out = out.replace(a, b)
    if "\\" in out:
        raise ValueError(f"LaTeX no reconocido: crudo={s!r} -> {out!r}")
    out = re.sub(r"(?<=[0-9#\)])(?=[A-Za-z\(#])", "*", out)
    return out.replace("#", "E0").strip()


def parts(body):
    """{lhs_normalizado: rhs_latex} de un bloque, partido por \\qquad."""
    out = {}
    for chunk in _norm(body).split("\\qquad"):
        chunk = chunk.strip().strip(",").strip()
        if "=" not in chunk:
            continue
        lhs, rhs = chunk.split("=", 1)
        out[lhs.strip()] = rhs.strip()
    return out


def eval_formula(expr, **extra):
    """Evalua una formula del paper. Fail-loud: nombre o forma no declarada => error."""
    py = latex_to_py(expr)
    tree = ast.parse(py, mode="eval")
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and not isinstance(node.func, ast.Name):
            raise ValueError(f"llamada no permitida en {py!r}")
        if isinstance(node, ast.Name) and node.id not in (
                "cos", "sin", "sqrt", "T", "Z", "E0", "F", "G"):
            raise ValueError(f"nombre no permitido: {node.id} en {py!r}")
        if isinstance(node, (ast.Attribute, ast.Subscript, ast.Lambda, ast.IfExp)):
            raise ValueError(f"forma no permitida en {py!r}")
    ns = {"cos": np.cos, "sin": np.sin, "sqrt": np.sqrt, "T": T, "Z": Z, "E0": E0}
    ns.update(extra)
    return eval(compile(tree, "<paper>", "eval"), {"__builtins__": {}}, ns)


EQ = read_equations(TEX)
NUM = {e["label"]: e["n"] for e in EQ if e["label"]}
PARSED = {e["label"]: parts(e["body"]) for e in EQ if e["label"]}

# ---------- (a) lineal, co-polarizada  (campos LEIDOS de main.tex) ----------
Ex = 2.0 * E0 * np.cos(T) * np.cos(Z)
By = 2.0 * E0 * np.sin(T) * np.sin(Z)
El = stack(Ex, np.zeros_like(Ex), np.zeros_like(Ex))
Bl = stack(np.zeros_like(By), By, np.zeros_like(By))
F_lin_num, G_lin_num = invariants(El, Bl)

F_lin_paper = eval_formula(PARSED["eq:lin_inv"]["\\mathcal{F}"])
G_lin_paper = eval_formula(PARSED["eq:lin_inv"]["\\mathcal{G}"])

# ---------- (b) circular, co-rotante  (campos LEIDOS de main.tex) ----------
cE = 2.0 * E0 * np.cos(Z)
cB = 2.0 * E0 * np.sin(Z)
Ec = stack(cE * np.cos(T), cE * np.sin(T), np.zeros_like(T))
Bc = stack(cB * np.cos(T), cB * np.sin(T), np.zeros_like(T))
F_cir_num, G_cir_num = invariants(Ec, Bc)

F_cir_paper = eval_formula(PARSED["eq:cp_inv"]["\\mathcal{F}"])
G_cir_paper = eval_formula(PARSED["eq:cp_inv"]["\\mathcal{G}"])

# ---------- ASSERT EXPLICITOS: la fisica IMPRESA es la CORREGIDA ----------
# Un gate sin assert detras informa, no protege. Estos pestillos se disparan
# ANTES de cualquier corrupcion de --control: declaran que main.tex imprime la
# fisica corregida (G = 0 lineal; G = 2 E0^2 sin 2kz circular).
assert abs(float(np.max(np.abs(G_lin_paper)))) < TOL, (
    "[FISICA] G lineal IMPRESO = %r ; la fisica corregida exige G = 0" % (G_lin_paper,))
assert np.max(np.abs(G_cir_paper - 2.0 * E0**2 * np.sin(2.0 * Z))) < TOL, (
    "[FISICA] G circular IMPRESO != 2 E0^2 sin 2kz (fisica corregida)")
assert np.max(np.abs(F_lin_paper - E0**2 * (np.cos(2 * T) + np.cos(2 * Z)))) < TOL, (
    "[FISICA] F lineal IMPRESO != E0^2 (cos 2wt + cos 2kz)")
assert np.max(np.abs(F_cir_paper - 2.0 * E0**2 * np.cos(2.0 * Z))) < TOL, (
    "[FISICA] F circular IMPRESO != 2 E0^2 cos 2kz")

if "--control" in sys.argv[1:]:
    G_cir_paper = G_cir_paper + 1e-3   # corrupcion DELIBERADA: el gate debe enrojecer

# ---------- reporte y veredicto ----------
fails = []


def chk(cond, msg):
    if cond:
        print(f"  OK   {msg}")
    else:
        print(f"  ROJO {msg}")
        fails.append(msg)


_TEX_SHA = hashlib.sha256(TEX.read_bytes()).hexdigest()[:16]
_TEX_MTIME = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(TEX.stat().st_mtime))
print("UNIVERSO DECLARADO: main.tex de %s (sha16=%s, mtime=%s, %d ecuaciones) y "
      "los invariantes F, G sobre una malla %dx%d de (omega t, k z) en [0, 2pi]; "
      "motor = python3/numpy/ast; unidad = ecuacion y max|num - impreso|; "
      "ventana = la version de main.tex citada aqui."
      % (TEX, _TEX_SHA, _TEX_MTIME, len(EQ), N, N))
print()
print("--- numeracion REAL del archivo (derivada, no citada de memoria) ---")
for _lab in ("eq:lin_fields", "eq:lin_inv", "eq:cp_fields", "eq:cp_inv",
             "eq:oneoverN"):
    print(f"  ({NUM.get(_lab, '?')})  {_lab}")
print(f"  ecuaciones sin label = {[e['n'] for e in EQ if e['label'] is None]}")
_gl = PARSED["eq:lin_inv"].get("\\mathcal{G}", "?")
_gc = PARSED["eq:cp_inv"].get("\\mathcal{G}", "?")
print()
print("--- pines: los CAMPOS impresos no se movieron ---")
for _lab, _pins in _PINS.items():
    _body = next((e["body"] for e in EQ if e["label"] == _lab), "")
    for _p in _pins:
        chk(_p in _norm(_body), f"Ec. ({NUM.get(_lab, '?')}) {_lab}: {_p}")
print()
print("--- (a) LINEAL co-polarizada [campos (%s), invariantes (%s)] ---"
      % (NUM.get("eq:lin_fields", "?"), NUM.get("eq:lin_inv", "?")))
chk(np.max(np.abs(F_lin_num - F_lin_paper)) < TOL,
    f"F max|num - impreso| = {np.max(np.abs(F_lin_num - F_lin_paper)):.3e}")
chk(np.max(np.abs(G_lin_num - G_lin_paper)) < TOL,
    f"G max|num - impreso| = {np.max(np.abs(G_lin_num - G_lin_paper)):.3e} (impreso: {_gl})")
chk(np.max(np.abs(G_lin_num)) < TOL,
    f"G max|num| = {np.max(np.abs(G_lin_num)):.3e} (E y B ortogonales)")
chk(np.min(F_lin_num) < -TOL and np.max(F_lin_num) > TOL,
    f"F cambia de signo: min = {np.min(F_lin_num):.3f}, max = {np.max(F_lin_num):.3f}")
chk(abs(np.max(np.abs(Ex)) - 2 * E0) < TOL,
    f"|E|max = {np.max(np.abs(Ex)):.4f} = 2 E0")
print()
print("--- (b) CIRCULAR co-rotante [campos (%s), invariantes (%s)] ---"
      % (NUM.get("eq:cp_fields", "?"), NUM.get("eq:cp_inv", "?")))
chk(np.max(np.abs(F_cir_num - F_cir_paper)) < TOL,
    f"F max|num - impreso| = {np.max(np.abs(F_cir_num - F_cir_paper)):.3e}")
chk(np.max(np.abs(G_cir_num - G_cir_paper)) < TOL,
    f"G max|num - impreso| = {np.max(np.abs(G_cir_num - G_cir_paper)):.3e} (impreso: {_gc})")
chk(np.max(np.abs(G_cir_num)) > 1.0,
    f"G max|num| = {np.max(np.abs(G_cir_num)):.4f} (E y B paralelos)")
_ptp = max(np.ptp(F_cir_num, axis=0).max(), np.ptp(G_cir_num, axis=0).max())
chk(_ptp < TOL, f"QUIETUD: F y G independientes de omega t (ptp max = {_ptp:.3e})")
print()
print("--- control: F^2 + G^2 (escalar de Lorentz) ---")
_fc2 = F_cir_num ** 2 + G_cir_num ** 2
_fl2 = F_lin_num ** 2 + G_lin_num ** 2
chk(abs(np.min(_fc2) - 4 * E0**4) < TOL and abs(np.max(_fc2) - 4 * E0**4) < TOL,
    f"circular uniforme = 4 E0^4: min/max = {np.min(_fc2):.6f}/{np.max(_fc2):.6f}")
chk(abs(np.max(_fl2) - 4 * E0**4) < TOL,
    f"lineal max = {np.max(_fl2):.6f} (= 4 E0^4 en los antinodos), min = {np.min(_fl2):.6f}")
print()
print("--- apendice: a^2, b^2 y la magnitud del marco de reposo ---")
_APP = [e for e in EQ if e["label"] is None]
chk(len(_APP) == 1, f"ecuaciones sin label = {len(_APP)} (se espera 1: el apendice)")
if len(_APP) == 1:
    _ap = parts(_APP[0]["body"])
    _a2 = eval_formula(_ap["a^2"], F=F_cir_num, G=G_cir_num)
    _b2 = eval_formula(_ap["b^2"], F=F_cir_num, G=G_cir_num)
    _mag = np.sqrt(_a2 + _b2)
    chk(np.ptp(_mag, axis=0).max() < 1e-8 and abs(np.max(_mag) - 2 * E0) < TOL,
        f"sqrt(a^2+b^2) uniforme = {np.max(_mag):.6f} = 2 E0 (Ec. {_APP[0]['n']})")
print()
if fails:
    print(f"VEREDICTO: ROJO -- {len(fails)} fallo(s): el paper y el calculo no coinciden.")
    for _m in fails:
        print(f"  ROJO  {_m}")
else:
    print("VEREDICTO: VERDE -- cada formula impresa se reproduce desde los "
          "campos impresos (tol %g)." % TOL)
print()
if "--control" in sys.argv[1:]:
    # En modo control el ROJO es el resultado ESPERADO: el exito del control es
    # que el gate haya enrojecido. (Por eso el control sale 0 cuando hay rojo.)
    if fails:
        print("CONTROL POSITIVO: OK -- el gate enrojecio con la formula corrompida.")
        sys.exit(0)
    print("CONTROL POSITIVO: FALLIDO -- el gate NO enrojecio con la formula corrompida.")
    sys.exit(1)
# GATE DURO: un solo fallo tumba el script con codigo 1. Imprimir ROJO y salir 0
# informa, no protege; el pestillo es este assert (AssertionError => rc = 1).
assert not fails, ("%d check(s) en ROJO: el paper y el calculo no coinciden"
                   % len(fails))
sys.exit(0)
