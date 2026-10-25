# Qué hay en este archivo y cómo usarlo
- **Contiene:** cómo está hecho el proyecto: repo, entorno, comandos, estructura y limitaciones conocidas. Es un resumen para no tener que buscarlo en el código.
- **No contiene:** el porqué de cada elección ni lo pendiente.
- **Se actualiza:** cuando cambia algo de lo que describe.

## Repo
- GitHub: https://github.com/rubengil-dev/rag-evolve (público). Rama principal: `main`.
- Ruta local: `C:\Data\1_MisCosas\Evolve\rag`.
- Saltos de línea LF, fijados en `.gitattributes`.

## Entorno
- Windows.
- Python 3.11.9, notebooks en VS Code. Ojo: el `python` por defecto del sistema es el 3.14; el 3.11 se llama con `py -3.11`.
- API key de Gemini en `.env` (fuera de git).
- Modelos: `gemini-3.5-flash-lite` para el chat y `gemini-embedding-2` para los embeddings, en variables de la celda de configuración.

## Comandos
En la terminal de VS Code (PowerShell), desde la carpeta del proyecto. Por confirmar hasta probarlos en la Fase 0.
- Crear el entorno virtual (una sola vez): `py -3.11 -m venv .venv`
- Instalar las dependencias: `.\.venv\Scripts\python -m pip install -r requirements.txt`
- Abrir el notebook: en VS Code, abrir el `.ipynb` → "Select Kernel" → `.venv (Python 3.11.9)`.

## Estructura
- `.gitignore`: deja fuera `.env`, `.venv/`, cachés de Python y Jupyter, `enunciado.pdf` y `data/white_castle.pdf`.
- `.claude/`: documentación de trabajo con Claude.
- `enunciado.pdf`: enunciado del proyecto. No se sube a git.
- `data/white_castle.pdf`: manual del juego. No se sube a git.
- Resto por definir.

## Datos
- Manual de White Castle en español, 20 páginas, descargado de BoardGameGeek.
- PDF escaneado: cada página es una sola imagen, sin capa de texto (`pypdf` no extrae nada).

## Limitaciones conocidas
Ninguna todavía.
