# customer-support-swarm
AI Agent for customer support triage

## Configuration

This project loads configuration from environment variables. For local development, copy `.env.example` to `.env` and fill in values (do not commit `.env` to git).

- `GROQ_API_KEY` — API key for Groq / ChatGroq
- `MODEL_NAME` — Chat model identifier (default: `llama-3.1-70b-instant`)
- `TEMPERATURE` — Sampling temperature (default: `0.2`)

We added `config.py` which reads `.env` and environment variables — import `config.py` from `main.py`.
