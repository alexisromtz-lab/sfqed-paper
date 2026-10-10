#!/usr/bin/env python3
"""
check_invariants.py -- verificación numérica de los invariantes de campo
de las Ecs. (11)-(15) de main.tex, ANTES de graficarlos.

Regla: el crudo manda. Si la fórmula impresa no coincide con el cálculo
directo desde los campos impresos, la fórmula es la que se corrige.

Convención: Heaviside-Lorentz, c = hbar = 1.
    F = (1/2)(|E|^2 - |B|^2)
    G = E . B
"""
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


# ---------- (a) lineal, co-polarizada  [Ec. (11)] ----------
Ex = 2.0 * E0 * np.cos(T) * np.cos(Z)
By = 2.0 * E0 * np.sin(T) * np.sin(Z)
El = stack(Ex, np.zeros_like(Ex), np.zeros_like(Ex))
Bl = stack(np.zeros_like(By), By, np.zeros_like(By))
F_lin_num, G_lin_num = invariants(El, Bl)

F_lin_paper = E0**2 * (np.cos(2 * T) + np.cos(2 * Z))
G_lin_paper = E0**2 * np.sin(2 * T) * np.sin(2 * Z)

# ---------- (b) circular, co-rotante  [Ec. (14)] ----------
cE = 2.0 * E0 * np.cos(Z)
cB = 2.0 * E0 * np.sin(Z)
Ec = stack(cE * np.cos(T), cE * np.sin(T), np.zeros_like(T))
Bc = stack(cB * np.cos(T), cB * np.sin(T), np.zeros_like(T))
F_cir_num, G_cir_num = invariants(Ec, Bc)

F_cir_paper = 2.0 * E0**2 * np.cos(2 * Z) * np.ones_like(T)
G_cir_paper = np.zeros_like(T)   # <-- lo que afirma la Ec. (15)

# ---------- reporte ----------
print("UNIVERSO DECLARADO: invariantes F y G evaluados en una malla de "
      f"{N}x{N} eventos (omega t, k z) en [0, 2pi], desde los CAMPOS "
      "impresos en las Ecs. (11) y (14) de main.tex; comparados contra las "
      "FORMULAS impresas en las Ecs. (12), (13) y (15).")
print()
print("--- (a) LINEAL co-polarizada ---")
print(f"  F  max|num - (12)| = {np.max(np.abs(F_lin_num - F_lin_paper)):.3e}")
print(f"  G  max|num - (13)| = {np.max(np.abs(G_lin_num - G_lin_paper)):.3e}")
print(f"  G  max|num|        = {np.max(np.abs(G_lin_num)):.3e}   "
      "(E y B ortogonales => G identicamente 0)")
print(f"  |E|max             = {np.max(np.abs(Ex)):.4f}  (2 E0 = {2*E0})")
print()
print("--- (b) CIRCULAR co-rotante ---")
print(f"  F  max|num - (15)| = {np.max(np.abs(F_cir_num - F_cir_paper)):.3e}")
print(f"  G  max|num - (15)| = {np.max(np.abs(G_cir_num - G_cir_paper)):.3e}")
print(f"  G  max|num - 2E0^2 sin2kz| = "
      f"{np.max(np.abs(G_cir_num - 2.0*E0**2*np.sin(2*Z))):.3e}")
print(f"  G  max|num|        = {np.max(np.abs(G_cir_num)):.4f}   "
      "(E y B PARALELOS => G =/= 0)")
# control de invariancia: F^2 + G^2 es escalar de Lorentz
print()
print("--- control: F^2 + G^2 (escalar de Lorentz) ---")
print(f"  circular  min/max = {np.min(F_cir_num**2+G_cir_num**2):.6f} / "
      f"{np.max(F_cir_num**2+G_cir_num**2):.6f}   (4 E0^4 = {4*E0**4})")
print(f"  lineal    min/max = {np.min(F_lin_num**2+G_lin_num**2):.6f} / "
      f"{np.max(F_lin_num**2+G_lin_num**2):.6f}")
print()
print("VEREDICTO: (a) F correcto, G en (13) NO;  (b) F correcto, G en (15) NO."
      if (np.max(np.abs(F_lin_num - F_lin_paper)) < 1e-9
          and np.max(np.abs(G_lin_num - G_lin_paper)) > 1e-6
          and np.max(np.abs(F_cir_num - F_cir_paper)) < 1e-9
          and np.max(np.abs(G_cir_num - G_cir_paper)) > 1e-6)
      else "VEREDICTO: revisar; el crudo no reproduce el patrón esperado.")
