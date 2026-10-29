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

### ¿Cómo se organiza el notebook?
- **Decisión:** como un relato, no como una batería de pruebas: intro con el mapa de secciones; cada sección empieza con el porqué de lo que hace; cada prueba termina con una celda de conclusiones. Cada idea se cuenta una sola vez, donde se descubre, y el resto de sitios remiten a ella. Solo se quedan las pruebas que pide el enunciado: la comprobación de la recuperación (1.4) y los ejemplos (3.1). Las pruebas de desarrollo (el agente sin memoria y las conversaciones de memoria) se quitaron, y lo que enseñaron se cuenta junto a cada decisión, diciendo que viene de ellas. Las celdas de texto solo llevan decisiones con su porqué y contexto: nada que explique conceptos que el profesor ya conoce por su enunciado (qué es un RAG, un grafo de LangGraph, un embedding o un checkpointer) ni analogías.
- **Por qué:** lo evalúa el profesor y se enseña en la demo; el porqué de cada decisión es parte de lo evaluado. Las pruebas de desarrollo repetían preguntas y alargaban la ejecución (unas 50 llamadas a Gemini en vez de unas 13). El porqué se queda en el notebook aunque también esté en el README, porque el notebook es lo que lee el profesor. Las explicaciones de conceptos eran para Rubén, no para el profesor (decisiones de Rubén).

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

### ¿Se sube el guion de la demo?
- **Decisión:** no; `guion_demo.md` va en `.gitignore` (por confirmar).
- **Por qué:** es material de Rubén para la presentación, no parte de la entrega.

### ¿Se sube `.claude/`?
- **Decisión:** sí, mientras dure el proyecto; al acabar se borra del repo.
- **Por qué:** así se ven en el editor los cambios desde el último commit y `HISTORICO.md` se puede commitear.

## Modelos

### ¿Qué modelos de Gemini se usan?
- **Decisión:** `gemini-3.5-flash-lite` para el chat y `gemini-embedding-2` para los embeddings, ambos gratuitos.
- **Por qué:** coste cero; Flash-Lite tiene bastante más cupo diario gratuito que Flash y le sobra calidad para las reglas de un juego.

### ¿Se usa un modelo mayor para la demo?
- **Decisión:** no; la demo usa `gemini-3.5-flash-lite`.
- **Por qué:** en la Fase 4 se probó `gemini-3.8-flash` con las preguntas que fallan. Su plan gratuito permite solo 20 llamadas al día (cada turno gasta dos) y sus primeras llamadas dieron `503`. La única respuesta que dio era correcta, pero Flash-Lite, con el prompt ajustado, también acierta esa pregunta casi siempre.

### ¿Cómo se fija el modelo en el código?
- **Decisión:** en una variable de la celda de configuración, no repetido por el notebook. El modelo de chat (`llm`) se crea una sola vez en el setup y lo comparten la transcripción y el agente. El porqué del modelo se explica en la sección 0 del notebook y en el README.
- **Por qué:** se puede cambiar en un sitio, y el limitador de llamadas se explica una sola vez.

## Datos

### ¿Cómo se saca el texto del manual escaneado?
- **Decisión:** Gemini transcribe cada página por separado (su imagen JPEG, sacada con `pypdf`) y cada una se guarda en su archivo Markdown. Las páginas ya transcritas se saltan.
- **Por qué:** el PDF no tiene texto extraíble y Gemini lee imágenes, así que no hace falta OCR. Página a página porque con el PDF entero el modelo tiende a resumir y se pierde la página de cada trozo; si una falla, solo se repite esa. Se transcribe una vez para no gastar cupo.

### ¿Qué se hace con iconos e ilustraciones?
- **Decisión:** se describen brevemente entre corchetes los que aportan reglas (`[Icono: 2 monedas]`); los decorativos se ignoran.
- **Por qué:** en un manual de juego muchas reglas (costes, recompensas) están solo en iconos.

### ¿Cómo se trocea el texto?
- **Decisión:** primero por títulos de sección, para no partir una regla; las secciones largas se subdividen en trozos de 1000 caracteres con 150 de solapamiento. Cada trozo guarda su página y su sección.
- **Por qué:** las reglas del manual van por secciones; la página y la sección permiten saber de dónde sale cada respuesta. Con esos valores, todas las preguntas de prueba encuentran su página, así que no se han tocado.

### ¿Cuántos trozos se recuperan por pregunta?
- **Decisión:** 5 (`RETRIEVAL_K`).
- **Por qué:** con 3, la versión larga de la pregunta del dado pierde uno de sus dos trozos clave (el orden de los pasos); con 5 los conserva todas las preguntas, y 5 trozos siguen siendo un contexto pequeño para Gemini.

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
- **Decisión:** 7 preguntas directas de Claude y 3 difíciles de Rubén, más versiones largas de dos de ellas. La recuperación se da por buena si sale un trozo de la página esperada entre los recuperados. Las respuestas se contrastan con las soluciones de Rubén (preparadas con ChatGPT u otra IA) y con el texto del manual.
- **Por qué:** ni Rubén ni Claude conocen el juego lo bastante para validarlo de memoria. Las soluciones de otra IA también son deducciones, así que, si chocan con la respuesta del agente, manda lo que diga el manual.

### ¿Reranking, búsqueda híbrida o métricas de calidad?
- **Decisión:** no en la primera versión.
- **Por qué:** el enunciado no lo pide; solo se plantea si la recuperación sale floja.

### ¿Se incluye un `.env.example`?
- **Decisión:** no, de momento; el README explica cómo crear el `.env`.
- **Por qué:** decisión mía; se revisa según lo que diga el profesor.

## Agente

### ¿Cómo es el system prompt?
- **Decisión:** el contenido lo define Rubén y Claude lo ordena. Está escrito en inglés y responde siempre en español. Solo responde con los trozos recuperados. Primero decide el tipo de pregunta (regla con respuesta, pregunta que no se entiende sola, regla sin respuesta, aprender a jugar, fuera de tema) y aplica el formato de ese tipo. Si no encuentra la regla, empieza con "No encuentro esta regla en el manual" y propone una regla de la casa, sin citar página. Fuera de tema, responde con una frase fija. Su porqué se explica en dos puntos (rol y tono; qué responde y con qué), igual en la sección 2.1 del notebook y en el README, sin tabla regla a regla, que quedaba como un registro de parches (decisión de Rubén).
- **Por qué:** los modelos siguen mejor las instrucciones en inglés, pero la demo es en español. El agente no puede distinguir un hueco del manual de una búsqueda fallida, así que la frase vale para los dos casos. El orden por tipos y la frase fija salieron de las pruebas: sin ellos, el modelo citaba páginas donde no tocaba.

### ¿Cómo se ajustó el prompt en la Fase 4?
- **Decisión:** tres cambios:
    - El tipo "pregunta que no se entiende sola" pide al jugador que concrete, solo en el primer turno de una conversación (idea de Rubén).
    - "Sí" o "No" solo en preguntas de sí o no, nombrando las palabras de pregunta ("qué", "cuánto"…) que nunca empiezan así; las tres partes de la respuesta no se numeran.
    - La primera respuesta del tutorial es solo la lista de pasos.
- **Por qué:** sin el primer cambio, el agente se inventaba a qué se refería "lo"; sin limitarlo al primer turno, pedía aclaración incluso cuando la conversación lo dejaba claro. Una regla general sobre "Sí" no bastaba. Sin el tercer cambio, el tutorial explicaba el primer paso sin esperar.

### ¿Cómo es el grafo?
- **Decisión:** un solo grafo, `START → rewrite → retrieve → generate → END`, compilado con el checkpointer. El estado lleva la conversación (`messages`), el tipo de pregunta, la pregunta que se busca y los trozos recuperados. Cada trozo llega a Gemini con la cabecera `[Página N]`. `chat()` muestra la respuesta y debajo cómo se buscó y las páginas de los trozos recuperados.
- **Por qué:** el grafo sin memoria (`retrieve → generate`) solo lo usaban las pruebas de desarrollo; con los dos había cinco parejas de piezas casi iguales. La cabecera permite citar la página. Ver las páginas recuperadas hace visible el RAG en la demo y ayuda a distinguir un fallo de búsqueda de uno de razonamiento.

### ¿Se dibuja el grafo con LangGraph?
- **Decisión:** no; el esquema se escribe a mano en una celda Markdown.
- **Por qué:** LangGraph lo dibuja enviando el grafo a un servicio web externo (mermaid.ink); para tres nodos en línea no compensa depender de él.

### ¿Se corrigen con el prompt los fallos de razonamiento?
- **Decisión:** no; los vistos en las pruebas se resumen en las conclusiones de la 3.1 y en "Known limitations" del README. El modelo mayor se probó en la Fase 4 y se descartó (ver "Modelos").
- **Por qué:** los fallos vienen de razonar mal con los trozos correctos delante, no de la búsqueda. `gemini-3.5-flash-lite` cambia de respuesta entre ejecuciones, así que ajustar el prompt a una pregunta concreta no garantiza nada.

### ¿Bucle de reintentos que vuelva a buscar si no puede responder?
- **Decisión:** no por ahora; queda en "Mejoras futuras" de `ESTADO.md`.
- **Por qué:** en los fallos vistos, los trozos correctos ya estaban recuperados, así que no los arreglaría. Además, tras 3 vueltas solo se habría leído una parte pequeña del manual (no permite afirmar "no viene, seguro"), el juez sería el mismo modelo poco fiable y cada pregunta pasaría a gastar de 2 a 4 llamadas.

### ¿Cómo son la celda de chat y los ejemplos?
- **Decisión:** la 3.1 tiene dos conversaciones. `examples` tiene 6 turnos que cubren los tipos de pregunta del system prompt; el segundo, "¿Y cuántos puntos da?", es una pregunta de seguimiento que demuestra la memoria (idea de Rubén: la respuesta depende del piso del que parte el cortesano). `new_conversation` hace esa misma pregunta sin conversación detrás, y el agente pide que concrete. La 3.2 es un bucle con `input()` que usa `chat()`: `nueva` empieza otra conversación y `salir` o una línea vacía terminan. Es la última celda del notebook.
- **Por qué:** el enunciado pide 5 ejemplos documentados y uno que demuestre la memoria con "una pregunta que hace referencia a una respuesta anterior"; la versión anterior lo demostraba con una respuesta del jugador a una aclaración, no con una pregunta. El chat va al final para que "Run All" no se quede esperando a mitad.

### ¿Qué se hace si un ejemplo documentado sale mal?
- **Decisión:** se corrige (decisión de Rubén, que cambia la anterior de dejarlo como saliera). Si el fallo tiene una causa general (por ejemplo, una palabra del jugador que no está en el manual), se arregla esa causa; si es solo la variabilidad del modelo, se vuelve a ejecutar y las conclusiones dicen que esa pregunta varía. Una respuesta incompleta pero no incorrecta se deja y se explica (la de los puntos del cortesano).
- **Por qué:** los ejemplos de la 3.1 son lo único que ve el profesor del agente respondiendo; un fallo entre 7 respuestas pesa mucho más que entre las 30 de antes.

## Memoria

### ¿Dónde se guarda la conversación?
- **Decisión:** en memoria, con el checkpointer `InMemorySaver` de LangGraph, una conversación por `thread_id`. Se pierde al reiniciar el kernel.
- **Por qué:** la demo y la corrección van en una sola ejecución del notebook. Guardarla en un archivo (SQLite) añadiría una dependencia que nadie necesita.

### ¿Cómo se buscan las preguntas de seguimiento?
- **Decisión:** un nodo `rewrite` antes de `retrieve`. Desde el segundo turno, Gemini clasifica la pregunta en `same_topic` (se reescribe para que se entienda sola, o se deja igual si ya se entiende) o `new_topic` (se deja igual). La respuesta llega como un diccionario estructurado (tipo y pregunta). La pregunta reescrita se usa para buscar y, si cambió, le llega a `generate` como nota (`FOLLOW_UP_NOTE`: "por sí sola, significa…"); `generate` sigue respondiendo a las palabras del jugador. En el primer turno no se llama a Gemini.
- **Por qué:** una pregunta como "¿y si somos dos?" no encuentra nada en la base. Solo reescribir arrastraba el tema anterior a preguntas claras. Con tres tipos (seguimiento, mismo tema clara y tema nuevo), confundía los dos primeros y buscaba "las dos cosas" tal cual. Con dos, si duda, como mucho reescribe de más, que no hace daño. La nota se añadió al rehacer los ejemplos: sin ella, "¿Y cuántos puntos da?" tras el coste de subir un cortesano se respondía pidiendo aclaración en 4 de 6 ejecuciones, con la conversación delante; con ella, se respondió en 4 de 4. La pregunta del jugador no se sustituye porque la reescritura a veces pierde un detalle.

### ¿Qué se hace cuando el jugador cambia de tema?
- **Decisión:** la pregunta se busca tal cual y a `generate` le llega una nota ("the player has changed topic") delante de la pregunta. No se le pasa un resumen de lo anterior.
- **Por qué:** idea de Rubén, con un ajuste de Claude: la nota va a `generate` y no a la búsqueda, porque las palabras del tema anterior en la pregunta buscada traerían trozos de ese tema. El resumen sobra porque `generate` ya ve toda la conversación.

### ¿Con qué palabras se reescribe?
- **Decisión:** con las que usó el asistente en la conversación, que vienen del manual, en vez de las informales del jugador ("la sala del Daimio", no "arriba del todo"). Los puntos se nombran "puntos de clan", como en el manual. Los pasos del modo tutorial se nombran por su contenido, no por su número.
- **Por qué:** en las pruebas, con las palabras del jugador o con "el segundo paso", la búsqueda no encontraba la página buena. Con "¿Y cuántos puntos da?" tras el coste de subir un cortesano, la búsqueda con "puntos" traía la acción del cortesano y no la puntuación de la página 14; con "puntos de clan", la página 14 sale la primera.

### ¿Se arreglan los fallos que quedan en las pruebas de memoria?
- **Decisión:** no. Se aceptan como limitaciones conocidas y quedan resumidos en las conclusiones de la 3.1 y en el README: la reescritura inestable (en cada ejecución falla una pregunta de seguimiento distinta) y la excepción de los jardineros en la última ronda, que está en un trozo que no se recupera.
- **Por qué:** decisión de Rubén. Acertar unas 4 de cada 5 es suficiente para un modelo tan pequeño y un proyecto de este tamaño, y un jugador que recibe una respuesta floja vuelve a preguntar con más contexto. Si `gemini-3.8-flash` los arregla en la Fase 4, mejor, pero no se busca a propósito.

### ¿Cómo se respeta el límite de llamadas del plan gratuito?
- **Decisión:** el modelo de chat y el de la transcripción espacian sus llamadas con `InMemoryRateLimiter` a `CHAT_REQUESTS_PER_SECOND = 0.2` (12 por minuto).
- **Por qué:** el plan gratuito de `gemini-3.5-flash-lite` permite 15 llamadas por minuto, y el notebook entero hace más de 30 seguidas: sin el limitador, la ejecución se cortaba con un error 429.

## Método

### ¿Quién fija los parámetros del RAG y la librería para leer el PDF?
- **Decisión:** Claude, con pruebas que lo justifiquen (tamaño de trozo, solapamiento, número de trozos recuperados).
- **Por qué:** lo delego; prefiero decidir con resultados delante.

### ¿Cómo se escriben las conclusiones de las pruebas del agente?
- **Decisión:** a partir de las salidas guardadas en el notebook. Si se vuelve a ejecutar una sección con respuestas del modelo, sus conclusiones se revisan.
- **Por qué:** el modelo de chat da respuestas distintas en cada ejecución, y las conclusiones tienen que cuadrar con lo que se ve.
