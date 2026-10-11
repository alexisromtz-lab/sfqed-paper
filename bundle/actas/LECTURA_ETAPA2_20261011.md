# LECTURA DE LA ETAPA 2 — el funcional del paper, medido fuera del PIC

**Comando que respalda toda cifra de este archivo:**

```
cd /Users/marlene/sfqed-paper && python3 -B sim/schwinger_offline.py
```

Corrido a **2026-10-11T00:19:30Z**, RC=0, 6 s. Crudo completo: `sim/pronostico_schwinger.json`.
Hora del `main.tex` que se leyó: `sha16 = 4299786a34bdb313` (pin OK).
UNIVERSO que imprime el propio instrumento:

> `main.tex` (cuerpos leídos; sha16 impreso) + `sim/configs.json` (campo pico por N) +
> mallas y tolerancias ELEGIDAS; motor `python3` float64 sin dependencias; medida = UNA celda
> del retículo (`lambda/2` × `T/2`), la MISMA en las dos geometrías; volumen y tiempo del
> rendimiento: `V = (pi w0^2/2)(c tau)`, `T = tau` **[SUPUESTO DECLARADO]**.

Lo que se midió: `eq:yield` con `eq:schwinger_rate` y `eq:ab`, sobre las **dos
geometrías que el paper separa** — circular co-rotante (`eq:cp_inv`, quieta en `t`)
y lineal contrapropagante (`eq:lin_inv`, con cruces) — evaluadas en los campos pico
que `sim/configs.json` ya tenía declarados.

## Los seis controles (todos verdes)

| control | resultado |
|---|---|
| CP1 dos contabilidades SI (ruta A `hbar^2 c` · ruta B `eV^4 → q^4/(hbar^4 c^3)`) | `abs(dA-dB) = 0.000e+00` dex |
| CP2 Lemma 1: onda plana → `a = 0` exacto | `a = 0.0` → **NO HAY PARES** (no *0.0 pares*) |
| CP3 las dos geometrías NO son la misma: la lineal cambia con `t` | cambio medido `6.844e+14` V/m |
| CP4 cola de la serie de Schwinger despreciable | `log10` cola(`n>1`) ≤ `-5275.7` |
| CP5 escala entre rutas constante en `E` y en `E/1000` | `0.000e+00` dex en los dos campos |
| CP6 convergencia de las rejillas (`z` y `u,v`) | peor divergencia `2.274e-13` dex |

Cota del **resto de la celda** (no se supone cero, se acota): aporta a lo sumo
`10^-88.1` de la media, peor caso entre N.

## La tabla (dex de `w` en `m^-3 s^-1`)

| N | `E_pico` V/m | `x = E_cr/E_pico` | `log10 w(pico)` | `log10<w>_circ` | `log10<w>_lin` | ventaja circ | `log10 N_circ` |
|---|---|---|---|---|---|---|---|
| 1 | 6.844163e+14 | 1933.5 | −2588.49 | −2590.48 | −2592.47 | **1.99** | **−2620.80** |
| 2 | 9.679109e+14 | 1367.2 | −1815.55 | −1817.47 | −1819.38 | 1.91 | −1847.78 |
| 4 | 1.368833e+15 | 966.7 | −1268.91 | −1270.75 | −1272.59 | 1.84 | −1301.07 |
| 8 | 1.935822e+15 | 683.6 | −882.29 | −884.06 | −885.82 | 1.76 | −914.37 |
| 16 | 2.737665e+15 | 483.4 | −608.82 | −610.51 | −612.20 | **1.69** | **−640.83** |

## Lo que esto dice, y lo que no

1. **La geometría quieta gana, y gana ~2 órdenes.** `10^(1.99)` a `N=1` y
   `10^(1.69)` a `N=16`: la ventaja es real en esta contabilidad y **se encoge** al
   subir `N` (a `x` menor la cresta del pico es más ancha y la lineal pierde menos).
   Se mide; no se explica aquí.
2. **El piso de doble no es un cero físico.** `exp(-pi x) = 0.0` con `x = 1933.45`,
   y `log10 w = −2588.49` es finito: por eso la cifra se reporta en dex. Los pares en
   doble son `0.0` porque faltan **2621 órdenes**, no porque el proceso sea nulo.
3. **La palanca `1/N` es exponencial en esta contabilidad:** de `N=1` a `N=16` el
   rendimiento sube de `10^-2621` a `10^-641`, unas **1980 órdenes**. Y aun así `N=16`
   queda **641 órdenes corto de un par**, con `Sigma = 100 J` y `lambda = 0.8 µm`
   declarados en `configs.json`. Esto es un enunciado **sobre esta contabilidad
   declarada**, no sobre el experimento.
4. **Lo que falta sigue faltando.** `sim/medidas_aN.csv` está ausente (verificado a
   las 00:19:39Z): no hay corrida PIC. Este instrumento evalúa **la receta del propio
   paper** (`eq:yield` con `eq:schwinger_rate`); la discusión del régimen de validez
   LCFA vive en el paper, no aquí. El veredicto verde/rojo del `1/N` lo sigue
   entregando `sim/falsador.py` y necesita la etapa 1.

## Dos lecciones pagadas en esta corrida (van al registro, no al paper)

- **El punto de prueba también se elige.** La primera versión de CP3 muestreaba
  `z = lambda/4`: ahí `kz = pi/2` ⇒ `a = 0` en **las dos** geometrías y el control
  salió rojo sin que nada estuviera mal. Corregido muestreando cuatro puntos y
  exigiendo que la lineal cambie. La elección del punto es parte del metro.
- **Un control que se ahoga en el piso de doble no es evidencia.** La primera versión
  de CP5 comparaba `10^(dex+320)` y dividía por cero: la forma del control estaba mal,
  no la física. Rehecho como constancia de la escala entre rutas en dos campos.
- **Colisión de rótulos, declarada y no renombrada:** `configs.json` llama `a_tot_pred`
  al parámetro adimensional del haz; la `a` de `eq:ab` es un **campo** en V/m. Misma
  letra, dos objetos: el instrumento los usa rotulados y el protocolo ya commiteado no
  se edita por esto.
