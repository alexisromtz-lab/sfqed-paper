# ETAPA 1 — la ley de escala del campo, medida en malla (11-Oct-2026)

Pieza: `sim/maxwell2d.py` (FDTD 2D3V en SI) + `sim/falsador.py` (test pre-registrado).
Objeto de la Etapa 1: el campo, no los pares. `a_medido = max_{(x,y),t} |E|` por corrida,
con `N` haces colineales en vacio clasico.

## 1. Un comando, un veredicto

```
cd /Users/marlene/sfqed-paper
python3 -B sim/maxwell2d.py --control-cfl          -> OK
python3 -B sim/maxwell2d.py --control-energia      -> candidato 2 = 7.944e-05 (ROJO vs 1e-9)
python3 -B sim/maxwell2d.py --control-energia-pec  -> candidato 2 = 4.441e-16 (OK vs 1e-9)
python3 -B sim/maxwell2d.py --serie                -> sim/medidas_aN.csv (5 filas)
python3 -B sim/falsador.py                         -> RC=0
```

Hora de la corrida: `2026-10-11T01:15:24Z` … `2026-10-11T01:15:44Z` (5 corridas, ~5 s cada una).

## 2. Series medidas (colineal, cfl 0.7, 1113 pasos, ventana de medida celdas [100,380])

| N | a_medido | a / (a(1)·sqrt(N)) − 1 |
|---:|---:|---:|
| 1 | 79.981733620 | +0.000e+00 |
| 2 | 113.111252428 | −7.772e-16 |
| 4 | 159.963467240 | +0.000e+00 |
| 8 | 226.222504855 | −7.772e-16 |
| 16 | 319.926934480 | +0.000e+00 |

`beta = 0.500000000000` (pendiente log-log, 12 cifras). Bandas pre-registradas: verde
`[0.45, 0.55]`, muerte `<= 0.35` o `>= 0.65`. **El falsador sale `RC=0` (VERDE)** y las
cinco desviaciones por N son `0.0000` contra `tol 0.20`.

## 3. ALCANCE — lo que la Etapa 1 NO prueba

1. **`beta = 0.5` es una identidad de superposicion, no un hallazgo.** El modelo inyecta
   `a_beam = A_REF / sqrt(N)` (`A_REF = 170.533802`, `sim/configs.json`) y el solver es
   lineal: la suma coherente de N haces colineales **tiene que** dar `sqrt(N)·A_REF`. La
   desviacion medida (0 o 1 ulp) lo confirma: la corrida mide **la cadena**, no la fisica.
   La proposicion `eq:oneoverN` de `main.tex` es la misma identidad bajo su propia
   hipotesis. Un solver lineal **no puede refutarla**.
2. **El invariante `a` de esta geometria es casi nulo.** En el pico de la ventana:
   `a_inv = 1.42785e+14 V/m`, `a_inv/|E|_pico = 0.9995` — el invariante **sigue a `|E|`**
   (rotulo del instrumento: `1.0 = campo puramente electrico`), y `cB/|E| = 0.9458`
   (transversa propagandose). El objeto del que habla la ley `1/N` (`a == E_cr`;
   `eq:ab`, `eq:cp_inv`) exige la geometria **contrapropagante**; el colineal la deja
   fuera. Por eso el VERDE colineal es **control de instrumento**, no evidencia.
3. **El maximo es ciego al desfase de brazo.** Extensión declarada, no corrida aqui:
   `--serie-contra-nulo` (`desplaza_dcha = 20` celdas = lambda/2) colapsa el foco y **no**
   mueve el maximo. Un instrumento que solo mira el maximo no mide el desacople.

## 4. Controles, y los cuatro defectos pagados en el camino

**(a) CFL.** El protocolo pre-registra `CFL_PRE = 0.9`. Eso **viola von Neumann en 2D**
(limite `1/sqrt(2) = 0.7071`). Medido: a 0.9 el campo es `inf` en el paso 400; a
`CFL_2D = 0.70` crece `3.171e+04`. **Correccion declarada, no silenciosa** (viaja dentro
del string `UNIVERSO`).

**(b) Transito.** El protocolo fija el transito `19.485 lambda_L` derivado de 866 pasos a
CFL 0.9. A CFL 0.70 hacen falta **1113 pasos**; `pasos` se **deriva** en `correr()`.
Medido: residuo del absorbedor `2.395e-01` -> **`2.595e-03`**, con el pico
**bit-identico** (`a_medido = 79.9817`) — la reparacion no movio el objeto medido.

**(c) Control de energia — DEFECTO #1 (el metro).** La version anterior anclaba `U0` en
`t = TAU/2`, **en medio del pulso y con la fuente todavia inyectando**, y lo rotulaba
"medido tras apagar": `2.464e-01` con **286 muestras**, de las cuales **214 median la
inyeccion**. Nada enrojecio porque **no habia `assert` detras del veredicto** (familia: un
rotulo fijo que afirma lo que la linea siguiente desmiente **no protege: informa**).
Corregido: ancla en el primer paso con la fuente apagada (paso 429 de 1800,
`t = 20.034 fs > TAU = 20.000 fs`), **1372 muestras libres**, 428 pasos excluidos.

**(d) Control de energia — DEFECTO #2 (el emparejamiento).** Mi "invariante exacto de Yee"
escrito a mano (E adelantada + producto de las dos H) dio `1.090e-03`: **no era el
invariante exacto**. El emparejamiento temporal se habia elegido **despues** de ver la
salida. Corregido midiendo **cinco emparejamientos en la MISMA corrida**. Lo unico
pre-registrado es el **umbral** (`1e-9`: un invariante exacto no puede diferir mas que
roundoff).

| candidato | sin PEC | con PEC |
|---|---:|---:|
| 1) E(n+1)^2 + H(n+1/2)·H(n−1/2) | 1.090e-03 | 2.545e-02 |
| **2) E(n)·E(n+1) + H(n+1/2)^2** | **7.944e-05** | **4.441e-16** |
| 3) E(n)·E(n+1) + H(n+1/2)·H(n−1/2) | 5.889e-04 | 1.284e-02 |
| 4) E(n)^2 + H(n−1/2)^2 | 5.947e-04 | 1.277e-02 |
| 5) E(n+1)^2 + H(n+1/2)^2 (sin centrar) | 5.798e-04 | 1.275e-02 |

**El invariante exacto es el candidato 2**: `U = 1/2 eps0 E(n)·E(n+1) + 1/2 mu0 |H(n+1/2)|^2`
(`H` centrada, `E` bilineal). Y **la hipotesis del muro queda confirmada**: cambiando
**solo** la condicion de pared (E tangencial = 0 en las cuatro paredes, `pec_muros()`), la
deriva pasa de `7.944e-05` a **`4.441e-16` = 2 ulp**. La causa era el par de diferencias
con relleno de ceros: `ddx = −ddx_f^T + (1/dx)(E_{N−1}H_{N−1} − E_0 H_0)`, adjunto
**solo si la E tangencial se anula en el muro**. `pec_muros()` **no** se usa en
`correr()`: la caja de produccion es absorbedora por diseno (60 celdas, `ALFA_ESPONJA =
0.10`, residuo `2.595e-03`), y eso es perdida declarada, no fuga.

**(e) Dos defectos del instrumento, ya corregidos** (declarados aqui porque movieron
cifras): el pico caia en la **linea de inyeccion** (celda (80,243)), que **no es objeto de
Maxwell** — ahi `cB/|E| = 0.514` y `|E|` es 6.9x (blando) / 21x (duro) lo prescrito;
resuelto **declarando la ventana [100,380]** y publicando el maximo de la caja como
artefacto (`a_medido_caja = 1161.69`, caja/ventana = 14.52). Y el signo de la curvatura
estaba invertido (el frente "divergia"): corregido por direccion, medido
4.2 -> 22.9 -> 65.2 -> **78.0 (foco)** -> 56.8 -> 27.1.

## 5. Calibracion lineal declarada (eta)

`a_beam = A_REF / sqrt(N)` con `A_REF = 170.533802`; la lamina radia ~la mitad de la
amplitud prescrita por direccion: **`eta = 79.981734 / 170.533802 = 0.469008`**, medido en
N=1. Es una calibracion **lineal, constante en N** => **cancela en beta** y por eso no
cambia el veredicto, pero **se declara, no se esconde** (el CSV la lleva en su cabecera).

## 6. Lo que falta (declarado, no adjudicado)

1. `--serie-contra` (beta y el invariante `a` en la geometria contrapropagante,
   `N = 2,4,8,16`) y `--serie-contra-nulo` — **es ahi** donde el objeto de `eq:cp_inv`
   tiene sentido; el colineal no lo toca.
2. `--serie-nulo` (nulo colineal del protocolo §5.2: la escala debe romperse).
3. El pico de la **caja** sigue siendo artefacto de la linea de inyeccion: si alguna
   corrida futura reporta el maximo de la caja en vez de la ventana, el numero cambia por
   un factor 14.5.

## 7. Cierre

- `beta = 0.500000000000`, `RC=0`, cinco desviaciones nulas contra `tol 0.20`.
- Veredicto **de instrumento**: la cadena inyecta, propaga, enfoca y suma como dice su
  propio modelo, a 12 cifras, con el absorbedor a `2.6e-03` y la energia del esquema
  conservada **exactamente** (2 ulp) cuando la caja es PEC.
- Veredicto **sobre el papel**: **ninguno**. La ley `1/N` que la pieza persigue vive en la
  geometria contrapropagante; esta Etapa 1 la dejo **medida en el caso donde es una
  identidad**, y eso es un control, no una prueba.
