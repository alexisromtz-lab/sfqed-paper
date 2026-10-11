# MOTORES · sello M0 (Darwin/BSD) y motor canónico (GNU/Linux)

```
T_UTC 2026-10-11T05:54:46Z
UNIVERSO DECLARADO: el anfitrion de esta sesion (uname/bash/python/shasum/gitleaks) + el arbol de
  sfqed-paper sin .git (26 archivos de bundle/ + 110 de sim/ + el resto) + el crudo
  /tmp/motores_medida_20261011.txt.
MOTOR: shasum -a 256 | wc | grep -cE | python3 -B | command -v.
UNIDAD: archivo | linea | byte | version.
VENTANA: el T_UTC de arriba. Toda cifra de conteo caduca al escribirse.
LECTURA SOLO.
```

Ratificación del dueño, 2026-10-11: **el motor canónico de registro pasa a GNU/Linux
(`.#gnu` = `#default`)** y **todo lo medido hasta hoy queda sellado como `M0`
(Darwin/BSD)**. Este archivo es el cuerpo normativo; viaja con el repo. El pin es
`flake.nix` (ver 4).

---

## 1 · Sello M0 · Darwin/BSD (identidad medida)

| pieza | valor medido `T_UTC 2026-10-11T05:54:46Z` |
|---|---|
| kernel / arco | `Darwin 25.5.0 arm64` (RELEASE_ARM64_T8103) |
| shell de los gates | `GNU bash, version 3.2.57(1)-release (arm64-apple-darwin25)` |
| shell interactiva | `zsh 5.9` |
| awk | BSD `awk 20200816` |
| python / numpy | `python 3.14.7` (homebrew, `/opt/homebrew/bin/python3`) · `numpy 2.4.6` |
| motor de hash del gate | `shasum -a 256` = `/usr/bin/shasum` (BSD/Perl) |
| gitleaks | `/opt/homebrew/bin/gitleaks` (fuera del repo; el bundle mide su presencia y su hash de casa) |
| git / jq | `/usr/bin/git` · `/usr/bin/jq` |
| nix / docker / podman | **AUSENTES** |

**Alcance del sello.** Todo artefacto de `sfqed-paper` con fecha ≤ 2026-10-11 se lee
como `M0`, esté o no etiquetado. `M0` no se degrada por esto: se **protege** — sin la
etiqueta, esas mediciones viajarían como si el piso fuera neutral.

**Trampa declarada del sello.** Este macOS 26 **sí** trae `/sbin/sha256sum` (medido).
Eso **no** vuelve GNU al motor: el hash que el gate usa es `shasum`, y así lo declara
el propio verificador en su encabezado. Un binario GNU presente **no** es un motor GNU.

---

## 2 · Motor canónico · GNU/Linux (`.#gnu` = default)

Por qué esta partición y no la inversa:

1. **La portabilidad no puede exigir hardware propietario.** Si el registro quedara en
   Darwin/BSD, todo tercero que clone la flake en un servidor Linux correría el *control
   secundario* y creería estar corriendo la verdad del proyecto.
2. **Higiene de linaje (append-only).** Declarar la serie previa como `M0` con fecha,
   arquitectura y hashes no la degrada: la fecha. Forzar una equivalencia ficticia
   entre BSD y GNU sería lo que rompe la trazabilidad.
3. **El primer experimento de la flake sale gratis.** `.#gnu` sobre el bundle es de
   hecho un **ensayo de invariancia inter-motor**: si reproduce los números de `M0` en
   las tolerancias pre-registradas, la física del modelo queda demostrada independiente
   del sistema operativo; si diverge, el fallo del METRO queda aislado en la capa del
   SO **antes** de tocar código de física.

Consecuencia: los artefactos **nuevos** se firman en GNU; `M0` pasa a **control**.

---

## 3 · Cláusula `MOTOR` (el tercer declarado que faltaba)

La línea declarada de toda medición gana un tercer campo. Nada más: **no es campo
nuevo, es el declarado que faltaba** junto a `UNIVERSO DECLARADO` y `UNIDAD`.

```
UNIVERSO DECLARADO: …   MOTOR: M0|GNU|M0-DIVERGENTE|BSD-NO-REPRODUCIBLE   UNIDAD: …   VENTANA: <T_UTC>
```

- La etiqueta **se mide, no se asume**: la emite la shell de la flake
  (`MOTOR_ETIQUETA`) o la deriva `tools/sello.sh` del anfitrión.
- `GNU` = piso de la flake. `M0` = anfitrión darwin **verificado** (shasum BSD + bash
  3.2.57 resueltos por PATH). `HOST-GNU` = linux **sin** pin: se declara, no se sella.
- El verificador ya declara su propio `MOTOR:` interno (`shasum -a 256 | cmp | grep -F
  | python3 -B | git -C`). La cláusula añade el **piso**, no lo repite.

---

## 4 · Invocación canónica, tricotomía y el pin

`flake.nix` es el **único** archivo declarativo de la raíz y gobierna también el OCI
(`packages.oci` vía `pkgs.dockerTools.buildLayeredImage`): **no existe ni debe existir
un Dockerfile paralelo**.

```
nix develop                 # == .#gnu  (piso canonico: GNU coreutils/findutils/grep/bash, python fijado)
nix develop .#bsd           # Darwin: PATH del anfitrion, sella M0 por MEDIDA · Linux: BSD-NO-REPRODUCIBLE
nix build .#oci && docker load < result
docker run --rm -i --network none sfqed-paper-verificador:20261011 </dev/null
```

- **RC sin traducción:** 0 = verde · 1 = fractura del objeto · 2 = contrato roto (metro
  ilegible). El `Entrypoint` corre `/bin/sh /bundle/verificar.sh` — el intérprete del
  shebang, PID 1, **sin envoltorio que colapse el RC** (no hay `|| true`, no hay pipe,
  no hay `tee`).
- **Corrección declarada:** `docker run -T` **no existe** (`unknown shorthand flag: 'T'`;
  `-T` es de `docker compose run`). Lo que se busca —no pseudo-TTY— es el *default* de
  `docker run`: **no se pasa `-t`** (`-t` fusiona stdout y stderr). `-i` + `</dev/null`
  cierra el stdin de forma explícita. `--network none` es añadido mío, declarado: un gate
  sin red no puede devolver verde por haber consultado algo de afuera.
- **Pre-registro falsable de la primera corrida:**
  - `.#gnu` sobre el repo con `.git` → esperado `VEREDICTO: VERDE · RC=0`.
  - `packages.oci` (bundle sin `.git`) → esperado `VEREDICTO: VERDE PARCIAL · RC=0` con
    **N ≥ 1** bloques NO MEDIDOS: sin repo git la custodia no se puede auditar.
  - Si `.#gnu` devuelve **RC=2**, los sospechosos declarados son, en orden: `shasum`
    ausente (`pkgs.perl`) y `gitleaks` ausente. Eso es **hallazgo del METRO**, no del
    objeto: se declara y **no se tapa con un shim**.
- **Estado del pin:** `flake.lock` **AUSENTE** ⇒ el pin está **ABIERTO** (una URL de
  canal flotante no es un pin). Y `nix` está AUCSENTE en `M0` ⇒ la flake **no ha sido
  evaluada**. Su primer evaluador es el primer `nix develop`.

---

## 5 · Protocolos de reducción de contexto (ratificados)

**5.1 · Línea atómica.** Toda verificación responde, en el chat, con **una** línea y la
ruta del crudo:

```
VEREDICTO: <palabra del verificador> · RC: <0|1|2> · MOTOR: <etiqueta> · SHA16: <sha16 del crudo>
CRUDO: <ruta absoluta>
```

Corrección declarada al vocabulario propuesto (`VERDE|FRACTURA|FALLO_METRO`): el
vocabulario es **del verificador**, no nuestro. `FRACTURA` = *FRACTURA del objeto*;
`FALLO_METRO` = **`CONTRATO ROTO`** (su palabra, RC=2); y **`VERDE PARCIAL` se conserva**,
no se redondea a `VERDE` — redondearlo sería declarar verde lo que no se midió.

**5.2 · Prohibido volcar registros.** Cero `tail` y cero lecturas de logs dentro de la
ventana de contexto. La inspección se hace por **conteo** (`wc -l`), **marca de fin**
(`RESUMEN`, `VEREDICTO`) y **código de salida**. El cuerpo vive en `corridas/<T>_<MOTOR>.txt`.

**5.3 · Punteros de índice.** `INDEX.md` en la raíz: metadatos por referencia, sin
recorrer el árbol. `el puntero viaja, el cuerpo no`.

**5.4 · Compuerta a código compilado (congelada).** El desarrollo numérico permanece en
**NumPy** hasta que se cumplan **las tres**, en este orden:

1. la **perilla de resolución** exista en la CLI — hoy **0** (medido: `add_argument('--(n|nx|ny|nt|steps|res` en `sim/maxwell2d.py` = 0 líneas);
2. **`segundos/paso`** se escriba en el jsonl de telemetría — hoy el único `.jsonl` bajo
   `sim/data` **no tiene campos de tiempo** (0 coincidencias;
   `sim/data/sigma_phi/telemetria_circular_sigma_phi_20261011.jsonl`, 2 l, 649 B, sha16 `34cb45c55fcc8937`);
3. una corrida en malla **480 × 480** **supere** el umbral de tiempo de integración que
   se pre-registre **antes** de correrla.

Y el piso GNU usa `mkShellNoCC`: **no trae compilador**, así que la compuerta no se puede
saltar por accidente desde el piso.

---

## 6 · Lo que NO queda sellado (declarado, no reparado)

- `flake.nix` **escrito y no evaluado** (`nix` AUSENTE en `M0`); `flake.lock` **ausente**.
- El bundle **en disco no es el bundle de `HEAD`**: `git status` marca ` M` en
  `bundle/00_INDICE.md`, `bundle/HASHES.sha256`, `bundle/verificar.sh`, `main.tex`,
  `main.pdf`. Los sha16 de §7/`INDEX.md` son los del **disco** en esa ventana, no los del
  commit `d4691d0`. Se declara; no se adjudica.
- `sim/lector_invariantes.py` (`635 l`, sha16 `9fab4e04d281d3cc`) sale **RC=2** con
  `--modos colineal contra --ns 1 2 4 8 16 --verbose`. Causa sin diagnosticar.
- El crudo del banco must-fail **pre-fix** no se conservó: esa cifra no se puede volver a
  medir. No se reconstruye; se declara.

---

## 6.A · Enmienda medida (T_UTC 2026-10-11T06:00:43Z) — la colisión de manos y el sello medido

**Colisión, declarada por slug completo.** `flake.nix` **no es de esta ventana**: otra mano
lo escribió a `2026-10-11T05:56:54Z` (**137 l · 6 570 B · sha16 `feef2fd47f6f3d51`**), unos
2 min **después** de que la medición de `05:54:46Z` lo declarara AUSENTE y ~30 s **antes** de
mi lote de tres archivos. Mi creación fue **rechazada** (`File already exists`): nada mío lo
sobrescribió. Lo leí completo y lo **completé de forma aditiva** (4 ediciones, **cero bytes de
su texto reescritos**):

1. `export MOTOR_ETIQUETA=GNU` en `devShells.default`;
2. ídem en `devShells.gnu`;
3. en `devShells.bsd`, etiqueta **medida** (condición: `uname -s` = `Darwin` **y**
   `command -v shasum` = `/usr/bin/shasum` → `M0`; si no, `BSD-NO-REPRODUCIBLE`), declarada
   como medida y no asumida;
4. la mitad **OCI ratificada** (`packages.oci = pkgs.dockerTools.buildLayeredImage` sobre un
   `buildEnv` con la **misma lista `motorGnu`** que `.#gnu`, `pathsToLink = [ /bin /lib /share ]`,
   `Entrypoint = [ /bin/sh /bundle/verificar.sh ]`, `WorkingDir = /bundle`,
   `Env = [ PATH=/bin · MOTOR_ETIQUETA=GNU · TZ=UTC ]`, `Labels` = título/versión/revisión de la
   imagen + `sfqed.motor` · `sfqed.motor.referencia` · `sfqed.gate` · `sfqed.universo`), más la
   corrección `-T` declarada y el pre-registro falsable de §4.

**Identidad post-edición (medida, no citada):** `224 l · 11 450 B · sha16 `cc770b142b93f88b` ·
mtime `2026-10-11T05:58:17Z`. Delimitadores balanceados (`{ }` 16/16 · `[ ]` 8/8) contados por un
script que **no es un parser** — declarado como tal. Sigue **sin evaluar** (`nix` AUSENTE) y
`flake.lock` sigue **AUSENTE**: el pin continúa abierto. **No se escribió `Dockerfile` paralelo**
(la palabra aparece **1** vez en la flake, y es justamente la línea que declara que no existe).

**Primera corrida del sello — y un defecto medido del propio sello.** `sh tools/sello.sh` →
crudo `corridas/20261011T055826Z_M0.txt` (4 872 B, sha16 `797e9b08ff0a2070`). La línea salió
`VEREDICTO: VERDE · · RC: 0`: un **separador colgante**, porque mi `sed` cortaba en `RC=` y
dejaba el `·` que lo precede. Es la familia del rótulo que afirma lo que la línea siguiente
desmiente, un piso abajo: **el defecto era del metro, no del objeto**. Junto a él, dos defectos
más del mismo instrumento: el `VERDE PARCIAL` del verificador habría perdido su discriminador
(el conteo de bloques NO MEDIDOS), y la leyenda decía «sin flake» con la flake ya en disco.

**Reparado y declarado** (`tools/sello.sh`, 66 l · 3 006 B · sha16 `a538e8eed904a635`): el
discriminador se **recose desde el `RESUMEN`** (`no_medido=N`, medido, no inventado).

**Segunda corrida (sello reparado, `T_UTC 2026-10-11T06:00:43Z`):**
`VEREDICTO: VERDE · RC: 0 · MOTOR: M0 · SHA16: 8a63de561cbe62af` · crudo
`corridas/20261011T060043Z_M0.txt`. La custodia quedó **medida** (git y `gitleaks` presentes ⇒
sin `no_medido`). **Los dos crudos se conservan** — el defectuoso y el reparado: junto a la foto
previa del objeto se guarda la del instrumento.

**Custodia de los crudos — cerrada (orden del dueño, `T_UTC 2026-10-11T06:18:14Z`).** El commit
`6b329189deaf09d4` citaba `8a63de561cbe62af` y el directorio `corridas/` no estaba ni versionado
ni ignorado: en un clon la cita **no resolvía**. Es deuda de la **letra ya publicada**, no de un
objeto en vuelo, y se cierra **versionando el par completo**: `corridas/20261011T055826Z_M0.txt`
(sha16 `797e9b08ff0a2070`) y `corridas/20261011T060043Z_M0.txt` (sha16 `8a63de561cbe62af`),
**70 l · 4 872 B cada uno**, medidos a `06:18:14Z` — no citados. Conservar sólo el reparado
habría borrado del registro la única foto del **defecto del instrumento**. `.gitignore` **no**
gana una línea para `corridas/`: la opción «subproducto efímero» se **declina**, y se declara
declinada: los crudos no son reproducibles **como par** — el pre-fix no se re-corre.

**Lo que esto NO cierra (declarado, no adjudicado).** La reconciliación del manifiesto de
`bundle/` queda **postergada a propósito**: `verificar.sh` es el **instrumento que produjo los
dos crudos**; cambiarlo antes de fijar los crudos habría dejado al par defecto/reparación **sin
referente**. Y `bundle/` sigue vivo en el árbol de trabajo (` M` ×3 más huérfanos sin custodiar):
su conteo de archivos, el número de entradas del manifiesto y la cláusula de cardinalidad del
verificador **se miden en el acto de escribir** — nunca se heredan de este párrafo.

---

## 6.B · Fe de erratas aditiva (T_UTC 2026-10-11T06:28:32Z–06:28:49Z, `HEAD` `85754379d6e4714d`) — el estado de la máquina manda sobre la narrativa previa

**Procedimiento (ratificado por el dueño, `T_UTC 2026-10-11T06:24Z`).** Cuando un **artefacto
commiteado** y un texto normativo anterior se contradicen, **el artefacto se queda** y el texto
recibe **fe de erratas aditiva**; **nunca un revert**. `§6.A` **no se edita**: su letra queda
como estaba y esta sección la **supersede por declaración**. Un revert habría borrado del
registro la decisión que sí se tomó.

**1 · La frase superada.** `§6.A` cierra su párrafo de custodia así: «`.gitignore` **no** gana una
línea para `corridas/`: la opción «subproducto efímero» se **declina**, y se declara declinada».
Era **verdadera** en su ventana (`T_UTC 2026-10-11T06:00:43Z`) y dejó de serlo **~22 min
después**, por otra mano, en el commit `872cd6461f3847fb` (`2026-10-11T06:22:33Z`, «`corridas/`
fuera del universo del bundle: regla selectiva en `.gitignore` del raiz»).

**2 · Lo que la máquina dice (medido, no citado; motor `git`/`wc`/`shasum`/`grep -n`, ventana de
esta sección).**

| objeto | `§6.A` (06:00:43Z) | `HEAD` (medido) |
|---|---|---|
| `.gitignore` | 16 l · 248 B · `d59fda8121906275` | **27 l · 924 B · `71b469307c641708`** |
| líneas con `corridas` | 0 | **4** — l.17 comentario («efímeras por diseño») · l.21 `corridas/*` · l.26 y l.27 las dos excepciones M0 |

**3 · Por qué no es una contradicción de fondo.** `§6.A` **declinó la regla** por una razón de
**reproducibilidad**, y esa razón **sigue en pie**: la regla que entró no la toca. Lo que entró no
afirma reproducibilidad — declara `corridas/` como **salida local de `tools/sello.sh`, efímera por
diseño**, y **conserva versionados los dos crudos M0**. La regla declinada y la vigente **no son
la misma regla**: la declinada era «una regla en lugar de la reproducibilidad»; la vigente es una
**frontera de árbol de trabajo**. Se declara el **cambio de suelo**; no se adjudica el motivo de
la otra mano.

**4 · Lo que la frontera NO toca (medido en el acto, mismos motores).** `bundle/` **35 piezas**
por `os.walk` = **35** por `git ls-tree -r HEAD bundle`; `HASHES.sha256` **34** entradas ⇒
`34 + 1 = 35`, el manifiesto sin entrada propia. `corridas/` **2** archivos en `HEAD`.
`git status --porcelain -uall` filtrado: **cero** entradas para `bundle/`, `corridas/` y
`MOTORES.md`; sólo ` M main.pdf` y ` M main.tex` (de otra mano, declarados). El universo del
bundle sigue siendo el suyo y **no contiene** `corridas/`.

**5 · Segunda afirmación de `§6.A` superada por el mismo hecho (declarada, no editada).** `§6.A`
cierra diciendo que `bundle/` «sigue vivo en el árbol de trabajo (` M` ×3 más huérfanos sin
custodiar)». Medido en la ventana de esta sección: **`bundle/` sin entradas en el porcelain**. La
reconciliación que `§6.A` **postergó a propósito** la ejecutó otra mano en `10db313` (`06:19:05Z`)
+ `872cd64` (`06:22:33Z`); esta ventana la **verifica corriendo el instrumento**, no la re-ejecuta.
La regla que `§6.A` dejó escrita sigue mandando: esas cifras **se miden en el acto de escribir y
no se heredan** — esta tabla incluida, que caduca con el próximo `git add`.

**6 · Frontera de esta sección.** No edita `§6.A`. No revierte `.gitignore`. No escribe en
`bundle/`. No toca `main.tex` ni `main.pdf`. `MOTORES.md` estaba limpio al escribir:
`7233902d98e5b541` en `HEAD` = `7233902d98e5b541` en disco. Y `HEAD` **se movió otra vez** entre
la medición previa (`872cd6461f3847fb`, `06:25:58Z`) y ésta (`85754379d6e4714d`): la ventana
previa queda declarada como **caducada a los ~2 min**, no adjudicada.
