# ADENDA 3 — Cuarta lectura del contra: la coincidencia espaciotemporal, la causa de las 2 celdas y las dos trampas

Hora de la medición: 2026-10-11T02:33Z (UTC). Sólo lectura: volcado de los dos JSON de etapa1, el testigo desplazado de /tmp y aritmética declarada. No se corrió FDTD. La pieza vieja (`ETAPA1_CONTRA_REPORTE_20261011.md`, sellada en 864f4a4) no se parchea: recibe apéndice.

## 1 Qué acierta la lectura (medido contra el crudo)
- Centro nominal del foco: celda 240 (`IC = JC = 240`), con brazos de 160 celdas a cada lado.
- Antinodo de la corrida simétrica: celda **232** = −8 celdas = **−0.2 λ** (crudo: `pico_i = 232` y `pico_lambda_del_foco = −0.2` en las **cuatro** filas).
- Traslado a **242** = +10 celdas = **+λ/4** (testigo desplazado: `pico_i = 242`).
- Desfase respecto al centro: **+2 celdas = +0.05 λ**.
- **β = 0.500000**: la razón `a_medido / sqrt(N)` es 1 / 1.41422 / 2.00000 / 2.82843 en las cuatro filas.
- **F = 1 − q²** exacto: q = 0.394424 da F = +0.844430, idéntico al `F_rel_pico` guardado (0.8444296302).
- El foco **no** es el antinodo: `foco/pico` = 0.476705 (simétrica) y 0.966092 (nulo).
- La fuga está declarada y medida: `cola_rel` = 1.850e−03 (simétrica) y 1.882e−03 (nulo).
- CONTROL y TESTIGO desplazado salen **bit a bit** idénticos (`109.933787` / `106.206118` / `242`).

## 2 La identidad que vuelve exacto el λ/4 (y que la lectura no nombra)
- Dos ondas contra-propagantes de igual amplitud: `E_L + E_R(x − δ) = 2 A exp(i k δ/2) cos(k x − k δ/2)` ⇒ el patrón se corre **δ/2**.
- δ = λ/2 = 20 celdas ⇒ **+10 celdas = λ/4**. No es coincidencia del conteo: es la mitad de la traslación.
- Es la misma cuenta con la fase: un desfase Δφ corre el patrón Δφ/(2k); Δφ = π da λ/4.
- Los brazos son simétricos (80 → 240 = 240 → 400 = 160) y **aun así** el antinodo simétrico no cae en 240 sino en 232. Ver §10 (convención).

## 3 «La causa exacta» cubre 0.966092 al 1.6 % y falla 0.476705 por ×1.54
- Envolvente de la onda estacionaria: |cos(π d / 20)|, con d = celdas del foco al antinodo (periodo λ/2 = 20 celdas).
- Simétrica: antinodos 232 / 252, foco 240 ⇒ d = 8 ⇒ predice **0.309017**; medido **0.476705** (×1.543).
- Nulo: antinodo 242, foco 240 ⇒ d = 2 ⇒ predice **0.951057**; medido **0.966092** (+1.58 %).
- ⇒ La geometría **sí** explica el **signo** del cambio (el foco pasa de 8 celdas del antinodo a 2, o sea de cerca-de-nodo a cerca-de-antinodo) y la magnitud del caso desplazado; **no** explica el caso simétrico.
- Un solo mecanismo no cubre el par: el residuo del caso simétrico (+54 %) queda sin causa nombrada.
- Ese residuo **no se puede examinar con el crudo**: el JSON guarda 9 muestras de sonda y las coordenadas del pico, no el perfil |E|(i) del eje en `t_max`.
- ⇒ «causa exacta del 0.9661» = **medición casi cerrada** (1.6 %); «causa exacta del par» = **pedida**, no hallazgo. El comando que la cerraría es una corrida con el perfil del eje.

## 4 El supremo del invariante no registra coordenada: «no coincide espacial ni temporalmente» no está medido
- Código (`sim/maxwell2d.py`, intacto, 1db75ea7b0b8cba4): `a_inv_max = max(a_inv_max, aim)` y `a_inv_rel_max = max(a_inv_rel_max, aim/em)`. Guarda **magnitud y razón**: ningún `(i, j)`, ningún instante.
- Lo medido: `a_inv_rel_al_pico` = 0.9920899249757815 (contra) y 0.9995132753995678 (colineal) ⇒ el supremo del invariante queda **0.79 %** y **0.049 %** por debajo del pico de |E|.
- Esa razón **no distingue** dos lecturas: (a) el supremo cae en **otra celda** (no coincidencia espacial); (b) cae en la **celda del pico** y allí q = sqrt(1 − 0.992090²) = 0.125529 (coincidencia espacial, con campo magnético chico).
- ⇒ «no coincide espacialmente» es **una** lectura posible, no una medición. Afirmarla exige guardar el argmax del supremo (edición declarada + hash nuevo).
- Lo que **sí** queda medido es la cota: q ≤ sqrt(1 − a_inv_rel²) = **0.125529** (contra) y **0.031196** (colineal) ⇒ F ≥ 0.984242 y F ≥ 0.999513.

## 5 La no-coincidencia temporal es, en parte, del metro
- `if k % DIAG_CADA == 0` con `DIAG_CADA = 20` ⇒ el invariante se evalúa en **55** de los 1113 pasos (cada 0.933979 fs); |E| se sigue en **todos** los pasos.
- Contra: `t_max` ⇒ k = 437, **437 mod 20 = 17** (no es instante de diagnóstico); `t_foco` ⇒ k = 447, **447 mod 20 = 7**.
- Colineal: `t_max` ⇒ k = 418, **418 mod 20 = 18**; `t_foco` ⇒ k = 448, **448 mod 20 = 8**.
- ⇒ **El instrumento nunca evaluó el invariante en el instante del pico**: la separación temporal observada no puede ser menor que la cadencia, y no se midió en el instante que importa.
- `t_foco` **no es un tiempo nominal de llegada**: es el argmax **temporal en la celda del foco** (rama `if ef > efoco_max`), idéntico a 15 dígitos en las 4 filas contra (20.921140050828093 fs) y en las 5 colineales (20.967839024155836 fs) ⇒ es forma de la celda, no reloj.
- La razón `foco/pico` compara **una celda con su propio máximo temporal** contra el **máximo espaciotemporal de la ventana** ⇒ es un hecho **espacial**, disfrazado de temporal.

## 6 La tabla intercambia celda e instante en la columna del nulo
- Los cuatro números con su par (celda, instante): 0.394424 = (232, t_max), pico de la simétrica; **0.3878 = (242, t_max)**, pico del nulo; **0.445 = (240, t_foco)**, sonda en el foco del nulo; 1.982 = (240, t_foco), sonda en el foco simétrico.
- ⇒ La columna del nulo imprime el **foco** (0.445) donde la otra imprime el **pico de la ventana** (0.394424): la fila compara dos sitios, y la caída 1.982 → 0.445 es **del foco**.
- Efecto del λ/2 **en el mismo sitio** (240, t_foco): 1.982 → 0.445 = **×4.454**. En el **pico** (232 vs 242, cada uno en su `t_max`): 0.394424 → 0.3878 = **×0.983** (1.7 %).
- ⇒ El «colapso del campo magnético» es del foco; el pico escalar apenas se mueve.

## 7 F en la columna Δφ = 0 es 0.9842, no 0.9996
- Cota con λ/2: q ≤ 0.019999 ⇒ **F ≥ 0.999600** ⇒ «F ≈ 0.9996» es correcto **para la columna del nulo**, y es cota, no medida.
- Cota de Δφ = 0: q ≤ 0.125529 ⇒ **F ≥ 0.984242**. La casilla «Casi puro (F ≈ 0.9996)» no describe esa columna.
- Razón de cotas: 0.125529 / 0.019999 = **6.2767** ⇒ el «× 6.3» de la lectura ✓, pero sobre **cotas**.
- Identidades contra el crudo: 1 − 0.394424² = 0.844430 = `F_rel_pico` (0.8444296302) · 1 − 0.3878² = 0.849611 · 1 − 0.445² = 0.801975 · 1 − 0.992090² = 0.015758 = cota de q² en el supremo (raíz 0.125529) · 1 − 0.9998² = 0.000400 (raíz 0.019999).

## 8 Las «dos trampas» son de la sonda impresa, no del localizador
- La sonda **no** localizó la cresta: `pico_i` sale de un `argmax` sobre la **matriz completa** de la ventana (celdas 100..380 por columnas 0..479) y el crudo imprime 232 / 242 ⇒ el submuestreo de la sonda no ocultó el antinodo a esta auditoría.
- La rejilla de la sonda **no** es «cada 1λ»: muestras 80, 100, 120, 160, 200, 240, 280, 320, 400 ⇒ huecos **20, 20, 40, 40, 40, 40, 40, 80** celdas (dos de λ/2, cinco de λ, uno de 2λ); hueco mínimo **20** celdas.
- Con estructura de periodo λ/2 = 20 celdas, un hueco de 40 muestrea **en** la tasa de Nyquist (2 por periodo), no por debajo: el riesgo es de **fase**, y en los datos las 9 muestras no cayeron todas en la misma fase (|E| de la sonda va de 3.5e11 a 4.3e14).
- Lo que sí es cierto y decisivo: el hueco mínimo es **20 celdas** y el desfase discutido es de **2** ⇒ la sonda no puede verlo; el desfase se midió con el localizador.
- «Desincronización temporal»: ver §5 — es de la cadencia, y `t_foco` es el argmax del foco.

## 9 Cifras del crudo que la lectura no cita
- Pico de la ventana en la simétrica: **111.719117598** (E_max = 4.483709e14 V/m en la celda 232), no ~106.
- El nulo: 109.933787 ⇒ el pico escalar casi no se mueve (**−1.5981 %**); lo que se mueve es **dónde** cae (232 → 242).
- Caja (incluye la línea de inyección = artefacto): 1180.011 vs 1179.98 ⇒ ×10.56 y ×10.73 de la ventana.
- `a_inv_rel` contra **no** es exactamente N-invariante: 0.9920899249757815 / …7712 / …7815 / …7991 ⇒ dispersión **2.787e−14** (el colineal sí: 2.220e−16).
- F en el foco simétrico es **negativo** (q = 1.982 ⇒ F = −2.928324): dominio magnético. La lectura no lo cita.
- Razón contra/colineal a N fijo: 78.997345641 / 113.111252428 = **0.698403951**, igual en las cuatro filas (dispersión 7.77e−16).
- `t_max` idéntico en las 4 filas contra y en las 5 colineales; `t_foco` también ⇒ la forma temporal en el foco es N-invariante.

## 10 Alcance, corrección propia y convención declarada
- **Corrección propia**: en la ADENDA 2 escribí 0.125529 como si fuera el valor de q en el supremo. Es una **cota superior**, derivada suponiendo que el supremo cae en la celda del pico — justo lo que no está medido (§4).
- **Convención declarada**: «+2 celdas» toma como referencia que el antinodo del **nulo** caiga en 240. Con la referencia simétrica (antinodo de Δφ = 0 en 240) el nulo queda en +10 y la simétrica en −8. Ninguna referencia está medida: 240 es el punto **simétrico de la geometría**, no el punto donde el antinodo deba caer (medido: cae en 232).
- Instrumentos intactos: `sim/maxwell2d.py` 1db75ea7b0b8cba4 · `sim/etapa1_contra.json` 221a9fe8c3e269f4 · `sim/etapa1_colineal.json` 33bcf93826ce494b · `sim/medidas_aN.csv` 4129d436e2cd081d · `sim/falsador.py` f04551c7f19ce73a.
- Pendientes que esta adenda deja **nombrados**, no ejecutados: (a) guardar el **argmax** del supremo del invariante; (b) el **perfil |E|(i)** del eje en `t_max`; (c) la serie nula colineal (`--serie-nulo`), declarada pendiente en §8 del reporte. Las tres exigen orden.

## 11 Frontera
- Se escribe **sólo** dentro de `sim/**`. La pieza sellada `ETAPA1_CONTRA_REPORTE_20261011.md` (864f4a4) **no se parchea**.
- El material de la mano vecina (`main.tex`, `main.pdf`, `refs.bib`, `sim/field_solver.py`, `sim/runner_2d3v.py`, `sim/PREREGISTRO_SIGMA_PHI_20261011.md` y compañía) queda **intacto y sin preparar**.
- `sim/medidas_aN.csv` (4129d436e2cd081d) no se toca: es el entregable sellado.
- No se relaja ninguna banda pre-registrada tras ver los datos; las correcciones se declaran como EXTRA (hoy no hubo ninguna que relajar).
