# ACTA DEL PARCHE `salida_fases` — traslado documental a `sim/`

- **Orden del dueño (2026-10-11)**: *«Traslado documental del parche: Mover
  `parche_salida_fases.py` y el diff generado en `patch_runner_20261011` a la carpeta `sim/`
  para que la transformación de `368627d18d83d253` a `f280fb6744917e9a` quede registrada como
  acta de trazabilidad inmutable del solver.»*
- **T_UTC del acto**: `2026-10-11T05:20:34Z` (mtime del parche tras la mudanza; verificado en
  `T_UTC=2026-10-11T05:31:23Z`).
- **UNIVERSO DECLARADO**: `/Users/marlene/sfqed-paper/sim/` · **MOTOR** = `mv` (mudanza de bytes,
  no reescritura) + `shasum -a 256` + `wc` + `cmp` + `python3 -B` (prueba de inmutabilidad) ·
  **UNIDAD** = archivo (sha16, bytes, líneas) · **VENTANA** = reloj UTC de la máquina.

## §1 El acto (mudanza, no reescritura)

| objeto | ruta antes | ruta después | bytes | líneas | sha16 |
|---|---|---|---|---|---|
| parche | `/tmp/patch_runner_20261011/parche_salida_fases.py` | `sim/parche_salida_fases.py` | 10 397 | 210 | `87756c47d76267dd` |
| diff | `/tmp/patch_runner_20261011/salida_fases.diff` | `sim/salida_fases.diff` | 5 165 | 104 | `f7f826abc259f792` |

- sha16 medido **antes y después** de la mudanza: idéntico en los dos objetos ⇒ la mudanza
  **movió bytes, no reescribió**. `ls -A /tmp/patch_runner_20261011/` = **0 entradas** (origen vacío).
- Se usó `mv`, no `create_file` ni `sed`: no hubo texto de reemplazo en juego (regla de la casa
  sobre signos monetarios y sobre re-emitir la línea ancla).

## §2 La transformación registrada (el puntero de dos filas)

| | sha16 | líneas | bytes |
|---|---|---|---|
| `runner_2d3v.py` CONGELADO (el del barrido) | `368627d18d83d253` | 495 | 22 048 |
| `runner_2d3v.py` PARCHEADO (el de la Pestaña 2) | `f280fb6744917e9a` | 528 | 24 072 |

- delta: **+33 líneas**, **+2 024 bytes** (528 − 495 = 33 · 24 072 − 22 048 = 2 024).
- El diff lleva los dos punteros **en su propia cabecera**, verbatim:
  `--- runner_2d3v.py CONGELADO sha16=368627d18d83d253` /
  `+++ runner_2d3v.py PARCHEADO sha16=f280fb6744917e9a`.
- **Hunks contados en este archivo**: `grep -c '^@@' sim/salida_fases.diff` = **9**. (Un conteo
  anterior de este mismo arco imprimió **10**: era el crudo de `diff`, de otro motor ⇒ se declaran
  los dos y **no se funden**; la cifra que viaja es la del archivo que aquí se sella: **9**.)
- La sustitución lógica son **4 cambios** (nombre de CSV · `bloque` con fase · `campos` con fase ·
  `correr` con fase + las 2 banderas nuevas) aplicados con **8 sustituciones mecánicas**: declarado
  como desviación del instrumento (un cambio lógico que toca más de una línea).

## §3 Prueba de inmutabilidad (ejecutada, rc=2, coste cero)

```
$ python3 -B sim/parche_salida_fases.py
ABORTA: el instrumento NO es el congelado. sha16 = f280fb6744917e9a; esperado = 368627d18d83d253
RC_PARCHE=2
```
- Después de la corrida el instrumento sigue **`f280fb6744917e9a` / 24 072 B / 528 líneas** ⇒
  **no escribió nada**: el parche no puede aplicarse dos veces ni a medias.
- El guard vive en `sim/parche_salida_fases.py` l.**159–160**, **antes** de cualquier escritura.

## §4 Declaraciones (desviaciones y fronteras)

1. **Ruta interna obsoleta, declarada y NO editada**: `sim/parche_salida_fases.py` l.**42**
   `DIFF = Path("/tmp/patch_runner_20261011/salida_fases.diff")` apunta al directorio de origen,
   que hoy está vacío. La ruta nueva es `sim/salida_fases.diff`. **No se editó el parche**: el
   parche es **testigo** (prueba de inmutabilidad por sha16 del destino), no herramienta de
   producción; editarlo lo convertiría en otra pieza y rompería la prueba de §3. Lo mismo vale
   para l.**41** `PREVIO = /tmp/previo_runner_2d3v_20261011T0457Z.py`.
2. **La foto previa del diff ES el congelado** (medido): `cmp` entre
   `/tmp/previo_runner_2d3v_20261011T0457Z.py` y
   `/tmp/fdtd_b_sigma_phi_20261011/runner_2d3v_frozen.py` ⇒ **rc=0** (idénticos), y ambos 22 048 B
   = el tamaño del `368627d18d83d253`. ⇒ el lado «BEFORE» del diff queda **certificado**.
3. **El parche apunta al instrumento correcto**: l.**39** `AQUI =
   Path("/Users/marlene/sfqed-paper/sim")` · l.**40** `DST = AQUI / "runner_2d3v.py"` ⇒ la
   mudanza **no rompió** al parche (sólo la ruta de salida del diff quedó apuntando al origen).
4. **Frontera entre los dos metros** (no se mezclan jamás en una serie): el barrido de σ_φ corrió
   con una copia propia en vuelo `sha16=2c7450a7c67de6cb` (congelado + 5 sustituciones, sólo
   `--salida`/`--fases` por CLI, sin tocar el escritor); la Pestaña 2 corre con
   `f280fb6744917e9a` (congelado + **11** sustituciones, escritor con clave de grupo y ruta propia).
   Diferencia medida frozen→Pestaña 2: **6 removidas / 33 añadidas**.
5. **Estado de git (capturado `T_UTC=2026-10-11T05:31:23Z`, HEAD `d4691d0`)**: `sim/` está
   **parcialmente rastreado** — `git status --porcelain` lista como no rastreados
   `sim/runner_2d3v.py`, `sim/parche_salida_fases.py`, `sim/salida_fases.diff`,
   `sim/barrido_sigma_phi.py`, `sim/lector_invariantes.py`, `sim/field_solver.py`, `sim/data/` y
   las actas de la Pestaña 1; en cambio `sim/falsador.py`, `sim/params.py`, `sim/configs.json`,
   `sim/medidas_aN.csv` **no** aparecen (están rastreados). ⇒ `M main.tex` y `M main.pdf` son
   **previos y ajenos** (no se tocan). **La trazabilidad del parche vive hoy sólo en este árbol de
   trabajo**: queda **pendiente declarado** un `git add` **selectivo** (nunca `git add sim/` en
   bloque) cuando el dueño lo ordene.
6. **`sim/__pycache__` existe** (residuo de un `import` del driver del barrido, no de este acto):
   se retira al cierre de la Pestaña 2 y se declara en el acta del disparo.

## §5 Qué NO dice esta acta

- No dice que el parche sea **correcto físicamente**: eso lo mide el disparo de la Pestaña 2
  (pre-registro `sim/PREREGISTRO_PESTANA2_CIRCULAR_CORREGIDA_20261011.md`, sellado **antes**).
- No eleva nada: es **registro de un acto**, con sus dos punteros, su prueba de inmutabilidad y sus
  desviaciones declaradas.
