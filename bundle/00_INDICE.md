# ÍNDICE 0 — SFQED: el corpus que se mide a sí mismo

**Qué es esta pieza.** El árbol canónico de reproducibilidad de la línea SFQED: los pre-registros que
fijan las bandas *antes* de la primera cifra, las actas de auditoría que registran lo que se midió, los
medidores que produjeron esas cifras y los instrumentos de custodia que impiden que el repo publique un
secreto. No es un resumen de los resultados: es el **aparato de medida**, con la dirección de cada
afirmación.

**Cómo se verifica.** Un solo comando, `./verificar.sh`, que hace cuatro fases y sale con un código de
salida que no admite interpretación: `0` verde · `1` fractura del objeto · `2` contrato o medidor roto.
No hay puerta de escape que devuelva verde.

```
UNIVERSO DECLARADO: 35 archivos bajo bundle/  =  34 declarados en HASHES.sha256 (todos menos el propio
                    manifiesto)  +  HASHES.sha256 (que no puede declararse a sí mismo)
                    Era 26 / 25 antes de la enmienda de esta madrugada, que incorporó las 8 piezas de
                    evidencia de la Pestaña 2 (§9). 26 + 8 = 34 y 25 + 8 = 33; con el acta del Paso 1 y
                    del Paso 2 —la novena pieza de §9— quedan 34 y 35, y el orden es el de la aritmética:
                    la cifra cuadra con el inventario, no con la memoria.
BANCO:              tests/bench_must_fail.sh = 7 casos must-fail, cada uno sobre una copia efímera
                    del bundle completo. NO se invoca desde verificar.sh: un verificador no se
                    valida a sí mismo. Aquí solo se declara su hash, como el de cualquier pieza.
MOTOR:              shasum -a 256 · cmp · grep -nF · python3 -B (stdlib) · git -C
MOTOR_ID:           M0 = Darwin/anfitrión · M1 = GNU/Linux (`nix develop .#gnu`) · M? = núcleo no medido.
                    El núcleo se MIDE con /usr/bin/uname -s en ruta absoluta, nunca desde el PATH:
                    el banco corre el verificador con un PATH falso que no trae `uname`, y un metro
                    que leyera su propio PATH mediría al banco en lugar del núcleo. El encabezado del
                    contrato (MOTOR/SHA16/T_UTC) no se emite en los RC=2 de contrato roto: allí el
                    motor que produce el SHA16 puede faltar (caso C: PATH sin `shasum`) y un contrato
                    que no se puede medir no se imprime.
COPIA (no enlace):  las 8 piezas de §9 entraron al bundle por `cp` y su sha256 se comprobó idéntico al
                    del original en sim/ (8/8, `cmp` sin divergencia) ANTES de declararlas aquí. El
                    bundle no apunta al objeto vivo: lo congela. Copiar no es citar: la copia se
                    declara, o el hash certifica una copia que nadie nombró.
UNIDAD:             archivo (inventario) · línea (anclas) · byte (identidad de custodia)
VENTANA:            el reloj UTC que verificar.sh imprime en su encabezado; toda cifra de este índice
                    caduca al escribirse, y su hora es parte de la cifra
T_UTC de redacción: 2026-10-11T04:42:37Z   ·   enmienda (universo + §9): 2026-10-11T06:05Z
                    sha16 de este archivo: el que imprime ./verificar.sh
```

---

## 1. Falsos verdes: el veredicto que no discrimina y el cero que miente en silencio

| Afirmación | Ancla | sha16 | La línea dice (verbatim, cortado) |
|---|---|---|---|
| El veredicto del falsador **no discrimina**: tres objetos distintos salen **los tres VERDE** | `actas/AUDITORIA_DE_LA_ORDEN_FDTD_Y_ORDEN_CORREGIDA_20261011.md:69` | `c116adc522144837` | `sim/medidas_aN.csv` (canónico, lineal) … **0.500000** … `0 VERDE` |
| el mismo | `…:70` | `c116adc522144837` | `sim/medidas_aN_circular.csv` … **0.486414** … `0 VERDE` |
| el mismo | `…:71` | `c116adc522144837` | el mismo, **solo la fila N=1** movida a `170.5338023` … **0.499999** … `0 VERDE` |
| **El cero falso silencioso**: el umbral del barrido cayó una hora en el futuro y el crudo imprimió `(sin salida)` **sin imprimir el error de parseo** — un cero sobre una hora que tenía 10 archivos movidos | `…:333` | `c116adc522144837` | `date -u` imprime la cadena **en UTC** y el `-newermt` de BSD la **parsea en hora local** … imprimió **`(sin salida)`** … **miente en silencio** |
| El cierre de un barrido **se cuenta, no se lee** | `…:131` | `c116adc522144837` | **Cierre con conteo, no con lectura.** El barrido son **12 σ × 5 N = 60 filas**: se cuentan |
| La cifra caduca al escribirla: dos β distintas en la misma pasada, y la que se cita como «la última» hay que fecharla | `…:178` | `c116adc522144837` | **670 B · `62824875f8739c79` · β = 0.487693 · `desv` = 0.0418 — sin testigo vivo** |
| Una fila movida cambia el veredicto por debajo del umbral impreso (+4.821 %) y **sigue saliendo verde** | `…:182` | `c116adc522144837` | la fila N = 1 del circular vivo vale **178.7553300762** contra `a_ref = 170.5338023` ⇒ **+4.821 %** |

**Y el instrumento de esta misma pieza tenía el mismo defecto, medido y cerrado.** Un archivo JSONL de
**0 bytes** —cero medidas— devolvía `rc 0` (verde), contradiciendo la tesis del propio módulo («el
silencio no es una línea»).

| Afirmación | Ancla | sha16 | La línea dice |
|---|---|---|---|
| La guarda del caso vacío: `return 2` con mensaje al `stderr` | `instrumentos/telemetria_minima.py:340-341` | `8ed0d71af359ce63` | `CONTRATO ROTO: 0 lineas no vacias: el silencio no es una linea, y un archivo vacio NO es verde (cero medidas no pueden diferir)` |
| El `return` que la ejecuta | `instrumentos/telemetria_minima.py:348` | `8ed0d71af359ce63` | `return 2` |
| El control **must-fail** dentro del `selftest`: un validador que acepta todo no discrimina, así que el `selftest` crea un archivo de 0 bytes y **exige `rc == 2`** | `instrumentos/telemetria_minima.py:270` (y siguientes) | `8ed0d71af359ce63` | `def selftest() -> int:` |
| El motor de la verificación repite ese mismo control en vivo | `verificar.sh` (paso 1) | — (se imprime su sha16 en tiempo de corrida) | `selftest` con `control de archivo vacio: rc = 2` |

---

## 2. Muestreo estroboscópico: la rejilla no puede resolver el patrón que dice medir

| Afirmación | Ancla | sha16 | La línea dice |
|---|---|---|---|
| La sonda muestrea `i` en saltos de **40 celdas = 1 λ = exactamente 2 espaciamientos de λ/2** ⇒ cada muestra golpea **la misma fase**; la «envolvente suave» que se lee en la tabla **es aliasing**, no una envolvente | `actas/ADENDA_2_LECTURA_CONTRA_20261011.md:90` | `57f1b88a7f90efde` | `λ/2 = 20` celdas, los saltos de **40 celdas = 1 λ** … cada muestra de 40 golpea **la misma fase** … es **aliasing**, no una envolvente |
| La rejilla, en el código del medidor (mismo sha16 que citan las actas) | `instrumentos/medidores/maxwell2d.py:352` | `1db75ea7b0b8cba4` | `for i in (I_SL, I_SL + 20, I_SL + 40, IC - 80, …` |

---

## 3. Sesgos instrumentales: el rojo es del ancla, no del objeto

| Afirmación | Ancla | sha16 | La línea dice |
|---|---|---|---|
| **El `RC = 1` es del ancla, no del objeto.** El gate ancla en *una fila de la propia medición*; en la geometría contra esa fila **no puede existir** | `actas/ADENDA_LECTURA_CONTRA_20261011.md:31` | `23a10dd7bf3e12c2` | **El RC = 1 es del ancla, no del objeto.** `falsador.py` l.121–125: … `if ref is None: fails.append("sin N=1 …")` |
| el mismo, en el código del medidor | `instrumentos/medidores/falsador.py:125` | `f04551c7f19ce73a` | `fails.append("sin N=1 no se puede medir el cociente contra sqrt(N)")` |
| El rojo se reproduce y se declara con su control: el **sandbox sale verde** (`RC = 0`), y el gate **no es reutilizable entre pestañas** por diseño de su ancla | `actas/ETAPA1_CONTRA_REPORTE_20261011.md:114` · `…:117` | `a56341e5587d2b80` | `control del sandbox: --sintetico 0.5 → VEREDICTO: VERDE · RC = 0 (el sandbox funciona)` · `no es reutilizable entre …` |
| **Un testigo no se identifica por el nombre de su carpeta**: el archivo que la pasada anterior declaró «el canónico lineal viejo» tiene cabecera `pol = circular` | `actas/AUDITORIA_…20261011.md:176` | `c116adc522144837` | **(i) Falso: el testigo del canónico viejo.** … **No lo es**: su cabecera dice `pol = circular` |
| La β medida y sus bandas, en el reporte de la corrida | `actas/ETAPA1_REPORTE_20261011.md:30` · `…:31` | `7c2021694fec5a8d` | `beta = 0.500000000000` (pendiente log-log, 12 cifras). Bandas pre-registradas: verde `[0.45, 0.55]`, muerte `<= 0.35` o `>= 0.65` |

---

## 4. Pre-registros: la banda se declara antes de la primera cifra

| Afirmación | Ancla | sha16 | La línea dice |
|---|---|---|---|
| Banda verde | `preregistros/PROTOCOLO_1overN.md:45` | `adf0e6b08bf7638e` | `0.45 ≤ beta ≤ 0.55` → **VERDE** |
| Banda gris (no concluyente, se declara gris) | `…:46` | `adf0e6b08bf7638e` | `0.35 < beta < 0.45` ó `0.55 < beta < 0.65` → **ROJO** |
| Zona de muerte (escalado refutado) | `…:47` | `adf0e6b08bf7638e` | `beta ≤ 0.35` ó `beta ≥ 0.65` → **ROJO** |
| Que las bandas se fijaron **antes** de medir, junto con la tolerancia y la malla | `…:50` | `adf0e6b08bf7638e` | `Declarado *antes* de la primera cifra: la banda, la tolerancia 0.20 y la malla de …` |
| El umbral del nulo de σ–φ, para que el barrido **pueda** enrojecer | `preregistros/PREREGISTRO_SIGMA_PHI_20261011.md:46` · `…:55` | `51d6a0d06c802244` | `Umbral: sigma* tal que beta_LS = 0.45 => 0.554987 rad` · `Aceptacion: abs(beta) <= 3 SE. Este nulo SI puede enrojecer el barrido.` |
| **Un control que no puede diferir no es un nulo: es un candado** | `preregistros/PREREGISTRO_KERR_20261011.md:12` | `b6ffaddcf6e67df0` | `Un control que no puede diferir no es un nulo: es un candado.` |
| El piso numérico **se declara piso, no señal** | `…:21` | `b6ffaddcf6e67df0` | Ese `5.444e-10` es el piso de maquina del invariante y hay que declararlo como piso, no como senal. |

---

## 5. Custodia: el repo no puede publicar un secreto, y el gate se verifica midiéndolo

| Pieza | sha16 | Qué es |
|---|---|---|
| `instrumentos/custodia/gitleaks_casa.toml` | `2e03d8999823ab6e` | las reglas de la casa (idénticas al origen `primer`); **ninguna ruta en `allowlist`** |
| `instrumentos/custodia/pre-commit` | `b596865080c6415f` | hook *fail-closed*: si falta el binario o el metro falla, sale **2** |
| `instrumentos/custodia/pre-push` | `024903581d44d706` | idem, antes del push |
| `instrumentos/custodia/install.sh` | `40515cea38f9808c` | instalador (enlaza, no copia) |
| `instrumentos/custodia/instalar_en_repos.sh` | `edb1bd60fe3b5751` | instalador por repos, con aborto si el origen no coincide |

`verificar.sh` audita esto con `cmp` (byte a byte contra el repo anfitrión), no leyendo el mensaje de éxito
de ningún instalador: **un gate se verifica contando y comparando, nunca leyendo su propio «OK».**

Y la regla que lo cierra, tomada de lo ya pagado en esta casa: **un gate sin `assert` detrás informa, no
protege**; y un hook cuyo código de salida **2** el propio git colapsa a **1** son **dos unidades para un
solo hecho** — se declaran las dos.

---

## 6. Límites de esta pieza (declarados, no disimulados)

1. **No circularidad del manifiesto.** `HASHES.sha256` no puede declararse a sí mismo: sería un bucle
   insatisfacible. Por eso **este índice no cita el sha16 del manifiesto**; lo imprime `verificar.sh` en
   tiempo de corrida, y esa impresión es la declaración no circular. Todo lo demás **sí** está declarado,
   incluido `verificar.sh` (un manifiesto que no cubre a su verificador deja el verificador sin testigo).
2. **El bundle no es el árbol `sim/` completo.** Es el *aparato de medida*: pre-registros, actas, los dos
   medidores que las actas citan (`maxwell2d.py`, `falsador.py`) y el instrumento de telemetría. Los
   medidores se copiaron con `cp` y su sha16 **coincide con el que las propias actas ya habían declarado**
   (`1db75ea7b0b8cba4`, `f04551c7f19ce73a`) ⇒ la ancla del índice y la ancla del acta son el mismo objeto.
3. **Cero modificaciones a los archivos medidos.** Durante el sellado no se tocó ningún archivo de `sim/`
   ni de documentación: sólo se copiaron. La frontera se mantiene por diseño.
4. **Una cifra sin hora no es cifra.** Los `T_UTC` de las actas son los suyos, dentro de su propio texto;
   este índice no los re-fecha. Las horas de este archivo son dos y cada una se declara en su línea: la de
   redacción de arriba y la de la enmienda §7.
5. **Lo que este índice no afirma.** No afirma que β = 0.5 sea el resultado físicamente correcto: afirma
   que **3 objetos distintos producen el mismo veredicto**, que es una propiedad del **metro**, no del
   objeto. Distinguir esas dos cosas es el contenido entero de esta pieza.

---

## 7. El banco must-fail: quién mide al metro (enmienda de 2026-10-11T05:34:09Z)

**Qué es.** `tests/bench_must_fail.sh` es el banco que mide al verificador **desde afuera**. No se invoca
desde `verificar.sh`: un verificador no se valida a sí mismo (la ley que ya regía para el `selftest` del
medidor). Corre **7 casos**, cada uno sobre una copia efímera del bundle completo, y cada caso exige **el
código de salida estricto Y la causa impresa**: un caso que devuelve el código esperado por otro motivo no
discrimina, y entonces el banco no mide lo que dice medir.

| Caso | Defecto inyectado | RC exigido | Causa exigida |
|---|---|---|---|
| A | un byte invertido (tamaño conservado) en una pieza del manifiesto | 1 | `FAILED` |
| B | el manifiesto con **0 bytes** | 2 | `MANIFIESTO` |
| C | `PATH` restringido **sin `shasum`** | 2 | `shasum ausente` |
| D | el medidor de telemetría retirado | 2 | `falta instrumentos/telemetria_minima.py` |
| E | un ancla caducada, con el manifiesto **regenerado** para que el único defecto sea el ancla | 1 | `ya no dice` |
| F | un sandbox que **no es repo git**: la custodia no se puede auditar | 0 | `PARCIAL` |
| G | `PATH` sin `gitleaks`, con anfitrión git presente | 2 | `gitleaks ausente` |

**Los dos defectos que el banco encontró en el verificador (medidos, no supuestos).**

1. **Un manifiesto de 0 entradas devolvía `VEREDICTO: VERDE · RC=0`.** El bloque [2] compara `NOK + NMAL`
   contra el número de líneas del manifiesto: con cero objetos declarados eso es `0 + 0 == 0`, que **se
   satisface a sí mismo**, así que la rama de fractura nunca entra y el `else` imprime «los 0 archivos
   declarados coinciden con su hash». Es el mismo cuerpo que el medidor ya tenía escrito (`archivo vacio
   NO es verde`) **un piso arriba**: allí el objeto era la telemetría; aquí el objeto es el manifiesto.
   Cierre: `if [ "$NLINEAS" -eq 0 ]` → `CONTRATO ROTO` + `RC=2` (caso B).
2. **Con `no_medido=1` el veredicto salía como `VERDE` a secas.** El encabezado del propio verificador
   promete lo contrario (*«Sin repo git anfitrión, la custodia NO se declara verde: se declara NO MEDIDA»*),
   y esa promesa se cumplía **bloque por bloque** y se perdía **en el resumen**. Cierre: el adjetivo solo
   no se emite; con `RC=0` y `NOMED > 0` sale `VEREDICTO: VERDE PARCIAL · RC=0` y se dice cuál bloque no
   se midió (caso F). El `RC` ya era correcto: **lo que mentía era la palabra**.

**Los dos defectos del banco mismo** (el metro del metro; se registran porque los cazó el **conteo**, no la
lectura): (i) la extracción del ancla del caso E usaba un `sed` anclado que arrancaba en el **delimitador de
cierre**, así que el ancla salía vacía y el caso pasaba **por otro motivo** — corregido con una lectura
estructural que imprime el conteo de filas **medido en la corrida** (26 el 2026-10-11T05:34:23Z: cifra
viva, crece si crece la tabla, no rótulo); (ii) la lista de herramientas del shim se escribió
**sin `shasum` ni `gitleaks`**, así que el caso C no medía nada (faltaban por omisión en **todos** los
shims) y el caso G moría en la rama equivocada; **el `RC` solo habría declarado G verde: lo cazó la
aserción de causa.** El rótulo del shim imprime el conteo **medido** (18 herramientas menos la que se deja
fuera = 17), no un número fijo.

**Crudo, con su hora.** Antes de parchear el verificador: `casos=7 · conformes=3 · rojos=4 · casos rojos: B
E F G`. De esos cuatro, **B y F eran del objeto** (los dos defectos de arriba) y **E y G eran del banco**
(el metro del metro). Con el banco ya corregido y el verificador todavía sin parchear:
`casos=7 · conformes=5 · rojos=2 · casos rojos: B F` — exactamente los dos defectos del verificador. Con el
verificador parcheado: `VEREDICTO BANCO: VERDE (7/7) · RC=0`.

**Dos rótulos, uno corregido y otro no.** El encabezado de `verificar.sh` decía «Hace tres cosas» y
enumeraba **cuatro** fases (`[1]`…`[4]`): se contaron y se corrigió la palabra. La sospecha simétrica
—que el «17» del shim fuera un rótulo fijo— **se midió y era falsa** (la lista tiene 18, el shim excluye
una): no se «corrigió» nada, porque corregir sin medir es el defecto, no la reparación.

## 8. La reproducción: dos crudos se pueden re-correr y uno no (enmienda de 2026-10-11T05:55:16Z)

La diferencia entre los tres crudos que cita §7 no está en la cifra: está en sí el instrumento que la
produjo sobrevivió para volver a correrla.

**Reproducido (medido otra vez, no citado de memoria).** Árbol: una copia de `bundle/` con el
verificador **pre-fix** — `eb14ce18e21c6b94 · 270 líneas`, conservado en la foto previa
`/tmp/foto_previa_paso2_20261011T052913Z/` — y el banco **vivo** (`7f9a2e4a207f1580 · 166 líneas`),
porque del banco pre-fix no se guardó copia. El banco se invocó desde dentro del bundle copiado:

    sh /tmp/rep_previo/bundle/tests/bench_must_fail.sh > /tmp/banco_previo_repro.txt 2>&1

Crudo con su hora (`T_UTC = 2026-10-11T05:52:13Z`, la del propio encabezado; 33 líneas ·
sha16 `4f34b53f1a73dc4a`; el código de salida se leyó aparte = 1):

    bundle = /tmp/rep_previo/bundle
    sha16(verificar.sh)   = eb14ce18e21c6b94
    sha16(HASHES.sha256)  = 5bd43f2b7a49b632   <- manifiesto PRE-fix de la copia; el del bundle vivo era 3de1aba9d4ab3648 al medir, y cambia al re-sellar este párrafo: el acto de escribirlo mueve su propia cifra
    RESUMEN BANCO  casos=7 · conformes=5 · rojos=2
    VEREDICTO BANCO: ROJO (5/7) · casos rojos: B F

Coincide con lo que §7 ya citaba: la reproducción **no añade un caso, confirma uno**. Y los dos
sandboxes que el banco conservó dicen la causa **desde adentro**, sin pasar por el rótulo del banco:
caso **B** → `entradas del manifiesto = 0 · OK = 0 · FAILED = 0` con `VEREDICTO: VERDE · RC=0` (el
verde falso del manifiesto vacío); caso **F** → `entradas = 25 · OK = 25 · FAILED = 0` con
`VEREDICTO: VERDE · RC=0` **sin la palabra `PARCIAL`** (el defecto que sólo mentía en la palabra). Los
dos defectos quedan medidos por tres vías: el verificador, el banco, y el crudo que el banco conservó.

**No reproducible, y se declara.** El primer crudo (`casos=7 · conformes=3 · rojos=4 · casos rojos:
B E F G`) no se puede volver a correr: el banco defectuoso **no se conservó** (búsqueda de copias = 0)
⇒ de ese crudo quedan los rótulos, no el instrumento. Regla que fija el caso: **se copia el instrumento
defectuoso antes de corregirlo**, o la cifra que lo delata deja de ser verificable y pasa a ser
testimonio. Es la foto previa aplicada **al metro**, no al objeto.

**Trampa pagada en el acto: el universo del banco es su propia ubicación.** El banco no recibe la raíz
del bundle: la **deriva** de donde vive (su raíz es el directorio padre del directorio del script). Una
copia del banco puesta **al lado** de `bundle/` en lugar de dentro hace que el universo sea el
directorio contenedor: ese crudo dice `bundle = /tmp/rep_previo` (faltaba el `/bundle`), imprime
`shasum: /tmp/rep_previo/verificar.sh: No such file or directory` y los siete casos mueren con
`RC=127` ⇒ **7/7 ROJO**. El banco no miente —enrojece fuerte cuando está mal alojado— pero ese rojo es
**del metro, no del objeto**: midió su propia casa. Disposición correcta: `tests/` **dentro** del
bundle copiado.

**Forma del crudo, medida.** La causa por caso no usa ` - ` como separador: la línea es
`  B   entradas del manifiesto en el sandbox = 0 bytes` (tres espacios) y la siguiente
`  B   RC=0  esperado=2  causa [MANIFIESTO] -> ROJO`. Un patrón de lectura con ` - ` imprime **cero
líneas** sobre un crudo que sí las tiene: el cero era del patrón.

**Un cero que era del metro, otra vez.** El conteo de sandboxes conservados se hizo primero con
`find /tmp -maxdepth 1 …` y dio **0** con sandboxes vivos en disco (`/tmp` es symlink: el `find` de
macOS no sigue el punto de partida). Con `ls -d` y con `find /private/tmp` aparecen los **7** (los 2 de
esta corrida y los 5 de la corrida mal alojada). Se declara con su motor: el cero no era del objeto.
Los siete se borraron después de atribuir los dos de esta corrida; el árbol `/tmp/rep_previo` se borra
cuando este párrafo esté dentro del manifiesto.

---

## 9. La Pestaña 2 entra al bundle: ocho piezas, copiadas y declaradas

**Qué se incorporó y por qué.** La pestaña 2 (ΣΦ circular corregida) produjo cinco instrumentos y una
medida, más tres actas que las auditan. Un bundle que sólo declara su aparato de custodia y no el
aparato que produjo la cifra que el paper cita deja fuera justamente lo que el paper afirma. Las ocho
piezas entraron por **copia** (`cp -p`) a este bundle, y su sha256 se comprobó **idéntico** al del
original en `sim/`: **8/8**, `cmp` sin divergencia. El bundle no es un puntero al objeto vivo: es una
copia congelada, y la copia se declara (§6.2 ya lo fijó para los medidores heredados).

| Pieza en el bundle | sha16 | tamaño | Original en sim/ |
|---|---|---|---|
| `evidencia/medidas_aN_circular_corregida_20261011.csv` | `c9aaa89b7d56ead7` | 82 l · 3366 B | `sim/data/medidas_aN_circular_corregida_20261011.csv` |
| `evidencia/control_pareado_convergente.json` | `41fce209adc05f98` | 1288 l · 27892 B | `sim/data/invariantes/control_pareado_convergente.json` |
| `instrumentos/medidores/fuego_pestana2_20261011.py` | `f09e781a65d3abe6` | 410 l · 20051 B | `sim/fuego_pestana2_20261011.py` |
| `instrumentos/medidores/control_pareado_convergente.py` | `2829d1e1ce1ee7e4` | 569 l · 29405 B | `sim/control_pareado_convergente.py` |
| `instrumentos/medidores/lector_invariantes.py` | `9fab4e04d281d3cc` | 635 l · 32113 B | `sim/lector_invariantes.py` |
| `actas/ACTA_DEL_PARCHE_SALIDA_FASES_20261011.md` | `89e71eb5a011ae4f` | 91 l · 6111 B | `sim/ACTA_DEL_PARCHE_SALIDA_FASES_20261011.md` |
| `actas/ACTA_DEL_DISPARO_PESTANA2_CIRCULAR_CORREGIDA_20261011.md` | `74f1213640b01724` | 149 l · 11357 B | `sim/ACTA_DEL_DISPARO_PESTANA2_CIRCULAR_CORREGIDA_20261011.md` |
| `actas/VEREDICTO_CONTROL_PAREADO_20261011.md` | `a6316f8db84d8885` | 254 l · 15118 B | `sim/data/invariantes/VEREDICTO_CONTROL_PAREADO_20261011.md` |

**Las anclas nuevas (12).** `verificar.sh` creció de 26 a **38** anclas: las 12 de esta tabla apuntan a
una línea **viva** de cada pieza nueva, y su token se midió con el **mismo motor** que usa el bloque [4]
—`sed -n "${lin}p" | grep -qF`— antes de escribirlas: `ok=12 rojas=0` a `2026-10-11T06:02:16Z`.
Cada ancla se anexó **al final** de `FIN_ANCLAS`, nunca en medio: el banco must-fail lee la **primera**
fila de la tabla (caso E) y reordenarla habría movido el objeto que ese caso mide.

```
evidencia/medidas_aN_circular_corregida_20261011.csv|3|f280fb6744917e9a
evidencia/medidas_aN_circular_corregida_20261011.csv|78|178.7588150970
evidencia/control_pareado_convergente.json|2|2026-10-11T05:48:12Z
instrumentos/medidores/fuego_pestana2_20261011.py|123|RE_N = re.compile
instrumentos/medidores/fuego_pestana2_20261011.py|5|f280fb6744917e9a
instrumentos/medidores/control_pareado_convergente.py|99|rama 2 (~0.74)
instrumentos/medidores/control_pareado_convergente.py|555|intacto: %s
instrumentos/medidores/lector_invariantes.py|42|0.078459
actas/ACTA_DEL_PARCHE_SALIDA_FASES_20261011.md|48|RC_PARCHE=2
actas/ACTA_DEL_DISPARO_PESTANA2_CIRCULAR_CORREGIDA_20261011.md|143|c9aaa89b7d56ead7
actas/VEREDICTO_CONTROL_PAREADO_20261011.md|19|rama 2
actas/VEREDICTO_CONTROL_PAREADO_20261011.md|68|28.2505
```

**Una ancla que se movió por escribir.** El ancla auto-referente `verificar.sh|103|MANIFIESTO declara 0
objetos` caducó en el acto de la enmienda: el encabezado nuevo (identidad del motor, universo 34/33)
empujó esa línea de la **103** a la **129**. Se re-midió y se re-escribió; queda como caso de la regla
que este índice ya trae escrita — *el acto de escribir mueve la cifra que el escrito postula*. Un ancla
auto-referente es el instrumento midiéndose a sí mismo: se corrige **contando la línea**, no leyendo el
párrafo.

**El contrato de cabecera también entró.** Los tres veredictos de `verificar.sh` ya no dicen `RC=0` a
secas: emiten `RC: 0 · MOTOR: <M0|M1|M?> · SHA16: <sha16 del manifiesto> · T_UTC: <sello>`. El cambio es
seguro para el banco **medido, no supuesto**: `arbitra()` sólo busca la **cadena de causa** de cada caso
(`FAILED`, `MANIFIESTO`, `shasum ausente`, `falta`, `ya no dice`, `PARCIAL`, `gitleaks ausente`) y nunca
la forma del veredicto. Los cinco RC=2 tempranos siguen imprimiendo `RC=2` y saliendo sin encabezado de
contrato: allí el metro que calcula el SHA16 es justamente el que falta.

**Límite declarado, no ensanchado en silencio.** Queda **fuera** del bundle
`sim/data/invariantes/crudo_lector_invariantes.json` (sha16 `96f66e9cb30a56ed`, el crudo del lector de
invariantes). Las actas `LECTURA_ETAPA2_20261011.md` e `INFORME_LECTOR_INVARIANTES_20261011.md`, que sí
están dentro, lo **citan**: el testigo de esa lectura vive fuera de la caja que lo cita. Se declara como
frontera abierta en vez de copiarlo por conveniencia; si entra, entra con su fila y su ancla como las
otras ocho.

**Y una novena pieza, escrita después de las ocho.**
`actas/ACTA_DEL_PASO_1_Y_PASO_2_20261011.md` · 112 l · 7887 B · sha16 `97c13bcb87ac4312` · es el cierre
documental del Paso 1 y la medición del Paso 2 en M0: `VEREDICTO: VERDE · RC: 0 · MOTOR: M0 · SHA16:
3866dbd1b785ea15` a `2026-10-11T06:08:38Z`, con el banco externo en **7/7** a `06:08:51Z` (crudos en
`/tmp/verif_paso2_M0_0607Z.txt` · sha16 `5664ee0894677da6` y `/tmp/banco_0609Z.txt` · sha16
`a58afb530d31ddeb`). Su **§5** declara —sin adjudicarlo— que el objeto **se movió mientras se medía**: otra
mano añadió el bloque `[2b] COMPLETITUD (fail-closed)` a `verificar.sh` (`330 → 387 l`, mtime
`06:10:02Z`), y la corrida que vale es la posterior, sobre el objeto ya quieto. Entra **la última**, y por
eso el `SHA16` que ella misma cita es el del manifiesto **anterior** a su propia fila: el valor
autoritativo es el que imprime `./verificar.sh`, que lo declara «no circular». Ninguna medición del cierre
se guarda aquí dentro — el acta **cita** su hora, y `/tmp` no es archivo.
