# ACTA — Convergencia de `p`: TERCERA MALLA (nodos = 481)

Frente 2 (Maxwell Fase 2 en QED). Cierra los dos pendientes metodológicos declarados como NO MEDIDOS.
Esta acta TRAZA la corrida; no adjudica física nueva.

---

## §0 UNIVERSO DECLARADO

```
UNIVERSO DECLARADO: 3 geometrias abanico (30.0·m=17 · 26.5651·m=17 · 30.0·m=9)
  DENOMINADOR : L0_exacto a 361 nodos de la MISMA geometria (referencia intrinseca, con_yee=False)
  MOTOR       : python3 -B + control_pareado_convergente.py importado SOLO LECTURA (Ruta B)
  UNIDAD      : nodos; h = dx/lambda = LADO/(nodos-1), adimensional
  VENTANA     : 2026-10-12T07:28:49Z (T_UTC del crudo)
  UMBRAL      : bandas de la seccion 4 del pre-registro (pre-declaradas, no elegidas post-hoc)
  LECTURA     : L4_completo contra L0_exacto; residuo eps = R - 1
```

**identidad al abrir (medida, no citada):** instrumento `2829d1e1ce1ee7e4` · `medidas_aN.csv`
`4129d436e2cd081d` · pre-registro `7476477b58cda501` · `medidas_aN_intacto = True` tras la corrida.

**escalera declarada:** `nodos = 60·2^k + 1` para k = 0..3 → `61 · 121 · 241 · 481`.
`h = 0.100000 · 0.050000 · 0.025000 · 0.012500`; los tres escalones dan `log(h1/h2) = 0.693147180560`.
La tercera malla (481, dx = lambda/80) es la que el pre-registro §3 declaró; no se eligió después de ver la salida.

---

## §1 REFERENCIA POR GEOMETRÍA (361 nodos, dx = lambda/60)

| geometría | R_0 | F_rel | G_rel |
|---|---|---|---|
| abanico 30.0 m=17 | 0.3141325303203359 | 9.867925e-02 | -6.04e-18 |
| abanico 26.5651 m=17 | 0.2793975056768241 | 7.806297e-02 | -4.78e-18 |
| abanico 30.0 m=9 | 0.3304056447464959 | 1.091679e-01 | -6.68e-18 |

`G_rel ~ 1e-18` en las tres: la referencia no lleva parte imaginaria apreciable.

---

## §2 EL OBJETO — eps y p por escalón

eps en porcentaje = 100·(R_L4 / R_0 − 1). `nan_extra = 0` en las doce celdas.

| geometría | 61 (λ/10) | 121 (λ/20) | 241 (λ/40) | 481 (λ/80) |
|---|---|---|---|---|
| 30.0 m=17 | +33.965762 | +9.690720 | +2.522583 | **+0.637467** |
| 26.5651 m=17 | +43.088974 | +12.603448 | +3.313774 | **+0.839850** |
| 30.0 m=9 | +30.498572 | +8.614886 | +2.234090 | **+0.563958** |

| geometría | p1 (61→121) | p2 (121→241) | p3 (241→481) | p2−p1 | p3−p2 | banda p3 |
|---|---|---|---|---|---|---|
| 30.0 m=17 | 1.809406 | 1.941702 | **1.984480** | +0.1323 | +0.0428 | VERDE |
| 26.5651 m=17 | 1.773500 | 1.927271 | **1.980271** | +0.1538 | +0.0530 | VERDE |
| 30.0 m=9 | 1.823838 | 1.947144 | **1.986028** | +0.1233 | +0.0389 | VERDE |

`h3 = 0.012500` en las tres. `eps3` = `6.374666e-03` · `8.398503e-03` · `5.639581e-03`.

**par (p, C) publicado** — se publica el PAR, no un `p = 2`:

| geometría | (p, C) con p = p3 | (p, C) con p = 2 fijo |
|---|---|---|
| 30.0 m=17 | (1.984480, 38.115515) | (1.984480, 40.797861) |
| 26.5651 m=17 | (1.980271, 49.298764) | (1.980271, 53.750422) |
| 30.0 m=9 | (1.986028, 33.949703) | (1.986028, 36.093318) |

`C = eps3 / h3**p` (prefactor del último escalón). La segunda columna muestra cuánto sube `C` si se
fuerza el exponente asintótico: el corrimiento es de +7.0 %, +9.0 %, +6.3 %.

---

## §3 VEREDICTO POR BANDAS PRE-DECLARADAS

```
BANDAS DECLARADAS (seccion 4 del pre-registro):
  VERDE          [1.96, 2.00)  Y  p3 >= p2
  GRIS           [1.90, 1.96)      (exigiria 961 nodos, dx = lambda/160)
  ROJO NO-SATURA p3 < 1.90
  ROJO SOBREPASO p3 >= 2.00
  ROJO NO-MONOTONO p3 < p2 (en cualquier geometria)
```

**VEREDICTO: VERDE** — `p` desacelera hacia 2 **desde abajo, sin alcanzarlo**, en las tres geometrías.
`p3 >= p2` se cumple en las tres (Δp3 = +0.0428 · +0.0530 · +0.0389); ninguna cae en GRIS, SOBREPASO ni
NO-SATURA; ninguna es NO-MONÓTONA. No hay MIXTO: las tres bandas coinciden.

**Deriva residual, declarada:** entre E2 y E3 el exponente se movió +0.0428/+0.0530/+0.0389 — sigue
subiendo, pero la subida se APLANA (E1→E2 fue +0.1323/+0.1538/+0.1233). Consistente con acercarse a 2
desde abajo; **no** demuestra que 2 sea el límite de la malla siguiente.

---

## §4 CONTROLES (todos ANTES de extraer E3)

- **C1 positivo sintético** (eps = C·h^p sobre h = 0.1/0.05/0.025/0.0125): p = 1.00 err 0.00e+00 · 1.50 err 4.44e-16 · 1.93 err 2.22e-16 · 2.00 err 0.00e+00 — OK las cuatro. El estimador recupera un exponente plantado.
- **C2 negativo sintético** (eps = C·h·log(1/h)): p estimado 0.6203 / 0.6997 / 0.7516; `no-es-2 = True`, `difiere-e1-e2 = True` — OK. El estimador discrimina.
- **C3 guarda de cero entradas**: 4 sondas, cada una imprime su CAUSA — OK.
- **C0 certificado del arnés** (receta heredada reproducida en 61/121/241, tolerancia 5.0e-05): las seis cifras de `p` y los nueve porcentajes salen **IDENTICO** dígito a dígito. Detalle: `1.809406 1.941702` / `33.965762 9.690720 2.522583` · `1.773500 1.927271` / `43.088974 12.603448 3.313774` · `1.823838 1.947144` / `30.498572 8.614886 2.234090`. **El arnés quedó certificado ANTES de medir E3**: si C0 hubiera dado DIVERGE, la corrida moría en rc 2 y E3 no se medía.
- **C4 control de la referencia**: eps decrece en los 3 escalones para las 3 geometrías — OK.

---

## §5 QUÉ NO HACE ESTA ACTA

- **No eleva nada.** `n = 1`. El exponente `p` es **instrumento**, no medida del artículo.
- **No escribe `p = 2` como resultado.** Se publica el par `(p, C)`.
- **No repara prosa sellada.** El defecto rotulado del abstract (la prosa escribió "≤ 2.5 %" y el máximo medido sube a 3.31 % con la 4ª/5ª geometría; y el rótulo "banda de malla" quedó falsado) se **conserva declarado**, no se edita.
- **No toca** `control_pareado_convergente.py`, `runner_2d3v.py`, `maxwell2d.py`, `field_solver.py`, `lector_invariantes.py`, `params.py`, ni `bundle/`. El instrumento se importó **solo lectura**.
- **No mide el falsador de mallas no anidadas** — ése es el entregable 2, ya separado (`sim/falsador_mallas_no_anidadas.py`, batería RC=0 / VERDE / `dbeta=+0.000000`).

---

## §6 CRONOLOGÍA (mtime medido, no citado)

```
06:26:39Z  PREREGISTRO_CONVERGENCIA_P_20261012.md   (sellado, 326 l · 17111 B · 7476477b58cda501)
06:28:59Z  sim/falsador_mallas_no_anidadas.py        (entregable 2, 467 l · 22732 B · 9a992758e31f8d5b)
07:15:28Z  gate A2.1 (post-verificacion de la reparacion 1)
07:20:27Z  corrida 1 -- barrido OK, C1/C2/C3 OK, aborta en C0 (defecto de impresion)
07:23:47Z  reparacion 1 (h_de + C0)
07:26:14Z  corrida 2 -- barrido + C0 IDENTICO + C4 OK, aborta en objeto() l.383 (desempaque)
07:28:09Z  reparacion 2 (objeto: guarda de contrato + iteracion plana)
07:28:28Z  reparacion 2-bis (guarda rc == 2: no se escribe crudo sin objeto)
07:28:49Z  corrida 3 -- T_UTC del crudo
07:28:58Z  crudo escrito
07:29:35Z  huelgas medidas
```

Enlace verificado: `mtime(pre-registro) < mtime(driver) < mtime(crudo)`.

---

## §7 HUELLAS

| pieza | líneas | bytes | sha16 | sha1 (blob) | mtime |
|---|---|---|---|---|---|
| `PREREGISTRO_CONVERGENCIA_P_20261012.md` (D1) | 326 | 17111 | `7476477b58cda501` | `ad1f24db1de7efcc220a11faa3022e0b84054ee4` | 06:26:39Z |
| `sim/falsador_mallas_no_anidadas.py` (D2) | 467 | 22732 | `9a992758e31f8d5b` | — | 06:28:59Z |
| `sim/driver_convergencia_p.py` (D3, final) | 580 | 26535 | `d7cde9ed0c6d6c81` | `668086645e033371c9d423fbb1f6cded855ac8cf` | 07:28:28Z |
| `sim/data/invariantes/convergencia_p_tercera_malla_20261012.json` | 492 | 9985 | `b381e3d77c6feff7` | `d0ca45cd685c39d940807e5b332b96617808db3f` | 07:28:58Z |

El crudo lleva `universo_declarado` + `T_UTC`, los seis controles, `objeto`, `veredicto`, `rc = 0`,
`medidas_aN_intacto = True`, y el bloque `sha16` con `driver` = la huella del propio escritor.

**Crudos de pantalla (efímeros, en /tmp — no copiados al repo):**
`/tmp/convergencia_p_2026-10-12T0720Z.txt` (barrido de la corrida 1) ·
`/tmp/convergencia_p_2026-10-12T0726Z.txt` (certificado C0 = IDENTICO + traza del aborto en l.383) ·
`/tmp/convergencia_p_2026-10-12T0729Z.txt` (corrida completa, RC=0) ·
`/tmp/falsador_no_anidadas_06Z.txt` (batería de D2).

---

## §8 DECLARACIONES HONESTAS (defectos medidos, NO reparados)

1. **Defecto de ruta en el pre-registro sellado.** §0.3 cita la fuente como
   `sim/marco-fibrado-20261011/ABSTRACT_Y_TABLA_CATEGORICA_20261011.md`; esa ruta **no resuelve**. La real
   es la raíz del repo: `marco-fibrado-20261011/ABSTRACT_Y_TABLA_CATEGORICA_20261011.md`
   (`26326856b7fb7d60`). Se declara; **no se edita** el pre-registro sellado.
2. **El gate A2.1 sobre la reparación 1 corrió como POST-verificación**, no antes de escribir. La doctrina
   dice "sin corrida previa con RC 0 está prohibido mutar el archivo". La sonda nominal devolvió **RC 11**
   (huella presente ⇒ la reparación SÍ había aterrizado), que es verificación del acto, no pre-vuelo.
3. **El RC 12 de la sonda de control fue defecto del METRO, no del objeto.** Se pasó `BLOB_PRE` como
   `sha256[:16]` (`aba7243b0473e61a`) cuando el gate compara el **sha1 completo de 40 hex** de
   `git hash-object`. El gate imprimió el esperado y el medido; con el sha1 correcto
   (`2672ce108259a0adc53b6d1ef9dd5553015e8629`) la identidad cerraba. Una sonda mal parametrizada no
   discrimina: su RC es veredicto sobre el metro.
4. **El gate no puede autorizar escritura sobre un archivo YA existente en `sim/`.** Con la huella nueva
   (ausente) devolvió **RC 13** — `sim/` está mayormente **untracked** (`??`), así que `git status` lo ve
   sucio y el gate cierra fail-closed. La reparación 2 se hizo **declarando el RC 13** y midiendo el blob
   antes/después (`2672ce108259a0adc53b6d1ef9dd5553015e8629` → `668086645e033371c9d423fbb1f6cded855ac8cf`)
   como traza sustituta. El destino NUEVO (crudo y esta acta) sí pasó por el gate con **RC 10**.
5. **Las dos corridas abortadas murieron en código de IMPRESIÓN/ITERACIÓN, nunca en una medición.**
   Corrida 1: `control_C0`, concatenación `tupla + str`. Corrida 2: `objeto()`, `zip(filas, HEREDADO)` con
   desempaque de 3 sobre tuplas de 4 (`HEREDADO` no se usa dentro del bucle: el acople era vestigial).
   Ambos barridos salieron completos y correctos antes del aborto. El punto de impresión es sitio de
   defecto y se audita ANTES de gastar el barrido.
6. **Defecto del `h_de` (reparado en la ronda 1), declarado por su alcance real:** el instrumento heredado
   imprime su columna `dx/l` como `LADO/(nodos-1)`, sin la constante física. La versión inicial multiplicaba
   por `LAMBDA` ⇒ la columna impresa salía `0.000000`. El error **se cancela** en `log(h1/h2)` (el cociente
   sigue siendo exactamente 2), así que `p` **nunca estuvo corrompido**; sí corrompía el prefactor publicado
   `C = eps/h**p` (desviado por `LAMBDA**p`) y la columna impresa. La corrida 3 imprime
   `0.100000 / 0.050000 / 0.025000 / 0.012500`. **La columna impresa también es medición.**

---

## §9 REPRODUCIR

```
export TZ=UTC
python3 -B /Users/marlene/sfqed-paper/sim/driver_convergencia_p.py --nodos 61,121,241,481 --geometrias 3
```

Añadir `--sin-escribir` para no tocar el crudo, `--json` para volcar el crudo a pantalla.
El driver aborta con rc 2 (y **no escribe crudo**) si C1/C2/C3 fallan, si la guarda de escalones falla, si
C0 no certifica IDENTICO, si C4 falla, si el objeto no se pudo extraer, o si un archivo sellado se mueve
durante la corrida. El pre-registro §4 sigue siendo el contrato: esta acta sólo lo ejecuta.
