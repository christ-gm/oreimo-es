#!/bin/bash
set -e
export DOTNET_ROOT=~/.dotnet
export PATH=~/.dotnet:$PATH

DLL="/mnt/c/Users/christ-gm/Desktop/code/oreimo/tool/OreimoAutomation/bin/Release/net10.0/OreimoAutomation.dll"
BASE="/mnt/c/Users/christ-gm/Desktop/code/oreimo-es/work/disc1"
OUT="/mnt/c/Users/christ-gm/Desktop/code/oreimo-es/Disc1_PRUEBA.iso"

export PATH="/mnt/c/Users/christ-gm/Desktop/code/oreimo-es/tool-bin:$PATH"

echo "== repack-game =="
dotnet "$DLL" repack-game --base "$BASE"

echo "== repack-iso =="
dotnet "$DLL" repack-iso "$OUT" --base "$BASE"

echo "== done =="
ls -la "$OUT"
