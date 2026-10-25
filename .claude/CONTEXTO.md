# Qué hay en este archivo y cómo usarlo
- **Contiene:** qué es el proyecto, por qué y para qué: la idea, el usuario, cómo debe ser la experiencia, cómo se va a construir a grandes rasgos y las restricciones.
- **No contiene:** nombres de carpetas, archivos ni variables, detalles técnicos, decisiones técnicas o metodológicas ni lo pendiente.
- **Se actualiza:** solo si yo lo pido, porque cambie la idea o el diseño del producto.

## Qué es
Un asistente experto en las reglas del juego de mesa White Castle: responde preguntas sobre el manual usando RAG. Es el proyecto final del módulo de IA Generativa de mi máster de data science (Evolve); no es un proyecto mío, lo corrige el profesor.

## Por qué y para qué
- Es un ejercicio evaluado que integra lo visto en el módulo: LLMs, ingeniería de prompts, RAG, LangGraph, agentes con memoria.
- Criterios de evaluación: base de conocimiento bien indexada y documentada, recuperación precisa con respuestas coherentes con el contexto, system prompt bien diseñado y justificado, memoria funcional entre turnos, código limpio con README claro, y demo fluida explicando las decisiones técnicas. Streamlit es bonus y no penaliza su ausencia.
- Elegí el manual de White Castle porque es directamente utilizable: unas 20 páginas, el mínimo que pide el enunciado.

## El producto
- El usuario pregunta en español sobre las reglas del juego.
- El agente busca los fragmentos del manual relevantes para la pregunta y responde a partir de ellos.
- Recuerda los turnos anteriores: entiende preguntas que se apoyan en una respuesta previa.
- Rol, tono, limitaciones y qué hace cuando el manual no tiene la respuesta: se definen en el system prompt, que redacto yo.

## Experiencia de usuario
- Celda de chat dentro de un notebook, en VS Code en local.
- Lo usamos nosotros y el profesor al corregir; se enseña en una demo en vivo de 5-10 minutos.
- El notebook incluye al menos 5 preguntas de ejemplo con sus respuestas, y una que demuestra la memoria.

### Diseño visual
No aplica en la primera versión: es un notebook.

## Cómo se construye
1. Leer el manual y limpiar el texto.
2. Trocearlo y convertir cada trozo en un vector con embeddings de Gemini.
3. Guardar los vectores en una base de conocimiento vectorial (ChromaDB).
4. Grafo del agente: recibe la pregunta → recupera los trozos relevantes → genera la respuesta con Gemini.
5. Memoria de conversación sobre ese grafo.
6. Celda de chat para conversar con él.

## Restricciones
- Coste cero: modelo gratuito de Gemini.
- Plazo: una semana (fecha en "Entregas" de `ESTADO.md`).
- Repo público: la API key nunca puede llegar a él.
- El manual y las respuestas, en español.

## Fuera de la primera versión
- Interfaz web en Streamlit y despliegue público en Streamlit Cloud: se hace solo si el RAG funciona y sobra tiempo, porque es bonus y lo evaluado es el RAG.
