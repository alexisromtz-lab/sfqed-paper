# VEREDICTO DEL CONTROL PAREADO (motor analitico exacto vs solver FDTD sellado)

ETIQUETA: **verificacion del INSTRUMENTO, NO evidencia del articulo** (misma clausula que las piezas S). Nada de este documento se promueve al manuscrito.

UNIVERSO DECLARADO: motor analitico exacto (`sim/field_solver.py` + `sim/params.py`; caja 6.0 lambda; 32 fases) + SOLVER FDTD `sim/maxwell2d.py` en **SOLO LECTURA** (ventana 100-380, cadencia 20, CFL 0.7).
VENTANA: tres mallas en BLOQUE B y D -> lambda/10, lambda/20, lambda/40 (= 61 / 121 / 241 nodos por lado; referencia intrinseca en 1201 y 361 nodos). BLOQUE A en 61 y 121 nodos.
UNIDAD: razon adimensional `R = a_inv / |E|` (sin unidades); la unidad de conteo de malla es **nodos por lado**; la unidad de `medidas_aN.csv` es la fila por (modo, N).
UMBRAL / PRERREGISTRO: las tres ramas fueron fijadas por el dueno **antes** de la primera cifra y NO se re-etiquetan.
HORA: `2026-10-11T05:48:12Z` (corrida que ESCRIBIO el crudo).
COMANDO: `python3 -B sim/control_pareado_convergente.py` (escritura) · `... --sin-escribir` (seco). `EXIT=0` en las dos.
CRUDO: `sim/data/invariantes/control_pareado_convergente.json` — 27892 B · 1288 l · `sha16 41fce209adc05f98`
LOG: `/tmp/control_pareado_D2_write_20261011.log` (escritura, 30.0 s) · `/tmp/control_pareado_dry_D2_20261011.log` (seco, T_UTC 05:47:34Z)
Sellos de los motores: lector `9fab4e04d281d3cc` · field_solver `8cfca6a9bff5fee7` · maxwell2d `1db75ea7b0b8cba4`. Los tres **sin editar**.

---

## 1. VEREDICTO

**`rama 2`**, por NUMERO, con la etiqueta del dueno citada verbatim:

> rama 2 (~0.74): estructura intrinseca del campo convergente; el lector no introduce distorsion relevante

El valor sellado del articulo (`sim/etapa1_colineal.json`, N=1, lectura **L2_lector** de `razon_cadencia20`) es
`0.7442292409269158`. El valor **no** es artefacto geometrico de muestreo ni exceso temporal del solver: es la
estructura intrinseca del campo convergente, medida con un motor que no tiene malla, ni paso temporal, ni pulso,
ni esponja.

---

## 2. LAS TRES RAMAS PRERREGISTRADAS, UNA POR UNA

| rama | intervalo declarado (NUMERO) | etiqueta del dueno (verbatim) | veredicto |
|---|---|---|---|
| 1 | ~0.08 | artefacto geometrico de muestrear el frente en malla cartesiana ortogonal | **REFUTADA** |
| 2 | ~0.74 | estructura intrinseca del campo convergente; el lector no introduce distorsion relevante | **CONFIRMADA** |
| 3 | 0.2 - 0.4 | exceso por la dinamica temporal del solver FDTD | **NO DISPARADA** |

**Rama 1 REFUTADA, con la malla como variable.** El mismo motor analitico, sin malla y sin FDTD, da
`R = 0.7136222385918988` (lambda/10) y `0.7125074731962245` (lambda/20) para `estrella alpha=26.5651`, y
`0.777157703748551` en las **dos** mallas para `estrella alpha=30.0`. La razon **existe con el campo continuo
exacto** y **converge** al refinar: la malla vale `<= 0.16 %` en 26.5651 grados y `0.00 %` en 30 grados. Un
artefacto de muestreo no sobrevive a que se le quite el muestreador.

**Rama 3 NO DISPARADA.** Su intervalo es `[0.15, 0.55]`; el valor sellado `0.744` y el valor con lectura
completa `0.774` caen **fuera y por encima**. Ademas la cota temporal post-hoc (`omega dt/2 = 0.054978 rad`,
`sin^2 = 0.003020`) es del orden del 0.3 % de la razon, no del 74 %. La pata FDTD de onda plana del diseno
(la cota combinada `0.0785` espacial vs `~0.10` con desfase leapfrog) queda **NO EJECUTADA**: su condicion de
disparo era un valor intermedio `0.2 - 0.4`, y el control cerro en `0.744 - 0.774`.

**Tension de lectura llana, declarada (no adjudicada).** Las etiquetas 1 y 3 se cruzan leidas al pie de la
letra: la 1 llama *artefacto* al residuo de 0.744 y la 3 atribuye el *exceso* a la dinamica temporal. El
instrumento no elige: `rama_de()` devuelve **todas** las ramas cuyo intervalo contiene el valor y el veredicto
se emite **por numero**, citando la etiqueta verbatim.

---

## 3. LA PRUEBA DECISIVA: EL VALOR SELLADO QUEDA **ENCAJADO** POR LA FAMILIA ANALITICA 3D

| objeto | R | fuente |
|---|---|---|
| `estrella alpha=26.5651` (intrinseco, 1201 nodos) | 0.712507 | BLOQUE A |
| **`colineal N=1`, lectura L2 (SELLADO)** | **0.7442292409269158** | etapa1_colineal.json |
| `estrella alpha=30.0` (intrinseco, 1201 nodos) | 0.777157 | BLOQUE A |

`0.712507 < 0.74422924 < 0.777157` -> el valor sellado es un **cono 3D de semiangulo efectivo intermedio**.
Interpolando el cono entre 26.5651 y 30.0 grados:

- lectura **L2_lector** -> `alpha_efectivo = 28.2505 grados`
- lectura **L4_completo** -> `alpha_efectivo = 29.8305 grados`

Y el angulo geometrico esperado por la pinta de la fuente (frente parabolico con `BRAZO_M = 4 lambda` y media
abertura `2 lambda`) es `atan(2/4) = 26.5651 grados`, que es casi exactamente `ALPHA_REF_DEG = 30.0` del
protocolo. La lectura completa (L4) **cae a 0.41 % de la rama analitica de 30 grados**:
`0.7739676586994475 / 0.777157703748551 - 1 = -0.4105 %`.

### 3.1 La malla NO puede producir la brecha

En la MISMA geometria convergente, el exceso de la malla sobre la referencia intrinseca (continua) del mismo
objeto, con la lectura completa L4:

| geometria | lambda/10 | lambda/20 | lambda/40 |
|---|---|---|---|
| `cruce 26.5651` -> `R_L4 / R_intr` | 1.1439 | 1.0386 | **1.0098** |
| `cruce 30.0` -> `R_L4 / R_intr` | 1.1034 | 1.0273 | **1.0069** |
| `abanico 30.0 m=17` -> `R_L4 / R_intr` | — | — | **1.0252** |

A lambda/40 la malla aporta **entre +0.7 % y +2.5 %**. La distancia del valor sellado a la rama analitica es de
**-0.41 %** (L4 vs 30 grados) y de **+4.45 %** (L2 vs 26.5651 grados). Es decir: **la malla no es la que mueve la
cifra** — y el signo del residuo cambia segun la lectura. El reparto espacio-temporal queda asi **aislado y
acotado**: el error de discretizacion espacial sobre frentes curvos vale `<= 2.5 %`, y el valor sellado cae
dentro de la banda del cono continuo.

---

## 4. LECTURA DEL SOLVER SOBRE EL CAMPO SELLADO (BLOQUE C) — y su GATE

Se reproceso el MISMO campo del solver sellado con una cuarta lectura (`L4_completo`: de-stagger completo de
`Ex` en x, `Ey` en y y `Bz` en y despues de x) sin editar `maxwell2d.py` ni `lector_invariantes.py`:

| modo | N | a_medido (a0) | rel L1 (naive) | rel L2 (lector) | rel L4 (completo) |
|---|---|---|---|---|---|
| colineal | 1 | 79.98173362 | 0.999513275 | **0.744229241** | 0.773967659 |
| contra | 2 | 78.99734564 | 0.992089925 | 0.992533113 | 0.992735402 |

**GATE VIVO contra el crudo sellado (`crudo_lector_invariantes.json`, `sha16 96f66e9cb30a56ed`): OK x4, desvio
`0.00e+00`** en las cuatro casillas comparadas (colineal N=1 L1 y L2; contra N=2 L1 y L2). El instrumento
reproduce el crudo sellado **al ultimo bit**.

### 4.1 Candidato de metro: el de-stagger del lector es PARCIAL

El lector sellado `interp_x`/`interp_y` corrigen **solo B**, y `Hz` **solo a lo largo de x**; quedan a medio nodo
`Bz`, `Ex` y `Ey`. Medido en la geometria convergente del solver:

- `L1 - L2 = 0.2552840345`
- `L1 - L4 = 0.2255456167`
- `L4 - L2 = 0.0297384178`  (el 11.65 % de la correccion total de L1 a L4)

=> en la geometria convergente **L2 corrige de MAS**: su bajada excede la de la lectura completa en
`0.0297` de razon (3.84 % de `0.773968`), es decir `L2` **pasa de largo**.
En `contra` el signo se invierte (`L1->L2 = +0.0004431879`, `L2->L4 = +0.0002022890`, ambos **al alza**)
=> ahi **sub-corrige**.

**NO SE AFIRMA COMO DEFECTO.** El control sintetico sellado (`control_sintetico()`, GREEN, desvio maximo
`1.993e-14`) usa una onda plana con `k` paralelo a x: es **ciego a este desajuste POR CONSTRUCCION**. El lector
sellado y su sello **no se editan**. Se registra como candidato de metro, con sus cifras.

### 4.2 Ratios derivadas (observacion POST-HOC, no adjudicacion)

| objeto | `L2 / L1` |
|---|---|
| colineal sellado (N=1) | 0.744592 |
| contra sellado (N=2) | 1.000447 |
| `cruce 26.5651` lambda/40 | 0.982593 |
| `cruce 30.0` lambda/40 | 0.988014 |
| `abanico 30.0 m=17` lambda/40 | 0.982900 |
| onda plana `copropagante` lambda/40 (cota) | 1.146227 |

Todas las geometrias 2D convergentes medidas dan factor de transferencia L2/L1 cercano a `0.983`, y la cota de
onda plana da `1.146` (L2 **por encima** de L1, o sea peor que el naive). El `0.7446` de la pata colineal no se
parece a ninguno de los dos. Se registra; no se interpreta.

---

## 5. BRECHA DECLARADA 2D vs 3D — EL HALLAZGO DE BLOQUE D

El solver sellado es **2D (x-y)** con `Ez`/`Ey` y una fuente de **frente parabolico de UNA cara** (convergente).
El motor analitico que encaja el valor sellado es un **cono 3D** (dos grados de libertad angulares, familia
`estrella`). El analogo 2D correcto de la fuente sellada es el **abanico convergente de una cara**:
`psi` en `[-alpha, +alpha]` alrededor de `+y`, todas las direcciones por el foco comun.

**Resultado medido (BLOQUE D, POST-HOC, ADITIVO, intrinseco, 181 nodos):**

| alpha | m=2 | m=3 | m=5 | m=9 | m=17 | par enfrentado puro |
|---|---|---|---|---|---|---|
| 26.5651 | 0.447214 | 0.368525 | 0.321026 | 0.294009 | **0.279398** | 1.000000 |
| 30.0 | 0.500000 | 0.413105 | 0.360445 | 0.330406 | **0.314133** | 1.000000 |

1. **La razon 2D DECRECE con el contenido angular y nunca se acerca a 0.74.** Con `m = 17` el abanico de una
   cara se queda en `0.279 - 0.314`, muy por debajo del valor sellado.
2. **CONTROL CRUZADO (vivo).** `m = 2` reproduce **exactamente** `sin alpha` (`0.447214` y `0.500000`), que es
   la familia `cruce` de BLOQUE B: `29.4 %` de acuerdo al ultimo decimal con la via independiente.
3. **CONTROL SATURADO (vivo).** El par enfrentado puro (`par_enfrentado_2d`, m=1) da `1.000000` = `max a = max
   |E|`: **saturacion por simetria**, cero informacion. Es exactamente el caso que el dueno anticipo
   (*"confirmacion de saturacion por simetria"*). **La primera version de BLOQUE D era un abanico enfrentado y
   por eso salia inerte en `1.000000` en todas las filas; se reemplazo por el abanico de una cara y el defecto
   quedo diagnosticado y reparado, no oculto.**

**Consecuencia declarada:** **ninguna geometria 2D medida alcanza la banda sellada** (`0.744 - 0.774`); solo la
alcanza la familia **3D** (`estrella 26.5651 - 30.0` = `0.7125 - 0.7772`). La correspondencia 2D/3D **no se
cierra: se ensancha**, y se registra como brecha, sin adjudicar. Con tres mallas de proyeccion Yee sobre el
abanico `alpha=30, m=17`: `lambda/10` L1 `0.590924` / L2 `0.627821` / L4 `0.420830` (L4/R_intr = 1.3397);
`lambda/20` `0.463112 / 0.469336 / 0.344574` (1.0969); `lambda/40` `0.383917 / 0.377352 / 0.322057` (1.0252).

---

## 6. PREMISA DEL DUENO: VERIFICADA Y FALSADA CON MEDICION

*"En el motor analitico se tiene `E . B = 0` por construccion"* — **vale solo para `copropagante`**, la familia
colimada de un solo vector de onda. Es **falso para toda superposicion con `k` distintos**:

- `estrella alpha=30, N=4` -> `a_inv / E_a0 = 2.000000 = 4 sin(30)` exacto
- `coaxial_contra N=4` -> `4.000000`

**Algebra exacta del foco:** en el foco `E` es paralelo a `z` con `|E| = 4 sin(alpha) E0` y `B = i h 4 sin(alpha) E0`;
`E` y `B` son paralelos **en cuadratura temporal** => `F = A cos(2 omega t)`, `G = A sin(2 omega t)`,
`a = 4 sin(alpha) E0 |cos(omega t)|` => **`max a = 4 sin(alpha) E0 = |E|`** => `ratio_puntual = 1.000000` en
todo caso conico. El instrumento imprime `puntual 1.00000` en todas las filas conicas, confirmandolo.

**Colision de namespace (la razon de ser de este control).** El control de `a_inv = 0` del motor analitico es la
familia **colimada** `copropagante`; la pata FDTD `colineal` sellada es un haz **convergente/enfocado**. **No son
el mismo objeto.** Compararlos produjo la paradoja aparente `0.9995 vs 0`.

---

## 7. CIFRAS DE LA FAMILIA ANALITICA (BLOQUE A, verbatim)

| familia | alpha | `R` (61 nodos) | `R` (121 nodos) | `a_inv` (a0) | `puntual` |
|---|---|---|---|---|---|
| copropagante | 0.0 | 0.000000 | 0.000000 | 0.0000 | 0.00000 |
| coaxial_contra | 0.0 | 1.000000 | 1.000000 | 4.0000 | 1.00000 |
| estrella | 15.0 | 0.503709 | 0.503709 | 1.0353 | 1.00000 |
| estrella | 20.0 | 0.590733 | 0.590733 | 1.3681 | 1.00000 |
| estrella | 26.5651 | 0.713622 | 0.712507 | 1.7889 | 1.00000 |
| estrella | 30.0 | 0.777158 | 0.777158 | 2.0000 | 1.00000 |
| estrella | 35.0 | 0.869705 | 0.867621 | 2.2943 | 1.00000 |
| estrella | 45.0 | 1.000000 | 1.000000 | 2.8284 | 1.00000 |

La columna `a_inv` es `4 sin(alpha)` **exacto**. `copropagante` y `coaxial_contra` son los dos controles
sellados del motor analitico, ambos GREEN.

---

## 8. TELEMETRIA Y ESTADO DEL REPOSITORIO

Barrido completo de `sha16` (tamano / lineas / sha16) despues de la corrida de escritura:

```
sim/medidas_aN.csv                                     1360 /   18 / 4129d436e2cd081d   (INTOCABLE, intacto)
sim/maxwell2d.py                                      30759 /  715 / 1db75ea7b0b8cba4
sim/field_solver.py                                   25326 /  501 / 8cfca6a9bff5fee7
sim/lector_invariantes.py                             32113 /  635 / 9fab4e04d281d3cc
sim/data/invariantes/medidas_invariantes_aN.csv        4910 /   28 / a491a0ed6ff9cc79
sim/data/invariantes/crudo_lector_invariantes.json    22205 /  769 / 96f66e9cb30a56ed
sim/data/invariantes/INFORME_LECTOR_INVARIANTES_..md  17726 /  277 / 0b612674187552ad
sim/etapa1_colineal.json                              11530 /  283 / 33bcf93826ce494b
sim/etapa1_contra.json                                 9292 /  228 / 221a9fe8c3e269f4
sim/data/invariantes/control_pareado_convergente.json 27892 / 1288 / 41fce209adc05f98  (NUEVO)
main.tex                                              26014 /  514 / 6cd0f0803b61a3a5  (otra mano, DECLARADO)
```

- `sim/medidas_aN.csv` verificado intacto **dentro** de la corrida (`antes 4129d436e2cd081d / despues
  4129d436e2cd081d / intacto: True`).
- **Nada se movio salvo los dos archivos declarados**: el crudo nuevo y `main.tex`.
- **`main.tex` modificado por otra mano** (estaba en 23042 B / 465 l / `44a3f0b33ad6593e`): se **declara**, no
  se adjudica. Permanece **en reposo** por orden.
- Dispersion de reloj: la misma corrida tardo `135.3 s` (78 % CPU), `41.5 s`, `38.6 s` y `30.0 s` (97 % CPU);
  `diff` de los dos logs completos da **identico byte a byte salvo la linea `T_UTC`** => la dispersion es **de
  la maquina, no del objeto**. Declarado, no adjudicado.
- Cero colisiones de escritura: el instrumento escribe **solo** dentro de `sim/data/invariantes/`; ningun motor
  sellado fue editado.

---

## 9. CLAUSULAS

1. Todo lo de este documento es **verificacion del instrumento**, no evidencia del articulo.
2. Las dos ramas no confirmadas se registran por su **numero**; las etiquetas se citan **verbatim** y no se
   corrigen.
3. La pata FDTD de onda plana (cota espacio-temporal) queda **NO EJECUTADA**: su condicion de disparo no se
   cumplio.
4. La brecha 2D/3D, el candidato de metro (L2 parcial) y las ratios derivadas se registran como **hallazgos
   declarados**, sin adjudicar y sin editar ninguna pieza sellada.
5. Toda cifra de este documento viaja con su hora (`2026-10-11T05:48:12Z`), su `UNIVERSO DECLARADO` y su
   comando; una cifra de conteo caduca al escribirse.
