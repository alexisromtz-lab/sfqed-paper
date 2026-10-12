# PREREGISTRO — EL EXPONENTE DE CONVERGENCIA `p` CON UNA TERCERA MALLA

**Archivo:** `sim/PREREGISTRO_CONVERGENCIA_P_20261012.md`
**Estado:** SELLADO ANTES DE LA PRIMERA CIFRA PROPIA.
**Naturaleza:** DISENO. Este documento **no mide `p`**. Nombra el objeto, la malla, el
estimador, las bandas y las guardas. La cifra la produce el comando del §7, y **nace
despues** de este archivo; el orden de los `mtime` es la evidencia (§8).
**Ventana del sello (UTC):** `2026-10-12T06:13:36Z` (medida con `date -u` en la corrida
del gate de pre-vuelo A2.1 sobre este mismo destino, que devolvio `RC=10` — no existia:
nada con que colisionar).
**Padres declarados (donde vive el pendiente):**
`sim/PREREGISTRO_INVOCACION_LECTOR_INVARIANTES_20261012.md:243` ·
`sim/PREREGISTRO_PARIDAD_CONMUTADOR_V2_20261012.md:118` ·
`sim/ACTA_DEL_FALSO_ROJO_DE_V1_Y_EL_VETO_SUSTANTIVO_DE_V5_20261011.md` §7 ·
`sim/ACTA_DEL_CICLO_V2_EL_VERDE_5_5_Y_EL_DESFASE_DECLARADO_20261012.md` §9.

---

## §0. ALCANCE

Se pre-registra la **extraccion del exponente de convergencia asintotico `p`** de la
cadena analitica (geometria + `field_solver`) mediante un **tercer escalon de malla**
que este documento elige **antes** de ver su salida.

`p` ya tiene **dos escalones medidos** y ninguno es propio de este ciclo (§0.3). Con dos
escalones se obtiene **una** pendiente y **dos** la fijan; el tercero es el primero que
**sobredetermina**: si los tres no caen en una recta en el plano `log eps` vs `log h`,
no hay ley de potencia que extraer y el exponente seria un ajuste, no una medida.

Regla que gobierna el ciclo, verbatim del sello §0.1 de
`sim/PREREGISTRO_PARIDAD_CONMUTADOR_20261011.md`:

> "dos escalones no extraen un exponente: lo fabrican."

---

## §0.1 COLISION DE NOMBRE: `lambda/40` ES DOS OBJETOS EN DOS INSTRUMENTOS

Esta seccion existe porque la doctrina vigente tiene escritas **las dos** frases y ambas
son verdaderas:

- `lambda/40` **NO es malla elegible** — `sim/ACTA_DEL_FALSO_ROJO_DE_V1_Y_EL_VETO_SUSTANTIVO_DE_V5_20261011.md` §7 ·
  `sim/PREREGISTRO_PARIDAD_CONMUTADOR_V2_20261012.md` §8 ·
  `sim/PREREGISTRO_INVOCACION_LECTOR_INVARIANTES_20261012.md` §7 A4.
- la tercera malla del estudio de `p` se escribe **`lambda/20`, `lambda/40`, `lambda/80`** —
  `sim/PREREGISTRO_PARIDAD_CONMUTADOR_20261011.md` §0.1.

No hay contradiccion: hay **un nombre con dos casas** y hay que declararlo antes de medir
(doctrina: *un nombre con casa leido como moneda nueva*).

| | instrumento | donde vive | naturaleza | elegible? |
|---|---|---|---|---|
| `lambda/40` (A) | cadena **FDTD** | `sim/maxwell2d.py:63` — `DX_OVER_LAMBDA = 1.0/40.0` | constante **sellada / heredada**, no elegida | **NO** |
| `lambda/40` (B) | cadena **analitica** | `sim/control_pareado_convergente.py` → `malla_2d(nodos)` con `nodos = 241` | rejilla **elegida libremente**, hermana de 61 y 121 | **SI** |

Las seis cifras de `p` que ya existen (§0.3) salen de la casa **(B)**. La prohibicion de
`lambda/40` habla de la casa **(A)**. Por eso:

- **La malla nueva NO se elige en la casa (A).** El FDTD no entra a este estudio: su paso
  de malla es constante sellada y moverlo seria editar el instrumento.
- **La malla nueva se elige en la casa (B)**, donde `nodos` es un parametro libre y la
  sucesion `61 / 121 / 241` esta simplemente escrita en `main()`.

Corolario que el ciclo paga: **la casa (A) queda citada y descartada por nombre propio**;
no se la re-mide, no se la re-etiqueta, no se la edita.

---

## §0.2 REGLA DE ELEGIBILIDAD DE MALLA (pre-registrada)

Una malla es **elegible** si y solo si se cumplen las tres:

1. **Es hermana de las que ya existen**, es decir, la produce la **misma receta** que
   produjo las cifras ya publicadas: mismo instrumento, misma geometria, misma ventana,
   misma referencia intrinseca. Cambiar la receta obliga a otro pre-registro.
2. **Conserva la ley de afinamiento.** Las tres mallas existentes son
   `nodos = 60 * 2**k + 1` con `k = 0,1,2` sobre un dominio de lado fijo `LADO = 6.0`
   `[declarado en el instrumento]`, luego `h = LADO * LAMBDA / (nodos - 1) = 0.1 * 2**(-k)`
   **exactamente**: cada escalon **divide `h` por 2**. Eso hace que el denominador del
   estimador, `log(h1/h2)`, valga `log 2` en **todos** los escalones y que los `p` sean
   comparables sin normalizacion. Una malla que no doble no es hermana: es otro estudio.
3. **No mueve el instrumento.** La malla se pide por parametro; no se edita el motor.

Bajo (1)-(3) la malla elegible siguiente es **`nodos = 481`** (§3), y **es la unica**:
`k = 3`.

---

## §0.3 LO HEREDADO: NO SE RE-MIDE, NO SE RE-ETIQUETA

Las cifras de abajo **no son de este ciclo**. Se citan para fijar el objeto y el
estimador; **no se re-miden** y **no se re-adjudican**.

**Fuente:** `sim/marco-fibrado-20261011/ABSTRACT_Y_TABLA_CATEGORICA_20261011.md` §5.b.
**Crudos citados:** v1 `4c9350125fa9b6d2` · v2 `19e1f4bf0b647154`
(archivo `falsador-geometria-20261011`, adenda sha16 `694c19ad2ee78459`).
**VENTANA de esa medicion:** `2026-10-11T19:02:42Z`. `RC=0`.

| geometria | `dx/l = 0.1000` (61) | `0.0500` (121) | `0.0250` (241) | `p` (61->121) | `p` (121->241) |
|---|---|---|---|---|---|
| `abanico 30.0 · m=17` | +33.9658 % | +9.6907 % | +2.5226 % | 1.8094 | 1.9417 |
| `abanico 26.5651 · m=17` | +43.0890 % | +12.6034 % | +3.3138 % | 1.7735 | 1.9273 |
| `abanico 30.0 · m=9` | +30.4986 % | +8.6149 % | +2.2341 % | 1.8238 | 1.9471 |

**Estimador implicito, reconstruido y verificado en este sello** (aritmetica declarada, no
supuesta): con `eps(h) = R(h) - 1` = **exceso relativo** sobre la referencia intrinseca,

```
p(h1 -> h2) = log( eps(h1) / eps(h2) ) / log( h1 / h2 )
```

Control de reconstruccion hecho a mano en el acto del sello, sobre la fila 1:
`log(0.339658 / 0.096907) / log 2 = 1.8094` **coincide** con el `p` publicado; y
`log(0.096907 / 0.025226) / log 2 = 1.9418` **coincide** con el segundo. La fila 3 da
`1.8242` y `1.9470` contra `1.8238` y `1.9471` publicados (**las dos cifras se imprimen;
la diferencia es de redondeo de la tabla citada, no del estimador**).

**Lectura heredada, verbatim de §5.b:** *"El exponente es comun a las tres geometrias …
`p ~ 1.93 … 1.95` a `lambda/40`, que tiende a `2` por abajo sin alcanzarlo => el regimen
asintotico de segundo orden no esta saturado en esta ventana. Escribir `O(dx^2)` es
correcto como **orden de la ley**; escribir `= 2` exigiria una malla mas fina."*

Esa ultima frase **es** el pendiente que este pre-registro ataca.

---

## §1. UNIVERSO DECLARADO

```
UNIVERSO DECLARADO: las 3 geometrias de abanico con secuencia completa en los crudos
  citados de §0.3 (abanico 30.0 m=17 · abanico 26.5651 m=17 · abanico 30.0 m=9),
  extendidas a un cuarto nodo de malla.
DENOMINADOR: referencia INTRINSECA de la MISMA geometria — familia `cruce`: referencia
  analitica (`sin alpha`); familia `abanico`: `L0_exacto` a 361 nodos. NUNCA se compara
  una geometria contra otra: el denominador de cada residuo es su propia geometria.
MOTOR: `python3 -B` (json + math) para las cifras heredadas; el motor del escalon nuevo
  es el del §7 y queda declarado al sellarlo — no se pre-declara un motor que aun no
  corre (un motor supuesto no es un motor declarado).
UNIDAD: `nodos` por lado (unidad del objeto) y `h = dx/lambda = LADO/(nodos-1)` (unidad
  del afinamiento). Las dos viajan juntas: una cifra de `p` sin su par de mallas y sin
  su `h` no es una cifra de `p`.
VENTANA: la del sello es `2026-10-12T06:13:36Z`; la del escalon nuevo se imprime con la
  corrida. Toda cifra de este estudio viaja con su hora.
UMBRAL: las bandas de §4, pre-registradas AQUI, antes de la corrida.
```

---

## §2. EL OBJETO Y EL ESTIMADOR (definidos antes de medir)

**El objeto** no es `p`: es la terna `(R, h, geometria)` y su residuo `eps = R - 1`, donde
`R` es la lectura de la componente declarada del campo contra la referencia intrinseca de
la misma geometria. `p` es una **funcion de dos escalones**, no una propiedad de un punto.

**Los tres escalones del estudio completo, ya nombrados:**

| escalon | par de mallas | `h1/h2` | estado |
|---|---|---|---|
| E1 | 61 -> 121 | 2 | **heredado** (§0.3) |
| E2 | 121 -> 241 | 2 | **heredado** (§0.3) |
| E3 | 241 -> 481 | 2 | **a medir** (el de este pre-registro) |

**Guarda del estimador (obligatoria antes de la primera cifra del escalon nuevo):**
1. `eps(h) > 0` en las tres mallas. Un `eps <= 0` no es un residuo: es otra cosa
   (saturacion o cambio de signo) => **CONTRATO ROTO**, no un `p` negativo.
2. `log(h1/h2) != 0` y **el mismo** en todos los escalones (`log 2`). Si un escalon no
   dobla, los `p` no son comparables => **CONTRATO ROTO**.
3. Con menos de **tres** escalones **no se emite veredicto**: `SIN MEDIDA`. Un `p` de dos
   puntos es un ajuste con cero grados de libertad.

---

## §3. LA MALLA NUEVA — `nodos = 481` (`dx = lambda/80`)

```
nodos = 481   =>   h = LADO * LAMBDA / (nodos - 1) = 6.0 / 480 = 0.0125  =  1/80
h(241) / h(481) = 0.025 / 0.0125 = 2.000000  exacto
```

`481 = 60 * 2**3 + 1`; `481 - 1 = 480 = 4 * 120`. La malla es **estrictamente anidada**
con las tres existentes (mismo dominio `6 x 6`, mismo origen) y **el afinamiento es
exacto**: no se interpola, no se extrapola, no se re-muestrea.

**Radio de accion declarado:** `nodos = 481` multiplica por 4 el numero de nodos de 241 y
por ~16 el coste de la corrida mas cara. Se declara **costo**, no se disimula: si la corrida
no termina, el veredicto es `SIN MEDIDA`, nunca un verde parcial.

**Lo que esta malla NO es:** no es un punto del continuo (ya estaba escrito: *"`dx/lambda =
0.0250` es un punto de operacion, no el continuo"*), y no es una malla del FDTD (§0.1).

---

## §4. PREDICCION FALSABLE Y BANDAS (pre-registradas)

**Hipotesis bajo prueba:** el residuo sigue una ley de potencia `eps(h) = C * h**p` con
**`p = 2`** en el limite, y la sucesion converge **desde abajo**.

**Prediccion concreta para E3 (241 -> 481), por geometria:**

```
p3 = p(241 -> 481)  en  [1.96, 2.00)   y   p3 >= p2   (convergencia desde abajo)
```

Justificacion declarada, no elegida: los increments observados entre E1 y E2 son
`+0.1323` (g1) · `+0.1538` (g2) · `+0.1233` (g3). Un regimen que se satura en 2 desde
abajo con una correccion de orden superior **positiva** predice un tercer incremento menor
que el segundo. Un incremento igual o mayor seria compatible con una ley distinta.

| banda | regla | veredicto |
|---|---|---|
| **VERDE** | `1.96 <= p3 < 2.00` y `p3 >= p2`, en **las tres** geometrias | segundo orden saturado en la ventana |
| **GRIS** | `1.90 <= p3 < 1.96` | segundo orden **en camino, no saturado**: exige 4a malla (`nodos = 961`, `h = lambda/160`) |
| **ROJO · NO-SATURA** | `p3 < 1.90` | el exponente **no** converge a 2 en esta ventana: la etiqueta `O(dx^2)` como ley asintotica queda **refutada en el rango medido** |
| **ROJO · SOBREPASO** | `p3 >= 2.00` | la prediccion "desde abajo" **es falsada**: o el esquema tiene orden mayor que 2, o el tercer escalon salio del regimen asintotico |
| **ROJO · NO-MONOTONO** | `p3 < p2` en cualquier geometria | la recta no existe: **no se promedian geometrias** (promediar escondería justo el defecto) |
| **MIXTO** | las tres geometrias no caen en la misma banda | **se declara, no se adjudica** |

**Prohibicion escrita:** `p = 2` **exacto** no se escribe nunca como resultado. Que el
exponente sea 2 es la hipotesis; lo que se mide son tres pendientes.

**Prohibicion heredada que se conserva:** `C` y `p` no son independientes (§5.b de la
fuente). Se publica **el par** `(p, C)`, nunca `C` solo, y nunca un `p` sin su par de
mallas.

---

## §5. CONTROLES (el arnes se prueba antes de juzgar)

Seis controles, con su causa impresa. **Un caso que devuelve el codigo esperado por otro
motivo no discrimina**: cada control imprime **que** defecto midio.

- **C0 — CERTIFICADO DEL ARNES (corre primero, en serie).** El comando nuevo, corrido con
  la receta heredada en `nodos = 61, 121, 241`, debe **reproducir las seis cifras de `p` de
  §0.3** (`1.8094 · 1.7735 · 1.8238` y `1.9417 · 1.9273 · 1.9471`). Si **una** difiere en
  el ultimo digito impreso, el defecto es **del comando nuevo**, no del objeto:
  `CONTRATO ROTO`, `rc=2`, y **el escalon E3 no se mide**. Este certificado es lo que ata
  al instrumento viejo **sin editarlo** (la cadena de custodia del ciclo V2 esta `untracked`
  y un motor en vuelo no se toca).
- **C1 — POSITIVO (ley de potencia sintetica).** Serie construida con `eps(h) = C * h**p`
  exacta, para `p` en `{1.00, 1.50, 1.93, 2.00}`, evaluada en `h = 0.1, 0.05, 0.025, 0.0125`.
  El estimador debe devolver `p` con error `<= 1e-12` en los tres escalones. Si no,
  `CONTRATO ROTO`, `rc=2`: el metro es el defecto.
- **C2 — NEGATIVO (debe enrojecer).** Serie que **no** es ley de potencia, p.ej.
  `eps(h) = C * h * log(1/h)`. El instrumento **debe** dar `p != 2` y **distinto entre
  escalones**. Si un no-ley-de-potencia sale VERDE, `CONTRATO ROTO`, `rc=2`.
- **C3 — GUARDA DE CERO ENTRADAS.** El instrumento **cuenta los escalones antes de juzgar**.
  Con `< 3` escalones, o con `eps <= 0`, o con `log(h1/h2) == 0`: **`CONTRATO ROTO`**, `rc=2`.
  Un cero que cuadra consigo mismo es un verde falso.
- **C4 — CONTROL DE LA REFERENCIA.** El residuo `eps` se mide contra la referencia
  **intrinseca de la misma geometria**. El control es la fila ya publicada: `eps(h) -> 0`
  al refinar. Si `eps` **no decrece** al refinar en alguna geometria, el denominador esta
  mal puesto, no el objeto: `CONTRATO ROTO` con la causa impresa (cual geometria, que par).
- **C5 — BARRIDO DE BANDAS.** El instrumento imprime, en el mismo renglon, `p3` **y** la
  banda en que cae **y** la banda de E1 y E2. **Se imprimen las cuatro cosas**: un veredicto
  sin sus dos escalones previos no se puede auditar.

---

## §6. LO QUE ESTE DOCUMENTO **NO** HACE

1. **No mide `p`.** Cero cifras propias. Este archivo nace **antes** que las cifras.
2. **No re-mide los escalones E1/E2.** Se citan por slug completo, con su crudo y su hora.
3. **No toca `sim/maxwell2d.py`.** El instrumento sellado (`sha16 1db75ea7b0b8cba4`) no se
   edita; la casa (A) de §0.1 queda fuera del estudio.
4. **No re-etiqueta `sim/control_pareado_convergente.py`.** Verbatim del padre: *"eso es
   otro instrumento y no se re-etiqueta aqui"*. Se extiende su **receta**, por un comando
   nuevo, con certificado C0.
5. **No toca `sim/medidas_aN.csv`** (`sha16 4129d436e2cd081d`) ni la cadena de la ley
   `1/N`. Ese es otro objeto.
6. **No escribe en `bundle/`.** `bundle/` es inmutable.
7. **No adjudica** el desfase V2 ni el `mtime` movido de §0.2 del padre: siguen declarados.

---

## §7. EL COMANDO (nombrado; su construccion es una escritura aparte, con su gate)

```
python3 -B sim/driver_convergencia_p.py --nodos 61,121,241,481 --geometrias 3 --json
```

**Estado: PENDIENTE. No existe todavia.** Se nombra aqui para que el pre-registro tenga
destinatario; construirlo es un acto de escritura que exige su propio gate de pre-vuelo
(A2.1) y **no se hace sin orden**.

**Ruta declarada (la decision se toma por costo, no por gusto):**

- **Ruta A — extender `sim/control_pareado_convergente.py` en su `main()`.** Reusaria el
  motor exacto que ya produjo E1/E2 ⇒ C0 seria trivial. **Coste:** editar una pieza
  `untracked` de un ciclo en vuelo (`sha16 2829d1e1ce1ee7e4`), es decir mover un
  instrumento ajeno. **Rechazada por defecto.**
- **Ruta B — driver NUEVO que importe el instrumento viejo en modo lectura.** Importa
  `malla_2d`, `muestreo_yee`, `_lecturas2d`, `razon_2d` y la receta, y **no lo edita**.
  **Coste:** obliga al certificado **C0**, que es exactamente el control que la Ruta A
  podria esquivar. **Elegida.**

**Salida declarada:** un crudo en `sim/data/invariantes/` (nombre impreso por el propio
comando) con `UNIVERSO DECLARADO` y hora, y la linea atomica de cierre
`VEREDICTO · RC · MOTOR · SHA16 · CRUDO: <ruta>`. **Ninguna escritura fuera de ese
directorio.**

---

## §8. CRONOLOGIA (el orden es la evidencia, no los relojes leidos a ojo)

Se verifica con `os.stat().st_mtime_ns`, no con la lectura del texto:

```
mtime( este pre-registro )  <  mtime( sim/driver_convergencia_p.py )  <  mtime( crudo nuevo )
```

Si el comando **no existe** cuando se lee este archivo, la cronologia esta **truncada y se
declara truncada**: no se simula un orden que no ocurrio.

---

## §9. FUERZA Y ESTANTE

- **`n = 1`.** Nada de este ciclo se eleva a familia. Un tercer escalon es **un** escalon.
- **Estante:** `p` es **instrumento**, no medida del articulo — la etiqueta de la cadena
  analitica ya lo dice: *"verificacion del INSTRUMENTO, NO evidencia del articulo"*.
- **Nada de `p` entra en `main.tex`** en este ciclo. El abstract publica el par `(p, C)`
  declarado como tendencia sin saturacion; una cifra nueva de `p` no reabre el manuscrito
  sin orden explicita.
- **Guarda del ciclo:** *"muchas posiciones no son muchos objetos — y tampoco son
  evidencia."* Una malla mas **no** es una medicion mas: es **el escalon que hace
  sobredeterminada** a la que ya habia.
