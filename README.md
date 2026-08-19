# Oreimo Portable — Traducción al Español (ES)

[![Progreso Disco 1](https://img.shields.io/badge/Progreso%20Disco%201-100%25-green)](translation/Translation.json)
[![Progreso Disco 2](https://img.shields.io/badge/Progreso%20Disco%201-0%25-red)](translation/Translation.json)
[![Estado](https://img.shields.io/badge/Estado-Traducci%C3%B3n%20100%25%20%7C%20Falta%20pruebas-yellow)]()
[![Licencia](https://img.shields.io/badge/Licencia-CC%20BY--NC--SA%204.0-lightgrey)](LICENSE)

Traducción **no oficial** al español latinoamericano de la novela visual PSP **_Oreimo Portable ga Tsuzuku Wake ga Nai_** (Discos 1 y 2), partiendo de la versión en inglés v1.

> Este repositorio registra el **progreso de traducción**, el **corpus extraído** y los **scripts de automatización** del proyecto. Las ISOs finales no se distribuyen aquí.

---

## Estado del proyecto

| Disco | Progreso |
|---|---|
| **Disco 1** (historia) | 18.805 / 18.805 líneas — **100%** (299 escenas, revisado) |
| Disco 2 (historia) | pendiente |
| envpsp.dat (texto del sistema) | pendiente |

Los **nombres** de personajes (38) ya están traducidos y aplicados en todas las escenas.

---

## Aviso importante (traducción MTL)

Esta traducción es **MTL (Machine Translation)**: fue generada con traducción automática y revisada manualmente en lo posible, **no** es una traducción humana profesional. Puede haber frases poco naturales, errores de contexto o detalles que no te gusten.

Quiero ser transparente desde el principio para que no te lleves sorpresas: simplemente quería una opción para jugar este juego en español y no me gustaban las alternativas que existían, así que me dediqué a crear la mía propia y compartirla para quien quiera usarla.

## Demo

![Captura 2](assets/image2.png)

![Captura 1](assets/image.png)

https://github.com/user-attachments/assets/89a1ea8c-f36d-41dd-9895-dd198a5309c8

## Créditos

- **[dizzyziddy — Oreimo Tsuzuku PSP Disc 1 Full English Patch](https://dizzyziddy.xyz/2015/02/14/oreimo-tsuzuku-psp-disc-1-full-english-patch-release/)** — este proyecto se construyó **sobre su parche en inglés v1**, que sirvió como base del texto. ¡Muchas gracias por ese trabajo!

---

## Cómo parchar tu ISO

Este repositorio **no incluye ISOs ni el código de la toolchain original** (ver [Herramientas usadas](#herramientas-usadas)). Incluye dos asistentes que hacen todo por ti: **`build_iso.bat`** (Windows) y **`build_iso.sh`** (Linux/WSL).

> El único requisito de entrada es tu **ISO con el parche EN v1 de dizzyziddy ya aplicado** (link en [Créditos](#créditos)).

### Windows (fácil) — `build_iso.bat`

1. Descarga este repositorio como **ZIP** (botón verde *Code* → *Download ZIP*) y descomprímelo.
2. Coloca tu ISO (ya con el parche EN aplicado) donde quieras, por ejemplo en la misma carpeta.
3. **Arrastra el archivo `.iso` sobre `build_iso.bat`** y suéltalo. (También puedes abrir `build_iso.bat` y escribir la ruta.)
4. Si te falta el .NET SDK, el propio asistente lo instalará automáticamente o te dará el enlace.
5. Al terminar tendrás tu ISO en español con el sufijo `_ES` y se abrirá la carpeta donde se guardó.

> La primera vez descarga la toolchain base de zapan (necesita internet); las siguientes reutilizan la copia local.
> Windows puede mostrar "Editor desconocido" al ejecutar el `.bat` (no está firmado): pulsa *Más información → Ejecutar de todas formas*.

### Linux / WSL — `build_iso.sh`

#### Prerrequisitos

1. Una **copia legal** \*guiño guiño\* del juego (ISO de PSP de *Oreimo Portable ga Tsuzuku Wake ga Nai*) Recomendablemente la de **[dizzyziddy — Oreimo Tsuzuku PSP Disc 1 Full English Patch](https://dizzyziddy.xyz/2015/02/14/oreimo-tsuzuku-psp-disc-1-full-english-patch-release/)**.
2. **.NET SDK** (10 o superior), **git** y **mkisofs** (de cdrtools) en tu `PATH`.
3. Linux / WSL (Windows Subsystem for Linux).
4. Windows -> Estoy Cansado Jefe... (Trabajando en ello)

#### Pasos

```bash
git clone https://github.com/christ-gm/oreimo-es.git
cd oreimo-es
./build_iso.sh /ruta/a/tu.iso          # genera /ruta/a/tu.iso con el sufijo _ES
```

Opciones del script:

- `--out <archivo.iso>`: nombre de la ISO resultante (por defecto: `<tu_iso>_ES.iso`).
- Variables de entorno `TOOLCHAIN_DIR` y `WORK_DIR` para reutilizar un clon existente de la toolchain y elegir el directorio de trabajo.

#### Pasos manuales (equivalente al script)

```bash
git clone https://github.com/christ-gm/oreimo-es.git
git clone https://github.com/zapan/FastAsyncOreimoTranslateTool.git

# Compila el driver (resuelve las librerías de la toolchain automáticamente)
cp -r oreimo-es/tool/OreimoAutomation FastAsyncOreimoTranslateTool/
cd FastAsyncOreimoTranslateTool
dotnet build OreimoAutomation -c Release

mkdir -p work
export DLL=$(pwd)/OreimoAutomation/bin/Release/net10.0/OreimoAutomation.dll
export BASE=$(pwd)/work

dotnet "$DLL" extract-iso /ruta/a/tu.iso --base "$BASE"        # 1) Extrae tu ISO
dotnet "$DLL" extract-game --base "$BASE"                      # 2) Extrae los datos del juego
cp ../oreimo-es/translation/Translation.json "$BASE"/Data/Translation.json
dotnet "$DLL" insert-linebreaks --base "$BASE"                 # 3) Aplica la traducción
dotnet "$DLL" repack-game --base "$BASE"                       # 4) Reempaqueta los datos
dotnet "$DLL" repack-iso "$BASE"/oreimo_es.iso --base "$BASE"  # 5) Reempaqueta la ISO
```

> **mkisofs**: si no lo tienes, en Debian/Ubuntu puedes instalarlo con `sudo apt install genisoimage` (o `cdrtools` en Arch). Asegúrate de que esté en tu `PATH`.

---

## Correcciones y reportes

¿Encontraste un error de traducción, una frase mal contextualizada o un detalle en los subtítulos? **Eres libre de abrir un [issue](https://github.com/christ-gm/oreimo-es/issues)** con la escena, el texto original y tu sugerencia de corrección.

Los iré revisando **a mi ritmo** (este es un proyecto personal). Además, conforme vaya jugando e identifique detalles, los iré corrigiendo yo mismo en futuras actualizaciones.

---

## Estructura del repositorio

```
├── translation/
│   ├── Translation.json      # Progreso de traducción (fichero principal)
│   ├── corpus/               # Texto EN extraído de las escenas (299 .tsv + names.txt)
│   └── review/               # Hojas XLSX de revisión (EN → ES)
├── scripts/                  # Scripts de traducción por lotes
├── tool/OreimoAutomation/    # Driver de automatización (C#, propio)
├── tool-bin/                 # Utilidades para el repaqueado de la ISO (mkisofs)
├── toolchain-patches/        # Parches propios para la toolchain de zapan
├── build_iso.bat             # Asistente para Windows (arrastra tu ISO)
└── build_iso.sh              # Asistente para Linux / WSL
```

### ¿Cómo funciona el flujo?

1. **Extracción**: la ISO EN v1 se desempaca en escenas (`.obj`) y se vuelca el corpus.
2. **Traducción**: las escenas se traducen por lotes (10 escenas por lote).
3. **Revisión**: cada lote se exporta a XLSX (`EN | ES`) para su revisión.
4. **Rempacado**: las traducciones se inyectan, se reinsertan los saltos de línea automáticos y se reconstruye la ISO con la fuente latina (soporta acentos).

> Los `Translation.json` y el corpus contienen únicamente **texto**, nunca assets ni código del juego.

## Herramientas usadas

- [FastAsyncOreimoTranslateTool](https://github.com/zapan/FastAsyncOreimoTranslateTool) — toolchain base de extracción/reempacado (de [IchinichiQ](https://github.com/IchinichiQ/ToradoraTranslateTool) y [computer-catt](https://github.com/computer-catt/FastAsyncToradoraTranslateTool)).
- `OreimoAutomation` — driver propio que automatiza todo el pipeline de forma headless.
- `.NET 10`, Python, `mkisofs`.

## Licencia

El trabajo de **traducción y los scripts propios** de este repositorio están bajo **CC BY-NC-SA 4.0**.

El contenido del juego (código, imágenes, audio y texto original) pertenece a sus respectivos titulares de derechos (**Aniplex / ASCII Media Works**). Este proyecto es una traducción de fans, sin fines comerciales, y no está afiliado ni respaldado por los titulares de derechos.

Para jugar necesitas una **copia legal** \*guiño guiño\* del juego. Este repositorio no incluye las ISOs.
