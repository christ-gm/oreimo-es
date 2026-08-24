#!/usr/bin/env bash
# build_iso.sh — crea tu ISO de Oreimo Portable en español.
#
# Uso:
#   ./build_iso.sh <juego.iso> [--out <salida.iso>]
#
# Requisitos:
#   - Tu ISO (copia legal) con el parche EN v1 de dizzyziddy aplicado.
#   - .NET SDK (10 o superior), git y mkisofs (cdrtools) en tu PATH.
#
# Acepta el disco 1 (NPJH-50568) o el disco 2 (NPJH-50569); el disco
# se detecta automáticamente tras extraer y se aplica su traducción.
#
# El script clona la toolchain base de zapan/FastAsyncOreimoTranslateTool
# (su código NO se redistribuye aquí), compila nuestro driver y ejecuta
# todo el pipeline: extraer -> aplicar traducción -> reempaquetar.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLCHAIN="${TOOLCHAIN_DIR:-$REPO/toolchain}"
WORK="${WORK_DIR:-$REPO/work}"


ISO_IN=""
ISO_OUT=""
while [ $# -gt 0 ]; do
    case "$1" in
        --out)
            [ $# -ge 2 ] || { echo "Falta el valor de --out" >&2; exit 1; }
            ISO_OUT="$2"; shift 2 ;;
        *)
            if [ -z "$ISO_IN" ]; then ISO_IN="$1"; else
                echo "Argumento inesperado: $1" >&2; exit 1
            fi
            shift ;;
    esac
done

if [ -z "$ISO_IN" ]; then
    echo "Uso: ./build_iso.sh <juego.iso> [--out <salida.iso>]" >&2
    exit 1
fi

ISO_IN="$(realpath "$ISO_IN")"
if [ ! -f "$ISO_IN" ]; then
    echo "No se encontró el archivo: $ISO_IN" >&2
    exit 1
fi
ISO_OUT="${ISO_OUT:-${ISO_IN%.iso}_ES.iso}"
ISO_OUT="$(realpath "$ISO_OUT")"

if ! command -v dotnet >/dev/null 2>&1; then
    echo "No se encontró dotnet. Instala el .NET SDK (10 o superior)." >&2
    exit 1
fi
if ! command -v mkisofs >/dev/null 2>&1; then
    if [ -x "$REPO/tool-bin/mkisofs" ] && grep -qi microsoft /proc/version 2>/dev/null; then
        export PATH="$REPO/tool-bin:$PATH"
    else
        echo "No se encontró mkisofs. Debian/Ubuntu: sudo apt install genisoimage | Arch: sudo pacman -S cdrtools" >&2
        exit 1
    fi
fi

echo "==> [0/5] Preparando toolchain base (zapan/FastAsyncOreimoTranslateTool)..."
if [ ! -d "$TOOLCHAIN/.git" ]; then
    git clone --depth 1 https://github.com/zapan/FastAsyncOreimoTranslateTool.git "$TOOLCHAIN"
fi
rm -rf "$TOOLCHAIN/OreimoAutomation"
cp -r "$REPO/tool/OreimoAutomation" "$TOOLCHAIN/OreimoAutomation"

# Aplica un pequeño parche propio para soportar sistemas de archivos con
# mayúsculas/minúsculas sensibles (ext4/Linux), donde el repack fallaría.
if git -C "$TOOLCHAIN" apply --check "$REPO/toolchain-patches/repack-case.patch" >/dev/null 2>&1; then
    git -C "$TOOLCHAIN" apply "$REPO/toolchain-patches/repack-case.patch"
fi

echo "==> Compilando driver OreimoAutomation..."
dotnet build "$TOOLCHAIN/OreimoAutomation" -c Release -v q

DLL="$TOOLCHAIN/OreimoAutomation/bin/Release/net10.0/OreimoAutomation.dll"
mkdir -p "$WORK"

echo "==> [1/5] Extrayendo ISO..."
STAGE="$WORK/_incoming"
rm -rf "$STAGE"
dotnet "$DLL" extract-iso "$ISO_IN" --base "$STAGE"

# Detectar disco por serial (UMD_DATA.BIN)
DISC=disc1
if grep -q "NPJH-50569" "$STAGE/Data/Iso/UMD_DATA.BIN" 2>/dev/null; then
    DISC=disc2
fi
echo "==> Disco detectado: $DISC"
BUILD="$WORK/$DISC"
rm -rf "$BUILD"
mv "$STAGE" "$BUILD"

echo "==> [2/5] Extrayendo datos del juego..."
dotnet "$DLL" extract-game --base "$BUILD"

echo "==> [3/5] Aplicando traducción al español..."
TRAD="$REPO/translation/Translation.json"
if [ "$DISC" = disc2 ]; then TRAD="$REPO/translation/Translation_disc2.json"; fi
cp "$TRAD" "$BUILD/Data/Translation.json"
# 0 = placeholder obligatorio del parser; 570 px = ancho real de la caja
dotnet "$DLL" insert-linebreaks 0 570 --base "$BUILD"

echo "==> [4/5] Reempaquetando datos del juego..."
dotnet "$DLL" repack-game --base "$BUILD"

echo "==> [5/5] Reempaquetando ISO..."
dotnet "$DLL" repack-iso "$ISO_OUT" --base "$BUILD"

echo
echo "¡Listo! Tu ISO en español: $ISO_OUT"
echo "Ábrela en PPSSPP para jugar."