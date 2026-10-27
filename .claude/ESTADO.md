# Qué hay en este archivo y cómo usarlo
- **Contiene:** en qué punto estamos respecto a las fases del proyecto, por dónde empezar la próxima sesión y lo pendiente para más adelante.
- **No contiene:** cifras, detalles de lo hecho ni decisiones ya cerradas.
- **Se actualiza:** al cerrar cada sesión.

## Próxima sesión
1. Fase 4, hablar antes de tocar nada: la celda de chat, las preguntas de ejemplo de la sección 4, los ajustes del prompt de "Pendiente para la Fase 4" y la prueba de `gemini-3.8-flash`.
2. Implementarlo. Con la Fase 4 se acaba el desarrollo; lo siguiente es la revisión completa de la Fase 5.

## Entregas
Domingo 2026-11-01:
- [ ] Notebook funcional (`.ipynb`): base vectorial con ChromaDB y embeddings de Gemini, agente LangGraph con RAG y memoria, celda de chat con al menos 5 ejemplos documentados.
- [ ] README: descripción del dominio, instalación y ejecución, justificación del system prompt, requisitos (dependencias, API key de Gemini).
- [ ] Presentación oral de 5-10 minutos con demo en vivo.
- [ ] (Opcional) URL pública de la app en Streamlit Cloud.

## Fases
- [x] **Fase 0, arranque:** `.gitignore`, entorno y esqueleto mínimo que arranca.
- [x] **Fase 1, base de conocimiento:** transcribir el manual con Gemini y guardar el texto (fuera de git, como el PDF), limpiarlo, trocearlo, indexarlo en ChromaDB con embeddings de Gemini y comprobar con consultas de prueba que recupera bien.
- [x] **Fase 2, agente RAG:** system prompt (lo trae Rubén: rol, tono, limitaciones, qué hacer sin información) y grafo de LangGraph que recupera y genera. Las decisiones del prompt se anotan sobre la marcha, para el README.
- [x] **Fase 3, memoria:** el agente recuerda los turnos anteriores y reescribe las preguntas de seguimiento antes de buscar, con un ejemplo en el notebook que lo demuestra.
- [ ] **Fase 4, chat y pruebas:** celda de chat y al menos 5 preguntas de ejemplo documentadas; ajustar el prompt según lo que falle y probar `gemini-3.8-flash` para la demo.
- [ ] **Fase 5, entrega:** revisión del programa entero de arriba abajo contra el enunciado (`enunciado.pdf`, que hay que releer) y los ajustes que salgan; después, README completo, notebook limpio que corre de arriba abajo y guion de la demo.
- [ ] **Fase 6, bonus (condicional):** Streamlit, solo si sobra tiempo tras la Fase 5. Ver "Fuera de la primera versión" de `CONTEXTO.md`.

## Pendiente para más adelante

### Tareas
- Al terminar el proyecto, Rubén borra `enunciado.pdf`.
- Al terminar el proyecto, recordar a Rubén que borre `.claude/` del repo (lo hace él, no Claude).

### Decisiones abiertas
**Modelo de chat para la demo**
- `gemini-3.5-flash-lite` o uno mayor (`gemini-3.8-flash`): se decide en la Fase 4, tras probar si el mayor razona mejor las preguntas con trampa y si su cupo y su disponibilidad aguantan una demo en vivo.

### Pendiente para la Fase 4
Lo que dejaron las pruebas de memoria de la sección 3.3; el detalle, en sus conclusiones.
- **Preguntas vagas:** sin contexto ("¿y luego cómo lo subo?" en una conversación nueva), el agente se inventa a qué se refiere en vez de preguntar. Idea de Rubén: un tipo más en el system prompt que pida contexto.
- **Formato:** empieza con "Sí" preguntas que no son de sí o no, y el modo tutorial numera las tres partes de la respuesta en vez de los pasos.
- **Mismo tema o tema nuevo:** la clasificación falla a menudo, aunque hoy no hace daño (ver `DECISIONES.md`). Solo se toca si empieza a hacerlo.

### Mejoras futuras
- Bucle de reintentos (*corrective RAG*): un nodo juez decide si los trozos bastan para responder y, si no, se vuelve a buscar trozos distintos, hasta 3 veces. Solo si en la Fase 4 aparecen fallos en los que la página buena no estaba entre los trozos recuperados.

### Pendiente de probar yo
Nada.
