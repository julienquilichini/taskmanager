# Task Manager Backend

> **Backend API pour un système de gestion de tâches intelligentes avec agents IA, appels téléphoniques et intégration Telegram.**

---

## 📌 À propos

Ce projet est une API FastAPI qui permet de :
- **Gérer des appels téléphoniques** (entrants/sortants) via Twilio
- **Intégrer des agents IA** (Mistral) pour des conversations vocales et textuelles
- **Envoyer/recevoir des messages** via Telegram
- **Planifier des tâches** avec des LLM (Large Language Models)

---

## ⚙️ Prérequis

- Python **≥ 3.12**
- [UV](https://docs.astral.sh/uv/) (recommandé) ou `pip`
- Un environnement virtuel (optionnel mais recommandé)

---

## 🛠 Installation

### 1. Cloner le dépôt
```bash
cd /chemin/vers/taskmanager/backend
```

### 2. Créer un environnement virtuel
```bash
# Avec UV
uv venv
source .venv/bin/activate  # Linux/macOS
# OU
.venv\Scripts\activate     # Windows

# Avec venv classique
python -m venv .venv
source .venv/bin/activate
```

### 3. Installer les dépendances
```bash
uv pip install -r pyproject.toml
# OU
pip install -r pyproject.toml
```

---

## 🗝 Configuration

### 1. Renommer le fichier `.env`
```bash
cp .env.example .env
```

### 2. Remplir les variables d'environnement dans `.env`

#### **API Keys (LLM)**
```ini
MISTRAL_API_KEY="votre_clé_api_mistral"
OPENAI_API_KEY="votre_clé_api_openai"
TAVILY_API_KEY="votre_clé_api_tavily"
LLM_CLIENT_TOKEN="votre_token_client_llm"
```

#### **Serveurs**
```ini
SERVER_0="votre-domaine-primaire.com"  # Ex: myapp.example.com
SERVER_1="votre-domaine-secondaire.com" # Optionnel
SERVER_2="votre-domaine-tertiaire.com" # Optionnel
```

#### **Twilio (Téléphonie)**
```ini
TWILIO_ACCOUNT_SID="votre_account_sid"
TWILIO_AUTH_TOKEN="votre_auth_token"
TWILIO_PHONE_NUMBER="+1234567890"       # Numéro Twilio
ALLOWED_NUMBERS='["+33123456789", "+33600000000"]'  # Numéros autorisés à appeler
```

#### **Telegram (Messagerie)**
```ini
TELEGRAM_JS_BOT_TOKEN="votre_token_bot_telegram_1"
TELEGRAM_VT_BOT_TOKEN="votre_token_bot_telegram_2"
TELEGRAM_CHAT_ID="votre_chat_id"  # ID du chat ou groupe
```

> ⚠️ **Important** : Sans ces clés, l'application ne pourra pas fonctionner correctement.

---

## 🚀 Démarrage

### Mode développement (avec rechargement automatique)
```bash
uvicorn app.main:app --reload --port 8000
```

### Mode production
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Accéder à l'API
- **URL de base** : `http://localhost:8000`
- **Documentation Swagger** : `http://localhost:8000/docs`
- **Documentation ReDoc** : `http://localhost:8000/redoc`

---

## 📡 Endpoints principaux

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/call/out` | Webhook Twilio pour appels sortants |
| `WS` | `/call/out/ws` | WebSocket pour stream vocal (Twilio) |
| `POST` | `/call/in` | Webhook pour appels entrants |
| `POST` | `/chat` | Envoyer un message via Telegram |
| `POST` | `/llm/planner` | Planification de tâches via LLM |
| `POST` | `/telegram/webhook` | Webhook Telegram |

---

## 🤖 Agents IA

### **VoiceAgent**
- Gère les conversations vocales en temps réel
- Utilise **Mistral Small** comme modèle par défaut
- Peut exécuter des outils (`make_phone_call`, `list_contacts`)
- Configurable via `app/core/agents_instructions.py`

### **BookingAgent**
- Agent spécialisé pour la gestion des appels sortants
- Utilisé pour les réservations et tâches spécifiques
- Peut être réinitialisé avec des instructions contextuelles

---

## 📞 Fonctionnalités téléphoniques

### Appels sortants
1. Twilio appelle un numéro
2. Le webhook (`/call/out`) est déclenché
3. Une connexion WebSocket est établie (`/call/out/ws`)
4. L'audio est streamé en temps réel
5. Le **BookingAgent** répond en fonction des instructions stockées en base

### Appels entrants
- Géré via `/call/in`
- Peut déclencher des actions personnalisées

---

## 🗃 Base de données

### Modèle principal : `OutboundCall`

| Champ | Type | Description |
|-------|------|-------------|
| `id` | INT (PK) | Identifiant unique |
| `call_sid` | STRING (unique) | ID de l'appel Twilio |
| `phone_number` | STRING | Numéro de téléphone appelé |
| `instructions` | TEXT | Instructions pour l'agent IA |
| `context` | TEXT | Contexte supplémentaire |
| `greeting` | TEXT | Message de bienvenue |
| `status` | STRING | Statut (`created`, `answered`, `completed`, etc.) |
| `created_at` | DATETIME | Date de création |
| `updated_at` | DATETIME | Dernière mise à jour |

### Migrations
Le schéma est créé automatiquement au démarrage via SQLAlchemy.

---

## 🛠 Outils disponibles

| Nom | Description |
|-----|-------------|
| `make_phone_call` | Passe un appel téléphonique via Twilio |
| `list_contacts` | Liste les contacts (à implémenter) |

> **Ajouter un outil** :
> 1. Créer un fichier dans `app/tools/`
> 2. Définir la fonction
> 3. L'ajouter dans `app/tools/tools_registry.py`
> 4. Décrire l'outil dans `app/tools/tools_descriptions.py`

---

## 🧪 Tests

### Lancer les tests
```bash
pytest tests/
```

### Tests disponibles
- `tests/websocket.py` : Tests pour le WebSocket Twilio

---

## 📂 Structure du projet

```
backend/
├── app/
│   ├── api/                  # Endpoints FastAPI
│   │   ├── call/             # Appels (entrant/sortant)
│   │   │   ├── incoming.py
│   │   │   └── outgoing.py
│   │   ├── chat.py           # Endpoint Chat
│   │   ├── llm_planner.py    # Planificateur LLM
│   │   └── telegram.py       # Webhook Telegram
│   │
│   ├── agents/               # Agents IA
│   │   ├── __init__.py
│   │   ├── booking_agent.py
│   │   └── voice_agent.py
│   │
│   ├── clients/              # Clients externes
│   │   └── LLM_server_client.py
│   │
│   ├── core/                 # Configuration
│   │   ├── __init__.py
│   │   ├── agents_instructions.py
│   │   └── config.py
│   │
│   ├── db/                   # Base de données
│   │   ├── __init__.py
│   │   ├── engine.py
│   │   ├── models.py
│   │   └── repositories/
│   │       └── outbound_call_repository.py
│   │
│   ├── schemas/              # Schémas Pydantic
│   │   └── chat.py
│   │
│   └── services/             # Services métiers
│       ├── stt.py
│       ├── task_splitter.py
│       └── telegram.py
│
├── tests/                   # Tests
│   └── websocket.py
│
├── .env.example              # Template de configuration
├── .python-version           # Version Python
├── pyproject.toml            # Dépendances
├── README.md                 # Ce fichier
└── main.py                   # Point d'entrée
```

---

## 📜 Licence

Ce projet est **propriétaire**. Tous droits réservés.

---

## 🙌 Contribuer

1. Forker le projet
2. Créer une branche (`git checkout -b feature/ma-fonctionnalité`)
3. Commiter vos changements (`git commit -m 'Ajout de ma fonctionnalité'`)
4. Pousser vers la branche (`git push origin feature/ma-fonctionnalité`)
5. Ouvrir une Pull Request

---

## 📞 Support

Pour toute question ou problème, contactez l'équipe de développement.
