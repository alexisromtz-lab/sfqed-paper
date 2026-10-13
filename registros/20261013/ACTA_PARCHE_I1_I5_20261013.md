# ACTA — Parche quirúrgico I1–I5 sobre `main.tex`

UNIVERSO DECLARADO: `/Users/marlene/sfqed-paper` (árbol git, 1 archivo destino)
VENTANA: 2026-10-13T08:15:23Z → 2026-10-13T08:33:48Z
UNIDAD: 1 archivo · MOTOR: `python3` (escritura) + `tectonic` v2 (compilación)

---

## 1. Pre-vuelo A2.1 (bloqueante, antes de escribir)

```
bash tools/gate_pre_escritura.sh \
  /Users/marlene/sfqed-paper/main.tex \
  61edfc7ef33d78a8805c8bc2d79c11e3824649c2 \
  INTERSECCION-I1-I5-PARCHE-QUIRURGICO-20261013 \
  652
```

`RC=0` · `PRE-VUELO OK` · `08:15:23Z`. Destino rastreado, limpio, huella ausente.

## 2. Identidad del destino (medida fuera, no estimada)

| | líneas | bytes | sha16 | blob git |
|---|---|---|---|---|
| PRE | 652 | 34003 | `ca7e8920abf8c55f` | `61edfc7ef33d78a8805c8bc2d79c11e3824649c2` (= `HEAD:main.tex`) |
| POST | 736 | 39650 | `87033ba575b39ba8` | `4f22c533ab36c94d55d7050b305cef62d140b35f` (= `git hash-object`) |

## 3. Delta atribuido

`git diff --numstat -- main.tex` → `96 12` (inserciones · borrados · archivo).
Las **12** líneas borradas caen **todas** dentro de los 5 bloques sustituidos
(verificado una a una en `git diff -U0`), sin pérdida colateral.

## 4. Estructura — el conteo, que es el único gate de un `.tex`

`\section` 5 · `\subsection` 9 · `\paragraph` **17** (16 previos + 1 nuevo) ·
`\begin{equation}` **19** (18 numeradas + 1 en el apéndice) ⇒ **ninguna ecuación
validada se renumeró**: toda la matemática nueva va **en línea**, no como
ecuación numerada.

## 5. Contenido aplicado

| bloque | sitio | qué declara |
|---|---|---|
| 0 | l.15 | huella del contrato, en comentario LaTeX (invisible al revisor del PDF) |
| I1 | l.194–202 | las **dos** condiciones de validez de la LCFA: temporal (Keldysh) y espacial (homogeneidad) |
| I2 | l.326 | preferencia del circular co-rotante **demostrada** (monotonía + convexidad de `w(a)`), no asertada |
| I3a | Resumen | el volumen de interacción, declarado en la cláusula (ii) |
| I3b | l.383 | umbral de **amplitud** vs rendimiento **integrado**; `Σ×τ` común e invariante en `N` |
| I3c | supuestos | supuesto **(v)** de linealidad, y remisión a la cota superior de `N` |
| I4 | l.691 | `\paragraph{Upper bound on $N$.}`: no linealidad del vacío + apantallamiento de plasma |
| I5 | l.563 | método tras las cifras: cuadratura sobre malla 3D, cubo `6λ`, `Δx = λ/32`, `w₀ = 2λ` |

## 6. Compilación

`tectonic -X compile main.tex` → `RC=0` · `main.pdf` 175.7 KiB.
Avisos: 3 `Underfull \hbox` + 2 `Overfull \vbox` (tipográficos, preexistentes).
**0 errores · 0 referencias indefinidas · 0 ecuaciones sin cerrar.**

## 7. Cierre A2.1

- **Sonda nominal** (la huella del contrato) → `RC=11 COLISION DETECTADA` ⇒ *la
  fila ya está escrita* ⇒ **cumplimiento pasivo, cero escrituras adicionales**.
- **Control** (huella que no existe) → `RC=13 ESTADO SUCIO`, porque el gate es
  *fail-closed* sobre un destino ya modificado. El control **no discrimina** por
  diseño; se declara en vez de adjudicarse.

## 8. Estado git

` M main.tex` (ordenado) · ` M main.pdf` (consecuencia de la corrida `tectonic`
ordenada) · **92** entradas no rastreadas preexistentes (`README.md` y
`mainNotes.bib` con mtime 11-Oct; `registros/` con mtime de hoy 08:12Z, que es la
entrega de la intersección). **No se hizo commit: no fue ordenado.**

⇒ `git dirty = 0` **no es alcanzable**: el destino está rastreado y lo modificó la
orden. Se declara el par de deltas atribuidos en lugar de forzar el cero.

## 9. DISCREPANCIA MEDIDA — declarada, no adjudicada

El plan ordenaba, para la condición espacial (I1), `kλ_C ≈ 3×10⁻³` con `λ = 800 nm`.

**Medido:** `2πλ_C/λ = 2π·3.8615926796e-13 / 8e-7 = 3.0×10⁻⁶`.

El valor ordenado correspondería a `λ = 2πλ_C/3e-3 = 8.09×10⁻¹⁰ m ≈ 0.81 nm`
⇒ **desfase de 10³ en la longitud de onda**, no un error de lectura.

Se escribió **el valor medido** (`3.0\times10^{-6}`), y el parche lo **calcula en
tiempo de corrida** a partir de `λ_C` y `λ` en vez de copiar la cifra ordenada.

## 10. Lo que NO entró (por contrato)

Residuos de una sola ronda (sin intersección) y los pares mutuamente refutados
(Objetivo 1-ii escalar/espinor; prefactor `×2` del tensor dual): **no se
escribieron**. Tampoco los diferidos (`eh → e\hbar`, resultados de la malla
ternaria, recompilación v2), que exigen orden explícita.
