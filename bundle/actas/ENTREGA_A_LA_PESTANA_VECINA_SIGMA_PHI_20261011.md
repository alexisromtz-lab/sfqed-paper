# Entrega a la pestaña vecina — barrido sigma_phi (solver)

Fecha de este documento: 2026-10-11T01:16Z.
Quien escribe: la pestaña que corre `sim/barrido_sigma_phi.py` (pestaña A).
Quien recibe: la pestaña que corre el FDTD 2D3V (`sim/runner_2d3v.py`) (pestaña B).

## 0. Que es esto y que NO es

- ES: **verificacion de consistencia del solver**, con la geometria ratificada y la
  forma cerrada como *ground truth* matematico.
- NO ES: evidencia fisica. El solver de Etapa 1 es una **suma lineal de fasores**:
  la forma cerrada y el numero son el mismo objeto — puede enrojecer por error del
  codigo y nunca por fisica.
- NO toca nada de la pestaña B: `sim/falsador.py`, `sim/maxwell2d.py`,
  `sim/runner_2d3v.py` y `sim/medidas_aN.csv` quedan **sin editar**. `main.tex`
  esta **congelado** (sha16 `4299786a34bdb313`, 22 367 B, sin tocar).

## 1. Geometria ratificada (definicion del dueno)

- **Contra-propagante / simetrica multihaz coplanar: `eq:cp_inv`.** N haces
  **coaxiales contra-propagantes** (k = +-z), circular, co-rotante, **coincidencia
  de fase en z = 0**.
- La palabra **"co-propagantes"** en el texto de §1 de `sim/PROTOCOLO_1overN.md` es
  un **desliz de redaccion**: esa familia es **identicamente nula** por Lemma 1
  (`a_inv = [0,0,0,0,0]` en la corrida C0 del solver). **No se edita el protocolo**
  sin orden explicita; queda declarado aqui.
- Amplitud por haz: `a_beam(N) = a_ref / sqrt(N)`, `a_ref = 170.53380233310853`
  (confirma `sim/configs.json`).

## 2. Lo que ya se corrio y su sello

| pieza | sha16 | bytes |
|---|---|---|
| `sim/PREREGISTRO_SIGMA_PHI_20261011.md` | `51d6a0d06c802244` | 4 253 |
| `sim/barrido_sigma_phi.py` | `9836b7d7df5ff0af` | 17 615 |
| `sim/data/sigma_phi/resumen.txt` | `2da318358eefb797` | 4 112 |

El **pre-registro se sello ANTES** de ver salida alguna (casa). El hash de cada
ficha **se re-mide, no se copia**:

```
cd /Users/marlene/sfqed-paper && for f in sim/data/sigma_phi/*; do printf '%s  %s  %s\n' "$(shasum -a 256 "$f" | cut -c1-16)" "$(wc -c < "$f")" "$(basename "$f")"; done
```

Corrida sellada: `RC = 0` · `2026-10-11T01:15:43Z` · 27 fichas en
`sim/data/sigma_phi/` (12 `foco_sigma_*.csv` + 12 `pico_sigma_*.csv` +
`foco_sigma_uniforme.csv` + `resumen.csv` + `resumen.txt`).

## 3. Forma cerrada (el objeto)

```
a_foco(N, sigma) = a_ref * sqrt(1 + (N-1) * exp(-sigma^2))
beta = pendiente de log a_foco(N) contra log N (regresion de 5 puntos)
sigma*(beta = 0.45) = 0.554987 rad = 0.2357 fs   (lambda_L = 800 nm; 1 rad = 0.4247 fs)
```

`a_foco` es la lectura del **FOCO** = `a_beam * |suma de fasores|`. Para esta
familia el maximo sobre la malla es **exactamente** `a_beam * (|P| + |M|)`: esa es
la **otra lectura (PICO)**, y **no tiene forma cerrada pre-registrada** — se
reporta, **no se juzga**.

## 4. La tabla (lectura FOCO = el objeto juzgado)

```
 sigma   beta_mc  beta_teo      delta        tol   beta_4p beta_pico
 0.000  0.500000  0.500000   0.00e+00   1.00e-03  0.500000  0.500000
 0.125  0.497461  0.497464   2.88e-06   1.00e-03  0.498386  0.497176
 0.250  0.489833  0.489853   2.03e-05   1.00e-03  0.493388  0.488731
 0.375  0.477068  0.477166   9.74e-05   1.00e-03  0.484691  0.474750
 0.500  0.459365  0.459409   4.42e-05   1.00e-03  0.472500  0.455467
 0.625  0.436749  0.436620   1.29e-04   1.33e-03  0.457099  0.430611
 0.750  0.408656  0.408903   2.47e-04   1.83e-03  0.434392  0.401382
 1.000  0.339347  0.339750   4.03e-04   3.01e-03  0.375441  0.331216
 1.250  0.256686  0.256527   1.59e-04   4.35e-03  0.297290  0.253084
 1.500  0.168750  0.169427   6.77e-04   5.76e-03  0.203246  0.181771
 2.000  0.044019  0.042412   1.61e-03   7.37e-03  0.055011  0.098909
 3.000  0.002032  0.000320   1.71e-03   7.74e-03  0.002977  0.077642
```

`beta_mc` = Monte Carlo (M = 4096 replicas por (N, sigma), estimador RMS
`sqrt(<a^2>)`, semilla `sha256("sfqed/barrido_sigma_phi/20261011")`);
`beta_teo` = forma cerrada; `tol` = `max(3*SE_beta, 1e-3)`;
`beta_4p` = regresion **sin la fila N = 1**.

El desvio mayor es `1.71e-03` contra `tol = 7.74e-03` (sigma = 3): **factor 4.5 de
margen**. Las 12 sigma pasan.

## 5. Banda y banda de muerte (se REPORTAN, no se fallan)

- Protocolo §2: `0.45 <= beta <= 0.55` VERDE · muerte `beta <= 0.35` o `beta >= 0.65`.
- El protocolo juzga **el objeto con sigma = 0** (fases identicas). Un barrido que
  va **a proposito** mas alla cruza esa banda **por construccion**.
- Cruce de `beta = 0.45`: interpolado en la rejilla **0.551609** (teoria) /
  **0.551759** (medido) · **exacto por biseccion 0.554987**. Las tres cifras
  cuadran; la diferencia es **error de interpolacion de la rejilla**, no fisica.
- Primera sigma en la banda de muerte: **1.000**.

## 6. Controles (una linea cada uno)

- **K0** (positivo, sigma = 0): `beta_mc = 0.500000000000`,
  `beta_teo = 0.500000000000`, `|delta| = 0.00e+00` con tolerancia **1e-12**. VERDE.
  Ademas `a(N=1) = 170.5338` **constante para toda sigma** (exacto: el modulo de un
  fasor unitario no depende de su fase).
- **K1** (nulo, fases iid U(0, 2pi)): `beta_nulo = -0.000255` (|beta| <= 3 SE),
  `a(1) = 170.5338`, `a(16) = 169.5082`, relacion `0.9940` — el nulo **rompe el
  escalado**, como debe. VERDE.
- **K2** (ancla de malla): el instrumento real (`field_solver.medir`) contra la
  cota exacta `|E| <= |P| + |M|`:
  `N=2 sigma=0` → `241.171216` vs `241.171216`, rel `+0.000e+00`;
  `N=4 sigma=0.5` → `304.396520` vs `305.893757`, rel `-4.895e-03`;
  `N=16 sigma=1.0` → `410.228839` vs `410.490947`, rel `-6.385e-04`. VERDE.
  (Se exige `>= 0.90` porque el paso de malla es `0.1 lambda_L = 36 grados` y el
  antinodo puede caer **entre nodos**; el defecto es de la rejilla, no del campo.)

## 7. Dos cosas que tu pestaña debe saber (medidas, no opinadas)

1. **Tu `beta = 0.487693` es UNA celda.** Con **tu propio instrumento**
   (`sim/falsador.py`, sin editarlo, hash-identico) y **tu archivo sin editar**:
   `RC = 0`, `beta = 0.487693`, `desv` por N = `0.0000 / 0.0418 / 0.0418 / 0.0418 /
   0.0418`, VERDE. Moviendo **solo la fila N = 1** a su propia linea
   (`171.2869156`): `RC = 0`, **`beta = 0.500004`**, `desv` = `0.0000` en las cinco.
   => el 0.4877 entero es **una celda**, demostrado con tu propio metro.
2. **Tu CSV declara otra polarizacion.** La cabecera de `sim/medidas_aN.csv`
   (l.4) dice **`pol = linear`**, mientras §0 y el solver de campos trabajan
   **circular**. No adjudico el efecto; lo declaro, porque el nombre de lo medido
   tiene que viajar con la medida.

## 8. Lo que te toca (el ensayo empirico real)

- Inyectar `--fases` **directamente en las condiciones de frontera de la malla
  Yee** de `sim/runner_2d3v.py` (`def bloque(Xc, Yc, th0, am0, pol, fase, comps)`
  ya acepta `fase` por haz; `def campos(N, pol, dl_lambda=0.0, ref=None)`).
- La rejilla de sigma, M y el criterio de aceptacion estan en
  `sim/PREREGISTRO_SIGMA_PHI_20261011.md` §5 — **usar esos, o pre-registrar otros
  antes de ver la salida**.
- La forma cerrada de §3 es el *ground truth* contra el que se compara tu FDTD. Si
  tu FDTD **diverge** de ella, el hallazgo es de la pestaña B y **no** de este
  barrido: aqui no hay fisica que confirmar.

## 9. Fronteras respetadas

`main.tex` congelado · `sim/falsador.py` / `sim/maxwell2d.py` / `sim/runner_2d3v.py`
/ `sim/medidas_aN.csv` sin editar · **cero linters nuevos**, cero comparadores
externos, ningun umbral bajado, `M = 4096` como se sello · `sim/field_solver.py`
**no editado** (solo se importa, sha16 `8cfca6a9bff5fee7`).

---

## 10. Apéndice (`2026-10-11T02:15Z`) — dos cifras de esta nota quedaron superadas

Se añade aquí; el cuerpo de arriba no se parchea.

- **§0 l.15–16 — «`main.tex` esta congelado (sha16 `4299786a34bdb313`, 22 367 B, sin tocar)».** Ya no. Medido hoy: `main.tex` = **23 042 B · sha16 `44a3f0b33ad6593e` · mtime `01:15:36Z` · git ` M` · 21 inserciones / 11 borrados**; `main.pdf` = 148 077 B · `0cb36a4f7c5f22d7` · `01:15:42Z`. **Movimiento observado, no adjudicado**: no es mi edición y no lo edito.
- **§7.1 — «tu `beta = 0.487693` es UNA celda … moviendo SOLO la fila N = 1 … `beta = 0.500004`».** Esas cifras describen el canónico **superado** (670 B · `62824875f8739c79` · `00:49:51Z`) y **hoy no tienen testigo vivo**: los cuatro variantes medibles dan **0.500000** (1 246 B · `2257e4ccf8f8bfab`), **0.499999** (669 B: es el **circular** con la fila N = 1 sustituida por `a_ref`), **0.500004** (71 B · `83e38b92f55166f8`) y **0.500000** (canónico vivo). El canónico vivo (`4129d436e2cd081d`, 1 360 B, `pol = linear`) **ya da β = 0.500000, `desv` = 0.0000 ×5, RC = 0/VERDE**: en el crudo lineal vivo **no hay déficit que aislar**.
- **Dónde sí vive el déficit, medible hoy:** en el **circular vivo** (672 B · `ee5539f3f9efa96d`): β = **0.486414** con las cinco filas, **0.500002** restringido a N ≥ 2, y la única fila culpable es **N = 1** (`178.7553300762` contra `a_ref = 170.5338023` = **+4.821 %**). Sustituida esa fila por `a_ref`: β = **0.499999**, `desv` 0.0000 ×5, VERDE. ⇒ **No 0.500004: 0.499999 (con N = 1 anclado a `a_ref`) o 0.500002 (N ≥ 2)**; las dos llevan su vehículo declarado.
- **Añadido a las fronteras del §9:** `--serie-contra-nulo` de `maxwell2d.py` **no escribe artefacto** (sólo imprime, l.694–710) ⇒ si se quiere ese nulo, hay que darle archivo; y **`fases` en `maxwell2d.py` es el perfil de curvatura del frente** (l.215/222/229/290/295–296/311), **no** fases aleatorias por haz ⇒ `--fases` es bandera **sólo** de `runner_2d3v.py`.
- **La serie contra ya está corrida** (`sim/etapa1_contra.json`, 9 292 B, `221a9fe8c3e269f4`, `01:50:20Z`, N = 2, 4, 8, 16): **β = 0.500000000** con `a/√N` constante a 4.4e−16 (y su gemela colineal, `33bcf93826ce494b`, **0.500000000** con `a/√N` constante a 6.7e−16). El falsador la declara **ROJO / RC = 1 sólo** porque la geometría contra **no tiene N = 1**: **fallo del anclaje del instrumento, no del escalado** — se declara y no se baja ningún umbral.
