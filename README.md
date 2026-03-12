## RAG-AURA Agronomy Chatbot
An intelligent, production-ready AI chatbot that provides natural and context-aware conversations using modern NLP and LLM techniques.​

AURA is designed as an end‑to‑end system: from clean data and modular backend services to an easy‑to‑use chat interface, making it a great showcase project for real‑world AI engineering.

## Table of content
* Overview

* Features

* Architecture

* Tech Stack

## Overview
AURA is a custom chatbot built to demonstrate how to integrate large language models, prompt engineering, and a clean software architecture into a single project.
​
The goal is to go beyond a simple API call and show an interview‑ready implementation: modular code, environment‑based configuration, logging, error handling, and extensibility for new features.
## Features
* Natural, multi‑turn conversation with maintained context.
* Pluggable LLM backend (e.g., Gemini/OpenAI/other providers via a single abstraction layer).
* Clear separation between UI, API, and model logic for easier maintenance and scaling.
* Config‑driven setup using environment variables for keys and secrets.
* Robust error handling and logging for debugging and production readiness.
* Easy to extend with custom tools (e.g., web search, document QA, domain knowledge base)
## Architecture
At a high level, AURA follows a three‑layer architecture:
* UI Layer – chat interface (web/CLI/app) that interacts with users.
* API Layer – backend endpoints for chat, conversation management, and health checks.
* AI Layer – model abstraction, prompt construction, and response post‑processing.

Data flows from the user → UI → API → LLM provider → back through post‑processing → UI, with conversation context stored and reused to maintain coherent dialogue.
## Tech Stack
* Language:  Python

* Backend:  FastAPI / Flask

* Frontend: HTML+CSS

* LLM Provider: Groq

* State/Storage: In‑memory

* Environment & Tools: Conda/venv, Git,

These technologies are commonly used for modern chatbot systems and align with industry practices.
