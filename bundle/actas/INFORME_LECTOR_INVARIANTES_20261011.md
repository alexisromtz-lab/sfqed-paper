# INFORME DEL LECTOR DE INVARIANTES — Pestaña 3

`T_UTC = 2026-10-11T03:31:36Z` · instrumento `sim/lector_invariantes.py` sha16 `9fab4e04d281d3cc`
· crudo `sim/data/invariantes/crudo_lector_invariantes.json` sha16 `96f66e9cb30a56ed` (22 205 B)
· csv `sim/data/invariantes/medidas_invariantes_aN.csv` sha16 `a491a0ed6ff9cc79` (4 910 B, 18 filas)

**ETIQUETA DEL ARTEFACTO: verificación del solver, NO evidencia.** Ninguna cifra de aquí se mueve a
`main.tex` (en reposo por orden), ni toca `sigma_phi`, ni toca `a_medido`.

---

## 0 · UNIVERSO DECLARADO (antes de toda cifra)

    UNIVERSO DECLARADO: FDTD malla xy 480x480 (12 lambda_L, dx = lambda_L/40 = 2.0e-08 m),
    CFL_2D = 0.700, transito = 19.485 lambda_L = 1113 pasos, dt = 4.669897332774128e-17 s,
    VENTANA DE MEDIDA = celdas x en [100, 380], unidad de campo = a0 (1 a0 = 4.0134e12 V/m),
    unidad de conteo = celda, ventana temporal = el transito entero, motor = numpy,
    N = numero de canales/brazos que inyectan; quedan FUERA: la corona de esponja (60 celdas),
    la columna j = 0 (interpolacion de Yee sin nodo j-1: declarada NaN) y todo t fuera del transito.
    UMBRAL: la puerta del sello es de TOLERANCIA; en esta corrida salio bit-exacta (ver 9.c).

Denominador de toda razon de este informe: `|E|` **del mismo paso y la misma celda** (puntual) o el
`max |E|` del paso (cadencia). Sin ese denominador la razon no existe.

---

## 1 · Comandos que respaldan cada cifra

| id | comando | qué respalda |
|---|---|---|
| C1 | `python3 -B sim/lector_invariantes.py` (log `/tmp/lector_inv2_20261011.log`) | las 9 patas, la tabla, el EXIT |
| C2 | `shasum -a 256 sim/lector_invariantes.py sim/maxwell2d.py sim/medidas_aN.csv sim/data/invariantes/*` | identidad de los 5 archivos |
| C3 | lector `csv` de las 18 filas del csv → `F_rel`, `G_rel`, `abs(G)/F`, `ratio` | la tabla derivada y el techo |
| C4 | bloque final `python3 -B -c` (deltas absolutos, contraste, headroom) | los deltas de §5 y el headroom de §6 |
| C5 | `python3 -B -c` volcado del crudo (claves `lecturas`, `pico`) | los valores a 16 cifras de §3 |
| C6 | `grep -c` de patas en el log | 9 patas `^-- FDTD` · 1 `NO APLICABLE` |

**EXIT de C1 = 0** (la puerta solo cierra; un informe sin código de salida no existe).

---

## 2 · Las tres lecturas y las cotas CERRADAS (pre-registradas, escritas antes de medir)

Control sintético: onda plana transversa circular, `lambda = 40 celdas`, verdad `a_inv = F = G = 0`
exacto (`E.B = 0` y `|B| = |E|/c`). `delta = k dx/2 = 0.078540 rad = 4.5000°`.

| magnitud | cota de malla (L1 naive) | cota de malla (L2 interpolado) |
|---|---|---|
| `a_inv / abs(E)` | `sqrt(sin delta) = 0.280106` | `sin delta = 0.078459` |
| `G / (eps0 E^2)` | `sin delta = 0.078459` | `0 exacto` |
| `F / (eps0 E^2 / 2)` | — | `sin^2 delta = 0.006156` |

Desvío máximo del control sintético contra su propia cota: `1.993e-14`. El control analítico también
verde: `copropagante N=4 -> 0.000000` y `coaxial_contra N=4 -> 4.000000` (desvío `0.00e+00`).

Nota estructural (de la pre-inscripción): `a_inv` es **raíz de una forma cuadrática** ⇒ un error
relativo `O(delta^2)` en el campo sale `O(delta)` en `a_inv`. La interpolación de Yee, para una onda
plana, es **atenuación pura** `cos(k dx/2) = 0.99692` y **desfase 0**.

Cota temporal (NO pre-registrada, **post-hoc**): medio paso de leapfrog `w dt/2 = pi*0.7/40 =
0.054978 rad` ⇒ `sin = 0.054950`, `sin^2 = 0.003020`. Va etiquetada: no entró al pre-registro.

---

## 3 · La tabla (18 filas = 9 patas x 2 lecturas; `nan_extra = 0` en las 18)

`cad20` = razon de maximos de ventana, **cadencia cada 20 pasos** (44 instantes muestreados).
`puntual` = cociente co-ubicado en la celda de `a_inv` supremo, **contra `|E|` de esa misma celda y paso**.
`F_rel = F / (eps0 E^2/2)`, `G_rel = G / (eps0 E^2)`, ambos del campo **interpolado**.

| N | modo | lectura | cad20 | puntual | sup_a0 | E_sup_a0 | F_rel | G_rel |
|---|---|---|---|---|---|---|---|---|
| 1 | colineal | naive | 0.9995132753995678 | 0.451314 | 35.750099 | 79.213443 | 0.093237 | -0.149985 |
| 1 | colineal | interpolado | 0.7442292409269158 | 0.379073 | 30.003925 | 79.150750 | 0.104942 | -0.074623 |
| 2 | colineal | naive | 0.9995132753995680 | 0.451314 | 50.558275 | 112.024725 | 0.093237 | -0.149985 |
| 2 | colineal | interpolado | 0.7442292409263918 | 0.379073 | 42.431957 | 111.936064 | 0.104942 | -0.074623 |
| 4 | colineal | naive | 0.9995132753995678 | 0.451314 | 71.500198 | 158.426886 | 0.093237 | -0.149985 |
| 4 | colineal | interpolado | 0.7442292409269158 | 0.379073 | 60.007849 | 158.301500 | 0.104942 | -0.074623 |
| 8 | colineal | naive | 0.9995132753995678 | 0.451314 | 101.116550 | 224.049451 | 0.093237 | -0.149985 |
| 8 | colineal | interpolado | 0.7442292409266690 | 0.379073 | 84.863914 | 223.872128 | 0.104942 | -0.074623 |
| 16 | colineal | naive | 0.9995132753995678 | 0.451314 | 143.000397 | 316.853772 | 0.093237 | -0.149985 |
| 16 | colineal | interpolado | 0.7442292409270357 | 0.379073 | 120.015699 | 316.602999 | 0.104942 | -0.074623 |
| 2 | contra | naive | 0.9920899249757815 | 0.929956 | 73.464038 | 78.997346 | 0.844420 | -0.132784 |
| 2 | contra | interpolado | 0.9925331129213314 | 0.926704 | 73.207194 | 78.997346 | 0.854646 | -0.059517 |
| 4 | contra | naive | 0.9920899249757712 | 0.929956 | 103.893839 | 111.719118 | 0.844420 | -0.132784 |
| 4 | contra | interpolado | 0.9925331129213386 | 0.926704 | 103.530607 | 111.719118 | 0.854646 | -0.059517 |
| 8 | contra | naive | 0.9920899249757815 | 0.929956 | 146.928076 | 157.994691 | 0.844420 | -0.132784 |
| 8 | contra | interpolado | 0.9925331129213314 | 0.926704 | 146.414388 | 157.994691 | 0.854646 | -0.059517 |
| 16 | contra | naive | 0.9920899249757991 | 0.929956 | 207.787678 | 223.438235 | 0.844420 | -0.132784 |
| 16 | contra | interpolado | 0.9925331129213377 | 0.926704 | 207.061213 | 223.438235 | 0.854646 | -0.059517 |

`cad20` va a 16 cifras (son las que lleva el crudo). `puntual` va a 6 cifras porque **es idéntica en
las patas de cada familia** salvo el último dígito; a 16 cifras, verificado en C5: colineal
naive `0.4513135378141239` (N=1) · colineal interpolada `0.3790731574103944` (N=1) · contra naive
`0.9299557770445093` (N=2 y N=8) · contra interpolada `0.9267044776657611` (idéntica en las 4 patas).

**Pata declarada NO APLICABLE** (ni medida ni contada): `contra N=1` —
`el modo contra necesita N par (pares enfrentados)`. Es el motivo por el que la familia `contra`
tiene 4 patas y no 5.

`a_medido_a0` por pata (colineal): `79.98173362000696 · 113.11125242752591 · 159.96346724001393 ·
226.22250485505182 · 319.92693448002785`; (contra): `78.99734564144379 · 111.719118… · 157.994691… ·
223.438235…`.

**Sub-cero declarado del ancla:** `N = 1` es `0/0` en el motor analítico (`a_inv(N=1) = 0` por
Lemma 1) ⇒ el ancla NO CERO mínima es `N = 2`; la ley esperada era `a_inv(N) = a_inv(2)*sqrt(N/2)`.

---

## 4 · El techo: `a_inv <= |E|` puntual (DERIVADO, con confirmación medida)

`a_inv = sqrt( sqrt(F^2+G^2) + F ) / sqrt(eps0)`, `F = (eps0 E^2 - B^2/mu0)/2 <= eps0 E^2/2`
siempre, porque `B^2/mu0 >= 0`; y `G^2 >= 0`. ⇒ `sqrt(F^2+G^2) + F <= eps0 E^2`, con igualdad
**solo si** `G = 0` y `F = eps0 E^2/2` (campo eléctrico puro). ⇒ `a_inv / |E| <= 1` **por definición**,
y toda lectura normalizada por `|E|` vive en `[0, 1]`.

Medido (C3): `max razon_cadencia20 = 0.9995132754 (<= 1 -> True)` · `max cociente_puntual =
0.929955777`.

Consecuencia que hay que decir en voz alta: el sello `a_inv_rel_al_pico = 0.9995132754` está
**0.049 % por debajo de su propio techo**. Una magnitud que vive a 5 diezmilésimas de su cota tiene
**casi cero rango dinámico**: que salga igual a 16 cifras en `N = 1, 2, 4, 8, 16` y a 0.75 % entre
geometrías **no es evidencia de invariancia física — es saturación**. Esto explica el hecho que
motivó toda la pestaña, y lo explica sin postular artefacto alguno.

---

## 5 · Contraste de geometrías a N apareado (idéntico en N = 2, 4, 8, 16)

| métrica | colineal | contra | exceso absoluto (unidad = techo 1) | relativo |
|---|---|---|---|---|
| cad20 naive | 0.9995132754 | 0.9920899250 | 0.0074233504 | **0.7483 %** |
| cad20 interpolado | 0.7442292409 | 0.9925331129 | 0.2483038720 | **25.0172 %** |
| puntual naive | 0.4513135378 | 0.9299557770 | 0.4786422392 | 51.4694 % |
| puntual interpolado | 0.3790731574 | 0.9267044777 | 0.5476313203 | 59.0945 % |

Se reporta el **exceso absoluto** junto a la razón (método de etiquetas, propiedad 6: con pocos
datos la razón no ordena). Lectura: la métrica **sellada** (cad20 naive) casi no separa las dos
geometrías — **0.75 %**; la misma métrica con la lectura **interpolada** las separa **25 %**
(**33 % relativo**, `1/0.749828`); y la lectura co-ubicada puntual las separa **2.06x** (naive) y
**2.44x** (interpolado).

**Ese es el rendimiento medido de la salvaguarda #1:** la interpolación de Yee no es cosmética —
es lo que hace que el metro **vea la geometría**.

---

## 6 · Qué compró la salvaguarda #1: el piso bajó 3.5701x

Lectura co-ubicada **en el pico de `|E|`** (celda y paso del máximo, `pico` del crudo), que es un
objeto distinto del supremo de `a_inv`:

| caso | naive | interpolado |
|---|---|---|
| colineal `a_inv/abs(E)` | 0.430159 | 0.360908 |
| contra `a_inv/abs(E)` | 0.929956 | 0.926704 |
| **headroom** colineal sobre la cota | 1.5357x | **4.6000x** |
| **headroom** contra sobre la cota | 3.3200x | **11.8113x** |

La interpolación **baja el piso** `sqrt(sin)/sin = 3.5701x` y **mueve el valor** solo −16.1 %
(colineal) y −0.35 % (contra) ⇒ el valor se aleja del piso: `1.5357 -> 4.6000` (colineal) y
`3.3200 -> 11.8113` (contra). El instrumento **ganó rango dinámico** al interpolar. Y en `contra`
el valor está cerca de 1, que es lo que la física espera (cancelación de `B` entre pares
enfrentados) ⇒ **en `contra` la lectura es del objeto, no del metro**: 93 % del techo, 11.8x sobre
su piso y estable bajo la corrección (−0.35 %).

Firma de la co-locación (para `contra`): `abs(G)/F` cae de `0.3145` a `0.1393` al interpolar
(−55.7 %), mientras `F_rel` **sube** de `0.844420` a `0.854646`; en colineal `abs(G)/F` cae de
`3.2173` a `1.4222` (−55.8 %) con `F_rel` subiendo `0.093237 -> 0.104942`. ⇒ la co-locación
**infla `abs(G)`** con un factor multiplicativo casi idéntico en las dos geometrías — exactamente
lo que la pre-inscripción predijo.

---

## 7 · La regla pre-registrada, aplicada al pie de la letra

La pre-inscripción decía: *«Si al interpolar (L2) el FDTD baja a ~0.08-0.28 ⇒ el sello era artefacto
del lector. Si NO baja ⇒ hay no-transversalidad real del haz convergente que el modelo analítico no
puede representar»*.

Medido (colineal, cad20): `0.9995132754 -> 0.7442292409`. **0.7442 no cae en la banda [0.08, 0.28]**
⇒ por la letra de la regla se indica la **segunda rama**. Pero la segunda rama **NO se cierra**, y hay
que decirlo con los tres matices medidos:

1. **La interpolación sí bajó el número: −0.2552840345 absoluto (−25.5 %).** Luego **una parte del
   sello sí era del lector** (la firma de `§6`: `abs(G)` inflado).
2. **El residuo queda por encima de los dos pisos medidos**: `0.744229 / 0.078459 = 9.486x` la cota
   interpolada y `0.744229 / 0.280106 = 2.657x` la naive (el sello naive era `3.568x` y `12.739x`).
3. **El piso FDTD de la lectura interpolada NO está medido.** Solo existe el control sintético
   espacial (0.078459) y una estimación post-hoc del medio paso temporal (0.054950). La suma de
   cota espacial + medio paso de leapfrog en esta malla/CFL **es una cuenta que no se hizo**: el
   pre-registro anticipaba «~0.36» para el **naive con desfase temporal añadido** (contra 0.280106
   puramente espacial, el término temporal añadía ~+29 %) — si ese mismo +29 % actuara sobre la
   lectura interpolada, su piso estaría en ~0.10, y 0.744 sería ~7x eso. **Es indicio, no medición.**

En **`contra` la interpolación SUBE el valor**: `0.9920899250 -> 0.9925331129`
(`+0.0004431879` absoluto, +0.0447 %). ⇒ ahí el lector **no puede ser la causa**; pero tampoco el
dato informa mucho, porque el valor vive a 0.75 % del techo (§4). **Artefacto y término físico
tienen signos opuestos en las dos geometrías.**

**VEREDICTO HONESTO: hallazgo MEDIDO; mecanismo NO adjudicado.** Y la medición que lo cerraría está
**declarada y no ejecutada**:

> **Siguiente medición pre-declarable (1 pata, ~80 s):** una pata FDTD de **onda plana** (misma
> malla, mismo `CFL_2D = 0.7`, misma ventana, misma cadencia) leída por las **dos** lecturas ⇒ fija
> el piso real del instrumento, incluido el **medio paso de leapfrog**, para L1 y L2. Sin ese piso,
> el residuo de 0.744 no se puede separar del offset temporal. **No corrida.** Su fecha límite es
> antes de cualquier frase sobre no-transversalidad.

Hermana de la anterior, del mismo signo: la salvaguarda #1 pedía interpolación **en el espacio**; el
offset declarado es **en el tiempo**. La corrección completa sería interpolar también `B` a un
instante común (`B(t) = (B(t - dt/2) + B(t + dt/2))/2`). **Declarado, no ejecutado.**

---

## 8 · Lo que se registra y NO se eleva

- **Invariancia en N de las lecturas:** colineal naive idéntica a 16 cifras
  (`0.9995132753995678`, con `…680` en N=2 ⇒ dispersión en el dígito 16); colineal interpolada entre
  `0.7442292409263918` (N=2) y `0.7442292409270357` (N=16) ⇒ dispersión en el dígito 13; contra
  naive entre `0.9920899249757712` y `0.9920899249757991` (dígito 14–15) e interpolada entre
  `0.9925331129213314` y `0.9925331129213386` (dígito 16). **La componente puntual co-ubicada da el
  MISMO patrón** (`F_rel`, `G_rel` idénticos en las 4–5 patas de cada familia).
- **Celda del supremo:** colineal `i = 213, j = 240` (naive) y `i = 208, j = 240` (interpolado), a
  `lambda_del_foco = -0.675` y `-0.800`; contra `i = 232, j = 240` ambas lecturas, a `-0.200`.
- **En `contra` el supremo de `a_inv` coincide EXACTAMENTE con el pico de `|E|`**
  (`E_en_supremo_a0 = a_medido_a0` en las 8 filas); en colineal **no** (`79.213443` vs
  `79.981734`).
- **GUARDA DEL DÍA (obligatoria):** las 9 patas son **9 posiciones, no 9 objetos** — y **tampoco son
  9 evidencias**. Cambiar `N` mueve el plano de lectura, no multiplica los objetos. La ley
  `sqrt(N/2)` **no se testea** con esto (la razón colineal interpolada es constante por saturación).
  **No se eleva** el patrón de invariancia: `n = 9` posiciones no fundan familia.
- **Par de posiciones, no dos experimentos** (amplitud casi igual, invariante 2x, `N` **no**
  apareado): `a_medido 79.98173362` (colineal N=1) vs `78.99734564` (contra N=2), diferencia
  relativa **1.25 %**; `a_inv_max` cadencia `1.4278534920762016e14` vs `2.926847388519371e14` V/m,
  razón **2.0498x**. Se cita como **par de posiciones**, nunca como «dos experimentos que difieren».

---

## 9 · Trampas de metro de esta corrida (declaradas)

- **(a) Namespace `colineal`/`contra` NO es el mismo entre motores.** El motor analítico da
  `copropagante N=4 -> a_inv = 0` (onda transversa verdadera) y `coaxial_contra N=4 -> a_inv = 4.0`
  (cancelación de `B`), en **sus** unidades de modelo; el FDTD mide un haz **enfocado/convergente**
  en unidades `a0` normalizadas por `|E|`. Que la pre-inscripción dijera *«el motor analítico da
  `a_inv = 0` para la misma familia»* es, medido, una **colisión de nombres entre dos objetos
  distintos** (medido: en la pata colineal FDTD el `abs(G)/F` interpolado del supremo es **1.4222**,
  no 0). **Registrado, no adjudicado.**
- **(b) `cad20` es un máximo de razones, no una razón de máximos.** Es el máximo, sobre 44 instantes
  muestreados, de `a_inv_max(paso) / E_max(paso)`. Por eso puede acercarse al techo sin que ninguna
  celda/paso muestre 1: en colineal el cociente co-ubicado en el supremo es `0.4513` mientras `cad20`
  es `0.9995`. Las dos cifras son verdaderas y miden **objetos distintos**; quien las reste está
  restando universos.
- **(c) La puerta del sello es de TOLERANCIA, pero esta corrida salió bit-exacta** — y el wobble
  vive **dentro del sello**: `0.9995132753995678` (N=1,4,8,16) vs `…680` (N=2). «Idéntico en todas
  las N» es verdad **hasta la cifra 16**, no hasta el infinito.
- **(d) `N = 1` es `0/0`** en el ancla analítica ⇒ el ancla no cero es `N = 2`; cualquier ley
  `a_inv(N) ∝ sqrt(N)` se testea desde 2, no desde 1.
- **(e) Puerta de escritura:** la corrida corrió 9 patas, escribió 18 filas y **verificó al terminar**
  que `sim/medidas_aN.csv` conservara su sha16, con `EXIT = 3` (rojo) si cambiaba.
  `sha16 antes = despues = 4129d436e2cd081d (intacto: True)`. `sim/maxwell2d.py`
  `1db75ea7b0b8cba4` **sin cambios** (el instrumento no lo editó: reprodujo su bucle).
  Desvío máxima de mi lectura naive contra la de la casa (`maxwell2d.invariante_a`): **`0.00e+00`**
  en las 9 patas.

---

## 10 · Lo que este informe NO toca

`main.tex` **en reposo** (465 l · 23 042 B · `44a3f0b33ad6593e`; nada de aquí se sella ni se cita allí).
`sim/medidas_aN.csv` **intocable** (movido **cero**). `sigma_phi` sin tocar: `sigma*` **solo** por la
puerta pre-registrada `beta en [0.45, 0.55]` (cruce en `0.554987 rad`), **nunca** por la coincidencia
exacta-75 % de Strehl en `N = 16` (`0.556916 rad`). Toda cifra tipo `S` viaja con su `N` y con la
etiqueta **«verificación del solver, NO evidencia»**. Dispersión 4.4 % PICO/FOCO aceptada como barra
metodológica. Lemma 1 sigue **sin autores** hasta tener entrada real en `refs.bib` y DOI verificado.

**Estado:** nada se adjudica; nada se eleva; el estado lo mueve el dueño.
