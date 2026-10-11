# PREREGISTRO_VACIO_NO_LINEAL_20261011

Pre-registro del regimen NO LINEAL del vacio sobre las dos geometrias ya calibradas
(par colineal en el foco y par contra-propagante).

- Estado: **CERRADO**. Este documento NO se edita despues de su sello. Lo que ocurra al
  correr va a un reporte aparte, y toda correccion entra como apendice (§11), nunca como
  parche del texto.
- Costo: **0 de computo** (no se ha compilado ni corrido nada para escribirlo).
- Instrumento congelado: `sim/maxwell2d.py` sha16 `1db75ea7b0b8cba4` · 715 l.
- Manuscrito citado, no abierto: `main.tex` sha16 `90bfcb2b73ff9855` · 631 l (`79d372a`).
- Frontera de contencion: este archivo vive FUERA de `bundle/`
  (sello `0ce97cf9d8c44987`, 35 hojas / 34 entradas), que no se toca.

## §0 Reglas de entrada (heredadas del pre-registro hermano, cinco)

1. **Ninguna cifra de este documento se lee de una corrida.** Toda cifra entra por cita
   con sha16 de la pieza que la imprime, o por comando fechado; y toda cita lleva su hora.
2. **El resultado no se puede componer aqui.** Un pre-registro fija la clausula; no
   anticipa el veredicto. Donde el signo o la magnitud no se derivan del algebra ya
   sellada, se declara **no declarado** y se mide.
3. **Lo que la pieza afirma sobre si misma es TRAMPA.** `sha16`, lineas y bytes se miden
   fuera; una pieza no es testigo de su propia huella.
4. **Una salida que no puede diferir no es evidencia.** Los controles que son identidades
   algebraicas se declaran CANDADO, y el numero que producen no se lee como resultado.
5. **El defecto del dia no se repara aqui.** Se declara y se aisla; la clase se cierra en
   la pieza que la pueda cerrar.

## §1 Universo declarado, motor, unidad, ventana

- UNIVERSO DECLARADO: `sim/maxwell2d.py` · `sim/params.py` · `sim/filtro_analitico.py` ·
  `sim/fuego_sensible.py` · `sim/field_solver.py` · `sim/configs.json` · la subseccion de
  benchmark sellada de `main.tex` (l.439-555) y `sim/data/invariantes/*` (sellos de
  etapa 1). Ningun otro archivo entra a los conteos de este pre-registro.
- MOTOR: `python3 -B` (numpy) para el solver; `grep -n` / `re` sobre bytes para los censos.
- UNIDAD: **celda** para el soporte; **ocurrencia** para los censos de nombres; **adimensional**
  para `R`, `xi`, `kappa` y los pisos. Se declara la unidad en cada renglon que la use.
- VENTANA DE MEDIDA: celdas `[100, 380]` en x e y (`VENTANA_I0/I1`, halo de 20 celdas
  alrededor de cada plano fuente). Fuera de ella no se lee ninguna magnitud fisica.
- VENTANA UTC: la hora de redaccion y la hora de cada medicion acompanan a la cifra. Una
  cifra sin hora no es una cifra.

## §2 El objeto de estudio: dos canales, y por que la geometria calibrada los maximiza

**Canal 1 — cuadraticos en los invariantes (Heisenberg-Euler).** La densidad efectiva se
escribe como correccion **relativa** a la accion de Maxwell con los DOS invariantes que el
manuscrito ya usa:

    rho_HE  =  c_* * ( F^2 + 7 G^2 ) / E_cr^4          [relativo, adimensional]

con `F = eps0/2 (E^2 - c^2 B^2)`, `G = eps0 c E.B` (la normalizacion del monitor del
motor, `sim/maxwell2d.py:266-276`, que YA evalua los dos invariantes y por eso comparte
soporte con el termino). La constante `c_*` **no se fija aqui**: su valor depende de la
convencion de la constante de estructura fina, y por eso las clausulas falsables de §7 se
eligen **invariantes de esa convencion** (la razon 1:7 y la forma temporal son
independientes de `c_*`).

**Canal 2 — saturacion por creacion de pares.** El exponente de Schwinger depende del
campo en reposo `a`, no de la forma combinada: el foco del par colineal es, por el algebra
sellada (`main.tex` l.487-492), el **caso de igualdad** donde `a = |E|` en todo instante:
es el punto de maxima excitacion del canal 2. Las dos geometrias del objeto — el foco
colineal y el par contra-propagante (antinodo parcial medido `cB/|E| = 0.445`) — son las
dos **ya calibradas**: la geometria no es una eleccion nueva de este pre-registro.

**Amplitud adimensional, medida (comando de hoy, `17:57:50Z`; `A0_CR = 329719` impreso por
`python3 -B sim/params.py` y citado en `sim/PROTOCOLO_1overN.md` §7):**

| cantidad | N = 1 | N = 16 |
|---|---|---|
| `a_tot` (modelo, `configs.json`, adimensional) | 170.533802 | 682.135209 |
| `a_tot / a0_cr` | 5.17210e-04 | 2.06884e-03 |
| `xi = (a_tot/a0_cr)^2` | 2.675057e-07 | 4.280091e-06 |

Si la constante tomara el borde mas generoso del rango declarado en §5 (`c_* = 1e-3`), la
correccion relativa valdria `c_* * xi = 2.675e-10` (N=1) y `4.280e-09` (N=16): **entre 8 y
11 decadas por debajo del piso de malla del instrumento** (§5). La tabla que mide esa
distancia es de §5; la conclusion de §10 la usa.

## §3 Separacion de capas: base y fibra

Regla que ordena todo lo que sigue: **sumar en un renglon cifras de distinta clase es el
defecto que este pre-registro aisla.** Se separan dos capas y ninguna se lee como la otra.

**Capa BASE — clasificadores de integridad (0/1, contables).** Deciden **si la corrida
cuenta**. Ninguno de sus numeros es una magnitud fisica.

| id | clasificador | forma | cota declarada |
|---|---|---|---|
| B1 | huellas del instrumento congelado | `sha16` medido fuera | `1db75ea7b0b8cba4` · `3ec003de4cb848d6` |
| B2 | formas y finitud | seis componentes `480 x 480` `float64`, `isfinite` | 0 no-finitos |
| B3 | estabilidad | CFL aplicado vs limite de von Neumann 2D `1/sqrt(2) = 0.7071` | CFL <= 0.7071 |
| B4 | adjuntez del par de diferencias (suma por partes) | `S = suma ddx(f)*g + suma f*ddx_f(g)` | `S == (f[479]g[479] - f[0]g[0])/dx` (identidad exacta) |
| B5 | ley de Gauss discreta sobre `D` | `max abs( ddx_f(Dx) + ddy_f(Dy) ) * dx / (eps0 * E_ref)` | `<= 1e-12` [ELEGIDO] |
| B6 | energia fuera del absorbedor | residuo relativo (`control_energia`) | `<= 1e-10` [ELEGIDO] |
| B7 | adjuntez del soporte declarado (§4) | conteo de celdas del soporte y del anillo excluido | `478*478 = 228484` · anillo `1916` |
| B8 | escalera de `R` (algebra, no umbral) | `0 <= R <= 1`, igualdad solo si `E || B` | 0 salidas fuera |
| B9 | paridad del termino (N2, §7) | `R(-E,-B) == R(E,B)` | identico al bit |
| B10 | candado de regresion (N0, §7) | `c_s = 0` reproduce la serie lineal sellada | identico al bit |
| B11 | conteo de cabezas del propio crudo | `^## ` en cada pieza escrita | el numero declarado en la pieza |

**Capa FIBRA — magnitudes fisicas (continuas).** Deciden **el veredicto**, y ninguna de
ellas decide si la corrida es admisible.

| id | magnitud | soporte | banda / piso |
|---|---|---|---|
| F1 | `R = a_inv / abs(E)` | ventana `[100,380]`, paso de diagnostico | piso de malla (§5) |
| F2 | `xi` y `c_s * xi` (dosis) | foco | declarado en la escalera (§5) |
| F3 | `dR(c_s)` y su pendiente | escalera completa | banda declarada (§7) |
| F4 | ancho `w` del maximo (morfologia) | ventana | piso de difraccion `4.94e-2` |

**Observable declarado, y no-observable declarado.** El observable es `R = a_inv/abs(E)`
(la columna de las tablas selladas que vale `0.744229241` para `colineal N=1`). NO se
declara observable la columna **relativa** que el filtro lee hoy
(`sim/filtro_analitico.py:186`, `a_inv_rel_al_pico`): es un cociente contra su propio pico,
por construccion insensible al angulo y saturado en el borde del barrido (medido: `45` grados,
`saturacion`). Un observable que no puede diferir no sostiene una clausula.

## §4 Soporte de la 2-celda (declarado ANTES de compilar o correr)

**Soporte de almacenamiento medido.** Las seis componentes viven en el MISMO par de indices
(`campos_vacios`, `sim/maxwell2d.py:145-147`: una rejilla `480 x 480` por componente). El
desplazamiento de Yee **no esta en el rango de indices: esta en el par de operadores
unilaterales**, y esto es medido, no supuesto:

- `ddx` (l.121) es diferencia **hacia atras**: `ddx(f)[i] = (f[i]-f[i-1])/dx`, definida en `i = 1..N-1`;
- `ddx_f` (l.133) es diferencia **hacia adelante**: `ddx_f(f)[i] = (f[i+1]-f[i])/dx`, definida en `i = 0..N-2`;
- `paso` (l.163) actualiza H con el par adelantado (`ddx_f`, `ddy_f`) y E con el par atrasado
  (`ddx`, `ddy`). Es la asignacion estandar del complejo: **`Ez` y `Hz` en la cara (2-celda);
  `Ex`, `Hy` en las aristas en x; `Ey`, `Hx` en las aristas en y.**

**Declaracion del soporte del termino correctivo.** La densidad del cuarctico es un escalar
formado por productos de componentes: en el complejo discreto es un **2-forma**, y por eso se
le asigna la **cara `(i,j)`**, el mismo punto donde el monitor ya evalua `F` y `G`. La
inyeccion de la correccion de vuelta al campo sigue el par adjunto que el esquema ya usa
(§B4), cara para el par `(Ez, Hz)` y arista para `(Ex, Hy)` y `(Ey, Hx)`.

**Rango declarado del soporte.** El par adjunto exige que las dos diferencias esten
definidas: la interseccion es `i = 1..N-2`, `j = 1..N-2`, es decir

- celdas del soporte: `478 x 478 = 228484`;
- anillo de borde excluido: `480^2 - 478^2 = 1916` celdas;
- y ese anillo (`1` celda) esta **contenido en la esponja** (`60` celdas por borde), asi que
  el recorte del soporte **no cambia ninguna frontera fisica**: `1 <= 60`, medido, y por eso
  no se reporta como hallazgo.

**La prueba del soporte es contable y es de la base.** Si el soporte se declara mal, (i) la
identidad de suma por partes `B4` deja de cancelar y (ii) la ley de Gauss `B5` enrojece
—y enrojece **antes** de que se lea ninguna magnitud de la fibra.

## §5 Umbrales de corte y pisos (declarados ANTES de compilar o correr)

**Pisos del instrumento, con su fuente.** Todos son de piezas ya selladas; ninguno se mide aqui.

| piso | valor | fuente |
|---|---|---|
| unidad, `abs(R-1)` | `5.444e-10` | sello del invariante (esquina transversal) |
| malla `lambda/40` | `<= 2.5e-2` | `main.tex` l.517-518, l.546 (benchmark sellado) |
| malla `lambda/20` | `3e-2 .. 4e-2` | `main.tex` l.518 |
| malla `lambda/10` | `1e-1 .. 1.4e-1` | `main.tex` l.517 |
| morfologico (difraccion) | `4.94e-2` | `sim/PREREGISTRO_KERR_20261011.md` §2.c |
| 2D contra referencia 3D | `4.1e-3` (`0.41 %`) | `main.tex` l.533-534 |
| corrimiento por malla `0.7442 -> 0.7740` | `2.97e-2` (`3.8 %`) | `main.tex` l.523-524 |

El piso **decisivo** para el canal 1 es el de malla: `2.5e-2`. Por debajo de el, una
correccion no es leible y se reporta como `NO_MEDIBLE`, no como cero.

**Escalera declarada de la correccion plantada `c_s`** (adimensional, relativa, declarada
antes de ver salida alguna):

| escalon `c_s` | leible contra `2.5e-2` | clase declarada |
|---|---|---|
| `0` | si (identidad al bit) | CANDADO (N0) |
| `3e-3` | no (`8.3x` bajo el piso) | `NO_MEDIBLE` |
| `1e-2` | no (`2.5x` bajo el piso) | `NO_MEDIBLE` |
| `3e-2` | si (`1.2x` sobre el piso) | `MEDIBLE_RASANTE` |
| `1e-1` | si (`4.0x` sobre el piso) | `MEDIBLE` |

**La distancia entre lo que se mide y la fisica, declarada como numero.** Con `c_*` en el
rango declarado de convenciones (`2.4e-6 .. 1e-3`, cuatro valores medidos hoy: `2.37e-6`,
`5.16e-5`, `1.62e-4`, `1e-3`) la correccion fisica relativa vale `c_* * xi` = `6.340e-13` ..
`2.675e-10` (N=1) y `1.014e-11` .. `4.280e-09` (N=16) — es decir, entre `7.97` y `10.60`
decadas **bajo** el piso de malla (comando de hoy, `17:57:50Z`). La conclusion es
**independiente de la convencion**: aun en el borde mas generoso (`1e-3`) la fisica esta
`9.3e7` veces bajo el piso. Y el escalon declarado con el que SI se mide (`3e-2`) esta
`1.1e8` .. `4.7e10` veces **por encima** del valor fisico: esa razon se declara y **no se
cierra corriendo**, porque ninguna corrida la puede cerrar.

**Criterio de truncamiento del cuarctico (declarado, no medido).** La serie efectiva se
trunca en el cuarto orden, admisible mientras `c_* * xi <= 1e-2` [ELEGIDO]. En el regimen
fisico se cumple por `7` a `10` ordenes; en los escalones altos de la escalera **no se
cumple**, y por eso la escalera mide un **sustituto declarado**, no el regimen fisico.

**Brecha del canal 2, declarada.** `I_cr = 4.64811e29 W/cm^2` contra el techo tecnico de
referencia `I_TECHNO = 1e23 W/cm^2` (`sim/params.py:37`): `6.667` ordenes (impreso en
`sim/PROTOCOLO_1overN.md` §7). El canal 2 **no se corre**: se declara fuera por brecha de
instalacion, con su numero.

## §6 Condiciones de frontera

- **Espacial.** Caja `12 lambda_L` por lado, `480 x 480` celdas, `dx = lambda_L/40`. Capa
  absorbente de `60` celdas por borde, pico `ALFA_ESPONJA = 0.10` por paso, aplicada
  multiplicativamente a las seis componentes dentro de `paso` (l.177-178). Control alterno
  de pared: `pec_muros` con `control_energia(pec=True)`.
- **Fuentes.** Planos en `i = 80` y `i = 400` (brazo `4 lambda_L`), con halo excluido de
  `20` celdas: la ventana de medida es `[100, 380]`. La fuente blanda (`duro=False`)
  **acumula** el campo casi-estatico de la propia linea (artefacto declarado: `abs(E)` inflado
  `6.9x`, `cB/abs(E) = 0.514`), y por eso **el termino correctivo NO se evalua sobre las
  lineas fuente**: la linea de inyeccion no es un objeto de Maxwell (declarado en
  `sim/maxwell2d.py:94-98`).
- **Temporal.** Envolvente `sin^2` de duracion `tau = 20 fs`, identicamente nula fuera de
  `[0, tau]`. Transito fisico `19.485 lambda_L` (`866` pasos a CFL `0.9`, el pre-registrado);
  a CFL `0.70` (el corregido por el limite de von Neumann 2D) son `1113` pasos con
  `dt = 4.669897e-17 s`. Diagnostico cada `20` pasos.
- **Frontera del encendido del termino.** Los campos arrancan en cero (`campos_vacios()` en
  `t = 0`), de modo que encender el termino **no introduce discontinuidad**: un escalon sobre
  campo nulo da `rho_HE = 0` en `t = 0`. Se declara porque una rampa de encendido moveria el
  numero y no es objeto del pre-registro.
- **Frontera de la custodia.** Ver §10: `bundle/` queda intacto; nada de este pre-registro
  entra al sello ni al manifiesto.

## §7 Nulos y clausulas falsables

| id | clausula | capa | que la hace ROJA | banda declarada |
|---|---|---|---|---|
| N0 | `c_s = 0` reproduce la serie lineal sellada **al bit** | base | cualquier diferencia | identico |
| N1 | nulo transversal **exacto**: si `F = G = 0`, `R = 0` con el termino encendido | base | soporte mal declarado que gotea | `abs(R) <= 5.444e-10` |
| N2 | **paridad**: `R(-E,-B) == R(E,B)` al bit (el cuarctico es par en los campos) | base | un termino impar en los campos | identico |
| N3 | **forma temporal**: al foco, `rho_HE` es constante mas UNA linea en `4 omega`, con razon linea/constante `= 3/4` y **sin linea en `1 omega` ni en `2 omega`** | fibra | una implementacion con otro cuarctico (p.ej. solo `F^2`, o coeficiente distinto) cambia la forma | razon `0.75 +- banda`; lineas `<= 1e-3` de la constante |
| N4 | **escalera monotona** en `c_s`, con `R(0)` dentro del piso de malla del valor lineal sellado | fibra | signo, o saturacion del metro | pendiente `!= 0`; `abs(R(0) - R_lineal) <= 2.5e-2` |
| N5 | el modo `colineal-nulo` **no** apaga el cuarctico | fibra | confundir el nulo del metro con el nulo del objeto | `delta R` distinto de cero en los escalones `MEDIBLE` |

N3 es el nudo del pre-registro y **no depende de la convencion de `c_*`**: la forma
`1 + 6 sin^2(2 omega t) = 4 - 3 cos(4 omega t)` sale del algebra sellada
(`main.tex` l.478-484: `F = E_f^2 cos(2 omega t)/2`, `G = -E_f^2 sin(2 omega t)/2`), y la
razon `3/4` cancela la constante. Un cuarctico con otro coeficiente para `G^2` da otra razon:
la clausula mide el **coeficiente 7** por la forma.

**Prediccion de forma cerrada, camino separado (requisito, no comodidad).** La forma que N3
promete NO se lee del FDTD: se calcula en el camino exacto ya existente
(`sim/field_solver.py`, suma de fasores en malla `61^3` con la ley constitutiva declarada),
y el FDTD se compara CONTRA esa prediccion. Un pre-registro que se compara consigo mismo no
tiene nulo.

## §8 Contrato RC y linea atomica de reporte

- **RC 0 conforme**: el filtro analitico intercepta la corrida (con su razon declarada) ->
  `VEREDICTO: DEDUCIDO_ANALITICO`; o el FDTD corre dentro de la banda declarada ->
  `VEREDICTO: FDTD_COMPLETO`. Escalon declarado `NO_MEDIBLE` se reporta como
  `VEREDICTO: NO_MEDIBLE`, no como cero ni como conforme.
- **RC 1 fractura**: una clausula de la FIBRA falla (N3, N4, N5, F4).
- **RC 2 fallo de metro**: `ValueError` fail-closed del filtro
  (`sim/filtro_analitico.py:105`), falta de interprete, o falta de un dato declarado.
- **RC 3 control fuera de su extremo**: un clasificador de la BASE (N0, N1, N2, B1-B11)
  sale de su extremo declarado. **No se reusa RC 2 para una corrida degenerada**: seria
  mentir sobre la clase.

Linea de reporte, atomica, una por corrida:

    VEREDICTO · RC · MOTOR · SHA16 · CRUDO: /ruta/en/disco

El crudo es un archivo en disco con encabezados `#` (convencion declarada, decidida en
`sim/falsador.py:43-55`, que ignora comentarios y lineas vacias). Sin crudo en disco no hay
corrida: la salida de pantalla no es el objeto.

## §9 Intercepcion y costo declarado de las dos rutas

`sim/maxwell2d.py` queda congelado: `correr(...)` (l.283) **no tiene parametro de
acoplamiento no lineal**, y anadir uno mueve la huella `1db75ea7b0b8cba4`, lo que invalida
los sellos previos y obliga a re-correr los dos gates (energia y CFL). Se declaran las dos
rutas con su precio, y **no se elige aqui**:

- **Ruta I (intercepcion, sin tocar el solver).** El termino vive en la familia de positivos
  y negativos declarados del filtro (`sim/filtro_analitico.py:158` y `:166`) y la clausula
  falsable se evalua contra el camino exacto de §7. Costo sobre la huella del solver: **0**.
  Precio declarado: el FDTD **nunca ve** la no-linealidad, y eso se reporta como tal.
- **Ruta II (FDTD con el termino).** Exige editar `sim/maxwell2d.py`: huella nueva, sellos
  previos invalidados, los dos gates re-corridos, y una columna nueva declarada. Costo
  declarado, **decision del dueno**, no tomada.

**Nombre del mecanismo.** El censo de hoy (`17:57:50Z`) da `chi3` `0`, `kerr` `0`, `P_NL`
`0`, `no_lineal` `0`, `heisenberg` `0`, `euler` `0` ocurrencias en los cinco instrumentos;
`polariz` `4` (todas en `sim/field_solver.py`, y son **polarizacion de haz**, no del medio);
`vac(io|uum)` `7 + 1` (todas son `campos_vacios` / `vacio clasico` en el bloque `UNIVERSO`);
`schwinger` `2 + 2`. Es decir: **el mecanismo no tiene nombre en el instrumento**, y ningun
modo de `MODOS_DEL_MOTOR` (`sim/maxwell2d.py:65`: cuatro modos) lo nombra. Nombrarlo es el
acto que lo vuelve afirmable, y ese acto es de la Ruta I o II, no de este documento.

## §10 Perimetro de custodia, costo y lo que este pre-registro NO afirma

- Custodia: `sim/data/vacio_no_lineal/` (creado por este pre-registro; medido **inexistente**
  antes, `porcelain = 0`). Fuera de `bundle/` (`0ce97cf9d8c44987`), que se audita solo desde
  fuera con `tools/verificar_bundle.sh` (`09ab3b5b24d9bb47`).
- Costo de computo de este pre-registro: **0**.

**NO afirma** (con su razon medida):

1. **NO afirma medir la no-linealidad del vacio con las amplitudes calibradas.** Medido: la
   correccion fisica esta entre `7.97` y `10.60` decadas bajo el piso de malla de
   `lambda/40` (§5), y la conclusion vale para todo `c_*` en el rango `2.4e-6 .. 1e-3`. Lo
   que la escalera mide es un **sustituto declarado**, `1.1e8` a `4.7e10` veces por encima
   del valor fisico.
2. **NO afirma el canal de creacion de pares.** Brecha de instalacion declarada: `6.667`
   ordenes entre `I_TECHNO` e `I_cr`.
3. **NO reabre el manuscrito.** `main.tex` queda en su sello (`90bfcb2b73ff9855`); el frente
   de calibracion lineal quedo cerrado por decision del dueno y esta pieza no lo toca.
4. **NO toca el instrumento congelado** ni la tabla sellada `sim/medidas_aN.csv`.
5. **NO usa la columna relativa** (`a_inv_rel_al_pico`) como observable (§3).
6. **NO promete direccion de `delta R`.** El signo lo fija el camino exacto de §7 cuando se
   corra, no este texto.
7. **NO convierte el control positivo en evidencia de fisica.** El control positivo es del
   sensor.

## §11 Sellos (medidos FUERA de este archivo)

    T_UTC de redaccion: 2026-10-11T17:57:50Z
    Instrumento congelado  sim/maxwell2d.py        1db75ea7b0b8cba4
    Conductor              sim/fuego_sensible.py   3ec003de4cb848d6
    Auditor del sello      tools/verificar_bundle.sh  09ab3b5b24d9bb47
    Manifiesto del bundle  bundle/HASHES.sha256    0ce97cf9d8c44987 (35 hojas / 34 entradas)
    Manuscrito citado      main.tex                90bfcb2b73ff9855

Este archivo no imprime su propia huella: se mide fuera, y la medicion entra como apendice
cuando exista una corrida. Toda correccion posterior es **apendice**, nunca parche.
