# ABSTRACT formal y TABLA DE DEFINICIONES CATEGÓRICAS
### Marco fibrado (Grothendieck) sobre un poset de escalas, con 2-celdas laxas

**Estado del documento:** borrador de escritura. Ninguna cifra entra sin comando. Las que no lo tienen van rotuladas `DECLARADO` o `SIN CASA`.
**Creado:** `2026-10-11`, sobre el ciclo de `sfqed-paper` (bloque N0–N3 / control pareado convergente).
**Regla de cero escrituras respetada:** no se toca `main.tex` (mtime de otra mano, objeto no adjudicado). El marco se registra **aquí**, en pieza nueva.

---

## §0 · UNIVERSO Y MOTOR DECLARADOS (de este documento)

```
UNIVERSO DECLARADO: (a) las cifras de física -> el log de MI re-medición
                    /tmp/cp_mio_20261011.log  · 143 líneas · 10361 B · sha16 53b628188aa35e19
                    mtime_utc 2026-10-11T17:43:36Z · RC=0 · 42.7 s
                    (b) el vocabulario -> TRES raíces: /Users/marlene/primer,
                    /Users/marlene/sfqed-paper, /Users/marlene/platino-labs.
                    Archivos *.md y *.tex.  EXCLUIDO .git y node_modules.
MOTOR:              python3 -B (aritmética y lectura de JSON) · grep -rEI (ERE)
                    · shasum -a 256 · wc -l / wc -c   ·   NOTA: en la corrida de
                    vocabulario se corrigen 3 erratas de motor propias (§10).
UNIDAD:             cifras de física = razón adimensional (rel) y nodos de malla.
                    vocabulario = LÍNEAS con el término (ocurrencias aparte, §10).
VENTANA:            2026-10-11T17:42Z – 17:46Z (UTC).
```

### Identidad de las piezas citadas (medida, no citada de memoria)

| pieza | líneas | bytes | sha16 |
|---|---|---|---|
| `sim/control_pareado_convergente.py` (instrumento) | 569 | 29405 | `2829d1e1ce1ee7e4` |
| `bundle/instrumentos/medidores/control_pareado_convergente.py` (copia de custodia) | 569 | 29405 | `2829d1e1ce1ee7e4` |
| `sim/data/invariantes/control_pareado_convergente.json` (crudo sellado) | 1288 | 27892 | `41fce209adc05f98` |
| `bundle/actas/VEREDICTO_CONTROL_PAREADO_20261011.md` (prosa) | 254 | 15118 | `a6316f8db84d8885` |
| `sim/medidas_aN.csv` (entrada, no debe moverse) | 18 | 1360 | `4129d436e2cd081d` |
| `/tmp/cp_mio_20261011.log` (mi crudo) | 143 | 10361 | `53b628188aa35e19` |

**Instrumento y custodia son byte-idénticos** (`2829d1e1ce1ee7e4` en ambos). El crudo sellado **no fue reescrito**: se corrió con `--sin-escribir`, y el propio instrumento lo certifica —
`sim/medidas_aN.csv sha16 antes 4129d436e2cd081d  despues 4129d436e2cd081d  (intacto: True)`.
Comando de la corrida: `python3 -B sim/control_pareado_convergente.py --sin-escribir --verbose`.

---

## §1 · ABSTRACT (EN, formal)

> We give a categorical reading of a situation that is common in multiphysics work and rarely formalised: several effective descriptions of one and the same object — a continuum analytic cone, a discrete Yee/FDTD solver, and a filesystem-level integrity state space — must be compared, and it is the comparison itself that gets audited.
>
> We organise them as the fibres of a Grothendieck fibration whose base is a poset of scales `(Λ, ≤)`. Reindexing functors `f*: F_σ → F_σ′` transport an observable between fibres, and their composition is required to reproduce the coarse-graining (renormalisation-group) semigroup. **No canonical cleavage exists**; hence every fibre-to-fibre comparison presupposes a choice of cartesian lift. We identify that choice with the observer, and we show that the failure of the resulting lax comparison to commute is **not a "loss of information" but a measured 2-cell** `α`, whose modulus is the numerical tolerance of the solver: the laboratory rule *declare window, unit and threshold before measuring* becomes, formally, the specification of the **support** of `α`.
>
> Two measurements anchor the claim. (i) For the transverse-magnetic cone at `α = 30°`, the complete (`L4`) reading of the sealed discrete field lies **0.4105 % below** the mesh-extrapolated continuum branch (`0.7739676586994475` against `0.777157703748551`). (ii) At `dx/λ = 0.0250` (241 nodes) the ratio `R_L4 / R_intrínseco` spans **1.0069 · 1.0098 · 1.0223 · 1.0252 · 1.0331** over five measured geometries — an envelope of **+0.69 % to +3.31 % over n = 5**. The excess is a **transient mesh prefactor**, not a bound attached to the cell size: its amplitude is set by the geometry, its maximum is reached by the most grazing case (`α = 26.5651° · m = 17`), and the same decay law holds in all three geometries followed through 61/121/241 nodes (fitted exponent `p ≈ 1.93 … 1.95` at `λ/40`).
>
> Finally we separate two notions that are routinely conflated. **A SHA-256 digest is a discrete classifier in the base category**: it decides strict isomorphism `A ≅ B` on disk, and it carries **no Noether charge**. The conserved quantity lives in the **continuous fibre**, and the classifier can neither see it nor be asked to. Consistency across fibres is therefore not a property of any single artefact: it is **the magnitude of a declared 2-cell**, and it is falsifiable.

---

## §2 · RESUMEN (ES, para el aparato crítico)

Un mismo objeto tiene varias descripciones efectivas (cono analítico continuo · solver Yee/FDTD discreto · espacio de estados de integridad en disco) y lo que se audita no es ninguna de ellas por separado: **es la comparación**. Se organizan como **fibras** de una fibración de Grothendieck sobre un poset de escalas `(Λ, ≤)`; el transporte entre fibras es un **functor de reindexación** `f*`, y su composición reproduce el **semigrupo de coarse-graining** (grupo de renormalización). Como **no hay clivaje canónico**, toda comparación entre fibras **exige fijar un levantamiento cartesiano**: esa elección **es el observador**. El defecto de conmutación no es pérdida: **es una 2-celda laxa medida**, y su módulo **es la tolerancia numérica** declarada. El hash es **clasificador discreto en la base**; la carga conservada vive en la fibra continua.

---

## §3 · TABLA DE DEFINICIONES CATEGÓRICAS

`estado`: **MEDIDO** (hay comando y crudo de esta sesión) · **DECLARADO** (estructura afirmada, sin medición propia) · **SIN CASA** (0 anclas en el corpus) · **AJENO** (entra por referencia).

| # | objeto | qué es | dónde vive en el repo | comando / ancla que lo respalda | estado |
|---|---|---|---|---|---|
| 1 | **Base `(Λ, ≤)`** | poset de escalas de discretización | `sim/control_pareado_convergente.py` bloques A/B/D | `grep -n 'dx/l' /tmp/cp_mio_20261011.log` | DECLARADO |
| 2 | **Escala `λ ∈ Λ`** | espaciado por longitud de onda | bloque B, columna `dx/l` | `0.1000 · 0.0500 · 0.0250` (nodos 61·121·241) en el log | MEDIDO |
| 3 | **Fibra `F_λ`** | teoría efectiva heterogénea en esa escala | bloque B (Yee) · bloque C (FDTD sellado) · bloque A (analítico) | `sed -n '40,130p' /tmp/cp_mio_20261011.log` | MEDIDO |
| 4 | **Objeto de la fibra** | observable `R` (razón de amplitudes / cociente) | campo `R4_sobre_R_intrinseco` y `yee.{L1_naive,L2_lector,L4_completo}` del JSON sellado | `sha16 41fce209adc05f98` (capa JSON interna: `field_solver 8cfca6a9bff5fee7 · lector 9fab4e04d281d3cc · maxwell2d 1db75ea7b0b8cba4`) | MEDIDO |
| 5 | **Reindexación `f*: F_σ → F_σ′`** | transporte del observable entre mallas | bloque B / gate vivo | `derivada con la malla (lam/10 -> lam/20): {'26.5651': (0.7136222385918988, 0.7125074731962245), '30.0': (0.777157703748551, 0.777157703748551)}` | MEDIDO |
| 6 | **Ley de composición `f* g* = (gf)*`** | el semigrupo RG | — | sólo hay **un par** de niveles impreso ⇒ composición **no medida** | DECLARADO |
| 7 | **2-celda laxa `α`** | defecto de no-conmutación = **ε numérico** | `R_L4 / R_intrínseco` | `−0.4105 %` (fibra discreta vs continua) · `+0.69 % … +3.31 %` (**cinco** geometrías, `dx/λ = 0.0250`) | MEDIDO |
| 8 | **Clivaje (*cleavage*)** | elección del levantamiento cartesiano | el **lector** elegido: `L1_naive` / `L2_lector` / `L4_completo` | `grep -n 'L1 naive\|L4 completo' sim/control_pareado_convergente.py` (l.238 · l.404) | MEDIDO |
| 9 | **No-canonicidad del clivaje** | `s` (lift) es extrínseco: el objeto **no es testigo de su propio lift** | memoria de método del dueño (`como-mirar.md`) | no hay comando en repo que lo mida | DECLARADO |
| 10 | **Clasificador discreto en la base** | `sha256` decide `A ≅ B` en disco | `bundle/HASHES.sha256` · `tools/verificar_bundle.sh` · sha16 de §0 | `shasum -a 256 <f> \| cut -c1-16` | MEDIDO |
| 11 | **Carga conservada (Noether)** | vive en la **fibra continua**, no en la base | — | `Noether` = **0 líneas / 0 archivos** en las tres raíces | SIN CASA |
| 12 | **Nulo de la 2-celda** (par enfrentado) | control de saturación, cota `\|E\|` | bloque B, familia `contra 0.0` | `R_L4/R_intr = 1.0000` **exacto** a las tres mallas | MEDIDO |
| 13 | **Universo cero** (copropagante) | fila sin señal: `R_intr(ref) = 0.000000` ⇒ razones `nan` | bloque B, familia `copropagante 0.0` | `na_extra L2 0 L4 0` (declarado por el instrumento) | MEDIDO · **EXCLUIDO** |
| 14 | **Auditor *fail-closed*** | guarda que decide si hay algo que medir **antes** de la identidad | `tools/verificar_bundle.sh` (guarda de cero entradas, `RC=2`) | `RC` esperado + causa impresa | DECLARADO |

### Comentario de la fila 8–9 (la corrección del dueño)
En el **clivaje** el observable tiene **muchas** preimágenes y el lift `s` **elige una**: la ida es múltiple y la vuelta es **extrínseca**. Por eso **no hay clivaje canónico que elegir**: lo que hay es **un clivaje declarado**. «La Capa 12» es exactamente ese sitio: **no una capa más, sino la elección del levantamiento**.

---

## §4 · Las tres correcciones del dueño, incorporadas

**(1) «El Hash es un clasificador discreto en la base, no una carga de Noether.»**
El digest vive en la **categoría discreta** de los estados en disco: su único trabajo es decidir `A ≅ B`. No conserva nada, no viaja a la fibra continua y no puede ser testigo de una magnitud. Ver filas 10–11: `clasificador` tiene casa (**318 líneas · 332 ocurrencias · 129 archivos**), `Noether` **no tiene ninguna**.

**(2) «Las tolerancias numéricas son el defecto de una transformación pseudonatural.»**
El error no es **pérdida**: es la **magnitud de la 2-celda** `α` que mide cuánto no conmuta el diagrama, con `‖α_{f,g}‖ ≤ ε`. La regla de laboratorio (**declarar ventana, unidad y umbral antes de medir**) queda así como **la especificación del soporte de `α`**, no como una precaución de estilo. Las cifras: el exceso de discretización a `λ/40` es una **envolvente de prefactores transitorios** `+0.69 % … +3.31 %` sobre `n = 5` geometrías (§5.b) — **no** una cota `≤ 2.5 %` — y la brecha fibra discreta/continua es `−0.4105 %` (§5.a).

**(3) «Capa 12 como clivaje no canónico (*cleavage*).»**
El observador **es** la elección del levantamiento cartesiano; no existe un clivaje universal canónico ⇒ **toda proyección exige fijar una sección**. Corolario ya medido en la casa: **el objeto no es testigo de su propio lift** ⇒ un verificador **no puede auditar su propio archivo** sin un metro externo o una fase desacoplada. (Familia ya conocida: «el instrumento que se cuenta a sí mismo», «un instrumento que reporta su propio acto no es testigo de su objeto».)

---

## §5 · CADENA DE LAS DOS CIFRAS DEL ABSTRACT

### §5.a · `−0.4105 %` — la 2-celda fibra discreta vs fibra continua

```
UNIVERSO DECLARADO: no hay universo de archivos; los tres operandos salen del mismo
                    log /tmp/cp_mio_20261011.log (143 l · sha16 53b628188aa35e19).
                    MOTOR python3 -B.  VENTANA 2026-10-11T17:43:36Z.  RC=0.
```
| operando | valor | de dónde |
|---|---|---|
| numerador: `rel L4` (bloque C, `colineal N=1`) | `0.773967659` | mi log, 9 decimales |
| numerador (16 d, del acta de prosa) | `0.7739676586994475` | `VEREDICTO_CONTROL_PAREADO_20261011.md` sha16 `a6316f8db84d8885` |
| denominador: referencia continua extrapolada | `0.777157703748551` | mi log, gate vivo: `derivada con la malla (lam/10 -> lam/20) {'30.0': (0.777157703748551, 0.777157703748551)}` |
| denominador (9 d) | `0.777158` | mi log, bloque A `estrella 30.0000 4` |

`python3 -B -c "print('%.4f %%' % ((0.7739676586994475/0.777157703748551-1)*100))"` → `-0.4105 %`

**Control de precisión (hecho):** la cifra se reproduce **con las tres combinaciones** —
`log9/ana9 = -0.4105 %` · `log9/acta16 = -0.4105 %` · `acta16/ana16 = -0.4105 %`.
⇒ la cifra **no depende** de cuántos decimales se imprimieron. Ese es el respaldo.

**Advertencia obligatoria (no es un detalle):** el denominador `0.777157703748551` **NO es una forma cerrada**: es un valor **derivado de la malla**, y lo que lo habilita como denominador es que **coincide consigo mismo en `λ/10` y en `λ/20`** (los dos elementos de la tupla son iguales). Se declara: *referencia de continuo extrapolada por malla*, no solución analítica.

**Lectura hermana (misma 2-celda, en grados):** `α_efectivo` del valor sellado — `L2_lector = 28.2505°` · `L4_completo = 29.8305°`, contra `ALPHA_REF_DEG = 30.0°` ⇒ la lectura completa queda a **−0.1695°**. Rotulada **DECLARADO**: se obtiene **interpolando el cono 3D** entre `26.5651` y `30`, según el propio crudo.

### §5.b · El exceso de discretización a `dx/λ = 0.0250` — prefactor geométrico, **no** una «banda de malla»

```
UNIVERSO DECLARADO: las 5 geometrías con fila a dx/l = 0.0250 (nodos 241) que existen
                    en los crudos del falsador; más la secuencia de malla 61/121/241 de
                    las 3 geometrías corridas en las tres mallas.
                    Crudos: v1 4c9350125fa9b6d2 · v2 19e1f4bf0b647154 (archivo
                    falsador-geometria-20261011, adenda sha16 694c19ad2ee78459).
                    Denominador = referencia intrínseca de la MISMA geometría: filas
                    `cruce` con referencia analítica (`sin α`), filas `abanico` con el
                    `L0_exacto` a 361 nodos.
                    MOTOR python3 -B (json + math).  VENTANA 2026-10-11T19:02:42Z.  RC=0.
```
| geometría @ `dx/λ = 0.0250` | `R_L4 / R_0` | exceso | prefactor efectivo `C` (con `p = 2` fijado) |
|---|---|---|---|
| `cruce 30.0000` | `1.0069340` | `+0.6934 %` | `11.0944` |
| `cruce 26.5651` | `1.0098361` | `+0.9836 %` | `15.7377` |
| `abanico 30.0 · m=9` | `1.0223409` | `+2.2341 %` | `35.7454` |
| `abanico 30.0 · m=17` | `1.0252258` | `+2.5226 %` | `40.3613` |
| `abanico 26.5651 · m=17` | `1.0331377` | `+3.3138 %` | `53.0204` |

`filas=5  min=1.006934  max=1.033138  ->  +0.69 % … +3.31 %`

**La envolvente a `dx/λ = 0.0250` es `[1.0069, 1.0331]` ⇒ `[+0.69 %, +3.31 %]`** sobre `n = 5` geometrías. El máximo `+3.3138 %` corresponde a la geometría **más rasante** ensayada (`α = 26.5651° · m = 17`).

**Secuencia de malla** (mismo instrumento y misma receta; sólo cambia `nodos`):

| geometría | `dx/λ = 0.1000` (61) | `0.0500` (121) | `0.0250` (241) | `p`(61→121) | `p`(121→241) |
|---|---|---|---|---|---|
| `abanico 30.0 · m=17` | `+33.9658 %` | `+9.6907 %` | `+2.5226 %` | `1.8094` | `1.9417` |
| `abanico 26.5651 · m=17` | `+43.0890 %` | `+12.6034 %` | `+3.3138 %` | `1.7735` | `1.9273` |
| `abanico 30.0 · m=9` | `+30.4986 %` | `+8.6149 %` | `+2.2341 %` | `1.8238` | `1.9471` |

**Lo medido, en tres partes:**

1. **El exponente es común a las tres geometrías.** Las tres caen juntas: `p`(61→121) = `1.81 / 1.77 / 1.82` y `p`(121→241) = `1.94 / 1.93 / 1.95`. **Declarado:** el valor **medido** es `p ≈ 1.93 … 1.95` a `λ/40`, que **tiende a `2` por abajo sin alcanzarlo** ⇒ el régimen asintótico de segundo orden **no está saturado en esta ventana**. Escribir `O(dx²)` es correcto como **orden de la ley** (idéntico para todas las geometrías); escribir `= 2` exigiría una malla más fina.
2. **La amplitud sí depende de la geometría.** El **prefactor efectivo** `C` separa la geometría más rasante de la más alineada por un factor `53.02 / 11.09 ≈ 4.78` (a `p = 2` fijado). Pero `C` y `p` **no son independientes**: `C` sólo existe **junto a un `p` declarado** (con el `p` medido `1.9273` la geometría rasante da `C ≈ 40.4`, no `53.0`). ⇒ Se publica **el par** `(p, C)`, nunca `C` solo.
3. **`dx/λ = 0.0250` es un punto de operación, no el continuo.** Los tres excesos son **colas de convergencia**, no cotas del error convergido.

⇒ **Rótulo depurado.** La envolvente `[+0.69 %, +3.31 %]` es el **rango de prefactores transitorios a `λ/40`** sobre `n = 5` geometrías: **el máximo lo fija la geometría elegida, no el paso de malla.** El término **«banda de malla» queda depreciado**.

> ### ⛔ DEFECTO ROTULADO — se conserva, no se borra
> **(a)** La prosa sellada escribe el error de discretización espacial como **`≤ 2.5 %`**. Medido: `2.52 %` era el **máximo de tres geometrías** (`n = 3`), **no una cota demostrada**; con la cuarta y la quinta geometría el máximo sube a **`3.31 %`**. **Un máximo de muestra presentado como cota** es un rótulo ancho, no un error de cifra.
> **(b)** El rótulo **«banda de malla»** (propiedad de `dx/λ = 0.0250`) quedó **FALSADO**: la banda no se movía por la malla sino por **qué geometrías se habían elegido**. Falsador pre-registrado ejecutado en sandbox (`RC=0`), veredicto **FALSADO**, con la geometría `α = 26.5651 · m = 17` cayendo **fuera** de `[1.0069, 1.0252]`.
> ⇒ En el abstract la cifra viaja como **«envolvente de prefactores transitorios a `λ/40` sobre `n = 5` geometrías»**, y **jamás** como `≤ 2.5 %` ni como «propiedad de la malla».
> *No se reparó la prosa sellada* (regla: la pieza vieja sólo recibe apéndices). Se declara aquí.

### §5.c · Nulos y controles de la 2-celda (obligatorios para que `α` no sea un adorno)

| control | valor | qué prueba |
|---|---|---|
| `contra 0.0` (par enfrentado) | `R_L4 / R_intr = 1.0000` **exacto**, a las tres mallas | la 2-celda **se anula** donde debe: el defecto no es del instrumento |
| `abanico m=2 · R_intr = sin(α)` | `0.447214` @ `26.5651°` · `0.500000` @ `30.0°` | la fibra de referencia **reproduce la geometría exacta** |
| `par enfrentado puro` | `R_intr = 1.000000` | saturación declarada (cota `\|E\|`) |
| `copropagante` | `R_intr = 0.000000` ⇒ razones `nan` | **universo cero**: `nan` **por construcción**, no un resultado. **NO CITAR como razón.** |

---

## §6 · LO QUE **NO** ENTRA EN EL ABSTRACT (y por qué)

1. **Las 13 capas / la numerología.** Vocabulario del corpus, no del marco. Entra como contexto del aparato, nunca como estructura del argumento.
2. **`Noether` como término del marco.** Medido: **0 líneas** en las tres raíces ⇒ **sin casa**. Se usa sólo como *contraste negativo* (lo que el clasificador **no** transporta) y va rotulado.
3. **`clivaje · cleavage · cartesian lift · celda laxa · pseudonatural`.** Medido: **0 líneas / 0 archivos** en las tres raíces ⇒ vocabulario **nuevo**, entra **por declaración**, no por autoridad (y se declara que se declara).
4. **`fibración`.** Medido: **2 líneas · 1 archivo**, y ese archivo la clasifica **`AJENO`** (`mesa/como-se-forma-un-espiral-20260925/ACTA_...md:564` y `:612`). ⇒ El propio corpus ya había marcado el término como **prestado**. Aquí entra como `[REF]·AJENO`, **sin elevar**.
5. **`canónico` en el sentido categórico.** ⚠️ **Colisión de namespace medida y declarada:** en este corpus `can[oó]nic` = **624 líneas · 660 ocurrencias · 280 archivos**, y el sentido dominante es **«pareja canónica» / «sus canónicos» / «dos canónicos»** = **ruta canónica · dueño único del estado**. Es un **objeto distinto** de *clivaje canónico*. ⇒ En el abstract, **la primera vez que aparezca la palabra se declara cuál de los dos sentidos se usa**.

---

## §7 · FALSADOR PRE-REGISTRADO (barato, antes de cualquier corrida nueva)

> **Hipótesis:** la banda `+0.69 % … +2.52 %` es **propiedad de la malla**, no del observable ni de la geometría.
> **Falsador:** añadir una **cuarta** geometría a `dx/λ = 0.0250` (p. ej. `abanico m = 9` o `α = 26.5651 · m = 17`).
> **Predicción falsable:** si el exceso cae **dentro** de `[1.0069, 1.0252]`, la banda **no se mueve** y se sostiene el rótulo «banda de malla». Si cae **fuera**, el rótulo es defectuoso: la banda **no era de la malla** sino de **qué geometrías se eligieron** (familia: «una cifra 3/3 puede ser artefacto de los 3 casos que YO elegí»).
> **Costo:** una corrida del mismo instrumento, `--sin-escribir`. **Cero escritura en repo.**
> **Estado:** **EJECUTADO** (2026-10-11, sandbox `/tmp/falsador_geometria/` y `/tmp/falsador_geometria_v2/`, `RC=0`, repo intacto: instrumento `2829d1e1ce1ee7e4` sin mover). **Veredicto: FALSADO** — `α = 26.5651 · m = 17` cae **fuera** de `[1.0069, 1.0252]` con `1.0331377` (`+3.3138 %`). El resultado se incorpora en §5.b; la hipótesis, el falsador y la predicción de arriba se conservan **verbatim** porque son el pre-registro.

---

## §8 · PENDIENTES (declarados, no adjudicados)

1. **El id estable.** Sigue pendiente (ya venía abierto del ciclo D23 · `§31`).
2. **La no-canonicidad como medición.** Hoy fila 9 es `DECLARADO`: no hay comando en repo que mida el defecto del lift. El candidato más cercano es `R_intr` de `abanico m=2 = sin(α)`, pero eso mide **la geometría**, no **la elección**.
3. **La colisión de `canónico`** (§6.5): declarada y medida; **no reparada**.
4. **La composición `f* g* = (gf)*`** (fila 6): sólo hay un par de niveles impreso. Con **tres** niveles de malla el semigrupo RG pasaría de `DECLARADO` a `MEDIDO`. Es la mejora de mayor rendimiento por unidad de costo.

---

## §9 · TÍTULOS CANDIDATOS (para el envío)

- `Fibred Structures and Lax Invariance across Heterogeneous Computational and Physical Regimes`
- `A Multiscale Categorical Framework for Epistemic Consistency in Multiphysics Solvers`
- `No Canonical Cleavage: tolerances as the support of a measured 2-cell`

Destino natural: *Applied Category Theory* · *Foundations of Physics* · *Synthese*.

---

## §10 · ERRATAS DE MOTOR DE ESTA SESIÓN (se registran; no se reparan)

Mismo día, tres ceros/cifras que **no eran del objeto**:

1. **Universo declarado ≠ universo recorrido.** Se declararon **tres** raíces y el `cd` dejó el recorrido en **una** ⇒ tres ceros que eran del **motor**.
2. **`$ROOTS` sin comillas en zsh NO se parte en palabras.** `grep` recibió **una sola ruta inexistente** ⇒ **cero en TODO**, incluido `can[oó]nic`, que tiene 280 archivos. *Familia: el cero puede ser del metro, no del objeto.*
3. **`-l` y `-c` en la misma invocación.** Conté el mismo objeto dos veces y el par salió idéntico (`280 / 280`, `129 / 129`), que es la firma de la mezcla. Separadas, las unidades quedan: `can[oó]nic` = 624 líneas / 660 ocurrencias / 280 archivos.

**Regla que sale de aquí:** *si un cero contradice una pieza que sabes que existe, el cero es del metro.* Se mide el motor **antes** de creer la cifra.
