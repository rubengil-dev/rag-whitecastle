"""
Streamlit chat for the White Castle rules agent:
    - Copy of the notebook's agent (sections 0, 1.3 and 2): it loads chroma_db/, it does not build it
    - Answers streamed word by word, with how the question was searched and the retrieved pages
    - Run: streamlit run app.py
"""

# Imports
import os
from itertools import chain
from pathlib import Path
from traceback import print_exc
from typing import Annotated, Literal, TypedDict
from uuid import uuid4
import streamlit as st
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

# Paths
PROJECT_DIR = Path(__file__).parent
ENV_PATH = PROJECT_DIR / ".env"
CHROMA_DIR = PROJECT_DIR / "chroma_db"
ASSETS_DIR = PROJECT_DIR / "assets"

# Models
CHAT_MODEL = "gemini-3.5-flash-lite"
EMBEDDING_MODEL = "gemini-embedding-2"
CHAT_REQUESTS_PER_SECOND = 0.2  # 12 q/min (free tier allows 15q/min)

# Vector store
COLLECTION_NAME = "white_castle_rules"
RETRIEVAL_K = 5

# Prompts (copied from the notebook, sections 2.1 and 2.2)
SYSTEM_PROMPT = """You are an expert on the rules of the board game White Castle. You help players during a game, so your answers are short and clear. Always answer in Spanish.

You answer only from the rulebook excerpts given with each question. Each excerpt shows its page and section. Never invent a rule or answer from general knowledge of the game.

First decide which of these five kinds of question it is, and answer only as its section says.

# 1. Rules question answered by the excerpts
Answer in three parts, written as plain text, without numbering or labelling them:
- Short answer, in the first sentence. Start with "Sí" or "No" only when the question asks whether something can be done or is true ("¿Puedo...?", "¿Se puede...?", "¿Es...?"). Questions with "qué", "cuánto", "cuándo", "cómo" or "cuál" never start with "Sí" or "No": start with the answer itself (a number, a cost, a moment of the game...).
- Explanation: one short paragraph with the details and the reasoning, so the player understands why.
- Source: the pages of the excerpts you used, for example "Lo tienes en la página 5."

Read quantities and limits literally (once, each, at most, only one): they are often the key to the answer. If the answer is not written literally but follows from the excerpts (for example, from the order of the steps), deduce it and explain the reasoning in the paragraph.

# 2. Question that cannot be understood on its own
Only for the first question of a conversation, when there are no earlier turns: it refers to something that was never said ("eso", "lo", "y luego", "en ese caso"). Do not guess what it means: ask the player, in one or two sentences, which rule or part of the game they mean. No page.
If there are earlier turns, the references point to them: never ask, answer with the kind that fits.

# 3. Rules question the excerpts do not answer
1. Start with "No encuentro esta regla en el manual" and say briefly that the rulebook may leave it open, or the search may not have found it. Never present an assumption as an official rule.
2. Propose a house rule for this game, clearly labelled as a suggestion, not an official rule.
Do not add a "Lo tienes en la página..." line: no page has the rule.

# 4. Learning to play
For broad questions, such as "enséñame a jugar", "cómo se prepara la partida" or "cómo se juega":
1. List the main steps as a short numbered stepper, one line per step.
2. Ask if the player is ready for the first step. This first answer has only the list and the question: do not explain any step yet.
3. Explain one step at a time: a short paragraph with its page, not the three parts of kind 1. Move to the next step only when the player confirms.
Never explain all the steps at once.

# 5. Not about White Castle
Reply only with "Solo puedo ayudarte con las reglas de White Castle.", with no explanation and no page."""

REWRITE_PROMPT = """You prepare the last question of a conversation about the rules of the board game White Castle for a search in the rulebook. Classify it into one of two kinds and return the question to search, in Spanish:
- "same_topic": it continues the topic of the earlier turns. If it depends on them (for example "y si...", "en ese caso", "eso", "lo", "las dos cosas", "arriba del todo", "sí", "siguiente"), rewrite it so that it can be understood on its own, replacing the references with what they refer to. If it can already be understood on its own, return it unchanged. If the player only confirms or asks to go on, write a question about the step the assistant offered to explain next, named by its content, not by its number.
- "new_topic": it can be understood on its own and is about a different topic. Return it unchanged, without adding anything from the earlier turns.
When you rewrite, use the words the assistant used in the conversation (they come from the rulebook) instead of the player's informal ones: for example "la sala del Daimio" instead of "arriba del todo". The rulebook calls points "puntos de clan": use that name when the player asks about points."""

TOPIC_CHANGE_NOTE = "Note: the player has changed topic. The earlier turns are about other rules: answer this question on its own."
FOLLOW_UP_NOTE = "Note: this question continues the conversation. On its own, it means: {question}"

# Interface
WELCOME_MESSAGE = (
    "Bienvenido al castillo. Soy tu experto en las reglas de **White Castle**: pregúntame cualquier duda "
    "del manual (costes, acciones, puntuación…) o pídeme que te enseñe a jugar paso a paso. "
    "Te diré en qué página lo tienes."
)
THINKING_MESSAGE = "Consultando el manual…"
INPUT_PLACEHOLDER = "Pregunta una regla de White Castle"
AVATARS = {"assistant": str(ASSETS_DIR / "robot.svg"), "user": str(ASSETS_DIR / "farmer.svg")}
SEARCH_KIND_LABELS = {
    "first_turn": "Primera pregunta",
    "same_topic": "Mismo tema",
    "new_topic":  "Tema nuevo",
}
BUSY_ERROR_MARKERS = ("429", "RESOURCE_EXHAUSTED", "503", "UNAVAILABLE")
BUSY_ERROR_MESSAGE = "⚠️ Gemini está saturado ahora mismo (demasiadas preguntas seguidas o servidores ocupados). Espera un momento y vuelve a preguntar."
OTHER_ERROR_MESSAGE = "⚠️ Algo ha fallado al consultar a Gemini. Vuelve a preguntar; si se repite, mira el error en la terminal donde arrancaste la app."
MISSING_KEY_MESSAGE = f"Falta la API key de Gemini: crea el archivo {ENV_PATH.name} con GOOGLE_API_KEY, como explica el README."
MISSING_STORE_MESSAGE = f"No encuentro la base vectorial en {CHROMA_DIR.name}/: ejecuta antes el notebook de arriba abajo para crearla."

# Page style
HEADER_HTML = """
<div class="wc-header">
    <div class="wc-seal">城</div>
    <div>
        <div class="wc-title">White Castle</div>
        <div class="wc-subtitle">Asistente de reglas · 白鷺城</div>
    </div>
</div>
<div class="wc-waves"></div>
"""
WAVE = "#9AA6B8"
PAPER = "#F6F0E1"
PAGE_STYLE = f"""
<style>
.wc-header {{ display: flex; align-items: center; gap: 1rem; margin-top: 0.5rem; }}
.wc-seal {{
    background: #B23A2E; color: {PAPER}; font-family: 'Shippori Mincho', serif; font-size: 2rem; font-weight: 800;
    width: 3.4rem; height: 3.4rem; display: flex; align-items: center; justify-content: center;
    border-radius: 0.35rem; transform: rotate(-4deg); box-shadow: inset 0 0 0 3px {PAPER}, inset 0 0 0 4px #B23A2E;
}}
.wc-title {{ font-family: 'Shippori Mincho', serif; font-size: 2.3rem; font-weight: 800; line-height: 1.1; color: #2B2522; }}
.wc-subtitle {{ font-family: 'Shippori Mincho', serif; font-size: 1rem; color: #7A6A58; letter-spacing: 0.05em; }}
.wc-waves {{
    height: 38px; margin: 0.8rem 0 1.4rem;
    background-color: {PAPER};
    background-image:
        radial-gradient(circle at 100% 150%, {PAPER} 24%, {WAVE} 24%, {WAVE} 28%, {PAPER} 28%, {PAPER} 36%, {WAVE} 36%, {WAVE} 40%, transparent 40%, transparent),
        radial-gradient(circle at 0 150%, {PAPER} 24%, {WAVE} 24%, {WAVE} 28%, {PAPER} 28%, {PAPER} 36%, {WAVE} 36%, {WAVE} 40%, transparent 40%, transparent),
        radial-gradient(circle at 50% 100%, {WAVE} 10%, {PAPER} 10%, {PAPER} 23%, {WAVE} 23%, {WAVE} 30%, {PAPER} 30%, {PAPER} 43%, {WAVE} 43%, {WAVE} 50%, {PAPER} 50%, {PAPER} 63%, {WAVE} 63%, {WAVE} 71%, transparent 71%, transparent),
        radial-gradient(circle at 100% 50%, {WAVE} 5%, {PAPER} 5%, {PAPER} 15%, {WAVE} 15%, {WAVE} 20%, {PAPER} 20%, {PAPER} 29%, {WAVE} 29%, {WAVE} 34%, {PAPER} 34%, {PAPER} 44%, {WAVE} 44%, {WAVE} 49%, transparent 49%, transparent),
        radial-gradient(circle at 0 50%, {WAVE} 5%, {PAPER} 5%, {PAPER} 15%, {WAVE} 15%, {WAVE} 20%, {PAPER} 20%, {PAPER} 29%, {WAVE} 29%, {WAVE} 34%, {PAPER} 34%, {PAPER} 44%, {WAVE} 44%, {WAVE} 49%, transparent 49%, transparent);
    background-size: 50px 25px;
    mask-image: linear-gradient(to right, transparent, black 15%, black 85%, transparent);
}}
[data-testid="stChatMessage"] {{
    background: #FBF7EE; border: 1px solid #DCCFB4; border-left: 3px solid #B23A2E; border-radius: 0.4rem; padding: 0.9rem 1rem;
}}
</style>
"""


def main():
    """Page → setup check → sidebar → saved conversation → new question, answered word by word."""
    st.set_page_config(page_title="White Castle · Reglas", page_icon="🏯")
    st.markdown(PAGE_STYLE, unsafe_allow_html=True)
    st.markdown(HEADER_HTML, unsafe_allow_html=True)
    check_setup()
    start_session()
    show_sidebar()
    show_conversation()
    question = st.chat_input(INPUT_PLACEHOLDER)
    if question:
        answer_question(question)


def check_setup():
    """API key in .env and vector store on disk, or an error on the page and stop."""
    load_dotenv(ENV_PATH)
    if not os.getenv("GOOGLE_API_KEY"):
        st.error(MISSING_KEY_MESSAGE)
        st.stop()
    if not (CHROMA_DIR / "chroma.sqlite3").exists():
        st.error(MISSING_STORE_MESSAGE)
        st.stop()


def start_session():
    """First run of the browser session → a new conversation."""
    if "thread_id" not in st.session_state:
        start_new_conversation()


def start_new_conversation():
    """New thread id and no messages: the agent starts a conversation from scratch."""
    st.session_state.thread_id = str(uuid4())
    st.session_state.messages = []


def show_sidebar():
    """Sidebar menu with the 'Nueva conversación' button."""
    with st.sidebar:
        st.markdown("### Menú")
        st.button("Nueva conversación", on_click=start_new_conversation, type="primary", width="stretch")
        st.caption("El asistente olvida la conversación actual y empieza de cero.")


def show_conversation():
    """Welcome message + every message of the current conversation."""
    show_message("assistant", WELCOME_MESSAGE)
    for message in st.session_state.messages:
        show_message(message["role"], message["content"], message["caption"])


def show_message(role, content, caption=None):
    """One chat bubble with its avatar, and the search caption below the answer if there is one."""
    with st.chat_message(role, avatar=AVATARS[role]):
        st.markdown(content)
        if caption:
            st.caption(caption)


def answer_question(question):
    """
    Question → bubble, answer streamed word by word and saved with its caption:
        - If Gemini fails, a friendly message instead of the answer
    """
    show_message("user", question)
    save_message("user", question)
    with st.chat_message("assistant", avatar=AVATARS["assistant"]):
        try:
            answer = stream_answer(question)
        except Exception as error:
            print_exc()
            message = describe_error(error)
            st.markdown(message)
            save_message("assistant", message)
            return
        caption = describe_search(question, get_agent().get_state(thread_config()).values)
        st.caption(caption)
    save_message("assistant", answer, caption)


def save_message(role, content, caption=None):
    """Message → session history, so it is shown again on every rerun."""
    st.session_state.messages.append({"role": role, "content": content, "caption": caption})


def stream_answer(question):
    """Agent turn → spinner until the first word, then the answer written word by word."""
    tokens = answer_tokens(question)
    with st.spinner(THINKING_MESSAGE):
        first_token = next(tokens, "")
    return st.write_stream(chain([first_token], tokens))


def answer_tokens(question):
    """Agent turn → pieces of the generate node's answer, as Gemini writes them."""
    updates = get_agent().stream({"messages": [HumanMessage(question)]}, thread_config(), stream_mode="messages")
    for chunk, metadata in updates:
        if metadata["langgraph_node"] == "generate" and chunk.text:
            yield chunk.text


def thread_config():
    """LangGraph config of the current conversation."""
    return {"configurable": {"thread_id": st.session_state.thread_id}}


def describe_search(question, state):
    """
    How the question was searched and the pages retrieved:
        Example: 'Mismo tema → buscada como «¿Cómo sube un cortesano de piso?» · Páginas recuperadas: 9, 14'
    """
    search = SEARCH_KIND_LABELS[state["question_kind"]]
    if state["search_query"] != question:
        search = f"{search} → buscada como «{state['search_query']}»"
    pages = ", ".join(dict.fromkeys(str(chunk.metadata["page"]) for chunk in state["chunks"]))
    return f"{search} · Páginas recuperadas: {pages}"


def describe_error(error):
    """Gemini error → friendly message: busy (429 / 503) or anything else."""
    if any(marker in str(error) for marker in BUSY_ERROR_MARKERS):
        return BUSY_ERROR_MESSAGE
    return OTHER_ERROR_MESSAGE


# Agent (copied from the notebook, sections 0, 1.3 and 2.3)
class AgentState(TypedDict):
    """
    State that travels through the graph:
        - messages: the conversation, user questions and agent answers
        - question_kind: first_turn, same_topic or new_topic
        - search_query: the last question, as it is searched in the rulebook
        - chunks: the rulebook chunks retrieved for the last question
    """
    messages: Annotated[list, add_messages]
    question_kind: str
    search_query: str
    chunks: list


class Rewrite(TypedDict):
    """Structured answer of the rewrite: kind of the last question and the question to search."""
    kind: Literal["same_topic", "new_topic"]
    question: str


@st.cache_resource(show_spinner=False)
def get_llm():
    """Gemini chat model with its rate limiter, created once and shared by every conversation."""
    return ChatGoogleGenerativeAI(model=CHAT_MODEL, rate_limiter=InMemoryRateLimiter(requests_per_second=CHAT_REQUESTS_PER_SECOND))


@st.cache_resource(show_spinner=False)
def get_rewriter():
    """Chat model → structured output of the rewrite node."""
    return get_llm().with_structured_output(Rewrite)


@st.cache_resource(show_spinner=False)
def get_vector_store():
    """ChromaDB collection already built by the notebook in CHROMA_DIR."""
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL),
        persist_directory=str(CHROMA_DIR),
    )


@st.cache_resource(show_spinner=False)
def get_agent():
    """Graph START → rewrite → retrieve → generate → END, compiled with an in-memory checkpointer."""
    graph = StateGraph(AgentState)
    graph.add_node("rewrite", rewrite)
    graph.add_node("retrieve", retrieve)
    graph.add_node("generate", generate)
    graph.add_edge(START, "rewrite")
    graph.add_edge("rewrite", "retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)
    return graph.compile(checkpointer=InMemorySaver())


def rewrite(state):
    """Rewrite node: earlier turns + last question → kind + question to search (first turn: unchanged, no Gemini call)."""
    *history, question = state["messages"]
    if not history:
        return {"question_kind": "first_turn", "search_query": question.content}
    prompt = [SystemMessage(REWRITE_PROMPT), HumanMessage(build_rewrite_message(history, question.content))]
    result = get_rewriter().invoke(prompt)
    return {"question_kind": result["kind"], "search_query": result["question"]}


def build_rewrite_message(history, question):
    """Earlier turns as 'Jugador:' / 'Asistente:' lines + the last question."""
    speakers = {"human": "Jugador", "ai": "Asistente"}
    turns = "\n\n".join(f"{speakers[message.type]}: {message.text}" for message in history)
    return f"Conversation:\n\n{turns}\n\nLast question: {question}"


def retrieve(state):
    """Retrieve node: question to search → top RETRIEVAL_K chunks of the rulebook."""
    return {"chunks": get_vector_store().similarity_search(state["search_query"], k=RETRIEVAL_K)}


def generate(state):
    """Generate node: system prompt + earlier turns + note, chunks and question → Gemini answer."""
    *history, question = state["messages"]
    note = build_note(state["question_kind"], question.content, state["search_query"])
    user_message = f"{note}{build_user_message(question.content, state['chunks'])}"
    prompt = [SystemMessage(SYSTEM_PROMPT), *history, HumanMessage(user_message)]
    return {"messages": [get_llm().invoke(prompt)]}


def build_note(question_kind, question, search_query):
    """
    Note before the excerpts, empty if none:
        - new_topic → TOPIC_CHANGE_NOTE
        - same_topic, rewritten → FOLLOW_UP_NOTE with the rewritten question
    """
    if question_kind == "new_topic":
        return f"{TOPIC_CHANGE_NOTE}\n\n"
    if question_kind == "same_topic" and search_query != question:
        return f"{FOLLOW_UP_NOTE.format(question=search_query)}\n\n"
    return ""


def build_user_message(question, chunks):
    """Question + its chunks, each one under a header with its page."""
    excerpts = "\n\n".join(f"[Página {chunk.metadata['page']}]\n{chunk.page_content}" for chunk in chunks)
    return f"Rulebook excerpts:\n\n{excerpts}\n\nQuestion: {question}"


if __name__ == "__main__":
    main()
