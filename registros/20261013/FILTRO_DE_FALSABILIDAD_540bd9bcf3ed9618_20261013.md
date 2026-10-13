# FILTRO DE FALSABILIDAD — re-anclaje al objeto nuevo y cierre de O10c

Pieza NUEVA (append-only: `FILTRO_DE_FALSABILIDAD_ca7e8920abf8c55f_20261013.md` NO se toca).
Registro derivado de la corrida de crítica ciega sobre el manuscrito. 13-Oct-2026.

UNIVERSO DECLARADO: `registros/20261013/` · UNIDAD = archivo · VENTANA = esta corrida · hora por bloque.

---

## 0. Identidad del objeto nuevo y transición medida

- OBJETO: `/Users/marlene/sfqed-paper/main.tex`
  - AHORA: `sha256-16 = 540bd9bcf3ed9618` · `blob = e5705c84f0ff1c54744d02fe90e582059fc64019` · `wc -l = 742` · `B = 40017` · mtime 2026-10-13T09:23Z
  - Comando: `python3 -c 'hashlib.sha256(open("main.tex","rb").read())'` + `git hash-object -- main.tex` · T_UTC 2026-10-13T09:25:41Z
- TRANSICIÓN (causa medida, no adjudicada):

| paso | sha256-16 | líneas | bytes | blob | causa | mano |
|---|---|---|---|---|---|---|
| base de los crudos | `ca7e8920abf8c55f` | 652 | 34003 | — | congelado antes de las 5 corridas | otra |
| parche I1–I5 | `4f22c533ab36c94d55d7050b305cef62d140b35f` (=HEAD:main.tex) | 736 | 39650 | `4f22c533ab36c94d5…` | `ACTA_PARCHE_I1_I5_20261013.md` + huella `INTERSECCION-I1-I5-PARCHE-QUIRURGICO-20261013` en L15 | otra |
| inserción κ (esta orden) | `540bd9bcf3ed9618` | 742 | 40017 | `e5705c84f0ff1c54744d02fe90e582059fc64019` | huella `HUELLA-DESAMBIGUACION-KAPPA-Y-REANCLAJE-20261013` en L632 + 5 líneas de prosa (L633–637) | mía |

- Diferencial de la inserción κ, medido en el objeto: `git diff --numstat -- main.tex` = `6  0  main.tex` · `hunks = 1` ⇒ +6 líneas, 0 borrados, una sola región.
- Las cinco comprobaciones del contrato se reportaron ANTES de compilar (T_UTC 2026-10-13T09:22:11Z): `huella_pre_en_destino = 0` · `RC_GATE_PRE = 0` · `blob_disco = blob_HEAD = 4f22c533…` · `l = 736` · `B = 39650`; más el diff exacto `6 0 main.tex`, 1 hunk.
- Gate POST: `RC_GATE_POST = 11` («la huella ya habita en main.tex») ⇒ **cumplimiento pasivo**, no fallo.
  Control negativo (`HUELLA-QUE-NO-EXISTE-CONTROL`): `RC_CONTROL = 13` (`ESTADO SUCIO`) ⇒ muere en el bloque 4 porque el objeto está modificado contra HEAD ⇒ **no discrimina RC 11 de RC 13 y se DECLARA, no se adjudica**.
- DECLARADO (fail-closed por diseño): el gate **no puede autorizar una creación** — su primer bloque es `[ ! -f "$TARGET" ]` ⇒ RC 10; y un destino sin rastrear da RC 13. Esta pieza es una CREACIÓN ordenada: se declara explícitamente, no se gatea.
- Compilación: `tectonic -X compile main.tex` ⇒ `RC_TECTONIC = 0`, `errores = 0`. PDF `main.pdf` 180186 B · `sha256-16 = b4a0dcea15f9c327` (contra `179933 B` / `bd15e70f7d7e7142` en HEAD).
- MOTOR de páginas (único vivo en esta máquina): zlib sobre `FlateDecode`. Medido: **7 → 7 páginas** (PRE `HEAD:main.pdf` vs POST disco, mismo motor). Los otros tres motores están muertos/ausentes — `strings | grep /Type */Page` = **0** · `qpdf` **no instalado** · `mdls` **vacío** — se declaran como tales.
- Numeración: `label{eq:` = **18**, líneas sin cambio de orden: 71, 101, 138, 147, 153, 173, 184, 215, 235, 280, 287, 304, 311, 361, 512, 539, 548, 570. `\begin{equation}` = **19**. ⇒ **sin colisión de numeración**.

---

## 1. Re-anclaje de las 22 filas por huella literal en el objeto nuevo

MOTOR: búsqueda de subcadena literal en línea (unidad = línea, no ocurrencia); para frases largas se imprime el par **crudo / normalizado** (espacios colapsados) porque una frase puede dar 0 por estar partida por salto de línea. T_UTC 2026-10-13T09:26:05Z y 09:26:27Z.

| # | ancla literal | línea (objeto viejo 652 l) | línea (objeto nuevo 742 l) | remediada por | veredicto |
|---|---|---|---|---|---|
| O1 | `eq:Ecr` | 66 | **71** | — | REFUTADA |
| O1 | «the work performed over one reduced Compton wavelength…» | 69–72 | crudo **0** / normalizado **1** (partida por salto) | — | REFUTADA |
| O2 | `eq:invariants` / `eq:invariants2` | 93 / 129 | **101 / 138** | — | VÁLIDA-COMO-REDACCIÓN |
| O3 | `F_{\rho\sigma}` | 127–128 | **131** (1 línea) | — | REFUTADA |
| O4 | `eq:cp_fields` / `eq:cp_inv` | 279 / 287 | **304 / 311** | — | REFUTADA |
| O5 | «The assumptions are explicit» | 340 | **397** | — | REFUTADA |
| O5 | «a fixed, common focal volume» | 344 | **401** | — | REFUTADA |
| O6 | `kw_0` | 585–588 | **656, 657, 658, 659, 660** (5 líneas) | — | REFUTADA |
| O7 | `adiabat` | 600 | **671** (+55, 475) | **I1–I5 L194–197** (γ = 1/a_0 ≪ 1 explícito) | REFUTADA |
| O8 | «the concrete content of» | 390 | **449** | — | VÁLIDA-COMO-ALCANCE |
| O9 | «makes a sharp, falsifiable prediction» | 397 | **458** | — | VÁLIDA-COMO-PROGRAMA |
| O9 | «a purely analytic treatment gives way to computation» | 429–436 | crudo **0** / normalizado **1** | — | VÁLIDA-COMO-PROGRAMA |
| O9 | «survives those assumptions is a result» | 429–436 | **497** | — | VÁLIDA-COMO-PROGRAMA |
| O10a | `eq:ratio` | 448 | **512** (usos 553, 561, 610) | — | REFUTADA |
| O10b | mallas `\lambda/10`, `\lambda/20`, `\lambda/40` | 505–546 | **582 / 583 / 583, 596, 611** | — | REFUTADA |
| O10b | región `$6\lambda$` | 505–546 | **562** (+660) | — | REFUTADA |
| O10b | cintura `w_0=2\lambda` | 505–546 | **564** — ojo: el filtro la citó con espacios (`w_0 = 2\lambda`) ⇒ **n = 0**; el objeto la escribe sin espacios (n = 1) | — | REFUTADA |
| **O10c** | `kappa` (todas) | 562, 570 (**2**) | **11**: 350, 357, 358, 363, 385, 386, 389, **627, 634, 635, 641** | **inserción κ L632–637** | **VÁLIDA → CERRADA** (§2) |
| O11 | `back-reaction` | 405 | **466** (+706) | — | REFUTADA |
| O11 | `screening` | 0 | **0** (diferencia de vocabulario) | — | REFUTADA |
| O12 | `gradient` | 0 | **0** | **I1–I5 L198–202** | **VÁLIDA → remediada en el objeto** (§3) |
| R1 | (dual + duplicación) | 127–134 | **131 / 138** | — | REFUTADA en el dual · VÁLIDA en O2 |
| R2 | = O5 | 339–347 | **397–401** | — | REFUTADA |
| R3 | = O9 | — | **458–497** | — | VÁLIDA-COMO-PROGRAMA |
| R4 | autotestigo `895f424497caa97e` | 505–576 | **630** | — | REFUTADA |
| R5 | Lemma 1 + paraxial | 236–246 / 585–593 | **656–660** | — | REFUTADA |
| R6 | `beta` banda pre-registrada | 617–618 | **688, 689** | — | REFUTADA / COINCIDE con el objeto |
| T1 | `helic` | 380–384 | **442, 443** (+298) | — | VÁLIDA-COMO-REDACCIÓN |
| T2 | `eq:focus_cone` | 472 | **539** (usos 559) | — | VÁLIDA-COMO-REDACCIÓN |

**Tally sin cambio:** REFUTADAS 14 · VÁLIDA 2 · VÁLIDA-COMO-REDACCIÓN 3 · VÁLIDA-COMO-ALCANCE 1 · VÁLIDA-COMO-PROGRAMA 2.
**Hallazgos propios H1–H4:** anclas intactas — H1 `eq:focus_cone` L539 / `eq:ratio` L512 · H2 `eq:focus_cone` L539 vs `eq:cp_inv` L311 · H3 `helic` L442–443 · H4 L539.
Ninguna fila cambió de veredicto por el re-anclaje: cambió **la casa**, no la medida.

---

## 2. Cierre de la fila O10c (κ_bulk sin definir + colisión de namespace κ)

- HUELLA: `HUELLA-DESAMBIGUACION-KAPPA-Y-REANCLAJE-20261013` — escrita en el objeto en **L632** como comentario `% PATCH:` (precedente L15, invisible al tipografiado).
- Lo que el objeto **ya tenía** antes de la inserción: `\kappa_{\mathrm{bulk}} = 0.329479` con techo de aceptación `0.5` (L626–628), y la predicción refutada `\kappa_{\mathrm{bulk}} < 0.15` (L641).
- Lo que la inserción **escribe** (L633–637, verbatim): «Two symbols in this text share a name and nothing else: throughout the paper `\kappa` is the coefficient of the beam energy, `\mathcal{E}_b=\kappa\,E_b^{2}`, while `\kappa_{\mathrm{bulk}}` bounds the volumetric spectral contamination of the numerical integrator; no constitutive relation links the two.»
- Censo medido: `kappa` 2 → **11** líneas; `kappa_{\mathrm{bulk}}` = **3** líneas (627, 635, 641) ⇒ ahora **está definido en el texto**, no sólo usado.
- TERMINADO: la fila O10c pasa de **VÁLIDA** a **VÁLIDA-CERRADA-EN-EL-OBJETO**.
- NO se importó constante nueva y NO se inventó una segunda κ_bulk: la propuesta `κ_bulk ≡ (α/90π)(E/E_cr)²` fue **descartada por medición** — invertida contra el valor sellado da `(E/E_cr)² = 12766.0` ⇒ `E/E_cr = 113`, contra «local fields well below `E_{\mathrm{cr}}`» (L403). Lo que faltaba era **desambiguar el nombre**, no añadir una ecuación.

---

## 3. Estado del resto de lo que el filtro dejó en pie

| pieza | estado en el objeto nuevo (742 l) | casa |
|---|---|---|
| O12 adiabaticidad **espacial** | **remediada**: L198–202 declara la condición espacial con número, `k\lambda_{\mathrm{C}} = 2\pi\lambda_{\mathrm{C}}/\lambda \simeq 3.0\times10^{-6} \ll 1` para λ = 800 nm | L198–202 (mano ajena, I1–I5) |
| O7 γ / LCFA | **remediada**: L194–197 da γ ≡ ω/(ω_C a_0) = m_eω/(eE) = 1/a_0 ≪ 1 | L194–197 (mano ajena, I1–I5) |
| H1 R no reproducible desde la forma cerrada | **abierta** | `eq:focus_cone` L539 · `eq:ratio` L512 |
| H2 1/N y quiescencia nunca juntas | **abierta** | L539 vs L311 |
| O8 frontera descriptiva | **abierta** (alcance, no error) | L449 |
| O9 / R3 programa numérico | **abierta** (ya concedida por el objeto) | L458–497 |
| O2 / H3 / H4 redacción | **abiertas** (duplicación F/G; helicidad; «at the focus») | 101/138 · 442–443 · 539 |
| F1–F4 (falsadores pre-registrados) | **no disparados en esta orden** | — |

---

## 4. Material crudo NO filtrable (sin cambio)

- `deepseek-v4-pro` (05:52:58): 200, `finish_reason=length`, contenido **0 B**, razonamiento 25501 B ⇒ NO ENTREGADA. Sus apartados 14 y 16 coinciden con H3 y H4.
- `kimi-k3` t=1.0 (05:58:11): 200, `length`, contenido **0 B**, razonamiento 45532 B ⇒ NO ENTREGADA. Su apartado 2 apunta a la Ec. 9 = `eq:variational`, que no tiene helicidad ⇒ referencia no direccionable.
- Fallos duros por contrato del proveedor, no por el objeto: 401 (llave inválida), 402 (crédito insuficiente), 400 (`kimi-k3` sólo admite temperatura 1).
- El defecto del metro del crítico (sus citas ≥ 8 saltan cuatro ecuaciones numeradas) **no se repara aquí**: las valoraciones siguen re-ancladas **por contenido**.

---

## 5. Cierre

- Objeto nuevo: `540bd9bcf3ed9618` · `e5705c84f0ff1c54744d02fe90e582059fc64019` · 742 l · 40017 B · PDF 180186 B / `b4a0dcea15f9c327` · 7 páginas (antes 7) · 18 `label{eq:` sin reordenar.
- Cero escrituras sobre el manuscrito en esta pieza. Cero re-disparo del instrumento. Ninguna llave impresa. Cero constantes importadas.
- La pieza previa `FILTRO_DE_FALSABILIDAD_ca7e8920abf8c55f_20261013.md` **queda intacta** (append-only); ésta la sucede por identidad de objeto, no la edita.
- Identidad del destino de ESTE archivo (bytes, líneas, sha256-16, blob) se reporta en el cierre del turno, no dentro del propio archivo — una identidad impresa dentro de la pieza describe su versión anterior.
