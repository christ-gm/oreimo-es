using System.Text;
using OBJEditor;
using RyuujiApi;
using TranslateCLI;

Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);

if (args.Length == 0) {
    Console.Error.WriteLine("Usage: OreimoAutomation <command> [args...] [--base <dir>]");
    Console.Error.WriteLine("Commands:");
    Console.Error.WriteLine("  extract-iso <isoPath>");
    Console.Error.WriteLine("  extract-game");
    Console.Error.WriteLine("  dump-corpus <outDir>");
    Console.Error.WriteLine("  dump-names <outFile>");
    Console.Error.WriteLine("  export-xlsx <outDir>");
    Console.Error.WriteLine("  import-xlsx <inDir>");
    Console.Error.WriteLine("  insert-linebreaks [maxWidth]");
    Console.Error.WriteLine("  repack-game [--debug]");
    Console.Error.WriteLine("  repack-iso <outPath>");
    Console.Error.WriteLine("  progress");
    return 1;
}

string command = args[0];

string basePath = Path.GetFullPath(Environment.GetEnvironmentVariable("OREMO_BASE") ?? AppContext.BaseDirectory);
string fontmap = Path.Combine(AppContext.BaseDirectory, "Resources", "fontmap.txt");
int maxWidth = 455;
string? posArg = null;

for (int i = 1; i < args.Length; i++) {
    if (args[i] == "--base") {
        basePath = Path.GetFullPath(args[++i]);
    } else if (args[i] == "--debug") {
        // handled by caller
    } else if (args[i] == "--translated") {
        // handled by caller
    } else if (posArg == null) {
        posArg = args[i];
    } else if (int.TryParse(args[i], out int w)) {
        maxWidth = w;
    }
}

try {
    switch (command) {
        case "extract-iso": {
            if (posArg == null) throw new ArgumentException("extract-iso requires <isoPath>");
            RyuujiApi.RyuujiApi api = new(basePath);
            Console.WriteLine($"Extracting ISO: {posArg}");
            await api.ExtractIso(posArg, f => { }, p => { });
            Console.WriteLine("ISO extracted to " + Path.Combine(basePath, "Data", "Iso"));
            break;
        }

        case "extract-game": {
            RyuujiApi.RyuujiApi api = new(basePath);
            Directory.CreateDirectory(Path.Combine(basePath, "Resources", "DebugMode"));
            Console.WriteLine("Extracting game data (RES.DAT + first.dat)...");
            await api.ExtractGame(Path.Combine(basePath, "Data"));
            Console.WriteLine("Game data extracted.");
            break;
        }

        case "dump-corpus": {
            if (posArg == null) throw new ArgumentException("dump-corpus requires <outDir>");
            TranslationProjectCli app = new(basePath);
            Directory.CreateDirectory(posArg);
            Console.WriteLine($"Dumping {app.Files.Count} files...");
            foreach (var file in app.Files) {
                app.LoadFile(file.FileName);
                string outFile = Path.Combine(posArg, file.FileName + ".tsv");
                using (StreamWriter w = new(outFile, false, new UTF8Encoding(false))) {
                    for (int i = 0; i < app.Strings.Count; i++) {
                        w.WriteLine($"{i}\t{app.Strings[i].Name}\t{app.Strings[i].Sentence}");
                    }
                }
            }
            Console.WriteLine("Corpus dumped to " + posArg);
            break;
        }

        case "dump-names": {
            if (posArg == null) throw new ArgumentException("dump-names requires <outFile>");
            TranslationProjectCli app = new(basePath);
            List<string> names = app.GetAllNames();
            File.WriteAllLines(posArg, names, new UTF8Encoding(false));
            Console.WriteLine($"{names.Count} names written to {posArg}");
            break;
        }

        case "export-xlsx": {
            if (posArg == null) throw new ArgumentException("export-xlsx requires <outDir> [--translated]");
            TranslationProjectCli app = new(basePath);
            bool translatedOnly = args.Contains("--translated");
            Console.WriteLine("Exporting xlsx review files...");
            if (!translatedOnly) {
                app.ExportAll(posArg);
            } else {
                Directory.CreateDirectory(posArg);
                foreach (var file in app.Files) {
                    if (file.TranslationPercent <= 0) continue;
                    app.LoadFile(file.FileName);
                    app.ExportText(Path.Combine(posArg, Path.GetFileNameWithoutExtension(file.FileName) + ".xlsx"));
                }
            }
            Console.WriteLine("Exported to " + posArg);
            break;
        }

        case "import-xlsx": {
            if (posArg == null) throw new ArgumentException("import-xlsx requires <inDir>");
            TranslationProjectCli app = new(basePath);
            Console.WriteLine("Importing xlsx review files (column C)...");
            app.ImportAll(posArg, 3, 1);
            Console.WriteLine("Imported.");
            break;
        }

        case "insert-linebreaks": {
            if (!File.Exists(fontmap)) throw new FileNotFoundException("fontmap.txt not found at " + fontmap);
            TranslationProjectCli app = new(basePath);
            Console.WriteLine($"Inserting line breaks (maxWidth={maxWidth})...");
            app.InsertLineBreaksAll(fontmap, maxWidth);
            Console.WriteLine("Line breaks inserted.");
            break;
        }

        case "repack-game": {
            bool debug = args.Contains("--debug");
            RyuujiApi.RyuujiApi api = new(basePath);
            Console.WriteLine("Repacking game data...");
            await api.RepackGame(Path.Combine(basePath, "Data"), debug);
            Console.WriteLine("Game data repacked.");
            break;
        }

        case "repack-iso": {
            if (posArg == null) throw new ArgumentException("repack-iso requires <outPath>");
            RyuujiApi.RyuujiApi api = new(basePath);
            string isoDir = Path.Combine(basePath, "Data", "Iso");
            Console.WriteLine("Repacking ISO (mkisofs) -> " + posArg);
            api.RepackIso("mkisofs", isoDir, posArg);
            Console.WriteLine("ISO repacked.");
            break;
        }

        case "progress": {
            TranslationProjectCli app = new(basePath);
            Console.WriteLine($"Total translation progress: {app.GetTotalPercent()}%");
            break;
        }

        case "dump-obj": {
            if (posArg == null) throw new ArgumentException("dump-obj requires <file> [more files...]");
            foreach (string p in args[1..]) {
                ObjHelper h = new(File.ReadAllBytes(p), 1);
                string[] s = h.Import();
                Console.WriteLine($"=== {p}: {s.Length} strings ===");
                for (int i = 0; i < s.Length; i++)
                    Console.WriteLine($"{i}\t{h.Actors?[i]}\t{s[i]}");
            }
            break;
        }

        default:
            Console.Error.WriteLine($"Unknown command: {command}");
            return 1;
    }

    return 0;
} catch (Exception ex) {
    Console.Error.WriteLine("ERROR: " + ex);
    return 1;
}