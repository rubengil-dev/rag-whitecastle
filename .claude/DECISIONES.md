# Qué hay en este archivo y cómo usarlo
- **Contiene:** las decisiones técnicas y metodológicas ya tomadas, agrupadas por área. Cada una es una pregunta con la decisión y su porqué.
- **No contiene:** decisiones abiertas ni decisiones de producto.
- **Se actualiza:** cuando se cierra una decisión abierta o se cambia una ya tomada. Para cambiar una, antes hay que hablarlo.

## Stack

### ¿Con qué tecnologías se construye?
- **Decisión:** Gemini (LLM y embeddings), ChromaDB como base vectorial, LangGraph sobre LangChain para el agente, y Jupyter.
- **Por qué:** lo impone el enunciado.

### ¿Versiones de las dependencias fijas o libres?
- **Decisión:** fijas (`==`) en `requirements.txt`, solo las librerías que usamos directamente; todo el stack se instaló en la Fase 0.
- **Por qué:** al profesor se le instala exactamente lo que hemos probado, y las incompatibilidades salen al principio y no a mitad de proyecto.

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
- **Decisión:** Gemini transcribe cada página por separado (su imagen JPEG, sacada con `pypdf`) y cada una se guarda en su archivo Markdown. Las páginas ya transcritas se saltan.
- **Por qué:** el PDF no tiene texto extraíble y Gemini lee imágenes, así que no hace falta OCR. Página a página porque con el PDF entero el modelo tiende a resumir y se pierde la página de cada trozo; si una falla, solo se repite esa. Se transcribe una vez para no gastar cupo.

### ¿Qué se hace con iconos e ilustraciones?
- **Decisión:** se describen brevemente entre corchetes los que aportan reglas (`[Icono: 2 monedas]`); los decorativos se ignoran.
- **Por qué:** en un manual de juego muchas reglas (costes, recompensas) están solo en iconos.

### ¿Cómo se trocea el texto?
- **Decisión:** primero por títulos de sección, para no partir una regla; las secciones largas se subdividen por tamaño con solapamiento. Cada trozo guarda su página y su sección. Los valores (tamaño, solapamiento, trozos recuperados) se ajustan con pruebas; se parte de 1000 caracteres y 150 de solapamiento.
- **Por qué:** las reglas del manual van por secciones; la página y la sección permiten saber de dónde sale cada respuesta.

### ¿Cada trozo lleva el título de su sección en el texto?
- **Decisión:** sí; el trozo empieza con la ruta de títulos (`PREPARACIÓN DE LA PARTIDA > PUENTES`), además de llevarla en los metadatos.
- **Por qué:** el embedding solo ve el texto; un trozo suelto como "Se colocan los puentes…" sin su sección pierde contexto al buscar.

### ¿Cómo se limpia la transcripción?
- **Decisión:** reglas de expresiones regulares en una tabla (`CLEANING_RULES`): marcas de fórmula, viñetas de flecha, signo de exclamación e ilustraciones decorativas. No se corrigen erratas sueltas.
- **Por qué:** es el ruido que se repite; corregir erratas a mano no compensa para el RAG.

### ¿La base vectorial se recalcula en cada ejecución?
- **Decisión:** no; se guarda en local y, si ya existe, se carga. Para reconstruirla tras cambiar la limpieza o el troceado, se pone `REBUILD_VECTOR_STORE = True` una vez.
- **Por qué:** no gastar cupo de embeddings en cada ejecución. El interruptor es explícito porque la base no sabe sola si los trozos han cambiado.

### ¿Cómo se valida la recuperación y las respuestas?
- **Decisión:** Claude propone 5 preguntas de prueba sacadas del manual y Rubén añade 2-3 difíciles. Las respuestas se contrastan con ChatGPT u otra IA.
- **Por qué:** ni Rubén ni Claude conocen el juego lo bastante para validarlo de memoria.

### ¿Reranking, búsqueda híbrida o métricas de calidad?
- **Decisión:** no en la primera versión.
- **Por qué:** el enunciado no lo pide; solo se plantea si la recuperación sale floja.

### ¿Se incluye un `.env.example`?
- **Decisión:** no, de momento; el README explica cómo crear el `.env`.
- **Por qué:** decisión mía; se revisa según lo que diga el profesor.

## Método

### ¿Quién fija los parámetros del RAG y la librería para leer el PDF?
- **Decisión:** Claude, con pruebas que lo justifiquen (tamaño de trozo, solapamiento, número de trozos recuperados).
- **Por qué:** lo delego; prefiero decidir con resultados delante.
