# URL Shortener — FastAPI + Supabase + uv

## Prerequisites
- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed

---

## Setup

### 1. Clone & enter the project
```bash
git clone <your-repo>
cd url-shortener
```

### 2. Create virtual environment & install dependencies
```bash
uv sync                  # creates .venv + installs all deps from uv.lock
uv sync --extra dev      # also installs pytest, httpx
```

### 3. Configure environment
```bash
# In the root 'url-shortener' folder
cp .env.example .env
# Edit .env and fill in your SUPABASE_URL, SUPABASE_KEY, BASE_URL
```

### 4. Set up the database
Copy `supabase_schema.sql` (if available) or create the table manually in **Supabase Dashboard → SQL Editor**.

**Required Table: `links`**
| Column | Type | Default |
|---|---|---|
| `id` | uuid | `uuid_generate_v4()` |
| `alias` | text (unique) | |
| `original_url` | text | |
| `click_count` | int4 | 0 |
| `is_custom` | bool | false |
| `created_at` | timestamptz | `now()` |
| `expires_at` | timestamptz | null |

### 5. Start the backend server
From the project root:
```bash
# Set PYTHONPATH so the code can find the 'app' module inside 'backend'
set PYTHONPATH=backend
uv run uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

---

## Common uv commands

| Command | What it does |
|---|---|
| `uv sync` | Install deps, create/update `.venv` |
| `uv add <pkg>` | Add a new dependency |
| `uv add --dev <pkg>` | Add a dev-only dependency |
| `uv run <cmd>` | Run a command inside the venv |
| `PYTHONPATH=backend uv run pytest` | Run tests |

---

## API Reference

| Method | Endpoint             | Description              |
|--------|----------------------|--------------------------|
| POST   | `/shorten`           | Create a short link      |
| GET    | `/{alias}`           | Redirect to original URL |
| GET    | `/analytics/`        | List all links           |
| GET    | `/analytics/{alias}` | Stats for one link       |
| DELETE | `/analytics/{alias}` | Delete a link            |
| GET    | `/health`            | Health check             |

---

## Project Structure
```
url-shortener/
├── backend/             # Python FastAPI service
│   ├── app/
│   │   ├── main.py      # Entry point
│   │   ├── database.py  # Supabase client
│   │   ├── config.py    # Env vars
│   │   ├── models.py    # Pydantic schemas
│   │   ├── utils.py     # Helpers
│   │   └── routes/      # API endpoints
│   └── tests/           # Pytest suite
├── frontend/            # React/Vite UI
├── pyproject.toml       # Backend dependencies
├── .env                 # Secret environment variables
├── .gitignore
└── README.md
```

### 6. Start the frontend
From the project root:
```bash
cd frontend
npm install
npm run dev
```
The frontend will be available at http://localhost:5173
