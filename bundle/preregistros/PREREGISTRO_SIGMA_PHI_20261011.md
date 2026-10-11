# PRE-REGISTRO — barrido de jitter de fase sigma_phi (pestana de CAMPOS, Etapa 1)

T_UTC de escritura: 2026-10-11T01:13Z
Autorizacion: el dueno ratifico (a) geometria contra-propagante coaxial eq:cp_inv
y (b) que `sim/field_solver.py` corre el barrido estocastico «catalogado
formalmente como verificacion de consistencia del solver, no como descubrimiento
fisico».
Se sella ANTES de ver cualquier salida del barrido.

## 0. UNIVERSO DECLARADO
- entradas: `sim/params.py` sha16=9983b3d25a68f032 (5343 B) ·
  `sim/configs.json` sha16=c7508e0430319162 (3030 B) ·
  `main.tex` sha16=4299786a34bdb313 (22367 B, NO se toca).
- geometria: N haces COAXIALES CONTRA-PROPAGANTES (+-z) con la misma helicidad de
  laboratorio (familia `coaxial_contra` de `field_solver.haces`) = eq:cp_inv.
  La palabra «co-propagante» del PROTOCOLO 1 §1 esta declarada ERRATA de
  redaccion (medido: ahi F = G = 0 identicamente => a == 0, Lemma 1).
- amplitud por haz: a_beam(N) = a_ref / sqrt(N); a_ref = 170.53380233310853.
- unidad: a0 = eE/(m_e omega c). Motor: numpy (suma de fasores) reutilizando
  `field_solver.haces` (NO se re-implementa el cono ni la geometria).
- ventana: reloj UTC de arriba.

## 1. QUE ES Y QUE NO ES (etiqueta obligatoria, va impresa en cada salida)
ES **verificacion de consistencia del solver**. NO es evidencia fisica.
Razon declarada: el solver de Etapa 1 es una SUMA LINEAL DE FASORES; la forma
cerrada y el numero son el mismo objeto. El barrido puede fallar por error del
codigo, nunca por fisica. El ensayo empirico real queda reservado al FDTD 2D3V
(`runner_2d3v.py`) de la pestana vecina.

## 2. OBJETO — dos lecturas del mismo campo, las dos declaradas
Con P = suma de los fasores de los haces +z y M = la de los -z:
- LECTURA FOCO: a_foco(fases) = a_beam * |P + M|          (suma vectorial EN el foco)
- LECTURA PICO: a_pico(fases) = a_beam * (|P| + |M|)      (maximo sobre la malla)
  [el max sobre la malla vale exactamente esto en esta familia: no hay envolvente
  longitudinal (rho = distancia PERPENDICULAR al eje del haz) y el antinodo del
  patron estacionario siempre cae dentro de la caja de 6 lambda_L]
- IDENTIDAD DECLARADA, NO EVIDENCIA: |P|+|M| >= |P+M| (desigualdad triangular).
- IDENTIDAD DECLARADA, NO EVIDENCIA: para N=2, a_pico = 2 a_beam para TODO sigma.

## 3. PREDICCION (forma cerrada = ground truth matematico)
Fases iid N(0, sigma^2). <|suma|^2>^(1/2) = sqrt(N + N(N-1) exp(-sigma^2)):

    a_foco(N, sigma) = a_ref * sqrt( 1 + (N-1) exp(-sigma^2) )

sigma=0 => a = a_ref sqrt(N) (coherente). sigma->inf => a -> a_ref (incoherente).
Umbral: sigma* tal que beta_LS(N in {1,2,4,8,16}) = 0.45  =>  0.554987 rad
= 0.2357 fs con lambda_L = 800 nm (1 rad = 0.4247 fs).
La LECTURA PICO no tiene forma cerrada pre-registrada (exige <|P|>) => se
reporta, NO se juzga.

## 4. CONTROLES
- K0 (POSITIVO) sigma = 0: todas las fases identicas => a_foco = a_pico = a_ref sqrt(N)
  => beta = 0.500000000 EXACTO. Tolerancia 1e-12.
- K1 (NULO) fases iid U(0, 2pi): E[exp(i phi)] = 0 => a_foco -> a_ref => beta = 0.
  Aceptacion: |beta| <= 3 SE. Este nulo SI puede enrojecer el barrido.
- K2 (ANCLA DE MALLA) UNA replica evaluada con el instrumento real
  `field_solver.medir()` sobre la malla 61^3: debe cumplir
  a_amp <= a_pico * (1 + 1e-9)  (cota exacta)  y  a_amp >= 0.90 * a_pico
  (paso de nodo 0.1 lambda = 36 grados: el antinodo puede caer entre nodos).
  Para sigma = 0 la igualdad se exige a 1e-12.

## 5. ACEPTACION Y SALIDAS
- rejilla sigma: 0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0
- M = 4096 replicas por (N, sigma); semilla = sha256 de una etiqueta fija
  (determinista y reproducible: `sfqed/barrido_sigma_phi/20261011`).
- estimador: RMS de la replica (a_med = sqrt(<a^2>)) = el objeto de la forma
  cerrada; SE por propagacion  SE(a_rms)/a_rms = 0.5 * SE(<a^2>)/<a^2>.
- criterio: |beta_MC(sigma) - beta_teo(sigma)| <= max(3 SE_beta, 1e-3) para TODA
  sigma => RC = 0. Si alguna falla => RC = 1 nombrando la sigma.
  Falta este pre-registro o falta `configs.json` => RC = 2 (SIN MEDIDA).
  K0/K1/K2 fuera de su extremo => RC = 3.
- artefactos: `sim/data/sigma_phi/` (CSV SIN fila de encabezado de datos:
  `sim/falsador.py:43-55` salta '#' y vacias, no una fila de titulos).
