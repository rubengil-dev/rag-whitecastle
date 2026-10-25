# Qué hay en este archivo y cómo usarlo
- **Contiene:** en qué punto estamos respecto a las fases del proyecto, por dónde empezar la próxima sesión y lo pendiente para más adelante.
- **No contiene:** cifras, detalles de lo hecho ni decisiones ya cerradas.
- **Se actualiza:** al cerrar cada sesión.

## Próxima sesión
1. Fase 1, cerrar la comprobación de la recuperación: Rubén trae 2-3 preguntas difíciles (preparadas con ChatGPT u otra IA) y se añaden a `TEST_QUESTIONS`. Las 7 de Claude ya recuperan bien la sección correcta en primer lugar.
2. Si alguna falla, ajustar el troceado o `RETRIEVAL_K`; si no, cerrar la Fase 1.
3. Fase 2: Rubén trae el system prompt.

## Entregas
Domingo 2026-11-01:
- [ ] Notebook funcional (`.ipynb`): base vectorial con ChromaDB y embeddings de Gemini, agente LangGraph con RAG y memoria, celda de chat con al menos 5 ejemplos documentados.
- [ ] README: descripción del dominio, instalación y ejecución, justificación del system prompt, requisitos (dependencias, API key de Gemini).
- [ ] Presentación oral de 5-10 minutos con demo en vivo.
- [ ] (Opcional) URL pública de la app en Streamlit Cloud.

## Fases
- [x] **Fase 0, arranque:** `.gitignore`, entorno y esqueleto mínimo que arranca.
- [ ] **Fase 1, base de conocimiento:** transcribir el manual con Gemini y guardar el texto (fuera de git, como el PDF), limpiarlo, trocearlo, indexarlo en ChromaDB con embeddings de Gemini y comprobar con consultas de prueba que recupera bien.
- [ ] **Fase 2, agente RAG:** system prompt (lo trae Rubén: rol, tono, limitaciones, qué hacer sin información) y grafo de LangGraph que recupera y genera. Las decisiones del prompt se anotan sobre la marcha, para el README.
- [ ] **Fase 3, memoria:** el agente recuerda los turnos anteriores, con un ejemplo en el notebook que lo demuestra.
- [ ] **Fase 4, chat y pruebas:** celda de chat y al menos 5 preguntas de ejemplo documentadas; ajustar el prompt según lo que falle.
- [ ] **Fase 5, entrega:** README completo, notebook limpio que corre de arriba abajo y guion de la demo.
- [ ] **Fase 6, bonus (condicional):** Streamlit, ver "Fuera de la primera versión" de `CONTEXTO.md`.

## Pendiente para más adelante

### Tareas
- Al terminar el proyecto, Rubén borra `enunciado.pdf`.
- Al terminar el proyecto, recordar a Rubén que borre `.claude/` del repo (lo hace él, no Claude).

### Decisiones abiertas
**Parámetros del RAG**
- Valores finales de tamaño de trozo, solapamiento y trozos recuperados por pregunta: los fija Claude tras las pruebas de la Fase 1.

### Mejoras futuras
Nada por ahora.

### Pendiente de probar yo
Nada.
