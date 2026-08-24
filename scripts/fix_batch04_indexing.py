"""Fix batch_04.json: entries were indexed by physical tsv line instead of obj string index.

For each scene, re-map every physical line of the corpus tsv to its record
(record == obj string index), concatenating the translated pieces of each record.
"""
import json
import re
import shutil
import struct
import sys

ROOT = "/mnt/c/Users/christ-gm/Desktop/code/oreimo-es"
BATCH = f"{ROOT}/translation/disc2_batches/batch_04.json"
CORPUS = f"{ROOT}/translation/corpus_disc2"
OBJDIR = f"{ROOT}/work/disc2/Data/Obj"


def parse_obj_strings(path: str) -> list[str]:
    """Replicates OBJEditor.Obj.Import() for the Oreimo version."""
    with open(path, "rb") as f:
        s = f.read()

    def i32(at):
        return struct.unpack_from("<i", s, at)[0]

    def i16(at):
        return struct.unpack_from("<h", s, at)[0]

    def gstr(at):
        n = i32(at)
        at += 4
        return s[at : at + n * 2].decode("utf-16-le")

    strings = []
    block_count = i32(0x00)
    block_len = i32(0x04)
    i = block_len
    for _ in range(block_count):
        code = i16(i + 4)
        index = i + 6
        if code in (0x64, 0x68):          # Dialogue / Dialogue2 (vOREIMO offset 11)
            strings.append(gstr(i + 11))
        elif code == 0x69:                # Choice
            entries = i32(index)
            for _ in range(entries):
                index += 0x8
                strings.append(gstr(index))
                index += i32(index) * 2 + 4
        elif code == 0x67:                # Choice2
            entries = i32(index)
            index += 0x8
            for _ in range(entries):
                strings.append(gstr(index))
                index += i32(index) * 2 + 4
                if i32(index) == 0x00:
                    index += 8
                else:
                    index += 4
                    index += i32(index) * 2 + 4
                    index += 4
        elif code == 0x0323:              # Question
            index += 4
            entries = i32(index)
            index += 4
            strings.append(gstr(index))
            index += 0x4 + i32(index) * 2
            for _ in range(entries):
                strings.append(gstr(index))
                index += 0x4 + i32(index) * 2 + 0x24
        elif code == 0x2BC:               # Chapter
            strings.append(gstr(index))
        i += i32(i)
    return strings


def tsv_records(path: str) -> list[list[int]]:
    """Return, per record, the list of physical line numbers it spans."""
    lines = open(path, encoding="utf-8-sig").read().split("\n")
    records: list[list[int]] = []
    expected = 0
    for n, line in enumerate(lines):
        m = re.match(r"^(\d+)\t", line)
        if m and int(m.group(1)) == expected:
            records.append([n])
            expected += 1
        elif records:
            records[-1].append(n)
    return records


def smart_join(pieces: list[str]) -> str:
    out = ""
    for p in pieces:
        if not p:
            continue
        if out and not out.endswith((" ", "\u3000")) and not p.startswith((" ", "\u3000")):
            out += " "
        out += p
    return re.sub(r"  +", " ", out).strip()


def main() -> None:
    if "--force" not in sys.argv:
        sys.exit(
            "ABORTED: this script is destructive if re-run on an already-fixed "
            "batch (it would treat string indices as tsv line numbers again). "
            "Pass --force to override."
        )
    backup = BATCH + ".bak"
    shutil.copy(BATCH, backup)
    batch = json.load(open(BATCH, encoding="utf-8-sig"))

    fixed = {}
    for scene, tr in batch.items():
        recs = tsv_records(f"{CORPUS}/{scene}.tsv")
        obj = parse_obj_strings(f"{OBJDIR}/{scene}/{scene}")
        if len(recs) != len(obj):
            sys.exit(f"FATAL: {scene}: {len(recs)} records != {len(obj)} obj strings")
        entry = {}
        for k, line_nums in enumerate(recs):
            entry[str(k)] = smart_join([tr.get(str(n), "") for n in line_nums])
        fixed[scene] = entry

    with open(BATCH, "w", encoding="utf-8") as f:
        json.dump(fixed, f, ensure_ascii=False, indent=2)

    print(f"fixed {len(fixed)} scenes -> {BATCH} (backup: {backup})")
    for scene, entry in fixed.items():
        print(f"  {scene}: {len(entry)} strings")


if __name__ == "__main__":
    main()
