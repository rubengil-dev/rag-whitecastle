# White Castle rules assistant

An assistant that answers questions about the rules of the board game **White Castle**, in Spanish, during a game. It uses RAG (retrieval-augmented generation): before answering, it looks up the relevant passages of the official rulebook in a vector store and answers only from them, citing the page. It remembers the conversation, so follow-up questions such as "¿Y luego cómo lo subo?" work.

Final project of the Generative AI module (Evolve data science master). Everything runs in a single notebook: [`white_castle_rag.ipynb`](white_castle_rag.ipynb). As an extra, [`app.py`](app.py) opens the same agent as a web chat in the browser (see [Optional: web chat](#optional-web-chat-streamlit)).

## The domain

White Castle is a board game of dice placement and resource management. Its Spanish rulebook has 20 pages, and many of its rules are short, precise and easy to misremember (costs, limits, the order of the steps of an action), which makes it a good case for an assistant that answers from the source and not from memory.

The rulebook is a **scanned PDF**: every page is a single image, with no text to search. The first step of the notebook turns it into text.

## How it works

| Step | Notebook section | What happens |
|---|---|---|
| PDF → text | 1.1 | Gemini transcribes each page image to Markdown, describing the icons that carry rules (costs, rewards) |
| Text → chunks | 1.2 | The text is cleaned and split by section, then by size (1,000 characters, 150 of overlap). Each chunk keeps its page and section |
| Chunks → vectors | 1.3 | Gemini embeddings (`gemini-embedding-2`), stored in a local ChromaDB collection |
| Search check | 1.4 | 12 test questions with known pages: the right page is among the 5 retrieved chunks in all of them |
| System prompt | 2.1 | Role, answer format and limits of the agent, with the reason for each rule |
| Memory | 2.2 | A checkpointer keeps each conversation, and a rewrite step turns follow-ups into standalone questions before searching |
| Agent | 2.3 | LangGraph graph that rewrites the question, retrieves the 5 closest chunks and answers with Gemini (`gemini-3.5-flash-lite`) |
| Examples and chat | 3 | Seven documented example questions and a chat cell |

The graph:

```
START → rewrite → retrieve → generate → END
```

- **rewrite:** from the second turn on, Gemini classifies the question as the same topic (rewritten so it can be understood on its own, with the rulebook's words) or a new topic (searched as it is).
- **retrieve:** the question to search → the 5 closest chunks of the rulebook.
- **generate:** system prompt + whole conversation + chunks, each under its page → the answer. A short note before the question says when the player changed topic, or what a follow-up means on its own (the rewritten question).

Under every answer, the notebook shows how the question was searched and the pages of the retrieved chunks, so a failed search can be told apart from a failed answer.

## Requirements

- **Python 3.11** (tested with 3.11.9) and Jupyter, for example VS Code with the Jupyter extension.
- **Dependencies:** listed with fixed versions in [`requirements.txt`](requirements.txt): LangChain, LangGraph, ChromaDB, the Gemini integration (`langchain-google-genai`), `pypdf` and `python-dotenv`, plus Streamlit for the optional web chat.
- **A Gemini API key**, free tier. Both models used are free.
- **The rulebook PDF.** It is not in the repository, because it is not clear that it can be shared publicly. It is sent separately and goes in `data/white_castle.pdf`.

## Installation

1. Clone the repository and open a terminal in its folder.
2. Create a virtual environment and install the dependencies:

   Windows (PowerShell):
   ```powershell
   py -3.11 -m venv .venv
   .\.venv\Scripts\python -m pip install -r requirements.txt
   ```

   macOS / Linux:
   ```bash
   python3.11 -m venv .venv
   .venv/bin/python -m pip install -r requirements.txt
   ```

3. **Gemini API key:** create one at [Google AI Studio](https://aistudio.google.com/apikey) ("Create API key"), and save it in a file called `.env` in the project folder, with this single line:
   ```
   GOOGLE_API_KEY=your_key_here
   ```
   The `.env` file is in `.gitignore`, so the key never reaches the repository. The notebook reads it from there and never prints it.
4. Place the rulebook at `data/white_castle.pdf`.

## Running it

Open `white_castle_rag.ipynb`, select the `.venv` kernel and run all the cells, top to bottom.

- **First run:** Gemini transcribes the 20 pages (`data/transcript/`) and the vector store is built (`chroma_db/`). Later runs load both from disk and spend no quota on them.
- **Time:** the free tier allows 15 calls per minute, so every Gemini call is spaced to 12 per minute (`CHAT_REQUESTS_PER_SECOND`). The whole notebook takes about 15 minutes on the first run, mostly the transcription, and about 5 on later runs. Each transcription is slightly different, so the number of chunks and the answers may differ a little from the saved outputs.
- **Chat:** the last cell opens a text box (in VS Code, at the top of the window) to talk to the agent. `nueva` starts a new conversation with no memory of the earlier one, and `salir` or an empty line ends the chat.

The settings live next to the explanation of their values: models and paths in section 0, chunking in 1.2, number of retrieved chunks in 1.4. To rebuild the vector store after changing the cleaning or the chunking, set `REBUILD_VECTOR_STORE = True` once (section 1.3).

## Optional: web chat (Streamlit)

[`app.py`](app.py) is a small web page, running on your own computer, to chat with the same agent in the browser. It is used for the live part of the demo, because it reads better than the notebook's text box. It is an extra: everything that is evaluated is in the notebook.

1. Run the notebook at least once first: the app loads the vector store from `chroma_db/` and does not build it. If it is missing, or the `.env` file is, the page says so.
2. Start it from the project folder:

   Windows (PowerShell):
   ```powershell
   .\.venv\Scripts\streamlit run app.py
   ```

   macOS / Linux:
   ```bash
   .venv/bin/streamlit run app.py
   ```

   It opens in the browser at http://localhost:8501. The first time, Streamlit may ask for an email in the terminal: press Enter to skip it. To stop it, press Ctrl+C in the terminal.

What it does:
- **Answers written as they arrive:** "Consultando el manual…" is shown until Gemini starts answering, and then the answer appears word by word. Under each answer, the same as in the notebook: how the question was searched and the pages of the retrieved chunks.
- **New conversation:** the sidebar (the arrow at the top left) has a "Nueva conversación" button, like `nueva` in the notebook's chat.
- **Friendly errors:** if Gemini is busy (`429` or `503`), a message in the chat asks to wait a moment instead of breaking the page. The full error is printed in the terminal.
- **Japanese-style theme,** like the game: washi paper, vermilion and seigaiha waves, with a rice farmer as the player's avatar and a robot as the assistant's, and no images from the game. The colours and fonts are in [`.streamlit/config.toml`](.streamlit/config.toml), the rest in the page style of `app.py`.

**Why `app.py` copies the agent instead of importing it:** Streamlit runs a `.py` file, and a notebook cannot be imported as a module. Moving the agent to a shared module would have changed the notebook, which is the deliverable, so `app.py` copies only what the agent needs to answer (settings, prompts and graph) and leaves out the transcription, the chunking and the tests. The prompts are the same as in the notebook: a change in one has to be copied to the other.

## System prompt

The system prompt of the agent (section 2.1 of the notebook):

```text
You are an expert on the rules of the board game White Castle. You help players during a game, so your answers are short and clear. Always answer in Spanish.

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
Reply only with "Solo puedo ayudarte con las reglas de White Castle.", with no explanation and no page.
```

These two points sum up the reasons behind it:
- **Role and tone:** an expert on the rules of White Castle who helps players in the middle of a game. They need to settle a doubt and keep playing, so the answers are short: the answer first, then a short paragraph with the reason, then the page where they can check it. It always answers in Spanish, like the rulebook and its players; the prompt itself is in English, which models follow best.
- **What it answers, and with what:** only questions about White Castle, and only with the rulebook excerpts retrieved for each question, never with what the model believes about the game, which may be wrong. When the excerpts do not have the answer, it says "No encuentro esta regla en el manual" and offers a house rule, labelled as unofficial, so the game can go on: with only a few chunks it cannot tell a gap in the rulebook from a failed search, and the sentence is honest about both. Anything outside White Castle gets a fixed reply.

To apply both, the prompt first makes the model decide which kind of question it faces: a rules question, a question that cannot be understood on its own (it asks back instead of guessing), a rule the rulebook does not have, learning to play (one step at a time, waiting for the player) or something outside White Castle. Each kind has its own format. That idea came from the tests: with all the rules in one list, the model cited a page even when it could not answer. For rules questions, it also reads limits literally and deduces answers that follow from the order of the steps, because tricky rules are rarely written word for word.

A second, smaller prompt (`REWRITE_PROMPT`, section 2.2) prepares follow-up questions for the search. It asks for the rulebook's words used in the conversation instead of the player's informal ones ("la sala del Daimio", not "arriba del todo"), and names points by the rulebook's term, "puntos de clan": with the player's words, the search missed the right page.

## Examples

Section 3.1 runs two conversations with seven questions that go through the five kinds of question of the system prompt: a direct rule, a follow-up that only makes sense with the turn before (the memory), a rule that has to be deduced, a rule the rulebook does not have, an off-topic question, the "learning to play" mode, and the same follow-up in a new conversation, where the agent asks what it refers to. The cell after them checks the answers against the rulebook.

The agent was tuned with more tests: harder questions that need several rules at once, and five conversations of up to five turns to test the memory. They are not kept in the notebook, to keep it short, but what they showed is explained next to each decision.

## Technical decisions

- **Transcription with Gemini, one page per request:** the PDF has no text layer, and Gemini reads images, so no OCR is needed. With the whole PDF at once the model tended to summarise and the page of each rule was lost.
- **Chunks by section first, then by size:** a rule is not cut in two, and each chunk starts with its section path, because the embedding only sees the text.
- **5 chunks per question:** with 3, the long version of a test question lost one of its two key chunks.
- **`gemini-3.5-flash-lite` for the chat:** it is free and has enough daily quota for a full run and a live demo. `gemini-3.8-flash` was tried on the questions where Flash-Lite fails: its free tier allows only 20 calls per day (each turn spends two) and it returned `503` errors when Google's servers were busy.
- **Memory in RAM (`InMemorySaver`):** the demo and the review run in a single session, so saving conversations to disk would add a dependency for nothing.

## Known limitations

- **Answers vary between runs:** `gemini-3.5-flash-lite` ignores `temperature`, so the same question can be answered right in one run and wrong in the next, mostly in questions that must be deduced from several rules. In the wrong answers seen, the right pages had been retrieved: the error is in the reasoning, not in the search.
- **The rewrite of follow-ups is not always right:** in each run of the memory tests, about one follow-up out of five was rewritten without a key word, and the search then missed its page.
- **A rule split across two chunks:** the exception of the gardeners in the last round is in a chunk that is not retrieved with the question about them.
- **Free tier:** about 15 calls per minute. The notebook spaces its calls, so it is slow but does not fail.

## Repository

```
white_castle_rag.ipynb   the notebook, with the outputs of its last run
app.py                   optional web chat with the same agent (Streamlit)
.streamlit/config.toml   theme of the web chat
assets/                  avatars of the web chat
requirements.txt         dependencies with fixed versions
data/                    the rulebook PDF and its transcription (not in the repository)
chroma_db/               the local vector store (not in the repository, built on the first run)
.env                     the Gemini API key (not in the repository)
```
