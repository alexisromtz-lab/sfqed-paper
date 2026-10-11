# ADENDA 4 — Quinta lectura del contra: la cadencia del invariante, la casa del nombre y las cotas

Hora de la medición: 2026-10-11T02:43Z (UTC). Sólo lectura: el bucle de `correr()` y las fuentes (`envolvente`, `perfiles`, `inyectar`) de `sim/maxwell2d.py` (sha16 `1db75ea7b0b8cba4`, intacto), `sim/params.py` (intacto), los dos JSON de etapa1, el testigo desplazado de `/tmp` y aritmética declarada sobre constantes declaradas. No se corrió FDTD. La pieza vieja (`ETAPA1_CONTRA_REPORTE_20261011.md`, `864f4a4`) y el apéndice anterior (`ADENDA_3_LECTURA_CONTRA_20261011.md`, `0d0d87c`) no se parchean: reciben apéndice.

UNIVERSO DECLARADO: lectura de código de `sim/maxwell2d.py` (715 líneas, sha16 `1db75ea7b0b8cba4`) + `sim/params.py` + las 4 filas de `sim/etapa1_contra.json` + las 5 de `sim/etapa1_colineal.json` + `/tmp/sonda_contra_nulo_dcha20_out.txt`. MOTOR: `sed -n`, `grep -nE`, `grep -ci`, `python3 -B` (sin FDTD). UNIDAD: paso de bucle `k` (el campo guardado es el de `t = (k+1) dt`, después de `paso()`), celda, grado de portadora. ÁMBITO: `sim/**`, sólo lectura salvo este archivo.

## 1 Qué acierta la quinta lectura, medido contra el crudo
- El paréntesis del instante: la cresta de `t_max` cae en el índice `k = 437`; el invariante se evalúa en `k` múltiplo de 20; `437 mod 20 = 17`. Entre 420 y 440 el instrumento **tiene** el hueco que la lectura denuncia.
- El traslado del pico: simétrico en (232, `t_max`) con `q = 0.3944241` ⇒ F = +0.844430; desplazado en (242, `t_max`) con `q = 0.3878` ⇒ F = +0.849611 ⇒ **×0.983208**.
- El hundimiento en el foco fijo (240, cada `t_foco`): `q` 1.982 → 0.445 = **÷4.454**; y F pasa de **−2.928324** a **+0.801975**. En el simétrico ese punto tiene F < 0: «predominio magnético» no es una metáfora, es el signo de la identidad F = 1 − q².
- Las dos cotas: `F ≥ a_rel²` con `a_rel = 0.9920899249757815` (4 filas del contra) da 0.9842424192; con `a_rel = 0.9998` (1 corrida desplazada) da 0.9996000400 ⇒ la razón de las anchuras `q`: 0.125529 / 0.019999 = **6.2767**.
- El 1.6 % de la corrida desplazada: 0.966092 medido contra 0.951057 del modelo ⇒ **+1.581 %**; y el simétrico falla **×1.5426** (0.476705 / 0.309017).
- Los dos máximos son de instantes distintos **en las dos** configuraciones: `t_foco − t_max` = 10.000000 pasos (contra) y 30.000000 pasos (colineal), con `dt = 4.669897332774128e−17 s`.

## 2 Corrección de atribución: la cadencia es del invariante, no de los campos
- El bucle lee los campos **cada paso**: `e = modulo_E(F)`, el máximo de la ventana, `idx = argmax`, `ef = e[IC, JC]`, y los dos ramales `if em > emax:` / `if ef > efoco_max:` que guardan `t_max` e `t_foco` con su celda.
- La cadencia de 20 es de **una sola línea**: `if k % DIAG_CADA == 0:` → `ai = invariante_a(F)`.
- Consecuencia: el localizador de la cresta **no tiene hueco**; quien puede tenerlo es el supremo de `a` (`a_inv_max`) y la razón (`a_inv_rel_max`). Atribuir el hueco a «los campos» le da al instrumento una ceguera que no tiene.
- Convención declarada: `k` es índice de bucle y el campo que se guarda es el de `t = (k+1) dt`; `t_max_fs` y `t_foco_fs` se imprimen así. La distancia de 3 pasos vale en las dos convenciones.

## 3 El ancho ciego real: 3 pasos y 2 pasos (no una cadencia entera)
- CONTRA `t_max`: índices de diagnóstico vecinos **420 (−17 pasos)** y **440 (+3 pasos)**.
- COLIN `t_max`: **400 (−18 pasos)** y **420 (+2 pasos)**.
- 3 pasos = 0.1400969 fs = **0.329868 rad = 18.90 grados** de portadora; 2 pasos = 0.219912 rad = 12.60 grados. Por paso: `omega dt = 0.109956 rad = 6.3000 grados`.
- ⇒ «saltándose por completo el instante» es exacto para el **instante** y exagerado para la **vecindad**: el invariante se evaluó a 3 pasos de la cresta, no a una cadencia. El artefacto que la cadencia puede fabricar queda **acotado** por el cambio del campo en 3 pasos — y ese cambio no está en el crudo.

## 4 Corrección de dirección: de «no medido» no se sigue «no existe»
- El crudo autoriza *no se puede afirmar el desacoplamiento*. No autoriza *el desacoplamiento no existe*.
- Pasar de lo primero a lo segundo es el mismo defecto categorial que la lectura corrige, con el signo cambiado.
- Lo que lo cerraría está ya nombrado y **no ejecutado** (ADENDA 3 §10.a): guardar el **argmax del supremo del invariante** (celda e instante). Es una línea de instrumento, no una corrida nueva.

## 5 Corrección de celda: la cresta está a 2 celdas del detector, y la cresta misma no es pura
- Cresta desplazada: **242**. Sonda y foco: **240**. «Encima» son **2 celdas = 0.05 λ**, el mismo +2 que la lectura marca en otro párrafo.
- En la cresta (242, `t_max`) el campo lee `q = 0.3878` ⇒ **F = +0.849611**: pura no es. La pureza 0.999600 es una **cota sobre un supremo cuya coordenada no se guarda**, no el valor en la cresta.
- Los dos números del par ×0.983 no están en la misma celda: 0.3944 es (232, `t_max`) y 0.3878 es (242, `t_max`) — cada uno en **su** cresta. Eso es lo correcto y conviene decirlo: es una comparación entre dos sitios, no dentro de uno.

## 6 Corrección de nombre de celda: 240 es el centro, no el origen
- 240 = `IC = JC = NX // 2` con `NX = 480`: el **centro geométrico** de la caja y el sitio donde la sonda muestrea.
- El origen de la malla es la celda 0. «El detector del origen» nombra con `origen` una celda que es el centro: el objeto no se mueve, el nombre sí.

## 7 La envolvente: transversal sí gaussiana (fórmula sin nombre), temporal no gaussiana (sin² compacta)
- Transversal: `g = exp( - ( ((j - JC) * DX) / W0 )² )`, con `W0 = 2.0 λ_L = 1.6e−06 m = 80 celdas`; en el borde de la caja `g = 1.330e−04` ⇒ el perfil no está truncado por el borde.
- La **palabra** `gauss` en `maxwell2d.py`: **0** veces (0 también en `params.py`, `falsador.py`, `lector_invariantes.py`, `schwinger_offline.py`; 2 en `field_solver.py`, 1 en `runner_2d3v.py`, 1 en `gen_configs.py`). El nombre tiene casa **en el resto de la carpeta**, no en mi metro: mi metro la escribe como fórmula.
- Temporal: `envolvente(t) = sin(π t / TAU)²` y **0 fuera de [0, TAU]** ⇒ finita y compacta, **no** gaussiana. `TAU = 20 fs = 428.27 pasos = 7.4948 ciclos`.
- Rótulo del archivo vecino, sin editar: `params.py` comenta `TAU` como «FWHM»; con esa casa el soporte es TAU y el **FWHM = TAU/2 = 214.14 pasos**. El rótulo no es la llave (familia ya escrita en el corpus).

## 8 El mecanismo del ×1.54: ingrediente medido, veredicto pendiente
- El mecanismo nombra un ingrediente que **existe** y ahora tiene dimensiones: cintura 80 celdas, brazo 160 celdas ⇒ `z_R = π W0² / λ = 502.7 celdas` ⇒ el perfil transversal sólo cambia **4.94 %** de ancho a lo largo del brazo.
- Peso del término transversal frente a `k²` en la ecuación: `( λ / (π W0) )² = 0.02533 = 2.533 %` — del orden del 1.6 % que la lectura da por bueno, y **no** convertible en el piso de un nodo sin el perfil axial.
- Sigue sin crudo: nada guardado tiene el perfil axial. La medición que lo cierra es el pendiente (b) de ADENDA 3 §10: el perfil `|E|(i)` sobre el eje en `t_max`.
- Se registra como hipótesis con casa localizada, `[REF]`: su ingrediente se puede medir en el archivo; su explicación, todavía no.

## 9 Las cotas: identidad, truncar, y no sumar conjuntos distintos
- `q ≤ sqrt(1 − a_rel²)` ⇒ `F = 1 − q² ≥ a_rel²` es **identidad**, no aproximación: la cota se **trunca**, no se redondea. `0.9842424192` se publica 0.984242; 0.984243 sería una cota optimista en 4e−07. (`ADENDA 3` §4 escribe 0.984242; la forma redondeada salió de una impresión mía en terminal — la pieza estaba bien, mi impresión floja.)
- Las **dos** cotas no vienen del mismo conjunto: 0.9842424192 sale de las **4** filas del contra; 0.9996000400 sale de **1** corrida desplazada. El cociente 6.2767 es un cociente entre una cota de 4 filas y una de 1.
- La tercera, colineal: `a_rel = 0.9995132753995678` ⇒ `F ≥ 0.9990267877`.
- Ninguna de las tres es el valor en la cresta: las tres son cotas de un supremo.

## 10 Frontera
- Sólo lectura fuera de este archivo: `sim/maxwell2d.py` (`1db75ea7b0b8cba4`) y `sim/params.py` intactos; `sim/medidas_aN.csv` (`4129d436e2cd081d`) intacto.
- No se tocó nada de la mano vecina: `main.tex`, `main.pdf`, `sim/field_solver.py`, `sim/runner_2d3v.py`, `sim/barrido_sigma_phi.py`, `sim/data/`, `sim/medidas_aN_circular.csv` ni los documentos del preregistro sigma-phi. El barrido de 1605 corridas en `/tmp/fdtd_b_sigma_phi_20261011/RUN_sweep.log` es de esa otra pestaña: se cita, no se hereda.
- Nada de este apéndice afirma física nueva: afirma **qué midió el instrumento, dónde y cuándo**, y dónde su lectura puede desviarse del objeto.
