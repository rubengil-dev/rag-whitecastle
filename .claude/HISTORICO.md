# Qué hay en este archivo y cómo usarlo
- **Contiene:** una entrada por sesión, la más reciente arriba: fecha, qué se hizo en pocas líneas y los hashes de commit. El detalle de cada cambio está en git (`git show <hash>`).
- **No contiene:** cifras, decisiones con su porqué ni el estado actual.
- **Se actualiza:** al cerrar cada sesión, después del commit del trabajo.

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
