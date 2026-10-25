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
- `.gitignore`: deja fuera `.env`, `.venv/`, cachés de Python y Jupyter, `enunciado.pdf`, `data/white_castle.pdf`, `data/transcript/` y `chroma_db/`.
- `.claude/`: documentación de trabajo con Claude.
- `white_castle_rag.ipynb`: el notebook único. Por ahora: título, imports, configuración (rutas y modelos), carga de la key, test de humo de los dos modelos, sección 1 (transcripción) y sección 2 (limpieza y troceado → variable `chunks`: 76 trozos de 118-1087 caracteres, mediana 616, con metadatos `h1`/`h2`/`h3`, `section` y `page`), sección 3 (base vectorial → variable `vector_store`, colección `white_castle_rules` con ids `chunk_000`…) y sección 4 (comprobación de la recuperación con `TEST_QUESTIONS`, `RETRIEVAL_K = 3`).
- `data/transcript/page_NN.md`: la transcripción, un archivo por página (20). No se sube a git.
- `chroma_db/`: base vectorial local (76 trozos). No se sube a git. Se reconstruye poniendo `REBUILD_VECTOR_STORE = True` una vez, o borrando la carpeta.
- `requirements.txt`: dependencias con versión fija.
- `.env`: la API key. No se sube a git.
- `enunciado.pdf`: enunciado del proyecto. No se sube a git.
- `data/white_castle.pdf`: manual del juego. No se sube a git.

## Datos
- Manual de White Castle en español, 20 páginas, descargado de BoardGameGeek.
- PDF escaneado: cada página es una sola imagen JPEG de 1102×1654, sin capa de texto (`pypdf` no extrae texto, pero sí la imagen con `page.images[0].data`).
- Transcripción: unos 44.000 caracteres en total. Revisadas a mano las páginas 5, 10 y 15 contra la imagen: el texto es fiel. Las páginas 15 y 19-20 son casi todo imagen o créditos.

## Limitaciones conocidas
- `gemini-3.5-flash-lite` ignora `temperature` (avisa con un `UserWarning`): no se le pasa.
- En la transcripción, algunas descripciones de iconos son aproximadas, hay sumas con formato de fórmula (`$10+10+3+1+1$`), las viñetas salen como `[Icono: Flecha roja]` y los niveles de título (`#`, `##`) no son del todo coherentes entre páginas. La limpieza quita lo repetido; quedan erratas sueltas (p. ej. "si seis 2/3/4 jugadores" en la p. 2) e iconos dentro de algunos títulos de sección.
