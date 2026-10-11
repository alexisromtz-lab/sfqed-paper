#!/bin/sh
# =============================================================================
# sfqed-paper · tools/sello.sh · UNA linea al chat, el cuerpo al disco.
#
#   sh tools/sello.sh           corre bundle/verificar.sh y sella
#   sh tools/sello.sh --ayuda   imprime este bloque
#
# El crudo NO se pierde: baja a corridas/<T_UTC>_<MOTOR>.txt y su sha16 viaja en
# la linea. Un crudo intermedio que no se conserva no se puede volver a medir.
#
# La etiqueta MOTOR no se inventa: la declara la shell de la flake
# (MOTOR_ETIQUETA=GNU | M0 | M0-DIVERGENTE | BSD-NO-REPRODUCIBLE) o, sin flake, se
# MIDE del anfitrion. Linux SIN pin no es el motor canonico: se sella HOST-GNU
# para que el desvio quede escrito y no se lea como GNU.
#
# El vocabulario del VEREDICTO es el del verificador, no el nuestro:
#   RC=0 + "VEREDICTO: VERDE"          ->  VERDE
#   RC=0 + "VEREDICTO: VERDE PARCIAL"  ->  VERDE PARCIAL   (NO se redondea a VERDE:
#                                           lo que no se midio no se declara verde)
#   RC=1 + "VEREDICTO: FRACTURA ..."   ->  FRACTURA del objeto
#   RC=2  (nunca llega al RESUMEN)     ->  CONTRATO ROTO    (el metro no se puede leer)
# Traducir "VERDE PARCIAL" a "VERDE" seria tapar lo que no se midio.
# =============================================================================
set -u

RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
BUNDLE="$RAIZ/bundle"
CORRIDAS="$RAIZ/corridas"

if [ "${1:-}" = "--ayuda" ]; then sed -n '2,26p' "$0"; exit 0; fi

T="$(TZ=UTC date -u '+%Y%m%dT%H%M%SZ')"

if [ -n "${MOTOR_ETIQUETA:-}" ]; then
  MOTOR="$MOTOR_ETIQUETA"; FUENTE="declarada por la flake (nix develop)"
else
  case "$(uname -s)" in
    Darwin) MOTOR=M0;          FUENTE="M0 · Darwin/BSD, sello vigente · nix AUSENTE en este anfitrion";;
    Linux)  MOTOR=HOST-GNU;    FUENTE="HOST-GNU · linux sin pin: NO es el motor canonico";;
    *)      MOTOR=DESCONOCIDO; FUENTE="medida: sistema no declarado";;
  esac
fi

[ -d "$BUNDLE" ] || { printf 'CONTRATO ROTO: no hay bundle en %s\n' "$BUNDLE"; exit 2; }
mkdir -p "$CORRIDAS"
DUMP="$CORRIDAS/${T}_${MOTOR}.txt"

( cd "$BUNDLE" && sh ./verificar.sh "$@" ) > "$DUMP" 2>&1
RC=$?

# El veredicto se lee de la linea que el propio verificador imprime; el resto de
# esa linea (RC y el detalle de bloques NO MEDIDOS) NO se descarta: el detalle se
# re-cose como no_medido=N, porque es lo que distingue verde pleno de parcial.
V="$(grep -m1 '^VEREDICTO:' "$DUMP" | sed -e 's/^VEREDICTO: *//' -e 's/[[:space:]]*RC=[0-9][0-9]*.*$//' -e 's/[[:space:]]*·[[:space:]]*$//' -e 's/[[:space:]]*$//')"
if [ -z "$V" ]; then
  if [ "$RC" -eq 2 ]; then V="CONTRATO ROTO"; else V="SIN_MARCADOR"; fi
fi
NM="$(sed -n 's/.*no_medido=\([0-9][0-9]*\).*/\1/p' "$DUMP" | head -1)"
if [ -n "$NM" ]; then
  case "$V" in *PARCIAL*) V="$V · no_medido=$NM";; esac
fi
SHA="$(shasum -a 256 "$DUMP" | cut -c1-16)"

printf 'VEREDICTO: %s · RC: %s · MOTOR: %s · SHA16: %s\n' "$V" "$RC" "$MOTOR" "$SHA"
printf 'CRUDO: %s  (%s)\n' "$DUMP" "$FUENTE"
exit $RC
