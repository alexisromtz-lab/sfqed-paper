# FILTRO DE FALSABILIDAD — objeción → objeto → metro → falsador → veredicto

Registro derivado de la corrida de crítica ciega sobre el manuscrito. 13-Oct-2026.
Este archivo NO edita el manuscrito ni re-dispara el instrumento: los crudos ya existen.

---

## 0. Identidad, procedencia y unidades

- OBJETO: `/Users/marlene/sfqed-paper/main.tex`
  - `sha256-16 = ca7e8920abf8c55f` · 34003 B · `wc -l = 652` · `count(nl)+1 = 653` · mtime 2026-10-12T05:07:24Z
  - Congelado ANTES de las corridas: los cinco crudos declaran `OBJETO_SHA256_16=ca7e8920abf8c55f`, `OBJETO_LINEAS=652`, `OBJETO_BYTES=34003`.
  - El par 652/653 NO es mutación: es unidad del metro (`wc -l` no cuenta la última línea sin salto vs `count(nl)+1`). Bytes idénticos ⇒ identidad intacta.
- MOTOR del crítico: `/Users/marlene/platino-labs/tools/critica_ciega.py` (205 l · 7974 B · mtime 2026-10-13T06:52 — POSTERIOR a las cinco corridas; se declara, no se adjudica).
- CRUDO: `/Users/marlene/sfqed-paper/registros/20261013/`
  - UNIVERSO DECLARADO: 11 archivos (6 `.json` + 5 `.txt`) = 5 corridas. UNIDAD = archivo.
- VENTANA: reloj UTC impreso en la cabecera de cada crudo.
- Cero escrituras sobre el manuscrito. Cero re-disparo. Ninguna llave impresa.
- Destino de este archivo: `registros/20261013/` (medido: NO ignorado por git; el directorio está sin rastrear ⇒ `?? registros/20261013/`).

### Comandos que respaldan las cifras de este archivo (metros)

    M1 mapa de ecuaciones:  python3 -c 'contar \begin{equation} en orden y extraer \label'
       ⇒ 19 `\begin{equation}` · 0 `align` · 0 `gather` · 0 `equation*` · 0 `\[`
    M2 censo literal por línea:  python3 -c 'listar líneas que contienen cada término'
       ⇒ unidad = línea (no ocurrencia)
    M3 invariantes temporales:  script numpy, 1000 muestras por periodo, E0=1, w=1,
       triad(k) = (k̂, ê1 = (−k_y,k_x,0)/|·|, ê2 = k̂ × ê1), E_j = E0(cosψ ê1 + s sinψ ê2),
       B_j = k̂ × E_j,  F = ½(E²−B²), G = E·B, a = sqrt(sqrt(F²+G²)+F)
    M4 gate de pre-vuelo:  tools/gate_pre_escritura.sh ⇒ RC 10 (objeto inexistente: el gate valida objetos existentes)

---

## 1. Qué entregó cada corrida (una corrida sin contenido no entregó objeción)

| base | T_UTC | proveedor/modelo | HTTP | finish | contenido | veredicto |
|---|---|---|---|---|---|---|
| `..._20261013T054927Z` | 05:49:27 | deepseek / deepseek-chat | **401** | — | — | NO ENTREGADA (llave `****cd46` inválida) |
| `..._20261013T055026Z_dsv4pro` | 05:52:58 | openrouter / deepseek-v4-pro | 200 | **length** | **0 B** | NO ENTREGADA (razonamiento truncado: 25501 B, 16 apartados) |
| `..._20261013T055314Z_dsv4pro-b` | 05:53:14 | openrouter / deepseek-v4-pro | **402** | — | — | NO ENTREGADA (crédito insuficiente) |
| `..._20261013T055324Z_dsv32` | 05:54:22 | openrouter / deepseek-v3.2 | 200 | **stop** | **10781 B** (txt 12114 B, sha16 `9908e731103e54f9`) | **ÚNICA ENTREGADA** |
| `..._20261013T055427Z_kimik3` | 05:54:27 | moonshot / kimi-k3 | **400** | — | — | NO ENTREGADA (sólo admite temperatura 1) |
| `..._20261013T055435Z_kimik3-t1` | 05:58:11 | moonshot / kimi-k3 | 200 | **length** | **0 B** | NO ENTREGADA (razonamiento truncado: 45532 B, 6 apartados) |

⇒ **1 de 5 corridas entregó respuesta.** Las dos truncadas dejaron razonamiento (material crudo), no dictamen.

---

## 2. Defecto del metro del crítico: sus referencias de ecuación no son direccionables

Mapa medido (M1), etiquetas del propio objeto:

| Ec. | Línea | etiqueta | | Ec. | Línea | etiqueta |
|---|---|---|---|---|---|---|
| 1 | 66 | `eq:Ecr` | | 11 | 263 | `eq:lin_inv` |
| 2 | 93 | `eq:invariants` | | 12 | 279 | `eq:cp_fields` |
| 3 | 129 | `eq:invariants2` | | 13 | 287 | `eq:cp_inv` |
| 4 | 140 | `eq:ab` | | 14 | 318 | `eq:oneoverN` |
| 5 | 147 | `eq:abrel` | | 15 | 448 | `eq:ratio` |
| 6 | 165 | `eq:EH` | | 16 | 472 | `eq:focus_cone` |
| 7 | 176 | `eq:schwinger_rate` | | 17 | 484 | `eq:focus_a` |
| 8 | 189 | `eq:yield` | | 18 | 500 | `eq:Rcone` |
| 9 | 206 | `eq:variational` | | 19 | 636 | (sin etiqueta, apéndice) |
| 10 | 256 | `eq:lin_fields` | | | | |

Re-anclaje de cada referencia del crudo ganador (`dsv32`):

| el crudo dice | contenido que nombra | objeto real |
|---|---|---|
| «Ec. (4) = tensor dual, sin bajar índices» | tensor dual | está **en línea, sin número**, L127–128; la Ec. 4 es `eq:ab` |
| «Ec. (8): E,B con `cos ωt, sin ωt`» | campos circulares | **Ec. 12** `eq:cp_fields` |
| «Ec. (10): el 1/N» | escalado 1/N | **Ec. 14** `eq:oneoverN` |
| «Ec. (11): la métrica R» | R | **Ec. 15** `eq:ratio` |
| «Ec. (7): LCFA» | tasa de Schwinger | **Ec. 7** `eq:schwinger_rate` ✔ |

**Offset medido:** las cuatro ecuaciones que `dsv32` salta son Ecs. 8, 9, 10, 11 = `eq:yield`, `eq:variational`, `eq:lin_fields`, `eq:lin_inv` — exactamente las que caen entre la Ec. 7 (que sí cuenta) y la Ec. 12 (que llama 8).
⇒ Ninguna de sus referencias ≥ 8 se puede adjudicar por su número. Cada objeción de abajo se re-ancló **por contenido**, no por la cita.

---

## 3. Filtro: las 22 filas de `dsv32` (12 objeciones + 6 recomendaciones + 2 del truncado v4-pro)

| # | objeción (crudo) | objeto (Ec./línea) | metro (medición) | falsador | veredicto |
|---|---|---|---|---|---|
| O1 | Ec. 1 es re-enunciado tautológico | `eq:Ecr` L66 + L69–72 | L69–72: «the work performed over one reduced Compton wavelength equals the rest energy of an electron–positron pair»; la regla #2 del encabezado es sobre constantes importadas, no sobre derivaciones | mostrar una Ec. 1 sin criterio físico | **REFUTADA** |
| O2 | Ecs. (3)/(4) redundantes | Ec. 2 L93–97 y Ec. 3 L129–134 | M2: el par (F,G) se define **dos veces** en dos ecuaciones numeradas (componentes y forma covariante) | mostrar que son objetos distintos | **VÁLIDA-COMO-REDACCIÓN** (duplicación medida; no es error físico) |
| O3 | Ec. (4) no coincide con el tensor dual; falta bajar índices | L127–128 | M2 (`F_{\rho\sigma}`): 2 líneas [127,128] — los índices **ya están bajados**; `index` = 0 líneas | mostrar la Ec. que sí falla | **REFUTADA** |
| O4 | Sec. 3.2(b) llama «quiescente» a campos dependientes del tiempo | Ec. 12 L279, Ec. 13 L287, L303, L357 | M3: F ≡ 2.000000 (oscilación 8.9e−16) y a ≡ 2.000000 (2.2e−16) sobre 1000 muestras en kz=0 ⇒ F y a **sí** son estacionarias; el objeto nunca afirma que E,B lo sean | exhibir una Ec. 13 con F dependiente del tiempo | **REFUTADA** |
| O5 | Ec. (10) esconde el límite no declarado del volumen focal | L339–347 | L340 «The assumptions are explicit and each is falsifiable»; (iii) L344 «a fixed, common focal volume Σ×τ»; (ii) phase matching | mostrar que (i)–(iv) no cubren el volumen | **REFUTADA** |
| O6 | el caveat de Lemma 1 se despacha con «transversality-preserving fields» | L585–593 | M2 (`kw_0`): 5 líneas [585–588]; E_z ~ E_⊥/(k w_0), corrección `(k w_0)^{-2}` = 6.3e−3 (w_0 = 2λ, k w_0 ≃ 12.6); f/1 declarado **fuera del régimen** | mostrar la corrección ausente | **REFUTADA** |
| O7 | validez de la LCFA no justificada; estimar γ | párrafo Adiabaticity, L600–613 | M2: `adiabat` 4 líneas [52,305,414,600]; `a_0` 4 líneas [603,604,607,612]; γ = m_eω/(eE) explícito, a_0 de 1.7e2 a 6.8e2 ⇒ γ de 5.9e−3 a 1.5e−3 | mostrar γ ausente | **REFUTADA** |
| O8 | Sec. 3.4: condiciones de frontera descriptivas, no derivadas | L376–390 | L390 «These conditions are the concrete content of “boundary-condition geometry”»: se presentan como especificación | mostrar que el objeto las llama derivadas | **VÁLIDA-COMO-ALCANCE** |
| O9 | «quiescent preferable» exige integrar numéricamente la Ec. 7 | L393–397, L429–436 | L397 «makes a sharp, falsifiable prediction»; L429–436 «a purely analytic treatment gives way to computation» + «a claim that survives those assumptions is a result» | mostrar una afirmación numérica sin declarar | **VÁLIDA-COMO-PROGRAMA** |
| O10a | la métrica R es no estándar | Ec. 15 L448 + Ec. 3 | L460: R se anula con F=G=0 (Lemma 1) y `0≤R≤1` por Cauchy–Schwarz | mostrar R fuera de [0,1] | **REFUTADA** |
| O10b | los números del benchmark no traen contexto de método | L505–546 | mallas λ/10, λ/20, λ/40; región cúbica 6λ; cintura w_0 = 2λ; error de interpolación de B 0.7442→0.7740 = 3.8 % | mostrar una cifra sin malla ni región | **REFUTADA** |
| O10c | el párrafo de κ_bulk y de la predicción refutada es críptico | L562, L570 | M2 (`kappa`): **2** apariciones [562,570] y **ninguna definición** en el manuscrito; además κ ya está tomado por otro objeto (ε_b = κ E_b², Ecs. 14, L316/323/324/329) ⇒ **colisión de namespace** | mostrar dónde se define κ_bulk | **VÁLIDA** |
| O11 | back-reaction/screening acota N (límite no declarado) | L403–406 | M2: `back-reaction` 1 línea [405] («because back-reaction from the…»), declarado como falsador del escalado; `screening` = 0 líneas (diferencia de vocabulario, no de contenido) | mostrar que el límite no se declara | **REFUTADA** |
| O12 | adiabaticidad **espacial** (campo constante sobre λ_C) no declarada | L600–613 vs L71 | M2: `gradient` = 0 líneas; única mención de Compton L71 = definición de E_cr en la Introducción; el párrafo de adiabaticidad sólo trata la variación **temporal** (γ) | medir `(\|∇a\|/a)·λ_C` sobre la configuración del cono y hallarlo ≪ 1 (entonces el límite es inocuo) | **VÁLIDA** (límite ausente) |
| R1 | consolidar F/G y arreglar el tensor dual | L127–134 | el dual no tiene defecto (O3); la consolidación sí (O2) | — | **REFUTADA** en el dual · **VÁLIDA** en la duplicación (O2) |
| R2 | declarar todas las suposiciones del 1/N | L339–347 | = O5 | — | **REFUTADA** |
| R3 | probar o suavizar «preferable» | = O9 | = O9 | — | **VÁLIDA-COMO-PROGRAMA** |
| R4 | reescribir **o eliminar** el benchmark | L505–576 | autotestigo con pre-registro (`895f424497caa97e`), techo fijado antes de la corrida, y una predicción refutada registrada como refutada | mostrar que la sección no se audita a sí misma | **REFUTADA** en su forma fuerte (lo que falta es O10c y H1) |
| R5 | discutir los dos límites (onda plana / paraxial) | Lemma 1 L236–246 + L585–593 | ambos declarados con su orden de magnitud | — | **REFUTADA** |
| R6 | añadir falsabilidad (simular N=2,4,8 a energía total fija, ajustar N^β) | L393, L615–620 | M2: `beta` [617,618] ⇒ banda **pre-registrada** `0.45 ≤ β ≤ 0.55`, abandonada en `σ_φ* ≃ 0.55 rad` (0.09 de periodo óptico, 0.24 fs a 800 nm) | — | **REFUTADA / COINCIDE con el objeto** |
| T1 | (v4-pro #14) «todas las hélices iguales… eso es incorrecto» | L380–384 | M3: el flip da F oscilante (osc_F = 4.000e+00) pero **G ≠ 0** (hasta 2 con E0=1), mientras el caso lineal tiene G ≡ 0 **exacto** | mostrar G ≡ 0 para el par contra-rotante | **VÁLIDA-COMO-REDACCIÓN** (la afirmación de fondo es verdadera; la identificación con el caso lineal no) |
| T2 | (v4-pro #16) la Ec. 15 (longitudinal uniforme) viola Maxwell | Ec. 16 L472–481 | M3: en x=0 las transversales se anulan (max\|Ex\|, \|Ey\| ≤ 3.3e−16) y max\|Ez\| = N sinα E₀ **exacto** ⇒ la Ec. es el **valor en el foco**, no un campo de todo el espacio | exhibir la Ec. como solución en una región | **VÁLIDA-COMO-REDACCIÓN** (debe declararse «at the focus») |

**Tally de las 22 filas:** REFUTADAS 14 · VÁLIDA 2 (O10c, O12) · VÁLIDA-COMO-REDACCIÓN 3 (O2, T1, T2) · VÁLIDA-COMO-ALCANCE 1 (O8) · VÁLIDA-COMO-PROGRAMA 2 (O9, R3).

---

## 4. Hallazgos del filtro (medidos aquí; no los levantó el crítico)

**H1 — VÁLIDA (hueco de reproducibilidad).** `eq:focus_cone` (Ec. 16, L472–481) es el **valor en el foco**: uniforme en el espacio, sin vectores de onda. Medido (M3): en x=0 las componentes transversales se anulan hasta 3.3e−16 y `max|Ez| = N sinα E₀` **exacto** (N=4, α=26.5651°, E₀=1: 1.788854 vs 1.788854). Pero `R = 0.7125 / 0.7772` (Ec. 18, L500) se obtiene **barriendo una región cúbica de lado 6λ**, y el manuscrito **no escribe** el campo fuera del foco (sólo dice que las componentes longitudinales de-fasan). ⇒ La forma cerrada impresa no alcanza para producir la cifra que se reporta.
*Falsador F1:* escribir la superposición espacial completa y recomputar R; si reproduce 0.7125/0.7772 dentro del piso declarado (2.5 %), H1 cae.

**H2 — observación de alcance (medida).** La configuración del cono **no es quiescente**: medido (M3), F oscila con amplitud 3.2 (N=4, α=26.5651°, E₀=1) ⇒ F oscila a 2ω. La geometría que carga el escalado 1/N (cono, `eq:focus_cone`) es **oscilatoria**; la configuración argumentada como óptima (dos haces circulares co-rotantes, `eq:cp_inv`) es **estacionaria pero N=2**. El manuscrito nunca exhibe **una** configuración que sea las dos cosas.
*Falsador F3:* exhibir una familia de N haces con F estacionaria en el tiempo y E_f = N sinα E₀.

**H3 — VÁLIDA-COMO-REDACCIÓN.** La frase de la helicidad (L380–384) es inexacta **en la invariante**: medido (M3), el par contra-rotante tiene G oscilante (|G| hasta 2 con E₀=1) mientras el caso lineal tiene G ≡ 0 exacto (0.000000 en 1000 muestras). La parte falsable de la frase («destruye la independencia temporal de F») es **verdadera** (osc_F = 4.000e+00); lo falso es la identificación «hacia el caso lineal»: el flip cae en una tercera clase (F y G ambos oscilantes).
*Falsador F4:* mostrar G ≡ 0 para el par contra-rotante.

**H4 — VÁLIDA-COMO-REDACCIÓN.** La Ec. 16 tal como está impresa no es solución de Maxwell sin fuentes en una región: E uniforme y longitudinal con ∂B/∂t ≠ 0 mientras ∇×E = 0. Medido (M3): la cancelación transversal ocurre **sólo en el punto focal**. Debe declararse como valor en el foco.

---

## 5. Material crudo NO filtrable

- `deepseek-v4-pro` (05:52:58): 200, `finish_reason=length`, contenido **0 B**, razonamiento 25501 B / 47 l / 16 apartados ⇒ **NO ENTREGADA**. Sus apartados 14 y 16 coinciden con H3 y H4; el resto es un barrido de Ecs. 1–15 sin conclusión.
- `kimi-k3` t=1.0 (05:58:11): 200, `length`, contenido **0 B**, razonamiento 45532 B / 127 l / 6 apartados ⇒ **NO ENTREGADA**. Su apartado 2 («la helicidad está al revés respecto de la Ec. (9)») apunta a la Ec. 9 = `eq:variational`, que no tiene helicidad ⇒ referencia no direccionable.
- Tres fallos duros por contrato del proveedor, no por el objeto: 401 (llave deepseek inválida), 402 (crédito insuficiente para 32000 tokens), 400 (`kimi-k3` sólo admite temperatura 1).

---

## 6. Cierre

- Entraron al filtro 22 filas del crudo (20 de `dsv32` + 2 del truncado de v4-pro) y salieron 4 hallazgos propios (H1–H4).
- Lo que el filtro deja en pie: **O10c** (κ_bulk sin definir + colisión de namespace κ), **O12** (adiabaticidad espacial sobre λ_C ausente), **H1** (R no reproducible desde la forma cerrada), **H2** (1/N y quiescencia nunca juntas), **O8** (frontera descriptiva), **O9/R3** (programa numérico ya concedido), **O2/H3/H4** (redacción).
- Lo que el filtro descarta: 14 objeciones refutadas por el objeto congelado (incluidas las dos que el crudo presentaba como errores de álgebra: el tensor dual **ya** trae índices bajados y el volumen focal fijo **ya** está declarado, y la falsabilidad que el crudo recomienda **añadir** ya existe con banda pre-registrada).
- Defecto del metro del crítico, medido: sus referencias de ecuación saltan cuatro ecuaciones numeradas ⇒ sus citas ≥ 8 no son direccionables; las valoraciones se re-anclaron por contenido.
- Cero escrituras sobre el manuscrito. Cero re-disparo del instrumento. Ninguna llave impresa.

*Artefactos de identidad del destino:* `sha256-16`, `git hash-object`, bytes, líneas y mtime se reportan en el cierre del turno, no dentro del propio archivo.
