#!/bin/sh
# ==============================================================================
# SFQED · bundle · banco must-fail del verificador
#
#   ./tests/bench_must_fail.sh
#
# No comprueba que el bundle este bien. Comprueba que ./verificar.sh SEPA decir
# que esta mal. Cada caso introduce UNA sola fractura conocida en una copia
# efimera del bundle y exige un codigo de salida ESTRICTO, mas la causa impresa
# en el crudo: un caso que devuelve el codigo esperado por otro motivo no
# discrimina, y entonces el banco no mide lo que dice medir.
#
#   A · byte invertido, mismo tamano, en pieza rastreada .... esperado RC=1
#   B · HASHES.sha256 de 0 bytes ............................ esperado RC=2
#   C · PATH sin shasum (todo lo demas presente) ............ esperado RC=2
#   D · medidor ausente ..................................... esperado RC=2
#   E · ancla caducada, manifiesto regenerado ............... esperado RC=1
#   F · sin repo git anfitrion .............................. esperado RC=0 declarado parcial
#   G · sin gitleaks en el PATH, con anfitrion git .......... esperado RC=2
#
# Aislamiento de causa, que es lo que hace util al banco:
#   A cambia bytes y NO regenera el manifiesto -> el unico defecto es el hash.
#   E cambia una linea anclada y SI regenera el manifiesto -> el unico defecto es
#     el ancla; sin esa regeneracion el caso pasaria por el manifiesto y no
#     probaria nada sobre la fase [4].
#   C y G quitan UNA herramienta y dejan las demas.
# La pieza de A y el ancla de E se leen del bundle en tiempo de corrida: el banco
# no lleva rutas escritas a mano que puedan caducar en silencio.
#
# UNIVERSO DECLARADO: 7 casos, cada uno sobre una copia efimera del bundle
#   completo en /tmp. Ninguna corrida escribe dentro del bundle original.
# MOTOR: /bin/sh + shasum + python3 -B + cp/rm/ln. UNIDAD: codigo de salida (RC)
#   y la causa impresa en el crudo de cada caso.
# VENTANA: el T_UTC impreso abajo. Toda cifra de conteo caduca al escribirse.
# ==============================================================================

set -u

BUNDLE_ROOT=$(cd "$(dirname "$0")/.." && pwd)
T0=$(TZ=UTC date -u '+%Y-%m-%dT%H:%M:%SZ')

CASOS=0
BIEN=0
MAL=0
FALLIDOS=""
SANDBOXES_VIVOS=""

sha16() { shasum -a 256 "$1" | cut -c1-16; }

echo "=============================================================="
echo "SFQED · bundle · banco must-fail del verificador"
echo "T_UTC = $T0"
echo "bundle = $BUNDLE_ROOT"
echo "UNIVERSO DECLARADO: 7 casos, cada uno sobre una copia efimera del bundle completo"
echo "MOTOR: /bin/sh + shasum + python3 -B · UNIDAD: RC + causa impresa · VENTANA: el T_UTC de arriba"
echo "sha16(verificar.sh)   = $(sha16 "$BUNDLE_ROOT/verificar.sh")"
echo "sha16(HASHES.sha256)  = $(sha16 "$BUNDLE_ROOT/HASHES.sha256")"
echo "=============================================================="

# --- utilidades ---------------------------------------------------------------

shim() {   # $1 = destino · $2 = herramienta que se deja FUERA
  mkdir -p "$1"
  for t in date cut grep sed wc tr cmp head readlink dirname basename git python3 awk sort uniq shasum gitleaks; do
    [ "$t" = "$2" ] && continue
    p=$(command -v "$t" 2>/dev/null) || continue
    [ -n "$p" ] && ln -sf "$p" "$1/$t"
  done
  return 0
}

sandbox() {   # imprime la ruta de un sandbox con el bundle copiado dentro
  d=$(mktemp -d "/tmp/bench_bundle_XXXXXX")
  cp -R "$BUNDLE_ROOT" "$d/bundle"
  printf '%s\n' "$d"
}

arbitra() {   # $1 sandbox · $2 etiqueta · $3 PATH o '-' · $4 RC esperado · $5 causa esperada
  sb=$1; etq=$2; ruta=$3; rc_esp=$4; causa=$5
  sal="$sb/crudo.txt"
  if [ "$ruta" = "-" ]; then
    ( cd "$sb/bundle" && /bin/sh ./verificar.sh ) > "$sal" 2>&1
  else
    ( cd "$sb/bundle" && PATH="$ruta" /bin/sh ./verificar.sh ) > "$sal" 2>&1
  fi
  rc=$?
  CASOS=$((CASOS + 1))
  if [ "$rc" -eq "$rc_esp" ] && grep -qF -- "$causa" "$sal"; then
    printf '  %-3s RC=%-2s esperado=%-2s causa [%s] -> OK\n' "$etq" "$rc" "$rc_esp" "$causa"
    BIEN=$((BIEN + 1))
    rm -rf "$sb"
  else
    printf '  %-3s RC=%-2s esperado=%-2s causa [%s] -> ROJO\n' "$etq" "$rc" "$rc_esp" "$causa"
    grep -nE 'VEREDICTO|FRACTURA|CONTRATO ROTO|RESUMEN' "$sal" | sed 's/^/        /'
    MAL=$((MAL + 1))
    FALLIDOS="$FALLIDOS $etq"
    SANDBOXES_VIVOS="$SANDBOXES_VIVOS $sb"
  fi
}

# --- A · byte invertido, mismo tamano ----------------------------------------
SB=$(sandbox)
PA=$(awk 'NR==1{print $2}' "$SB/bundle/HASHES.sha256")
python3 -B -c "import pathlib,sys;p=pathlib.Path(sys.argv[1]);b=bytearray(p.read_bytes());n=len(b);b[10]=b[10]^1;p.write_bytes(bytes(b));print('    pieza = '+sys.argv[1]+' con un byte invertido en la posicion 10, tamano conservado = '+str(n))" "$SB/bundle/$PA"
printf '  A   pieza elegida del manifiesto: %s\n' "$PA"
arbitra "$SB" A - 1 "FAILED"

# --- B · manifiesto de 0 bytes ------------------------------------------------
SB=$(sandbox)
: > "$SB/bundle/HASHES.sha256"
printf '  B   entradas del manifiesto en el sandbox = %s bytes\n' "$(wc -c < "$SB/bundle/HASHES.sha256" | tr -d ' ')"
arbitra "$SB" B - 2 "MANIFIESTO"

# --- C · PATH sin shasum ------------------------------------------------------
SB=$(sandbox)
shim "$SB/bin" shasum
printf '  C   shim con %s herramientas y SIN shasum\n' "$(ls "$SB/bin" | wc -l | tr -d ' ')"
arbitra "$SB" C "$SB/bin" 2 "shasum ausente"

# --- D · medidor ausente ------------------------------------------------------
SB=$(sandbox)
INS=$(grep -E '^INS=' "$SB/bundle/verificar.sh" | head -1 | cut -d= -f2)
rm -f "$SB/bundle/$INS"
printf '  D   medidor retirado = %s\n' "$INS"
arbitra "$SB" D - 2 "falta $INS"

# --- E · ancla caducada, con el manifiesto regenerado -------------------------
SB=$(sandbox)
INFO=$(python3 -B -c "import pathlib,sys
v=pathlib.Path(sys.argv[1]); base=pathlib.Path(sys.argv[2])
t=v.read_text(encoding='utf-8').split(chr(10))
i=t.index(next(x for x in t if x.startswith('done <<') and 'ANCLAS' in x))
j=t.index('FIN_ANCLAS',i)
filas=[x for x in t[i+1:j] if x.strip()]
rel,lin,tok=filas[0].split('|')
p=base/rel; L=p.read_text(encoding='utf-8').split(chr(10))
L[int(lin)-1]='linea retirada por el banco: el ancla perdio su token'
p.write_text(chr(10).join(L),encoding='utf-8')
print(rel+' :'+lin+' ['+tok+'] | filas de la tabla = '+str(len(filas)))" "$SB/bundle/verificar.sh" "$SB/bundle")
printf '  E   ancla elegida del propio verificador: %s\n' "$INFO"
( cd "$SB/bundle" && shasum -a 256 $(awk '{print $2}' HASHES.sha256) > HASHES.sha256 )
printf '      manifiesto regenerado para que el unico defecto sea el ancla\n'
arbitra "$SB" E - 1 "ya no dice"

# --- F · sin repo git anfitrion -----------------------------------------------
SB=$(sandbox)
printf '  F   el sandbox no es un repo git: el verificador no puede auditar custodia\n'
arbitra "$SB" F - 0 "PARCIAL"

# --- G · sin gitleaks en el PATH, con anfitrion git ---------------------------
SB=$(sandbox)
shim "$SB/bin" gitleaks
git init -q "$SB"
printf '  G   shim con %s herramientas y SIN gitleaks, anfitrion git presente\n' "$(ls "$SB/bin" | wc -l | tr -d ' ')"
arbitra "$SB" G "$SB/bin" 2 "gitleaks ausente"

# --- veredicto ----------------------------------------------------------------
echo "=============================================================="
echo "RESUMEN BANCO  casos=$CASOS · conformes=$BIEN · rojos=$MAL"
if [ "$MAL" -eq 0 ]; then
  echo "VEREDICTO BANCO: VERDE ($BIEN/$CASOS) · los $CASOS codigos de salida son los estrictos"
  exit 0
fi
echo "VEREDICTO BANCO: ROJO ($BIEN/$CASOS) · casos rojos:$FALLIDOS"
echo "sandboxes conservados para inspeccion:$SANDBOXES_VIVOS"
exit 1
