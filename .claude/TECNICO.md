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
- Arrancar el chat web: `.\.venv\Scripts\streamlit run app.py` → se abre en http://localhost:8501. La primera vez, Streamlit puede pedir un email en la terminal: Enter para saltarlo. Ctrl+C la para. Necesita `chroma_db/` creada antes por el notebook.
- Claude prueba el chat web arrancándolo con `--server.headless true` (sin abrir navegador ni pedir email) y abriéndolo en su navegador.
- Claude ejecuta el notebook con `nbclient` desde un entorno aparte, en su carpeta temporal, con un kernelspec propio que apunta al `python` del `.venv`. `nbclient` no está en `requirements.txt`. Se salta siempre la celda del chat (3.2), que esperaría un `input()`.

## Estructura
- `.gitignore`: deja fuera `.env`, `.venv/`, cachés de Python y Jupyter, `enunciado.pdf`, `data/white_castle.pdf`, `data/transcript/`, `chroma_db/` y `guion_demo.md`.
- `README.md`: dominio, cómo funciona, requisitos, instalación (Windows y macOS/Linux), ejecución, chat web opcional, system prompt completo con su porqué, ejemplos, decisiones técnicas y limitaciones. En inglés.
- `app.py`: chat web en Streamlit con el agente del notebook. Arriba, las constantes: rutas, modelos, prompts copiados del notebook (idénticos), textos de la interfaz y estilo de la página (`PAGE_STYLE`, `HEADER_HTML`). Después, la página: `main()` → `check_setup` → `start_session` → `show_sidebar` → `show_conversation` → `answer_question`, que escribe la respuesta según llega (`stream_answer` con `stream_mode="messages"`, solo los trozos del nodo `generate`) y la guarda en `st.session_state.messages`. Abajo, el agente copiado; el modelo, el reescritor, la base y el grafo salen de funciones con `st.cache_resource` (`get_llm`, `get_rewriter`, `get_vector_store`, `get_agent`), así que se crean una vez y los comparten todas las conversaciones. Una conversación por pestaña del navegador, con un `thread_id` aleatorio.
- `.streamlit/config.toml`: tema del chat web (colores, fuentes de Google Fonts, tema claro fijo), barra de herramientas mínima y sin estadísticas de uso.
- `assets/`: avatares SVG del chat web, `farmer.svg` (jugador) y `robot.svg` (asistente).
- `guion_demo.md`: guion de la presentación para Rubén, en español. No se sube a git.
- `.claude/`: documentación de trabajo con Claude.
- `white_castle_rag.ipynb`: el notebook único, con las salidas guardadas. Secciones:
  - Intro con el mapa del notebook.
  - 0, setup: imports, rutas y modelos, carga de la key y modelo de chat `llm` con su limitador, compartido por la transcripción y el agente.
  - 1, base de conocimiento:
    - 1.1, transcripción.
    - 1.2, limpieza y troceado → `chunks`: 76 trozos de 118-1087 caracteres, mediana 616, con metadatos `h1`/`h2`/`h3`, `section` y `page`.
    - 1.3, base vectorial → `vector_store`, colección `white_castle_rules` con ids `chunk_000`….
    - 1.4, comprobación de la recuperación: `RETRIEVAL_K = 5` y `TEST_QUESTIONS = DIRECT_QUESTIONS + HARD_QUESTIONS` (7 + 5, con la página esperada), con una tabla y una celda de conclusiones.
  - 2, agente con memoria:
    - 2.1, `SYSTEM_PROMPT` y su porqué en dos puntos (rol y tono; qué responde y con qué).
    - 2.2, memoria: `REWRITE_PROMPT`, `TOPIC_CHANGE_NOTE` y `FOLLOW_UP_NOTE`.
    - 2.3, `AgentState` (`messages`, `question_kind`, `search_query`, `chunks`), `Rewrite` (salida estructurada del reescritor, en `rewriter`), nodos `rewrite`, `retrieve` y `generate` → grafo `agent` con `InMemorySaver`; `chat(question, thread_id)` muestra la respuesta, cómo se buscó y las páginas.
  - 3, ejemplos y chat:
    - 3.1, `EXAMPLE_CONVERSATIONS`: hilo `examples` (6 turnos, uno por tipo de pregunta, con un seguimiento que demuestra la memoria) y `new_conversation` (el mismo seguimiento sin conversación), con una celda de conclusiones.
    - 3.2, las preguntas del chat en directo de la demo (para copiar y pegar) y `chat_loop()`: chat con `input()`, un hilo `chat_N` por conversación (`nueva` / `salir`). Última celda del notebook.
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
- En `app.py`, las funciones con `st.cache_resource` llevan `show_spinner=False`: LangGraph ejecuta los nodos en otros hilos, sin acceso a la página, y el spinner de carga daba `NoSessionContext` la primera vez que un nodo creaba el modelo.
- Gemini manda la respuesta en trozos de una frase más o menos; `st.write_stream` los escribe con efecto de máquina de escribir.
- `agent.get_graph().draw_mermaid_png()` envía el grafo a mermaid.ink, un servicio externo: no se usa.
- En la transcripción, algunas descripciones de iconos son aproximadas, hay sumas con formato de fórmula (`$10+10+3+1+1$`), las viñetas salen como `[Icono: Flecha roja]` y los niveles de título (`#`, `##`) no son del todo coherentes entre páginas. La limpieza quita lo repetido; quedan erratas sueltas (p. ej. "si seis 2/3/4 jugadores" en la p. 2) e iconos dentro de algunos títulos de sección.
