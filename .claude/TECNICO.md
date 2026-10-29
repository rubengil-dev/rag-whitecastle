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
- Modelos: `gemini-3.5-flash-lite` para el chat y `gemini-embedding-2` para los embeddings (vectores de 3072 dimensiones), en variables de la celda de configuración, junto con `CHAT_REQUESTS_PER_SECOND`.

## Comandos
En la terminal de VS Code (PowerShell), desde la carpeta del proyecto.
- Crear el entorno virtual (una sola vez): `py -3.11 -m venv .venv`
- Instalar las dependencias: `.\.venv\Scripts\python -m pip install -r requirements.txt`
- Abrir el notebook: en VS Code, abrir el `.ipynb` → "Select Kernel" → `.venv (Python 3.11.9)`.
- Claude ejecuta el notebook con `nbclient` desde un entorno aparte, en su carpeta temporal, con un kernelspec propio que apunta al `python` del `.venv`. `nbclient` no está en `requirements.txt`. Se salta siempre la celda del chat (4.2), que esperaría un `input()`; los bucles de la 2.3 y la 3.3 se saltan si no hay que regenerar sus salidas, y entonces conservan las guardadas.

## Estructura
- `.gitignore`: deja fuera `.env`, `.venv/`, cachés de Python y Jupyter, `enunciado.pdf`, `data/white_castle.pdf`, `data/transcript/`, `chroma_db/` y `guion_demo.md`.
- `README.md`: dominio, cómo funciona, requisitos, instalación (Windows y macOS/Linux), ejecución, system prompt completo con la tabla del porqué, ejemplos, decisiones técnicas y limitaciones. En inglés.
- `guion_demo.md`: guion de la presentación para Rubén, en español. No se sube a git.
- `.claude/`: documentación de trabajo con Claude.
- `white_castle_rag.ipynb`: el notebook único, con las salidas guardadas. Secciones:
  - Intro con el mapa del notebook.
  - 0, setup: imports, rutas y modelos, y carga de la key.
  - 1, base de conocimiento:
    - 1.1, transcripción.
    - 1.2, limpieza y troceado → `chunks`: 76 trozos de 118-1087 caracteres, mediana 616, con metadatos `h1`/`h2`/`h3`, `section` y `page`.
    - 1.3, base vectorial → `vector_store`, colección `white_castle_rules` con ids `chunk_000`….
    - 1.4, comprobación de la recuperación: `RETRIEVAL_K = 5` y `TEST_QUESTIONS = DIRECT_QUESTIONS + HARD_QUESTIONS` (7 + 5, con la página esperada), con una tabla y una celda de conclusiones.
  - 2, agente:
    - 2.1, `SYSTEM_PROMPT` y la tabla con el porqué de cada regla.
    - 2.2, `AgentState`, nodos `retrieve` y `generate` → grafo compilado `agent`; modelo de chat en `llm`.
    - 2.3, `ask()` sobre `TRY_QUESTIONS` (las difíciles de la 1.4, una sin respuesta en el manual y una fuera de tema), con una celda de conclusiones.
  - 3, memoria:
    - 3.1, `REWRITE_PROMPT` y `TOPIC_CHANGE_NOTE`.
    - 3.2, `MemoryState` (añade `question_kind` y `search_query`), `Rewrite` (salida estructurada del reescritor, en `rewriter`), nodos `rewrite`, `retrieve_search_query` y `generate_in_conversation` → grafo `memory_agent` con `InMemorySaver`; `chat(question, thread_id)` muestra la respuesta, cómo se buscó y las páginas.
    - 3.3, `MEMORY_CONVERSATIONS`: `dice`, `courtiers` y `topic_changes` (5 turnos cada una), `new_thread` y `tutorial`, con una celda de conclusiones.
  - 4, chat:
    - 4.1, `EXAMPLE_CONVERSATION`: 6 turnos en el hilo `examples`, uno por cada tipo de pregunta, con una celda de conclusiones (incluye por qué no se usa `gemini-3.8-flash`).
    - 4.2, `chat_loop()`: chat con `input()`, un hilo `chat_N` por conversación (`nueva` / `salir`). Última celda del notebook.
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
- `gemini-3.5-flash-lite` ignora `temperature` (avisa con un `UserWarning`): no se le pasa. Por eso la misma pregunta puede dar respuestas distintas en cada ejecución.
- El plan gratuito de `gemini-3.5-flash-lite` permite 15 llamadas por minuto; al pasarse, devuelve `429 RESOURCE_EXHAUSTED`. El modelo de chat lleva un limitador a 12 por minuto (`CHAT_REQUESTS_PER_SECOND`), así que el notebook entero tarda unos minutos.
- `gemini-3.8-flash` puede devolver `503 UNAVAILABLE` cuando Google lo tiene saturado, y entonces cada llamada tarda minutos en reintentos. Su plan gratuito permite 20 llamadas al día por modelo (`GenerateRequestsPerDayPerProjectPerModel-FreeTier`).
- `agent.get_graph().draw_mermaid_png()` envía el grafo a mermaid.ink, un servicio externo: no se usa.
- En la transcripción, algunas descripciones de iconos son aproximadas, hay sumas con formato de fórmula (`$10+10+3+1+1$`), las viñetas salen como `[Icono: Flecha roja]` y los niveles de título (`#`, `##`) no son del todo coherentes entre páginas. La limpieza quita lo repetido; quedan erratas sueltas (p. ej. "si seis 2/3/4 jugadores" en la p. 2) e iconos dentro de algunos títulos de sección.
