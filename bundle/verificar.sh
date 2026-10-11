#!/bin/sh
# ==============================================================================
# SFQED · bundle · verificación en UN comando
#
#   ./verificar.sh
#
# Hace cuatro fases y devuelve un código de salida que no admite interpretación:
#
#   [1] selftest del instrumento de telemetría  -> si el medidor está roto: RC=2 y SE PARA.
#   [2] integridad de HASHES.sha256             -> si un archivo no cuadra: fractura (RC=1).
#   [3] auditoría de custodia                   -> piezas, identidad con el anfitrión,
#                                                 hook enganchado, core.hooksPath, binario.
#   [4] anclas de 00_INDICE.md                  -> cada afirmación apunta a una línea VIVA.
#
# Precedencia: 2 (medidor roto) > 1 (objeto fracturado) > 0 (verde).
# Un medidor roto NO se sigue usando: continuar mediría con un metro que no sabemos leer.
# No hay bandera, entorno ni ruta de escape que devuelva verde.
#
# Límites declarados:
#   - HASHES.sha256 no puede declararse a sí mismo: su sha16 se imprime aquí, en corrida.
#   - verificar.sh SÍ está declarado en el manifiesto: un manifiesto que no cubre a su
#     verificador deja al verificador sin testigo.
#   - HASHES.sha256 es un artefacto EMITIDO POR MAQUINA: una entrada por linea, sin
#     comentarios, sin lineas en blanco y sin finales redundantes. [2] cuenta LINEAS
#     (wc -l) y [2b] descarta vacias: si el formato se rompe, las dos cifras dejan
#     de ser el mismo objeto. El gate que mide esa paridad es el chequeo
#     NOK + NMAL != NLINEAS de [2]; aqui solo se declara, no se repara.
#   - El bundle no es el árbol sim/ completo: es el aparato de medida.
#   - Sin repo git anfitrión, la custodia NO se declara verde: se declara NO MEDIDA,
#     y el veredicto global viaja como VERDE PARCIAL. El adjetivo solo no se emite.
#   - PISO DEL MANIFIESTO: por debajo de 25 entradas declaradas el manifiesto es
#     contrato roto (RC=2), y el caso 0 se satisface a si mismo (0 + 0 == 0): ese
#     verde es falso. El 25 es un PISO DECLARADO (elegido), no una cota derivada de
#     un conteo: la foto del defecto historico (34 archivos reales contra 25
#     declarados = 9 huerfanos viajando verdes) es el caso que lo motiva, no el
#     numero que lo mide. Ese caso de hoy NO lo atrapa el piso (25 no es < 25): lo
#     atrapa [2b], que mide COBERTURA. Piso y cobertura no son el mismo metro.
#   - El banco must-fail (tests/bench_must_fail.sh) se corre APARTE: este verificador
#     no se valida a si mismo. Aqui solo se verifica su hash, como el de cualquier pieza.
#     (el bloque [3] imprime NO MEDIDO por cada pieza que no se pudo auditar.)
#   - Las 8 piezas de evidencia de la Pestana 2 entraron al bundle por COPIA (cp), y su
#     sha256 se comprobo identico al del original en sim/: este bundle no es un puntero al
#     objeto vivo, es una copia congelada. Copiar no es citar: la copia se declara.
#   - El encabezado del contrato (MOTOR / SHA16 / T_UTC) NO se emite en los RC=2 de
#     contrato roto: alli el motor que produce el SHA16 puede faltar (caso C del banco:
#     PATH sin shasum) y un contrato que no se puede medir no se imprime.
# ==============================================================================

set -u

cd "$(dirname "$0")" || { echo "CONTRATO ROTO: no se pudo entrar al directorio del bundle"; exit 2; }

T0=$(TZ=UTC date -u '+%Y-%m-%dT%H:%M:%SZ')

# --- identidad del motor: el nucleo se MIDE en ruta absoluta, no se adivina del PATH ----
# El banco must-fail corre este script con un PATH falso que NO trae uname: si aqui se
# llamara a "uname" a secas, el banco mediria su propio PATH y no el nucleo.
MKERN=""
if [ -x /usr/bin/uname ]; then MKERN=$(/usr/bin/uname -s 2>/dev/null); fi
case "$MKERN" in
  Darwin) MOTOR_ID="M0" ;;
  Linux)  MOTOR_ID="M1" ;;
  *)      MOTOR_ID="M?" ;;
esac
if [ -n "$MKERN" ]; then
  MOTOR_DECL="$MKERN $(/usr/bin/uname -r 2>/dev/null)"
else
  MOTOR_DECL="nucleo no medido: /usr/bin/uname ausente"
fi

sha16() { shasum -a 256 "$1" | cut -c1-16; }

RC=0
VERDE=0
ROJO=0
NOMED=0
AN_TOT=0
AN_OK=0
AN_MAL=0

echo "=============================================================="
echo "SFQED · bundle · verificacion en un comando"
echo "T_UTC = $T0"
echo "UNIVERSO DECLARADO: todo archivo bajo bundle/, incluidos este verificador y HASHES.sha256"
echo "BANCO MUST-FAIL: tests/bench_must_fail.sh (7 casos). NO se invoca desde aqui:"
echo "  un verificador no se valida a si mismo; el banco lo mide desde afuera."
echo "MOTOR: shasum -a 256 | cmp | grep -F | python3 -B | git -C"
echo "MOTOR_ID: M0 = Darwin/anfitrion · M1 = GNU/Linux (nix develop .#gnu) · M? = nucleo no medido"
echo "  aqui: $MOTOR_ID ($MOTOR_DECL)"
echo "UNIDAD: archivo (inventario y cobertura) | linea (anclas) | byte (custodia)"
echo "VENTANA: el T_UTC de este encabezado. Toda cifra de conteo caduca al escribirse."
if [ -f HASHES.sha256 ]; then
  SHMAN=$(sha16 HASHES.sha256)
  echo "sha16(HASHES.sha256) = $SHMAN   <- no circular: lo imprime el verificador"
else
  SHMAN="(AUSENTE)"
  echo "sha16(HASHES.sha256) = (AUSENTE)"
fi
echo "sha16(verificar.sh)  = $(sha16 verificar.sh)"
echo "sha16(00_INDICE.md)  = $(sha16 00_INDICE.md)"
echo "=============================================================="

# ---------------------------------------------------------------- [1] MEDIDOR
echo "[1] selftest del instrumento de telemetria (must-fail controls incluidos)"
INS=instrumentos/telemetria_minima.py
if ! command -v python3 >/dev/null 2>&1; then
  echo "CONTRATO ROTO: python3 ausente: no hay medidor"; echo "RC=2"; exit 2
fi
if [ ! -f "$INS" ]; then
  echo "CONTRATO ROTO: falta $INS"; echo "RC=2"; exit 2
fi
echo "    instrumento: $INS  sha16=$(sha16 "$INS")"
SAL1=$(python3 -B "$INS" selftest 2>&1)
RC1=$?
printf '%s\n' "$SAL1" | sed 's/^/    /'
if [ "$RC1" -eq 0 ]; then
  VERDE=$((VERDE + 1))
else
  echo "CONTRATO ROTO: el selftest salio RC=$RC1 (esperado 0). Un medidor que no pasa su"
  echo "  propio control must-fail no puede usarse para medir nada. NO se sigue midiendo."
  echo "RC=2"; exit 2
fi

# ------------------------------------------------------------ [2] INTEGRIDAD
echo "[2] integridad de HASHES.sha256 (byte a byte)"
if ! command -v shasum >/dev/null 2>&1; then
  echo "CONTRATO ROTO: shasum ausente: no hay motor de hash"; echo "RC=2"; exit 2
fi
if [ ! -f HASHES.sha256 ]; then
  echo "CONTRATO ROTO: falta HASHES.sha256: sin manifiesto no hay integridad medible"; echo "RC=2"; exit 2
fi
NLINEAS=$(wc -l < HASHES.sha256 | tr -d ' ')
SAL2=$(shasum -a 256 -c HASHES.sha256 2>&1)
NOK=$(printf '%s\n' "$SAL2" | grep -c ': OK$')
NMAL=$(printf '%s\n' "$SAL2" | grep -c 'FAILED')
printf '%s\n' "$SAL2" | grep 'FAILED' | sed 's/^/    /'
echo "    entradas en el manifiesto = $NLINEAS · OK = $NOK · FAILED = $NMAL"
if [ "$NLINEAS" -lt 25 ]; then
  echo "    CONTRATO ROTO: el MANIFIESTO declara $NLINEAS entradas, por debajo del piso"
  echo "      declarado (25). Un manifiesto degenerado se satisface a si mismo si esta"
  echo "      vacio (0 + 0 == 0): ese verde seria falso. El piso es DECLARADO, no derivado;"
  echo "      la cobertura (todo lo que HAY esta declarado) la mide [2b], no este bloque."
  echo "RC=2"; exit 2
fi
if [ "$((NOK + NMAL))" -ne "$NLINEAS" ]; then
  echo "    FRACTURA: el motor no evaluo todas las lineas (evaluadas=$((NOK + NMAL)) < $NLINEAS)"
  RC=1
  ROJO=$((ROJO + 1))
elif [ "$NMAL" -gt 0 ]; then
  echo "    FRACTURA: algun archivo del bundle no es el que el manifiesto declara"
  RC=1
  ROJO=$((ROJO + 1))
else
  echo "    OK: los $NOK archivos declarados coinciden con su hash"
  VERDE=$((VERDE + 1))
fi

# ------------------------------------------------ [2b] COMPLETITUD (fail-closed)
# Orden del dueno: si hay UN archivo en el bundle que el manifiesto no declara,
# el retorno es RC=1. Las dos mitades no son el mismo metro y ninguna basta sola:
#   [2]  shasum -c  mide IDENTIDAD: lo declarado es lo que dice ser. Es CIEGO a
#        los archivos que no estan en la lista (no los ve, no los puede ver).
#   [2b] el conteo  mide COBERTURA: todo lo que hay esta declarado. Es CIEGO a
#        las sustituciones: un byte cambiado no mueve el conteo.
# Medido antes de escribir este bloque: 34 archivos reales contra 25 declarados
# => 8 huerfanos viajando verdes. [2] sin [2b] deja pasar huerfanos; [2b] sin [2]
# deja pasar un archivo declarado y sustituido. Van los dos.
# MOTOR del conteo: python3 -B (ya declarado en la linea MOTOR y garantizado por
# [1], que sale RC=2 si falta). NO find: find no esta declarado arriba, y un
# medidor que aparece sin declarar es el mismo defecto que un archivo sin declarar.
# No se excluye nada: ni .DS_Store ni __pycache__. Un archivo no declarado es un
# archivo no declarado, venga de donde venga; se borra o se declara. El dia que el
# Finder cree un .DS_Store, este gate lo dira en rojo: eso es correcto.
# Quien escriba dentro del bundle despues de esta corrida regenera HASHES.sha256,
# o el bundle queda en RC=1: el sello es del ultimo que escribe, no del primero.
SAL2B=$(python3 -B - <<'FIN_COBERTURA'
import os
raiz = "."
declaradas = set()
with open("HASHES.sha256", encoding="utf-8") as f:
    for l in f:
        l = l.strip()
        if l:
            declaradas.add(l.split(None, 1)[1].lstrip("*").strip())
reales = set()
for d, sub, ficheros in os.walk(raiz):
    for f in ficheros:
        reales.add(os.path.relpath(os.path.join(d, f), raiz))
huerfanos = sorted(reales - declaradas - {"HASHES.sha256"})
print("CONTEO reales=%d declaradas=%d huerfanos=%d" % (len(reales), len(declaradas), len(huerfanos)))
for h in huerfanos:
    print("    HUERFANO sin entrada en el manifiesto: %s" % h)
FIN_COBERTURA
)
NREAL=$(printf '%s\n' "$SAL2B" | grep -F 'CONTEO reales=' | head -1 | cut -d= -f2 | cut -d' ' -f1)
NHUER=$(printf '%s\n' "$SAL2B" | grep -F 'CONTEO reales=' | head -1 | cut -d= -f4)
case "$NREAL$NHUER" in
  ''|*[!0-9]*)
    echo "    CONTRATO ROTO: el contador de completitud no imprimio un numero usable."
    echo "      Un conteo vacio no es un conteo: no se sigue midiendo con un metro ilegible."
    echo "RC=2"; exit 2 ;;
esac
printf '%s\n' "$SAL2B" | sed 's/^/    /'
echo "    cobertura: reales=$NREAL · declarados=$NLINEAS · reales - 1 (el propio manifiesto) = $((NREAL - 1))"
if [ "$NREAL" -ne "$((NLINEAS + 1))" ]; then
  echo "    FRACTURA DE COMPLETITUD: $NHUER archivo(s) del bundle no tienen entrada en el manifiesto."
  echo "      Un archivo sin entrada viaja sin testigo: el sello declara identidad, no cobertura."
  RC=1
  ROJO=$((ROJO + 1))
else
  echo "    OK: cobertura completa ($NREAL = $NLINEAS declarados + el propio manifiesto)"
  VERDE=$((VERDE + 1))
fi

# -------------------------------------------------------------- [3] CUSTODIA
echo "[3] custodia: piezas, identidad con el anfitrion, enganche y binario"
while IFS='|' read -r rel esp; do
  [ -z "$rel" ] && continue
  if [ ! -f "$rel" ]; then
    echo "    FALTA $rel (declarado sha16=$esp)"
    RC=1; ROJO=$((ROJO + 1)); continue
  fi
  got=$(sha16 "$rel")
  if [ "$got" = "$esp" ]; then
    echo "    $rel  sha16=$got OK"
    VERDE=$((VERDE + 1))
  else
    echo "    $rel  sha16=$got != declarado $esp -> FRACTURA"
    RC=1; ROJO=$((ROJO + 1))
  fi
done <<'FIN_PIEZAS'
instrumentos/custodia/gitleaks_casa.toml|2e03d8999823ab6e
instrumentos/custodia/pre-commit|b596865080c6415f
instrumentos/custodia/pre-push|024903581d44d706
instrumentos/custodia/install.sh|40515cea38f9808c
instrumentos/custodia/instalar_en_repos.sh|edb1bd60fe3b5751
FIN_PIEZAS

if ! command -v git >/dev/null 2>&1; then
  echo "    NO MEDIDO: git ausente: no se puede auditar el repo anfitrion"
  NOMED=$((NOMED + 1))
  HOST=""
else
  HOST=$(git -C .. rev-parse --show-toplevel 2>/dev/null)
fi

if [ -z "$HOST" ]; then
  echo "    NO MEDIDO: sin repo git anfitrion (no se declara verde lo que no se midio)"
  NOMED=$((NOMED + 1))
else
  echo "    repo anfitrion: $HOST"
  while IFS='|' read -r h b; do
    [ -z "$h" ] && continue
    if [ ! -f "$HOST/$h" ]; then
      echo "    NO MEDIDO: el anfitrion no tiene $h"
      NOMED=$((NOMED + 1)); continue
    fi
    if cmp -s "$HOST/$h" "$b"; then
      echo "    identico: $h == $b"
      VERDE=$((VERDE + 1))
    else
      echo "    DIVERGE: $h != $b -> FRACTURA"
      RC=1; ROJO=$((ROJO + 1))
    fi
  done <<'FIN_IDENT'
.gitleaks.toml|instrumentos/custodia/gitleaks_casa.toml
scripts/util/git-hooks/pre-commit|instrumentos/custodia/pre-commit
scripts/util/git-hooks/pre-push|instrumentos/custodia/pre-push
FIN_IDENT

  while IFS= read -r h; do
    [ -z "$h" ] && continue
    L="$HOST/.git/hooks/$h"
    if [ -L "$L" ]; then
      tgt=$(readlink "$L")
      echo "    hook $h = enlace relativo -> $tgt"
      if cmp -s "$L" "instrumentos/custodia/$h"; then
        echo "      el contenido del enlace es la pieza del bundle -> OK"
        VERDE=$((VERDE + 1))
      else
        echo "      Diverge de instrumentos/custodia/$h -> FRACTURA"
        RC=1; ROJO=$((ROJO + 1))
      fi
    elif [ -f "$L" ]; then
      echo "    hook $h = archivo regular (no enlace): instala el instalador, no la mano"
      NOMED=$((NOMED + 1))
    else
      echo "    NO MEDIDO: el anfitrion no tiene .git/hooks/$h"
      NOMED=$((NOMED + 1))
    fi
  done <<'FIN_HOOKS'
pre-commit
pre-push
FIN_HOOKS

  HP=$(git -C "$HOST" config --get core.hooksPath 2>/dev/null)
  if [ -z "$HP" ]; then
    echo "    core.hooksPath: SIN DECLARAR (aplican los hooks de .git/hooks) OK"
    VERDE=$((VERDE + 1))
  else
    echo "    core.hooksPath = $HP : los hooks de .git/hooks NO aplican -> FRACTURA"
    RC=1; ROJO=$((ROJO + 1))
  fi

  GL=$(command -v gitleaks 2>/dev/null)
  if [ -z "$GL" ]; then
    echo "CONTRATO ROTO: binario gitleaks ausente. Un verde sobre un gate que no se puede"
    echo "  medir es exactamente el falso verde que esta pieza denuncia. No se emite juicio."
    echo "RC=2"; exit 2
  fi
  GLS=$(sha16 "$GL")
  GVER=$(gitleaks version 2>/dev/null | head -1)
  echo "    gitleaks: $GL sha16=$GLS version=$GVER"
  if [ "$GLS" = "f414bc2fb952be6c" ]; then
    echo "      mismo binario que el declarado (8.30.1) OK"
    VERDE=$((VERDE + 1))
  else
    echo "      MEDIDOR CAMBIADO: otro binario es otro metro; el verde no seria reproducible"
    RC=1; ROJO=$((ROJO + 1))
  fi
fi

# ----------------------------------------------------------------- [4] ANCLAS
echo "[4] anclas de 00_INDICE.md: cada afirmacion apunta a una linea viva y a un archivo con hash"
while IFS='|' read -r rel lin tok; do
  [ -z "$rel" ] && continue
  AN_TOT=$((AN_TOT + 1))
  if [ ! -f "$rel" ]; then
    echo "    FRACTURA: falta $rel:$lin (token: $tok)"
    AN_MAL=$((AN_MAL + 1)); RC=1; ROJO=$((ROJO + 1)); continue
  fi
  nlin=$(wc -l < "$rel" | tr -d ' ')
  if [ "$lin" -gt "$nlin" ]; then
    echo "    FRACTURA: $rel tiene $nlin lineas, no $lin"
    AN_MAL=$((AN_MAL + 1)); RC=1; ROJO=$((ROJO + 1)); continue
  fi
  if sed -n "${lin}p" "$rel" | grep -qF -- "$tok"; then
    echo "    OK $rel:$lin  [$tok]"
    AN_OK=$((AN_OK + 1)); VERDE=$((VERDE + 1))
  else
    echo "    FRACTURA: $rel:$lin ya no dice [$tok]"
    AN_MAL=$((AN_MAL + 1)); RC=1; ROJO=$((ROJO + 1))
  fi
done <<'FIN_ANCLAS'
actas/AUDITORIA_DE_LA_ORDEN_FDTD_Y_ORDEN_CORREGIDA_20261011.md|69|0.500000
actas/AUDITORIA_DE_LA_ORDEN_FDTD_Y_ORDEN_CORREGIDA_20261011.md|70|0.486414
actas/AUDITORIA_DE_LA_ORDEN_FDTD_Y_ORDEN_CORREGIDA_20261011.md|71|0.499999
actas/AUDITORIA_DE_LA_ORDEN_FDTD_Y_ORDEN_CORREGIDA_20261011.md|131|Cierre con conteo, no con lectura
actas/AUDITORIA_DE_LA_ORDEN_FDTD_Y_ORDEN_CORREGIDA_20261011.md|176|No lo es
actas/AUDITORIA_DE_LA_ORDEN_FDTD_Y_ORDEN_CORREGIDA_20261011.md|182|178.7553300762
actas/AUDITORIA_DE_LA_ORDEN_FDTD_Y_ORDEN_CORREGIDA_20261011.md|333|miente en silencio
actas/ADENDA_2_LECTURA_CONTRA_20261011.md|90|no una envolvente
actas/ADENDA_LECTURA_CONTRA_20261011.md|31|El RC = 1 es del ancla, no del objeto
actas/ETAPA1_CONTRA_REPORTE_20261011.md|114|control del sandbox
actas/ETAPA1_CONTRA_REPORTE_20261011.md|117|no es reutilizable entre
actas/ETAPA1_REPORTE_20261011.md|31|0.45
preregistros/PROTOCOLO_1overN.md|45|0.45
preregistros/PROTOCOLO_1overN.md|47|zona de muerte
preregistros/PROTOCOLO_1overN.md|50|antes
preregistros/PREREGISTRO_SIGMA_PHI_20261011.md|55|Este nulo SI puede enrojecer
preregistros/PREREGISTRO_KERR_20261011.md|12|no es un nulo: es un candado
preregistros/PREREGISTRO_KERR_20261011.md|21|piso de maquina
instrumentos/medidores/falsador.py|125|sin N=1 no se puede medir el cociente
instrumentos/medidores/maxwell2d.py|352|I_SL + 40
instrumentos/telemetria_minima.py|341|archivo vacio NO es verde
verificar.sh|139|CONTRATO ROTO: el MANIFIESTO declara
tests/bench_must_fail.sh|112|B - 2 "MANIFIESTO"
tests/bench_must_fail.sh|118|shasum ausente
tests/bench_must_fail.sh|148|F - 0 "PARCIAL"
tests/bench_must_fail.sh|155|gitleaks ausente
evidencia/medidas_aN_circular_corregida_20261011.csv|3|f280fb6744917e9a
evidencia/medidas_aN_circular_corregida_20261011.csv|78|178.7588150970
evidencia/control_pareado_convergente.json|2|2026-10-11T05:48:12Z
instrumentos/medidores/fuego_pestana2_20261011.py|123|RE_N = re.compile
instrumentos/medidores/fuego_pestana2_20261011.py|5|f280fb6744917e9a
instrumentos/medidores/control_pareado_convergente.py|99|rama 2 (~0.74)
instrumentos/medidores/control_pareado_convergente.py|555|intacto: %s
instrumentos/medidores/lector_invariantes.py|42|0.078459
actas/ACTA_DEL_PARCHE_SALIDA_FASES_20261011.md|48|RC_PARCHE=2
actas/ACTA_DEL_DISPARO_PESTANA2_CIRCULAR_CORREGIDA_20261011.md|143|c9aaa89b7d56ead7
actas/VEREDICTO_CONTROL_PAREADO_20261011.md|19|rama 2
actas/VEREDICTO_CONTROL_PAREADO_20261011.md|68|28.2505
FIN_ANCLAS

# --------------------------------------------------------------- [5] RESUMEN
T1=$(TZ=UTC date -u '+%Y-%m-%dT%H:%M:%SZ')
echo "=============================================================="
echo "RESUMEN  verde=$VERDE · rojo=$ROJO · no_medido=$NOMED · anclas=$AN_TOT ok=$AN_OK rojo=$AN_MAL"
echo "T_UTC inicio=$T0 fin=$T1"
if [ "$RC" -eq 0 ] && [ "$NOMED" -eq 0 ]; then
  echo "VEREDICTO: VERDE · RC: 0 · MOTOR: $MOTOR_ID · SHA16: $SHMAN · T_UTC: $T1"
elif [ "$RC" -eq 0 ]; then
  echo "VEREDICTO: VERDE PARCIAL · RC: 0 · MOTOR: $MOTOR_ID · SHA16: $SHMAN · T_UTC: $T1 · $NOMED bloque(s) NO MEDIDO(s):" 
  echo "  lo que no se midio no se declara verde. Verde de lo medido, y se dice cual."
else
  echo "VEREDICTO: FRACTURA del objeto · RC: $RC · MOTOR: $MOTOR_ID · SHA16: $SHMAN · T_UTC: $T1"
fi
exit $RC
