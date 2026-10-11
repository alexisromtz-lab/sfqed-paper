# FRONTERA ENTRE PESTAÑAS — medida, no supuesta

Hora de la medición: **2026-10-11T00:19:39Z** (comando: `TZ=UTC stat -f '%Sm %z %N'`,
`git log`, `git status` en `/Users/marlene/sfqed-paper`).
Ventana única de VS Code (`b04c3a42dd7f32a1bcc1461c822b4f3`), varias pestañas de chat.
**Pestaña que escribe este archivo: `2cd28bb3`.**

## 1. Lo que NO es de esta pestaña (huella del objeto, con hora)

| pieza | mtime UTC | B | mano |
|---|---|---|---|
| `refs.bib`, `lint_tex.py` | 2026-10-10T22:38:05Z | 3694 · 4481 | hermana |
| `figures/fig_invariants.png/.pdf` | 2026-10-10T23:00:51Z | 153599 · 46576 | hermana |
| `main.tex` | 2026-10-10T23:16:33Z | 22367 | hermana |
| `figures/fig_invariants.py` | 2026-10-10T23:16:33Z | 5894 | hermana |
| `figures/check_invariants.py` | 2026-10-11T00:00:05Z | 12281 | hermana |
| `main.pdf` | 2026-10-11T00:01:49Z | 146772 | hermana |
| `ZENODO_DEPOSITO_CAMPOS_20261010.md` | 2026-10-11T00:03:43Z | 11762 | hermana |
| `sfqed-paper-zenodo-20261010.tar.gz` | 2026-10-11T00:04:13Z | 340248 | hermana |

Líneas hermanas activas en esta ventana: (a) DOI del tag contra los bytes del
artefacto; (b) carril de subida a Zenodo, que además editó `main.tex`; (c) gates,
`refs.bib`, `check_invariants.py`, `fig_invariants.py`, `lint_tex.py`, `ZENODO_*`;
(d) censo del corpus en `primer/`; (e) el censo de frontera que midió la propia
ventana. **Las cinco están sobre la línea del paper/Zenodo.**

## 2. Lo que SÍ es de esta pestaña

Territorio: **`sfqed-paper/sim/**` y nada más.** Es la única línea de esta ventana
que no es paper ni Zenodo: la etapa de simulación — el falsador del `1/N`.

Reglas que se sostienen mientras las hermanas sigan vivas:

1. Esta pestaña **no escribe `ACTA_*` ni `ADENDA_*` en la raíz de `platino-labs`**
   (ahí escriben las hermanas). El entregable largo va **dentro de `sim/`**.
2. **No se toca**: `main.tex` · `main.pdf` · `ZENODO_*` · `*.tar.gz` · `figures/*`
   · `lint_tex.py` · `refs.bib`.
3. `main.tex` es **solo lectura** y se usa **solo como fuente de fórmula**: el
   instrumento lo lee, imprime su `sha16` y compara contra los pines.
   Pin verificado a **00:19:30Z**: `sha16 = 4299786a34bdb313` para
   `eq:schwinger_rate` `b043587212f4522b` · `eq:ab` `7a20202407815345` ·
   `eq:yield` `b27213b3542beb39` · `eq:lin_inv` `ade47f905f9ac06e` ·
   `eq:cp_inv` `46e99b22931bb5a1`.
   El pin es **por contenido, no por hora**: el `mtime` de `main.tex` es
   23:16:33Z y el cuerpo que los pines fijan sigue siendo el mismo.
4. Si un archivo cambia bajo la mano de esta pestaña, **se declara y no se
   adjudica**.

## 3. Estado del territorio

`git status` a las 00:19:39Z: solo dos archivos sin seguimiento, y los dos son
míos — `sim/schwinger_offline.py` y `sim/pronostico_schwinger.json`.
`sim/medidas_aN.csv` **ausente** (verificado: `No such file or directory`): la
etapa 1 (un motor PIC de verdad) no se ha corrido y no se finge.
