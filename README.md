# Task Manager

Backend API pour gérer des appels téléphoniques via Twilio, des agents IA (Mistral) et des messages Telegram.

---

## Prérequis

- Python ≥ 3.12
- UV ou pip

---

## Installation

```bash
uv venv
source .venv/bin/activate
uv pip install -r pyproject.toml
```

Copier `.env.example` en `.env` et configurer les clés API (Twilio, Mistral, Telegram).

---

## Démarrage

```bash
uvicorn app.main:app --reload --port 8000
```

API disponible sur `http://localhost:8000`
Docs Swagger : `http://localhost:8000/docs`

---

## Endpoints principaux

- `GET /` – Health check
- `POST /call/out` – Appel sortant (Twilio)
- `WS /call/out/ws` – Stream audio
- `POST /call/in` – Appel entrant
- `POST /chat` – Message Telegram
- `POST /llm/planner` – Planificateur de tâches
- `POST /telegram/webhook` – Webhook Telegram

---

## Structure

```
app/
├── api/          # Endpoints
├── agents/       # Agents IA
├── db/           # Base de données
├── tools/        # Outils
└── services/     # Logique métier
```
