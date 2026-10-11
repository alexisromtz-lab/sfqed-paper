---
# --- Front-matter de depósito (Zenodo) ---
title: "Auditoría metrológica del bundle de reproducibilidad de sfqed-paper: integridad, cobertura y anclaje a revisión"
upload_type: publication
publication_type: technicalnote
language: spa
date: 2026-10-11
version: "1.0.0"
license: CC-BY-4.0
creators:
  - name: "Román Martínez, José Alexis"
    affiliation: "Platino Labs"
keywords:
  - strong-field QED
  - Schwinger effect
  - pair creation
  - vacuum instability
  - coherent fields
  - boundary conditions
  - hep-ph
  - physics.plasm-ph
related_identifiers:
  - identifier: "10.5281/zenodo.23289363"
    relation: isSupplementTo
    scheme: doi
    resource_type: publication
    x_procedencia: "DOI del depósito vivo del pre-print; impreso por la API de Zenodo"
  - identifier: "10.5281/zenodo.23288831"
    relation: isSupplementTo
    scheme: doi
    resource_type: publication
    x_procedencia: "leído en el campo related_identifiers del registro vivo 23289363"
# --- Anclaje de la medición (campos propios, no Zenodo) ---
x_repositorio: sfqed-paper
x_rama: main
x_commit_cierre: 000916239dd2f013b5e7417281551ae32119e9db
x_commit_padre: 2508ba0b3e6831d0e3d7b00b102aec15f8682b10
x_objeto_sellado: "bundle/ — 35 hojas · 34 entradas · HASHES.sha256 = 0ce97cf9d8c44987"
x_motor_de_medicion: "shasum -a 256 | cmp | grep -F | python3 -B | git (Darwin, M0)"
---

# Auditoría metrológica del bundle de reproducibilidad de `sfqed-paper`

Este informe es autónomo: no requiere el registro interno de laboratorio que lo originó, ni ningún archivo que no esté en el repositorio o en el PATH del lector. Todas las cifras se acompañan del motor, la unidad, la ventana y el comando que las respalda; ninguna cifra de conteo sobrevive a la hora en que fue escrita sin declararla.

## 1. Alcance y límites declarados

Se audita **un objeto**: el directorio `bundle/` del repositorio `sfqed-paper` en la revisión `0009162` (`000916239dd2f013b5e7417281551ae32119e9db`), con su manifiesto criptográfico, su verificador propio, su índice y su banco de casos negativos. Se audita con **dos metros independientes en su autoría de escritura**: el verificador que vive *dentro* del objeto (`bundle/verificar.sh`) y un auditor *externo* (`tools/verificar_bundle.sh`) que vive fuera de él precisamente para no reabrir la cadena sellada.

`bundle/` es inmutable: este informe **no lo modifica**, no lo regenera y no lo re-sella. Cualquier corrección futura entra por una versión nueva del auditor externo o por un commit nuevo del objeto, nunca por una edición en sitio.

Lo que este informe **no** certifica está en la sección 11 y es parte del contrato, no una nota al pie.

## 2. Objeto y revisiones de cierre

UNIVERSO DECLARADO: rama `main` del repositorio `sfqed-paper` · UNIDAD: revisión de git · MOTOR: `git` · VENTANA: hasta 2026-10-11T16:36Z.

- `HEAD` al cerrar: `0009162` = `000916239dd2f013b5e7417281551ae32119e9db`, comprometido 2026-10-11T16:23:20Z, mensaje *"tools: auditor externo de bundle v2 con guarda de piso estricta y banco must-fail (7/7)"*.
- Revisión consolidada previa (padre de `HEAD`): `2508ba0` = `2508ba0b3e6831d0e3d7b00b102aec15f8682b10`, comprometida 2026-10-11T06:39:36Z, mensaje *"bundle: cierre aditivo del re-sello consolidado (4 correcciones de forma + ancla viva)"*.
- Universo de revisiones disponibles: **24 commits** (`git rev-list --all`).
- Estado del árbol de trabajo: `git status --porcelain` = **22 entradas** en total; restringido al objeto, `git status --porcelain -- bundle/` = **vacío**. El objeto está limpio.
- Este informe nace **no versionado**, igual que `README.md` y `METHODOLOGY_AND_BOUNDARIES.md` en la raíz. Su propia identidad (sha256, líneas, bytes) se vuelve re-anclable en el commit que lo introduzca; por eso no se imprime aquí su hash: la cifra interna de una pieza describe siempre la versión anterior de esa pieza.

Comando que respalda esta sección: `git rev-parse HEAD HEAD^ && git rev-list --all | wc -l && git status --porcelain -- bundle/`.

## 3. Estado sellado de `bundle/` (medido)

UNIVERSO DECLARADO: `bundle/` completo · UNIDAD: hoja (archivo regular) y entrada de manifiesto · MOTOR: `find` + `awk` + `shasum -a 256` · VENTANA: 2026-10-11T16:36Z.

| cantidad | valor | comando que lo respalda |
|---|---|---|
| hojas reales | **35** | `find bundle/ -type f` (coincide con `git ls-files bundle/`) |
| entradas del manifiesto | **34** | `wc -l < bundle/HASHES.sha256` (3 623 B) |
| sha16 del manifiesto | **0ce97cf9d8c44987** | `shasum -a 256 bundle/HASHES.sha256` |
| manifiesto que se lista a sí mismo | **0** | `grep -c 'HASHES.sha256' bundle/HASHES.sha256` |
| integridad | 34 OK · 0 FAILED | `shasum -a 256 -c bundle/HASHES.sha256` |
| cobertura | 35 hojas = 34 entradas + el propio manifiesto | verificación de partición del auditor externo |
| `bundle/verificar.sh` | `09beca42ea0289da` · 398 l · 18 454 B | es la línea 34 del manifiesto |
| `bundle/00_INDICE.md` | `22f48984250839ae` · 326 l | mismo blob en `2508ba0` y `0009162` |
| `bundle/tests/bench_must_fail.sh` | `7f9a2e4a207f1580` · 166 l · 7 614 B · modo 755 | mismo blob en 7 revisiones |

Lectura de la tabla: **35 hojas, 34 entradas**. El único elemento presente en el árbol y ausente del manifiesto es el propio manifiesto; esa excepción no se asume, se **mide** (el auditor externo aborta con `CONTRATO ROTO` si el conjunto sin entrada deja de ser exactamente `{HASHES.sha256}`).

## 4. Cómo reproducir (tres comandos, sin rutas locales)

Todos los comandos se ejecutan **desde la raíz del repositorio** y no escriben dentro del objeto. Requisitos en el PATH: `shasum`, `git`, `python3`, `gitleaks`.

1. Auditor externo (vive fuera del objeto, sha16 `09ab3b5b24d9bb47` · 251 l · 11 643 B · modo 755):

```
sh tools/verificar_bundle.sh
```

El auditor deposita su crudo en el directorio temporal del sistema y **rehúsa correr** (RC=2) si el crudo o el propio script caen dentro de `bundle/`. El lector que quiera fijar el destino usa `sh tools/verificar_bundle.sh --crudo RUTA_FUERA_DEL_OBJETO`.

2. Verificador propio del objeto (dentro del objeto, se invoca desde él):

```
cd bundle && ./verificar.sh
```

3. Banco de casos negativos (prueba que los metros **pueden** enrojecer):

```
sh bundle/tests/bench_must_fail.sh
```

El banco construye cada caso en un sandbox efímero creado con `mktemp -d` y copiado con `cp -R`; no toca el objeto real.

## 5. Vocabulario de veredictos y qué no dicen

Los dos metros hablan distinto y esa diferencia es deliberada.

Auditor externo (`tools/verificar_bundle.sh`, versión `v2`), precedencia `2 > 1 > 0`:

- `VERDE · RC: 0` — integridad, partición y piso conformes.
- `FRACTURA DEL OBJETO · RC: 1` — los bytes o la partición no cierran.
- `CONTRATO ROTO · RC: 2` — el metro no pudo medir: manifiesto malformado, vacío, por debajo del piso declarado, o el crudo dentro del objeto.

Verificador del objeto (`bundle/verificar.sh`):

- `VERDE · RC: 0` — todas las piezas declaradas medidas y conformes.
- `VERDE PARCIAL · RC: 0` — hay piezas verdes y al menos un bloque **no medido**: el veredicto nombra los bloques que no midió en lugar de callarlos.
- `FRACTURA del objeto · RC: n` — fallo de integridad, de cobertura (`FRACTURA DE COMPLETITUD`) o de custodia; cada fase nombra su causa.
- `SHA16: <manifiesto>` — la identidad del objeto medido viaja en la propia línea de veredicto.

Ninguno de los dos dice nada sobre **si el contenido científico es correcto**; dicen que el contenido es **el mismo** que el sellado y que la cobertura no tiene agujeros. Sección 11.

## 6. Banco de casos must-fail

El banco declara siete casos, cada uno con su código de salida **estricto**; el criterio de aislamiento de causa es que cada caso toca una sola cosa (un caso cambia bytes sin regenerar el manifiesto; otro cambia una línea anclada y **sí** regenera el manifiesto; los otros quitan exactamente una herramienta del PATH).

| caso | manipulación | RC exigido |
|---|---|---|
| A | byte invertido, mismo tamaño, en pieza rastreada | 1 |
| B | `HASHES.sha256` de 0 bytes | 2 |
| C | PATH sin `shasum` | 2 |
| D | medidor ausente | 2 |
| E | ancla caducada, manifiesto regenerado | 1 |
| F | sin repositorio git anfitrión | 0, declarado parcial |
| G | sin `gitleaks` en el PATH, con anfitrión git | 2 |

Resultado esperado y observado: `casos=7 · conformes=7 · rojos=0` → `VEREDICTO BANCO: VERDE (7/7)`. Un banco negativo conforme es la prueba de que el verde del objeto **no es vacuo**: el mismo metro sabe enrojecer, y se le vio hacerlo siete veces.

## 7. Cadena por revisión (punteros vivos)

Una cifra que sólo existe en un estado intermedio de la construcción —el archivo escrito pero todavía no comprometido— **no tiene referente**: un sha16 sin commit rastreable es un puntero sin casa. La cadena siguiente sustituye toda foto intermedia por una revisión: cada fila es reproducible con `git show <rev>:<ruta>`.

| pieza | primera revisión | sha16 | l |
|---|---|---|---|
| `bundle/verificar.sh` | `d4691d0` … `6b32918` | `eb14ce18e21c6b94` | 270 |
| `bundle/verificar.sh` | `bf87e38` … `10db313` | `356d681a37a20860` | 387 |
| `bundle/verificar.sh` | `2508ba0`, `0009162` | `09beca42ea0289da` | 398 |
| `bundle/HASHES.sha256` | hasta `d4691d0` | `bd7ba3ee00325c98` | 24 |
| `bundle/HASHES.sha256` | `bf87e38` … `10db313` | `91e410c2a90e9709` | 34 |
| `bundle/HASHES.sha256` | `2508ba0`, `0009162` | `0ce97cf9d8c44987` | 34 |
| `bundle/00_INDICE.md` | hasta `d4691d0` | `0adae0cbeb229451` | 120 |
| `bundle/00_INDICE.md` | `bf87e38` … `0009162` | `22f48984250839ae` | 326 |
| `bundle/tests/bench_must_fail.sh` | `bf87e38` … `0009162` | `7f9a2e4a207f1580` | 166 |
| `tools/verificar_bundle.sh` | `0009162` (introducido aquí) | `09ab3b5b24d9bb47` | 251 |

Procedimiento determinista que reconstruye la tabla (no usa nombres de archivo temporales; imprime a la salida estándar):

```python
python3 -B - <<'PY'
import hashlib, subprocess as sp
RUTAS = ["bundle/verificar.sh", "bundle/HASHES.sha256",
         "bundle/00_INDICE.md", "bundle/tests/bench_must_fail.sh"]
def run(*a): return sp.run(a, capture_output=True)
revs = run("git", "rev-list", "--all").stdout.decode().split()
filas = set()
for r in revs:
    for p in RUTAS:
        if run("git", "cat-file", "-e", r + ":" + p).returncode != 0:
            continue
        b = run("git", "show", r + ":" + p).stdout
        filas.add((p, hashlib.sha256(b).hexdigest()[:16], str(b.count(10)), r[:7]))
for f in sorted(filas):
    print("|".join(f))
print("UNIVERSO DECLARADO:", len(revs), "commits ·", len(RUTAS), "rutas · filas unicas =", len(filas))
PY
```

## 8. Crudo: dónde se deposita

La regla es una sola y la aplica el auditor como guarda dura, verificada **antes** de crear el archivo: **el crudo vive fuera del objeto auditado**. Si el crudo o el script caen dentro de `bundle/`, el auditor devuelve `CONTRATO ROTO · RC: 2` sin medir. El lector elige el depósito (por defecto, el directorio temporal del sistema declarado por `TMPDIR`); lo que este informe **no** hace es citar rutas absolutas de la máquina del autor. Un crudo citado por su ruta personal no es evidencia: es un recuerdo. El crudo citado por un informe es el que el lector puede regenerar con los tres comandos de la sección 4.

## 9. Resultados de la corrida de cierre

UNIVERSO DECLARADO: `bundle/` + `tools/verificar_bundle.sh` · UNIDAD: pieza y línea anclada · MOTOR: M0 (Darwin) · VENTANA: 2026-10-11T16:36:36Z – 2026-10-11T16:36:38Z.

Auditor externo:

```
PISO=25  N_LINEAS=34  N_HOJAS=35  N_OK=34  N_MAL=0
SIN_ENTRADA=1  ENT_SIN_HOJA=0  DUP=0  MALFORMADAS=0
SHA16_MANIFIESTO: 0ce97cf9d8c44987
VEREDICTO: VERDE · RC: 0 · MOTOR: tools/verificar_bundle.sh v2
```

Verificador del objeto:

```
RESUMEN verde=53 · rojo=0 · no_medido=0 · anclas=38 ok=38 rojo=0
T_UTC inicio=2026-10-11T16:36:37Z fin=2026-10-11T16:36:38Z
VEREDICTO: VERDE · RC: 0 · MOTOR: M0 · SHA16: 0ce97cf9d8c44987
```

Banco de casos negativos:

```
RESUMEN BANCO casos=7 · conformes=7 · rojos=0
VEREDICTO BANCO: VERDE (7/7) · los 7 codigos de salida son los estrictos
```

Tres cifras que viajan con su fecha y su comparación, porque miden deriva y no defecto: el verificador cuenta hoy `verde=53` sobre el objeto de hoy; el `piso` del auditor es una **cota declarada** (25), no una derivación; y el número de anclas vivas es 38 con 38 conformes. Correr el aparato completo deja, de nuevo, `git status --porcelain -- bundle/` **vacío**: medir no ensucia el objeto.

## 10. Re-anclaje: la regla del cociente

UNIVERSO DECLARADO: 24 commits × 4 rutas del objeto = 96 pares, 37 filas únicas · UNIDAD: sha16 citado · MOTOR: `git rev-list` + `shasum -a 256` · VENTANA: 2026-10-11T16:40Z.

El registro interno de laboratorio que originó este documento cita **16 sha16 distintos**; de ellos, **2** son re-anclables a una revisión (`eb14ce18e21c6b94`, `7f9a2e4a207f1580`) y **14** no existen en ninguna de las 24 revisiones: describen estados intermedios de la construcción —archivos escritos y todavía no comprometidos— que el proceso se llevó consigo.

Cociente medido: `re-anclables / citados = 2/16 = 0.125`.

De ahí la regla que gobierna la publicación: **un informe técnico sólo constituye evidencia si `re-anclables / citados = 1`.** Este informe cita únicamente piezas que un tercero puede volver a medir: las cuatro identidades de la sección 3, la cadena por revisión de la sección 7 y las revisiones de git de la sección 2. La bitácora interna —útil e intacta— es memoria forense de la construcción, no evidencia de tercero; se conserva donde nació y no se deposita como prueba.

## 11. Lo que este informe NO certifica

- **Corrección del contenido.** Los metros cuentan presencia, identidad e integridad; no juzgan si la física, los preregistros o las mediciones del objeto son correctos. Un `VERDE` dice *idéntico a lo sellado*, no *cierto*.
- **Autovalidación.** El objeto y su verificador fueron escritos por la misma mano; el auditor externo reduce ese sesgo —vive fuera, no puede re-sellar el objeto— pero no lo elimina. Un instrumento no es su propio testigo.
- **El piso.** `PISO=25` es una cota **declarada** en la cabecera del auditor, no una cota derivada del objeto. Informa; no protege por sí misma. Lo que protege es el conteo de cobertura y la partición, que sí se miden.
- **El motor M1.** Los dos scripts declaran dos motores (`Darwin` = M0, `Linux` = M1) y esta corrida certifica **M0**; la ruta M1 está declarada por el mismo código y no se ejercitó aquí.
- **El binario de custodia.** El verificador comprueba por sha256 la presencia del binario de `gitleaks` en el PATH (constante del metro `f414bc2fb952be6c`, ~15,3 MB): se verifica su identidad, **no se copia ni se deposita**. Su peso —unas 46 veces el del objeto— queda declarado como decisión abierta, no como omisión.
- **La nomenclatura.** Existen divergencias conocidas entre la especificación escrita y el disco en los nombres de algunas piezas; se declaran pendientes y **no** se corrigen aquí, porque `bundle/` es inmutable.

## 12. Cómo citar

Objeto auditado: repositorio `sfqed-paper`, rama `main`, revisión `000916239dd2f013b5e7417281551ae32119e9db`; directorio `bundle/` con manifiesto `HASHES.sha256` = `0ce97cf9d8c44987` (34 entradas) sobre 35 hojas.

Pre-print asociado: DOI `10.5281/zenodo.23289363`. Depósito relacionado declarado en el registro vivo: `10.5281/zenodo.23288831`.

Este informe: `BUNDLE_VERIFICATION_REPORT_20261011.md`, raíz de `sfqed-paper`, junto a `README.md` y `METHODOLOGY_AND_BOUNDARIES.md`. Se publica bajo licencia CC-BY-4.0, autoría de José Alexis Román Martínez, Platino Labs.

Reproducir antes de citar: los tres comandos de la sección 4, en la revisión nombrada arriba. Si algún resultado difiere del de la sección 9, la cifra vigente es la del lector.
