# PRE-REGISTRO — barrido FDTD (Yee 2D3V) del jitter de fase sigma_phi (pestana B)

T_UTC de sello: se imprime al escribir el archivo (ver ficha). Sellado ANTES de
ver cualquier salida del barrido.

Autorizacion: orden del dueno 2026-10-11 («TOMA EL TESTIGO»). La vecina
(`2cd28bb3`) dejo fijado el benchmark analitico sigma_phi* = 0.554987 rad
= 0.2357 fs y catalogO su barrido como verificacion de consistencia del solver.
El ensayo FDTD 2D3V es el paso siguiente.

## 0. UNIVERSO DECLARADO
- instrumento: copia congelada `runner_2d3v_frozen.py` sha16=368627d18d83d253
  (22048 B, 495 l) + UN parche declarado (`--fases`) => el sha16 del parcheado se
  imprime en el sello. Ningun otro cambio.
- entradas: `sim/params.py` sha16=9983b3d25a68f032 (5343 B) ·
  `sim/configs.json` sha16=c7508e0430319162 (3030 B).
- malla 480x480 = 12 lambda_L por lado ; dx = lambda_L/40 ; CFL = 0.6 (declarado
  en el instrumento; el limite 2D es 1/sqrt(2) = 0.7071) ; 300 pasos ;
  medicion hasta el paso 260 (ventana CAUSAL: el primer rebote del borde llega
  despues) ; Omega_foco = disco r <= 80 celdas = 2 lambda.
- unidad: a0 = eE/(m_e omega c). Motor: numpy float64 (FDTD Yee 2D3V,
  c = omega = k = 1).
- polarizacion: **linear** (pol = zhat). [DECLARADO: con linear, en el foco todas
  las contribuciones son PARALELAS => |suma| es el modulo de la suma de fasores
  escalar, y la forma cerrada del benchmark vale TAL CUAL. Con `circular` el
  sumando en el plano se anula solo para N>=2 y la forma cerrada seria otra
  (offset 2 en vez de 1): NO se usa.]
- ventana: reloj UTC.

## 1. QUE ES Y QUE NO ES (etiqueta obligatoria, va impresa)
ES el ensayo con **evolucion temporal real**: la condicion inicial del
instrumento es la superposicion exacta de ondas planas y el solver la propaga
paso a paso.
DECLARADO, y es una frontera: **el objeto no cambia; cambia el metro.** El FDTD
aniade la discretizacion y la marcha temporal, y no aporta una fuente fisica
independiente: su estado inicial ya es la solucion analitica. Lo que se mide es
si el instrumento conserva su propio dato. Etiqueta: **verificacion del
instrumento contra su propia solucion exacta; NO evidencia fisica.**
DIVERGENCIA DECLARADA con la letra de la orden (no se adjudica): la orden dice
inyectar en «la frontera de la caja». El instrumento NO inyecta en la frontera:
**la inyeccion es la CONDICION INICIAL** (`campos()`), y `campos()` ya recibia un
`fase` por haz, luego el parche solo lo hace accesible.

## 2. OBJETO — dos lecturas del mismo campo, las dos declaradas
- LECTURA FOCO: `a_centro` = max_t |E(r = 0, t)|, en el nodo (NX//2, NY//2).
  ES la suma de fasores en el foco => **tiene forma cerrada**. Se juzga.
- LECTURA PICO: `a_fdtd` = max_{r en Omega_foco, t} |E(r,t)|.
  **NO tiene forma cerrada pre-registrada** => se reporta, NO se juzga.
  (Regla heredada, verbatim, del pre-registro de la vecina.)

## 3. PREDICCION (ground truth matematico)
Fases phi_j iid N(0, sigma^2). |suma|^2 = N + 2 sum_{j<k} cos(phi_j - phi_k) =>
E|suma|^2 = N + N(N-1) e^{-sigma^2}. Con amplitud por haz a_b(N) = a_ref/sqrt(N):

    a_foco(N, sigma) = a_ref * sqrt( 1 + (N-1) exp(-sigma^2) )

sigma = 0 => a = a_ref sqrt(N) (coherente, = N a_b). sigma -> inf => a -> a_ref.
beta_teo(sigma) = pendiente log-log por minimos cuadrados sobre el MISMO conjunto
de N que se mida. Punto critico analitico: sigma* = 0.554987 rad = 0.2357 fs
(1 rad = 0.4247 fs con lambda_L = 800 nm).

## 4. CONTROLES
- **K0 (POSITIVO) sigma = 0**: la serie es DETERMINISTA (una fase global no cambia
  |E| => una sola realizacion da el valor de la ensemble, no una estimacion).
  Se exige beta_{N>=2}(0) en 0.5000 +- 5e-3. Fuera => RC = 3.
- **K1 (NULO)** phi_j iid U(0, 2pi): E[e^{i phi}] = 0 => a -> a_ref => beta = 0.
  Aceptacion |beta| <= 3 SE. **Este nulo SI puede enrojecer.**
- **K2 (ANCLA DEL INSTRUMENTO)**: el propio instrumento calcula la solucion
  exacta; se exige |a_centro / a_exacto - 1| <= 0.05 en cada (N, sigma).

## 5. DISENO Y ACEPTACION (sellado antes de ver la salida del barrido)
- rejilla sigma (rad): **0.0, 0.25, 0.555, 0.75, 1.00** (la de la orden,
  verbatim). En fs: 0.000, 0.106, 0.236, 0.319, 0.425.
- N: 1, 2, 4, 8, 16.  **M = 64 replicas** por (N, sigma) para sigma > 0;
  M = 1 para sigma = 0 (determinista, ver K0).
- fases: phi_j iid N(0, sigma^2), j = 0..N-1, con `numpy.random.default_rng(s)`,
  s = los 8 primeros bytes de sha256("sfqed/fdtd_sigma_phi/20261011|s<si>|N<N>|r<rep>").
  El vector se pasa al parametro `--fases` (uno por haz, rad).
- estimador: a(sigma, N) = sqrt( <a_rep^2> ) (RMS; es el objeto de la forma
  cerrada). SE(a)/a = 0.5 * sd(a^2)/<a^2> / sqrt(M).
- beta por minimos cuadrados de log a contra log N, en DOS conjuntos: los 5 N y
  N >= 2 (el sesgo conocido del haz monomodal se declara, no se arrastra).
- **sesgo del instrumento**: ademas del beta crudo se reporta beta_norm sobre
  a(sigma,N)/a(0,N) (la serie sigma = 0 es la calibracion del sesgo del
  instrumento; a(0,N) = a_ref sqrt(N) por K0).
- criterio: |beta_norm(sigma) - beta_teo(sigma)| <= max(3 SE_beta, 5e-3) en TODO
  sigma => RC = 0. Si falla alguna => RC = 1 nombrando la sigma. Falta el
  pre-registro o falta `configs.json` => RC = 2. K0/K1/K2 fuera de su extremo => RC = 3.
- pregunta ordenada: si beta(0.555) <= 0.45 => el umbral de ruptura ocurre a
  sigma MENOR que 0.2357 fs; si beta(0.555) > 0.45 => a sigma MAYOR.

## 6. LO YA VISTO ANTES DEL SELLO (declarado, no adjudicado)
Una sola salida del instrumento se vio antes de sellar: la fila **N = 8,
pol = linear, sigma = 0** corrida a las **01:49:42Z** como **medicion de COSTO**
(`a_fdtd = 484.4772432`, `ratio` contra a_pred = 1.00443, 4 s). Ninguna otra
salida del barrido existia al sellar. Se declara porque el pre-registro deja de
ser «antes de toda salida» en sentido estricto: es «antes de toda salida con
sigma > 0 y antes de todo beta».

## 7. COEXISTENCIA (medida antes de escribir, no supuesta)
`sim/` es territorio de la vecina `2cd28bb3`. Medido: cinco archivos de `sim/`
re-escritos a las 01:22:32Z–01:22:40Z (entre ellos `runner_2d3v.py`, el
instrumento de esta orden) **con bytes identicos** (re-sello, no cambio: sha16
368627d18d83d253 antes y despues), y `main.tex` / `main.pdf` sucios por una
tercera pestana. Por eso el barrido se corre en **cuarentena** (`/tmp`) sobre una
copia congelada y **solo se aterrizan** los dos artefactos ordenados dentro de
`sim/data/sigma_phi/`.

## 8. PERIMETRO
No se toca: `sim/medidas_aN.csv` (residuo historico congelado, 1360 B, 18 l,
sha16 4129d436e2cd081d) ni ningun otro archivo de `sim/`. Cero actas en la
raiz de `platino-labs/`. Salida unica del barrido:
`sim/data/sigma_phi/medidas_fdtd_sigma_phi.csv`.
