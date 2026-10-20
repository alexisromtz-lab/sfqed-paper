# ÍNDICE · sfqed-paper (metadatos por referencia)

> **El puntero viaja, el cuerpo no.** Este archivo dice **dónde vive qué** y **con qué
> identidad**, para no recorrer el árbol en cada pregunta. Las cifras de identidad
> caducan: viajan con su ventana.
>
> ```
> T_UTC 2026-10-11T05:54:46Z   ·   UNIVERSO: el arbol sin .git   ·   LECTURA SOLO
> UNIDAD: archivo | linea | byte | sha16   ·   MOTOR: shasum -a 256 | wc | python3 -B
> ```

---

## 0 · POR DÓNDE ENTRAR

| quiero… | voy a |
|---|---|
| correr la verificación (un comando) | `sh tools/sello.sh` → una línea al chat, el crudo a `corridas/` |
| saber **qué motor** firma qué | `MOTORES.md` (sello `M0`, canónico GNU, protocolo de contexto) |
| el piso de ejecución | `flake.nix` (pin único: `.#gnu` = default, `.#bsd` control, `.#oci`) |
| el aparato de medida, pieza por pieza | `bundle/00_INDICE.md` (el índice del propio bundle) |
| el papel | `main.tex` (+ `refs.bib`, `main.pdf`) |
| qué declara y qué no declara el trabajo | `README.md`, `METHODOLOGY_AND_BOUNDARIES.md` |
| el depósito | `ZENODO_DEPOSITO_CAMPOS_20261010.md`, `sfqed-paper-zenodo-20261010.tar.gz` |

---

## 1 · RAÍZ (piezas que **no** viajan al bundle)

| pieza | qué es | tamaño / sha16 (ventana de arriba) |
|---|---|---|
| `flake.nix` | **el pin**: shells GNU/BSD + derivación OCI | *nuevo 2026-10-11* |
| `MOTORES.md` | sello `M0` + motor canónico + 4 protocolos de contexto | *nuevo 2026-10-11* |
| `INDEX.md` | este índice | — |
| `tools/sello.sh` | la línea atómica (`VEREDICTO · RC · MOTOR · SHA16`) y el crudo a disco | *nuevo 2026-10-11* |
| `main.tex` | el manuscrito | 514 l · 26 014 B · `6cd0f0803b61a3a5` · ` M` (otra mano) |
| `README.md` | entrada del repo | 12 473 B |
| `METHODOLOGY_AND_BOUNDARIES.md` | método y fronteras declaradas | **publicada 2026-10-20** · ventana propia: 261 l · 15 577 B · `ca7578850989c48d` |
| `refs.bib` | bibliografía | 3 694 B |
| `lint_tex.py` | linter del manuscrito | 4 481 B |
| `.gitleaks.toml` | reglas de la casa para el gate de custodia | 5 381 B |
| `sfqed-paper-zenodo-20261010.tar.gz` | el tarball depositado | 340 248 B |

<!-- HUELLA-INDEX-METHODOLOGY-MEDIDO-20261020 -->
> **Frontera re-medida (2026-10-20T23:12Z, HTTP anónimo sobre `main`).** De las piezas de esta
> tabla: `README.md` **existe pero no es la declarada** (la de 12 473 B describía qué declara y qué
> no el trabajo, y ese texto no está); `METHODOLOGY_AND_BOUNDARIES.md` **existe** con la identidad
> anotada arriba y declara sus propias fronteras; el `tar.gz` de 340 248 B sigue **404**. Las demás
> cifras de la tabla son la ventana 2026-10-11 y **no** se re-midieron aquí.

---

## 2 · `bundle/` = **el aparato de medida** (26 archivos)

`UNIVERSO DECLARADO` por el propio verificador: **26 archivos = 25 declarados en
`HASHES.sha256` + el manifiesto**. **No es `sim/`: es el aparato.**

| pieza | qué es | identidad (ventana de arriba) |
|---|---|---|
| `verificar.sh` | el gate de un comando: `[1]` medidor · `[2]` integridad · `[3]` custodia · `[4]` anclas | 292 l · 12 269 B · `b51b2b93baa630a7` · ` M` |
| `HASHES.sha256` | el manifiesto (no puede declararse a sí mismo) | 25 l · 2 587 B · `3de1aba9d4ab3648` · ` M` |
| `00_INDICE.md` | el índice del bundle: cada afirmación apunta a una línea **viva** | 179 l · 15 537 B · `e54241ed2aac8449` · ` M` |
| `actas/` | 10 piezas: lecturas contra, auditoría del orden FDTD, entrega a la pestaña vecina… | — |
| `preregistros/` | 3 piezas: `PREREGISTRO_KERR`, `PREREGISTRO_SIGMA_PHI`, `PROTOCOLO_1overN` | — |
| `instrumentos/medidores/` | `falsador.py`, `maxwell2d.py` | — |
| `instrumentos/telemetria_minima.py` | el medidor que se auto-prueba (`[1]` del gate) | — |
| `instrumentos/custodia/` | `gitleaks_casa.toml`, `install.sh`, `instalar_en_repos.sh`, `pre-commit`, `pre-push` | — |
| `tests/bench_must_fail.sh` | **7 casos** que miden al verificador **desde afuera** (un verificador no se valida a sí mismo) | 166 l |

**Tricotomía:** `0` = VERDE · `1` = FRACTURA del objeto · `2` = CONTRATO ROTO (metro
ilegible; incluye manifiesto de 0 entradas, que se satisface solo: `0 + 0 == 0`).

---

## 3 · `sim/` = el laboratorio (110 archivos)

### 3.1 Piezas ancla

| pieza | qué es | identidad |
|---|---|---|
| `PREREGISTRO_KERR_20261011.md` | pre-registro sellado: nulo A falsable, nulo B reescrito por su propio metro, piso lineal 4.94% | 98 l · 9 643 B · `b6ffaddcf6e67df0` |
| `maxwell2d.py` | el kernel FDTD (instrumento citado por su sha16 en el mensaje de commit) | 715 l · 30 759 B · `1db75ea7b0b8cba4` |
| `lector_invariantes.py` | lee invariantes entre modos · **RC=2 sin diagnosticar** | 635 l · 32 113 B · `9fab4e04d281d3cc` |
| `runner_2d3v.py` | el corredor 2D3V | 528 l · 24 072 B · `f280fb6744917e9a` |
| `ACTA_DEL_DISPARO_PESTANA2_CIRCULAR_CORREGIDA_20261011.md` | el acta del disparo corregido | 149 l · 11 357 B · `74f1213640b01724` |

### 3.2 Datos

| pieza | qué es | identidad |
|---|---|---|
| `data/invariantes/VEREDICTO_CONTROL_PAREADO_20261011.md` | el veredicto (las cifras viven en la pieza, no en este índice) | 254 l · 15 118 B · `a6316f8db84d8885` |
| `data/invariantes/INFORME_LECTOR_INVARIANTES_20261011.md` | el informe · **no editado** (mtime verificado) | 277 l · 17 726 B · `0b612674187552ad` |
| `data/invariantes/control_pareado_convergente.json` | el crudo del control pareado | 1 288 l · 27 892 B · `41fce209adc05f98` |
| `data/sigma_phi/medidas_fdtd_sigma_phi.csv` | las medidas · **33 líneas de comentario** (`^#`) | 1 669 l · 214 596 B · `4ed3cd7990fd75c7` |
| `data/sigma_phi/telemetria_circular_sigma_phi_20261011.jsonl` | telemetría · **0 campos de tiempo** | 2 l · 649 B · `34cb45c55fcc8937` |

---

## 4 · Consultas (sin recorrer el árbol)

```
grep -n '<clave>' INDEX.md            # buscar una pieza por nombre o tema
grep -n '<etiqueta>' MOTORES.md       # M0 | GNU | HOST-GNU | BSD-NO-REPRODUCIBLE | compuerta
sed -n '<l1>,<l2>p' <pieza>           # leer el bloque exacto, no el archivo entero
sh tools/sello.sh                     # el estado vivo del aparato, en una linea
```

## 5 · Lo que NO está sellado

Puntero: **`MOTORES.md` § 6**. (Ahí van `flake.lock` ausente, `nix` ausente en el
anfitrión, los ` M` del bundle, el RC=2 del lector y el crudo pre-fix perdido.)
