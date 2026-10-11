# ÍNDICE 0 — SFQED: el corpus que se mide a sí mismo

**Qué es esta pieza.** El árbol canónico de reproducibilidad de la línea SFQED: los pre-registros que
fijan las bandas *antes* de la primera cifra, las actas de auditoría que registran lo que se midió, los
medidores que produjeron esas cifras y los instrumentos de custodia que impiden que el repo publique un
secreto. No es un resumen de los resultados: es el **aparato de medida**, con la dirección de cada
afirmación.

**Cómo se verifica.** Un solo comando, `./verificar.sh`, que hace tres cosas y sale con un código de
salida que no admite interpretación: `0` verde · `1` fractura del objeto · `2` contrato o medidor roto.
No hay puerta de escape que devuelva verde.

```
UNIVERSO DECLARADO: 25 archivos bajo bundle/  =  24 declarados en HASHES.sha256 (todos menos el propio
                    manifiesto)  +  HASHES.sha256 (que no puede declararse a sí mismo)
MOTOR:              shasum -a 256 · cmp · grep -nF · python3 -B (stdlib) · git -C
UNIDAD:             archivo (inventario) · línea (anclas) · byte (identidad de custodia)
VENTANA:            el reloj UTC que verificar.sh imprime en su encabezado; toda cifra de este índice
                    caduca al escribirse, y su hora es parte de la cifra
T_UTC de redacción: 2026-10-11T04:42:37Z   ·   sha16 de este archivo: el que imprime ./verificar.sh
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
   este índice no los re-fecha. La única hora de este archivo es la de redacción de arriba.
5. **Lo que este índice no afirma.** No afirma que β = 0.5 sea el resultado físicamente correcto: afirma
   que **3 objetos distintos producen el mismo veredicto**, que es una propiedad del **metro**, no del
   objeto. Distinguir esas dos cosas es el contenido entero de esta pieza.
