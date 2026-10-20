# METHODOLOGY_AND_BOUNDARIES — el método de medida y la frontera declarada

<!-- HUELLA-METHODOLOGY-BOUNDARIES-20261020 -->

> **EN —** How this paper is measured, by which instrument, and what the apparatus **cannot**
> certify. Every count below was re-measured on 2026-10-20 and travels with the command that
> produced it. Where this repository declares something that measurement no longer supports,
> the drift is **written down**, not rewritten away.

Este documento **no** describe la física: describe **cómo se mide lo que este repositorio
afirma, y hasta dónde puede medirlo**. Es la pieza que `INDEX.md` §1 declaraba como
`METHODOLOGY_AND_BOUNDARIES.md` (15 393 B) y que hasta hoy respondía `404`.

Un documento de método que no declara su propia frontera es una segunda capa de narrativa.
Por eso esta pieza termina con lo que **no** afirma (§8) y con cómo refutarla (§11).

---

## §0 · Ventana, motor, unidad

```
T_UTC   2026-10-20T23:04Z–23:10Z  ·  UNIVERSO: clon limpio de `main` @ d2299b9  ·  LECTURA
MOTOR   M0 = Darwin 25.5.0 · shasum -a 256 | cmp | grep -F | python3 -B | git   (nix AUSENTE)
UNIDAD  archivo (inventario) | línea (anclas) | byte (custodia) | caso (banco)
```

Toda cifra de este documento caduca al escribirse. No se presentan como estado permanente:
se presentan como **medición con ventana**, igual que las del `INDEX.md`.

---

## §1 · Qué mide este repositorio, y con qué

| instrumento | objeto que mide | comando | resultado medido (ventana §0) |
|---|---|---|---|
| `bundle/verificar.sh` | el aparato entero, en 4 etapas | `sh bundle/verificar.sh` | `VEREDICTO: VERDE PARCIAL · RC=0 · 51 verde / 0 rojo / 2 no medido · anclas 38 ok=38` |
| `bundle/tests/bench_must_fail.sh` | **al propio verificador**, desde fuera | `sh bundle/tests/bench_must_fail.sh` | `casos=7 · conformes=7 · rojos=0` |
| `bundle/HASHES.sha256` | identidad byte a byte del bundle | `shasum -a 256 -c HASHES.sha256` (dentro de `bundle/`) | `34 entradas · 34 OK · 0 FAILED · 0 huérfanos` |
| `bundle/instrumentos/telemetria_minima.py` | a sí mismo, con casos must-fail | etapa `[1]` del gate | `válidos 3/3 · malformados 10/10 · archivo vacío rc=2` |
| `tools/sello.sh` | el estado vivo en una línea | `sh tools/sello.sh` | `VEREDICTO · RC · MOTOR · SHA16 0ce97cf9d8c44987` + crudo a `corridas/` |
| `lint_tex.py` | **estructura** del manuscrito (no su contenido) | `python3 -B lint_tex.py` | `RC=0 · ROJOS: NINGUNO` (tras la corrección de §7) |
| `.github/ci.yml` + `.github/ci-apparatus` | el aparato en un runner desnudo | GitHub Actions | run `39508276952` @ `d2299b9`: **success** (banco 7/7) |

Dos cosas que esta tabla dice y conviene no leer de más:

1. **El banco no se invoca desde el gate.** Es deliberado y está escrito en la cabecera de
   `verificar.sh`: *«un verificador no se valida a sí mismo; el banco lo mide desde afuera»*.
2. **`lint_tex.py` mide forma, no verdad.** Cuenta entornos, llaves, dólares, labels, citas y
   meta-lenguaje. No evalúa si una ecuación es correcta. Un `RC=0` suyo significa «el TeX está
   estructuralmente sano», nunca «la física está bien».

---

## §2 · El método: tres valores, y un cuarto estado

El veredicto es **tricotómico** y cada valor tiene consecuencia distinta:

| RC | valor | significado | qué NO significa |
|---|---|---|---|
| `0` | **VERDE** (o VERDE PARCIAL) | lo medido pasó | que todo se haya medido |
| `1` | **FRACTURA** | el objeto no cumple su propio contrato | que el metro esté roto |
| `2` | **CONTRATO ROTO** | el metro no pudo leer | que el objeto esté mal |

`RC=2` existe porque un verificador que solo sabe decir «bien» o «mal» es ciego a su propia
ceguera. El caso canónico está medido en el banco (caso **B**): un manifiesto de **0 bytes** se
satisface solo, porque `0 + 0 == 0`. Sin la rama `2`, ese vacío habría salido **verde**.

**El cuarto estado es `NO MEDIDO`, y no es verde.** El gate lo imprime en el veredicto y lo
repite como sentencia:

```
2 bloque(s) NO MEDIDO(s):
  lo que no se midio no se declara verde. Verde de lo medido, y se dice cual.
```

Hoy esos dos bloques son concretos y están en §5: en un clon recién hecho **no existen**
`.git/hooks/pre-commit` ni `.git/hooks/pre-push`, así que la custodia se mide por **identidad
de las piezas** (5 piezas OK, 3 comparaciones `idéntico`) pero **no por enganche**.

---

## §3 · El banco must-fail: los 7 casos

El banco **fabrica su propio defecto** sobre una copia efímera del bundle completo y exige el
código de salida **estricto** (no «distinto de cero»: el que corresponde). Medido:

| caso | defecto inyectado | RC esperado | RC medido | causa impresa |
|---|---|---|---|---|
| **A** | un byte invertido en `00_INDICE.md:10`, tamaño conservado (27 017 B) | `1` | `1` | `[FAILED]` |
| **B** | manifiesto reducido a **0 bytes** | `2` | `2` | `[MANIFIESTO]` |
| **C** | *shim* con 17 herramientas y **sin `shasum`** | `2` | `2` | `[shasum ausente]` |
| **D** | medidor retirado: `instrumentos/telemetria_minima.py` | `2` | `2` | `[falta instrumentos/telemetria_minima.py]` |
| **E** | ancla viva movida: `actas/AUDITORIA…:69 [0.500000]` (38 filas) | `1` | `1` | `[ya no dice]` |
| **F** | *sandbox* sin `.git` — la custodia no es auditable | `0` | `0` | `[PARCIAL]` |
| **G** | *shim* con 17 herramientas y **sin `gitleaks`** | `2` | `2` | `[gitleaks ausente]` |

El caso **F** es el más instructivo y el más fácil de malinterpretar: sale `0` **porque la
custodia no se pudo medir**, y el veredicto lo dice con la palabra `PARCIAL`. Es un verde que
**nombra su propio agujero**: exactamente lo contrario de un verde silencioso. Si el mismo
escenario devolviera `VERDE` a secas, el banco estaría midiendo mal y el caso F dejaría de ser
un control.

---

## §4 · Vocabulario de las cifras

- **`sha16`** — los primeros 16 hex de un `sha256`. Sirve para citar un objeto sin copiarlo.
- **`UNIVERSO DECLARADO`** — qué entró en la cuenta, escrito antes de contar. Cambiarlo cambia
  el resultado sin cambiar el objeto.
- **`ventana`** — el `T_UTC` en que la cifra era verdad. Un conteo sin ventana es una opinión.
- **`no circular`** — el manifiesto **no puede declararse a sí mismo**. El gate lo verifica:
  `cobertura completa (35 = 34 declarados + el propio manifiesto)`.

Inventario medido de la ventana §0 (`git ls-files`, 114 archivos rastreados):

| zona | archivos | qué es |
|---|---|---|
| `bundle/` | 35 | el aparato: `actas/` 15 · `instrumentos/` 11 · `preregistros/` 3 · `evidencia/` 2 · `tests/` 1 · `verificar.sh` 1 · `HASHES.sha256` 1 · `00_INDICE.md` 1 |
| `sim/` | 47 | el laboratorio: `data/` 5 · `reproducibilidad/` 4 · el resto en la raíz de `sim/` |
| raíz | 14 | `main.tex`, `main.pdf`, `refs.bib`, `lint_tex.py`, `flake.nix`, `MOTORES.md`, `INDEX.md`, `README.md`, `LICENSE`, `AGENTS.md`, `BUNDLE_VERIFICATION_REPORT_20261011.md`, `ZENODO_DEPOSITO_CAMPOS_20261010.md`, `.gitleaks.toml`, `.gitignore` |
| otros | 18 | `figures/` 4 · `registros/` 3 · `scripts/` 3 · `corridas/` 2 · `marco-fibrado-20261011/` 2 · `.github/` 2 · `tools/` 2 |

---

## §5 · Frontera declarada: lo que **no** está sellado

Ocho puntos. Ninguno es un detalle: son el borde del trabajo.

| # | frontera | estado medido (ventana §0) | por qué no se «arregla» aquí |
|---|---|---|---|
| 1 | `flake.lock` **ausente**; `nix` **ausente** en el anfitrión | `flake.nix` escrito y **no evaluado** (`MOTORES.md` §6) | el pin no se puede cerrar desde una máquina sin `nix`; se declara abierto |
| 2 | enganche de hooks | `NO MEDIDO: el anfitrion no tiene .git/hooks/pre-commit` · idem `pre-push` · `core.hooksPath: SIN DECLARAR` | en un clon recién hecho no hay hooks instalados; la custodia se mide por **identidad** de las 5 piezas, no por enganche |
| 3 | `gitleaks` en CI | ausente en el runner desnudo → `verificar.sh` devolvería `RC=2 [CONTRATO ROTO: binario gitleaks ausente]` | por eso el aparato declarado en CI es **el banco**; el gate se mide donde el binario existe (local, `8.30.1`, `sha16 f414bc2fb952be6c`) |
| 4 | `sim/lector_invariantes.py` | `RC=2`, causa **sin diagnosticar** (`MOTORES.md` §6) | diagnosticarlo exige el corpus de modos completo, fuera de esta ventana |
| 5 | crudo **pre-fix** del banco | no se conservó | esa cifra no se puede volver a medir; no se reconstruye |
| 6 | **contenido** del manuscrito | `lint_tex.py` mide estructura: `entornos 29/29 · llaves 584/584 · dólares 586 · labels 24 / refs 23 · citas 10 / bib 10` | un conteo balanceado no es una demostración; la revisión física es otra pieza |
| 7 | depósito Zenodo | campos declarados en `ZENODO_DEPOSITO_CAMPOS_20261010.md`; el `tar.gz` declarado (340 248 B) sigue `404` | el depósito no se verifica desde el repositorio; el tarball ausente **se declara**, no se regenera por conveniencia |
| 8 | `bundle` en disco vs `HEAD` | `MOTORES.md` §6 (2026-10-11) declaró ` M` en 5 piezas. **Medido hoy en clon limpio: `34/34 OK`, `0 huérfanos`** | la deriva de aquella ventana **no aplica a `HEAD` hoy**; se anota el cambio de estado, no se borra el acta |

El punto 8 merece énfasis: una frontera puede **cerrarse sola** con el tiempo, y la forma
correcta de decirlo es una fila nueva con su ventana — nunca editando el acta que decía lo
contrario.

---

## §6 · Deuda de punteros: las piezas declaradas que no existen

`INDEX.md` §1 declaró tres piezas con tamaño. Re-medidas hoy por HTTP anónimo sobre `main`:

| pieza declarada | tamaño declarado | estado hoy (2026-10-20) | qué se hizo |
|---|---|---|---|
| `README.md` | 12 473 B | `200` · 98 l · 5 695 B | existe un README **nuevo**; **no** es la pieza declarada — aquel texto describía qué declara y qué no el trabajo, y se perdió. **Declarado** |
| `METHODOLOGY_AND_BOUNDARIES.md` | 15 393 B | `404` → **este documento** | se escribe ahora, con su identidad real (§9). **No** se rellenó hasta 15 393 B: esa cifra era de una pieza que nunca existió en el árbol |
| `sfqed-paper-zenodo-20261010.tar.gz` | 340 248 B | `404` | **no se regenera**: un tarball fabricado no es el depósito |

### Cuentas que envejecieron (drift declarado, no corregido en su fuente)

| pieza que lo afirma | cifra declarada | medido §0 | nota |
|---|---|---|---|
| `README.md` | «26 archivos = 25 declarados» | **35 archivos = 34 declarados + manifiesto** | el universo del bundle creció; el gate imprime el conteo vivo |
| `README.md` | «`actas/` 10 piezas» | **15** | |
| `README.md` | «`sim/` 110 archivos» | **47** | |
| `INDEX.md` §1 | `main.tex` 514 l | **742 l** | la fila ya marcaba ` M` («otra mano») |
| `INDEX.md` §2 | `00_INDICE.md` 179 l · `verificar.sh` 292 l | **326 l** · **398 l** | |

Estas filas **no** se reescriben aquí: `README.md` e `INDEX.md` son piezas de otra mano y su
ventana es 2026-10-11. Se declaran, que es lo que este documento existe para hacer. Lo que sí
se corrige en ellos (§9) es lo mínimo para que no señalen a un hueco que ya está lleno.

---

## §7 · Un defecto del linter del manuscrito, medido y corregido

`lint_tex.py` es el instrumento que dice si el `.tex` está estructuralmente sano. Medido hoy,
tenía **dos** defectos, y el segundo hacía inútil al primero:

**(1) Su rojo no viajaba.** Con `ROJOS: 1` el proceso salía **`RC=0`**. El veredicto se
imprimía y no se propagaba: nada podía enrojecer con él. Peor: `lint_tex.py` **no está
invocado** desde `verificar.sh`, ni desde `tools/sello.sh`, ni desde `.github/workflows/ci.yml`
(medido por `grep`), así que ese rojo no vivía en ninguna parte.

**(2) Su regla de meta-lenguaje contaba subcadenas.** La regla `meta` incluye la palabra
`gate`, y `low.count("gate")` contaba el **`gate` de `aggregate`** — `main.tex:604`,
*«aggregate quantity»*, prosa legítima. Resultado: un **rojo fabricado** sobre un texto limpio.
Es la misma familia del `grep` que se cuenta a sí mismo.

Corrección (2 ediciones, cero bytes de la física tocados):

| qué | antes | después |
|---|---|---|
| conteo | `low.count(w.lower())` | frontera: `(?<![a-z0-9_])palabra(?![a-z0-9_])` |
| salida | termina tras imprimir | `raise SystemExit(1 if rojos else 0)` |

Controles medidos, en este orden:

| control | entrada | esperado | medido |
|---|---|---|---|
| frontera (el falso rojo) | `main.tex` real | `ROJOS: NINGUNO` | `ROJOS: NINGUNO` · `RC=0` |
| meta-lenguaje real | `main.tex` + `"The gate is open and the corpus grows."` | `RC=1` | `RC=1` · `ROJO META-LENGUAJE: corpus=1 gate=1` |
| frontera negativa | `main.tex` + `"The aggregate quantity is bounded."` | `RC=0` | `RC=0` · `ROJOS: NINGUNO` |
| estructura rota | `main.tex` + `\begin{equation} x \end{align}` | `RC=1` | `RC=1` · `ROJO ENTORNOS` |
| no regresión | conteo estructural pre vs post sobre `main.tex` real | idéntico | **idéntico** (`diff` vacío, excluyendo la línea de rojos) |

Después de la corrección el linter **puede** enrojecer, y en la ventana §0 **no** enrojece: el
manuscrito no contiene meta-lenguaje del corpus interno.

---

## §8 · Lo que este documento **no** afirma

1. **No es revisión por pares.** Un método declarado no es un método aceptado.
2. **No certifica la física.** Certifica que las medidas son reproducibles y que las fronteras
   están dichas. Que las ecuaciones estén bien es otra pieza, y no está aquí.
3. **No sustituye a `main.tex`.** El papel dice qué se sostiene; este documento dice cómo se
   comprobó y dónde se dejó de comprobar.
4. **No promete permanencia de las cifras.** Cada una viaja con su ventana.
5. **No promete integridad externa.** `MIT` cubre el código, no los resultados; y ningún
   archivo impide copiar del navegador.

---

## §9 · Identidad de las piezas de esta enmienda

| pieza | líneas | bytes | sha16 |
|---|---|---|---|
| `METHODOLOGY_AND_BOUNDARIES.md` | — | — | *su identidad no puede viajar dentro de sí misma: va en el mensaje de commit* |
| `README.md` (cuentas medidas) | 98 | 5 695 | *idem* |
| `lint_tex.py` (corregido) | 135 | 5 123 | `803d29ad03afa207` |

---

## §10 · Régimen de enmienda

- **Aditivo.** Se añade `§ADENDA n` al final con su `T_UTC`; **no** se reescribe el cuerpo.
- **Un rojo no se esconde**: si una medición nueva contradice una fila de arriba, la fila vieja
  se queda y la nueva se declara debajo, con su ventana.
- **Una cifra caducada no se «actualiza» en silencio**: se re-mide y se anota el drift (§6).
- **Un puntero roto no se tapa**: se declara (§6) hasta que la pieza exista, y cuando exista se
  dice qué es y qué no es (§6, primera fila).

---

## §11 · Cómo refutar este documento

Cada afirmación de arriba tiene un comando. Si alguno da otra cosa, el documento está mal:

```sh
git ls-files | wc -l                                   # 114 archivos rastreados
find bundle -type f | wc -l                             # 35
awk 'NF>=2' bundle/HASHES.sha256 | wc -l                # 34
(cd bundle && shasum -a 256 -c HASHES.sha256 | grep -c ': OK$')   # 34
sh bundle/verificar.sh                                  # VERDE PARCIAL · RC=0 · 2 NO MEDIDO
sh bundle/tests/bench_must_fail.sh                      # casos=7 · conformes=7 · rojos=0
python3 -B lint_tex.py; echo "RC=$?"                    # ROJOS: NINGUNO · RC=0
grep -n 'lint_tex' bundle/verificar.sh tools/sello.sh .github/workflows/ci.yml   # (vacío)
```

---

**Parte del archivo de instrumentos de [alexisromtz-lab](https://github.com/alexisromtz-lab).**
Licencia MIT — ver [`LICENSE`](LICENSE).
