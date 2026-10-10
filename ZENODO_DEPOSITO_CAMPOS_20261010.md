# ZENODO · HOJA DE CAMPOS DEL DEPÓSITO DEL PREPRINT (2026-10-10)

`ESTADO · esta hoja es auxiliar de captura, NO es pieza de registro.`
`La pieza de registro es platino-labs/ADENDA_3_…EL_PRE_REGISTRO_DEL_DOI_DEL_PREPRINT_20261010.md (§5).`
`ADJUDICACIÓN = 0` · append-only.

`T_UTC_MEDICION = 2026-10-10T23:12:55Z`
`MOTOR = wc -c · shasum -a 256 · python3 (re)` · `UNIDAD = byte y archivo` · `VENTANA = reloj UTC de arriba`

---

## 0. Lo que Zenodo EXIGE y lo que es opcional

Obligatorios (5): **Resource type** · **Title** · **Creators** · **Description** · **License**.
Recomendados: **Publication date** · **Keywords** · **Language** · **Related works**.
Opcionales, se pueden dejar vacíos: Funding, Contributors, Subjects (clasificación), Version,
Alternate identifiers, References, Notes, Location, Dates, Method, Software, Instruments.

Regla: si un campo no está abajo, **se deja vacío**. Zenodo no lo exige.

---

## 1. FILES (primero esto)

Arrastrar **en este orden** a «Drag and drop files here»:

| # | archivo | bytes | sha256 (16) | papel |
|---|---------|-------|-------------|-------|
| 1 | `main.pdf` | 146 779 | `753e25234203a649` | **documento principal / vista previa** |
| 2 | `sfqed-paper-zenodo-20261010.tar.gz` | 189 022 | `c567b5f9a7712357` | fuentes + figuras (6 miembros, sin `._` ni `.DS_Store`) |

- **El orden importa:** en Zenodo la vista previa es **el primer archivo** cuyo tipo se puede previsualizar
  ⇒ `main.pdf` va **primero**.
- Alternativa (equivalente al tar.gz, si prefieres archivos sueltos): `main.tex` (22 358 B · `5fa1315b33ff0769`),
  `refs.bib` (3 694 B · `940e3cf07ce24a1b`), `figures/fig_invariants.py` (5 894 B · `d1626c36036e62b8`),
  `figures/fig_invariants.pdf` (46 576 B · `a97886dd5135371d`).
- Si al terminar la subida la vista previa no es el PDF, arrastra `main.pdf` al primer puesto de la lista.

---

## 2. BASIC INFORMATION

| Campo | Valor |
|-------|-------|
| **Resource type** | `Publication` → `Preprint` |
| **Title** | `Boundary-condition geometry for energy-minimal Schwinger pair creation in coherent electromagnetic fields` |
| **Publication date** | `2026-10-10` (si publicas después de medianoche UTC, `2026-10-11`) |
| **Language** | `English` |

---

## 3. CREATORS

| Campo | Valor |
|-------|-------|
| Family name | `Román Martínez` |
| Given names | `José Alexis` |
| Affiliation | `Platino Labs` |
| ORCID / Role | vacío (opcional) |

---

## 4. DESCRIPTION (texto del resumen)

Pegar **una** de las dos versiones. La (A) es la salida literal del `.tex` (contiene LaTeX: se vería literal).
La (B) es la misma prosa en HTML, que el editor de Zenodo sí interpreta (subíndices, superíndices, cursiva).

### (A) literal del `.tex` — 1 486 caracteres

Direct pair creation from the quantum vacuum requires electromagnetic fields comparable to the Sauter--Schwinger critical field $E_{\mathrm{cr}}=m_e^2c^3/(e\hbar)\simeq1.32\times10^{18}\,\mathrm{V\,m^{-1}}$, five to six orders of magnitude above present laser intensities. Because the local pair-production rate is a function of the two Lorentz invariants of the field, the only controllable levers at fixed total energy are the geometry and the coherence of the field superposition. We cast the problem as a variational one: minimise the total input pulse energy subject to a prescribed pair yield. Three statements are established analytically. (i)~A single plane wave is a null field, $\mathcal{F}=\mathcal{G}=0$, and creates no pairs; pair creation is therefore a property of the \emph{collision} of fields, not of an individual pulse. (ii)~For $N$ phase-matched beams focused into a common volume at fixed total energy, the peak field scales as $\sqrt{N}$, so the energy required to reach a given invariant scales as $1/N$, under explicitly stated assumptions. (iii)~The residual freedom is polarisation and temporal structure, which decide whether the strong-field region is oscillatory (counter-propagating linear standing wave) or quiescent (co-rotating circular collision); the quiescent configuration is preferable for adiabatic pair creation. We state the boundary conditions implied by phase matching and propose a falsifiable one- and two-dimensional particle-in-cell test.

### (B) misma prosa, en HTML (recomendada)

Direct pair creation from the quantum vacuum requires electromagnetic fields comparable to the Sauter–Schwinger critical field E<sub>cr</sub> = m<sub>e</sub><sup>2</sup>c<sup>3</sup>/(eℏ) ≃ 1.32×10<sup>18</sup> V m<sup>−1</sup>, five to six orders of magnitude above present laser intensities. Because the local pair-production rate is a function of the two Lorentz invariants of the field, the only controllable levers at fixed total energy are the geometry and the coherence of the field superposition. We cast the problem as a variational one: minimise the total input pulse energy subject to a prescribed pair yield. Three statements are established analytically. (i) A single plane wave is a null field, ℱ = 𝒢 = 0, and creates no pairs; pair creation is therefore a property of the <em>collision</em> of fields, not of an individual pulse. (ii) For <em>N</em> phase-matched beams focused into a common volume at fixed total energy, the peak field scales as √<em>N</em>, so the energy required to reach a given invariant scales as 1/<em>N</em>, under explicitly stated assumptions. (iii) The residual freedom is polarisation and temporal structure, which decide whether the strong-field region is oscillatory (counter-propagating linear standing wave) or quiescent (co-rotating circular collision); the quiescent configuration is preferable for adiabatic pair creation. We state the boundary conditions implied by phase matching and propose a falsifiable one- and two-dimensional particle-in-cell test.

---

## 5. LICENSE

`Creative Commons Attribution 4.0 International` (CC-BY-4.0).

---

## 6. KEYWORDS (8, una por línea)

```
strong-field QED
Schwinger effect
pair creation
vacuum instability
coherent fields
boundary conditions
hep-ph
physics.plasm-ph
```

---

## 7. RELATED WORKS

| Relación | Identifier | Resource type |
|----------|-----------|---------------|
| `isSupplementTo` | `10.5281/zenodo.23288831` | `Software` (el registro de `protocol-core`) |

Nota de frontera, sin adjudicar: la receta que dictaste fija la relación `isSupplementTo`.
La relación inversa (`isSupplementedBy`) describiría «este artículo es complementado por aquel registro».
Se captura **el valor dictado**; si el orden de la relación se decide distinto, se corrige **aquí, antes de publicar**,
porque después el DOI es permanente.

---

## 8. NOTES (opcional, un solo párrafo)

```
Source, bibliography and figure scripts are included in sfqed-paper-zenodo-20261010.tar.gz.
main.pdf (146779 B, sha256 753e25234203a649…) is the version of record.
Compiled with tectonic 0.17.0; RevTeX 4-2. The package contains no auxiliary build byproducts.
```

---

## 9. PUBLICAR

1. **Publish** (no basta *Save*: el DOI se acuña al publicar).
2. Al publicar, Zenodo devuelve **`10.5281/zenodo.XXXXXXX`** — copiarlo de la cabecera del registro.
3. **Pasarme ese identificador.** Es lo único que falta para cerrar **Puerta 1**:
   se escribe en `§5` de `ADENDA_3_AL_ACTA_DE_PUBLICACION_EL_PRE_REGISTRO_DEL_DOI_DEL_PREPRINT_20261010.md`
   (`10.5281/zenodo.__________` → valor real, + `T_UTC_DOI`), y la pieza vieja **no se parchea**:
   el acta madre y `ADENDA_1`/`ADENDA_2` quedan intactas.

Gate de la anexión (pre-registrado): al recibir el DOI se **re-mide** `main.pdf`.
Si no da `146 779 B · 753e25234203a649…`, el DOI **no se anexa** hasta declarar la divergencia.

---

`T_UTC_HOJA = 2026-10-10T23:12:55Z`

---

## 4.b VARIANTE (C) — sin etiquetas HTML, sólo Unicode

Sirve si el desplegable de **Description** no ofrece `HTML` (opciones `Paragraph` / `Markdown`).
Se pega tal cual, sin etiquetas y sin LaTeX: los signos son caracteres reales.

Direct pair creation from the quantum vacuum requires electromagnetic fields comparable to the Sauter–Schwinger critical field E_cr = m_e²c³/(eℏ) ≃ 1.32×10¹⁸ V m⁻¹, five to six orders of magnitude above present laser intensities. Because the local pair-production rate is a function of the two Lorentz invariants of the field, the only controllable levers at fixed total energy are the geometry and the coherence of the field superposition. We cast the problem as a variational one: minimise the total input pulse energy subject to a prescribed pair yield. Three statements are established analytically. (i) A single plane wave is a null field, ℱ = 𝒢 = 0, and creates no pairs; pair creation is therefore a property of the *collision* of fields, not of an individual pulse. (ii) For N phase-matched beams focused into a common volume at fixed total energy, the peak field scales as √N, so the energy required to reach a given invariant scales as 1/N, under explicitly stated assumptions. (iii) The residual freedom is polarisation and temporal structure, which decide whether the strong-field region is oscillatory (counter-propagating linear standing wave) or quiescent (co-rotating circular collision); the quiescent configuration is preferable for adiabatic pair creation. We state the boundary conditions implied by phase matching and propose a falsifiable one- and two-dimensional particle-in-cell test.

En Markdown los asteriscos de *collision* se ven como cursiva; en Paragraph quedan como asteriscos (inofensivo).
