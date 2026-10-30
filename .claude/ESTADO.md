# Qué hay en este archivo y cómo usarlo
- **Contiene:** en qué punto estamos respecto a las fases del proyecto, por dónde empezar la próxima sesión y lo pendiente para más adelante.
- **No contiene:** cifras, detalles de lo hecho ni decisiones ya cerradas.
- **Se actualiza:** al cerrar cada sesión.

## Próxima sesión
1. Entrega, la hace Rubén: enviar el PDF del manual al profesor, adaptar `guion_demo.md` para hacer el chat en directo en la app de Streamlit y grabar la presentación. No queda código pendiente.

## Entregas
Domingo 2026-11-01:
- [x] Notebook funcional (`.ipynb`): base vectorial con ChromaDB y embeddings de Gemini, agente LangGraph con RAG y memoria, celda de chat con al menos 5 ejemplos documentados.
- [x] README: descripción del dominio, instalación y ejecución, justificación del system prompt, requisitos (dependencias, API key de Gemini).
- [ ] Presentación oral de 5-10 minutos con demo en vivo.
- (Opcional) URL pública de la app en Streamlit Cloud: no se hace, la app es solo local (ver `DECISIONES.md`).

## Fases
- [x] **Fase 0, arranque:** `.gitignore`, entorno y esqueleto mínimo que arranca.
- [x] **Fase 1, base de conocimiento:** transcribir el manual con Gemini y guardar el texto (fuera de git, como el PDF), limpiarlo, trocearlo, indexarlo en ChromaDB con embeddings de Gemini y comprobar con consultas de prueba que recupera bien.
- [x] **Fase 2, agente RAG:** system prompt (lo trae Rubén: rol, tono, limitaciones, qué hacer sin información) y grafo de LangGraph que recupera y genera. Las decisiones del prompt se anotan sobre la marcha, para el README.
- [x] **Fase 3, memoria:** el agente recuerda los turnos anteriores y reescribe las preguntas de seguimiento antes de buscar, con un ejemplo en el notebook que lo demuestra.
- [x] **Fase 4, chat y pruebas:** celda de chat y al menos 5 preguntas de ejemplo documentadas; ajustar el prompt según lo que falle y probar `gemini-3.8-flash` para la demo.
- [x] **Fase 5, entrega:** revisión del programa entero de arriba abajo contra el enunciado (`enunciado.pdf`, que hay que releer) y los ajustes que salgan; después, README completo, notebook limpio que corre de arriba abajo y guion de la demo.
- [x] **Fase 6, bonus:** chat web en Streamlit, en local, para el chat en directo de la demo, sin tocar el notebook.

## Pendiente para más adelante

### Tareas
- Al terminar el proyecto, Rubén borra `enunciado.pdf`.
- Al terminar el proyecto, recordar a Rubén que borre `.claude/` del repo (lo hace él, no Claude).

### Decisiones abiertas
Ninguna.

### Mejoras futuras
- Bucle de reintentos (*corrective RAG*): un nodo juez decide si los trozos bastan para responder y, si no, se vuelve a buscar trozos distintos, hasta 3 veces. No hizo falta en la Fase 4: en los fallos vistos, la página buena estaba entre los trozos recuperados.
- Mismo tema o tema nuevo: la clasificación falla a menudo, aunque no hace daño (ver `DECISIONES.md`). Solo se toca si empieza a hacerlo.
- Publicar el chat web en Streamlit Cloud.

### Pendiente de probar yo
Nada.
