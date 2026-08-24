import struct, gzip, sys

PATH = "/mnt/c/Users/christ-gm/Desktop/code/oreimo-es/work/disc1/Data/Extracted/RES/script/AKYO_0020T/000/003image_tukkomi.dat"

with open(PATH, "rb") as f:
    data = f.read()

magic = data[0:4]
total_size, = struct.unpack_from("<q", data, 4)
total_entries, = struct.unpack_from("<i", data, 12)
print("magic:", magic, "total_size:", total_size, "entries:", total_entries)

entries = []
off = 16
for i in range(total_entries):
    entry_offset, entry_size, name_offset = struct.unpack_from("<qii", data, off)
    entries.append((entry_offset, entry_size, name_offset))
    off += 16

for entry_offset, entry_size, name_offset in entries:
    name_len, = struct.unpack_from("<i", data, name_offset)
    name = data[name_offset+4:name_offset+4+name_len].decode("ascii", errors="replace").strip("\x00").strip()
    payload = data[entry_offset:entry_offset+entry_size]
    print("---", name, "size:", entry_size, "payload header:", payload[:4].hex())
    try:
        decompressed = gzip.decompress(payload)
        print("   decompressed len:", len(decompressed), "magic:", decompressed[:12])
    except Exception as e:
        print("   gzip decompress failed:", e)
