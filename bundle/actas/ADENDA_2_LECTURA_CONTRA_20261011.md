# ADENDA 2 — el antinodo, el pico y el supremo (auditoría de la tercera lectura del contra)

T_UTC: 2026-10-11T02:25:09Z

UNIVERSO DECLARADO: `sim/etapa1_contra.json` (9292 B, sha16 `221a9fe8c3e269f4`, T_UTC 2026-10-11T01:50:20Z) + `sim/etapa1_colineal.json` (11530 B, T_UTC 2026-10-11T01:15:44Z) + `/tmp/sonda_contra_nulo_dcha20_out.txt` (testigo de la corrida N=4 con lambda/2, hora 2026-10-11T02:15:55Z) + `sim/maxwell2d.py` (sha16 `1db75ea7b0b8cba4`) + `sim/falsador.py` (sha16 `f04551c7f19ce73a`). MOTOR = `python3 -B` / `cat -n` / `grep -n` / `sed -n`. UNIDAD = campo declarado, celda, línea. VENTANA = el reloj UTC de arriba.

PIEZA BASE: `sim/ADENDA_LECTURA_CONTRA_20261011.md` (112 l, sha16 `23a10dd7bf3e12c2`, commit `8e46865`). NO se parchea: recibe apéndice, como manda la casa.

NATURALEZA: auditoría de una lectura en prosa contra el crudo. En este tramo no se corrió ninguna simulación nueva y no se editó ni un instrumento ni una pieza sellada.

## §1 Lo que la lectura acierta (con su comando detrás)

Medido en `sim/etapa1_contra.json`, fila N=4:

- El desplazamiento es **+10 celdas exactas**: `pico_i` pasa de **232** a **242** (testigo de la corrida desplazada, l.1: `pico_i=242`), y 10 celdas = **λ/4** = 0.25 λ con `dx = λ_L/40`. La lectura dice «+10 celdas exactas»: ✓ crudo.
- El foco **sube**: `a_foco` 53.257051507 → 106.206118 ⇒ razón **1.994217** (`106.206118/53.257051507`). La lectura dice «×1.994»: ✓ crudo.
- La relación magnética en el foco **colapsa**: **1.982 → 0.445** (sonda del eje, unshifted y shifted). La lectura dice «de 1.982 a 0.445»: ✓ crudo.
- La identidad del §2 de la lectura, `F/(½|E|²) = 1 − (cB/|E|)²`, es **exacta**: `1 − 0.394424² = 0.844430` frente al `F_rel_pico = +0.844430` impreso; `1 − 0.387838² = 0.849611` frente al `+0.8496` de la corrida desplazada. ✓ crudo y analítico.
- `beta = 0.500000` dentro de la banda pre-registrada `[0.45, 0.55]` (`falsador.py` l.31): ✓ crudo.
- El **RC = 1** es del ancla, no del objeto: el único fallo es `sin N=1 no se puede medir el cociente contra sqrt(N)` (`sim/falsador.py` l.120–125), y en el contra la N=1 **no puede existir** (el modo contra exige N par y enfrenta pares). Control `--sintetico 0.5` → `VEREDICTO: VERDE` · `RC = 0`. ⇒ El ROJO es del metro. ✓

## §2 El «~106» de la lectura no tiene testigo: son dos objetos, de otra N y de otra corrida

La lectura escribe «el campo eléctrico medido allí era apenas la mitad del pico (**53.25 frente a ∼106**)». La mitad **sí** es correcta y está declarada por el instrumento: `b_foco_rel = 0.476705` en las **cuatro** filas contra (`python3 -B` sobre el JSON). Pero el **rótulo `~106`** no señala al pico de esa corrida:

```
python3 -B -c "t=open('sim/etapa1_contra.json').read(); [print(v, t.count(v)) for v in ('111.719118','106.514103','53.257052','106.206118','107')]"
```

- `111.719118` → **0** ocurrencias; `53.257052` → **0**; `107` → **0**.
- `106.514103` → **1** ocurrencia: es el `a_foco` de la fila **N=16** de la misma corrida, es decir **otro N**.
- `106.206118` → **0**: es el `a_foco` de la corrida **desplazada** (otro objeto, otra hora).

El **pico de la ventana** de la corrida que la lectura cita es **111.719117598** (celda 232), no 106. Los tres números — 106.514103 (foco, N=16), 106.206118 (foco desplazado, N=4), 111.719118 (pico de la ventana, N=4) — tienen **el mismo tamaño y ningún nombre compartido**: mismo caso que el `106.206` / `106.514` / `111.719` ya declarado en la adenda base §6. El cociente de la lectura es correcto; **la cifra que lo acompaña es de otro objeto**.

## §3 El foco no es el antinodo: faltan 2 celdas (0.05 λ) del ideal, y en las dos configuraciones

Medido, `pico_lambda_del_foco`:

- **Sin desplazar**: el máximo de la ventana está en la celda **232** = **−0.200 λ** del foco. El ideal de un patrón estacionario simétrico con un nudo en el foco pondría la cresta a **−0.250 λ** (λ/4 = 10 celdas). Medido: **8 celdas**. Sobran **2 celdas**.
- **Desplazado λ/2**: el máximo está en la celda **242** = **+0.050 λ**. El ideal lo pondría **sobre** el foco. Medido: **2 celdas** después.

⇒ El desfase respecto del ideal es **+2 celdas (0.05 λ) en las dos configuraciones**, reproducible. Y la razón que la lectura usa para decir «directamente sobre el origen» no es 1: `foco/pico = 106.206118/109.933787 = ` **0.966092** (el instrumento imprime `a_foco/a_medido = 0.9661`). **La cresta no aterriza en el foco: pasa 2 celdas al lado.**

La regularidad de las 2 celdas se **declara medida**; su causa (fase de Gouy del haz enfocado, o la convención del frente de onda curvo `omega rho²/2R` de la inyección) se declara **conjetura, no adjudicada** — misma frontera que la conjetura ya declarada de `(1/√2)·0.987675` en la adenda base.

## §4 El foco tampoco es un nudo eléctrico: es 0.4767 del máximo, con cB/|E| = 1.982 finito

La lectura dice «antinodo magnético / **nodo** eléctrico en el origen (0,0)». Medido en el foco, sonda del eje, corrida sin desplazar: `|E| = 2.13741e14 V/m` y `cB/|E| = ` **1.982**.

- Un **nudo** eléctrico ideal da `|E| → 0` y `cB/|E| → infinito`. Medido: `|E|` es **0.4767 del máximo** y `cB/|E|` es **1.982**, finito. El foco es un **mínimo relativo con exceso magnético ×1.982**, no un nudo.
- El denominador importa: 0.4767 es contra el **pico de la ventana** de esa corrida (111.719117598), no contra el «~106» de §2.

## §5 «Puramente eléctrico» es 0.445, no 0 — y el invariante da la cifra que falta

Con el nulo λ/2, la lectura dice que el antinodo es «**puramente** eléctrico». Medido en el foco, sonda de la corrida desplazada (l.20 del testigo): `|E| = 4.26245e+14`, `a0 equiv = 106.2061`, `cB/|E| = ` **0.445**; y `F/(eps0 E²/2) = +0.8496`. Un campo puramente eléctrico daría `cB/|E| = 0` y `F = 1`. ⇒ El foco desplazado es un antinodo eléctrico **parcial**: el campo magnético no desaparece, baja al **44.5 %** del eléctrico (desde el 198.2 %).

Cifra que la lectura no usó y que sí respalda su intuición — **el supremo del invariante**: `a_inv_rel_al_pico` es **0.992090** (contra, cuatro filas) y **0.9998** (desplazado). Si en su propio supremo el invariante vale `raiz(E² − (cB)²)`, entonces allí `cB/|E| = raiz(1 − q²)`:

- contra sin desplazar: `raiz(1 − 0.992090²)` = **0.125529**
- N=4 desplazado λ/2: `raiz(1 − 0.9998²)` = **0.019999**
- (colineal, control: `raiz(1 − 0.999513²)` = **0.031196**)

⇒ Medido en la moneda del invariante, el nulo λ/2 **sí** entrega lo que la lectura intuye: el supremo del invariante pasa de `cB/|E| = 0.1255` a **0.0200**, es decir **×6.3 más puramente eléctrico**. La intuición es correcta; el testigo es el **supremo del invariante**, no el foco. (Precisión declarada: 0.0200 sale de un `a_inv/pico` impreso con 4 cifras ⇒ 0.020 ± 0.003.)

## §6 §1 y §3 de la lectura son UN solo hecho: el máximo es invariante de fase

La lectura presenta como dos confirmaciones separadas: (i) «el misterio de por qué el antinodo *no cancelaba* queda resuelto por la **posición espacial de la cresta**», y (ii) «la ley `max = A + B` se cumple en los 4 casos». Son **el mismo enunciado**.

Medido: para `(A,B,phi)` en `(1,1,0) (1,1,pi) (1,0.7,pi) (2,1,pi)`, `max|A e^{ikx} + B e^{−i(kx+phi)}| = A + B` = 2.000000 / 2.000000 / 1.700000 / 3.000000. El máximo **no depende de la fase**: el desfase no puede cancelar nada en el máximo, sólo puede **moverlo de sitio**. Y eso es exactamente lo que el crudo enseña: mientras la cresta se mueve **+10 celdas exactas**, la métrica se mueve **−1.5981 %** (`111.719117598 → 109.933787`).

⇒ «Por qué no cancelaba» **no era una pregunta de posición**: era de invariancia. La posición de la cresta explica **dónde** está el máximo; **no** explica que el máximo valga `A + B`. La lectura acierta el hecho y lo cuenta dos veces como si fueran dos.

## §7 «No había ninguna fuga»: la fuga está medida y declarada, no ausente

Medido (`cola_rel`, residuo del absorbedor en los últimos 100 pasos): **1.850e-03** en las cuatro filas contra y **1.882e-03** en la corrida desplazada. No es cero. Y `a_medido_caja` / `a_medido` = 834.394/78.997 = **10.56** (sin desplazar) y 1179.98/109.934 = **10.73** (desplazado): el campo sobre las líneas de inyección es **10.6× / 10.7×** el de la ventana, un artefacto ya declarado en el propio `UNIVERSO` del instrumento («excluye la línea de inyección, que no es objeto de Maxwell: ahí cB/|E| = 0.514 y |E| = 6.9x lo prescrito, medido»).

⇒ Lo correcto es «**la fuga está medida y declarada**: 1.9e-03 del pico, y el exceso de la caja es un artefacto de las líneas de inyección, declarado». Decir «no había ninguna fuga» **borra las dos cifras que la declaración existe para acotar** — y borrar un residual declarado es la forma más rápida de que deje de estar declarado.

## §8 La precaución de la «Pestaña 3»: premisa a medias y cifra nueva

La lectura advierte que no hay que «evaluar `a_inv` ciegamente en el punto (0,0)» sino «muestrear tanto el origen como el **supremo espacial** (`max_r a_inv`)». La precaución es **correcta**; su premisa es **a medias**:

- `max_r a_inv` **ya existe** en el instrumento desde la primera corrida: `sim/maxwell2d.py` l.342–343 ejecuta `aim = float(ai[VENTANA_I0:VENTANA_I1 + 1, :].max())` y `a_inv_max = max(a_inv_max, aim)`, y l.375–376 lo devuelve como `a_inv_max_V_m` / `a_inv_rel_al_pico` — presentes en las **30 claves** de cada fila. No hay que añadirlo.
- Lo que **no** existe como campo propio es el invariante evaluado **en la celda del foco** (el foco tiene `E_foco_V_m`, `a_foco`, `b_foco_rel`, pero no su `a_inv`).
- Y la precaución **no** es cosmética: medido, el supremo del invariante **no** es el pico de `|E|`. En el pico de `|E|` el contra tiene `cB/|E| = 0.394424`, pero el supremo del invariante se alcanza donde `cB/|E| = 0.125529` (§5); en el colineal, `0.945773` contra `0.031196` ⇒ **en el colineal el pico de `|E|` está lejísimos de ser un objeto eléctrico, y el supremo del invariante sí lo es.** Muestrear el invariante en el pico de `|E|` habría dado una cifra que describe otro sitio.

## §9 Dos trampas de metro del mismo testigo (la rejilla de la sonda y su instante) y una del mío

(a) **La rejilla de la sonda no puede resolver el patrón.** `sim/maxwell2d.py` l.352 muestrea `i` en `(I_SL, I_SL+20, I_SL+40, IC−80, IC−40, IC, IC+40, IC+80, I_SR)` = 80, 100, 120, 160, 200, 240, 280, 320, 400. Con `λ/2 = 20` celdas, los saltos de **40 celdas = 1 λ = exactamente 2 espaciamientos de λ/2**: cada muestra de 40 golpea **la misma fase** del patrón estacionario. La «envolvente» suave de 200 a 320 que se lee en la tabla (39.8 · 40.3 · 19.4 …) es **aliasing**, no una envolvente. La posición de la cresta sólo la da `pico_i`, que se calcula sobre la ventana entera y no sobre la rejilla.

(b) **La sonda y el pico no comparten instante.** `sim/maxwell2d.py` l.428 imprime «sonda del eje en el instante del pico del **foco**»: el testigo desplazado lo fecha en `t_foco = 21.01 fs`, mientras `cB/|E| en el pico de la ventana = 0.3878` se toma en `t_max = 21.11 fs` (y sin desplazar: 20.921 fs frente a 20.454 fs). ⇒ `1.982` y `0.3878` son **dos sitios y dos instantes**; emparejarlos como «el foco contra el pico» mezcla las dos cosas. Además, los dos extremos de la sonda (`i = 80`, `i = 400`) **son** las dos líneas de inyección, es decir lo que el propio `UNIVERSO` excluye del objeto.

(c) **Trampa mía, cazada en este tramo:** emparejé con `zip()` las filas del contra (4 filas: N=2,4,8,16) con las del colineal (**5** filas: N=1,2,4,8,16) y el `zip` me devolvió `contra/colineal = 0.987692340` «constante» — un cociente **corrido una fila** (contra N=2 contra colineal N=1). Re-emparejado **por N** (`{f['corrida']['N']: f['corrida']}`), la razón real es **0.698403951** en las cuatro, con dispersión **7.77e-16** (idéntica hasta el último bit de doble precisión). Familia de «el mismo nombre, otro objeto»: una serie de 4 contra una de 5 no se alinea por posición.

## §10 ALCANCE: qué NO prueba esta adenda

- No prueba ni refuta **física nueva**: los invariantes de Lorentz ya estaban activos en el contra (`F > 0`), y el `0.394424` del pico es idéntico en las cuatro N.
- No adjudica la **causa** de las 2 celdas (§3) ni el factor `0.698403951` contra/colineal (declarado antes como conjetura `(1/√2)·0.987675`): se declaran, no se resuelven.
- No toca el **`--serie-nulo`** colineal, que sigue **pendiente, no corrido y no ordenado** (reporte base §8).
- No abre la **serie** del contra con nulo: `serie()` no reenvía `desplaza_dcha` y no hay camino de CLI a `serie("contra", nulo=True)`; abrirla exige **editar el instrumento** y **re-declarar su hash**. No se hizo.
- El residual `1.850e-03 / 1.882e-03` está medido, no explicado.
- Nada de este tramo se re-midió corriendo la simulación: todas las cifras salen del crudo ya sellado y de los testigos de `/tmp`, con la hora de arriba.

## §11 Frontera

Escrito en este tramo: **este archivo**, dentro de `sim/`. `sim/maxwell2d.py` (`1db75ea7b0b8cba4`), `sim/falsador.py` (`f04551c7f19ce73a`), `sim/medidas_aN.csv` (`4129d436e2cd081d`) y `sim/ADENDA_LECTURA_CONTRA_20261011.md` (`23a10dd7bf3e12c2`) quedan **intactos**. La mano vecina (`M main.tex`, `M main.pdf`, y los `sim/*` no rastreados de la pestaña sigma/phi) no se toca ni se cita como nuestra.
