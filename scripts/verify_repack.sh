#!/bin/bash
set -e
export DOTNET_ROOT=~/.dotnet
export PATH=~/.dotnet:$PATH

DLL="/mnt/c/Users/christ-gm/Desktop/code/oreimo/tool/OreimoAutomation/bin/Release/net10.0/OreimoAutomation.dll"
ISO="/mnt/c/Users/christ-gm/Desktop/code/oreimo-es/Disc1_PRUEBA.iso"
CHECK="/mnt/c/Users/christ-gm/Desktop/code/oreimo-es/work/check"

rm -rf "$CHECK"
dotnet "$DLL" extract-iso "$ISO" --base "$CHECK"
dotnet "$DLL" extract-game --base "$CHECK"

echo "=== target file info ==="
ls -la "$CHECK/Data/Extracted/RES/script/AKYO_0020T/000/003image_tukkomi/TKA0020A.gim"
md5sum "$CHECK/Data/Extracted/RES/script/AKYO_0020T/000/003image_tukkomi/TKA0020A.gim"
md5sum "/mnt/c/Users/christ-gm/Desktop/code/oreimo-es/work/disc1/Data/Extracted/RES/script/AKYO_0020T/000/003image_tukkomi/TKA0020A.gim"
