"""Entry point for PyInstaller builds. Kept outside the oreimo_translator
package so its internal relative imports (from .gui import ...) work
correctly when frozen - pointing PyInstaller directly at main.py inside
the package breaks that (it gets treated as a top-level script, not part
of the package)."""
from oreimo_translator.main import main

if __name__ == "__main__":
    main()
