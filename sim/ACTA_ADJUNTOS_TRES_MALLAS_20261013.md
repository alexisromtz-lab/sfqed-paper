# ACTA — FRENTE §8.4: ORDEN DE ADJUNTOS Y LEY DE COMPOSICIÓN EN TRES MALLAS

## 0. ESTADO Y DESBLOQUEO

La **Adenda §8.4** (`marco-fibrado-20261011/ADENDA_8_4_ORDEN_DE_ADJUNTOS_Y_LEY_DE_COMPOSICION_EN_TRES_MALLAS_20261013.md`)
quedó anclada bajo el protocolo A2.1: gate **RC 10** (creación nominal, target ausente) y **RC 11** (control positivo
post-huella). Commit atómico **exclusivo** (sin `git add .` ni `git add -A`):

```
bf0868b8683d29570f0b798199b91d6fc204f7ef   2026-10-13T04:48:25+00:00
1 file changed, 145 insertions(+)   blob en HEAD identico al disco
sha16 92f825a5846fc923   blob 8014e889e355028ef8f507c779bdaf0c58d8e203   145 l · 14 531 B
post-vuelo: 13 cabezas (NIVEL2=6, NIVEL3=4, COMENTARIOS_SHELL=3) · TABLAS=16 · SIGNO_MONETARIO=0
censo no rastreado: 124 -> 123 | rastreado sucio: 0
```

Con eso **el frente §8.4 queda oficialmente desbloqueado**, y esta acta es la corrida del evaluador numérico.

**Casa de §8.4 — inferida por medición, NO adjudicada.** La fila 6 (`Ley de composición f* g* = (gf)*`, `DECLARADO`)
vive en `marco-fibrado-20261011/ABSTRACT_Y_TABLA_CATEGORICA_20261011.md` (232 l · 23 168 B · sha16 `26326856b7fb7d60`),
por sus líneas 73 (la fila), 210 (§8 ítem 4: «con **tres** niveles de malla el semigrupo RG pasaría de `DECLARADO` a
`MEDIDO`») y 94 (§4 (2), la 2-celda). Se registra como **inferencia medida**; no se adjudica casa.

## 1. UNIVERSO DECLARADO Y PIEZAS

```
UNIVERSO DECLARADO (ejecucion): escalera sellada NODOS = [61, 121, 241, 481]  (LADO = 6.0, 60*2**k + 1)
  VENTANA: 2026-10-13T04:53:30Z (instrumento) · 2026-10-13T05:08:15Z (control)
  MOTOR: python3 -B (solo stdlib) · UNIDAD: nodo · H = [0.100000, 0.050000, 0.025000, 0.012500]
  anidamiento exacto: N[k] == 2*N[k-1] - 1  (481-1 = 480 = 2*240, 241-1 = 240 = 2*120, 121-1 = 120 = 2*60, 61-1 = 60)
  paso entre mallas consecutivas: 2 en cada escalon · paso DIRECTO 61 -> 241: 4 · 61 -> 481: 8
UNIVERSO DECLARADO (bandas): heredadas del Frente 2 (PREREGISTRO_CONVERGENCIA_P_20261012.md seccion 4); no se re-eligen
  VERDE 1.96 <= p < 2.00 y p3 >= p2 | GRIS [1.90, 1.96) (pediria nodos = 961) | ROJO NO-SATURA p < 1.90
  ROJO SOBREPASO p3 >= 2.00 | ROJO NO-MONOTONO p3 < p2 | MIXTO se declara, no se adjudica
```

| pieza | rol | l | B | sha1 |
|---|---|---|---|---|
| `sim/evaluador_adjuntos_tres_mallas.py` | instrumento (hermano v1) | 449 | 20 857 | `bddca445502ad319203c1f0b4c13084e5ffaea8b` |
| `sim/data/invariantes/adjuntos_tres_mallas_20261013.json` | crudo de v1, RC 0 | 167 | 4 997 | `8655c5cd8302e18b684b72f522424cf81464e937` |
| `sim/control_referencia_directa_20261013.py` | control del metro (escrito en esta corrida) | 241 | 9 419 | `b697a8e3287390cc788c891730fc332a953fea24` |
| `/tmp/control_referencia_directa_20261013.txt` | crudo del control, RC 0 | 44 | 2 950 | `15a55038650f1efd6697ba6e661c234cd15ed46e` |

Huellas de pre-registro en el cuerpo: instrumento `HUELLA-EVALUADOR-ADJUNTOS-TRES-MALLAS-20261013` (post-vuelo **RC 11**) ·
control `HUELLA-CONTROL-REFERENCIA-DIRECTA-20261013` (post-vuelo **RC 11**).

El control **no escribe ningún archivo** (sale por stdout), **no corre el driver** y **no eleva nada**: su único objeto es
decidir si un rojo de O(1) pertenece al objeto o al metro.

## 2. CONDICIÓN 1a — ORDEN DE COMPOSICIÓN (adoptado vs formalizado)

**Orden adoptado en el arnés:** `X Y := X o Y` **diagramático**; en código, `aplicar(comp(X, Y), v) == X @ (Y @ v)`.
Coincide con la convención formalizada en la adenda (composición de la izquierda con lo de la derecha).

Medido en el crudo (sección `c_ord`):

```
residuo_diagramatico_vs_matricial = 0.0        (los dos caminos dan el mismo vector)
residuo_adjunto_gf_vs_fg          = 0.0        (identidad de algebra: f* g* = (gf)*)
orden_adjunto_forzado_por_dimensiones = true
orden_inverso_definido                = false
```

**El orden no fue elegido: está forzado por dimensiones.** Con `R_k` de forma (61,121) actuando sobre vectores finos,
la cadena `R1(R2(R3 v))` consume un vector de 481 y devuelve 61; el orden `R3(R2(R1 v))` **no está definido**
(121 contra 481: no hay producto). El arnés **no eligió** la convención: la única cadena que compone es la que la
adenda formaliza. Declarado como hecho; la identidad de álgebra `(gf)* = f* g*` se **declara**, no se adjudica.

## 3. CONDICIÓN 1b — LA LEY EN LAS TRES MALLAS, CON EL METRO CORREGIDO

La primera corrida de v1 dio, en su sección 3, un rojo de orden **O(1)** donde se esperaba redondeo:

```
ley_composicion (v1):  residuo_R = 0.0 · residuo_P = 1.9881707187556599 · residuo_A = 15.216904260722458
vectores_de_prueba = 5 · metrica = "identidad de operadores"
```

**Diagnóstico: el rojo era del METRO, no del objeto.** Causa leída verbatim en la fuente de v1:
`P_mat(nc, nf)` escribe `M[2*j][j] = 1.0` y `M[2*j+1][j] = M[2*j+1][j+1] = 0.5`, y `A_mat(nc, nf)` llama
`R_mat(nc, nf, 2)`: **las dos funciones llevan el paso 2 escrito a mano** y usan `nf` sólo como número de filas ⇒
son exactas **si y sólo si** `nf == 2*nc - 1` (todo llamado anidado) y quedan mal en las **referencias directas**
`P_mat(61,481)` / `A_mat(61,481)` de esa sección. La tercera pata **no** comparte el defecto: `Rdir(nc, nf)` sí pasa
`(nf-1)//(nc-1)` ⇒ su `0.0` es correcto (y además es un corte de índices, sin aritmética: 0 exacto por construcción).

**Control escrito para medir el defecto (`sim/control_referencia_directa_20261013.py`).** Reproduce las funciones
defectuosas **literales** (`P_v1`, `A_v1`) contra una construcción de **paso general** (`P_gen`, `A_gen`), y da:

```
1. censo de filas            P_v1(61,481): filas=481  no_nulas=121  en_cero=360  ultima_no_nula=120
                             A_v1(61,481): filas=481  no_nulas=61   en_cero=420  ultima_no_nula=120
   => la referencia directa de v1 solo alcanza las filas 0..121 de 480
2. control negativo          P_v1 vs P_gen @ (61,121): max|dif| = 0.000e+00
                             A_v1 vs A_gen @ (61,121): max|dif| = 0.000e+00
   => 0 exacto: las patas ANIDADAS de la cadena de v1 estaban bien
3. control POSITIVO          P: cadena P1(P2(P3 v)) vs P_v1(61,481) v  =  1.988e+00   (reproduce 1.988e+00)
                             A: cadena A1(A2(A3 v)) vs A_v1(61,481) v  =  1.522e+01   (reproduce 1.522e+01)
4. metro de paso general     R: 0.000e+00 (corte de indices) · P: 2.220e-16 · A: 0.000e+00
5. identidad del adjunto     anidados (paso 2): A_gen 0.000e+00 · A_v1 0.000e+00
                             DIRECTO (paso 8, 61 -> 481): A_gen 0.000e+00 · A_v1 1.657e-01
```

**Cierre de la condición 1b.** Con la referencia de paso general, la ley `f* g* = (gf)*` se compone **al nivel del
operador** con residuo de redondeo (2.22e-16 en la interpolación, 0 en el adjunto), no con discrepancia. Los dos
testigos coinciden: (i) el censo de filas, (ii) la identidad del adjunto al paso directo (1.657e-01). Y el **par
(con / sin)** es lo que lo decide: mismo objeto, misma malla, dos construcciones de la referencia ⇒ **el defecto es de
la función, no de la malla**.

**Declarado y NO elevado:** los ceros corregidos son **identidades de la operación** (los dos caminos son el mismo
interpolante) ⇒ se declaran, **no son evidencia**. `n = 1`.

## 4. CONDICIÓN 2 — NORMA DEL ERROR DE ADJUNCIÓN, PUNTO A PUNTO, EN LAS TRES MALLAS

Medido en el crudo de v1 (secciones `adjuncion`, `celda_2`). Se separan los **dos planos**, que no son el mismo metro:

**Plano del EMPAREJAMIENTO (escisura).** Defecto de la escisura frente al emparejamiento trapezoidal `G_n = diag(h_n w_n)`:

```
D_escisura = [0.0009545472729790422, 0.0002359015173194895, 5.8807759135567905e-05]
p_esc      = [2.016631949369875, 2.0041062751338026]        (escalones 121->241 y 241->481)
D_identidad = [0.0, 0.0, 0.0]   => control que NO PUEDE diferir: se declara identidad, NO es medicion
```

**Plano del OPERADOR.** El adjunto exacto **no es** la interpolación lineal; la discrepancia es estructural:

```
operador_O1 = {escalon 1: 1.0, escalon 2: 1.0, escalon 3: 1.0}   => |P - A| infinito = 1.000000, O(1), SIN tasa
```

Esto es **exactamente** la predicción pre-registrada (`prediccion_operador`: «al nivel del OPERADOR el adjunto exacto
NO es la interpolación lineal: la discrepancia es estructural, O(1), sin tasa»). Se reporta como **coincidencia con la
predicción**, no como hallazgo.

**2-celda `u - P R u`** (error de interpolación lineal en los nodos IMPARES), punto a punto:

| k | h | nodos_fino | delta_inf | delta_en_nodos_pares | nodo del maximo | x del maximo |
|---|---|---|---|---|---|---|
| 1 | 0.05 | 121 | 4.894348e-02 | 0.0 | 95 | 4.7500 |
| 2 | 0.025 | 241 | 1.216008e-02 | 0.0 | 231 | 5.7750 |
| 3 | 0.0125 | 481 | 3.073163e-03 | 0.0 | 419 | 5.2375 |

El **nodo del máximo se mueve con la malla** (95, 231, 419) y `delta_en_nodos_pares = 0.0` **exacto** en las tres
(control que no puede diferir). `rho = delta_inf` en las tres filas.

## 5. CONDICIÓN 3 — LA TASA PRESERVA p = 2

```
2-celda:   p_121_241 = 2.0089637828352562    p_241_481 = 1.984356611722882       banda: ROJO NO-MONOTONO
escisura:  p_121_241 = 2.016631949369875     p_241_481 = 2.0041062751338026      banda: ROJO SOBREPASO
```

Las dos bandas rojas se resuelven **contra el DOMINIO del umbral sellado, no contra el umbral**:

1. **2-celda = ROJO NO-MONOTONO.** El defecto de la 2-celda es cuadrático **por construcción** (`|delta| = (h al
   cuadrado / 8) * |u''|`: la razón 4 por escalón es exacta, no asintótica) ⇒ `p3 < p2` **es lo que la construcción
   predice** (la tasa medida baja hacia 2 desde arriba). Se declara **defecto de dominio**: **el umbral NO se baja.**
2. **escisura = ROJO SOBREPASO.** `p3 = 2.004 > 2.00` en un objeto cuadrático por construcción: que toque la banda
   superior es un **hecho de dominio**, no una violación. El propio pre-registro lo dice (`prohibiciones`: «un defecto
   EXACTAMENTE cuadrático no es un objeto asintótico: si toca la banda superior, se declara el defecto de DOMINIO del
   umbral, no se baja el umbral»). **El umbral NO se baja.**

**Sólo existen DOS tasas** (tres mallas dan dos escalones). Una tercera tasa exigiría la 4a malla **`nodos = 961`**
(es lo que la banda GRIS `[1.90, 1.96)` pide cuando se cae en ella; aquí no se cayó). Y **no se publica `p = 2` como
resultado**: el instrumento publica `p` **junto a los defectos de sus propios escalones** (el testigo de escala) y
**sin** una constante ajustada `C`; esa ausencia del par (p, C) se **declara**, no se repara en esta corrida.

## 6. FALSADOR (pre-registrado: el anidamiento es la causa)

```
falsador (fino desfasado media malla fina):
  e_inf = [0.15643446504023883, 0.07845909572784894, 0.039259815759074154]
  p_121_241 = 1.0679428031629985     p_241_481 = 0.9988873054289255      banda: ROJO NO-SATURA
  residuo_ley_bajo_desfase = 0.0
```

Sale **rojo con p ~ 1** (≈ 0.9989, O(h)) **como estaba pre-registrado** (`prediccion_falsador`), y la ley de
composición **sobrevive al desfase** (residuo 0.0): la ley es un corte de índices, y lo que el anidamiento decide es la
**consistencia**. El falsador no refuta la ley; la refuta como fuente de la tasa.

## 7. DEFECTOS DECLARADOS (declarados, NO reparados)

1. **Metro de v1, sección 3 (defecto vivo).** Paso 2 escrito a mano en `P_mat` y `A_mat`; correcto sólo si
   `nf == 2*nc - 1`. Contamina **únicamente** las referencias directas `P_mat(61,481)` / `A_mat(61,481)`; las patas
   anidadas y **las secciones 2, 4, 5, 6 y 7 quedan intactas** (lo certifica el control negativo: paso 2 ⇒ 0 exacto).
   El crudo de v1 **se deja tal cual** y esta acta lo declara: la medición corregida es la del control.
2. **Bloqueo A2.1 sobre targets no rastreados.** El gate, sobre un target que existe y **no** está rastreado, imprime
   `?? …` en `git status --porcelain` ⇒ **RC 13**, sin camino a RC 0 ⇒ **mutar el hermano v1 está prohibido bajo A2.1**.
   La excepción se declara aquí en lugar de repararse en el lugar. (`UNTRACKED = 126` = 123 previos + instrumento +
   control + crudo json; `TRACKED_DIRTY = 0`.)
3. **Errata de rótulo del control (mía).** Su línea 4 imprime `PASO entre mallas: [2, 2, 2]` (la lista **correcta**:
   el factor anidado es 2 en cada escalón) y a continuación el paréntesis «paso entero = 2, 4, 8», que pertenece a la
   escalera **directa** (61→241 = 4, 61→481 = 8). Las cifras impresas no se mueven; el paréntesis es un **rótulo que
   afirma lo que la línea desmiente** ⇒ informa, no protege. No se repara (misma restricción de A2.1).
4. **El orden nombra el target por nombre desnudo** (`ADENDA_8_4_…md`) ⇒ el gate exige target **absoluto**; relativo da
   un RC 128 no declarado. Se **declara la corrección**: la corrida usó la ruta absoluta.
5. **Rótulo `ANIDAMIENTO EXACTO` del crudo sellado.** Imprime `480/120 = 8` mientras sus propias cifras se descomponen
   `480/60 = 8 · 240/60 = 4 · 120/60 = 2`: el rótulo lleva la razón **directa**, no la del escalón. Errata declarada,
   no reparada (el archivo viejo sólo recibe apéndices).
6. **Colisión de namespace `can[oó]nic`** (624 l · 660 ocurrencias · 280 archivos) y **doble casa de `lambda/40`**:
   declaradas, sin adjudicar. **Ruta no resolvente** en el pre-registro padre (`sim/marco-fibrado-…`): declarada.
7. **Filas 9 y 11 de la tabla de §3** de la adenda: se declaran sin adjudicar en esta corrida.

## 8. LO QUE NO SE HACE

- No se escribe `p = 2` como **resultado** (se publica `p` con el testigo de escala de sus escalones).
- Una **identidad no es evidencia**: `D_identidad = 0.0`, los ceros corregidos del control y `delta_en_nodos_pares = 0.0`
  se **declaran**, no se adjudican.
- **Ningún umbral sellado se baja**: los dos rojos por encima de 2.00 se registran como **defecto de dominio**.
- **Nada sobre `p` entra en `main.tex`.**
- `n = 1`: **no se eleva nada.**
- No se usa `git add .` ni `git add -A`; la pieza vieja **sólo recibe apéndices**.
- El control **no escribe archivo alguno**, no corre el driver y no toca instrumentos del repo.
