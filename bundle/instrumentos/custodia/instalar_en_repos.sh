#!/usr/bin/env bash
# 🔐 instalar_en_repos.sh — lleva el gate de gitleaks (las piezas PROBADAS de la
# casa) a OTRO repositorio git. NO reescribe nada: copia y corre lo ya pagado.
#
# Uso:
#   bash scripts/util/git-hooks/instalar_en_repos.sh --dry /ruta/repo1 [/ruta/repo2 ...]
#   bash scripts/util/git-hooks/instalar_en_repos.sh       /ruta/repo1 [/ruta/repo2 ...]
#
# Qué hace, por destino y en este orden:
#   0. PRE-CHECK: git rev-parse --is-inside-work-tree.
#      · Si NO es repo git -> lo REPORTA en su salida y SIGUE con el siguiente
#        destino. NO aborta con error y NO crea estructuras .git ficticias.
#   1. Copia las piezas (2 hooks + install.sh + .gitleaks.toml) desde ESTE repo
#      al destino, verificando sha256 corto contra el MANIFIESTO de abajo.
#   2. Corre el install.sh PROBADO dentro del destino (no reimplementa el
#      symlink relativo ../../scripts/util/git-hooks/<hook>).
#   3. Verifica el resultado POR IDENTIDAD (cmp + sha16), no por su mensaje de
#      éxito: el éxito de un instrumento es del acto, no del objeto.
#
# Idempotente: si lo copiado ya es idéntico, no reescribe y lo declara.
# NO hace commit, NO hace push, NO usa --no-verify, NO toca repos comerciales
# salvo que se le nombre esa ruta explícitamente en la línea de comandos.
set -euo pipefail

# ── MANIFIESTO: lo que se porta, con la identidad MEDIDA en el origen ────────
# Hora de la medida: 2026-10-11T04:26:21Z.
# Si el origen cambió, el port ABORTA: no se propaga un objeto distinto al medido.
SHA16_PRE_COMMIT="b596865080c6415f"   # scripts/util/git-hooks/pre-commit
SHA16_PRE_PUSH="024903581d44d706"     # scripts/util/git-hooks/pre-push
SHA16_INSTALL="40515cea38f9808c"      # scripts/util/git-hooks/install.sh
SHA16_GITLEAKS="2e03d8999823ab6e"     # .gitleaks.toml (17 reglas de la casa)

sha16() { shasum -a 256 "$1" | cut -c1-16; }
ahora() { TZ=UTC date -u '+%Y-%m-%dT%H:%M:%SZ'; }

DRY=0
DESTINOS=()
for A in "$@"; do
  case "$A" in
    --dry|--simular) DRY=1 ;;
    -h|--help)
      sed -n '2,26p' "${BASH_SOURCE[0]}"
      exit 0 ;;
    -*) echo "⛔ opción desconocida: $A" >&2; exit 1 ;;
    *) DESTINOS+=("$A") ;;
  esac
done

if [ "${#DESTINOS[@]}" -eq 0 ]; then
  echo "⛔ Sin destinos. Este instalador NO barre nada por su cuenta: se le nombra" >&2
  echo "   cada repo. Los repositorios comerciales quedan intocables si no se nombran." >&2
  echo "   Uso: bash $0 --dry /ruta/repo1 [/ruta/repo2 ...]" >&2
  exit 1
fi

# ── ORIGEN: se deriva de la UBICACIÓN DEL PROPIO SCRIPT, jamás del cwd ──────
# Medido 2026-10-11T04:28:27Z: con el cwd dentro de OTRO repo, un
# `git rev-parse --show-toplevel` contestaba la raíz de ESE repo y el origen
# salía sin piezas (RC=1). El instrumento estaba respondiendo sobre lo que lo
# rodeaba, no sobre sí mismo. La raíz se pregunta a la ubicación del script.
SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$SCRIPTS_DIR"
ORIGEN="$(cd "$SRC/../../.." && pwd)"

# Co-locación: las piezas, el .gitleaks.toml y este script deben vivir en el
# MISMO repo. Si el árbol miente, el port ABORTA antes de copiar nada.
GIT_ROOT="$(git -C "$SRC" rev-parse --show-toplevel 2>/dev/null || true)"
if [ -n "$GIT_ROOT" ] && [ "$GIT_ROOT" != "$ORIGEN" ]; then
  echo "❌ el script vive en $ORIGEN y git dice que el repo es $GIT_ROOT: piezas descolocadas." >&2
  echo "   Port abortado sin copiar nada." >&2
  exit 1
fi

printf '🔐 gate de gitleaks — origen: %s\n' "$ORIGEN"
printf '   T_UTC=%s  modo=%s\n' "$(ahora)" "$([ "$DRY" -eq 1 ] && echo DRY || echo REAL)"

# ── GATE DEL ORIGEN (fail-closed: sin piezas medidas no hay port) ────────────
ORIGEN_OK=1
for P in pre-commit pre-push install.sh; do
  F="$SRC/$P"
  if [ ! -f "$F" ]; then echo "❌ falta pieza de origen: $F" >&2; ORIGEN_OK=0; continue; fi
  case "$P" in
    pre-commit) ESP="$SHA16_PRE_COMMIT" ;;
    pre-push)   ESP="$SHA16_PRE_PUSH" ;;
    install.sh) ESP="$SHA16_INSTALL" ;;
  esac
  OBT="$(sha16 "$F")"
  if [ "$OBT" != "$ESP" ]; then
    echo "❌ el ORIGEN cambió: $P mide $OBT y el manifiesto dice $ESP. Port abortado." >&2
    ORIGEN_OK=0
  else
    printf '   · origen %-11s sha16 %s OK\n' "$P" "$OBT"
  fi
done
if [ ! -f "$ORIGEN/.gitleaks.toml" ]; then
  echo "❌ falta pieza de origen: $ORIGEN/.gitleaks.toml" >&2; ORIGEN_OK=0
else
  OBT="$(sha16 "$ORIGEN/.gitleaks.toml")"
  if [ "$OBT" != "$SHA16_GITLEAKS" ]; then
    echo "❌ el ORIGEN cambió: .gitleaks.toml mide $OBT y el manifiesto dice $SHA16_GITLEAKS." >&2
    ORIGEN_OK=0
  else
    printf '   · origen .gitleaks.toml sha16 %s OK\n' "$OBT"
  fi
fi
[ "$ORIGEN_OK" -eq 1 ] || exit 1

# ── RESOLUCIÓN DEL BINARIO (misma política que los hooks: fail-closed) ───────
GITLEAKS_BIN=""
if command -v gitleaks >/dev/null 2>&1; then
  GITLEAKS_BIN="$(command -v gitleaks)"
else
  for C in /opt/homebrew/bin/gitleaks /usr/local/bin/gitleaks /opt/local/bin/gitleaks; do
    if [ -x "$C" ]; then GITLEAKS_BIN="$C"; break; fi
  done
fi
if [ -z "$GITLEAKS_BIN" ]; then
  echo "⚠️  gitleaks NO está en PATH ni en las rutas conocidas."
  echo "    Los hooks que se instalan son FAIL-CLOSED: ABORTARÁN el commit (exit 2)."
  echo "    Instálalo: brew install gitleaks"
else
  printf '   · escáner: %s (version %s)\n' "$GITLEAKS_BIN" "$("$GITLEAKS_BIN" version 2>/dev/null || echo '?')"
fi

STAMP="$(TZ=UTC date -u '+%Y%m%dT%H%M%SZ')"
N_INST=0; N_YA=0; N_SINREPO=0
RC=0

# ── copiar_pieza <src> <dst> <sha_esperado> <modo> ───────────────────────────
# Idempotente por identidad. Respalda lo que ya existía y NO coincidía.
copiar_pieza() {
  local SRC_F="$1" DST_F="$2" ESP="$3" MODO="$4" RUTA_REL="$5"
  if [ -f "$DST_F" ]; then
    local OBT; OBT="$(sha16 "$DST_F")"
    if [ "$OBT" = "$ESP" ]; then
      printf '     = %-26s ya idéntico (sha16 %s)\n' "$RUTA_REL" "$OBT"
      N_YA=$((N_YA + 1))
      return 0
    fi
    if [ "$DRY" -eq 1 ]; then
      printf '     ~ %-26s DIFIERE (mide %s) — en real se respaldaría y se reemplazaría\n' "$RUTA_REL" "$OBT"
      return 0
    fi
    cp -p "$DST_F" "$DST_F.bak.$STAMP"
    printf '     📦 respaldo de lo previo: %s.bak.%s\n' "$RUTA_REL" "$STAMP"
  fi
  if [ "$DRY" -eq 1 ]; then
    printf '     + %-26s se copiaría (sha16 %s)\n' "$RUTA_REL" "$ESP"
    return 0
  fi
  mkdir -p "$(dirname "$DST_F")"
  install -m "$MODO" "$SRC_F" "$DST_F"
  local POST; POST="$(sha16 "$DST_F")"
  if [ "$POST" != "$ESP" ]; then
    printf '     ❌ %s quedó con sha16 %s y el manifiesto dice %s\n' "$RUTA_REL" "$POST" "$ESP" >&2
    return 1
  fi
  printf '     + %-26s copiado (sha16 %s)\n' "$RUTA_REL" "$POST"
  N_INST=$((N_INST + 1))
  return 0
}

for T in "${DESTINOS[@]}"; do
  echo ""
  echo "── destino: $T"
  if [ ! -d "$T" ]; then
    printf '   ⛔ no existe (o no es directorio). Nada se hace.\n'
    printf '   REPORTE destino=%s es_repo=NO motivo=ruta_inexistente gate=NO\n' "$T"
    N_SINREPO=$((N_SINREPO + 1))
    continue
  fi

  # 0. PRE-CHECK — la condición del dueño: preguntar a git, no asumir.
  if ! git -C "$T" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    printf '   ⛔ NO es un repositorio git (git rev-parse --is-inside-work-tree -> no).\n'
    printf '      No se instala hook: sin .git no hay dónde anclarlo.\n'
    printf '      NO se crea ningún .git ficticio. Estado REPORTADO, no reparado.\n'
    printf '   REPORTE destino=%s es_repo=NO motivo=sin_git gate=NO accion=ninguna\n' "$T"
    N_SINREPO=$((N_SINREPO + 1))
    continue
  fi

  ROOT="$(git -C "$T" rev-parse --show-toplevel)"
  HD="$(cd "$T" && git rev-parse --git-path hooks)"
  case "$HD" in /*) : ;; *) HD="$T/$HD" ;; esac
  printf '   · es repo git. raiz=%s  hooks=%s\n' "$ROOT" "$HD"

  # 1. piezas al MISMO camino relativo que en el origen (para que el install.sh
  #    probado —y su symlink relativo— funcionen sin tocarlos).
  copiar_pieza "$SRC/pre-commit" "$ROOT/scripts/util/git-hooks/pre-commit" "$SHA16_PRE_COMMIT" 0755 "scripts/util/git-hooks/pre-commit" || RC=2
  copiar_pieza "$SRC/pre-push"   "$ROOT/scripts/util/git-hooks/pre-push"   "$SHA16_PRE_PUSH"   0755 "scripts/util/git-hooks/pre-push"   || RC=2
  copiar_pieza "$SRC/install.sh" "$ROOT/scripts/util/git-hooks/install.sh" "$SHA16_INSTALL"    0755 "scripts/util/git-hooks/install.sh" || RC=2
  copiar_pieza "$ORIGEN/.gitleaks.toml" "$ROOT/.gitleaks.toml" "$SHA16_GITLEAKS" 0644 ".gitleaks.toml" || RC=2

  # 2. enganchar los hooks.
  HOOKS_ESPERADO="$ROOT/.git/hooks"
  if [ "$HD" != "$HOOKS_ESPERADO" ]; then
    # worktree / gitdir fuera del árbol: el symlink RELATIVO del install.sh
    # apuntaría a otro sitio. Se copia REAL (misma identidad) y se declara.
    printf '     ⚠️  hooks fuera de %s: se copia REAL en vez de symlink (y se declara).\n' "$HOOKS_ESPERADO"
    for H in pre-commit pre-push; do
      if [ "$DRY" -eq 1 ]; then
        printf '     + %-26s se copiaría REAL (sin symlink)\n' ".git/hooks/$H"
      else
        install -m 0755 "$SRC/$H" "$HD/$H"
        printf '     + %-26s copia REAL (sha16 %s)\n' ".git/hooks/$H" "$(sha16 "$HD/$H")"
        N_INST=$((N_INST + 1))
      fi
    done
  elif [ "$DRY" -eq 1 ]; then
    printf '     ~ .git/hooks/{pre-commit,pre-push} se enlazarían con el install.sh probado\n'
  else
    # 3. REUSAR la pieza probada: ella crea los symlinks relativos y respalda
    #    cualquier hook previo que no sea suyo.
    ( cd "$ROOT" && bash "$ROOT/scripts/util/git-hooks/install.sh" ) || RC=2
  fi

  # 4. VERIFICACIÓN POR IDENTIDAD (no por mensaje de éxito).
  if [ "$DRY" -eq 0 ]; then
    for H in pre-commit pre-push; do
      if [ -f "$HD/$H" ] && cmp -s "$HD/$H" "$SRC/$H"; then
        local_tipo="$(stat -f '%HT' "$HD/$H" 2>/dev/null || echo '?')"
        printf '     ✅ %-16s enganchado (%s, sha16 %s)\n' "$H" "$local_tipo" "$(sha16 "$HD/$H")"
      else
        printf '     ❌ %-16s NO quedó igual al origen\n' "$H" >&2
        RC=2
      fi
    done
    if cmp -s "$ROOT/.gitleaks.toml" "$ORIGEN/.gitleaks.toml"; then
      printf '     ✅ %-16s reglas de la casa idénticas al origen\n' ".gitleaks.toml"
    else
      printf '     ❌ .gitleaks.toml del destino NO es idéntico al origen\n' >&2
      RC=2
    fi
  fi

  printf '   REPORTE destino=%s es_repo=SI raiz=%s hooks=%s gate=%s\n' \
    "$T" "$ROOT" "$HD" "$([ "$RC" -eq 0 ] && echo INSTALADO || echo INCOMPLETO)"
done

echo ""
printf 'RESUMEN copiadas=%s ya_identicas=%s destinos_sin_repo=%s rc_destino=%s\n' \
  "$N_INST" "$N_YA" "$N_SINREPO" "$RC"
echo "   NO se hizo commit, NO se hizo push, NO se usó --no-verify."
echo "   Bypass consciente, fuera del hook: git commit --no-verify"
exit "$RC"
