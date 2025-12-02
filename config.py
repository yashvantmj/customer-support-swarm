"""
Centralized configuration for the project.
- Reads from a `.env` file (if present) using `python-dotenv`.
- Also reads from environment variables.
"""

from __future__ import annotations
import os
from dotenv import load_dotenv

# Load .env into environment for local dev
load_dotenv()

# Basic config values with defaults where applicable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.1-70b-instant")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))
VERBOSE = os.getenv("VERBOSE", "false").lower() in ("1", "true", "yes")

# Validate required config
if not GROQ_API_KEY:
    # In production, prefer raising an exception so programs fail fast with clear message
    raise EnvironmentError("GROQ_API_KEY is not set. Use .env or environment variables to configure it.")

__all__ = ["GROQ_API_KEY", "MODEL_NAME", "TEMPERATURE", "VERBOSE"]
