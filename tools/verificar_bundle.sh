#!/bin/sh
# ============================================================================
# tools/verificar_bundle.sh  ·  AUDITOR EXTERNO del especimen  bundle/  (v2)
#
# QUE ES
#   Un verificador que NO vive dentro del objeto que mide. Nace de una orden
#   del dueno (11-Oct-2026): auditar bundle/ desde FUERA, con el piso
#   contractual calculado EN CORRIDA, sin compartir sellos con el verificado.
#
# POR QUE FUERA (el motivo, no el capricho)
#   bundle/verificar.sh esta declarado en bundle/HASHES.sha256: es una de las
#   hojas del especimen bajo custodia. Mutarlo por una discrepancia de
#   redaccion en su cabecera o por una omision de su logica interna reabriria
#   una cadena criptografica ya cerrada. El defecto de un objeto congelado se
#   DECLARA como divergencia; se repara en una VERSION NUEVA, fuera del objeto.
#
# CONTRATO DE RC (declarado ANTES de medir; precedencia 2 > 1 > 0)
#   RC=0  VERDE     piso alcanzado Y manifiesto integro Y particion cuadra
#   RC=1  FRACTURA  del OBJETO: hash que no cuadra · hoja sin entrada (salvo
#                   la excepcion declarada) · entrada sin hoja en el disco
#   RC=2  CONTRATO  del METRO: piso no alcanzado · manifiesto ausente o
#         ROTO      ilegible · motor ausente · arbol declarado inexistente ·
#                   linea de manifiesto que este metro no puede partir ·
#                   crudo o script DENTRO del universo medido
#
# LIMITES DECLARADOS
#   - NO certifica la CORRECCION del objeto: certifica integridad, piso y
#     particion. Que su contenido sea el correcto es otro metro.
#   - NO se valida a si mismo: su banco must-fail se corre APARTE
#     (--piso imposible · --crudo dentro del objeto · --bundle inexistente ·
#     copia alterada fuera del objeto).
#   - Su propia identidad NO se imprime aqui: una pieza que imprime su propio
#     sha16 describe su version ANTERIOR (familia x == x). Se mide desde fuera.
#   - El 25 es un PISO DECLARADO (elegido), no una cota derivada de un conteo.
#   - La excepcion de particion (una hoja sin entrada) NO se asume: se mide, y
#     debe ser exactamente el propio manifiesto. Si es otra cosa, es fractura.
#   - El conteo de entradas es de awk (NR): no pierde la ultima linea si al
#     manifiesto le falta el \n final. wc -l se imprime AL LADO como control.
#   - ORDEN DE LOS GUARDS: la co-locacion se verifica ANTES de crear el crudo.
#     Un guard que crea el archivo dentro del objeto antes de dispararse no
#     protege: ensucia.
# ============================================================================
set -u

VERSION='v2'
PISO=25
BUNDLE=''
CRUDO=''
QUIET=0

uso() {
  echo "uso: verificar_bundle.sh [--bundle DIR] [--piso N] [--crudo PATH] [--quiet]"
  echo "  --bundle  arbol a auditar (por defecto: <dir del script>/../bundle)"
  echo "  --piso    piso contractual de entradas (por defecto: 25)"
  echo "  --crudo   ruta del crudo de telemetria (por defecto: TMPDIR)"
  echo "  --quiet   no imprime en stdout; el crudo se escribe igual"
}

while [ $# -gt 0 ]; do
  case "$1" in
    --bundle) [ $# -ge 2 ] || { echo "CONTRATO ROTO: --bundle sin valor"; exit 2; }; BUNDLE=$2; shift 2 ;;
    --piso)   [ $# -ge 2 ] || { echo "CONTRATO ROTO: --piso sin valor"; exit 2; };   PISO=$2;   shift 2 ;;
    --crudo)  [ $# -ge 2 ] || { echo "CONTRATO ROTO: --crudo sin valor"; exit 2; };  CRUDO=$2;  shift 2 ;;
    --quiet)  QUIET=1; shift ;;
    -h|--help) uso; exit 0 ;;
    *) echo "CONTRATO ROTO: opcion desconocida: $1"; uso; exit 2 ;;
  esac
done

case "$PISO" in
  ''|*[!0-9]*) echo "CONTRATO ROTO: --piso no es un entero no negativo: $PISO"; exit 2 ;;
esac

# ---------------------------------------------------------------- [0] METRO
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd -P) || { echo "CONTRATO ROTO: no se pudo resolver el dir del script"; exit 2; }
[ -n "$BUNDLE" ] || BUNDLE="${SCRIPT_DIR}/../bundle"

T0=$(TZ=UTC date -u '+%Y-%m-%dT%H:%M:%SZ')
case "$(/usr/bin/uname -s 2>/dev/null || echo '?')" in
  Darwin) MOTOR_ID='M0' ;;
  Linux)  MOTOR_ID='M1' ;;
  *)      MOTOR_ID='M?' ;;
esac
KERNEL=$(/usr/bin/uname -srm 2>/dev/null || echo 'no medido')

if [ -z "$CRUDO" ]; then
  CRUDO="${TMPDIR:-/tmp}/verificar_bundle_$(TZ=UTC date -u '+%Y%m%dT%H%M%SZ')_$$.txt"
fi

FALTA=''
for m in shasum find awk sort comm uniq wc tr sed grep; do
  command -v "$m" >/dev/null 2>&1 || FALTA="$FALTA $m"
done
if [ -n "$FALTA" ]; then
  echo "CONTRATO ROTO: motor ausente:$FALTA — sin el no hay medicion posible"
  echo "RC=2"; exit 2
fi

if [ ! -d "$BUNDLE" ]; then
  echo "CONTRATO ROTO: el arbol declarado no existe o no es un directorio: $BUNDLE"
  echo "RC=2"; exit 2
fi
BUNDLE_ABS=$(cd "$BUNDLE" && pwd -P) || { echo "CONTRATO ROTO: no se pudo resolver $BUNDLE"; echo "RC=2"; exit 2; }
CRUDO_DIR=$(cd "$(dirname "$CRUDO")" 2>/dev/null && pwd -P) || { echo "CONTRATO ROTO: no se pudo resolver el dir del crudo: $CRUDO"; echo "RC=2"; exit 2; }
CRUDO_ABS="${CRUDO_DIR}/${CRUDO##*/}"

case "$SCRIPT_DIR/" in
  "$BUNDLE_ABS"/*) echo "CONTRATO ROTO: el auditor vive DENTRO del universo que mide: $SCRIPT_DIR"; echo "RC=2"; exit 2 ;;
esac
case "$CRUDO_ABS" in
  "$BUNDLE_ABS"/*) echo "CONTRATO ROTO: el crudo caeria DENTRO del objeto (no se creo nada): $CRUDO_ABS"; echo "RC=2"; exit 2 ;;
esac

if ! : > "$CRUDO" 2>/dev/null; then
  echo "CONTRATO ROTO: el crudo no se puede escribir en: $CRUDO"
  echo "RC=2"; exit 2
fi

say() { [ "$QUIET" -eq 1 ] || printf '%s\n' "$1"; printf '%s\n' "$1" >> "$CRUDO"; }

say "AUDITOR EXTERNO DEL ESPECIMEN bundle/ · $VERSION"
say "T_UTC = $T0"
say "MOTOR: $MOTOR_ID · $KERNEL · POSIX sh"
say "MOTOR DE HASH: shasum -a 256 (BSD/perl)"
say "UNIVERSO DECLARADO: todo archivo regular bajo $BUNDLE, incluidos el verificador del objeto y su manifiesto"
say "UNIDAD: entrada de manifiesto = linea · integridad = byte · particion = ruta relativa"
say "VENTANA: reloj UTC de arriba. LECTURA SOLO: este script no escribe dentro del objeto."
say "PISO CONTRACTUAL DECLARADO: $PISO entradas"
say "CONTRATO DE RC: 0 verde · 1 fractura del objeto · 2 contrato roto del metro (precedencia 2 > 1 > 0)"
say ""
say "[0] preflight OK: shasum find awk sort comm uniq wc tr sed grep presentes"
say "    OBJETO  = $BUNDLE_ABS"
say "    AUDITOR = $SCRIPT_DIR (fuera del objeto, verificado)"
say "    CRUDO   = $CRUDO (fuera del objeto, verificado)"
say ""

# ---------------------------------------------------------------- [1] PISO
say "[1] piso contractual del manifiesto"
MAN="$BUNDLE_ABS/HASHES.sha256"
if [ ! -f "$MAN" ]; then
  say "CONTRATO ROTO: falta HASHES.sha256: sin manifiesto no hay integridad ni piso medibles"
  say "RC=2"; exit 2
fi
if [ ! -r "$MAN" ]; then
  say "CONTRATO ROTO: HASHES.sha256 no es legible"
  say "RC=2"; exit 2
fi

N_LINEAS=$(awk 'NF && $0 !~ /^[[:space:]]*$/ {n++} END{print n+0}' "$MAN")
N_LINEAS_WC=$(wc -l < "$MAN" | tr -d ' ')
N_MALFORMADAS=$(awk 'NF!=2 {b++} END{print b+0}' "$MAN")
case "$N_LINEAS$N_LINEAS_WC$N_MALFORMADAS" in
  ''|*[!0-9]*) say "CONTRATO ROTO: el contador no imprimio un numero usable"; say "RC=2"; exit 2 ;;
esac
say "    entradas (awk NR, no vacias) = $N_LINEAS"
say "    entradas (wc -l, control)    = $N_LINEAS_WC"
if [ "$N_LINEAS_WC" != "$N_LINEAS" ]; then
  say "    DIVERGENCIA DECLARADA (no adjudicada): awk y wc no coinciden; al manifiesto le falta el \\n final"
fi
say "    lineas que este metro NO puede partir (NF != 2) = $N_MALFORMADAS"

if [ "$N_MALFORMADAS" -gt 0 ]; then
  say "CONTRATO ROTO: hay lineas de manifiesto con NF != 2 (rutas con espacios): este metro no puede medir ese objeto"
  say "RC=2"; exit 2
fi
if [ "$N_LINEAS" -eq 0 ]; then
  say "CONTRATO ROTO: manifiesto VACIO. Un conteo vacio satisface su propia identidad (0 + 0 == 0): ese verde seria falso."
  say "RC=2"; exit 2
fi
if [ "$PISO" -ge 1 ] && [ "$N_LINEAS" -lt "$PISO" ]; then
  say "CONTRATO ROTO: el MANIFIESTO declara $N_LINEAS entradas, por debajo del piso declarado ($PISO)."
  say "      El piso es DECLARADO (elegido), no derivado de un conteo; no se baja el piso: se declara el defecto."
  say "RC=2"; exit 2
fi
[ "$PISO" -ge 1 ] || say "      AVISO: el llamador desactivo el piso (--piso $PISO); queda en pie el guard de manifiesto vacio."
say "    piso: $N_LINEAS >= $PISO  OK"
say ""

# ----------------------------------------------------------- [2] INTEGRIDAD
say "[2] integridad del manifiesto (byte a byte, dentro del objeto)"
SAL2=$(cd "$BUNDLE_ABS" && shasum -a 256 -c HASHES.sha256 2>&1)
RC2=$?
N_OK=$(printf '%s\n' "$SAL2" | grep -c ': OK$')
N_MAL=$(printf '%s\n' "$SAL2" | grep -c 'FAILED')
say "$(printf '%s\n' "$SAL2" | sed 's/^/    /')"
say "    manifiesto = $N_LINEAS · OK = $N_OK · FAILED = $N_MAL · rc(shasum) = $RC2"
if [ "$((N_OK + N_MAL))" -ne "$N_LINEAS" ]; then
  say "    FRACTURA: el motor no evaluo todas las lineas (evaluadas=$((N_OK + N_MAL)) != $N_LINEAS)"
fi
say ""

# ------------------------------------------------------------ [3] PARTICION
say "[3] particion arbol <-> manifiesto (calculada aqui, no copiada del objeto)"
F_DISCO="${TMPDIR:-/tmp}/vb_$$_disco.txt"
F_DECL="${TMPDIR:-/tmp}/vb_$$_decl.txt"
trap 'rm -f "$F_DISCO" "$F_DECL" 2>/dev/null' 0 2 15

( cd "$BUNDLE_ABS" && find . -type f ) | sed 's|^\./||' | LC_ALL=C sort > "$F_DISCO"
awk '{p=$2; sub(/^\*/,"",p); sub(/^\.\//,"",p); print p}' "$MAN" | LC_ALL=C sort > "$F_DECL"

N_HOJAS=$(wc -l < "$F_DISCO" | tr -d ' ')
N_DECL_PATHS=$(wc -l < "$F_DECL" | tr -d ' ')
N_DECL_DUP=$(uniq -d "$F_DECL" | wc -l | tr -d ' ')
N_SIN_ENTRADA=$(comm -23 "$F_DISCO" "$F_DECL" | wc -l | tr -d ' ')
N_ENT_SIN_HOJA=$(comm -13 "$F_DISCO" "$F_DECL" | wc -l | tr -d ' ')
LISTA_SIN_ENTRADA=$(comm -23 "$F_DISCO" "$F_DECL" | tr '\n' ' ')
LISTA_ENT_SIN_HOJA=$(comm -13 "$F_DISCO" "$F_DECL" | tr '\n' ' ')

say "    hojas en disco               = $N_HOJAS"
say "    rutas declaradas             = $N_DECL_PATHS (duplicadas: $N_DECL_DUP)"
say "    hojas SIN entrada            = $N_SIN_ENTRADA : [$LISTA_SIN_ENTRADA]"
say "    entradas SIN hoja en disco   = $N_ENT_SIN_HOJA : [$LISTA_ENT_SIN_HOJA]"
say "    excepcion declarada: el manifiesto no puede declararse a si mismo"
say "    (esperado: 1 hoja sin entrada, y su nombre HASHES.sha256)"
say ""

# ----------------------------------------------------------- [4] VEREDICTO
RC=0
CAUSA=''
if [ "$N_MAL" -gt 0 ]; then
  RC=1; CAUSA="hash que no cuadra: $N_MAL archivo(s) FAILED"
elif [ "$((N_OK + N_MAL))" -ne "$N_LINEAS" ]; then
  RC=1; CAUSA="el motor no evaluo todas las lineas del manifiesto"
elif [ "$N_DECL_DUP" -gt 0 ]; then
  RC=1; CAUSA="rutas declaradas duplicadas: $N_DECL_DUP"
elif [ "$N_ENT_SIN_HOJA" -gt 0 ]; then
  RC=1; CAUSA="entrada declarada sin hoja en el disco: [$LISTA_ENT_SIN_HOJA]"
elif [ "$N_SIN_ENTRADA" -ne 1 ] || [ "$LISTA_SIN_ENTRADA" != 'HASHES.sha256 ' ]; then
  RC=1; CAUSA="la excepcion de particion no es la declarada: hojas sin entrada = [$LISTA_SIN_ENTRADA]"
elif [ "$N_HOJAS" -ne "$((N_LINEAS + 1))" ]; then
  RC=1; CAUSA="la aritmetica de la particion no cierra: hojas=$N_HOJAS != entradas+manifiesto=$((N_LINEAS + 1))"
fi

SHA16_MAN=$(shasum -a 256 "$MAN" | cut -c1-16)

say "[4] telemetria"
say "    PISO=$PISO · N_LINEAS=$N_LINEAS · N_HOJAS=$N_HOJAS · N_OK=$N_OK · N_MAL=$N_MAL"
say "    SIN_ENTRADA=$N_SIN_ENTRADA · ENT_SIN_HOJA=$N_ENT_SIN_HOJA · DUP=$N_DECL_DUP · MALFORMADAS=$N_MALFORMADAS"
say "    SHA16_MANIFIESTO=$SHA16_MAN"
[ -z "$CAUSA" ] || say "    CAUSA: $CAUSA"
say ""

case "$RC" in
  0) V='VERDE' ;;
  1) V='FRACTURA DEL OBJETO' ;;
  *) V='CONTRATO ROTO' ;;
esac

say "VEREDICTO: $V · RC: $RC · MOTOR: tools/verificar_bundle.sh $VERSION · SHA16_MANIFIESTO: $SHA16_MAN · CRUDO: $CRUDO"
say "RC=$RC"
exit "$RC"
