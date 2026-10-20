# sfqed-paper — el papel, su aparato de medida y la custodia del bundle

> **EN —** A paper plus its **measuring apparatus**: a 26-file verifiable bundle, a one-command gate,
> a three-valued verdict (`0` VERDE / `1` FRACTURA / `2` CONTRATO ROTO), a 7-case *must-fail* bench that
> measures the verifier **from outside**, and a declared list of what is **not** sealed.

Este repositorio no es "un paper con scripts": es **el papel + el aparato que lo mide + la custodia que
lo protege**. La distinción es la que permite que un verificador **no se valide a sí mismo**.

## Por dónde entrar

| quiero… | voy a |
|---|---|
| correr la verificación (un comando) | `sh tools/sello.sh` → una línea atómica al chat (`VEREDICTO · RC · MOTOR · SHA16`) y el crudo a `corridas/` |
| saber **qué motor** firma qué | [`MOTORES.md`](MOTORES.md) — sello `M0`, motor canónico, 4 protocolos de contexto |
| el piso de ejecución | [`flake.nix`](flake.nix) — pin único: `.#gnu` (default), `.#bsd` (control), `.#oci` |
| el aparato, pieza por pieza | [`bundle/00_INDICE.md`](bundle/00_INDICE.md) |
| el papel | [`main.tex`](main.tex) + [`refs.bib`](refs.bib) + `main.pdf` |
| el depósito | [`ZENODO_DEPOSITO_CAMPOS_20261010.md`](ZENODO_DEPOSITO_CAMPOS_20261010.md) |
| la salud del bundle | [`BUNDLE_VERIFICATION_REPORT_20261011.md`](BUNDLE_VERIFICATION_REPORT_20261011.md) |

## `bundle/` = el aparato de medida (26 archivos)

`UNIVERSO DECLARADO` por el propio verificador: **26 archivos = 25 declarados en `HASHES.sha256` + el
manifiesto**. No es `sim/`: es el aparato.

| pieza | qué es |
|---|---|
| `bundle/verificar.sh` | el gate de un comando, 4 etapas: `[1]` medidor · `[2]` integridad · `[3]` custodia · `[4]` anclas |
| `bundle/HASHES.sha256` | el manifiesto (no puede declararse a sí mismo) |
| `bundle/actas/` | 10 piezas: lecturas contra, auditoría del orden FDTD, entrega a la pestaña vecina, veredicto del control pareado |
| `bundle/preregistros/` | 3 piezas: `PREREGISTRO_KERR`, `PREREGISTRO_SIGMA_PHI`, `PROTOCOLO_1overN` |
| `bundle/instrumentos/medidores/` | `falsador.py`, `maxwell2d.py` |
| `bundle/instrumentos/custodia/` | `gitleaks_casa.toml`, `pre-commit`, `pre-push`, `install.sh` |
| `bundle/tests/bench_must_fail.sh` | **7 casos** que miden al verificador **desde afuera** |

**Tricotomía del veredicto:** `0` = VERDE · `1` = FRACTURA del objeto · `2` = **CONTRATO ROTO** (metro
ilegible; incluye el manifiesto de 0 entradas, que se satisfaría solo: `0 + 0 == 0`). Un verificador
que no sabe decir "no puedo medir" es un verificador ciego.

## `sim/` = el laboratorio (110 archivos)

| pieza | qué es |
|---|---|
| `sim/maxwell2d.py` | el kernel FDTD citado por su `sha16` en el mensaje de commit (`1db75ea7b0b8cba4`) |
| `sim/runner_2d3v.py` | el corredor 2D3V |
| `sim/lector_invariantes.py` | lee invariantes entre modos — **`RC=2` sin diagnosticar** (declarado, no escondido) |
| `sim/PREREGISTRO_KERR_20261011.md` | pre-registro sellado: nulo A falsable, nulo B reescrito **por su propio metro**, piso lineal `4.94 %` |
| `sim/data/invariantes/` | veredicto del control pareado + su crudo (`control_pareado_convergente.json`) |
| `sim/data/sigma_phi/medidas_fdtd_sigma_phi.csv` | las medidas, con **33 líneas de comentario** (`^#`) |

## Reproducir

```sh
sh tools/sello.sh                 # una línea: VEREDICTO · RC · MOTOR · SHA16  (+ crudo a corridas/)
sh bundle/verificar.sh            # el gate del aparato: medidor, integridad, custodia, anclas
sh bundle/tests/bench_must_fail.sh  # 7 casos que deben FALLAR: el banco mide al medidor
python3 lint_tex.py               # linter del manuscrito
nix develop                       # piso `.#gnu` (default) · `.#bsd` = control · `.#oci`
```

## Lo que **NO** está sellado (declarado, con puntero)

Fuente: [`MOTORES.md`](MOTORES.md) §6.

- `flake.lock` **ausente**; `nix` **ausente** en el anfitrión de la ventana medida.
- Los ` M` (sucios) del bundle: la integridad se declara por archivo, no por árbol.
- El `RC=2` del lector de invariantes, **sin diagnosticar**.
- El **crudo pre-fix perdido** de la primera corrida.

Ninguno de estos cuatro es un detalle: son la frontera explícita del trabajo, y por eso están escritos.

## Deuda declarada (medida 2026-10-20)

El propio `INDEX.md` §1 lista tres piezas que **hoy no existen en el repositorio** — medida por
`gh api` sobre `main`, código HTTP `404`:

| pieza declarada en `INDEX.md` §1 | tamaño declarado | estado medido |
|---|---|---|
| `README.md` | 12 473 B | **404** |
| `METHODOLOGY_AND_BOUNDARIES.md` | 15 393 B | **404** |
| `sfqed-paper-zenodo-20261010.tar.gz` | 340 248 B | **404** |

**Se declaran; no se reconstruyen por conveniencia.** Este `README.md` es nuevo y **no** sustituye al
que el índice declaraba: aquel describía "qué declara y qué no declara el trabajo", y esa pieza sigue
pendiente de publicarse. Un índice que apunta a un hueco es un dato, no un adorno.

## Licencia y citación

MIT — ver [`LICENSE`](LICENSE). Depósito: `ZENODO_DEPOSITO_CAMPOS_20261010.md`.

**Parte del archivo de instrumentos de [alexisromtz-lab](https://github.com/alexisromtz-lab).**
