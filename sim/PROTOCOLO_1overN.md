# Pre-registro — Protocolo de la serie 1/N (simulación)

Estado: **PRE-REGISTRO** (escrito antes de la primera corrida de PIC; sin datos).
Comando que respalda cada cifra: `python3 -B sim/params.py` y
`python3 -B sim/gen_configs.py`, corridos a `2026-10-11T00:04:49Z`.
Artefacto que se juzga: `sim/configs.json` (predicho) contra `sim/medidas_aN.csv` (medido).
Verdugo: `python3 -B sim/falsador.py` (0 = verde · 1 = rojo · 2 = sin medida).

El manuscrito es la fuente de las fórmulas; este protocolo NO las reescribe. Sus
ecuaciones se citan por **label**, nunca por número de memoria:
`eq:lin_fields` · `eq:lin_inv` · `eq:cp_fields` · `eq:cp_inv` · `eq:oneoverN`.

---

## §0 Universo declarado

UNIVERSO DECLARADO: SI 2019 (CODATA 2018) + `lambda_L = 0.8 µm` **[ELEGIDO]**,
`tau = 20 fs` **[ELEGIDO]**, `w0 = 2 lambda_L` **[ELEGIDO]**, `Sigma = 100 J`
**[ELEGIDO]**, malla `N ∈ {1,2,4,8,16}` **[ELEGIDO]**; intensidad definida para
onda **circular** de amplitud `E0` (`I = eps0 c E0²`) y **no** para lineal (esa vale
la mitad). Motor de la tabla: python3 stdlib. Motor del juicio: `sim/falsador.py`.

Convención declarada porque decide el número: dos convenciones de intensidad dan
dos cifras distintas para el mismo campo. Al publicar cualquier `I` se declara cuál.

## §1 Objeto y cantidad falsable

**Objeto:** la energía umbral de un pulso láser contra el campo crítico, cuando la
misma energía total se reparte en `N` pulsos co-propagantes **co-rotantes**
circulares en coincidencia de fase.

**Cantidad falsable:** la pendiente en log-log

```
beta = d log(a_tot) / d log(N)      a energía total fija y tau fija
```

El modelo del paper (`eq:oneoverN`, con `eq:cp_inv`) predice `beta = 0.5`, es decir
`a_tot(N) = sqrt(N) a_ref` y por tanto umbral de energía `∝ 1/N`.

## §2 Banda pre-registrada (no se toca después de ver la salida)

| Regla | Umbral | Acción |
|---|---|---|
| `beta` dentro de banda | `0.45 ≤ beta ≤ 0.55` | **VERDE** |
| banda gris | `0.35 < beta < 0.45` ó `0.55 < beta < 0.65` | **ROJO** (no concluyente, se declara gris) |
| zona de muerte | `beta ≤ 0.35` ó `beta ≥ 0.65` | **ROJO** (escalado refutado) |
| fallo por caso | `|a(N)/(a(1)·√N) − 1| > 0.20` en algún `N` | **ROJO** |

Declarado *antes* de la primera cifra: la banda, la tolerancia `0.20` y la malla de
`N`. Elegirlas después es familia (a) y no valdría más que un `3/4` elegido al ver
el resultado.

**Nulo:** el escalado debe **caer** con desajuste declarado (§5, control 2). Si el
escalado sobrevive al desajuste, no mide coherencia: mide otra cosa.

## §3 Serie

Predicho por el modelo (no medido) — `python3 -B sim/gen_configs.py`:

| N | Σ/N [J] | a_beam | a_tot_pred | beta | I_tot [W/cm²] |
|---|---|---|---|---|---|
| 1 | 100 | 170.53 | 170.53 | 0.50 | 1.243×10²³ |
| 2 | 50 | 120.59 | 241.17 | 0.50 | 2.487×10²³ |
| 4 | 25 | 85.27 | 341.07 | 0.50 | 4.974×10²³ |
| 8 | 12.5 | 60.29 | 482.34 | 0.50 | 9.947×10²³ |
| 16 | 6.25 | 42.63 | 682.14 | 0.50 | 1.989×10²⁴ |

`a_ref(N=1) = 170.534`. La columna `beta` es la del **modelo**: 0.5 **por
construcción**. No es evidencia; es lo que el PIC debe refutar o no.

## §4 Numérica declarada

- `dx = lambda_L/40 = 2.0×10⁻⁸ m` · `CFL = 0.9` · `dt = 6.00415×10⁻¹⁷ s`
- caja `12 lambda_L` por lado · `n_pasos = 866` · diagnóstico cada 20 pasos
- unidades del motor: naturales `hbar = c = 1`, `m_e = 1`; la tabla va en SI
- derivados: `omega = 2.354564459×10¹⁵ rad/s`, `T = 2.66851 fs` (7.495 ciclos en `tau`)

## §5 Controles obligatorios (sin ellos el verde no vale)

1. **Onda plana sola ⇒ `a ≡ 0`.** Lemma 1 del paper: una sola onda plana tiene
   `F = G = 0`, luego `a² = b² = 0`. Es un control de **extremo conocido**.
2. **Desajuste `DeltaL = lambda_L/2` ⇒ el escalado se rompe.** Control del nulo:
   sin él, un `beta ≈ 0.5` podría venir de la energía, no de la coherencia.
3. **Polarización.** Lineal (`eq:lin_inv`): `F` cambia de signo y `G ≡ 0`.
   Circular co-rotante (`eq:cp_inv`): `F` y `G` quietos en `omega t` (quiescencia).
4. **Energía total conservada** dentro de la tolerancia que el motor declare.

Un control de cada punta: el caso conocido-cero (1) y el caso conocido-roto (2).

## §6 Dos etapas, y por qué

**Etapa 1 (la que decide el protocolo): clásica.** Del PIC se mide `a_tot(N)` y el
tiempo por encima del umbral, a partir de `E` y `B` simulados. Todo lo que juzga
`sim/falsador.py` sale de aquí.

**Etapa 2 (offline, sobre los campos de la Etapa 1):** se integra la tasa de
Schwinger `w(E) = ((eE)²/4π³) Σ (1/n²) exp(−nπ m²/eE)` sobre los campos guardados.
Es exactamente lo que la §Discussion del paper prescribe: la tasa se integra
**después**, no dentro del solver.

## §7 Honestidad de alcance (medida, no supuesta)

`python3 -B sim/params.py` a `2026-10-11T00:04:49Z`:

- `E_cr = 1.32329×10¹⁸ V/m` · `a0_cr = 329719` · `I_cr = 4.64811×10²⁹ W/cm²`
- a `a0 = 1`: `E0 = 4.01338×10¹² V/m`, `I = 4.27552×10¹⁸ W/cm²`
- órdenes entre `I_cr` y el techo técnico de referencia (`10²³ W/cm²`): **6.667**

⇒ **El Schwinger directo no es alcanzable y este protocolo no lo promete.** La
serie corre con `a0` de `170` a `682`, i.e. `a0 >> 1` (relativista, Etapa 1
clásica) y `a0/a0_cr` entre `5.17×10⁻⁴` (N=1) y `2.07×10⁻³` (N=16) — cociente de
las dos cifras impresas arriba (`170.534/329719`, `682.135/329719`), a tres-cuatro
órdenes del par. El escalado `1/N` es una afirmación **clásica** de los campos; la
Etapa 2 la traduce a rendimiento.

## §8 Qué se reporta

Se reporta, con hora y `sha16` de `main.tex` citado:

- `beta` medida, su banda, y la tabla `N → a_medido` con el archivo de campos usado;
- el resultado de los cuatro controles de §5;
- si un control falla, **se reporta el control**, no el escalado;
- si no hay medición: **SIN MEDIDA** (exit 2). Ni verde ni rojo: no hay objeto.

## §9 Qué NO es este protocolo

- NO es un conjunto de namelists listos para correr. `sim/configs.json` trae una
  tabla agnóstica de motor y un **mapeo declarado** de nombres de clave
  (`MAPPING`). Un namelist "listo" que nadie corrió sería una cifra sin comando.
- NO toca `main.tex` (otra mano lo escribe) ni reescribe sus fórmulas.
- NO promete Schwinger observable: eso está medido en §7.
