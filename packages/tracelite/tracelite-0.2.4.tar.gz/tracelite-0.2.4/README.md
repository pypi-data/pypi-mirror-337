# Tracelite

[![PyPI version](https://img.shields.io/pypi/v/tracelite)](https://pypi.org/project/tracelite/)
[![Test](https://github.com/yeongseon/tracelite/actions/workflows/test.yml/badge.svg)](https://github.com/yeongseon/tracelite/actions/workflows/test.yml)

**Lightweight request & response tracing for your Flask, Django, or FastAPI dev server**

Tracelite logs incoming HTTP requests and outgoing responses in a structured format. It's ideal for local development and debugging.

## Features
- 🔍 Logs method, path, status, duration, client IP, headers, body
- ⚙️ Configurable masking and path exclusion (via `tracelite.toml`)
- 📦 SQLite-based local storage
- 📊 Pretty CLI output using `rich`

## Usage
### CLI
```bash
tracelite view
tracelite export --format json
```

### Flask Integration
```python
from flask import Flask
from tracelite.middleware.flask import TraceliteMiddleware
from tracelite.core.storage.sqlite import SQLiteStorage
from tracelite.core.config import load_config

app = Flask(__name__)
config = load_config(app.config)
storage = SQLiteStorage(db_path=config.db_path)

app.wsgi_app = TraceliteMiddleware(app.wsgi_app, storage, config)
```

### FastAPI Integration
```python
from fastapi import FastAPI
from tracelite.middleware.fastapi import TraceliteMiddleware
from tracelite.core.storage.sqlite import SQLiteStorage
from tracelite.core.config import load_config

app = FastAPI()
config = load_config()
storage = SQLiteStorage(db_path=config.db_path)

app.add_middleware(TraceliteMiddleware, storage=storage, config=config)
```

### Django Integration

In your Django `settings.py`, add:

```python
# settings.py
from tracelite.core.config import load_config
from tracelite.core.storage.sqlite import SQLiteStorage

TRACELITE_CONFIG = load_config()
TRACELITE_STORAGE = SQLiteStorage(db_path=TRACELITE_CONFIG.db_path)

MIDDLEWARE = [
    # ... other middleware ...
    "tracelite.middleware.django.TraceliteMiddleware",
]
```

## Configuration (tracelite.toml)
```toml
[tracelite]
enabled = true

[storage]
type = "sqlite"
path = "tracelite.db"

[filter]
exclude_paths = ["/static", "/favicon.ico"]
mask_keys = ["password", "token"]
```


## Development

### 1. Environment Setup

```bash
# Create & activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies (with extras)
make install
```

### 2. Pre-commit Hooks (Optional but Recommended)

```bash
# Install pre-commit hooks
pre-commit install

# Run all hooks manually
pre-commit run --all-files
```

### 3. Common Development Commands

| Command             | Description                           |
|---------------------|---------------------------------------|
| `make venv`         | Create virtualenv                     |
| `make install`      | Install all dependencies              |
| `make test`         | Run tests with coverage report        |
| `make lint`         | Run code linting (black, isort, ruff) |
| `make format`       | Auto format code                      |
| `make build`        | Build package (hatchling)             |
| `make publish`      | Publish to PyPI                       |
| `make clean`        | Remove build artifacts                |

### 4. Run Demo Apps

You can try Tracelite in sample apps:

```bash
# Flask Demo
cd examples/flask_demo
python app.py

# FastAPI Demo
cd examples/fastapi_demo
uvicorn main:app --reload

# Django Demo
cd examples/django_demo
python manage.py runserver
```

### 5. Versioning & Release

- Version is managed in **pyproject.toml**
- Follow **Semantic Versioning (MAJOR.MINOR.PATCH)**
- Create Git tag after version bump:

```bash
git tag v0.1.1
git push origin v0.1.1
```


---

MIT © Yeongseon Choe