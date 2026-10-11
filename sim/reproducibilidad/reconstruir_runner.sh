#!/bin/sh
# ============================================================================
# reconstruir_runner.sh — receta de reconstruccion de la compuerta de la triada
#                          FDTD (barrido sigma-phi). Aterrizaje 2026-10-11.
#
# No mide nada nuevo: reproduce un resultado YA medido y lo declara.
#   base congelada : runner_2d3v_frozen_368627d18d83d253.py  (22048 B · sha16 368627d18d83d253)
#   parche         : fases.diff                              ( 2411 B · sha16 17c54fb44b673a61)
#   resultante     : runner_2d3v_2c7450a7c67de6cb.py         (22365 B · sha16 2c7450a7c67de6cb)
#
# Comando medido (BSD patch = /usr/bin/patch, macOS), reproducido en /tmp antes de
# aterrizar esta receta:
#     patch -s -p0 -o runner_2d3v_2c7450a7c67de6cb.py \
#           runner_2d3v_frozen_368627d18d83d253.py < fases.diff
#
# NOTA DE METRO: la cabecera del parche es ASIMETRICA
#     --- runner_2d3v_frozen.py
#     +++ runner_2d3v.py
# por eso el archivo de entrada se pasa como OPERANDO explicito y NO se deduce del
# header: deducirlo obligaria a que el archivo se llamara como el header y a elegir
# la silaba (--- o +++) que gana. El operando quita la eleccion.
#
# NOTA DE NAMESPACE: este fases.diff (17c54fb44b673a61) NO es sim/salida_fases.diff
# del repositorio: mismo nombre de familia, otro objeto.
#
# CONTRATO DE RC (precede 2 > 1 > 0):
#   0 = verde   · el resultante coincide en bytes Y en sha16 con lo declarado
#   1 = fractura del OBJETO · una entrada no es la declarada, o el parche no aplica,
#                             o el resultante no coincide
#   2 = METRO roto · falta una entrada o falta patch(1); no hay nada que medir
# ============================================================================

LC_ALL=C; export LC_ALL
TZ=UTC; export TZ

HERE=$(dirname "$0")
cd "$HERE" || { echo 'RC=2 METRO ROTO: no se pudo entrar al directorio de la receta'; exit 2; }

BASE=runner_2d3v_frozen_368627d18d83d253.py
DIFF=fases.diff
OUT=runner_2d3v_2c7450a7c67de6cb.py
BASE_B=22048; BASE_S=368627d18d83d253
DIFF_B=2411;  DIFF_S=17c54fb44b673a61
EXP_B=22365;  EXP_S=2c7450a7c67de6cb

sha16() { shasum -a 256 "$1" | cut -c1-16; }
bytes() { wc -c < "$1" | tr -d ' '; }

echo "T_UTC=$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
echo "UNIVERSO DECLARADO: $(pwd) — la base congelada y el parche de la triada, con los tres sha16 declarados en la cabecera de este script."
echo "MOTOR = patch(1) BSD -p0 + shasum -a 256 + wc -c.  UNIDAD = byte / sha16.  VENTANA = reloj UTC de arriba."

for f in "$BASE" "$DIFF"; do
  if [ ! -f "$f" ]; then echo "RC=2 METRO ROTO: falta $f"; exit 2; fi
done
command -v patch >/dev/null 2>&1 || { echo 'RC=2 METRO ROTO: no hay patch(1)'; exit 2; }

bB=$(bytes "$BASE"); bS=$(sha16 "$BASE")
dB=$(bytes "$DIFF"); dS=$(sha16 "$DIFF")
echo "  base      $BASE  bytes=$bB (declarado $BASE_B)  sha16=$bS (declarado $BASE_S)"
echo "  parche    $DIFF  bytes=$dB (declarado $DIFF_B)   sha16=$dS (declarado $DIFF_S)"
if [ "$bB" != "$BASE_B" ] || [ "$bS" != "$BASE_S" ]; then echo 'RC=1 FRACTURA DEL OBJETO: la base no es la declarada'; exit 1; fi
if [ "$dB" != "$DIFF_B" ] || [ "$dS" != "$DIFF_S" ]; then echo 'RC=1 FRACTURA DEL OBJETO: el parche no es el declarado'; exit 1; fi

rm -f "$OUT"
patch -s -p0 -o "$OUT" "$BASE" < "$DIFF"
rc=$?
if [ "$rc" -ne 0 ] || [ ! -f "$OUT" ]; then echo "RC=1 FRACTURA DEL OBJETO: patch rc=$rc (el parche no aplico)"; exit 1; fi

oB=$(bytes "$OUT"); oS=$(sha16 "$OUT")
echo "  resultante $OUT  bytes=$oB (esperado $EXP_B)  sha16=$oS (esperado $EXP_S)"
if [ "$oB" != "$EXP_B" ] || [ "$oS" != "$EXP_S" ]; then echo 'RC=1 FRACTURA DEL OBJETO: el resultante no coincide con lo declarado'; exit 1; fi

echo "VEREDICTO · RC=0 · MOTOR=patch(1) BSD -p0 + shasum -a 256 · SHA16=$oS · BYTES=$oB · RECETA=sim/reproducibilidad/reconstruir_runner.sh"
exit 0
