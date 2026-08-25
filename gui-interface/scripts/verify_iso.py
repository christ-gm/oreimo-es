"""
Verifies an ISO produced by iso_grow.write_files_into_iso against the
source it was built from.

The in-place filesystem edit is only safe if the disc a reader sees
afterwards is the disc we intended: every untouched file identical byte
for byte, the replaced ones matching exactly what we asked for, and the
whole thing still parseable as ISO9660 by an implementation that isn't
ours (pycdlib), so we aren't just agreeing with our own bugs.

Usage:
    python scripts/verify_iso.py SOURCE.iso BUILT.iso [inner=path/to/expected.bin ...]

Exits non-zero and prints every mismatch if anything is wrong.
"""
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from oreimo_translator.core import iso_grow  # noqa: E402

SECTOR = iso_grow.SECTOR


def digest_via_records(iso_path, entry):
    """Reads a file the way the directory record says to."""
    h = hashlib.sha256()
    with open(iso_path, "rb") as f:
        f.seek(entry.extent * SECTOR)
        remaining = entry.length
        while remaining > 0:
            chunk = f.read(min(1 << 22, remaining))
            if not chunk:
                break
            h.update(chunk)
            remaining -= len(chunk)
    return h.hexdigest()


def entries_of(iso_path):
    with open(iso_path, "rb") as f:
        return {e.path.upper(): e for e in iso_grow.read_entries(f) if not e.is_dir}


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    source, built = sys.argv[1], sys.argv[2]
    expected = {}
    for arg in sys.argv[3:]:
        inner, _, path = arg.partition("=")
        expected[inner.upper()] = Path(path).read_bytes()

    src_entries = entries_of(source)
    out_entries = entries_of(built)

    problems = []

    # ---- 1. an independent reader must still understand the disc ----
    # Names are compared case-insensitively between the two images, but
    # pycdlib is case-sensitive and this disc is ISO level 4 (mixed-case
    # names, no ';1' version suffix), so look records up by the exact
    # identifier the record carries.
    try:
        import pycdlib
        iso = pycdlib.PyCdlib()
        iso.open(built)
        try:
            unresolved = []
            for key, entry in out_entries.items():
                try:
                    iso.get_record(iso_path=entry.path)
                except Exception:
                    unresolved.append(entry.path)
        finally:
            iso.close()
        if unresolved:
            problems.append(
                f"pycdlib could not resolve {len(unresolved)} record(s): "
                + ", ".join(unresolved[:5]))
        else:
            print(f"pycdlib   : abre la imagen y resuelve los {len(out_entries)} registros  OK")
    except Exception as exc:
        problems.append(f"pycdlib cannot read the built ISO: {exc}")

    # ---- 2. the file set must be unchanged, minus reclaimed filler ----
    missing = set(src_entries) - set(out_entries)
    added = set(out_entries) - set(src_entries)
    for path in sorted(missing):
        problems.append(f"file disappeared from the disc: {path}")
    for path in sorted(added):
        problems.append(f"unexpected new file on the disc: {path}")

    # ---- 3. contents ----
    print(f"{'archivo':<40} {'estado'}")
    for path, out_entry in sorted(out_entries.items()):
        src_entry = src_entries.get(path)
        if src_entry is None:
            continue
        if path in expected:
            want = expected[path]
            got_hash = digest_via_records(built, out_entry)
            want_hash = hashlib.sha256(want).hexdigest()
            if out_entry.length != len(want):
                problems.append(
                    f"{path}: length is {out_entry.length}, expected {len(want)}")
                status = "LONGITUD INCORRECTA"
            elif got_hash != want_hash:
                problems.append(f"{path}: contents differ from the bytes supplied")
                status = "CONTENIDO INCORRECTO"
            else:
                status = f"reemplazado OK  ({len(want):,} B @LBA {out_entry.extent})"
        elif out_entry.length == 0 and src_entry.length > 0:
            status = f"relleno reclamado ({src_entry.length:,} B liberados)"
        else:
            if src_entry.length != out_entry.length:
                problems.append(
                    f"{path}: length changed {src_entry.length} -> {out_entry.length}")
                status = "LONGITUD CAMBIADA"
            else:
                a = digest_via_records(source, src_entry)
                b = digest_via_records(built, out_entry)
                if a != b:
                    problems.append(f"{path}: contents changed but shouldn't have")
                    status = "CONTENIDO ALTERADO"
                elif src_entry.extent != out_entry.extent:
                    status = f"movido intacto  (LBA {src_entry.extent} -> {out_entry.extent})"
                else:
                    status = "intacto"
        print(f"{path:<40} {status}")

    # ---- 4. no two files may claim the same sectors ----
    runs = sorted((e.extent, e.extent + (e.length + SECTOR - 1) // SECTOR, p)
                  for p, e in out_entries.items() if e.length > 0)
    for (s1, e1, p1), (s2, e2, p2) in zip(runs, runs[1:]):
        if s2 < e1:
            problems.append(f"overlapping files: {p1} [{s1},{e1}) and {p2} [{s2},{e2})")

    print()
    if problems:
        print(f"FALLOS ({len(problems)}):")
        for p in problems:
            print("  -", p)
        return 1
    print("Todo correcto: la imagen es legible, ningún archivo intacto cambió, "
          "los reemplazos coinciden y no hay solapamientos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
