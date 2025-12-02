# customer-support-swarm
AI Agent for customer support triage

## Configuration

This project loads configuration from environment variables. For local development, copy `.env.example` to `.env` and fill in values (do not commit `.env` to git).

- `GROQ_API_KEY` — API key for Groq / ChatGroq
- `MODEL_NAME` — Chat model identifier (default: `llama-3.1-70b-instant`)
- `TEMPERATURE` — Sampling temperature (default: `0.2`)

We added `config.py` which reads `.env` and environment variables — import `config.py` from `main.py`.

## Testing

You can run the app in two modes:

- Dry-run / offline mode (no external API calls):
	- Set `TEST_MODE=1` to use a built-in dummy LLM that returns placeholder responses.
	- Example: `TEST_MODE=1 python main.py`.
- Live mode (requires real API keys):
	- Copy `.env.example` to `.env` and add `GROQ_API_KEY` (and `OPENAI_API_KEY` if needed).
	- Example: `python main.py`.

If you see an error about `OPENAI_API_KEY is required`, add an OpenAI key or run in `TEST_MODE=1`.
