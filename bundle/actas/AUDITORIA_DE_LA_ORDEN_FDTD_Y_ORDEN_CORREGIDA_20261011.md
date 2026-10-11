# AUDITORÍA DE LA ORDEN AL FDTD + ORDEN CORREGIDA

**medida** 2026-10-11T01:21Z–01:24Z (UTC). Cada cifra de aquí lleva su hora o el sha16 de la pieza que midió. Nada está estimado.

**UNIVERSO DECLARADO**: `/Users/marlene/sfqed-paper` — `main.tex` · `sim/runner_2d3v.py` (22 048 B, sha16 `368627d18d83d253`, mtime `01:09:37Z`) · `sim/falsador.py` (5 160 B, sha16 `f04551c7f19ce73a`, **no editado**) · `sim/medidas_aN.csv` (1 360 B, `4129d436e2cd081d`, cabecera `generado: 2026-10-11T01:15:44Z`) · `sim/medidas_aN_circular.csv` (672 B, `ee5539f3f9efa96d`, cabecera `hora = 2026-10-11T01:11:39Z`) · `sim/data/sigma_phi/` (27 fichas; `resumen.csv` `b3d2a08a74f5b736`, `resumen.txt` `2da318358eefb797`) · `sim/PREREGISTRO_SIGMA_PHI_20261011.md` (4 253 B, `51d6a0d06c802244`).
**MOTOR**: `git --no-pager` · `grep -nE` · `python3 -B`. **UNIDAD**: fila `N,a` y línea de archivo. **VENTANA**: las horas UTC citadas.

**AVISO**: el universo se movió durante la auditoría (§E). Las cifras de §D son de `01:21–01:23Z` y llevan el sha16 de lo que midieron.

---

## §A. Los pedidos de la orden, contra lo que existe

| # | la orden pide | estado medido |
|---|---|---|
| A1 | inyectar el vector de fases por `--fases` de `runner_2d3v.py` | **la bandera no existe** (§B): hay que **escribirla**, no invocarla |
| A2 | correr el ensayo empírico real en el FDTD | **ya hay dos corridas**: `circular` (cabecera `01:11:39Z`) y `lineal` (cabecera `01:15:44Z`) (§D) |
| A3 | aislar el desfase conocido de la celda N=1 | **correcto, y ya está medido**: en la circular toda la desviación vive en N=1 (§D) |
| A4 | escribir a archivo por polarización, no al canónico | **correcto y ya en práctica**: existe `medidas_aN_circular.csv` |
| A5 | declarar la polarización explícitamente | **correcto, y es un hueco mío** (§F) |

---

## §B. H1 — `--fases` no existe en el runner vivo

- `grep -cE 'fases|FASES' sim/runner_2d3v.py` = **0**; `grep -nE -- '--fase' …` = **0 líneas**.
- CLI completo (l.418–424), **7 banderas**: `--modo` (default `barrido`; choices `barrido, control1, control4`), `--n`, `--todo`, `--pol` (default **`linear`**; choices `linear, circular`), `--dl`, `--pasos`, `--json`.
- La fase **sí** existe dentro del código: `def bloque(Xc, Yc, th0, am0, pol, fase, comps)` (l.132), `cf, sf = math.cos(fase), math.sin(fase)` (l.140), `Cq = Cp*cf − Sp*sf` (l.151), `Sq = Sp*cf + Cp*sf` (l.152). **Único llamador**: l.211, con la fase calculada en l.207 = `−2π·dl_lambda` si `dl != 0`, y `0.0` si no.

⇒ Dos hechos: (i) `--dl` da **una** fase determinista al **último** haz, no un vector iid; (ii) el parámetro `fase` de `bloque(...)` es el sitio correcto para inyectarlo. La orden debe pedir **escribir la bandera**, no invocarla: nombra un dato que no existe.

---

## §C. H2 — la lectura del FDTD es un MÁXIMO: ese objeto es PICO, no FOCO

Declarado por el propio crudo de la pestaña vecina (cabecera de `sim/medidas_aN_circular.csv`, l.1 y l.3): `a_medido = (e/(m_e c omega)) * max_(r en Omega_foco, t) |E(r,t)|` — *"medicion = max de |E| sobre el disco |r| <= w0 y sobre la ventana CAUSAL de pasos"*.

Un máximo discreto sobre el disco es el **PICO** (`a_beam·(|P|+|M|)`), no el fasor `|P+M|` (**FOCO**, la lectura juzgada en el sello). Medido sobre mi tabla sellada:

| lectura | cruce β = 0.45 | fuente |
|---|---|---|
| FOCO, bisección exacta (pre-registrada) | **0.554987 rad = 0.2357 fs** | `resumen.txt` l.27 |
| FOCO, interpolado en la rejilla de 12 σ | 0.551609 (teoría) / 0.551759 (medido) | `resumen.txt` l.28–30 |
| **PICO**, interpolado en la misma rejilla | **0.527493 rad = 0.2240 fs** | columnas `beta_pico` de `resumen.csv`: σ=0.500 → 0.455467 ; σ=0.625 → 0.430611 |

**El cambio de objeto mueve el cruce 0.027494 rad = 4.95 % de σ\* = 0.554987** (y **4.40 %** si el denominador es el cruce FOCO interpolado, 0.551761: 0.024268 rad). Los dos denominadores se declaran porque dan dos números distintos.

A σ = 0 las dos lecturas **coinciden exactamente** (`foco_sigma_000.csv` y `pico_sigma_000.csv`, fila N=16 = 682.1352093 las dos) ⇒ la corrida circular de ellos (σ = 0) reproduce ambas por igual, y **el desdoblamiento solo aparece al encender σ > 0**, que es justo donde va la orden.

Intervalo sellado por σ a N = 16 (fichas `foco_sigma_*.csv` / `pico_sigma_*.csv`, fila `16,`), con la razón PICO/FOCO:

| σ | FOCO | PICO | PICO/FOCO |
|---|---|---|---|
| 0.0 | 682.1352093 | 682.1352093 | 1.000000 |
| 0.5 | 607.3271497 | 611.9268304 | 1.007574 |
| 1.0 | 435.5044546 | 450.5297418 | 1.034501 |
| 3.0 | 170.8957744 | 228.9339199 | 1.339611 |

Auto-auditoría del sello: **0 violaciones de PICO ≥ FOCO en las 60 parejas (σ, N)** (el teorema `|P|+|M| ≥ |P+M|` del pre-registro, comprobado ficha por ficha).

---

## §D. H3 — el desfase vive en UNA fila, y ya está medido

Motor: `sim/falsador.py` **tal cual** (sha16 `f04551c7f19ce73a`), sobre **copias sandbox** en `/tmp` (`/tmp/audit_circ_0122`, `/tmp/audit_lin_0123`), sin tocar un byte de la pestaña vecina.

| crudo | sha16 | hora de cabecera | β | `desv` por N | RC |
|---|---|---|---|---|---|
| `sim/medidas_aN.csv` (canónico, lineal) | `4129d436e2cd081d` | 01:15:44Z | **0.500000** | 0.0000 en las 5 | 0 VERDE |
| `sim/medidas_aN_circular.csv` | `ee5539f3f9efa96d` | 01:11:39Z | **0.486414** | **0.0460 idéntico** en N=2,4,8,16 | 0 VERDE |
| el mismo, **solo la fila N=1** movida a `170.5338023` | — | — | **0.499999** | 0.0000 en las 5 | 0 VERDE |

Descomposición fila por fila de la circular, `a_medido/(a(1)·√N)`: **0.9540012 · 0.9540012 · 0.9540037 · 0.9540039** para N = 2, 4, 8, 16 ⇒ las cuatro filas N ≥ 2 son **exactamente** proporcionales a √N (`|desv| = 0.0460` idéntico), y la de N = 1 está **+4.82 %** (178.7553300762 vs `a_ref` = 170.5338023).

Contra el álgebra sellada σ = 0 (`resumen.csv`, columnas `a_1/a_2/a_4/a_8/a_16`); `ratio` = medido/álgebra, `rel` = `ratio − 1`:

| N | álgebra σ=0 | FDTD circular | ratio | rel | FDTD lineal | rel |
|---|---|---|---|---|---|---|
| 1 | 170.5338023 | 178.7553300762 | 1.048211 | +4.821e−02 | 79.98173362 | −5.30992e−01 |
| 2 | 241.1712161 | 241.1697981457 | 0.99999412 | −5.88e−06 | 113.1112524 | −5.30992e−01 |
| 4 | 341.0676047 | 341.0655993725 | 0.99999412 | −5.88e−06 | 159.9634672 | −5.30992e−01 |
| 8 | 482.3424322 | 482.3408425826 | 0.99999670 | −3.30e−06 | 226.2225049 | −5.30992e−01 |
| 16 | 682.1352093 | 682.1331202323 | 0.99999694 | −3.06e−06 | 319.9269345 | −5.30992e−01 |

Tres lecturas que la orden necesita:

1. **El escalado lo mide la malla**, con 5–6 dígitos, con código ajeno y en las dos polarizaciones (N ≥ 2). Lo que falla es **la escala absoluta de una fila**.
2. La corrida **lineal** tiene el factor **η = 0.469008 uniforme en las cinco filas** (su propia cabecera lo declara: `eta = a_medido(1)/a_tot_pred(1) = 0.469008`) ⇒ el falsador lo cancela y β = 0.500000. La **circular** tiene ratio ≈ 0.99999 en las cuatro filas N ≥ 2 y **+4.82 %** en N = 1 ⇒ β = 0.486414.
3. **La banda pre-registrada [0.45, 0.55] no distingue estas dos corridas**: 0.500000 y 0.486414 caen las dos dentro. La banda juzga el escalado; **la escala absoluta viaja aparte** y aquí es la que cambia.

**Corrección de una cifra mía, declarada**: la versión anterior del canónico (670 B, sha16 `62824875f8739c79`, cabecera `00:49:51Z`) daba **β = 0.487693** con `desv` 0.0418 plano. **Esa cifra describe un archivo que ya no existe**: el vivo (1 360 B, `01:15:44Z`) da 0.500000 con `desv` 0.0000. El mecanismo «toda la desviación en una celda» sigue en pie, pero **su testigo cambió de archivo** y hay que citarlo con la versión.

---

## §E. H4 — el universo se movió (declarado, no adjudicado)

| pieza | antes | ahora | hora |
|---|---|---|---|
| `main.tex` | 22 367 B · `4299786a34bdb313` | **23 042 B · `44a3f0b33ad6593e`** · `git status` = ` M` · 21 inserciones / 11 borrados | 01:15:36Z |
| `main.pdf` | 146 773 B | 148 077 B · `0cb36a4f7c5f22d7` | 01:15:42Z |
| `sim/runner_2d3v.py` | 20 770 B | **22 048 B · `368627d18d83d253`** | 01:09:37Z |
| `sim/medidas_aN.csv` | 670 B | **1 360 B · `4129d436e2cd081d`** | 01:15:44Z |
| `sim/medidas_aN_circular.csv` | no existía | **672 B · `ee5539f3f9efa96d`** | 01:11:39Z |

Los tres cambios de `main.tex` (verbatim por `git --no-pager diff -U1 main.tex`; aquí las fórmulas van **elididas y marcadas** con corchetes, para que no viaje una cita a medias):

- **(a)** el nulo de Lemma 1 pasa a: *"For a field transverse to a single propagation direction, an arbitrarily intense \emph{single} pulse therefore creates no pairs from the vacuum, and pair creation requires at least two fields whose wave vectors are not parallel. The null is exact for a plane wave and holds for a paraxial beam; it fails at the focus of a tightly focused pulse, where [nabla·E = 0] forces a longitudinal component [E_z ~ E_perp/(k w_0)] and the time-averaged invariant acquires a term of relative order [(k w_0)^(−2)]. The results below are stated for transversality-preserving fields."*
- **(b)** *"This is the analytic core of the geometric route…"* → *"The algebra here is that of coherent addition and is elementary; what the proposition establishes is that the linear-in-N reduction of the threshold energy follows from vacuum superposition alone, with no further assumption about the interaction."*
- **(c)** el párrafo de LUXE pasa a decir que sus configuraciones son *"of two beams, not of the optimised N-beam geometry — so that they constrain the strong-field framework and the two-beam invariants [eq:lin_inv–eq:cp_inv], rather than the energy scaling of [eq:oneoverN]"*.

**No es mi edición y no la adjudico.** Consecuencia operativa: mi nota de entrega §2 (l.16) cita `main.tex` «congelado · sha16 `4299786a34bdb313` · 22 367 B · sin tocar» ⇒ **esa fila quedó vieja**; la que vale es la de esta tabla, con su hora.

---

## §F. Hueco propio (declarado): mi pre-registro no declara la polarización

`grep -nE 'circular|linear|pol' sim/PREREGISTRO_SIGMA_PHI_20261011.md` = **0 líneas**, mientras el runner tiene `--pol` con default **`linear`** (l.421) y ya existe una corrida **`circular`** viva. La exigencia de declarar polarización que trae la orden es **correcta**; el hueco es mío, no de la orden, y el remedio es que la pestaña vecina lo declare **en su propio pre-registro, antes de correr** (anotarlo después no cuenta: elegir el parámetro con la salida a la vista es el defecto).

---

## §G. ORDEN CORREGIDA (texto listo para pegar)

> **Orden a la pestaña FDTD — barrido estocástico de σ_φ (`eq:cp_inv`, coaxial contra-propagante).**
>
> 1. **Pre-registro primero, archivo propio, antes de la primera cifra.** Debe declarar: la polarización (`--pol circular` o `linear`, no el default por omisión); la geometría `coaxial contra-propagante` (`eq:cp_inv`); `a_beam = a_ref/√N`; la σ de cada corrida; el número de realizaciones y la semilla; y **qué objeto mide** (ver 4).
> 2. **La bandera `--fases` NO existe hoy en `runner_2d3v.py`** (22 048 B, `368627d18d83d253`): hay que **escribirla**. El sitio correcto es el parámetro `fase` de `bloque(...)` (l.132; `cf, sf = cos, sin` en l.140; la rotación en l.151–152), que hoy recibe del único llamador (l.211) la fase de l.207 = `−2π·dl_lambda` para **el último** haz, o `0.0`. Se necesita **un vector de N fases iid U(0, 2π)**, una por haz, con semilla declarada. Si se reusa `--dl`, hay que decir que es otra cosa: una fase determinista en un haz.
> 3. **Salida a archivo propio por polarización**, p. ej. `sim/medidas_aN_sigma_<pol>_<σ>.csv`, con la cabecera `#` completa (hora, sha16 del pre-registro, UNIDAD declarada, y **qué se mide**). **Nunca** escribir al canónico `sim/medidas_aN.csv`.
> 4. **El objeto juzgado es el que la cabecera diga, y el cruce se reporta contra SU objeto.** Un máximo sobre el disco `|r| ≤ w0` es el objeto **PICO**; su cruce sellado de β = 0.45 es **0.527493 rad = 0.2240 fs**. La lectura **FOCO** (`|P+M|`, la juzgada en el sello) cruza en **0.554987 rad = 0.2357 fs**. Citar 0.554987 para una lectura de máximo instala un adelanto de **4.95 % de σ\*** (o 4.40 % si el denominador es 0.551761) **por construcción, no por física**. Si se quiere comparar con FOCO, hay que extraer del retículo la lectura de suma coherente —no el máximo— y decirlo.
> 5. **Ancla de malla con el umbral ya sellado, aplicada a las 12 σ** (mi control K2, sin inventar umbral nuevo): para cada (σ, N), `a_medido ≤ PICO(σ,N)·(1+1e−9)` (cota exacta `|E| ≤ |P|+|M|`) y `a_medido ≥ 0.90·PICO(σ,N)` (el 0.90 está declarado porque el paso de nodo es 0.1 λ_L = 36°). Los dos extremos se leen de `sim/data/sigma_phi/pico_sigma_<σ>.csv`, columna `N,a_medido`, con σ en el nombre sin punto (`000, 125, 250, 375, 500, 625, 750, 1000, 1250, 1500, 2000, 3000`). A N = 16: σ=0 → [682.1352093, 682.1352093]; σ=0.5 → [607.3271497, 611.9268304]; σ=1.0 → [435.5044546, 450.5297418]; σ=3.0 → [170.8957744, 228.9339199].
> 6. **La fila N = 1 va aparte, declarada como propiedad de ESE csv, no como ley.** Medido en el crudo circular de hoy: las cuatro filas N ≥ 2 dan `|a(N)/(a(1)√N) − 1| = 0.0460` idéntico (cociente 0.9540012 ⇒ son exactamente √N entre sí) y la de N = 1 está **+4.82 %**; corregida sólo esa fila, β pasa de **0.486414 → 0.499999** con `desv` 0.0000 en las cinco. En el crudo lineal no hay nada que aislar: las cinco filas son exactamente `a(1)·√N` (β = 0.500000, `desv` = 0.0000).
> 7. **Cierre con conteo, no con lectura.** El barrido son **12 σ × 5 N = 60 filas**: se cuentan. Control σ = 0 obligatorio: β debe dar **0.500000** en las dos polarizaciones (es el objeto donde FOCO y PICO coinciden, ya verificado a 5.9e−06 relativo en N ≥ 2). El veredicto del falsador se reporta con **su** RC y sin bajar umbrales: banda [0.45, 0.55] VERDE, muerte ≤ 0.35 o ≥ 0.65, `desv` por N tolerada a 0.20.
> 8. **El falsador no se edita.** Se corre tal cual (`sim/falsador.py`, sha16 `f04551c7f19ce73a`). Si aparece su RC = 2, hay que distinguir **las dos causas que hoy comparte** (no hay medición / no hay predicción) antes de citarlo.

---

## §H. Lo que queda en pie de la orden original, y lo que no se toca

- **En pie y bien**: escribir sólo a archivo por polarización; exigir la declaración de polarización; el FDTD como **ensayo empírico real** y el solver de fasores como **verificación de consistencia, no evidencia** (la propia cabecera de mi `resumen.csv` lo dice); el falsador como instrumento del veredicto.
- **No se toca**: `sim/medidas_aN.csv` (canónico), `sim/falsador.py`, `sim/runner_2d3v.py` (es de la pestaña vecina), las 27 fichas selladas, `sim/PROTOCOLO_1overN.md`, y **`main.tex`** (no es mío: su movimiento se declara, no se edita).
- **Sin cambios de umbral, sin linters nuevos, sin comparadores externos.** M sigue en el 4096 sellado.

---

## §I. CONFIRMACIÓN DEL DUEÑO (texto listo para pegar) — y las declaraciones que la hacen lícita

Medido `2026-10-11T02:01:43Z`–`02:02:33Z`. **Solo lectura** sobre `sim/`; nada de la pestaña vecina se escribió. Apéndice: esta pieza no se parchea, sólo recibe apéndices.

### §I.1. La confirmación, verbatim del dueño

> **Auditoría aceptada en su totalidad.**
> 1. Se adopta el umbral de **PICO (0.5275 rad ≈ 0.2240 fs)** como el benchmark legítimo para el operador supremo del FDTD.
> 2. Queda registrado que la serie circular reproduce β → 0.499999 para N ≥ 2, aislando definitivamente el sesgo en la normalización de N = 1.
> 3. Ejecuta la **orden corregida** tal como la redactaste en la sección final de `AUDITORIA_DE_LA_ORDEN_FDTD_Y_ORDEN_CORREGIDA_20261011.md`.

Con esto la pestaña FDTD corre el ensayo **bajo sus banderas reales** (`runner_2d3v.py --modo barrido --pol circular`; la bandera `--fases` hay que **escribirla**, §G.2) y contra el observable físicamente coherente. Mi lado no ejecuta nada: la orden es de ellos y la corre esto chat.

### §I.2. Tres declaraciones que la adopción exige (sin ellas el benchmark no es lícito)

**(a) El benchmark es la columna `beta_pico` — y mi propio artefacto declara esa columna «se reporta, NO se juzga».** Nombres de columna tomados de su escritor (`sim/barrido_sigma_phi.py`, 17 615 B, `9836b7d7df5ff0af`, l.196): `sigma, beta_mc, beta_teo, delta, tol, beta_4p, beta_pico, a(1), a(2), a(4), a(8), a(16)` = 12 columnas, **sin fila de encabezado** en el csv. Cruces de β = 0.45 por **posición** en `sim/data/sigma_phi/resumen.csv`:

| col | nombre | objeto | cruce (interpolado en la rejilla de 12 σ, **no** bisección) |
|---|---|---|---|
| 1 | `beta_mc` | lectura FOCO, medido | 0.551761 rad (entre σ=0.500 → 0.459365 y σ=0.625 → 0.436749) |
| 2 | `beta_teo` | lectura FOCO, teoría | 0.551609 rad |
| 5 | `beta_4p` | **regresión sin la fila N = 1** | 0.664079 rad (entre σ=0.625 → 0.457099 y σ=0.750 → 0.434392) |
| **6** | **`beta_pico`** | **la otra lectura del mismo campo, sin forma cerrada pre-registrada** | **0.527493 rad = 0.2240 fs** (entre σ=0.500 → 0.455467 y σ=0.625 → 0.430611) |

Bisección de la forma cerrada (pre-registrada): σ* = **0.554987 rad = 0.2357 fs**. Adelanto del benchmark PICO: **0.027494 rad = 4.95 % de σ\*** (4.40 % contra 0.551761 — los dos denominadores declarados). ⇒ **Adoptar PICO como objeto juzgado es promover a juzgada una columna que el pre-registro declara reportada**: es una enmienda, y aquí queda declarada. El acto es legítimo por una razón que **no** es conveniencia: **lo fuerza el operador** — un máximo sobre el disco `|r| ≤ w0` es estructuralmente PICO, no FOCO.

**(b) La polarización.** `sim/PREREGISTRO_SIGMA_PHI_20261011.md` (4 253 B, `51d6a0d06c802244`) tiene **cero líneas que declaren `circular` o `linear`**, y `runner_2d3v.py` trae **default `--pol linear`** (l.418–424). El ensayo se corre con `--pol circular` **declarado en el pre-registro**, o el crudo no dirá qué se midió.

**(c) La procedencia del número.** 0.527493 rad **no sale de una bisección**: sale de interpolar la rejilla de 12 σ entre 0.500 y 0.625 sobre `beta_pico`. Viaja con eso escrito.

### §I.3. Corrección de DOS cifras mías (append-only; las piezas viejas no se parchean)

**(i) Falso: el testigo del canónico viejo.** En esta misma pasada afirmé que `/tmp/audit_circ_0122/medidas_aN.csv` (669 B, sha256 `5a3a80ebca3278bf…`) era el testigo superviviente del canónico **lineal** viejo. **No lo es**: su cabecera dice `pol = circular` y `hora = 2026-10-11T01:11:39Z`, y sus filas son las del crudo circular con **la fila N = 1 sustituida por `170.5338023`** (3 bytes menos que el circular vivo de 672 B: 672 − 3 = 669). Sobre él, el falsador ajeno tal cual: **β = 0.499999, `desv` = 0.0000 en las cinco, VERDE**. Error de metro mío, del nombre de la carpeta (`audit_circ_…`) leído como objeto.

**(ii) 670 B · `62824875f8739c79` · β = 0.487693 · `desv` = 0.0418 — sin testigo vivo.** Los cuatro variantes medibles hoy dan: `/tmp/falsador_e1/medidas_aN.csv` (1 246 B, `2257e4ccf8f8bfab`) → β = 0.500000, VERDE · `/tmp/corr_n1_005544/medidas_aN.csv` (71 B, `83e38b92f55166f8`) → β = 0.500004, VERDE · canónico vivo (1 360 B, `4129d436e2cd081d`) → β = 0.500000, `desv` 0.0000 ×5, VERDE · circular vivo (672 B, `ee5539f3f9efa96d`) → β = 0.486414, `desv` 0.0460 ×4, VERDE. **Ninguno reproduce 0.487693.** La cifra queda **declarada como medida en su hora (`00:49:51Z`) y superada** — el archivo fue reescrito por otra mano a `01:15:44Z` — y **no viaja** como estado del árbol de hoy.

**El punto 2 del dueño, verificado y cuantizado con comando:**
- circular vivo (672 B), **restringido a N ≥ 2** (4 filas): **β = 0.500002** (fórmula loglog del falsador ajeno, l.62–72).
- la fila N = 1 del circular vivo vale **178.7553300762** contra `a_ref = 170.5338023` ⇒ **+4.821 %**; sustituida por `a_ref`, β → **0.499999**, `desv` 0.0000 ×5, VERDE.
- la columna `beta_4p` de mi propio `resumen.csv` (misma regresión **sin** la fila N = 1) mueve su cruce de 0.551761 → **0.664079 rad**: el mismo sesgo, medido por mi artefacto. **Es chequeo interno, no evidencia independiente** (mismas 4096 réplicas, el mismo campo).

### §I.4. Hallazgo nuevo: el vecino ya corrió la geometría real, con dos motores, y β = 0.500000 exacto

**(1) El instrumento y sus dos series.** `sim/maxwell2d.py` (30 759 B, `1db75ea7b0b8cba4`) tiene CLI a mano (**0** `add_argument`); `def serie(...)` escribe `sim/etapa1_<etiqueta>.json` (l.452). Medido hoy con la fórmula del falsador:

| artefacto | hora | N | a/√N | dispersión de a/√N | β |
|---|---|---|---|---|---|
| `sim/etapa1_colineal.json` (11 530 B, `33bcf93826ce494b`) | 01:15:44Z | 1, 2, 4, 8, 16 | **79.981733620** | 6.7e−16 | **0.500000000** |
| `sim/etapa1_contra.json` (9 292 B, `221a9fe8c3e269f4`) | 01:50:20Z | 2, 4, 8, 16 | **55.859558799** | 4.4e−16 | **0.500000000** |

**La ley √N es exacta a precisión de máquina en las dos geometrías**, y el cruce de motores cierra: mi suma de fasores (σ = 0, `a_ref`·√N = 170.533802·√N) y su FDTD contra-propagante (55.859559·√N) dan **el mismo exponente, 0.500000**, con **otra escala**: 55.859559/170.533802 = **0.327556**. **Se declara, no se adjudica** (familia del reparto circular/lineal y del desfase de un haz).

**(2) El reparto FOCO/PICO leído del crudo del vecino, en las dos geometrías.** Constantes **idénticas en todas las filas de cada serie** (dispersión 0):

| constante | colineal | contra |
|---|---|---|
| `F_rel_pico` (campo en el foco / campo máximo) | **0.1055143023** | **0.8444296302** |
| `pico_lambda_del_foco` | **−0.575** | **−0.2** |
| `a_inv_rel_al_pico` | 0.9995132754 | 0.992089925 |
| `cB/E` en el pico | 0.9457725401 | 0.3944240989 |

Dos consecuencias, y la segunda **acota** el hallazgo H2 del §C:
- **el máximo medido no está en el foco** en ninguna de las dos; en la co-propagante el campo del foco es sólo el **10.55 %** del máximo de la ventana (que cae a −0.575 λ del foco);
- **`F_rel_pico` no depende de N** ⇒ PICO = FOCO dividido por una constante ⇒ **la diferencia FOCO/PICO es una ESCALA, no un exponente** ⇒ **no puede mover β**; sólo mueve el **cruce de σ**. El peligro de citar 0.554987 para una lectura de máximo es real, pero está **confinado al cruce** (0.2240 fs contra 0.2357 fs), no a la ley de escalado.

**(3) El falsador ajeno sobre la serie contra: ROJO por construcción, no por física.** Corrido tal cual (jaula propia, `falsador.py` sin editar) sobre las 4 filas N = 2, 4, 8, 16: imprime **β = 0.500000** y luego **`VEREDICTO: ROJO`, RC = 1**, un solo fallo: «sin N=1 no se puede medir el cociente contra sqrt(N)». La geometría contra-propagante **no tiene N = 1** (una pareja necesita dos haces) ⇒ el fallo es del **anclaje del instrumento**, no del escalado. Se declara; **no se baja ningún umbral**.

**(4) Dos fronteras de nombre en el instrumento vecino.**
- `--serie-contra-nulo` (**l.694**) corre y **sólo imprime** (`print(json.dumps(...))`, l.710): **no escribe artefacto**. Si la orden corregida pide ese nulo, hay que darle archivo.
- en `maxwell2d.py` la palabra **`fases`** ya tiene casa: es el **perfil de curvatura del frente** (`fases[col]`, l.215 / 222 / 229 / 290 / 295–296 / 311), **no** fases aleatorias por haz. ⇒ la bandera `--fases` del §G.2 es de **`runner_2d3v.py`** y de nadie más: pedirla en `maxwell2d.py` sería pedir otro objeto con el mismo nombre.

### §I.5. Anclas para verificar antes de correr (nada se corre sin esto)

`runner_2d3v.py` 22 048 B · `368627d18d83d253` · `01:22:40Z` · **7** banderas · `fases|FASES` = **0** líneas · `--fase` = **0** · `--pol` default **`linear`** ‖ `maxwell2d.py` 30 759 B · `1db75ea7b0b8cba4` ‖ `falsador.py` 5 160 B · `f04551c7f19ce73a` · **no se edita** ‖ `PREREGISTRO_SIGMA_PHI_20261011.md` 4 253 B · `51d6a0d06c802244` ‖ esta auditoría **15 047 B · `96012083b5617a96` · 140 l · 8 × `## §`**, sin cambios (su mtime se movió a `01:49:54Z` con **bytes idénticos**: re-sello, no edición) ‖ `sim/data/sigma_phi/resumen.csv` `b3d2a08a74f5b736` · `resumen.txt` `2da318358eefb797`.

- **No se toca**: `main.tex` (su movimiento se declara, no se adjudica), los archivos de la pestaña vecina, las 27 fichas selladas, el canónico `sim/medidas_aN.csv`, `sim/PROTOCOLO_1overN.md`. **Sin umbrales nuevos, sin linters, sin comparadores externos; M sigue en 4096.**

---

## §II. PASO 1 — estado medido: la corrida circular ya existe, y sus dos prerequisitos siguen abiertos

`T_UTC = 2026-10-11T02:26:17Z` y `02:30:22Z`.
**UNIVERSO DECLARADO**: `sim/runner_2d3v.py` · `sim/maxwell2d.py` · `sim/falsador.py` · `sim/medidas_aN.csv` · `sim/medidas_aN_circular.csv` · `sim/PREREGISTRO_SIGMA_PHI_20261011.md` · `sim/data/sigma_phi/` · los `.md` de `sim/` y los dos `.md` nuevos de la raíz. **MOTOR** = `wc -c` / `shasum -a 256` / `grep -nE` / `sed -n` / `python3 -B` / `git`. **UNIDAD** = byte, línea, ocurrencia, bandera. **VENTANA** = los dos relojes UTC de arriba. **SOLO LECTURA**: en este tramo no se corrió ninguna simulación ni se editó ningún instrumento.

### §II.1. Cero deriva en instrumentos y crudos (contra la tabla del §I.5)

| ancla | §I.5 decía | medido `02:26Z` | veredicto |
|---|---|---|---|
| `sim/runner_2d3v.py` | 22 048 B · `368627d18d83d253` · 495 l · 7 banderas · `fases\|FASES` 0 · `01:22:40Z` | idéntico | **sin deriva** |
| `sim/maxwell2d.py` | 30 759 B · `1db75ea7b0b8cba4` · 715 l · `01:22:32Z` | idéntico | **sin deriva** |
| `sim/falsador.py` | 5 160 B · `f04551c7f19ce73a` · 145 l · `00:08:48Z` | idéntico | **sin deriva** |
| `sim/PREREGISTRO_SIGMA_PHI_20261011.md` | 4 253 B · `51d6a0d06c802244` · 73 l | idéntico · **0** líneas con `circular\|linear\|--pol` | **sin deriva** |
| `sim/medidas_aN.csv` | 1 360 B · `4129d436e2cd081d` · 18 l · `01:15:44Z` | idéntico | **sin deriva** |
| `sim/medidas_aN_circular.csv` | 672 B · `ee5539f3f9efa96d` · 9 l · `01:11:39Z` | idéntico | **sin deriva** |
| `resumen.csv` / `resumen.txt` | `b3d2a08a74f5b736` / `2da318358eefb797` | idénticos | **sin deriva** |

⇒ **lo que se movió no es el objeto: es prosa y sello.** La mano vecina commiteó `8e46865` (Adenda 1) y `6aa716a` (Adenda 2, 13 571 B, `02:25:09Z`); en la raíz aparecieron `README.md` (12 473 B · `9cd086f21a07559a` · 188 l) y `METHODOLOGY_AND_BOUNDARIES.md` (15 393 B · `90ac67a600799e98` · 274 l), los dos **sin rastrear** y **ajenos**; `main.tex` y `main.pdf` siguen en ` M`. Se declara, **no se adjudica**.

### §II.2. El objeto del Paso 1 ya estaba declarado por su propio instrumento — y es PICO

Cabecera de `sim/medidas_aN_circular.csv`, verbatim (9 líneas, leído entero):

- `a_medido = (e/(m_e c omega)) * max_(r en Omega_foco, t) |E(r,t)|`
- `medido con sim/runner_2d3v.py (FDTD Yee 2D3V, numpy, c = omega = k = 1)`
- `medicion = max de |E| sobre el disco |r| <= w0 y sobre la ventana CAUSAL de pasos`
- `pol = circular ; Omega_foco = |r| <= w0 ; N_LISTA = [1, 2, 4, 8, 16] ; hora = 2026-10-11T01:11:39Z`
- filas: `1,178.7553300762` · `2,241.1697981457` · `4,341.0655993725` · `8,482.3408425826` · `16,682.1331202323`

Dos consecuencias:

1. **el instrumento de la serie circular es `runner_2d3v.py`**, no `maxwell2d.py` (el canónico *lineal* sí es de `maxwell2d.py`) ⇒ el archivo donde vive el Paso 1 es el que trae la partición por polarización, no el propagador;
2. la cabecera declara **un máximo sobre el disco** ⇒ por la ley del §C ese objeto es **PICO**: su cruce es **0.527493 rad = 0.2240 fs** (columna 6 `beta_pico` de las 12 de `resumen.csv`, leída **por posición**, sin fila de cabecera; procedencia = **interpolación de rejilla**, no bisección) y **no** 0.554987, que adelantaría 0.027494 rad = **4.95 %** de σ* **por construcción**.

⇒ **no hay que corregirle el objeto: hay que leerlo con su propio cruce.**

### §II.3. Lo que el Paso 1 ya tiene, y los dos prerequisitos que siguen en `0 líneas`

**Ya hecho:** (a) la corrida determinista `--pol circular` **existe** (`01:11:39Z`); (b) §G.3 **ya está implementado** en el instrumento — `runner_2d3v.py` l.66–71 trae `CSV_NOMBRE = {"linear": "medidas_aN.csv", "circular": "medidas_aN_circular.csv"}` con la razón escrita («`--todo` sobrescribía `sim/medidas_aN.csv` en CADA corrida y borraba la trazabilidad del estado (una corrida circular pisó la serie lineal del 10-Oct)»), que es exactamente la partición que la orden pedía.

**Abierto, medido hoy:**

- **§G.1 (pre-registro)** — el único pre-registro que existe es **mío**, cubre el barrido de **fasores** y trae **0** líneas que declaren `circular`, `linear` o `--pol`. ⇒ **la corrida circular no tiene pre-registro que la cubra.**
- **§G.2 (`--fases`)** — `fases|FASES` = **0** líneas en las 495 del runner, `--fase` = **0**, 7 banderas. ⇒ **la parte estocástica (rejilla σ de 12 × 5 N = 60 filas) no tiene instrumento**: el barrido σ_φ existe hoy sólo del lado de fasores (`sim/data/sigma_phi/`, 27 fichas) ⇒ **el ensayo empírico independiente del FDTD todavía no se puede correr**.

### §II.4. La consecuencia que el orden obliga a escribir (no se puede reparar hacia atrás)

El pre-registro se sella **antes** de ver la salida. La serie circular **ya corrió** (`01:11:39Z`) y su pre-registro **no existe** ⇒ una declaración de polarización escrita **hoy** no sería un pre-registro: sería una **declaración de hecho**. Para que la corrida quede pre-registrada hay que **volver a correrla** con el pre-registro sellado antes. Y el re-corrido **no puede pisar el testigo citado**: `sim/medidas_aN_circular.csv` (`ee5539f3f9efa96d`) está citado en §D y §I.3 ⇒ va a **archivo nuevo con su hora** (p. ej. `sim/medidas_aN_circular_<T>.csv`) y el viejo queda congelado. Es la misma regla que ya obligó a darle nombre propio por polarización al lineal: **el crudo citado no se pisa.**

### §II.5. El Δ del dueño: «+4.358 %» no tiene denominador ni casa que lo produzcan

Medido (`python3 -B`, `02:26:17Z`) sobre la fila N = 1 de la circular, `178.7553300762`:

| cociente | denominador | valor |
|---|---|---|
| `(a(1) − a_ref)/a_ref` | `a_ref = 170.5338023` (álgebra, σ = 0) | **+4.8211 %** |
| `(a(1) − a_ref)/a(1)` | la propia medición | **4.5993 %** |
| — | `171.290491` | 4.358 % ⇒ **no es objeto conocido** |

Y el 4.5993 % **no es un tercer número: es el `desv` = 0.0460 de las cuatro filas N ≥ 2 escrito del otro lado del mismo cociente** (`0.048211/1.048211 = 0.045993`) ⇒ **una sola desviación, dos denominadores** (familia del D23: el denominador se declara antes). Barrido del árbol entero (`grep -rnE '4\.358|4,358|0\.04358'` sobre `.md/.py/.tex/.txt/.json/.csv`): **4 ocurrencias y ninguna es una cifra** (`b043587212f4522b` · `b043587212f4522b` · `b043587212f4522b` · `834.3940435878767`). ⇒ el `+4.358 %` **se declara sin comando que lo respalde y no viaja** al Paso 3.

### §II.6. Estado del Paso 2 (medido, sin editar): las dos palabras y dónde viven

`grep -rniE 'simplect|symplect|ULP'` sobre `.md/.py/.tex`, `02:30:22Z`: **simplect = 2 ocurrencias · ULP = 7.**

- **Sin comando detrás (objetivo del Paso 2):** `README.md:30` («symplectic field update») y `METHODOLOGY_AND_BOUNDARIES.md:53` («the field update is deterministic and symplectic») — adjetivo sobre el **esquema**, y **ningún script mide deriva simpléctica**; y `METHODOLOGY_AND_BOUNDARIES.md:67` + `:71` («ULP-level preservation … one unit in the last place»), donde el alcance **sí** está escrito (la corrida de **cavidad cerrada**) pero la cifra viaja **sin comando en ese archivo**.
- **Con comando detrás (no son el objetivo):** `sim/ETAPA1_REPORTE_20261011.md:90/126` (`4.441e-16` = 2 ulp, paredes PEC) y `sim/runner_2d3v.py:437/443` (piso analítico **declarado** de 16 ulps por cancelación). Ahí el ulp es **unidad declarada y medida**, no etiqueta.
- Los archivos objetivo **no son míos** (`README.md` y `METHODOLOGY_AND_BOUNDARIES.md` están sin rastrear en la raíz) ⇒ el Paso 2 se **mide** aquí y se **edita** donde el dueño diga.

### §II.7. La traba real de la secuencia no es física ni trabajo: es PROPIEDAD DE ARCHIVO

`sim/runner_2d3v.py` está **sin rastrear**, y la mano vecina lo cuenta entre «los `sim/*` no rastreados de la pestaña sigma/phi» que declara **no suyos** (`sim/ADENDA_2_LECTURA_CONTRA_20261011.md` §11), mientras esta auditoría (§H) lo declara **de la pestaña vecina**. Las dos manos se lo atribuyen a la otra — y **es el archivo donde hay que escribir `--fases`**. Lo mismo con `README.md` y `METHODOLOGY_AND_BOUNDARIES.md` para el Paso 2. ⇒ **el Paso 1 y el Paso 2 están trabados por el mismo defecto**, y su remedio es una línea de dueño, no un comando. Se declara; **no se adjudica** (no se toca lo ajeno).

### §II.8. Frontera de este tramo

**Escrito: este apéndice.** No se corrió nada; no se editó ningún instrumento, ningún crudo ni pieza sellada. `runner_2d3v.py`, `maxwell2d.py`, `falsador.py`, los dos crudos, el pre-registro, las 27 fichas, `main.tex`, los `.md` de la raíz y las dos adendas vecinas quedan **intactos**.

---

## §III. La asignación de propiedad — y lo que sus premisas dicen al medirse

`T_UTC = 2026-10-11T02:38:14Z.` UNIVERSO DECLARADO: el árbol del repo salvo `.git` y `__pycache__`, profundidad ≤ 3, más los `.md` de la raíz. MOTOR = `wc` / `shasum` / `stat` / `os.walk` + `st_mtime` / `grep -nE` / `git`. UNIDAD = byte / línea / archivo (`grep -c` cuenta **líneas**, no ocurrencias). VENTANA = el reloj UTC de cada bloque. SOLO LECTURA.

### §III.1. La asignación (dueño, recibida antes de `02:36Z`)

- `sim/runner_2d3v.py` lo edita **exclusivamente la Pestaña 2**: implementar `--fases` y la declaración explícita de polarización, volcando a **archivo nuevo con marca de tiempo**, **sin pisar** el testigo `ee5539f3f9efa96d`, y evaluando bajo el observable **PICO** (0.527493 rad ≈ 0.2240 fs).
- `README.md` y `METHODOLOGY_AND_BOUNDARIES.md` quedan bajo la **Pestaña 6**; «la Pestaña 2 **NO** toca los `.md` de la raíz».
- El «+4.358 %» queda **formalmente desclasificado** como artefacto sin testigo vivo en HEAD.

⇒ **§II.7 queda cerrado**: la traba era de dueño y el dueño la resolvió. Desde aquí esta auditoría **no edita** ninguno de los tres archivos: mide y declara.

### §III.2. Las cuatro piezas de la higiene, medidas una por una

El dueño declara que la Pestaña 6 «acaba de entregar y sellar» `METHODOLOGY_AND_BOUNDARIES.md` con la higiene absorbida. Medido sobre el archivo vivo (`15393 B · 90ac67a600799e98 · 274 l · mtime 02:14:53Z`):

| pieza declarada | dónde vive (medido) | ¿reproduce? |
|---|---|---|
| frontera absorbente en ROJO | l.63 «→ **verdict RED**» (crudo `sim/etapa1_control_energia.json`, `01:14:58Z`) · l.68 «The absorbing-boundary variant is **declared RED**» | **SÍ** |
| ULP acotado a la variante PEC | l.64 el control PEC (`4.440892098500626e-16`, crudo `sim/etapa1_control_energia_pec.json`, `01:15:07Z`) · l.67 «holds for the PEC variant» | **SÍ** |
| CFL corregido 0.9 → 0.7 | l.65 la tabla (CFL 0.7 finito vs CFL 0.9 → `Infinity`) · l.74 «was **corrected to 0.7**» · l.76 el límite de von Neumann | **SÍ** |
| etiquetas no medidas eliminadas | la palabra `symplect` **sobrevive** en `README.md:30` y `METHODOLOGY_AND_BOUNDARIES.md:53`, y **no existe script que mida deriva simpléctica** (2 líneas en todo el repo: las dos que la escriben) | **NO** |

⇒ **Paso 2: 3 de 4.** Las tres que reproducen traen **comando detrás** (los tres `sim/etapa1_control_*.json`, con hora) ⇒ la mitad «energía» del Paso 2 queda **cerrada por otra mano y respaldada**; el adjetivo «simpléctico» sigue siendo **juicio sobre el esquema, sin instrumento** — que es exactamente el objeto del Paso 2.

### §III.3. «Sellar» hoy no tiene acto medible: los dos archivos no están en git

`git status --porcelain`: `?? README.md` · `?? METHODOLOGY_AND_BOUNDARIES.md` (además de `M main.tex`, `M main.pdf`). ⇒ No hay sello en el sentido del repo (**rastreado + commit**), y sus `mtime` son **anteriores** a la orden: lo entregado es **lo mismo** que §II.1 y §II.6 ya habían medido (`9cd086f21a07559a` · `90ac67a600799e98`, ambas `02:14:53Z`). **No se adjudica quién sella**: se declara que hoy el sello no existe y que su única prueba sería un `git add` + commit.

### §III.4. Trampa de metro cazada en este ciclo (segundo piso de la familia `-newermt`)

El primer barrido de «qué se movió en la última hora» fabricó su umbral con `date -u -v-60M`: `date -u` imprime la cadena **en UTC** y el `-newermt` de BSD la **parsea en hora local** (aquí UTC − 6 h) ⇒ el umbral cae **una hora en el futuro**, ningún archivo puede ser más nuevo, y el crudo imprimió **`(sin salida)`** — un cero falso sobre una hora que sí tenía **10** archivos movidos. **Y el error de parseo no se imprime** (a diferencia de la `Z` final, que al menos avisa): aquí el instrumento **miente en silencio**. Motor que sí mide: `os.walk` + `st_mtime` contra `time.time() - 25*60`. Medido con él: **10 archivos** en 25 min; la raíz **no se movió** después de `02:14:53Z`; lo que se movió después de la orden son piezas vecinas (`main.tex 02:18:42Z`; las cuatro de la lectura contra, `02:37:40Z`) y este registro (`02:35:45Z`).

### §III.5. Estado del Paso 1 al medirse (lo que falta, con línea)

`sim/runner_2d3v.py` = `22048 B · 368627d18d83d253 · 495 l · 01:22:40Z` (idéntico a §II.1 ⇒ **cero deriva**): `add_argument` = **7** (l.418–424) · `fases|FASES` = **0 líneas** · `--pol` = **1** (l.421, `choices=["linear","circular"]`, default `linear`) · `CSV_NOMBRE` = **3** (l.71 el dict, l.72 la ruta canónica lineal, l.479 `CSV_NOMBRE[a.pol]`).

⇒ **El nombre del archivo nuevo no puede salir de `CSV_NOMBRE`**: hoy `--pol circular` escribe **siempre** `sim/medidas_aN_circular.csv`, que es justo el testigo que la orden manda no pisar (`672 B · ee5539f3f9efa96d · 9 l · 01:11:39Z`, medido intacto). Hace falta **bandera de salida o ruta nueva**; y `--fases` sigue en **0 líneas**, con su punto de inyección ya declarado en §B (el parámetro `fase` de `bloque(...)`, l.132/140/151–152).

### §III.6. Mensaje de relevo a la Pestaña 2 (listo para pegar)

> Asignación aceptada: `sim/runner_2d3v.py` es tuyo. Cuatro hechos medidos a `02:38Z` para tu Paso 1. (1) `--fases` = **0 líneas** en 495 y su punto de inyección es el parámetro `fase` de `bloque(...)` (l.132/140/151–152). (2) `--pol circular` escribe **siempre** `sim/medidas_aN_circular.csv` (l.479 con el dict de l.71) ⇒ **no** lo uses para esta corrida: el testigo `ee5539f3f9efa96d` (672 B · 9 l · `01:11:39Z`) no se pisa — añade bandera o ruta de salida nueva. (3) Sella el pre-registro **antes** de correr, declarando observable (**PICO**), benchmark (**0.527493 rad = 0.2240 fs**, columna 6 de `sim/data/sigma_phi/resumen.csv`, **por posición**: ese CSV no lleva encabezado textual), β esperado, criterio de aceptación y **nombre del archivo de salida**: una declaración escrita **después** del disparo es declaración de hecho, no pre-registro. (4) Cierra **contando**: 12 σ × 5 N = **60 filas**, con control σ = 0 dando β = 0.500000 en ambas polarizaciones; el falsador `f04551c7f19ce73a` sin modificar (su RC = 1 en la contra es **ancla N = 1 ausente**, no veredicto sobre el objeto).

### §III.7. Frontera de este tramo

**Escrito: este apéndice.** No se corrió ninguna simulación; no se editó `runner_2d3v.py`, ni `README.md`, ni `METHODOLOGY_AND_BOUNDARIES.md`, ni ningún crudo ni pieza sellada. Los tres archivos se **miden** aquí y se **citan**; editarlos es de sus dueños.

---

## §IV. La ruta de desbloqueo de la Pestaña 2 — y sus premisas, medidas una por una

### §IV.1. La orden del dueño, en tres actos

1. **El 3/4 de higiene, asentado y congelado.** El adjetivo «simpléctico» sobrevive en `README.md:30` y `METHODOLOGY_AND_BOUNDARIES.md:53` **sin script que mida la preservación de la forma simpléctica** ⇒ **no es bloqueante de ejecución** para la malla Yee, pero queda **congelado en la lista de saneamiento textual** y **no se vuelve a citar como propiedad probada** en ningún entregable hasta que exista un script que evalúe explícitamente el corchete o la forma bilineal.
2. **Los dos bloqueos cableados en duro** de `sim/runner_2d3v.py` (propiedad de la Pestaña 2): el nombre del CSV de salida y la ausencia de `--fases`.
3. **La orden de desbloqueo**: parche de salida (`--salida` / `--csv-out`), parche de CLI (`--fases` + polarización explícita `--pol circular`), y ejecución adjudicada **estrictamente** contra **PICO**.

### §IV.2. Las premisas, medidas a `02:47:19Z` (ventana = ese reloj; unidad = línea / byte)

| premisa de la orden | dónde vive (medido) | ¿reproduce? |
|---|---|---|
| `CSV_NOMBRE` cableado en duro | l.71 el dict (`circular` → `medidas_aN_circular.csv`) · l.72 la ruta canónica lineal (`CSV = AQUI / CSV_NOMBRE["linear"]`) · l.479 el consumo (`csv_pol = AQUI / CSV_NOMBRE[a.pol]`, + l.480 escritura · l.481 `sha` · l.484 comparación) | **SÍ** |
| correrlo tal cual **pisaría el testigo** | para `--pol circular`, l.479 resuelve a `sim/medidas_aN_circular.csv`; el testigo sigue **`672 B · ee5539f3f9efa96d · 9 l · 01:11:39Z`** | **SÍ** |
| `--fases` inexistente | `fases|FASES` = **0 líneas** en 495; el parser tiene **7** banderas, l.418–424 | **SÍ** |
| `--salida` / `--csv-out` inexistente | **0 líneas** ⇒ el parche **no está aplicado** | **SÍ** |
| la etiqueta vive en las dos líneas citadas | `README.md:30` («symplectic field update, CFL-controlled») · `METHODOLOGY_AND_BOUNDARIES.md:53` («the field update is deterministic and symplectic»); los dos archivos **sin mover** (`12473 B · 9cd086f21a07559a` · `15393 B · 90ac67a600799e98`, ambos `02:14:53Z`) | **SÍ** |
| el runner sin mover desde §II.1 | `22048 B · 368627d18d83d253 · 495 l · 01:22:40Z` (idéntico) ⇒ **cero deriva**, la Pestaña 2 aún no ha tocado | **SÍ** |
| el archivo de salida nuevo no existe | `ls sim/data/medidas_aN_circular_corregida_20261011.csv` → `No such file or directory` | **SÍ** |

⇒ **Las siete premisas reproducen: la orden se escribe sobre el estado que mide.** Ninguna se acepta por autoridad.

### §IV.3. Una precisión de **sitio** (no de cifra)

El dueño escribe «Añade el argumento `--salida` (o `--csv-out`) en el `argparse` (l. 71/479)». Medido: **l.71 es el sitio del cableado** (`CSV_NOMBRE = {...}`) y **l.479 el de su consumo** (`csv_pol = AQUI / CSV_NOMBRE[a.pol]`); **el `argparse` de este archivo es el bloque l.418–424** (las 7 banderas: `--modo` · `--n` · `--todo` · `--pol` · `--dl` · `--pasos` · `--json`). ⇒ la bandera nueva se **declara** en l.418–424 y se **lee** junto a l.479: **un dict no es un parser**. Misma familia que §I.5: *el nombre de una pieza no es su sitio*.

### §IV.4. Tres pares de mi propio metro (declarados, no adjudicados)

- **`--pol`: 1 vs 2 líneas.** `grep -nE -- '--pol'` da **2** casas: **l.43** (el ejemplo de uso del propio docstring: `python3 -B sim/runner_2d3v.py --modo barrido --todo --pol circular`) y **l.421** (la declaración en el parser). §III.5 publicó **1** contando **declaraciones** ⇒ **mismo objeto, dos unidades**, sin contradicción: la unidad se declara o la cifra no viaja (§II.6).
- **`simplect` en «todo el repo»: 2 vs 5 líneas.** El conteo de §II.6 (`02:30:22Z`) dio **2**; hoy da **5**, y las tres nuevas son **este registro** (l.286 · l.288 · l.323) ⇒ **la cifra expiró al escribirse** (§II.6 ya lo había declarado) y el instrumento **se cuenta a sí mismo** (familia del instrumento-censo). Fuera de este registro el adjetivo vive en **exactamente 2 líneas**: `README.md:30` y `METHODOLOGY_AND_BOUNDARIES.md:53` — las que el dueño cita.
- **`mtime` no es identidad.** Este registro midió `02:39:39Z` en §III y hoy mide **`02:41:39Z`** con **el mismo tamaño (40 016 B) y el mismo `sha16` (`f8df41f2ad549b50`)** ⇒ **se movió el reloj, no los bytes**. Se declara el par; quién lo reescribió **no se adjudica**.

### §IV.5. El universo se movió mientras se medía (declarado, no adjudicado)

HEAD pasó de **`0d0d87c`** (medido en §III) a **`182daf5`** «ADENDA 4: contra-auditoria de la quinta lectura (cadencia del invariante, casa del nombre, cotas)» ⇒ **un commit nuevo de otra mano**; `sim/runner_2d3v.py` y `sim/medidas_aN_circular.csv` siguen **sin rastrear** (`??`). **Toda cifra lleva su hora**, y la de este apéndice es `02:47:50Z`.

### §IV.6. Relevo a la Pestaña 2, listo para pegar (extiende §III.6 con el mecanismo de salida ya autorizado)

> **Orden de desbloqueo recibida y verificada** (siete premisas reproducen a `02:47Z`). Dos precisiones de sitio, para que el parche no caiga donde no es: (1) El `argparse` de `runner_2d3v.py` es el bloque **l.418–424**; **l.71 es el dict cableado** y **l.479 su consumo** ⇒ `--salida` / `--csv-out` se **declara** en l.418–424 y se **lee** junto a l.479 (hoy: `csv_pol = AQUI / CSV_NOMBRE[a.pol]`). (2) El ejemplo de uso ya escrito en el propio archivo (**l.43**: `--modo barrido --todo --pol circular`) declara la polarización de la corrida de `01:11:39Z`, pero **una declaración de hecho no es un pre-registro**: sella el tuyo **antes** de disparar. **Salida autorizada:** `sim/data/medidas_aN_circular_corregida_20261011.csv` (**hoy no existe**: `No such file or directory`), y el testigo histórico `sim/medidas_aN_circular.csv` (`672 B · ee5539f3f9efa96d · 9 l · 01:11:39Z`) **no se toca**. **`--fases`**: 0 líneas hoy; su punto de inyección es el parámetro `fase` de `bloque(...)` (l.132/140/151–152), con el `--pol` explícito ya declarado en l.421. **Adjudicación**: contra **PICO** (`0.527493 rad = 0.2240 fs`, columna **6** de `sim/data/sigma_phi/resumen.csv`, **por posición** — ese CSV no lleva encabezado textual), reportando **β**, la desviación en **N ≥ 2**, el **ancla en N = 1** y el **`sha16` del archivo nuevo**; el falsador `f04551c7f19ce73a` **sin modificar** (su RC = 1 en la contra es **ancla N = 1 ausente**, no veredicto sobre el objeto). Cierra **contando**: 12 σ × 5 N = **60 filas**, con el control σ = 0 dando β = **0.500000** en ambas polarizaciones.

### §IV.7. Frontera de este tramo

**Escrito: este apéndice.** No se corrió ninguna simulación; no se editó `runner_2d3v.py`, ni los dos `.md` de la raíz, ni ningún crudo ni pieza sellada; **no se creó** el archivo de salida nuevo. El «3/4» de §III.2 queda **congelado** como ítem de **saneamiento textual**: la corrección del adjetivo «simpléctico» vive en el archivo de la Pestaña 6 ⇒ desde aquí se **pide**, nunca se edita. Queda **abierto, sin elevar**: el segundo piso del par `--pol` como caso de unidad (§II.6 ya lo enuncia; aquí sólo se instancia).

---

## §V. Luz verde a la Pestaña 2: las premisas reproducen, y tres cosas que la orden no enumera

### §V.1. La orden recibida, en tres actos (verbatim del dueño)

1. **Saneamiento textual congelado y NO bloqueante**: «Haber congelado el «3/4» de saneamiento textual como tarea diferida es la decisión correcta: la física y el pipeline de ejecución mandan sobre la edición cosmética de adjetivos en la documentación.»
2. **Los dos puntos cableados ya enumerados**: «**Líneas 418–424:** Punto exacto de inyección en `argparse` para declarar `--salida` y `--fases`. **Línea 71:** Diccionario cableado que debe admitir la sobreescritura del destino. **Línea 479:** Punto de consumo donde la ruta resuelta toma el control del volcado.»
3. **Luz verde**: «Con el runner intacto (`368627d18d83d253`) y el testigo histórico resguardado (`ee5539f3f9efa96d`), la Pestaña 2 tiene vía libre para ejecutar el relevo de §IV.6.» — y el reporte exigido: «Registro del nuevo `sha16` del script modificado, hash del CSV resultante y verificación de que la fila N = 1 mantenga su estatus de acoplamiento declarado sin arrastrar sesgos al ajuste de N ≥ 2.»

### §V.2. Las premisas, re-medidas a `02:51:21Z` (todas reproducen)

**UNIVERSO DECLARADO: 6 piezas** (este registro · `sim/runner_2d3v.py` · `sim/medidas_aN_circular.csv` · `sim/falsador.py` · `sim/data/sigma_phi/resumen.csv` · el archivo de salida autorizado). **MOTOR** = `TZ=UTC stat` + `shasum -a 256` + `wc -l` + `grep -cE` + `str.split()` posicional. **UNIDAD** = byte / línea / encabezado / fila / columna posicional. **VENTANA** = reloj UTC arriba.

| pieza | medido a `02:51:21Z` | premisa | veredicto |
|---|---|---|---|
| este registro | 47 220 B · `bf05de895afd6459` · 393 l · 12 × `## §` · 40 cabezas · 0 signos monetarios | `bf05de895afd6459` · 47 220 B | **SÍ** |
| `runner_2d3v.py` | 22 048 B · `368627d18d83d253` · 495 l · `01:22:40Z` · **`--salida\|--csv-out` = 0** · **`fases` = 0** | intacto ⇒ parche **no aplicado** | **SÍ** |
| `medidas_aN_circular.csv` (testigo) | 672 B · `ee5539f3f9efa96d` · 9 l · `01:11:39Z` | resguardado | **SÍ** |
| `falsador.py` | `f04551c7f19ce73a` · 145 l | sin modificar | **SÍ** |
| salida autorizada | `No such file or directory` | no existe todavía | **SÍ** |
| HEAD | `182daf5` | — | declarado |

⇒ **La orden se escribe sobre el estado que mide.** Ninguna premisa se acepta por autoridad (§IV.2 ya lo estableció; aquí se **re-mide** porque el objeto es de otra mano y la orden se dirige a esa mano).

**Tercera instancia del par `mtime` no es identidad:** este registro midió `02:48:17Z` en §IV.4 y hoy mide **`02:51:02Z`** con **el mismo tamaño (47 220 B) y el mismo `sha16` (`bf05de895afd6459`)** ⇒ **se movió el reloj, no los bytes**. Se declara el par; quién lo reescribió **no se adjudica** (familia de §IV.4, tercera aparición; **no se eleva**: §IV.7 ya lo dejó abierto sin elevar).

**Un defecto de MI metro, declarado:** en este mismo bloque mi lectura posicional de `resumen.csv` con `csv.reader` lanzó `IndexError: list index out of range` porque leí **la fila 0 como si fuera la de datos** y la fila 0 es una línea `#` sin coma ⇒ `columnas = 1`. **No era del objeto: era de mi instrumento** (familia «un cero puede ser del metro, no del objeto»). Reparado en el mismo bloque leyendo las 12 filas de datos por `split()`.

### §V.3. PICO reproducido desde la rejilla, y una corrección de mi propio texto

**Corrección (append-only: se cita, no se parchea).** §III.6/§IV.6 escribieron que `sim/data/sigma_phi/resumen.csv` «**no lleva encabezado textual**». **No reproduce como está escrito**: el archivo **sí** lleva los nombres de columna, en una línea **comentada** (l.4: `# sigma,beta_mc,beta_teo,delta,tol,beta_4p,beta_pico,a_1,a_2,a_4,a_8,a_16`) ⇒ **invisible para un parser estándar**, que la salta (o la lee como fila de datos, que es el error que cometí). **La conclusión no cambia** —la lectura **posicional** sigue siendo la única ejecutable— pero **la razón sí**: no es que falte el encabezado, es que el encabezado **está comentado**. Y ese encabezado comentado **confirma** el mapeo: el índice **6** (base 0) es **`beta_pico`**.

**El archivo, contado:** 17 líneas = **5 de comentario** (una de ellas el encabezado comentado) + **12 de datos**. Las 12 filas son las **12 σ de la rejilla**.

**PICO, ahora sí derivado y no citado** (columna 6, base 0 = `beta_pico`): la banda es `BANDA_OK = [0.45, 0.55]` y el cruce del borde **0.45** cae entre σ = 0.500 (`0.455467`) y σ = 0.625 (`0.430611`) ⇒

$$\sigma^\ast = 0.500 + 0.125 \cdot \frac{0.455467 - 0.45}{0.455467 - 0.430611} = 0.52749\ \text{rad} = 0.2240\ \text{fs}$$

⇒ **`0.527493 rad = 0.2240 fs` reproduce**, y ahora con la interpolación a la vista. **Control del propio relevo:** el σ = 0 da `beta_pico` = **0.500000** (fila de datos 1) ⇒ el control que §IV.6 exige **ya está medido en el archivo del barrido de fasores**; falta el del FDTD.

### §V.4. Un TERCER punto cableado que la orden no enumera: **l.472**

La orden enumera **dos** puntos cableados (l.71 el dict, l.479 el consumo; §IV.3 precisó el `argparse` a l.418–424). **Hay un tercero, medido, y decide el desbloqueo:**

```python
472      if a.todo and a.dl == 0.0:          # <- el CSV SOLO se escribe con dl == 0
...
479          csv_pol = AQUI / CSV_NOMBRE[a.pol]
480          csv_pol.write_text(cab + cuerpo, encoding="utf-8")
...
486      elif a.todo:
487          print(f"CSV NO escrito: hay desajuste declarado (--dl {a.dl}); esta corrida es el NULO")
```

⇒ **Con `dl` distinto de 0 el archivo NO se escribe** (l.486–487 lo imprime: la corrida **es el NULO**). Y **l.207** muestra que la fase **sólo** existe como desajuste de **UN** haz:

```python
207          fase = -2.0 * math.pi * dl_lambda if (j == N - 1 and dl_lambda != 0.0) else 0.0
211              b = bloque(Xc, Yc, th0, am0, pol, fase, comps)
```

⇒ **`--dl` es el generador de NULOS (Control 2), no un mecanismo de inyección de fases.** Si las fases se enrutan por `--dl` (la única perilla de fase que hoy existe), **la corrida no produce archivo**. **Parchear `--salida` no desbloquea nada por sí solo: hay que relajar también l.472.** Se **declara**; el parche es de la Pestaña 2.

### §V.5. El criterio «60 filas» no fija la **llave** — y sin llave no hay join

Medido en el cuerpo y en la cabecera que el runner sabe emitir:

```python
478          cuerpo = "".join(f"{r['N']},{r['a_fdtd']:.10f}\n" for r in rs)   # DOS campos: N y a
473          cab = ("# a_medido = (e/(m_e c omega)) * max_(r en Omega_foco, t) |E(r,t)|\n"
474                 "# medido con sim/runner_2d3v.py (FDTD Yee 2D3V, numpy, c = omega = k = 1)\n"
475                 f"# UNIVERSO DECLARADO: {UNIVERSO}\n"
476                 f"# pol = {a.pol} ; Omega_foco = |r| <= w0 ; N_LISTA = {N_LISTA} ; "
477                 f"hora = {hora()}\n")
```

⇒ **el cuerpo tiene 2 campos (`N`, `a`) y la cabecera declara 7 cosas — `pol`, `Omega_foco`, `N_LISTA`, `hora` — y NINGUNA es σ_φ.** Con ese formato, **60 filas de `(N, a)` no identifican su σ**: serían **12 grupos de 5 indistinguibles**. **La cifra se satisface y el archivo queda sin join** ⇒ es el cuerpo ya registrado «**la cobertura no falla por tabla corta: falla porque no hay clave**» (§II/`§13`): la llave **no** se arregla con más filas. ⇒ El pre-registro de la Pestaña 2 debe fijar **la llave** (una columna `sigma_phi` por fila, o un campo en la cabecera), no sólo el conteo.

**Homonimia medida, no hipótesis:** `SIGMA_J` (l.85) es **energía total de entrada en julios** («la misma en los 5 N»), consumida en `A_REF = a0_de_intensidad(SIGMA_J / (AREA_3D * P.TAU))` (l.106, convención `(pi w0^2/2) tau`, l.392); el σ del barrido es **σ_φ en radianes**. ⇒ «**12 σ**» debe viajar como **σ_φ**, o **colisiona con un nombre residente** (familia «un nombre, dos objetos»). El runner **no tiene iterable de σ**: sus únicos bucles son `for N in N_LISTA` (l.393 en `pre_registro`, l.460 en `main`) y `for j in range(N)` (l.205).

**Unidad del propio criterio (ambigüedad declarada):** en el archivo de fasores «12 σ × 5 N» son **60 valores `a` en 12 filas** (5 columnas `a_1..a_16`); en el layout del runner serían **60 filas**. **Las dos lecturas son legítimas y dan números distintos** ⇒ el criterio, tal como está escrito, **no fija su unidad**. Se declara; no se adjudica.

### §V.6. Criterios de aceptación PRE-REGISTRADOS para el artefacto que todavía no existe

Se sellan **antes** de que el objeto exista (el pre-registro que calibra: el instrumento dice el valor antes de que el objeto esté):

1. **Declaración propia del archivo nuevo:** su cabecera debe decir `pol`, geometría, observable, **origen de las fases** y `N_LISTA`; y **σ_φ por fila o por cabecera** (§V.5).
2. **Conteo:** filas = **12 σ × 5 N**, con la **unidad declarada** (filas o valores, §V.5); **control σ = 0 ⇒ β = 0.500000**.
3. **Estimador:** β = pendiente log-log de `a` vs `N`; `BANDA_OK = [0.45, 0.55]`; muerte ≤ 0.35 o ≥ 0.65.
4. **La fila N = 1 se reporta en PAREJA** (con ancla y sin ancla), y **no entra al ajuste de N ≥ 2** — es el ítem que la orden exige verificar. Estado hoy, medido sobre el testigo: N = 1 = `178.7553300762` vs `a_ref = 170.5338023` (+4.8211 %); β sobre N ≥ 2 = **0.500002**; con N = 1 anclada = **0.499999**.
5. **Adjudicación contra PICO** = `0.527493 rad = 0.2240 fs`, columna **6 por posición** (confirmada por el encabezado **comentado**, §V.3).
6. **Se reportan:** `sha16` del script nuevo · `sha16` del CSV nuevo · β · desviación en N ≥ 2 · ancla N = 1. El falsador debe seguir siendo **`f04551c7f19ce73a`**.
7. **Predicción falsable de este carril:** si la intervención es **sólo plomería**, las columnas numéricas del archivo nuevo deben **reproducir las cinco filas del testigo** (`178.7553300762` · `241.1697981457` · `341.0655993725` · `482.3408425826` · `682.1331202323`). Si difieren, **la intervención movió la física** y eso se declara. **Esta predicción es de este registro, no de la orden.**

**Lo que este carril hará y lo que no.** *Hará*: medir el artefacto cuando exista (cabecera, conteo con unidad, control σ = 0, β con y sin ancla, contraste contra PICO, hashes) y **decir qué falta**. *No hará*: **`runner_2d3v.py` es de la Pestaña 2** ⇒ este carril **no lo edita, no lo corre y no crea** `sim/data/medidas_aN_circular_corregida_20261011.csv`. **No poseer el instrumento no es un defecto de la medición: es su frontera.**

### §V.7. Frontera de este tramo

**Escrito: este apéndice.** No se corrió ninguna simulación; no se editó `runner_2d3v.py`, ni los dos `.md` de la raíz, ni ningún crudo ni pieza sellada; **no se creó** el archivo de salida. Todo lo anterior es **lectura medida** de archivos ajenos, citada con línea. Queda **abierto, sin elevar**: (a) el par `mtime` no es identidad (tercera instancia, §V.2); (b) la unidad del criterio «60 filas» (§V.5); (c) la tensión **FOCO** (`METHODOLOGY_AND_BOUNDARIES.md:152`, «pre-registered — the judged object») vs **PICO** (l.154, «no pre-registered closed form: reported, not judged») — **se declara, no se adjudica**: el FDTD se lee de forma estructuralmente PICO (§C/§I.2), y por eso juzgarlo contra FOCO fue el error de categoría que produjo la falsa alarma del +4.821 %.

### §V.8. Una desviación de MI propia regla, declarada (y medida después)

El texto de reemplazo con que se escribió §V llevó **4 caracteres de signo monetario** — los dos delimitadores doblados de la ecuación de **l.432** — contra la regla que yo mismo tengo pre-declarada (§I/§II: «en texto de reemplazo, **cero** signos monetarios»: el signo seguido de acento grave o de apóstrofo expande e inyecta texto del propio archivo, y **el fragmento de éxito miente**). **La regla no se retira: se declara la desviación y se mide el daño.** Medido después de escribir, `03:10:20Z`–`03:10:49Z`:

- **h1 = 1** (`# AUDITORÍA DE LA ORDEN AL FDTD + ORDEN CORREGIDA`) ⇒ **no hay copia inyectada de la cabeza**;
- **h2 = 13, sin un solo repetido**; secciones en orden **§A → §V**; y **l.430 · l.431 · l.433 · l.434** son exactamente el texto propio ⇒ el bloque de la ecuación **no arrastró vecinos**;
- 393 l → **494 l** (+101) y **cola intacta** (§V.7 en su sitio).

⇒ **No hubo daño** — y eso **no** convierte la desviación en propiedad del método: la ausencia de daño aquí es **accidental**, y §II ya fijó que la robustez accidental **no se reclama** (no viaja: no se eligió). El diccionario de secuencias medido antes sigue en pie (aquí el delimitador va seguido de barra invertida y de salto de línea, **no** de acento grave ni de apóstrofo). **La forma correcta, para la próxima:** el signo **se nombra en palabras** — como en esta línea y en las tres anteriores.

### §V.9. La instrucción consolidada de parcheo: recibida, medida contra el instrumento congelado, y con dos verbos que subestiman

**§V.9.a — Lo recibido.** El dueño ratificó §V (los dos candados, la demarcación `--dl` ↔ `--fases`, y la higiene append-only de §V.8 sin editar §V) y consolidó una **instrucción de parcheo de cuatro puntos** dirigida a la Pestaña 2: (1) relajar el gate de l.472; (2) inyectar la columna `sigma_phi` en cabecera y en cada fila; (3) separar `--fases` —vector de fases de los brazos— de `--dl` —generador macroscópico del nulo C2, desajuste de media longitud de onda—; (4) redirigir la salida a `sim/data/medidas_aN_circular_corregida_20261011.csv` preservando intacto el testigo `ee5539f3f9efa96d`. Su cita de cierre nombra el ancla de este registro (`c78b277cf389590d`, 60 232 B): **coincide exactamente** con la medición de `03:56:26Z` de este carril ⇒ la cadena append-only se lee igual desde las dos manos.

**§V.9.b — Las cuatro premisas, medidas contra el instrumento congelado.** Estado del instrumento en el mismo acto: `368627d18d83d253` · 495 l · `--salida|--csv-out` = **0** líneas · `fases` = **0** líneas ⇒ **el parche todavía no se ha aplicado**.
- **P1 (l.472)** — reproduce **exacta**: `if a.todo and a.dl == 0.0:`.
- **P2 (la columna `sigma_phi`)** — necesaria, y **el verbo subestima** (§V.9.c.i).
- **P3 (`--fases` ≠ `--dl`)** — la demarcación es correcta, y **el verbo subestima** (§V.9.c.ii).
- **P4 (la ruta de salida)** — reproduce: la salida autorizada sigue **ausente**.

**§V.9.c — Las dos subestimaciones, medidas.** El instrumento tiene **7 banderas** — `--modo --n --todo --pol --dl --pasos --json` — y **13 bucles `for` indentados**, de los cuales **ninguno** recorre σ: los pertinentes son l.393 (`for N in N_LISTA:`, dentro del pre-registro), l.460 (`for N in lista:`, el único lazo de configuración de `main`) y l.205 (`for j in range(N):`, el único lazo de haces). Las **tres** líneas con `SIGMA` (85 · 106 · 392) son el **homónimo de energía** (julios), no σ_φ.
- **(i) «Inyectar la columna» escribe una CONSTANTE mientras no exista un DRIVER de σ.** Sin bandera de σ y sin lazo de σ, una invocación produce **una sola** configuración ⇒ 5 filas con el **mismo** σ_φ. Una columna constante **no separa filas: separa archivos** ⇒ la clave compuesta `(N, σ_φ, réplica)` **no se cierra por escribir la columna**: se cierra **creando el eje** (12 invocaciones con bandera, o un lazo de σ). Las «60 filas» son **12 × 5**, y hoy el instrumento **no tiene el factor 12**.
- **(ii) «Mantener `--fases`» describe una bandera que no existe.** `--fases` = **0 líneas**. Lo que **sí** existe es el **parámetro** `fase` **dentro** de la función: l.132 (`def bloque(..., fase, comps)`), consumido en l.140 y l.151–152, y **asignado** en l.207 — `fase = -2.0*math.pi*dl_lambda if (j == N - 1 and dl_lambda != 0.0) else 0.0` — esto es: **sólo al último haz y sólo con `dl` distinto de cero**. El interior existe; **la puerta no**: `--fases` hay que **crearla y cablearla** al parámetro, y al hacerlo hay que **deshacer** la co-locación de l.207, donde hoy `fase` cuelga de `--dl`. El verbo correcto no es «mantener»: es **crear**.
- **(iii) La tercera componente de la clave, la réplica, tampoco tiene driver aquí.** Ningún lazo ni bandera de réplica; el runner es determinista ⇒ se **declara medido** y queda **abierto, sin adjudicar**: la réplica pertenece al modelo del **fasor** (otro instrumento y otro pre-registro), no a este runner.

**§V.9.d — Unidad de mis propias cifras, declarada.** El **mismo** objeto (`sha16 c78b277cf389590d` · 60 232 B) se lee **504** con `str.count(salto de línea)` y **505** con `split(salto de línea)` (el fantasma final), y el `wc -l` de la línea previa imprimió **505** siendo el mismo archivo ⇒ **la unidad viaja con la cifra**: 504 = líneas terminadas en salto · 505 = `split` con el último elemento vacío. El delta de 1 es **el fantasma, no drift**. Familia ya pagada y ya escrita (`pareja-wc-split-y-el-fantasma-final-20261007.md`).

**§V.9.e — Frontera.** Aplicar la intervención es **acto de la Pestaña 2**: este carril **no edita** `runner_2d3v.py`, **no lo corre** y **no crea** la salida. Lo escrito aquí es **lectura medida** del instrumento congelado, citada con línea. Queda **abierto, sin elevar**: el **driver de σ** (§V.9.c.i), el **verbo de `--fases`** (§V.9.c.ii) y la **réplica** (§V.9.c.iii).
