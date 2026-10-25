# Qué hay en este archivo y cómo usarlo
- **Contiene:** las decisiones técnicas y metodológicas ya tomadas, agrupadas por área. Cada una es una pregunta con la decisión y su porqué.
- **No contiene:** decisiones abiertas ni decisiones de producto.
- **Se actualiza:** cuando se cierra una decisión abierta o se cambia una ya tomada. Para cambiar una, antes hay que hablarlo.

## Stack

### ¿Con qué tecnologías se construye?
- **Decisión:** Gemini (LLM y embeddings), ChromaDB como base vectorial, LangGraph sobre LangChain para el agente, y Jupyter.
- **Por qué:** lo impone el enunciado.

## Organización

### ¿Un solo notebook o notebook con módulos `.py`?
- **Decisión:** un solo notebook, más el README.
- **Por qué:** el entregable es un `.ipynb`; menos piezas que revisar y el profesor lo ejecuta de arriba abajo.

## Repo y datos

### ¿Repo público o privado?
- **Decisión:** público.
- **Por qué:** lo tiene que corregir el profesor.

### ¿Se sube el manual al repo?
- **Decisión:** no; `data/white_castle.pdf` va en `.gitignore`.
- **Por qué:** el repo es público y no está claro que el manual sea libre; solo lo usamos nosotros.

### ¿Cómo consigue el profesor el manual?
- **Decisión:** se lo envío yo aparte. El README indica dónde colocarlo (`data/white_castle.pdf`) (por confirmar).
- **Por qué:** el manual no está en el repo.

### ¿Se sube `enunciado.pdf`?
- **Decisión:** no; va en `.gitignore`.
- **Por qué:** decisión mía; es material de trabajo, no parte de la entrega (por confirmar).

### ¿Se sube `.claude/`?
- **Decisión:** sí, mientras dure el proyecto; al acabar se borra del repo.
- **Por qué:** así se ven en el editor los cambios desde el último commit y `HISTORICO.md` se puede commitear.

## Modelos

### ¿Qué modelos de Gemini se usan?
- **Decisión:** `gemini-3.5-flash-lite` para el chat y `gemini-embedding-2` para los embeddings, ambos gratuitos.
- **Por qué:** coste cero; Flash-Lite tiene bastante más cupo diario gratuito que Flash y le sobra calidad para las reglas de un juego.

### ¿Cómo se fija el modelo en el código?
- **Decisión:** en una variable de la celda de configuración, no repetido por el notebook.
- **Por qué:** se puede cambiar en un sitio, por ejemplo a `gemini-3.8-flash` para la demo si el cupo lo permite.

## Datos

### ¿Cómo se saca el texto del manual escaneado?
- **Decisión:** Gemini transcribe las 20 páginas (imágenes) una sola vez y el texto se guarda en un archivo, que es lo que se trocea e indexa.
- **Por qué:** el PDF no tiene texto extraíble; Gemini lee imágenes y así no hace falta instalar OCR. Se transcribe una vez para no gastar cupo en cada ejecución.

### ¿Se incluye un `.env.example`?
- **Decisión:** no, de momento; el README explica cómo crear el `.env`.
- **Por qué:** decisión mía; se revisa según lo que diga el profesor.

## Método

### ¿Quién fija los parámetros del RAG y la librería para leer el PDF?
- **Decisión:** Claude, con pruebas que lo justifiquen (tamaño de trozo, solapamiento, número de trozos recuperados).
- **Por qué:** lo delego; prefiero decidir con resultados delante.
