# ADENDA §8.4 — CONVENCIÓN DE ORDEN DE ADJUNTOS Y LEY DE COMPOSICIÓN MEDIDA SOBRE TRES MALLAS ANIDADAS

`HUELLA: ORDEN-DE-ADJUNTOS-SELLADO-20261013` · apertura `2026-10-13T02:2xZ` · motor `python3 -B` · `TZ=UTC`

**UNIVERSO DECLARADO: el crudo sellado `sim/data/invariantes/convergencia_p_tercera_malla_20261012.json` (sha16 `b381e3d77c6feff7` · sha1 `d0ca45cd685c39d940807e5b332b96617808db3f` · 492 l · 9985 B · `T_UTC = 2026-10-12T07:28:49Z` · `RC = 0`) y su ACTA `sim/ACTA_CONVERGENCIA_P_TERCERA_MALLA_20261012.md` (sha16 `4f915187b77dc691`), más el documento-casa `marco-fibrado-20261011/ABSTRACT_Y_TABLA_CATEGORICA_20261011.md` (sha16 `26326856b7fb7d60`).** UNIDAD: `nodos = 60·2^k + 1`, `h = dx/λ` (`h = 0.100000 · 0.050000 · 0.025000 · 0.012500`). DENOMINADOR: `L0_exacto` a **361** nodos de la **misma** geometría (`referencia_dx_sobre_lambda = 0.016666666666666666`). VENTANA: la del crudo (`07:28:49Z`). UMBRAL/bandas: las pre-registradas en `sim/PREREGISTRO_CONVERGENCIA_P_20261012.md` §4 (`sha16 7476477b58cda501`). **Esta adenda NO corre nada: es LECTURA DERIVADA del crudo sellado.**

---

## §1 · LA CASA DE «§8.4» — SE DECLARA INFERENCIA MEDIDA, NO ADJUDICACIÓN

**Medido, no adjudicado.** El literal `§8.4` **no existe** en ninguna pieza del repo con el sentido de «sección 8.4»: `main.tex` tiene **5** `\section` (l.60/120/227/393/628) y **ninguna** es §8 ⇒ `main.tex` **descartado como casa**. La casa medible es el documento `marco-fibrado-20261011/ABSTRACT_Y_TABLA_CATEGORICA_20261011.md` (rastreado en git, `git status --porcelain -uall -- marco-fibrado-20261011/` = **vacío**):

| ancla | qué dice (verbatim) |
|---|---|
| **§8, item 4** (l.210) | «**La composición `f* g* = (gf)*`** (fila 6): sólo hay un par de niveles impreso. Con **tres** niveles de malla el semigrupo RG pasaría de `DECLARADO` a `MEDIDO`. Es la mejora de mayor rendimiento por unidad de costo.» |
| **fila 6 de la tabla §3** (l.73) | «Ley de composición `f* g* = (gf)*` · el semigrupo RG · — · sólo hay **un par** de niveles impreso ⇒ composición **no medida** · `DECLARADO`» |
| **fila 5 de la tabla §3** (l.72) | «Reindexación `f*: F_σ → F_σ′` · transporte del observable entre mallas · `derivada con la malla (lam/10 -> lam/20)` · **MEDIDO**» |
| **§4 (2)** | «Las tolerancias numéricas son el defecto de una transformación pseudonatural … es la **magnitud de la 2-celda** `α` que mide cuánto no conmuta el diagrama, con `‖α_{f,g}‖ ≤ ε`.» |
| **fila 7 de la tabla §3** | «2-celda laxa `α` · defecto de no-conmutación = **ε numérico** · `R_L4 / R_intrínseco` · MEDIDO» |

⇒ **`§8.4` ≡ §8 item 4 ≡ fila 6.** Esta equivalencia es **inferencia medida por dos literales** (`(gf)` aparece **sólo** en l.73 y l.210 de esa pieza); **no** lleva firma del dueño. Si el dueño adjudica otra casa, esta pieza queda con su propia ruta y no se renumera nada.

**Trampa declarada (no reparada):** el pre-registro padre cita la ruta `sim/marco-fibrado-…`, que **no resuelve**; la ruta real es la **raíz del repo**. Ya está declarado en `sim/ACTA_CONVERGENCIA_P_TERCERA_MALLA_20261012.md` §8 (1).

---

## §2 · LA CONVENCIÓN DE ORDEN (C-ORD) — DECLARACIÓN PURA, CERO CIFRAS

El **mismo signo** nombra **dos objetos distintos** en este marco, y no se mezclan:

| namespace | signo | qué es | dónde vive |
|---|---|---|---|
| **(A) reindexación** | `f*` | *pullback* del observable entre fibras: `f* : F_σ → F_σ′` | fila 5 de la tabla §3 (**MEDIDO**) |
| **(B) adjunto** | `A^*` | adjunto de Hilbert / transposición discreta | el `(gf)^*` de la orden del ciclo |

### C-ORD (fijada aquí)

1. **La yuxtaposición se lee con el factor de la DERECHA aplicado primero:** `X Y := X ∘ Y`. Es la convención de composición de funciones, y es la única que hace que la cadena se lea **de derecha a izquierda en la base**.
2. **Consecuencia 1 (ley de composición).** `f* g* = f* ∘ g* = (g∘f)*`. **No** es `g* f*`: la reindexación es **contravariante** respecto de la flecha base, y lo que la ley afirma es que la cadena de reindexaciones compone **al revés** que la cadena de escalas.
3. **Consecuencia 2 (adjuntos).** El adjunto **invierte el orden**: `(gf)^* = f^* g^*`. Escribir `(fg)^*` **nombra otro operador**; y `(gf)^* ≠ (fg)^*` salvo que los factores conmuten — que es **exactamente la pregunta**, no un supuesto de partida. **Queda declarada la lectura excluida:** en esta adenda `(gf)^*` **nunca** se lee como `g^* f^*`.
4. **Consecuencia 3 (lo que se mide).** Si la ley se cumple, la 2-celda es nula (`α = 0`, `‖α_{f,g}‖ ≤ ε` con `ε = 0`). La **2-celda laxa `α`** es por tanto la **medida del defecto de la composición respecto de la ley** — y es lo único que tiene contenido numérico. La convención **no aporta cifras: gobierna qué se compara con qué.**

**Trampa que la convención cierra (familia «un nombre, dos objetos»):** escribir el producto como `f* g*` y leerlo como `g* ∘ f*` **cambia el sentido sin cambiar el texto**. Un orden que no se declara no se puede leer; peor, **dos lectores disciplinados obtienen dos leyes distintas del mismo renglón**.

**Lo que la escalera regala (declarado, no supuesto):** los tres escalones son **uniformes** — `log(h1/h2) = 0.693147180560` **idéntico en los tres** (valor declarado en la fuente) y cada escalón **divide `h` por 2** ⇒ la composición de dos escalones consecutivos es **otra vez un escalón** del mismo semigrupo (factor 4) y la de tres también (factor 8). **No hace falta normalizar** para comparar los exponentes compuestos con los de un escalón.

---

## §3 · LA LEY DE COMPOSICIÓN SOBRE LAS TRES MALLAS ANIDADAS — MEDIDA

Escalera de la fuente: **4 mallas** (`61 · 121 · 241 · 481`) ⇒ **3 escalones** (`k = 0..3`), `LADO = 6.0`, `λ = 1`. Con **dos** mallas hay **una** flecha: la ley **no se puede leer**. Con **tres** hay **dos flechas componibles** y **una compuesta** ⇒ la ley queda **sobredeterminada**. Ése es el sentido exacto en que la fila 6 pasa de `DECLARADO` a `MEDIDO`.

### §3.1 · El crudo de la lectura derivada (comando único; todas las cifras de §3 salen de aquí)

```
TZ=UTC python3 -B /tmp/lectura_derivada_8_4_20261013.py
```

```
UNIVERSO DECLARADO: crudo sellado b381e3d77c6feff7 (492 l, 9985 B, sha1 d0ca45cd685c39d940807e5b332b96617808db3f)
VENTANA DE LA FUENTE: 2026-10-12T07:28:49Z | RC fuente: 0 | mallas: [61, 121, 241, 481]
MOTOR: python3 -B (lectura, CERO corridas) | UNIDAD: h = dx/lambda, nodos = 60*2**k + 1
LOG(h1/h2) declarado en la fuente: 0.693147180560 (identico en los 3 escalones)

geometria              eps1[%]  eps2[%]  eps3[%]  eps4[%] |    p(E1)    p(E2)    p(E3) | 1-p1/2   1-p2/2   1-p3/2 | r12     r23
abanico 30.0 m=17    33.9658   9.6907   2.5226   0.6375 |  1.809406  1.941702  1.984480 | 0.095297 0.029149 0.007760 |  3.269   3.756
abanico 26.5651 m=17 43.0890  12.6034   3.3138   0.8399 |  1.773500  1.927271  1.980271 | 0.113250 0.036364 0.009864 |  3.114   3.686
abanico 30.0 m=9     30.4986   8.6149   2.2341   0.5640 |  1.823838  1.947144  1.986028 | 0.088081 0.026428 0.006986 |  3.333   3.783

COMPOSICION (dos pares al MISMO factor 4 y la triple al factor 8):
geometria                  c(61>241,f4)  c(121>481,f4)  c(61>481,f8) | c12-c23    c123-mean | c12-(p1+p2)/2
abanico 30.0 m=17            1.875553768    1.963091095   1.911862574 | -0.087537  -0.007460 | -2.22e-16
abanico 26.5651 m=17         1.850385769    1.953771176   1.893680884 | -0.103385  -0.008398 | +0.00e+00
abanico 30.0 m=9             1.885491198    1.966585906   1.919003316 | -0.081095  -0.007035 | -2.22e-16

ANIDAMIENTO EXACTO (la parte de la ley que solo depende del conjunto de nodos):
  mallas [61, 121, 241, 481] -> 481-1=480, 241-1=240, 121-1=120, 61-1=60 ; 480/120=8 120/60=4 60/30=2
  => los nodos de 61/121/241 son subconjuntos EXACTOS de 481: restriccion sin interpolacion (denominador entero)
VEREDICTO LITERAL DE LA FUENTE: VERDE -- p desacelera hacia 2 desde abajo sin alcanzarlo, en las tres geometrias
RC_LECTURA=0
```

**ERRATA DE RÓTULO del instrumento de lectura (se declara, no se repara):** en el bloque `ANIDAMIENTO EXACTO` el **rótulo** de la línea final está mal escrito (`480/120=8  120/60=4  60/30=2`); las **cifras impresas son correctas** y su descomposición real es `480/60 = 8` · `240/60 = 4` · `120/60 = 2`. El rótulo **afirma lo que las cifras desmienten**: manda la cifra con su descomposición, no el rótulo. (Familia: «un rótulo fijo que afirma lo que la línea siguiente desmiente no protege: informa».)

### §3.2 · Lo que se cumple **por construcción** (identidad — **NO es evidencia**)

1. **Anidamiento estricto.** Los nodos de 61/121/241 son **subconjuntos exactos** de los de 481: los denominadores son enteros (`480/60 = 8`, `240/60 = 4`, `120/60 = 2`) ⇒ la restricción de la malla fina a la gruesa **no interpola**. Ésta es la mitad de la ley que **sólo depende del conjunto de nodos**, y se cumple **exactamente**.
2. **La identidad del estimador.** `c12 − (p1+p2)/2 = −2.22e−16` en dos geometrías y exactamente `0` en la tercera; `c123 − media(c12,c23)` **no** es nulo (abajo), pero `c123 − (p1+p2+p3)/3` sí lo es. La razón es elemental: bajo escalones uniformes, `log(eps1/eps3)/log 4` **es** el promedio aritmético de los dos `p` de sus escalones. ⇒ **Una identidad no es evidencia**: esto **verifica el metro** (que el estimador compone como debe), **no mide el objeto**. Se publica como identidad, con su hora.

### §3.3 · Lo que **sí** tiene contenido: la 2-celda no es nula

**(a) Contra el límite continuo.** El exceso `1 − p_k/2` (la distancia del escalón a la ley `h²`) **decrece en los tres escalones y en las tres geometrías**, y su razón por halving va **de ~3.1–3.3 a ~3.7–3.8**, acercándose a **4** desde abajo — la firma de un `p` que sube hacia 2 sin alcanzarlo:

| geometría | `1 − p1/2` | `1 − p2/2` | `1 − p3/2` | razón 1→2 | razón 2→3 |
|---|---|---|---|---|---|
| abanico 30.0 m=17 | 0.095297 | 0.029149 | 0.007760 | 3.269 | 3.756 |
| abanico 26.5651 m=17 | 0.113250 | 0.036364 | 0.009864 | 3.114 | 3.686 |
| abanico 30.0 m=9 | 0.088081 | 0.026428 | 0.006986 | 3.333 | 3.783 |

**(b) Contra la lectura ingenua de «asociatividad».** Los dos pares composibles **van al MISMO factor 4** y por tanto son comparables en la misma unidad: `c12 − c23 = −0.087537 / −0.103385 / −0.081095`. **Esa diferencia NO es un fallo de asociatividad** (la compuesta de una cadena es la misma aplicación, se agrupe como se agrupe) — es la medida de que **el exponente del compuesto depende de QUÉ escalones se compongan**, es decir de que la ley **no es exacta** en la escalera finita. Se imprime el par, **no se elige**, y **no se adjudica** como defecto de la ley categórica.

**(c) La conmutación que la orden pide, dicha con precisión.** El diagrama que **sí** puede no conmutar no es `f* g*` contra `(gf)*` (eso es lo de §3.2 y es exacto por construcción), sino **la reindexación contra el resolutor**: `[restricción, resolver]`. La solución en la malla fina **restringida** a los nodos de la gruesa **no** es la solución en la gruesa, y esa diferencia **es** `eps`. Su tasa es `p`, y su distancia a `h²` es `1 − p/2` ⇒ **la 2-celda decrece desde arriba hacia cero, con `p → 2⁻`, no saturada en la ventana**. El límite continuo **conmuta en el límite**, no en la ventana.

**(d) Veredicto del crudo, verbatim:** `VERDE -- p desacelera hacia 2 desde abajo sin alcanzarlo, en las tres geometrias`. Bandas pre-registradas (§4 del pre-registro): `p(E3)` cae en **VERDE** (`1.96 ≤ p3 < 2.00` y `p3 ≥ p2`) en las **tres** geometrías; `p(E1)` en **ROJO NO-SATURA** y `p(E2)` en **GRIS** en las tres ⇒ **una sola banda cada una, sin MIXTO**.

**(e) Guardas que se respetan (no se re-miden, se citan):** `eps > 0` en las cuatro mallas de las tres geometrías · `log(h1/h2) ≠ 0` e **idéntico** en los tres escalones (`0.693147180560`) · **tres** escalones (con menos de tres, `SIN MEDIDA`). **El par `(p, C)` viaja junto** (`C_p2 / C_p3` de la fuente: `40.797860649 / 38.115514524` · `53.750421998 / 49.298764253` · `36.093317725 / 33.949702798`): **un `p` sin su par de mallas no se publica**. **`p = 2` no se escribe como resultado.**

---

## §4 · LO QUE ESTA ADENDA **NO** HACE

1. **No corre nada.** Cero corridas nuevas; las cifras de §3 son **lectura derivada** del crudo sellado `b381e3d77c6feff7`, con comando y ventana.
2. **No eleva.** `n = 1`: se registra el paso de fila 6 de `DECLARADO` a `MEDIDO` en su **forma estructural**, y el valor medido de `α`; **nada se eleva a familia**.
3. **No toca instrumentos.** `sim/maxwell2d.py` (`1db75ea7b0b8cba4`) **intocado**; `sim/control_pareado_convergente.py` sólo lectura (Ruta B del pre-registro); `sim/medidas_aN.csv` (`4129d436e2cd081d`) intocado.
4. **No re-mide E1/E2/E3.** Se citan **por slug** desde el pre-registro §0.3 y el crudo.
5. **No entra a `main.tex`** ni a `bundle/` (inmutable). La prohibición de este ciclo sigue en pie.
6. **No repara** la colisión `can[oó]nic` (§6.5 de la casa) ni las filas 9 y 11 de la tabla §3.
7. **No adjudica** la doble casa de `λ/40` — (A) constante sellada del FDTD `DX_OVER_LAMBDA = 1.0/40.0`, **no elegible**; (B) cadena analítica con `nodos` libre, **elegible** —: se **cita**; las seis cifras de `p` salen de (B).
8. **No promedia geometrías** ni elige una como representativa: se imprimen las tres.
9. **No adjudica la casa de §8.4** (§1: inferencia medida).

---

## §5 · RIESGO DECLARADO

- La casa (§1) es **inferencia por dos literales**, no adjudicación del dueño.
- La identidad de §3.2 **no es evidencia**; si alguien la cita como confirmación de la ley de composición, el error es de lectura, no del metro.
- `p` es **instrumento, no evidencia del artículo** (estante §9 del pre-registro).
- La errata de rótulo de §3.1 está **en el instrumento de lectura**, no en el crudo sellado.

---

## §6 · REPRODUCIR

```
export TZ=UTC
# 1) la corrida que produjo el crudo (NO se corrió en este ciclo)
python3 -B /Users/marlene/sfqed-paper/sim/driver_convergencia_p.py --nodos 61,121,241,481 --geometrias 3
# 2) la lectura derivada de esta adenda (cero escrituras, cero corridas)
python3 -B /tmp/lectura_derivada_8_4_20261013.py
```

---

`ORDEN-DE-ADJUNTOS-SELLADO-20261013` · cierre `2026-10-13T02:2xZ` · **cero escrituras fuera de este archivo**.
