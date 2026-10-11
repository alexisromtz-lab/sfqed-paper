#!/usr/bin/env python3
"""sim/filtro_analitico.py -- filtro analitico PREVIO: intercepta corridas saturadas antes del solver.

ORDEN DEL DUENO (verbatim, 11-Oct-2026). Redactar la funcion pura
`evaluar_sensibilidad_previa(modo, alpha_deg, N, tol_rango=1e-4) -> tuple[bool, str]`:
  - Retorna `(True, "")` si la corrida es valida y no degenerada.
  - Retorna `(False, razon)` si la corrida cae en saturacion analitica (debe abortar).
  Regla 1 (contra-propagacion): si `modo == "contra"` y el punto de lectura espacial
  coincide con un antinodo electrico donde analiticamente `B -> 0`:
  `abs(1 - r) = abs(1 - a_inv / abs(E)) < tol_rango` =>
  `(False, "Saturacion por antinodo: B -> 0 fuerza r -> 1.0 por Cauchy-Schwarz; medicion
  degenerada")`. La cota se resuelve POR DEDUCCION; el FDTD NO se invoca.
  Regla 2 (abanicos): si `alpha_deg == 0` en modos con convergencia supuesta, el
  semiangulo nulo reduce el sistema a onda plana pura colimada (`E . B = 0`), forzando
  `a_inv = 0` continuo => `(False, "Semiangulo nulo: campo colimado identicamente
  transversal")`.

UNIVERSO DECLARADO: aqui NO hay malla, ni campo, ni tiempo. El universo de este modulo
son los CUATRO NOMBRES de modo del motor (`sim/maxwell2d.py`, docstring l.28-34:
`colineal` | `colineal-nulo` | `contra` | `contra-nulo`), el algebra del invariante
eq:ab en las unidades del motor (`sim/maxwell2d.py:266` `invariante_a`: `F = eps0/2
(E^2 - c^2 B^2)`, `G = eps0 c E.B`, `a_inv = sqrt(sqrt(F^2 + G^2) + F) / sqrt(eps0)`,
devuelto en V/m), y nada mas. Cero FDTD: `--control` prueba que tras importar este
modulo NI `maxwell2d` NI `numpy` estan en `sys.modules`.

LA COTA DE LA REGLA 1 ES ALGEBRA, NO UMBRAL (y por eso `tol_rango` casi no manda):
en el antinodo electrico `B = 0` y `E . B = 0` => `G = 0` y `F = (eps0/2) |E|^2 > 0` =>
`a_inv = sqrt(sqrt(F^2) + F) / sqrt(eps0) = sqrt(2F) / sqrt(eps0) = |E|` => `r = 1`
EXACTO, con `eps0` cancelada. Entonces `abs(1 - r) = 0.0 < tol_rango` para TODO
`tol_rango > 0`: la regla 1 es estructural y no depende del valor de la tolerancia.
Lo que la tolerancia protege es solo que exista (`tol_rango <= 0` => ValueError): una
tolerancia no positiva no es una tolerancia. Si el dueno quisiera un umbral EFECTIVO,
la cota tendria que venir de la medicion (0.0079 en el sello, ver abajo) y eso seria
otra regla, no esta: no se cambia sin orden.

FRONTERA DECLARADA (la trampa obvia, para que nadie la repare de mas): los DOS sellos
miden `a_inv / |E|` cerca de 1 -- `etapa1_contra.json` 0.9920899249757815 y
`etapa1_colineal.json` 0.9995132753995678. La regla 1 dispara SOLO en `contra`, porque
lo que la funda es el MECANISMO (pares enfrentados => antinodo electrico en el punto de
lectura), no el valor medido. Generalizarla a "cualquier r > 0.99 dispara" fabricaria un
falso positivo en `colineal`, que el dueno NO ordeno interceptar. La regla es del
mecanismo; el umbral sobre el valor medido seria un instrumento distinto y sin orden.

PUREZA Y SELLO: este modulo es NUEVO y no edita ninguna pieza sellada. `sim/maxwell2d.py`
queda intacto (`1db75ea7b0b8cba4`): su pre-registro declara "instrumento
1db75ea7b0b8cba4 sin editar". El cableado dentro de `correr()` es el paso siguiente y
requiere que el dueno abra ese sello. Un archivo nuevo en `sim/` NO entra al universo del
manifiesto del bundle (las rutas de `bundle/HASHES.sha256` son relativas a `bundle/`) =>
no fabrica huerfano alli.

Uso:
  python3 -B sim/filtro_analitico.py --control
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

AQUI = Path(__file__).resolve().parent

# Catalogo de modos del motor (sim/maxwell2d.py, docstring l.28-34). No se inventa:
# se copia, y si el motor cambia, este conjunto debe cambiar con el.
MODOS_DEL_MOTOR = ("colineal", "colineal-nulo", "contra", "contra-nulo")

# "Modos con convergencia supuesta" (regla 2): los que SUPONEN convergencia al foco.
# El motor declara los `-nulo` como CONTROLES de ruptura ("control 5.2: el escalado
# DEBE romperse"): no suponen convergencia. Se deriva del catalogo, no se lista a mano,
# para que la convencion quede a la vista y no escondida.
MODOS_CON_CONVERGENCIA_SUPUESTA = tuple(
    m for m in MODOS_DEL_MOTOR if not m.endswith("-nulo")
)

# Las DOS razones, verbatim de la orden. No se parafrasean: son el texto que el gate
# imprime y contra el que se comparan los controles.
RAZON_ANTINODO = (
    "Saturación por antinodo: B -> 0 fuerza r -> 1.0 por Cauchy-Schwarz; "
    "medición degenerada"
)
RAZON_SEMIANGULO = "Semiángulo nulo: campo colimado idénticamente transversal"


def punto_de_lectura_es_antinodo(modo: str) -> bool:
    """Segundo miembro de la regla 1: el punto de lectura cae en un antinodo electrico.

    Por CONSTRUCCION del motor, y solo en `contra`: `terminos_de()` (sim/maxwell2d.py:246)
    reparte N/2 haces en el plano fuente izquierdo y N/2 en el derecho (pares
    enfrentados), y el punto de lectura es la celda del foco `(IC, JC)`; ahi los pares
    llegan en fase, el campo electrico es NO nulo y `B = 0` (docstring l.33: "contra ...
    campo NO nulo, B = 0 en el foco"). Deducido, no medido.

    Si alguna vez la geometria mueve el punto de lectura, esta funcion deja de ser un
    nombre del modo y pasa a necesitar las COORDENADAS: se declara aqui en vez de
    esconderse.
    """
    return modo == "contra"


def cota_deducida_antinodo() -> float:
    """r deducida en el antinodo electrico. Ver el algebra en el docstring del modulo."""
    return 1.0


def evaluar_sensibilidad_previa(
    modo: str,
    alpha_deg: float,
    N: int,
    tol_rango: float = 1e-4,
) -> tuple[bool, str]:
    """Intercepta corridas degeneradas ANTES del solver.

    Retorna `(True, "")` si la corrida es valida y no degenerada.
    Retorna `(False, razon)` si cae en saturacion analitica (debe abortar).

    PRECEDENCIA DECLARADA (no emergente): la regla 1 se evalua antes que la regla 2. Con
    `modo == "contra"` y `alpha_deg == 0` las dos aplican; nombra la 1 porque nombra la
    causa mas especifica (el modo), y la corrida aborta igual.

    Lo que NO es una corrida evaluable no devuelve verde ni una razon de saturacion
    falsa: levanta `ValueError` (fail-closed, ruidoso). Las razones de saturacion son
    solo las dos que la orden nombra.
    """
    if modo not in MODOS_DEL_MOTOR:
        raise ValueError(
            "modo no declarado: %r. Los modos del motor son %s (sim/maxwell2d.py:28-34)."
            % (modo, ", ".join(MODOS_DEL_MOTOR))
        )
    if not (tol_rango > 0.0):
        raise ValueError(
            "tol_rango no positivo (%r): una tolerancia no positiva no es una tolerancia."
            % (tol_rango,)
        )
    n = int(N)
    if n < 1:
        raise ValueError("corrida no evaluable: N = %d; el motor reparte energia en N haces." % n)
    if modo == "contra" and n % 2:
        raise ValueError(
            "corrida no evaluable: el motor exige N par en contra "
            "(sim/maxwell2d.py:246, terminos_de)."
        )

    # --- Regla 1: saturacion por simetria en contra-propagacion -------------
    if modo == "contra" and punto_de_lectura_es_antinodo(modo):
        r = cota_deducida_antinodo()
        if abs(1.0 - r) < tol_rango:
            return (False, RAZON_ANTINODO)

    # --- Regla 2: degeneracion angular en abanicos --------------------------
    if float(alpha_deg) == 0.0 and modo in MODOS_CON_CONVERGENCIA_SUPUESTA:
        return (False, RAZON_SEMIANGULO)

    return (True, "")


# --------------------------------------------------------------------- control
# POSITIVOS: deben interceptarse, y con ESTA razon exacta.
POSITIVOS = (
    (("contra", 30.0, 2), RAZON_ANTINODO, "modo contra con angulo no nulo: par enfrentado"),
    (("contra", 26.5651, 4), RAZON_ANTINODO, "el mismo modo con N = 4 (medio par por lado)"),
    (("colineal", 0.0, 4), RAZON_SEMIANGULO, "angulo nulo, modo con convergencia supuesta"),
    (("contra", 0.0, 2), RAZON_ANTINODO, "las dos reglas aplican: precedencia declarada"),
)
# NEGATIVOS: deben pasar. El control del medio es `contra-nulo`: antinodo PARCIAL
# (medido cB/|E| = 0.445 en el sello de la pestana), no antinodo pleno.
NEGATIVOS = (
    (("colineal", 26.5651, 4), "el modo del control pareado que converge"),
    (("colineal", 30.0, 2), "el otro angulo del control pareado"),
    (("contra-nulo", 30.0, 2), "antinodo parcial medido: no dispara"),
    (("colineal-nulo", 30.0, 2), "control de ruptura: no supone convergencia"),
    (("colineal", 0.5, 4), "solo el CERO exacto degenera; casi-cero no"),
    # Frontera de la convencion declarada: los `-nulo` NO suponen convergencia, asi
    # que el angulo nulo NO los degenera. Si alguien mete los nulos dentro de
    # MODOS_CON_CONVERGENCIA_SUPUESTA, estos dos se caen y el control lo dice.
    (("colineal-nulo", 0.0, 2), "frontera: nulo con angulo nulo no supone convergencia"),
    (("contra-nulo", 0.0, 2), "frontera: nulo con angulo nulo, y sin antinodo pleno"),
)


def _sellos():
    """Lee `a_inv / |E|` de los dos sellos de etapa 1. Cita, no criterio del filtro."""
    fuera = {}
    for nom in ("etapa1_contra.json", "etapa1_colineal.json"):
        p = AQUI / nom
        if not p.is_file():
            fuera[nom] = None
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        vals = [f["corrida"]["a_inv_rel_al_pico"] for f in d["filas"] if "a_inv_rel_al_pico" in f.get("corrida", {})]
        fuera[nom] = (d.get("modo"), min(vals), max(vals), len(vals)) if vals else None
    return fuera


def control() -> int:
    """Par de controles del filtro. RC = veredicto: 0 discrimina, 1 no, 2 SIN MEDIDA."""
    print("T_UTC=%s" % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    print(
        "UNIVERSO DECLARADO: %d controles (%d positivos, %d negativos) sobre la funcion "
        "pura; el universo del filtro son los %d modos del motor."
        % (len(POSITIVOS) + len(NEGATIVOS), len(POSITIVOS), len(NEGATIVOS), len(MODOS_DEL_MOTOR))
    )
    print("UNIDAD: caso de control (par booleano + razon exacta). MOTOR: python3 -B, solo math/json.")

    fallos = 0
    print("--- POSITIVOS (deben disparar con la razon exacta) ---")
    for args, esperada, nota in POSITIVOS:
        ok, razon = evaluar_sensibilidad_previa(*args)
        bien = (ok is False) and (razon == esperada)
        fallos += 0 if bien else 1
        print("  %-4s modo=%-13s alpha=%-8s N=%d  ->  ok=%-5s  [%s]"
              % ("OK" if bien else "ROJO", args[0], args[1], args[2], ok, nota))
        if not bien:
            print("        esperado (False, %r); obtenido (%r, %r)" % (esperada, ok, razon))

    print("--- NEGATIVOS (deben pasar) ---")
    for args, nota in NEGATIVOS:
        ok, razon = evaluar_sensibilidad_previa(*args)
        bien = (ok is True) and (razon == "")
        fallos += 0 if bien else 1
        print("  %-4s modo=%-13s alpha=%-8s N=%d  ->  ok=%-5s  [%s]"
              % ("OK" if bien else "ROJO", args[0], args[1], args[2], ok, nota))
        if not bien:
            print("        esperado (True, ''); obtenido (%r, %r)" % (ok, razon))

    print("--- CORRIDAS NO EVALUABLES (deben levantar ValueError, no devolver verde) ---")
    for args, porque in (
        (("xyz", 30.0, 2), "modo no declarado"),
        (("contra", 30.0, 3), "N impar en contra"),
        (("colineal", 30.0, 0), "N < 1"),
        (("colineal", 30.0, 2, 0.0), "tol_rango no positivo"),
    ):
        try:
            r = evaluar_sensibilidad_previa(*args)
        except ValueError:
            print("  OK   %-30s ->  ValueError  [%s]" % (str(args), porque))
        else:
            fallos += 1
            print("  ROJO %-30s ->  devolvio %r  [%s]" % (str(args), r, porque))

    print("--- PUREZA (el FDTD no se invoca) ---")
    sucio = [m for m in ("maxwell2d", "numpy", "field_solver") if m in sys.modules]
    print("  %-4s modulos del solver en sys.modules tras importar el filtro: %s"
          % ("OK" if not sucio else "ROJO", sucio or "ninguno"))
    fallos += 1 if sucio else 0

    print("--- ACUERDO CON LOS SELLOS (cita, no criterio del filtro) ---")
    r_ded = cota_deducida_antinodo()
    s = _sellos()
    faltan = [k for k, v in s.items() if v is None]
    for nom, v in s.items():
        if v is None:
            print("  SIN MEDIDA  %s ausente" % nom)
            continue
        modo, lo, hi, n = v
        print("  %-10s modo=%-9s a_inv/|E| medido en %d fila(s): [%r, %r] · "
              "r deducida = %r · abs(1 - r) medido = [%r, %r]"
              % (nom, modo, n, lo, hi, r_ded, abs(1.0 - lo), abs(1.0 - hi)))
    print("  nota: la regla 1 dispara por el MECANISMO del modo contra, no por estos")
    print("        valores; los sellos solo confirman que la cota deducida cae cerca.")

    if fallos:
        print("VEREDICTO: EL FILTRO NO DISCRIMINA · RC: 1 · %d control(es) en rojo" % fallos)
        return 1
    if faltan:
        print("VEREDICTO: FILTRO OK, ACUERDO SIN MEDIDA · RC: 2 · ausentes: %s" % ", ".join(faltan))
        return 2
    print("VEREDICTO: FILTRO DISCRIMINA · RC: 0 · %d modos, %d controles, pureza verificada"
          % (len(MODOS_DEL_MOTOR), len(POSITIVOS) + len(NEGATIVOS)))
    return 0


def main(argv: list[str]) -> int:
    if "--control" in argv:
        return control()
    print(__doc__)
    print("Sin --control no se mide nada: la funcion pura no tiene efecto por si sola.")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
