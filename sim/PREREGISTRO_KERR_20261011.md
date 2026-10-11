# PRE-REGISTRO DE LA LINEA B (KERR) — el nulo se sella antes de la primera cifra

T_UTC de redaccion: 2026-10-11T03:14:53Z
Estado: CERRADO. Es un pre-registro: nada de este documento se edita despues de su sello; lo que ocurra en la corrida va a un reporte aparte.
Costo: 0 de computo. Este documento no corre nada en este Mac.
Instrumento congelado: `sim/maxwell2d.py` sha16 `1db75ea7b0b8cba4` · 715 l. El hash se mide FUERA y se reporta con su hora: una identidad impresa dentro de una pieza describe su version anterior.
Frontera de contencion: `sim/medidas_aN.csv` sha16 `4129d436e2cd081d` (1360 B · 2026-10-11T01:15:44Z) NO se toca. Nada fuera de `sim/` se toca. `main.tex`, `main.pdf` y los archivos de la pestana vecina: ajenos.

## §0 Reglas de entrada (cinco, heredadas y medidas)

1. No se publica que el modelo funciona: se publica que se puede poner rojo.
2. Un control que no puede diferir no es un nulo: es un candado.
3. Toda cifra viaja con su hora, su universo y su unidad.
4. El nombre de un mecanismo tiene que existir en el instrumento antes de poder afirmarlo (§2.b).
5. La pieza vieja no se parchea: solo recibe apendices (§6).

## §1 El objeto (lo medido, no lo citado)

- El metro del invariante, verbatim del instrumento: L266 `def invariante_a(F):` -> L272 `Fs = 0.5*(P.EPS0*e2 - b2/MU0)` -> L273 `Gs = (Ex*Bx+Ey*By+Ez*Bz)/(P.C*MU0)` -> L275 `return np.sqrt(np.maximum(raiz+Fs, 0.0))/math.sqrt(P.EPS0)`.
- Forma cerrada del vacio, medida hoy (bloque A): `F/(0.5*EPS0*|E|^2) = 1 - q^2/R`, con `q = cB/|E|` y `R = EPS0*MU0*C^2 = 0.99999999945558082` (`|R-1| = 5.444e-10`). Residuo maximo sobre 200 000 campos aleatorios: `1.554e-15` => la identidad es exacta al ULP.
- Nota de unidad que gobierna todo test de residuo: `R` no es 1 exacto porque el SI no lo es en EPS0/MU0/C. Ese `5.444e-10` es el piso de maquina del invariante y hay que declararlo como piso, no como senal.
- Linea B: `P_NL = EPS0*chi3*|E|^2*E` y `D = EPS0*E + P_NL`. Viene del material externo de la pestana vecina; entra como `[REF]`, nunca por autoridad (Adenda 7 §3.b y §6).

## §2 Auditoria de los dos nulos propuestos (el diagnostico acierta; su propio metro falla)

### §2.a El Nulo B, tal como esta impreso, no es un nulo: es un metro de `q` — y enrojece en el regimen LINEAL

Medido hoy (bloque A): `delta_F = 1 - q^2 - F/(0.5*|E|^2)` **no contiene** `|E|` ni `chi3`; su forma cerrada es `(1 - q^2) - EPS0*(1 - q^2/R)` (diferencia medida contra 200 000 campos aleatorios: `0.000e+00`). En la pareja YA medida de la corrida CONTRA, `q = 0.3944240989060718`:

```
delta_impreso = 0.8444296302
```

y el propio texto fija para el regimen lineal `delta_F == 0 dentro del error de discretizacion`, con umbral impreso `1e-3` => **enrojece por 844 x con `chi3 = 0`**. Su minimo (`delta -> 0`) esta en `q = 1`, o sea `|F| = 0`: el delta mide `q` — una propiedad puramente lineal — y no la no-linealidad.

Clase: la misma familia que el candado que el propio texto expulsa (una salida que no puede diferir no es evidencia), un piso arriba — aqui el defecto esta en el **metro propuesto**, no en el candado.

Lo que si es identidad: `F/(0.5*EPS0*|E|^2) - (1 - q^2/R) = 0` al ULP. Cualquier diferencia entre las dos formas impresas es de **unidad**, no de fisica.

### §2.b El metro del invariante es funcion de los CAMPOS: no puede ver el mecanismo

`invariante_a(F)` lee solo `e2`, `b2` y `E.B` => es una funcion algebraica de `(E, B)`. Medido hoy, ocurrencias en el instrumento y en `params.py`: `chi` 0/0 · `CHI` 0/0 · `Kerr` 0/0 · `kerr` 0/0 · `P_NL` 0/0 · `no_lineal` 0/0 · `nolineal` 0/0 · `polariz` 0/0 · `n2` 0/0 · `NL` 0/0. El nombre del mecanismo no existe en el instrumento.

Corolario que gobierna todo este pre-registro: aun con `chi3` implementado, ese metro seguira devolviendo la misma funcion de `(E, B)`; lo unico que puede moverse es la **evolucion de los campos**. Por eso el Nulo B no puede anclarse en "la identidad se rompe": tiene que anclarse en una prediccion calculada CON la ecuacion constitutiva declarada (§3, F2).

### §2.c El Nulo A (morfologia) es el unico falsable de los dos — con su piso declarado

`R_w = w_out/w_in` si depende de `chi3` (autoenfoque). Tres reparos medidos:

1. Exige que el termino exista: hoy no existe (§2.b) => es clausula para despues de la edicion, no para hoy.
2. Su tolerancia no es libre. Piso lineal de la malla, calculado hoy (bloque C; convencion de haz sobre el perfil transversal, declarada como ESTIMACION y no como medicion del solver): `W0 = 80 celdas` · `lambda = 40 celdas` · `brazo = 160 celdas` · `z_R = pi*W0^2/lambda = 502.65 celdas` => `brazo/z_R = 0.3183` => `R_w(0) = sqrt(1 + 0.3183^2) = 1.049439` => **4.94 % de ensanchamiento sin ninguna no-linealidad**. Un `Delta_w_tol` por debajo de eso mide difraccion, no Kerr.
3. `P_cr` exige el mapeo `chi3 -> n2` en SI, que es `[REF]` y no nuestro, y la geometria del solver es una losa 2D3V, no un haz 3D: la convencion se declara o no se mide.

### §2.d Lo que el texto acierta, medido (COINCIDE)

- L340-345: el invariante se evalua solo en multiplos de `DIAG_CADA` y se guardan **escalares globales** (`a_inv_max`, `a_inv_rel_max`), sin indice `(i,j)` y sin paso `k`. Medido en la fuente: COINCIDE.
- Editar ese monitor cambia el hash del solver, invalida los sellos previos y obliga a re-correr los controles de CFL y energia: COINCIDE.
- La errata de la Adenda 7 §3.c (`mascota_esponja` -> `mascara_esponja`, L150; `campos_vacios` L145 queda exacta): COINCIDE. Viaja como apendice en su propia base (§6).
- El piso de difraccion y el piso de unidad (§1, §2.c) **no** estan en el texto recibido: se anaden aqui y son el unico cambio de fondo a su propuesta.

## §3 El pre-registro (clausulas, selladas tal cual)

| Clausula | Valor pre-registrado | Clase |
|---|---|---|
| Ecuacion constitutiva | `D = EPS0*E + P_NL`, `P_NL = EPS0*chi3*|E|^2*E` | modelo declarado |
| Candado de regresion | `chi3 = 0` reproduce la serie lineal **al bit** | CANDADO, no nulo: la operacion es exacta => la salida no puede diferir; vigila que la rama lineal no se rompio. Se corre y se reporta como gate, jamas como evidencia |
| Control positivo de forma | `chi3` plantado `> 0` debe mover `q` (o `a`) mas alla de la banda | unico control con capacidad de enrojecer sin ambiguedad |
| F1 (geometrico) | `R_w(chi3) <= 0.90 * R_w(0)` a `P = 1.5*P_cr` | falsable; piso declarado 4.94 % (§2.c); exige el termino implementado y un brazo mas largo que `0.318 z_R` |
| F2 (invariante, REESCRITO) | desviacion de `q` (o de `F/(0.5*EPS0*|E|^2)`) respecto de la prediccion calculada CON la constitutiva declarada, en el pico de interaccion: `> 1e-3` relativo | falsable; NO se ancla en la diferencia de dos formas de la misma identidad (§2.a) |
| Piso de unidad | `5.444e-10` (`|R-1|`): todo residuo por debajo de eso es unidad, no fisica | restriccion |
| Frontera de contencion | `sim/medidas_aN.csv` (`4129d436e2cd081d`) intocable; instrumento en `1db75ea7b0b8cba4` | restriccion |
| Fuera de la v1 | coordenadas `(i,j,k)` del supremo del invariante | postergado CON su costo declarado: editar el monitor + hash nuevo + re-verificar CFL y energia |
| Secuencia de disparo | primero el candado (y su reporte), despues F1/F2, y solo despues de la edicion declarada | orden |

## §4 Lo que hoy NO se puede afirmar

1. Que el invariante "se rompe" con `chi3`: no medido — y el metro propuesto para medirlo no puede diferir (§2.a).
2. Donde y cuando ocurre el supremo: `(i,j,k)` no se guardan; la pregunta espacial esta postergada con su costo (§3, ultima fila).
3. Que F1 pueda correr hoy: el termino no existe en el instrumento (§2.b).
4. Que el ancho focal sea medible con la fuente actual sin declarar antes como se separa el haz saliente del entrante: el propio instrumento declara un artefacto de acumulacion de `6.9x` en la linea (`cB/|E| = 0.514`) para la fuente aditiva suave.

## §5 Frontera y contencion

- Nada fuera de `sim/` se toca. `main.tex` y `main.pdf` (modificados por otra mano) y los archivos de la pestana vecina: ajenos, ni se editan ni se citan como nuestros.
- `sim/medidas_aN.csv` intacto: `4129d436e2cd081d`.
- La edicion del monitor, cuando se autorice, sera una **decision declarada** con hash nuevo y re-verificacion de los dos gates (energia y CFL), no un parche silencioso.

## §6 Fe de erratas para la Adenda 7 (viaja como apendice, no como parche)

- La Adenda 7 §3.c imprime `mascota_esponja`; la fuente dice `mascara_esponja` (L150 de `sim/maxwell2d.py`). `campos_vacios` (L145) queda exacta.
- Va en su propia base: `ADENDA_8_AL_ACTA_DE_PUBLICACION_LA_FE_DE_ERRATAS_DE_LA_ADENDA_7_20261011.md`. El numeral 8 estaba libre **en esa base** (los dos `ADENDA_8_*` del directorio pertenecen a otra acta): los numerales son locales a su acta base.
- El cuerpo de la Adenda 7 no se edita.

## §7 Sellos

- Los sellos de este documento (lineas, bytes, sha16, encabezados) se miden FUERA y se reportan con su hora. La pieza no imprime su propio sha16 vigente: seria el de su version anterior.
- Universo y motor de cada cifra de este documento: los dos bloques de terminal de `2026-10-11T03:14:18Z` y `2026-10-11T03:14:53Z`; motor `python3 -B` / `grep -o` / `sed`; unidad = ocurrencia / linea / ULP; ventana = reloj UTC de esos dos encabezados.
- Erratum de metodo de este ciclo, declarado: mi primer bloque A imprimio A4/A5 con una forma cerrada que su propio A3 desmentia (uso `(1-q^2)*(1-1/R)` donde la medida daba `(1-q^2) - EPS0*(1-q^2/R)`). Lo delato el A3 del mismo bloque y se corrigio en el bloque siguiente. Ninguna cifra de §2.a sale del bloque defectuoso.
