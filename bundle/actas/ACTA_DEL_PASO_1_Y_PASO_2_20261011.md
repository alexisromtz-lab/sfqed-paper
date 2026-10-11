# Acta del Paso 1 y del Paso 2 — el objeto se congela y el intérprete se mide en M0

**Qué cierra esta acta.** El cierre de tres pasos que el dueño dictó («no se congela el intérprete sobre
un objeto que todavía se está moviendo»). Aquí quedan medidos el **Paso 1** (sincronización del objeto y
cierre documental) y el **Paso 2** (validación inicial en M0). El **Paso 3** (`flake.nix` y verificación
cruzada M0 → GNU) **no** se cierra aquí: se declara abierto y con su obstáculo medido.

```
UNIVERSO DECLARADO: bundle/ = 34 archivos = 33 declarados en HASHES.sha256 + el propio manifiesto
                    (+1 = esta acta, que entra al manifiesto después de escribirse)
MOTOR:              shasum -a 256 · cmp · sed -n | grep -qF · awk · git -C · sh -n
UNIDAD:             archivo (inventario) · línea (anclas) · byte (identidad)
VENTANA:            el reloj UTC de cada comando; toda cifra de este acta caduca al re-sellar el
                    manifiesto, y por eso cada una viaja con su hora
T_UTC de redacción: 2026-10-11T06:10Z
```

## 1. Paso 1 — lo que se movió, medido

| Movimiento | Antes | Después | Motor |
|---|---|---|---|
| Anclas en `verificar.sh` | 26 filas | **38** filas (`+12`) | `awk` entre `FIN_ANCLAS` |
| Universo declarado | 26 archivos / 25 declarados | **34 / 33** | `find . -type f ! -name HASHES.sha256 \| wc -l` |
| `HASHES.sha256` | 25 líneas | **33** líneas, `OK=33 FAILED=0` | `shasum -a 256 -c` |
| `verificar.sh` | 270 l · `eb14ce18e21c6b94` | **330 l · `f2b3459f8a199928`** | `wc -l` · `shasum` |
| `00_INDICE.md` | 234 l · 8 cabezas | **313 l · 9 cabezas** | `grep -c '^## '` |

**Las 8 piezas entraron por copia.** `cp -p` desde `sim/` y `cmp` sin divergencia **8/8**; el sha256 de
cada copia se comprobó idéntico al del original **antes** de declararla. Copiar no es citar: el bundle no
apunta al objeto vivo, lo congela. Las 12 anclas nuevas se midieron con el **mismo motor del bloque [4]**
(`sed -n "${lin}p" | grep -qF`) antes de escribirlas: `ok=12 rojas=0` a `2026-10-11T06:02:16Z`. Se
anexaron **al final** de `FIN_ANCLAS`, nunca en medio: el caso E del banco lee la **primera** fila, y
reordenar la tabla habría movido el objeto que ese caso mide.

**Un ancla auto-referente caducó al escribir.** `verificar.sh|103|MANIFIESTO declara 0 objetos` apuntaba a
una línea que el encabezado nuevo empujó a la **129**. Re-medida y re-escrita. Es la regla de la casa otra
vez, y ahora dentro del propio verificador: *el acto de escribir mueve la cifra que el escrito postula*.
Un ancla auto-referente es el instrumento midiéndose a sí mismo: se corrige **contando la línea**, no
leyendo el párrafo. Verificación posterior de las 38 filas: `ok=38 rojas=0`.

**El contrato de cabecera entró al veredicto.** Los tres desenlaces emiten ahora
`RC: 0 · MOTOR: <M0|M1|M?> · SHA16: <sha16 del manifiesto> · T_UTC: <sello>`; los cinco RC=2 tempranos
siguen imprimiendo `RC=2` **sin** encabezado de contrato, porque allí el metro que calcula el SHA16 puede
ser justamente el que falta (caso C del banco: PATH sin `shasum`). El núcleo se mide con
`/usr/bin/uname -s` en **ruta absoluta**, no desde el PATH: el banco corre el verificador con un PATH
falso que **no trae `uname`**, y un metro que leyera su propio PATH mediría al banco en vez del núcleo.

## 2. Paso 2 — M0, con el contrato exacto

```
T_UTC arranque = 2026-10-11T06:08:37Z      T_UTC cierre = 2026-10-11T06:08:38Z
rc = 0
VEREDICTO: VERDE · RC: 0 · MOTOR: M0 · SHA16: 3866dbd1b785ea15 · T_UTC: 2026-10-11T06:08:38Z
RESUMEN  verde=52 · rojo=0 · no_medido=0 · anclas=38 ok=38 rojo=0
crudo: /tmp/verif_paso2_M0_0607Z.txt · 84 l · sha16 5664ee0894677da6
```

El encabezado declara `MOTOR_ID: … aqui: M0 (Darwin 25.5.0)` ⇒ el núcleo **sí se midió**, no se supuso.
La regla del cierre se cumple: **RC=0 en M0** y no se avanzó a la flake con un RC distinto.

**Una trampa de mi propio metro, en el acto.** El primer conteo imprimió `FAILED=1` sobre un crudo que
dice `entradas en el manifiesto = 33 · OK = 33 · FAILED = 0`: mi `grep -c 'FAILED'` había contado la
**etiqueta**, no el veredicto. El objeto no tenía fallas; el cero/uno era del patrón. Se deja escrito
porque es la familia que esta casa ya tiene pagada (el rótulo leído como medición).

## 3. El gate externo: el banco must-fail vuelve a 7/7

```
T_UTC = 2026-10-11T06:08:48Z → 2026-10-11T06:08:51Z      rc_banco = 0
RESUMEN BANCO  casos=7 · conformes=7 · rojos=0
VEREDICTO BANCO: VERDE (7/7) · los 7 codigos de salida son los estrictos
crudo: /tmp/banco_0609Z.txt · sha16 a58afb530d31ddeb
```

El caso **E** imprimió `filas de la tabla = 38`, es decir el banco **leyó** la tabla enmendada y siguió
enrojeciendo por la causa correcta (`ya no dice`, RC=1). El patch del verificador **no** relajó ningún
caso: A `FAILED` · B `MANIFIESTO` · C `shasum ausente` · D `falta …` · E `ya no dice` · F `PARCIAL` ·
G `gitleaks ausente`. Que el banco siga verde importa porque es el **único** gate que juzga al
verificador desde afuera; su validez no la firma el verificador.

## 4. Límites declarados (abiertos, no ensanchados en silencio)

1. **Fuera del bundle**: `sim/data/invariantes/crudo_lector_invariantes.json` (`96f66e9cb30a56ed`), el
   crudo del lector de invariantes. Las actas que lo citan **sí** están dentro: el testigo de esa lectura
   vive fuera de la caja que lo cita. Se declara como frontera en vez de copiarlo por conveniencia.
2. **`flake.nix` ya existe** (137 l · `feef2fd47f6f3d51` · mtime `05:56:54Z`), escrito por otra mano
   **fuera de orden** respecto de esta secuencia. Entra en el Paso 3, donde se **reconcilia**, no se
   reescribe de cero. `flake.lock` no existe.
3. **`nix` NO está instalado en este anfitrión** ⇒ el Paso 3 no se puede cerrar desde M0; su verificación
   cruzada exige la máquina con `nix develop .#gnu`.
4. **El hash del manifiesto cita su instante.** `3866dbd1b785ea15` es el manifiesto **antes** de que esta
   acta entre a él; al re-sellarlo cambia. El valor autoritativo es el que imprime `./verificar.sh`, y el
   propio verificador lo declara «no circular: lo imprime el verificador».
5. **Los crudos viven en `/tmp`**: `/tmp/verif_paso2_M0_0607Z.txt` y `/tmp/banco_0609Z.txt`, con los
   sha16 de arriba. Se citan con su hora porque `/tmp` no es archivo: lo que no se copia, se cita.

## 5. Apéndice — el objeto se movió **mientras** se medía (declarado, no adjudicado)

`verificar.sh` creció de **330 l · `f2b3459f8a199928`** a **387 l** entre `06:08:51Z` y `06:10:02Z`
(mtime medido): **otra mano** le añadió el bloque **[2b] COMPLETITUD (fail-closed)** (l.147–164) y un
contador de cobertura en `python3`. Su propio comentario declara el estado que lo motivó: «34 archivos
reales contra 25 declarados ⇒ 8 huérfanos viajando verdes». La tabla de §1 mide el objeto **de su hora** y
no se edita (es el registro de lo que había cuando se escribió). Tras esa llegada se corrigió el universo
declarado en los **dos** textos —`verificar.sh:74` y `00_INDICE.md:14` pasan a **35 archivos / 34
declarados**— y se regeneró el manifiesto: **34 entradas**, `OK=34 FAILED=0`, sha16 `bd4db023af5e25c0`.
Corrida final sobre el objeto ya quieto (`06:10:40Z`→`06:10:41Z`): `rc=0`,
`VEREDICTO: VERDE · RC: 0 · MOTOR: M0 · SHA16: bd4db023af5e25c0 · T_UTC: 2026-10-11T06:10:41Z`,
`verde=53 · rojo=0 · no_medido=0 · anclas=38 ok=38 rojo=0`, y **[2b] en verde**:
`CONTEO reales=35 declaradas=34 huerfanos=0 · OK: cobertura completa`. Crudo `/tmp/verif_final_0612Z.txt`
· 87 l · sha16 `67f4690d438769df`. Este apéndice **no cita el manifiesto que lo contendrá** —el que entra
después de escribirlo—: es el mismo límite 4, un piso más abajo, y por eso el sello que vale es el que
imprime `./verificar.sh` después de la última escritura.
