# PLAN — Traducción al español de Oreimo PSP "Portable ga Tsuzuku Wake ga Nai"

## 1. Objetivo
Traducir al español (latinoamericano neutro) la novela visual para PSP *Ore no Imouto ga Konna ni Kawaii Wake ga Nai Portable ga Tsuzuku Wake ga Nai* (2 discos, NPJH-50568 / NPJH-50569), partiendo de las ISOs en inglés v1 (Rinjinbu Translations).

## 2. Decisiones confirmadas
| Tema | Decisión |
|---|---|
| Idioma fuente | EN → ES (traducción directa del texto inglés ya extraído) |
| Base técnica | ISOs EN v1 (la fuente latina `font.pgf` con acentos ya está instalada) |
| Variante de español | Latinoamericano neutro |
| Alcance Disco 1 | Historia + menús/sistema + `envpsp.dat` (título, flowchart, OREs) |
| Revisión | Lotes en XLSX editables (col B = texto EN, col C = traducción ES) |
| Orden | Disco 1 completo y probado primero; luego Disco 2 |
| Entorno | Toolchain corre en WSL sin sudo; `mkisofs.exe` de Windows vía interop WSL; revisión y PPSSPP en Windows |

## 3. Hallazgos técnicos (verificados sobre las ISOs)
### 3.1 Dónde vive el texto
| Archivo | Contenido | Ubicación en ISO |
|---|---|---|
| `RES.DAT` (~200 MB) | Guiones de diálogo compilados `.obj.gz` (UTF-16LE; bloques de diálogo/elección/pregunta/capítulo) | `PSP_GAME/INSDIR/` |
| `first.dat` (~1.7 MB) | Texto narrativo `text/utf16.txt.gz` + `seekmap.dat` | `PSP_GAME/USRDIR/` |
| `envpsp.dat` (~104 KB) | Título, ORNAMENT INFORMATION, OREs, flowchart | `PSP_GAME/USRDIR/` |
| `font.pgf` (solo EN) | Fuente latina **con glifos de español** (á é í ó ú ñ ¿ ¡ «» …) | `PSP_GAME/USRDIR/` |
| `libfont.prx` | Módulo de fuente (parcheado en la ISO EN) | `PSP_GAME/USRDIR/` |

### 3.2 Formatos de texto
- Strings con prefijo de longitud (`UInt32`) en **UTF-16LE**.
- Texto extraído por la tool: UTF-16LE sin BOM, una línea = una frase.
- Marcadores que deben conservarse al traducir:
  - `「」` → diálogo (el hablante viene del diccionario de "Actors" del `.obj`)
  - `（）` → narración
  - `＿` (Fullwidth Low Line) → salto de línea manual
  - `｛NN：...｝` → control de tamaño de fuente
  - `[frase]` → insertar frase nueva; `[DEL]` → eliminar frase
- Imágenes con texto: placas de nombres (`sg_chaname.png` + `charaname.txt`, Shift-JIS), nombres de lugares (`placename.txt`), títulos de CG, comentarios. **Fuera de alcance de esta primera versión.**

### 3.3 Toolchain
`zapan/FastAsyncOreimoTranslateTool` (fork C#/.NET 8 de `FastAsyncToradoraTranslateTool`):
- Soporta **exactamente estos discos** (detección vía `UMD_DATA.BIN`: `NPJH-50568` → OreimoDisc1, `NPJH-50569` → OreimoDisc2; rutas internas `script/AKYO_0000A` y `script/_AKYO_0000A`).
- Flujo: `ExtractIso` → `ExtractGame` (DatWorker descomprime `RES.DAT` + `first.dat`; descompresión de `.obj.gz` → `Data/Obj` y `utf16.txt.gz` → `Data/Txt`) → `ExportAll/ImportAll` (XLSX) → `InsertLineBreaksAll` (métricas de `fontmap.txt`) → `RepackGame` → `RepackIso` (mkisofs).
- `DatWorker` es 100% C# (sin exes externos) en esta fork.
- La traducción se guarda en `Data/Translation.json` (`{"<archivo>": {"<índice>": "<traducción>", ...}, "names": {...}}`).

### 3.4 Entorno disponible (verificado)
- WSL interop con Windows: **funciona** (puedo ejecutar `mkisofs.exe` desde WSL, sin sudo).
- 7-Zip de Windows disponible: `C:\Program Files\7-Zip\7z.exe` (necesario para el `.7z` del Disco 2 EN).
- No hay .NET SDK ni mkisofs instalados ni en Windows ni en WSL → se instalarán (`.NET` sin sudo vía `dotnet-install.sh`; `mkisofs.exe` + `cygwin1.dll` descargados del repo `IchinichiQ/ToradoraTranslateTool` en `ToradoraTranslateTool/Data/Mkisofs/`).

## 4. Fases de ejecución
### Fase 0 — Entorno
1. Instalar .NET 8 SDK en WSL (`dotnet-install.sh`, ~/.dotnet, sin sudo).
2. Clonar `zapan/FastAsyncOreimoTranslateTool` en la carpeta del proyecto.
3. Descargar `mkisofs.exe` + `cygwin1.dll` a `bin/` local y añadirlos al PATH (resuelve el repack de ISO sin sudo).
4. Compilar la solución.
5. Verificar `DetectGameFromIso` → OreimoDisc1 con el `UMD_DATA.BIN` del Disco 1 EN.
6. (Opcional) Descargar PPSSPP portable para pruebas.

### Fase 1 — Extracción Disco 1 (EN)
1. `ExtractIso(EN Disc 1)` → `Data/Iso`.
2. `ExtractGame` → `Data/Extracted` (`RES/script/*.obj.gz`, `first/text/utf16.txt.gz`, `seekmap`), `Data/Obj`, `Data/Txt`.
3. Validar que la estructura interna coincide con lo esperado.

### Fase 2 — Corpus
1. Volcado de todas las líneas (narración `utf16.txt` + cada `.obj`: diálogos, elecciones, preguntas, capítulos) con nombre de personaje asociado.
2. Esqueleto de `Data/Translation.json`.
3. Lista única de nombres de personajes → diccionario de traducción.
4. Informe de volumen (nº de líneas por archivo).

### Fase 3 — Traducción IA (EN → ES, latam neutro)
1. Traducción por lotes preservando códigos (`「」`, `（）`, `＿`, `｛NN：｝`, `[x]`, `[DEL]`).
2. Diccionario de nombres consistente (ej. Kyousuke, Kirino, Kuroneko, Saori…).
3. Glosario de términos (honoríficos, referencias otaku/moe).
4. Generar XLSX de revisión por lote (col A = personaje, col B = EN, col C = ES).

### Fase 4 — Revisión del usuario
1. El usuario corrige las celdas C en Excel/LibreOffice.
2. Reimportar los XLSX → `Translation.json`.
3. Iterar hasta aprobación.

### Fase 5 — Saltos de línea
1. `InsertLineBreaksAll(fontmap.txt, maxWidth)` (auto-wrap según métricas de la fuente EN).
2. Control del límite de caja de diálogo (~7 líneas); recorte/inserción manual de frases en líneas largas.

### Fase 6 — Reempaquetado
1. `RepackGame`: reempaqueta `.obj`, `txt`, `RES.DAT`, `seekmap`, `first.dat` y copia los archivos modificados a `Data/Iso`.
2. Herramienta custom (Python/C#) para `envpsp.dat` (strings LP UTF-16LE: título, ornamentos, flowchart/ORE).
3. `font.pgf` se mantiene intacto.

### Fase 7 — ISO
1. `RepackIso` con `mkisofs.exe` → `Oreimo (Spanish) Disc 1.iso`.

### Fase 8 — Pruebas (PPSSPP en Windows)
1. Arranque del juego y menús.
2. Render de acentos y nombres.
3. Cajas de diálogo sin desbordes.
4. Elecciones y saltos de capítulo (offsets de `jump` ajustados automáticamente por la tool).
5. Flowchart y OREs.
6. Iterar correcciones.

### Fase 9 — Disco 2
1. Extraer `Ore no Imouto (English v1) Disc 2.7z` con el 7-Zip de Windows.
2. Repetir fases 1-8 con los discos 2 (JP y EN).

## 5. Riesgos y mitigación
| Riesgo | Mitigación |
|---|---|
| La fork podría tener bugs puntuales en estos discos | Validar Disco 1 de punta a punta antes de invertir en Disco 2 |
| Español ~15-20% más largo que el inglés | Saltos de línea automáticos + recorte manual; verificación visual en PPSSPP |
| Fallo de la tool en algún paso | Respaldo: toolchain Python propia (formato GPDA/LP ya mapeado) |
| `envpsp.dat` requiere parsing custom | Formato conocido (strings LP UTF-16LE); riesgo bajo; archivo pequeño |
| Instalación de herramientas | `.NET` sin sudo; `mkisofs.exe` vía interop WSL (sin sudo) |

## 6. Entregables
- `Oreimo (Spanish) Disc 1.iso` y `Oreimo (Spanish) Disc 2.iso`.
- Carpeta de trabajo reutilizable: corpus, `Translation.json`, XLSX de revisión, scripts.
- Documentación reproducible (este `PLAN.md` + notas de ejecución).

## 7. Notas de ruta
- Rutas WSL: `/mnt/c/Users/christ-gm/Desktop/code/oreimo/` (equivalente a `C:\Users\christ-gm\Desktop\code\oreimo\`).
- ISOs disponibles: JP Disc 1 y 2 (extraídos), EN Disc 1 (extraído), EN Disc 2 (`.7z`).