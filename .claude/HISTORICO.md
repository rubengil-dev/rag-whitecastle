# Qué hay en este archivo y cómo usarlo
- **Contiene:** una entrada por sesión, la más reciente arriba: fecha, qué se hizo en pocas líneas y los hashes de commit. El detalle de cada cambio está en git (`git show <hash>`).
- **No contiene:** cifras, decisiones con su porqué ni el estado actual.
- **Se actualiza:** al cerrar cada sesión, después del commit del trabajo.

## 2026-10-25: arranque del proyecto y Fase 0
- Creada la documentación de `.claude/` con `/nuevo-proyecto`, el manual movido a `data/` y el repo con `.gitattributes` y `.gitignore`.
- Repo conectado a GitHub y subido.
- Fase 0: entorno `.venv` con Python 3.11.9, `requirements.txt` con versiones fijas, API key en `.env` y notebook con test de humo de los dos modelos de Gemini.
- Commits: `e892a68` (`.gitattributes` y `.gitignore`), `3e21d13` (`.claude/` y `.gitignore` sin `.claude/`), `567288b` (nombre del repo, `rag-whitecastle`, y recordatorio de borrar `.claude/`), `b80ee6a` (Fase 0).
