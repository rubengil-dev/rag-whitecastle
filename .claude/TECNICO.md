# Qué hay en este archivo y cómo usarlo
- **Contiene:** cómo está hecho el proyecto: repo, entorno, comandos, estructura y limitaciones conocidas. Es un resumen para no tener que buscarlo en el código.
- **No contiene:** el porqué de cada elección ni lo pendiente.
- **Se actualiza:** cuando cambia algo de lo que describe.

## Repo
- GitHub: https://github.com/rubengil-dev/rag-whitecastle (público). Rama principal: `main`.
- Ruta local: `C:\Data\1_MisCosas\Evolve\rag`.
- Saltos de línea LF, fijados en `.gitattributes`.

## Entorno
- Windows.
- Python 3.11.9, notebooks en VS Code. Ojo: el `python` por defecto del sistema es el 3.14; el 3.11 se llama con `py -3.11`.
- Entorno virtual en `.venv/` (fuera de git), dependencias con versión fija en `requirements.txt`.
- API key de Gemini en `.env` como `GOOGLE_API_KEY` (fuera de git). LangChain la lee sola de esa variable.
- Modelos: `gemini-3.5-flash-lite` para el chat y `gemini-embedding-2` para los embeddings (vectores de 3072 dimensiones), en variables de la celda de configuración.

## Comandos
En la terminal de VS Code (PowerShell), desde la carpeta del proyecto.
- Crear el entorno virtual (una sola vez): `py -3.11 -m venv .venv`
- Instalar las dependencias: `.\.venv\Scripts\python -m pip install -r requirements.txt`
- Abrir el notebook: en VS Code, abrir el `.ipynb` → "Select Kernel" → `.venv (Python 3.11.9)`.

## Estructura
- `.gitignore`: deja fuera `.env`, `.venv/`, cachés de Python y Jupyter, `enunciado.pdf` y `data/white_castle.pdf`.
- `.claude/`: documentación de trabajo con Claude.
- `white_castle_rag.ipynb`: el notebook único. Por ahora: título, imports, configuración (rutas y modelos), carga de la key y test de humo de los dos modelos.
- `requirements.txt`: dependencias con versión fija.
- `.env`: la API key. No se sube a git.
- `enunciado.pdf`: enunciado del proyecto. No se sube a git.
- `data/white_castle.pdf`: manual del juego. No se sube a git.

## Datos
- Manual de White Castle en español, 20 páginas, descargado de BoardGameGeek.
- PDF escaneado: cada página es una sola imagen, sin capa de texto (`pypdf` no extrae nada).

## Limitaciones conocidas
Ninguna todavía.
