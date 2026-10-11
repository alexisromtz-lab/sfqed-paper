# ACTA DEL DISPARO — Pestaña 2, circular corregida (2026-10-11)

**Quién hace qué.** El disparo lo corrió **otra mano** (el orquestador `fuego_pestana2_20261011.py`, editado
por esa mano; no el driver que este pre-registro imaginaba). Esta acta la escribe la mano **que audita**:
no disparó, no escribió el canónico, no tocó el runner, no volvió a medir ninguna `a`. Todo lo de aquí se
obtuvo **leyendo y contando** del disco, con `python3 -B` (3.14.7) + numpy 2.4.6, entre `05:47Z` y `05:49Z`
del 11-Oct-2026. **UNIVERSO DECLARADO** de la auditoría: `sim/` completo, excluyendo `.git`; **UNIDAD**:
fila y archivo (declaradas por medición, no por costumbre); **MOTOR**: `python3 -B` + `hashlib.sha256`.

---

## 1. La cadena del motor, medida comando a comando

Los 12 comandos están **verbatim** en la primera línea de cada `log_sigma_<σ>.txt`. Patrón (σ = 0.500):

```
/opt/homebrew/opt/python@3.14/bin/python3.14 -B .../runner_2d3v.py --todo --pol circular
  --fases -1.0457097788,...,0.0237523229 --sigma-phi 0.500
  --salida .../pestana2_circular_corregida_20261011/sigma_0.500.csv
```

- **12/12** comandos llevan `--salida` de **su propio** grupo y `--fases` con **16** flotantes **iguales al
  vector sellado** (comparados a 10 decimales, la precisión del sello).
- El runner se invocó con `--todo` ⇒ **los cinco N en un solo proceso por σ**; `pared = 115.4 s` (`rc=0`,
  `T_UTC_fin=2026-10-11T05:38:35Z` en σ = 0.500).
- Las tres oleadas de mtimes de grupo — **05:36:39Z ×4 · 05:38:34–35Z ×4 · 05:40:29–30Z ×4** — están
  separadas por **≈115 s** = la pared declarada ⇒ **4 grupos concurrentes, 3 tandas** (12 grupos). El motor
  es subprocess por σ con pool de 4, tal como se selló.
- Los 12 `log_sigma_<σ>.txt` tienen **5 líneas `^N=`** cada uno (12/12) ⇒ las 60 filas existen **en la
  fuente**, no sólo en la unión.

## 2. Piezas y hashes (medidos en disco, no citados del texto)

| pieza | líneas | bytes | sha16 | mtime_utc |
|---|---|---|---|---|
| `runner_2d3v.py` | 528 | 24 072 | `f280fb6744917e9a` | 04:59:27Z |
| `PREREGISTRO_..._CIRCULAR_CORREGIDA_20261011.md` | 137 | 11 289 | `d44cf0c5e948c04f` | 05:35:06Z |
| `data/medidas_aN_circular_corregida_20261011.csv` (canónico) | 82 | 3 366 | `c9aaa89b7d56ead7` | 05:44:07Z |
| `medidas_aN_circular.csv` (testigo) | 9 | 672 | `ee5539f3f9efa96d` | 01:11:39Z |
| `fuego_pestana2_20261011.py` (orquestador real) | 410 | 20 051 | `f09e781a65d3abe6` | 05:44:02Z |
| `driver_circular_sigma_phi.py` (borrador viejo) | 292 | 11 744 | `7efee77ccec677db` | 05:36:36Z |

El `sha16` que el **propio canónico declara** en su preámbulo para el runner (`f280fb6744917e9a`) **coincide
con el del runner vivo** ⇒ la cadena de hashes del artefacto se verifica contra el disco, no se cita a sí
misma. Mismo caso con el sello (`d44cf0c5e948c04f`) y el testigo (`ee5539f3f9efa96d`).

## 3. Los cuatro criterios del §5, con sus números

- **K4 — contar (la única cifra de cierre). VERDE.** Canónico: **82 líneas = 10 preámbulo + 12 líneas de
  grupo + 60 filas de datos**; **22** líneas `#`; **12 claves × 5 filas** exactas; los **12 `sha16_grupo`
  declarados coinciden con los reales (12/12)**; la unión **canónico == grupos en 60/60 filas**.
  Nota de metro: los CSV de grupo vienen **`N,a_medido,sigma_phi`** (clave en la 3ª columna, como manda el
  §3 del sello) y el canónico viene **`sigma_phi,N,a_medido`** (clave en la 1ª) ⇒ la comparación exige
  mapear columnas por archivo; hacerlo "a ojo" produce un `ValueError` y, peor, un falso rojo.
- **K0 — control σ = 0. VERDE, escrito como manda el sello.** Las cinco `a` del grupo σ = 0 reproducen
  **bit-for-bit a 10 decimales** las del testigo (`178.7553300762 · 241.1697981457 · 341.0655993725 ·
  482.3408425826 · 682.1331202323`), y el testigo sigue **intacto** (9 l · 672 B · `ee5539f3f9efa96d`).
  β del testigo con la misma fórmula: **β_5p = 0.486414 · β_4p = 0.500002**. Se escribe **«el testigo se
  reproduce»**; **no** se escribe «β = 0.500000» (ése es el fasor, otro objeto).
- **K3 — el cruce. VERDE, dentro de la tolerancia sellada.** Cruce de β = 0.45 por interpolación lineal
  entre σ vecinos: **β_5p → 0.608596 rad**, distancia al objeto PICO (0.527493 rad) = **+0.081103 rad**;
  **β_4p → 0.586499 rad**, distancia **+0.059006 rad**. Tolerancia declarada = 1 paso de rejilla =
  **0.125 rad** ⇒ **DENTRO** las dos. La serie β(σ) **no es monótona** después de σ = 0.625 (baja a
  0.237270 en σ = 1.5, sube a 0.305243 en σ = 3.0, siempre por debajo de 0.45) ⇒ **un solo cruce por
  estimador**, y así se contó. El cruce FOCO (0.554987 rad) se **reporta**, no se adjudica.
- **K2 — identidad declarada, NO evidencia. CUMPLIDA.** Por parseo de los `centro = …` y `a_fdtd = …` de
  las 60 corridas: `a_PICO ≥ a_FOCO` en **60/60**, con **margen mínimo exactamente 0.0** (se alcanza la
  igualdad; p. ej. N = 2, σ = 0.000, donde el máximo cae en el centro). Que se cumpla no confirma física
  alguna: es |P| + |M| ≥ |P + M|. **Lectura distinta, reportada y no adjudicada:** con el campo
  `cent_pico` la comparación da 34/60 (margen mínimo −152.6) ⇒ ese campo mide **otro objeto**; el criterio
  sellado se cumple con `centro`.

## 4. Guardas del sello (ejecutables, corridas aquí)

- **Eco del vector — 12/12 con igualdad exacta**: la cabecera de cada `sigma_<σ>.csv`
  (`fases_por_haz = [...]`) es **la misma cadena** que sella el §4.
- **Receta determinista — 12/12 a 10 decimales**: `numpy.random.default_rng(semilla_sellada).normal(0.0, σ, 16)`
  reproduce el vector sellado **redondeado a 10 decimales**, que es la precisión a la que el sello lo imprime.
  ⚠️ **Trampa de metro propia, medida y declarada:** comparando en **doble exacto** sale **1/12** — y ese 1
  es σ = 0 (`[0.0]*16`, por definición); los otros 11 difieren en el último dígito **porque el sello está
  impreso redondeado**. El «1/12» no dice que la receta falle: dice que yo comparé dos precisiones
  distintas. Se registra para que nadie lo lea como fallo de la receta.
- **σ = 0 ⇒ `[0.0]*16`** por definición (verificado en el eco y en la receta).

## 5. Estados del canónico: la escritura no es atómica

El canónico se leyó **tres veces** y no todas fueron el mismo objeto:

1. `05:41:36Z` — **72 l · 12 `#` · `c1c1e5d22b343e9f`** ⇒ **NO es el estado final**; toda cita de ese sha16
   queda **caduca**.
2. `05:41:46Z` — **82 l · 22 `#` · 60 filas · 3 366 B · `c9aaa89b7d56ead7`** ⇒ estado cerrado.
3. `05:44:07Z` — **mismo sha16, mismos bytes**; sólo se movió el **mtime**.

El escritor es `fuego_pestana2_20261011.py` en su unión: `CSV_CANONICO.write_text(out, encoding="utf-8")`
(l. **259**) **sin `.tmp` ni `os.replace`** ⇒ un lector concurrente puede ver un estado a medias (eso es,
probablemente, el estado 1). Y el canónico se **re-escribió** (mtime 05:41:46 → 05:44:07) con contenido
**idéntico**, **5 s después** de que la mano vecina editara `fuego` (05:44:02Z) ⇒ es **otro acto del mismo
instrumento**, no un demonio periódico: en dos sondeos de `ps` (`05:45:20Z`, `05:45:32Z`) **no había ningún
escritor vivo** (sólo un proceso corto de 34 s).
**Regla que sale de aquí: la identidad del canónico es su `sha16`; su `mtime` no es identidad, es acto.**

## 6. Divergencias declaradas (no reparadas; se declaran, no se tocan)

1. **La clave cambia de columna entre grupo y canónico** (§3, K4). El §3 del sello la quiere en la **3ª**
   columna («las dos primeras siguen siendo las que lee `sim/falsador.py`») ⇒ los **grupos cumplen** y el
   **canónico no**. Consecuencia medida, no supuesta: el canónico **no es directamente falsador-compatible**;
   los grupos sí.
2. **El orquestador real no es el driver que el pre-registro imaginaba.** Disparó
   `fuego_pestana2_20261011.py` (410 l · `f09e781a65d3abe6`). El `driver_circular_sigma_phi.py` (292 l ·
   `7efee77ccec677db`) quedó como **borrador viejo**: usa `np.random.seed(SEMILLA)` (l. 181), no tiene
   subprocess ni pool ni `os.replace`, y su cabecera afirma «geometria = coaxial contra-propagante» (l. 261)
   — **falso**: el docstring vivo del runner dice que los N haces son **coplanarios** en el plano xy
   (θ_j = 2πj/N).
3. **Peligro vivo, medido:** ese borrador escribe **el mismo camino** que el canónico
   (`SALIDA = AQUI/"data"/"medidas_aN_circular_corregida_20261011.csv"`, l. 64–65, escritura en l. 275).
   Correrlo hoy **destruiría el testigo sellado** con la receta vieja (y además su salida no llevaría las
   12 líneas de grupo: por eso **no** es el productor del artefacto actual). Sólo dos archivos en `sim/`
   mencionan ese camino: él y `fuego`.
4. **El resumen del orquestador no existe:** `data/pestana2_circular_corregida_20261011/resumen_pestana2.csv`
   **ausente** ⇒ la corrida escribió el canónico (unión) y **no** llegó a su bloque de cierre
   (`CSV_RESUMEN.write_text`, l. 367). Los cruces de esta acta se calcularon **independientemente** con la
   misma fórmula declarada (OLS de log a contra log N), no copiados de un resumen.
5. **La mano vecina está viva mientras se audita** (`fuego` 05:44:02Z · `control_pareado_convergente.py`
   05:44:42Z, y nuevos `PREREGISTRO_KERR_20261011.md`, `LECTURA_ETAPA2_20261011.md`, `ADENDA_2/3/4…`).
   Toda cifra de esta acta vale **para su instante**; se declaran los hashes para poder repetirla.

## 7. Deudas declaradas (ninguna repara las cifras de arriba; todas bloquean una re-corrida)

- **D1 — el rótulo `N_LISTA` del runner.** En el runner vivo (528 l) la línea del defecto es la **496**
  (`… N_LISTA = {N_LISTA} …`, imprime la lista entera en vez de la lista efectiva `lista`); el «l. 476» que
  circuló es la numeración de la **copia congelada** (495 l, `368627d18d83d253`) ⇒ **deriva declarada**.
  Es **inerte** para lo alcanzable hoy: la escritura por grupo exige `--todo` ⇒ `lista is N_LISTA`.
- **D2 — escritura atómica** en `fuego` l. 259 (`.tmp` + `os.replace`), y el `resumen` que falta.
- **D3 — reconciliar el driver con el sello**: el sellado (§4) y el que corrió (`fuego`) deben quedar
  reconciliados por escrito, con subprocess por σ + pool, las fases anidadas de 16 componentes, la guarda
  del eco con **igualdad exacta** y **aborto rc=2 antes de unir**, y un destino explícito para `TOL_DESV`
  (declarada y **no usada**).
- **D4 — plantilla del §4**: los grupos cumplen (`sigma_<σ>.csv`, clave en 3ª columna); el canónico no
  (clave en 1ª). Se declara la corrección; no se renumera ni se reescribe el producto.

## 8. Cierre

**K4 = 60 filas contadas · 12 claves · 22 `#` (82 l · 3 366 B · `c9aaa89b7d56ead7`)** · **K0 VERDE («el
testigo se reproduce», β_5p 0.486414 · β_4p 0.500002)** · **K2 cumplida 60/60, margen mínimo 0.0
(identidad: no es evidencia)** · **K3 DENTRO de la rejilla**: β_5p 0.608596 rad (+0.081103) y β_4p
0.586499 rad (+0.059006), tolerancia 0.125 rad, objeto 0.527493 rad ⇒ **el archivo reproduce la ventana
crítica del modelo**. Guardas: eco **12/12** exacto · receta **12/12** a la precisión del sello.
**Debts:** D1 rótulo del runner (inerte) · D2 atomicidad + resumen ausente · D3 driver/sello · D4 columna de
la clave. **Nada se eleva**: es el acta del disparo.
