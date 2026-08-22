# Oreimo Translator GUI

Interfaz gráfica de escritorio (PySide6) para traducir el guion de
*Ore no Imouto ga Konna ni Kawaii Wake ga Nai Portable* (PSP) al español.

Es la "productización" del motor de reingeniería inversa desarrollado en el
proyecto hermano (carpeta padre de este repo) — reutiliza exactamente la
misma lógica de formato ya probada en el juego real (contenedor `GPDA`,
bloques `.obj` con `blockLen`, parcheo binario del ISO), empaquetada aquí
como un paquete Python propio (`src/oreimo_translator/core/`) para que esta
app funcione de forma independiente.

## Qué hace

- Abre el ISO del juego y **extrae automáticamente los ~19,000 diálogos**
  de las 300 escenas.
- Lista las escenas y permite **buscar** texto en todos los diálogos a la
  vez (original o traducción).
- Editar la traducción de una línea es instantáneo y **no toca el ISO** —
  todo vive en memoria hasta que decides compilar.
- **Compilar**: genera un ISO nuevo y jugable con los cambios aplicados
  (nunca sobreescribe el original).
- **Exportar/Importar tabla** (CSV o TSV): para traducir en Excel/Sheets o
  con otra herramienta, y traer los cambios de vuelta.

## Cómo correrlo

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src python3 -m oreimo_translator.main
```

## Descargas

Cada tag `vX.Y.Z` dispara un build automático (GitHub Actions) para
**macOS y Windows**, publicado como [Release](../../releases) — no hace
falta tener Python instalado para usar la app compilada.

## Estado / limitaciones actuales

- El acceso al ISO es 100% Python puro (sin `hdiutil` ni herramientas del
  sistema) — funciona igual en macOS, Windows y Linux.
- Solo se pueden traducir líneas de tipo **Dialogue/Dialogue2** (diálogo
  normal) y **Chapter** (títulos de escena) — cubre todo lo usado hasta
  ahora. Los bloques de tipo **Choice/Choice2/Question** (menús de opciones
  del jugador) se preservan intactos pero aún no son editables desde aquí.
- El orden de la lista de escenas es el orden interno del archivo, no
  necesariamente el orden real del juego (pendiente de mejorar).

## Planeación

La planeación detallada (specs, roadmap, tareas) se maneja fuera de este
repositorio. Aquí solo vive el código y las pruebas.
