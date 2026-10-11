#!/usr/bin/env bash
# 🔐 Instala los hooks de gitleaks en esta copia del repo.
# Requisito: gitleaks instalado (brew install gitleaks).
# Uso: bash scripts/util/git-hooks/install.sh
#
# Instala DOS hooks (16-Sep-2026):
#   pre-commit → escanea lo staged            (bloquea el commit)
#   pre-push   → escanea lo que se va a subir (bloquea el push)
# Son symlinks al repo: clonar + correr esto = las mismas defensas.
set -euo pipefail

# La raíz se pregunta a git, no se adivina con ../.. (ese cálculo estaba mal:
# daba «scripts/» y el instalador nunca encontraba los hooks).
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
if [ -z "$REPO_ROOT" ]; then
  cd "$(dirname "${BASH_SOURCE[0]}")/../../.." || exit 1
  REPO_ROOT="$(pwd)"
fi

echo "🔐 Hooks de seguridad — repo: $REPO_ROOT"

if ! command -v gitleaks >/dev/null 2>&1; then
  echo "⚠️  gitleaks no está en PATH. Los hooks son FAIL-CLOSED (30-Sep-2026):"
  echo "    buscan /opt/homebrew/bin · /usr/local/bin · /opt/local/bin y, si no"
  echo "    aparece en ninguna, ABORTAN el commit/push con exit 2."
  echo "    Instálalo: brew install gitleaks"
fi

# Reemplaza cualquier hook previo (guarda copia de respaldo si existe y no es el nuestro)
for HOOK in pre-commit pre-push; do
  HOOK_SRC="$REPO_ROOT/scripts/util/git-hooks/$HOOK"
  HOOK_DST="$REPO_ROOT/.git/hooks/$HOOK"

  if [ ! -f "$HOOK_SRC" ]; then
    echo "❌ No encuentro el hook fuente: $HOOK_SRC"
    exit 1
  fi

  if [ -e "$HOOK_DST" ] && [ ! -L "$HOOK_DST" ]; then
    cp "$HOOK_DST" "$HOOK_DST.bak.$(date +%Y%m%d%H%M%S)"
    echo "📦 Respaldo del hook anterior creado ($HOOK)."
  fi

  ln -sfn "../../scripts/util/git-hooks/$HOOK" "$HOOK_DST"
  chmod +x "$HOOK_SRC"
  echo "✅ Hook instalado: $HOOK_DST -> $HOOK_SRC"
done

if [ -f "$REPO_ROOT/.gitleaks.toml" ]; then
  echo "✅ Reglas de la casa: .gitleaks.toml (extiende el catálogo por defecto)"
else
  echo "⚠️  Sin .gitleaks.toml: gitleaks usará solo su catálogo por defecto"
fi

echo "   Bypass temporal (no recomendado): git commit --no-verify · git push --no-verify"
