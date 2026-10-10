#!/usr/bin/env python3
"""
fig_invariants.py -- figura analitica de dos paneles para main.tex.

Panel (a): F(omega t) en el plano de campo fuerte kz = 0, para la colision
           lineal co-polarizada (campos + invariante) y la circular co-rotante
           (campos + invariante). Contrasta oscilatorio (cruza cero) vs
           quiescente.
Panel (b): escalado 1/N de la energia de entrada y el campo pico sqrt(N) a
           energia total fija.

Los numeros de ecuacion NO se escriben a mano: se derivan de ../main.tex
contando \begin{equation} en orden y cortando en \appendix, y el script aborta
si los labels esperados no estan o si dejan de ser consecutivos. Un numero a
mano caduca en silencio: la leyenda decia (12) y (15) cuando el texto ya decia
(11) y (13) (medido 2026-10-10T23:00Z, main.tex 455 l).

Dependencias: numpy, matplotlib. Nada mas.
Guarda fig_invariants.pdf (vectorial, para LaTeX) y .png (vista rapida).
"""
import pathlib
import re

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---- numeros de ecuacion derivados de la fuente de verdad (main.tex) ----
_HERE = pathlib.Path(__file__).resolve().parent
_MAIN = _HERE.parent / "main.tex"
_src = _MAIN.read_text(encoding="utf-8")
_src = re.sub(r"(?<!\\)%.*", "", _src)              # fuera comentarios
_corte = _src.find("\\appendix")                      # el apendice renumera A1...
_cuerpo = _src if _corte < 0 else _src[:_corte]
_num, _n = {}, 0
for _m in re.finditer(r"\\begin\{equation(\*)?\}(.*?)\\end\{equation\*?\}",
                      _cuerpo, re.S):
    if _m.group(1):                                   # equation* no numera
        continue
    _n += 1
    for _lab in re.findall(r"\\label\{([^}]+)\}", _m.group(2)):
        _num[_lab] = _n
for _lab in ("eq:lin_fields", "eq:lin_inv", "eq:cp_fields", "eq:cp_inv",
             "eq:oneoverN"):
    assert _lab in _num, f"{_lab} no esta en {_MAIN}"
assert _num["eq:lin_fields"] + 1 == _num["eq:lin_inv"], \
    "lineal: campos e invariante ya no son consecutivas"
assert _num["eq:cp_fields"] + 1 == _num["eq:cp_inv"], \
    "circular: campos e invariante ya no son consecutivas"
EQ_LIN_INV = _num["eq:lin_inv"]
EQ_CP_INV = _num["eq:cp_inv"]
EQ_ONE_OVER_N = _num["eq:oneoverN"]

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "axes.linewidth": 0.8,
    "figure.dpi": 160,
    "savefig.dpi": 300,
    "mathtext.fontset": "dejavuserif",
})

E0 = 1.0

fig, ax = plt.subplots(1, 2, figsize=(7.0, 2.9))

# ---------------- Panel (a): F(omega t) en kz = 0 ----------------
wt = np.linspace(0.0, 2.0 * np.pi, 1200)
z0 = 0.0

# lineal co-polarizada en kz = 0: invariante eq:lin_inv, numero derivado:
F_lin = E0**2 * (np.cos(2 * wt) + np.cos(2 * z0))
# circular co-rotante en kz = 0: invariante eq:cp_inv, numero derivado:
F_cir = 2.0 * E0**2 * np.cos(2 * z0) * np.ones_like(wt)

ax[0].axhline(0.0, color="0.6", lw=0.6)
ax[0].plot(wt / np.pi, F_lin / E0**2, color="#c0392b", lw=1.6,
           label=rf"linear co-polarised, Eq. ({EQ_LIN_INV})")
ax[0].plot(wt / np.pi, F_cir / E0**2, color="#1f4e79", lw=1.6,
           label=rf"circular co-rotating, Eq. ({EQ_CP_INV})")
ax[0].fill_between(wt / np.pi, 0.0, F_lin / E0**2,
                   where=F_lin >= 0, color="#c0392b", alpha=0.10)
ax[0].set_xlabel(r"$\omega t/\pi$")
ax[0].set_ylabel(r"$\mathcal{F}/E_0^2$   (at $kz=0$)")
ax[0].set_xlim(0.0, 2.0)
ax[0].set_ylim(-0.45, 2.6)
ax[0].set_xticks([0.0, 0.5, 1.0, 1.5, 2.0])
ax[0].legend(loc="lower center", fontsize=7, frameon=False)
ax[0].text(0.03, 0.93, "(a)", transform=ax[0].transAxes, fontsize=10,
           fontweight="bold")
ax[0].annotate("crosses zero\n(twice per period)", xy=(0.5, 0.0),
               xytext=(0.62, 0.55), fontsize=6.5, color="#c0392b",
               arrowprops=dict(arrowstyle="->", color="#c0392b", lw=0.7))

# ---------------- Panel (b): 1/N y sqrt(N) ----------------
N = np.arange(1, 33)
E_in = 1.0 / N              # energia de entrada normalizada a la de 1 haz
E_peak = np.sqrt(N)         # campo pico a energia total fija, normalizado

ax[1].loglog(N, E_in, color="#1f4e79", lw=1.6, marker="o", ms=2.6,
             label=r"$\mathcal{E}_{\rm in}/\mathcal{E}_{\rm ref}=1/N$")
ax[1].loglog(N, E_peak, color="#2e7d32", lw=1.6, marker="s", ms=2.6,
             label=r"$E_{\rm peak}(N)/E_{\rm peak}(1)=\sqrt{N}$")
ax[1].axhline(1.0, color="0.6", lw=0.7, ls="--")
ax[1].set_xlabel(r"$N$ (coherent beams)")
ax[1].set_ylabel("normalised value")
ax[1].set_xlim(1, 32)
ax[1].set_ylim(0.03, 8.0)
ax[1].legend(loc="lower left", fontsize=6.5, frameon=False)
ax[1].text(0.03, 0.93, "(b)", transform=ax[1].transAxes, fontsize=10,
           fontweight="bold")
ax[1].annotate(r"slope $-1$", xy=(14.0, 1 / 14), xytext=(12.0, 0.037),
               fontsize=6.5, color="#1f4e79",
               arrowprops=dict(arrowstyle="->", color="#1f4e79", lw=0.7))
ax[1].annotate(r"slope $+1/2$", xy=(24, np.sqrt(24)), xytext=(5.0, 4.2),
               fontsize=6.5, color="#2e7d32",
               arrowprops=dict(arrowstyle="->", color="#2e7d32", lw=0.7))

fig.tight_layout(pad=0.4)
fig.savefig("fig_invariants.pdf")
fig.savefig("fig_invariants.png")

# ---------------- crudo ----------------
print("UNIVERSO DECLARADO: figura analitica de 2 paneles; panel (a) evalua "
      "F(wt) en kz=0 desde los invariantes ("
      f"{EQ_LIN_INV}) y ({EQ_CP_INV}) derivados de main.tex; panel (b) evalua "
      f"las curvas 1/N ({EQ_ONE_OVER_N}) y sqrt(N) para N = 1..32.")
print(f"panel (a) lineal  : F/E0^2 in [{F_lin.min()/E0**2:.3f}, "
      f"{F_lin.max()/E0**2:.3f}]  (cruza cero)")
print(f"panel (a) circular: F/E0^2 = {F_cir[0]/E0**2:.3f}  (constante en t)")
print(f"panel (b) N=2 -> E_in/E_ref = {1/2:.4f}, sqrt(N) = {np.sqrt(2):.4f}")
print(f"panel (b) N=32 -> E_in/E_ref = {1/32:.4f}, sqrt(N) = {np.sqrt(32):.4f}")
print("escrito: fig_invariants.pdf, fig_invariants.png")
