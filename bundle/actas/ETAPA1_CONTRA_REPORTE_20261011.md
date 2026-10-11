# ETAPA 1 · GEOMETRÍA CONTRA-PROPAGANTE (`eq:cp_inv`) — reporte

- instrumento: `sim/maxwell2d.py` sha16 = **1db75ea7b0b8cba4** (sin editar desde el commit b88c5d6)
- gate: `sim/falsador.py` sha16 = **f04551c7f19ce73a** (sin editar; copiado al sandbox bit a bit)
- horas: orden 1 → `01:50:01Z` (corridas `01:50:05` / `:10` / `:15` / `:20Z`) · orden 2 → `01:50:45Z` (corrida `01:50:50Z`)
  · extras declaradas → `01:51:50Z` y `01:52:41Z` · falsador → `01:57:08Z`
- escribe: `sim/etapa1_contra.json` (9292 B, T_UTC raíz `2026-10-11T01:50:20Z`).
- NO toca `sim/medidas_aN.csv` (entregable sellado de la etapa 1: 1360 B, Oct 10 19:15 local, sha256 prefijo `4129d436e2cd081d`,
  verificado antes y después). Los crudos quedan en `/tmp/serie_contra_out.txt`, `/tmp/serie_contra_nulo_out.txt`,
  `/tmp/sonda_contra_n4_out.txt`.

## UNIVERSO DECLARADO (verbatim del instrumento)

    malla xy 480x480 = 12 lambda_L por lado, dx = lambda_L/40; transito fisico = 19.485 lambda_L
    (los 866 pasos pre-registrados a CFL 0.9) = 1113 pasos a CFL 0.7; diagnostico cada 20 pasos
    (PROTOCOLO_1overN.md 4); CFL de 2D = 0.7 [CORREGIDO del 0.9 pre-registrado: limite de von Neumann
    en 2D = 1/sqrt(2) = 0.7071]; vacio clasico, SI 2019 (CODATA 2018) via sim/params.py; motor numpy;
    unidad de conteo = celda; VENTANA DE MEDIDA = celdas [100,380] (excluye la linea de inyeccion, que
    no es objeto de Maxwell: ahi cB/|E| = 0.514 y |E| = 6.9x lo prescrito, medido)

## 1. Qué se corrió

| # | comando | RC | escribe |
|---|---|---|---|
| 1 | `python3 -B sim/maxwell2d.py --serie-contra` | 0 | `sim/etapa1_contra.json` (4 filas) |
| 2 | `python3 -B sim/maxwell2d.py --serie-contra-nulo` | 0 | nada (sólo stdout: N=4, brazo derecho λ/2 = 20 celdas) |
| 3 | `python3 -B sim/maxwell2d.py --modo contra --n 4 --sonda` (EXTRA declarada) | 0 | nada (tabla axial del eje) |
| 4 | `correr(modo='contra', n=4, desplaza_dcha=20, sonda=True)` desde `python3 -c` (EXTRA declarada) | — | nada |

El modo `contra` reparte N/2 haces en `I_SL = 80` y N/2 en `I_SR = 400`, cada uno con `a_beam = a_ref/sqrt(N)`;
`terminos_de` devuelve `izq + der`. **N = 1 no existe** en esta geometría (`raise ValueError: el modo contra necesita N par`);
la serie recorre N ∈ {2, 4, 8, 16} ⇒ tres puntos de pendiente, no cuatro.

## 2. Serie contra: β y la forma del campo

| N | a_medido | a_foco | cB/\|E\|\_pico | F/(ε₀E²/2)\_pico | a_inv/\|E\|\_pico | celda del pico | t_max |
|---|---|---|---|---|---|---|---|
| 2 | 78.997346 | 37.658422 | 0.3944 | +0.8444 | 0.9921 | (232,240) = −0.200 λ | 20.45 fs |
| 4 | 111.719118 | 53.257052 | 0.3944 | +0.8444 | 0.9921 | (232,240) = −0.200 λ | 20.45 fs |
| 8 | 157.994691 | 75.316845 | 0.3944 | +0.8444 | 0.9921 | (232,240) = −0.200 λ | 20.45 fs |
| 16 | 223.438235 | 106.514103 | 0.3944 | +0.8444 | 0.9921 | (232,240) = −0.200 λ | 20.45 fs |

- cocientes contra N=2: **1 / 1.41422 / 2.00000 / 2.82843** = 1, √2, 2, 2√2
- **β = 0.500000** (impreso por el instrumento; banda pre-registrada [0.45, 0.55])
- constantes independientes de N: `a_foco/a_medido = 0.4767` · `residuo del absorbedor = 1.850e-03` ·
  `caja/ventana = 10.56` (a_medido_caja = 834.394 / 1180.01 / 1668.79 / 2360.02 — ARTEFACTO de la línea de inyección, ya declarado)
- factor geométrico contra/colineal, **idéntico en los cuatro N**: 78.997346/113.111252 =
  111.719118/159.963467 = 157.994691/226.222505 = 223.438235/319.926934 = **0.698398**
  ⇒ η_contra = 0.32755 contra η_colineal = 0.469008. La constante 0.698398 se mide; su descomposición
  (1/√2 × 0.987675) se declara **conjetura, no adjudicada**.
- Las cifras colineales de contraste salen del reporte sellado: `sim/ETAPA1_REPORTE_20261011.md` ll. 24 (79.981733620),
  28 (319.926934480), 44 (`cB/|E| = 0.9458`), 107 (eta = 0.469008), respaldadas con `grep` a `01:57:44Z`.

**Lectura (la misma que el dueño ratificó para colineal):** β = 0.500000 es **identidad de superposición**
(`a_beam ∝ N^(−1/2)` + solver lineal ⇒ `a ∝ N^(+1/2)`), **no** evidencia de física de pares. Ahora hay algo más:
la geometría contra **sí enciende los invariantes** (F pasa de +0.1055 colineal a +0.8444 contra, 8×; `cB/|E|`
de 0.9458 a 0.3944) y **β no se mueve en la última cifra** ⇒ β **mide la linealidad del solver, no la presencia
del invariante**.

## 3. Invariantes locales: sonda del eje en el instante del pico del foco (N=4, `--sonda`)

| i | x−λ | \|E\| s/desfase (V/m) | cB/\|E\| s/desfase | \|E\| con λ/2 (V/m) | cB/\|E\| con λ/2 |
|---|---|---|---|---|---|
| 80 | −4.000 | 4.51105e+13 | 0.023 | 4.48877e+13 | 0.018 |
| 100 | −3.500 | 5.5227e+12 | 0.622 | 4.24508e+12 | 0.236 |
| 120 | −3.000 | 4.30624e+12 | 7.106 | 1.94823e+13 | 0.603 |
| 160 | −2.000 | 3.53177e+13 | 4.675 | 1.25813e+14 | 0.542 |
| 200 | −1.000 | 1.59836e+14 | 2.296 | 3.47755e+14 | 0.483 |
| **240** | **0.000** | **2.13741e+14** | **1.982** | **4.26245e+14** | **0.445** |
| 280 | +1.000 | 1.61738e+14 | 1.983 | 3.36938e+14 | 0.407 |
| 320 | +2.000 | 7.77895e+13 | 2.031 | 1.84692e+14 | 0.360 |
| 400 | +4.000 | 4.15577e+13 | 0.008 | 6.80137e+11 | 1.067 |

(Las dos columnas se toman en instantes distintos: pico del foco a 20.92 fs sin desfase y a 21.01 fs con λ/2.
Las razones con |E| muy chico — i=100, 120 — están mal condicionadas: declárense como ratio de dos números chicos.)

- **El antinodo puramente eléctrico NO se observa en el foco en la configuración sin desfase:** `cB/|E| = 1.982`
  (|B| ≈ 2|E|/c: nodo de E, B sumando). Se reporta medido, no se maquilla.
- **Sí aparece con el desfase λ/2:** `cB/|E| = 0.445` en el foco y ~0.36–0.48 en ±2λ. Y **no llega a 0**: el
  antinodo es **parcial** (B cancela ~55 %), coherente con que las dos alas no llegan al foco con amplitud idéntica.
- `a_inv/|E|_pico` ≈ 0.99 en los dos casos (el máximo de `a` en la ventana cae donde el campo es casi puramente
  eléctrico); no es el foco.

## 4. El nulo λ/2: poder de discriminación medido

| observable | contra N=4 | con λ/2 en el ala derecha | Δ |
|---|---|---|---|
| a_medido | 111.719118 | 109.933787 | **−1.60 %** |
| a_medido_caja | 1180.01 | 1179.98 | −0.003 % |
| cB/\|E\|\_pico | 0.3944 | 0.3878 | −1.7 % |
| F/(ε₀E²/2)\_pico | +0.8444 | +0.8496 | +0.6 % |
| **a_foco** | **53.257052** | **106.206** | **+99.4 %** |
| **celda del pico** | **232 (−0.200 λ)** | **242 (+0.050 λ)** | **+10 celdas = +λ/4 exacto** |
| a_inv/\|E\|\_pico | 0.9921 | 0.9998 | +0.8 % |
| residuo del absorbedor | 1.850e-03 | 1.882e-03 | +1.7 % |

- **No hay cancelación nodal en el observable pre-registrado.** El motivo es estructural, no de resolución:
  para dos haces contra-propagantes, `max_x |A e^{ikx} + B e^{−ikx}| = A + B` **independiente de la fase relativa**
  ⇒ **`a_medido` es ciego al desfase por construcción**; el −1.60 % es el residuo de truncamiento/curvatura, no
  una cancelación. **Poder de discriminación del observable pre-registrado contra un desfase λ/2 = 1.6 %.**
- **El observable que sí discrimina es la celda local**: `a_foco` ×1.994 y el desplazamiento del patrón exactamente
  **+λ/4 = +10 celdas**, con el antinodo cayendo **sobre el foco** en el caso desplazado (`a_foco/a_medido` 0.4767 → 0.9661).
- **Identidad del instrumento (declarar para no contar dos veces):** `F/(ε₀E²/2) = 1 − (cB/|E|)²` — comprobado exacto
  en los tres casos: 1 − 0.3944² = 0.84443 · 1 − 0.3878² = 0.84961 · 1 − 0.9458² = 0.10546. Son **una medición con dos rótulos**,
  no dos hallazgos.

## 5. El falsador sobre la partición contra (sandbox `/tmp/audit_contra_0153/`, `01:57:08Z`)

`sim/falsador.py` copiado bit a bit (sha16 copia = origen = `f04551c7f19ce73a`) + `configs.json`; el CSV del sandbox
lleva en cabecera que **no es** el sellado de la etapa 1 (que quedó intacto, `4129d436e2cd081d`).

- `beta = 0.500000` — **dentro** de la banda pre-registrada [0.45, 0.55]
- `VEREDICTO: ROJO -- 1 fallo(s): sin N=1 no se puede medir el cociente contra sqrt(N)` · **RC = 1**
- control del sandbox: `--sintetico 0.5` → `VEREDICTO: VERDE` · **RC = 0** (el sandbox funciona)

**El ROJO es del metro, no del objeto:** el único fallo es el **ancla N=1**, que en la geometría contra **no existe**
(N par obligatorio). El gate no puede decir VERDE sobre contra por diseño de su ancla ⇒ **no es reutilizable entre
geometrías sin re-declarar el ancla**. La forma pre-registrada con el ancla declarada en N=2 da desviación 0.0000 en
los tres N, pero se imprime como **EXTRA**, no como veredicto (cambiar el ancla después de ver la medición es el defecto
que el propio protocolo prohíbe).

## 6. La esponja en la columna desplazada (declarar, no adjudicar)

La máscara es un **producto de las dos rampas** (x e y). Mi primera lectura (`m[i,0]`) mezclaba la rampa en y; la rampa en x
sobre el eje (j = 240) es:

| i | 80 | 400 | 419 | **420** | 440 | 479 |
|---|---|---|---|---|---|---|
| rampa_x | 1.00000000 | 1.00000000 | 1.00000000 | **0.99997222** | 0.98775000 | 0.90000000 |

⇒ en la columna 420 (donde queda la fuente derecha con λ/2) el amortiguado es **2.78e-5 por paso**, no 0.1; la región
amortiguada de verdad es `[419, 479]` pero con rampa cuadrática. El máximo de caja **no se movió**:
4.73583e+15 → 4.73571e+15 (razón 1.00003). Se declara como limitación cuantificada del nulo, **sin adjudicarle** el −1.60 %.

## 7. ALCANCE — qué NO prueba esto

1. **No refuta ni confirma Schwinger.** El solver es lineal: ninguna identidad de superposición puede fallar aquí.
2. **β = 0.500000 en las dos geometrías** ⇒ β mide el solver, no la física del par. La orden se cumple (β e invariantes
   locales registrados), pero β no es observable de pares.
3. `F > 0` y `a_inv/|E| ≈ 1` **no** son evidencia de creación de pares: son la forma del campo clásico de dos alas
   contra-propagantes. Lo que sí queda medido es **que la geometría contra enciende el invariante** (F: 0.1055 → 0.8444)
   **y β no se mueve**: separación limpia entre lo que el instrumento mide y lo que el modelo predice.
4. El **antinodo puramente eléctrico** (B = 0) no se alcanza: mínimo medido `cB/|E| = 0.445` (cancelación parcial de B).

## 8. Frontera

- Escrito: `sim/etapa1_contra.json` (instrumento) + este reporte. Nada más dentro de `sim/`.
- No tocados por esta mano: `sim/medidas_aN.csv` (sha256 `4129d436e2cd081d…`, verificado antes y después), `refs.bib`,
  `figures/`, `lint_tex.py`, `ZENODO_*`, el tarball.
- **Otra mano trabaja en el mismo repo a `01:57:44Z`:** `git status` muestra `M main.tex`, `M main.pdf` y sin seguimiento
  `sim/AUDITORIA_DE_LA_ORDEN_FDTD_Y_ORDEN_CORREGIDA_20261011.md`, `sim/PREREGISTRO_SIGMA_PHI_20261011.md`,
  `sim/ENTREGA_A_LA_PESTANA_VECINA_SIGMA_PHI_20261011.md`, `sim/barrido_sigma_phi.py`, `sim/field_solver.py`,
  `sim/runner_2d3v.py`, `sim/medidas_aN_circular.csv`, `sim/data/`. Se **declara, no se adjudica**: el commit de esta mano
  toca **sólo** sus dos archivos (`sim/etapa1_contra.json` y este reporte).
- Sandbox: `/tmp/audit_contra_0153/` (fuera del repo).
- Pendiente declarado, no corrido: `--serie-nulo` colineal (no ordenado).
