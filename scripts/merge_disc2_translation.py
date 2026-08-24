"""Merge disc2 batch translations into the game's Translation.json.

Reads every translation/disc2_batches/batch_*.json and produces
work/disc2/Data/Translation.json with all translated scenes plus the
character-name mapping. Scenes without a batch yet are left out
(the tool treats missing keys as untranslated).

Usage: python3 scripts/merge_disc2_translation.py [--dry-run]
"""
import glob
import json
import os
import re
import sys

# Los objs guardan el diálogo como 'Nombre「texto」' pero la toolchain
# (ObjHelper) separa nombre y texto: la tabla de actores lleva el nombre
# (traducido vía NAMES_ES) y el string sólo debe ser '「texto」'.
SPEECH_RE = re.compile(r"^([^「]{1,25})「(.*)」$", re.S)


def to_game_format(text: str) -> str:
    m = SPEECH_RE.match(text)
    if m:
        return f"「{m.group(2)}」"
    return text

ROOT = "/mnt/c/Users/christ-gm/Desktop/code/oreimo-es"
BATCHES = f"{ROOT}/translation/disc2_batches"
OUT = f"{ROOT}/work/disc2/Data/Translation.json"

NAMES_ES = {
    "Kiririn": "Kiririn",
    "Kuronyan": "Kuronyan",
    "Kyousuke": "Kyousuke",
    "???": "???",
    "Kirino": "Kirino",
    "Yoshino": "Yoshino",
    "Daisuke": "Daisuke",
    "Kanako": "Kanako",
    "Kyousuke & Kirino": "Kyousuke y Kirino",
    "Kirara": "Kirara",
    "Saori": "Saori",
    "Ayase": "Ayase",
    "Akane": "Akane",
    "Akagi": "Akagi",
    "Kirino & Kyousuke": "Kirino y Kyousuke",
    "Brats": "Niños",
    "Sena": "Sena",
    "Kuroneko": "Kuroneko",
    "Manami": "Manami",
    "Ruri": "Ruri",
    "??": "??",
    "Everybody": "Todos",
    "Yuuno": "Yuuno",
    "Ryousuke": "Ryousuke",
    "Hinata": "Hinata",
    "Tamaki": "Tamaki",
    "Fate": "Fate",
    "Woman": "Mujer",
    "Commentary": "Comentarista",
    "Otaku 1": "Otaku 1",
    "Otaku 2": "Otaku 2",
    "Kyousuke & Kuroneko": "Kyousuke y Kuroneko",
    "TV 1": "TV 1",
    "TV 2": "TV 2",
    "Yuri": "Yuri",
    "fairy": "Hada",
    "Bajeena": "Bajeena",
    "Maid": "Sirvienta",
    "Kanata": "Kanata",
    "Kaori": "Kaori",
    "Both": "Ambos",
    "Saori & Kaori": "Saori y Kaori",
    "Otaku Girls": "Chicas otaku",
    "Tomoka": "Tomoka",
    "Kurara": "Kurara",
    "Girl": "Chica",
    "Grandpa": "Abuelo",
    "Employee": "Empleada",
    "Landlady": "Dueña",
    "Tourist": "Turista",
    "Granny": "Abuela",
    "Rock": "Rock",
    "Nao": "Nao",
    "Mio": "Mio",
    "Photographer": "Fotógrafo",
    "Clerk": "Dependiente",
    "Chitose": "Chitose",
    "President": "Presidenta",
    "Makabe": "Makabe",
    "Trio": "Trío",
    "Boy A": "Chico A",
    "Boy B": "Chico B",
    "Butler": "Mayordomo",
    "Woman A": "Mujer A",
    "Woman B": "Mujer B",
    "Woman C": "Mujer C",
    "Hinata & Tamaki": "Hinata y Tamaki",
    "????": "????",
    "Fairy": "Hada",
    "Kamineko": "Kamineko",
    "All Kuroneko": "Todas las Kuroneko",
    "Yamineko": "Yamineko",
    "Kanami": "Kanami",
    "Bridget": "Bridget",
    "Meruru": "Meruru",
}


def main() -> None:
    dry = "--dry-run" in sys.argv

    merged: dict[str, dict] = {}
    for path in sorted(glob.glob(f"{BATCHES}/batch_*.json")):
        data = json.load(open(path, encoding="utf-8-sig"))
        for scene, entry in data.items():
            if not scene.startswith("000script"):
                continue
            if scene in merged:
                sys.exit(f"FATAL: {scene} duplicada en {path}")
            merged[scene] = entry

    out = {"names": NAMES_ES}
    out.update({sc: {i: to_game_format(t) for i, t in entry.items()} for sc, entry in merged.items()})

    total_strings = sum(len(v) for v in merged.values())
    empty = sum(1 for v in merged.values() for t in v.values() if not t.strip())
    print(f"escenas traducidas : {len(merged)}/268")
    print(f"strings            : {total_strings - empty}/{total_strings} no vacíos")

    # nombres EN sin traducción definida
    listed = [
        l.strip()
        for l in open(f"{ROOT}/translation/names_disc2.txt", encoding="utf-8-sig")
        if l.strip()
    ]
    missing_names = [n for n in listed if n not in NAMES_ES]
    unused_names = [n for n in NAMES_ES if n not in listed]
    if missing_names:
        print("nombres SIN mapeo  :", missing_names)
    if unused_names:
        print("nombres sin uso    :", unused_names)

    if dry:
        return
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False)
    print(f"escrito: {OUT}")


if __name__ == "__main__":
    main()
