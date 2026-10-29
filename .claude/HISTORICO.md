# Qué hay en este archivo y cómo usarlo
- **Contiene:** una entrada por sesión, la más reciente arriba: fecha, qué se hizo en pocas líneas y los hashes de commit. El detalle de cada cambio está en git (`git show <hash>`).
- **No contiene:** cifras, decisiones con su porqué ni el estado actual.
- **Se actualiza:** al cerrar cada sesión, después del commit del trabajo.

## 2026-10-29: Revisión del notebook contra el enunciado
- Quitadas las pruebas de desarrollo (2.3 y 3.3) y el agente sin memoria: queda un solo grafo con memoria y el modelo de chat se crea una vez en el setup. Lo que enseñaron las pruebas se cuenta junto a cada decisión.
- Ejemplos nuevos en la 3.1: el seguimiento "¿Y cuántos puntos da?" demuestra la memoria, y la misma pregunta en una conversación nueva pide aclaración. Para que funcione: "puntos de clan" en el prompt de reescritura y una nota con la pregunta reescrita para `generate`.
- Porqué del system prompt en dos puntos en vez de una tabla, y celdas de texto solo con decisiones y contexto, sin explicar conceptos.
- Guion de la demo reescrito como texto hablado por secciones; preguntas del chat en directo probadas y añadidas a la 3.2.
- Trabajo en la rama `notebook-cleanup`, fusionada a `main`; el último commit, directo en `main`.
- Commits: `4289ebb` (limpieza del notebook), `b4c3fb8` (system prompt), `63bf080` (textos y preguntas del chat).

## 2026-10-28: Fases 4 y 5, chat, pruebas y entrega
- Probado `gemini-3.8-flash` en las preguntas que fallan: solo 20 llamadas al día gratis y errores `503`. Se queda `gemini-3.5-flash-lite`.
- System prompt ajustado: tipo nuevo para preguntas que no se entienden solas (solo en el primer turno), "Sí/No" solo en preguntas de sí o no y tutorial que espera a la confirmación. La primera versión pedía aclaración de más y se corrigió.
- Sección 4: conversación de ejemplo de 6 turnos, uno por tipo de pregunta, y celda de chat con `input()`. Un ejemplo que salió mal se deja documentado (decisión de Rubén).
- Fase 5: notebook re-ejecutado entero con conclusiones nuevas en 2.3, 3.3 y 4.1, limitador también en la transcripción, prueba desde cero en una carpeta limpia, README completo y guion de la demo fuera de git.
- Trabajo en la rama `phase-4-chat`, fusionada a `main`.
- Commits: `ec5c037` (Fases 4-5), `25b8db8` (`.claude/`).

## 2026-10-27: Fase 3, memoria
- Memoria por conversación con `InMemorySaver` y el nodo `rewrite` antes de buscar: clasifica cada pregunta como del mismo tema (la reescribe si hace falta, con las palabras del manual) o de tema nuevo (la deja igual y avisa a `generate`).
- Probada con tres conversaciones de 5 turnos (preguntas claras, de seguimiento y con cambios de tema), más una conversación nueva y el modo tutorial, y contrastada con el manual: la memoria aguanta y quedan dos fallos aceptados.
- Limitador de llamadas en el modelo de chat: el plan gratuito corta a 15 por minuto.
- Trabajo en la rama `phase-3-memory`, fusionada a `main`.
- Commits: `49ad851` (Fase 3), `dd96010` (`.claude/`).

## 2026-10-26: cierre de la Fase 1, notebook como relato y Fase 2
- Fase 1 cerrada: preguntas difíciles de Rubén añadidas a la comprobación de la recuperación y `RETRIEVAL_K` fijado en 5.
- Notebook reestructurado como relato: intro con mapa, porqué de cada paso, conclusiones tras cada prueba y títulos vacíos para lo pendiente. Fuera el test de humo.
- Fase 2: system prompt de Rubén ordenado y ajustado con pruebas, grafo `retrieve → generate` con LangGraph, `ask()` con las páginas recuperadas y primeras respuestas documentadas (los fallos son de razonamiento de flash-lite, no de búsqueda).
- Quitadas repeticiones del notebook: una sola lista de preguntas y cada idea contada una vez.
- Trabajo en la rama `notebook-storytelling`, fusionada a `main`.
- Commits: `7bd3813` (notebook como relato y cierre de la Fase 1), `cb73347` (Fase 2), `6a349f2` (sin repeticiones), `5983672` (`.claude/`).

## 2026-10-25: arranque del proyecto, Fase 0 y casi toda la Fase 1
- Creada la documentación de `.claude/` con `/nuevo-proyecto`, el manual movido a `data/` y el repo con `.gitattributes` y `.gitignore`.
- Repo conectado a GitHub y subido.
- Fase 0: entorno `.venv` con Python 3.11.9, `requirements.txt` con versiones fijas, API key en `.env` y notebook con test de humo de los dos modelos de Gemini.
- Fase 1: transcripción del manual escaneado con Gemini página a página, limpieza, troceado por secciones, indexado en ChromaDB y comprobación de la recuperación con 7 preguntas. Falta añadir las preguntas difíciles de Rubén.
- Commits: `e892a68` (`.gitattributes` y `.gitignore`), `3e21d13` (`.claude/` y `.gitignore` sin `.claude/`), `567288b` (nombre del repo, `rag-whitecastle`, y recordatorio de borrar `.claude/`), `b80ee6a` (Fase 0), `9b0cdda` (transcripción), `9a1b0d9` (limpieza, troceado, ChromaDB y comprobación de la recuperación).
