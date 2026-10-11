# ADENDA — auditoría de la lectura de `864f4a4` (geometría contra-propagante)

> `sim/ETAPA1_CONTRA_REPORTE_20261011.md` **no se parchea**: recibe este apéndice.
> Lo que sigue no es una opinión sobre la lectura: es el crudo puesto al lado de la prosa.

`T_UTC = 2026-10-11T02:16:09Z`

UNIVERSO DECLARADO: malla xy 480x480 = 12 lambda_L por lado, dx = lambda_L/40; transito fisico = 19.485 lambda_L (los 866 pasos pre-registrados a CFL 0.9) = 1113 pasos a CFL 0.7; diagnostico cada 20 pasos (PROTOCOLO_1overN.md §4); CFL de 2D = 0.7 [CORREGIDO del 0.9 pre-registrado: limite de von Neumann en 2D = 1/sqrt(2) = 0.7071]; vacio clasico, SI 2019 (CODATA 2018) via sim/params.py; motor numpy; unidad de conteo = celda; VENTANA DE MEDIDA = celdas [100,380] (excluye la linea de inyeccion, que no es objeto de Maxwell: ahi cB/|E| = 0.514 y |E| = 6.9x lo prescrito, medido)

Piezas y sellos:

| pieza | sello | hora |
|---|---|---|
| `sim/maxwell2d.py` | sha16 `1db75ea7b0b8cba4` | — |
| `sim/falsador.py` | sha16 `f04551c7f19ce73a` | — |
| `sim/etapa1_contra.json` | 9292 B · sha16 `221a9fe8c3e269f4` | `01:50:20Z` |
| `sim/etapa1_colineal.json` | 11530 B | `01:15:44Z` |
| `sim/medidas_aN.csv` (sellado) | 1360 B · sha16 `4129d436e2cd081d` | intacto, verificado `02:16:09Z` |
| crudos | `/tmp/serie_contra_out.txt` · `/tmp/serie_contra_nulo_out.txt` · `/tmp/sonda_contra_n4_out.txt` · `/tmp/sonda_contra_nulo_dcha20_out.txt` | `01:50Z`–`02:15Z` |

Motor de esta auditoría: `python3 -B` + `json` + `shasum`. **Sólo lectura de `sim/`**: no se escribió CSV ni JSON, no se tocó ninguna pieza sellada.

---

## §1 Lo que la lectura acierta — con el comando detrás

1. **β = 0.500000** (control interno del instrumento, `/tmp/serie_contra_out.txt` l.50). Medido como pendiente log-log de `a_medido` contra N: `78.997346 · 111.719118 · 157.994691 · 223.438235` para N = 2 · 4 · 8 · 16 ⇒ cocientes `1 · 1.41422 · 2.00000 · 2.82843` = `1 · √2 · 2 · 2√2`. Cae **dentro** de la banda pre-registrada `[0.45, 0.55]`.
2. **F se activa**: `F/(ε0E²/2)` = **+0.8444** contra vs **+0.1055** colineal. Y el contraste **tiene crudo, no sólo prosa**: `sim/etapa1_colineal.json` trae `cB_sobre_E_en_el_pico = 0.945773` y `F_rel_pico = 0.105514` **idénticos en las cinco filas** (N = 1, 2, 4, 8, 16, `pico_i = 217`). El `0.9458` de la prosa del reporte es ese crudo redondeado.
3. **La identidad del máximo es correcta como álgebra**: con `x = linspace(0, 4π, 400001)`, `max|A·e^{ikx} + B·e^{−i(kx+φ)}|` = `A+B` = 1.700000 / 2.000000 / 3.000000 para (A,B,φ) = (1,1,0) · (1,1,π) · (1,0.7,π) · (2,1,π). No hay cancelación en el máximo.
4. **El corrimiento λ/4 está medido**: λ/4 = 10.0 celdas · λ/2 = 20.0 celdas; el pico de la ventana pasa de la celda **232** a la **242** = **+10 celdas exactas**. El desplazamiento predicho por la identidad se ve.
5. **El RC = 1 es del ancla, no del objeto.** `falsador.py` l.121–125: `ref = None; for n, a in pares: if n == 1.0: ref = a; break` · `if ref is None: fails.append("sin N=1 no se puede medir el cociente contra sqrt(N)")`. El gate ancla en **una fila de la propia medición**; en la geometría contra **esa fila no puede existir** (`terminos_de` exige N par: pares enfrentados). El único fallo del veredicto es la ausencia de su ancla. `a_ref_N_1` de `configs.json` (= 170.53380233310853) **no** se usa para anclar: sólo alimenta el control `--sintetico` (l.82), que sale VERDE.

---

## §2 Lo que la lectura invierte: `a_foco` SUBE, no cae

| corrida | `a_medido` | `a_foco` | `a_foco/a_medido` | pico (celda) | `cB/|E|` en el pico | `cB/|E|` en el foco |
|---|---|---|---|---|---|---|
| contra N=2 entero | 78.997346 | 37.658422 | 0.4767 | (232,240) = −0.200 λ | 0.394424 | — |
| contra N=4 entero | 111.719118 | 53.257052 | 0.4767 | (232,240) = −0.200 λ | 0.394424 | **1.982** |
| contra N=8 entero | 157.994691 | 75.316845 | 0.4767 | (232,240) | 0.394424 | — |
| contra N=16 entero | 223.438235 | 106.514103 | 0.4767 | (232,240) | 0.394424 | — |
| contra N=4 **desplazado λ/2** | 109.933787 | **106.206118** | **0.9661** | (242,240) = +0.050 λ | 0.3878 | **0.445** |

- `a_foco` **sube** `53.257052 → 106.206118` = **× 1.9940**. `a_foco/a_medido` pasa de **0.4767 → 0.9661**: el desfase hace que el antinodo **caiga sobre el foco**, no que lo cancele.
- `a_medido` apenas se mueve: `111.719118 → 109.933787` = **−1.60 %**.
- En **ninguna** de las dos corridas hay cancelación en el foco: allí hay **0.48** y **0.97** del pico de la ventana.
- La curva de `a_foco` **en el nulo** (×1.994) y la curva **en N** (×√N) son dos objetos distintos. El rerun declarado reproduce **bit a bit** la corrida de `01:52:41Z`: `a_medido = 109.933787`, `a_foco = 106.206118`, `pico_i = 242` (control de determinismo a las dos horas).

---

## §3 Dos cifras, una medición: `F = 1 − (cB/|E|)²`

Verificado exacto en las tres filas citadas:

| `cB/|E|` | `1 − (cB/|E|)²` | `F/(ε0E²/2)` impreso |
|---|---|---|
| 0.394424 | 0.844430 | 0.844430 |
| 0.3878 | 0.849610 | 0.8496 |
| 0.945773 | 0.105514 | 0.105514 |

⇒ «F salta» y «cB/|E| colapsa» **no son dos observaciones: son una**, contada en dos rótulos. Y la propia lectura las escribe como dos hallazgos separados en §1. El objeto que cambió es **uno**.

Corolario medido: `cB/|E|_pico = 0.394424` y `F_pico = 0.844430` son **idénticos en N = 2, 4, 8, 16** ⇒ la forma del campo es **independiente de N** (lo único que escala es la amplitud, √N). «Progresivamente» describe mal: no hay evolución con N; hay **una** forma y **un** factor.

---

## §4 El rótulo: el pico de la ventana no es el foco

- `0.3944` es el campo rotulado por el propio instrumento `cB/|E| en el pico de la ventana`, y ese pico está en la celda **(232, 240) = −0.200 λ del foco**, no en el foco.
- En el **foco** (celda 240,240), crudo de la sonda del eje (`/tmp/sonda_contra_n4_out.txt`): `|E| = 2.13741e14 V/m` · `a0 equiv = 53.2571` · **`cB/|E| = 1.982`** ⇒ **B domina en el foco** en la corrida entera. El antinodo puramente eléctrico (`cB/|E| → 0`) **no se observa** en el foco.
- Con el desfase λ/2 el foco pasa a **`cB/|E| = 0.445`** (antinodo **parcial**) y `a0 equiv = 106.2061`.
- La misma advertencia vale en la colineal: su pico está en la celda **217** = −0.575 λ del foco.
- En ambos casos el rótulo correcto es «en el pico de la ventana»; leerlo como «en el antinodo/el foco» es la trampa de denominador de siempre: **la misma palabra, dos celdas, dos números** (0.3944 vs 1.982).

---

## §5 El funcional de volumen propuesto **desborda a cero**

El «único observable inmune al desfase» de la lectura es `∫ exp(−π E_cr/E) dV`. Medido:

- `a0_cr = λ_L/(2π λ_C) = 329718.758651`.
- Para **todos** los valores del barrido medido (`a0` = 11.2400 · 53.2571 · 106.2061 · 111.7191 · 170.5338 · 685.1550): `E_cr/E` = 92156.8 · 19449.8 · 9753.1 · 9271.8 · 6074.1 · 1511.8 ⇒ **`exp(−x) = 0.0` exactamente en los seis**.
- Para que `exp(−x)` llegue siquiera a `1e-2` haría falta `a0 = 224938.6` = **328.3 × el mayor del barrido**.

⇒ En este régimen el funcional vale **0** con desfase y sin desfase: **una salida que no puede diferir no es evidencia**, y no puede ser «el único observable inmune» porque no es un observable. No está construido en el instrumento: se propone, no se mide.

---

## §6 Dos trampas de mi propio metro, cazadas en esta auditoría

1. **`.get()` que devuelve `None` y parece una declaración del objeto.** Leí `a_ref_N_1 = None` en la raíz de los dos JSON; al contar claves: `['T_UTC', 'UNIVERSO DECLARADO', 'etiqueta', 'filas', 'modo', 'nulo']` ⇒ **la clave no existe**. El `None` era mío, del diccionario consultado, no del instrumento. (Familia: el `0` del metro, no del objeto — aquí un `None` mío, no del objeto.)
2. **Mismo nombre, dos objetos:** `106.206` (contra N=4 **desplazado**) y `106.514` (contra N=16 **entero**) son cifras parecidas que **no** se pueden restar ni comparar: distinto N y distinta geometría. Se imprimen con su etiqueta o no son cifras.

---

## §7 ALCANCE — qué NO prueba esto

- **F > 0 ≠ Schwinger.** Que `F/(ε0E²/2) = +0.8444` diga «más eléctrico que magnético» no mide producción de pares: el solver es **clásico y lineal**; `a0` en el barrido llega a **685** frente a `a0_cr ≈ 3.2972e5` ⇒ **~480× por debajo**. El campo crítico **no** se alcanza.
- **El desplazamiento λ/2 no se hizo en la malla entera**: `a_medido` lo ignora por construcción (el máximo de la ventana no distingue la fase), pero el foco **sí** lo ve (×1.994). Un nulo que sólo un punto del eje ve **no** es un nulo del instrumento.
- **La descomposición `0.698398 = (1/√2)·0.987675` sigue siendo conjetura declarada**, no medida. Y «proyección geométrica de los vectores de onda cruzados» **no tiene comando**: los haces contra viajan **antiparalelos sobre ±x** (opuestos), no cruzados. El factor **es** invariante en N (medido, cuatro filas); su *explicación* no está medida.
- **2 → 16 son 3 duplicaciones** (`log2(16/2) = 3`), no «4 órdenes de duplicación».
- El **nulo colineal** (`--serie-nulo`) sigue **sin correr**: declarado pendiente, no ordenado.

---

## §8 Frontera

- Se tocó **sólo** `sim/`: esta adenda. **No** se editó `maxwell2d.py` (`1db75ea7b0b8cba4`) ni `falsador.py` (`f04551c7f19ce73a`) ni ninguna pieza sellada.
- `sim/medidas_aN.csv` **intacto**: 1360 B · `4129d436e2cd081d`, verificado antes y después (`02:16:09Z`).
- `main.tex` y `main.pdf` siguen `M` en `git status`, y los `sim/*` de la otra ventana siguen **sin seguimiento**: declarados, no adjudicados, no tocados.
- `HEAD = 864f4a4`.
